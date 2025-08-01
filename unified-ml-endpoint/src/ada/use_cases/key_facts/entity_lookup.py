"""Entity Lookup Module

This module performs entity lookups, matching, and abbreviation retrieval
from a database using strategies like vector similarity and fuzzy matching."""

from fuzzywuzzy import process

from ada.components.llm_models.generic_calls import generate_embeddings_from_string
from ada.use_cases.key_facts.pydantic_parsing import DaxEntityValue


class EntityLookup:
    """Handles entity retrieval, abbreviation lookups, and closest matching entity determination
    using raw values and entity types. It supports entities like suppliers, regions, countries,
    continents and plants."""

    def __init__(self, pg_db_conn, category):
        """Initialization"""
        self.db_conn = pg_db_conn
        self.category = category
        self.table_name = "dax_entity_lookup"

    def entity_lookup_data(self, entity_type) -> list[str]:
        """Retrieve a list of entity values from the db for given entity type.

        Parameters:
            entity_type (str): entity type for which to retrieve values.

        Returns:
            list[str]: A list of entity values if found; otherwise, an empty list.
        """
        db_data = self.db_conn.select_records_with_filter(
            table_name=self.table_name,
            filtered_columns=["entity_values"],
            filter_condition=f"entity_name = '{entity_type}'",
        )
        if len(db_data):
            return db_data[0][0]
        return []

    def entity_lookup_abbreviations(self, entity_type="region_abbreviations") -> dict:
        """Retrieve entity abbreviations from the db for given entity type.

        Args:
            entity_type (str): The type of entity for which to retrieve abbreviations.
                            Defaults to "region_abbreviations".

        Returns:
            dict: containing entity abbreviations if found; otherwise,
                an empty dictionary.
        """
        db_data = self.db_conn.select_records_with_filter(
            table_name=self.table_name,
            filtered_columns=["entity_values"],
            filter_condition=f"entity_name = '{entity_type}'",
        )
        if len(db_data):
            return db_data[0][0]
        return {}

    def closest_matching_entity(self, raw_value, entity_type) -> str | None:
        """
        Find the closest matching entity based on the provided raw value and entity type.

        This method searches for the most relevant entity match using
        vector similarity and fuzzy matching.

        Args:
            raw_value (str): The raw input value to be matched against entities.
            entity_type (str): The type of entity to match.

        Returns:
            Union[str, None]: The closest matching entity name if a match is found,
            None otherwise.
            For "supplier", the match is based on cosine distance.
            For regions, countries, continents, and plants, fuzzy matching scores are considered.
        """

        def get_fuzzy_match(entity_type: str, threshold: int = 85) -> str | None:
            lookup_data = self.entity_lookup_data(entity_type)
            if lookup_data:
                match, score = process.extractOne(raw_value, lookup_data)
                if score > threshold:
                    return match
            return None

        if entity_type == "supplier":
            supplier_data = self.db_conn.search_by_vector_similarity(
                table_name="supplier_profile",
                query_emb=generate_embeddings_from_string(raw_value),
                emb_column_name="supplier_name_embedding",
                num_records=1,
                conditions={"LOWER(category_name)": self.category.lower()},
            )
            if supplier_data and supplier_data[0][-1] < 0.15:
                return supplier_data[0][1]
        elif entity_type in ["region", "market_region"]:
            abbreviations_dict = self.entity_lookup_abbreviations("region_abbreviations")
            abbreviations = abbreviations_dict.get(raw_value.upper())
            if abbreviations:
                return ", ".join([f'"{item}"' for item in abbreviations])
            return get_fuzzy_match("region")
        elif entity_type == "company":
            company_levels = [
                "company_level_1",
                "company_level_2",
                "company_level_3",
                "company_level_4",
            ]
            company_lookup_data = sum(
                [self.entity_lookup_data(level) for level in company_levels],
                [],
            )
            if company_lookup_data:
                match, score = process.extractOne(raw_value, company_lookup_data)
                if score > 85:
                    return match
        elif entity_type in ["country", "continent", "plant", "procurement_hub"]:
            return get_fuzzy_match(entity_type)

        return None

    def run_lookup(self, extracted_entities: dict) -> dict:
        """Run lookups for all entities in extracted_entities and returns actual values.

        Args:
        extracted_entities (dict) : contains list of DaxEntityValue objects with only raw entity
        values extracted from dax query.

        Returns:
        actual_entities (dict) : contains list of DaxEntityValue objects with raw entity values
        and actual entity values derived from lookup logic.
        """
        actual_entities = {}
        for key, entity_list in extracted_entities.items():
            updated_entity_list = []
            for dax_entity_obj in entity_list:
                updated_entity_list.append(
                    DaxEntityValue(
                        raw_value=dax_entity_obj.raw_value,
                        actual_value=self.closest_matching_entity(dax_entity_obj.raw_value, key),
                    ),
                )
            if updated_entity_list:
                actual_entities[key] = updated_entity_list
        return actual_entities
