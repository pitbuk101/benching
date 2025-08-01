"""Class to connect to Postgres database."""

import os
from typing import Any, Dict, List

import pandas as pd
import psycopg2
import psycopg2.extras
from pgvector.sqlalchemy import Vector
from sqlalchemy import create_engine

# from ada.components.db.azure_connector import AzureConnector
from ada.components.db.db_connector import DBConnector
from ada.utils.config.config_loader import read_config
from ada.utils.io.misc import get_tenant_key_name
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time

log = get_logger("pg_connector")

COMMON_DB_USER = "common-db-user"


# pylint: disable=R0904
class PGConfigException(Exception):
    """Raised when there is config issue of PG connector"""

    def __init__(self, message):
        super().__init__(message)

class PGConnector(DBConnector):
    """Class to connect to Postgres database."""

    @log_time
    def __init__(
        self,
        tenant_id: str,
        credentials_file: str = "pg_credentials.yml",
        cursor_type: str = "tuple",
    ):
        """
        Create a postgres connector object. If this is run locally it will use the PostgrsDB image.
        If it is run on Azure, it will use the Azure function to connect to the Postgres DB.
        """
        # for more cursors: https://www.psycopg.org/docs/extras.html
        if cursor_type == "dict":
            self.__cursor_factory = psycopg2.extras.DictCursor
        elif cursor_type == "real_dict":
            self.__cursor_factory = psycopg2.extras.RealDictCursor
        elif cursor_type == "tuple":
            self.__cursor_factory = None
        else:
            raise PGConfigException(f"The cursor type {cursor_type} is not an option")

        # Overwriting credentials file for local testing if LOCAL_DB_MODE is set to 1 if 0 it will connect to aws hosted db.

        self._tenant_id = tenant_id
        key_name = get_tenant_key_name(tenant_id)

        if int(os.getenv("LOCAL_DB_MODE")) == 1:
            # if we are running locally these are the user, pws
            # credentials = read_config("pg_credentials_local.yml")
            self._connect_to_db(
                user=os.getenv('PGUSER'),
                password=os.getenv("PGPASSWORD", "admin"),
                host=os.getenv('PGHOST'),
                port=os.getenv('PGPORT'),
                database=os.getenv('PGDATABASE'),
            )

        else:
            log.info("Connecting to AWS RDS Postgres")
            log.info("key_name: %s", key_name)
            credentials = read_config('pg_credentials.yml')
            self._connect_to_db(
                user=tenant_id,
                password=os.getenv("PGPASSWORD"),
                host=os.getenv('PGHOST'),
                port=os.getenv('PGPORT'),
                database=os.getenv('PGDATABASE'),
                )
     
            # !! Azure Connector Connecction code ** (Commenting this code since we are moving to AWS postgres)
            #else: 
                #  ** Will be deleted later, once everything works fine in AWS 
                # log.info("AWS DB Connector connection started")
                # azfa_url_details = globals().get("azfa_url_details")

                # if azfa_url_details is None:
                #     azfa_url_details = get_secrets(
                #         secret_names={"azfa_url": "azure-pg-connector-url"},
                #     )
                #     globals()["azfa_url_details"] = azfa_url_details

                # self.__cursor = self.__conn = AzureConnector(
                #     azure_pg_connector_url=azfa_url_details["azfa_url"],
                #     cursor_type=self.__cursor_factory,
                #     tenant_key=key_name,
                #     tenant_id=tenant_id,
                # )
                # log.info("Azure Connector connection completed")

        log.info("Connected to Postgres database.")

    def _connect_to_db(self, **kwargs):
        """Database connection."""
        self.__conn = psycopg2.connect(**kwargs)
        self.__cursor = self.__conn.cursor(cursor_factory=self.__cursor_factory)
        self.alchemy_engine = create_engine(
            f"postgresql+psycopg2://{kwargs['user']}:"
            f"{kwargs['password']}@{kwargs['host']}:"
            f"{kwargs['port']}/{kwargs['database']}",
        )

    @log_time
    def _retrieve_query(
        self,
        query: str,
        values: tuple | None = None,
    ) -> tuple[Any] | dict[str, Any]:
        if values:
            self.__cursor.execute(query, values)
        else:
            self.__cursor.execute(query)
        return self.__cursor.fetchall()

    @log_time
    def _submit_query(self, query: str, values: tuple | None = None) -> None:
        if values:
            self.__cursor.execute(query, values)
        else:
            self.__cursor.execute(query)
        self.__conn.commit()

    def get_condition_string(self, cond: tuple[str, str, Any]) -> str:
        """
        This function help to generate cpg condition string considering
        the special character.

        Args:
            cond(tuple[str, str, Any]): tuple of 3 elements i.e. column name,
                            operator in string format (like in, =, != etc) and values

        Raises:
            ValueError: if the operator in `in` but values are not list/tuple or blank list/tuple

        Returns:
            (str): condition in string format
        """
        column, operator, value = cond
        if operator == "in":
            if not isinstance(value, list) and not isinstance(value, tuple):
                raise ValueError("for operator `in` value must be list or tuple")
            if len(value) == 0:
                raise ValueError("values are empty")
            element_type = type(value[0])
            if element_type == str:
                value = [f"""'{str(element).replace("'", "''")}'""" for element in value]
            cond_string = f"{column} {operator} ({', '.join(map(str, value))})"
            return cond_string
        if operator == "=":
            value_str = str(value) if not isinstance(value, str) else f"'{value}'"
            value_str = f"""'{value_str.replace("'", "''")}'"""
            cond_string = f"{column} = {value_str}"
            return cond_string
        if operator == "ILIKE":
            if len(value) == 0:
                raise ValueError("values are empty")
            value = f"""'{str(value).replace("'", "''")}'"""
            cond_string = f"{column} {operator} {value}"
            return cond_string
        raise ValueError("Operator is not supported yet.")

    def select_records_with_filter(
        self,
        table_name: str,
        num_records: int | None = None,
        filtered_columns: list | None = None,
        filter_condition: str | None = None,
        distinct: bool = False,
        distinct_on: list[str] | None = None,
        group_by: list[str] | None = None,
        order_by: tuple[str, str] | None = None,
    ) -> tuple[Any] | dict[str, Any]:
        """
        Select n rows from table with filtered columns and condition.
        Args:
            distinct: bool if distinct records to be selected
            table_name:  name of table in DB to be queried
            num_records: number of records to limit response by
            filtered_columns: columns to select from the table
            filter_condition: SQL string containing a filter condition e.g. `'id IS NOT NULL' `
            distinct (bool): distinct keyword to allow for a distinct value
            distinct_on (list[str]): distinct on columns
            order_by (tuple[str, str]): return output in sorting order
        Returns: query output

        """
        if distinct and distinct_on:
            raise ValueError("Distinct and distinct_on cannot be used together")
        if distinct_on and not order_by:
            raise ValueError("Distinct on requires order by")
        distinct_str = ""
        if distinct:
            distinct_str = "distinct"
        elif distinct_on:
            distinct_str = f"distinct on ({', '.join(distinct_on)})"
        if group_by:
            group_by_str = f"group by {', '.join(group_by)}"
        query = f"""
                        SELECT {distinct_str}
                        {','.join(filtered_columns) if filtered_columns is not None else '*'}
                        FROM {table_name}
                        {f'where {filter_condition}' if filter_condition is not None else ''}
                        {f'{group_by_str}' if group_by is not None else ''}
                        {f'order by {order_by[0]} {order_by[1]}' if order_by is not None else ''}
                        LIMIT {num_records or 'ALL'};
                    """

        return self._retrieve_query(query=query)

    def upsert_records(
        self,
        table_name: str,
        data: pd.DataFrame,
        key_col_value_map: Dict[str, List],
    ):
        """Upsert records to table"""

        base_delete_query = f"""DELETE from {table_name} where  """

        if not key_col_value_map:
            raise ValueError("Argument key_col_value is empty")

        for col, value in key_col_value_map.items():
            if not value:
                raise ValueError(
                    f""" Argument key_col_value has empty list values for key '{col}' """,
                )

        conditions = []
        for col, value in key_col_value_map.items():
            value_str = "(" + ",".join([str(val) for val in value]) + ")"
            conditions.append(f""" {col} in {value_str} """)

        condition_final = " and ".join(conditions)
        delete_query = base_delete_query + condition_final
        self._submit_query(query=delete_query)

        data.to_sql(
            table_name,
            self.alchemy_engine,
            dtype={"embedding": Vector},
            if_exists="append",
            index=False,
        )

        log.info("Successfully upserted %s", table_name)

    def update_or_insert(self, table_name: str, values: dict[str, Any], conditions: dict[str, Any]):
        """
        Update or insert records in the table based on provided condition and values

        Args:
            table_name (str):  name of table in DB to be queried
            values (dict[str, Any]): records that needs to be inserted or updated
                                    each dict contains column_name (key) and expected value (value)
            conditions (dict[str, Any]) : filter conditions to identify rows to be updated
                                    each dict contains column_name (key) and value
        """
        condition_str = " AND ".join(
            map(
                lambda cv: (
                    f"{cv[0]} = '{cv[1]}'" if isinstance(cv[1], str) else f"{cv[0]} = {cv[1]}"
                ),
                conditions.items(),
            ),
        )
        if len(self.select_records_with_filter(table_name, filter_condition=condition_str)) == 0:
            conditions.update(values)
            self.insert_values_into_columns(
                tuple_with_columns=tuple(conditions),
                list_with_values=list(conditions.values()),
                table_name=table_name,
            )
        else:
            self.update_values(table_name, values, conditions)

    def insert_values_into_columns(self, tuple_with_columns, list_with_values, table_name):
        """
        Insert records into the specified table based on provided columns and values.
        Args:
            tuple_with_columns: Tuple containing column names
            list_with_values: List of tuples, each tuple representing values for insertion
            table_name: Name of the table to insert records into
        """
        if not tuple_with_columns or not list_with_values:
            raise ValueError("Col names or data not available")

        columns_str = ",".join(tuple_with_columns)
        placeholder = ",".join(["%s"] * len(tuple_with_columns))

        query = f"""
            INSERT INTO {table_name} ({columns_str})
            VALUES ({placeholder});
        """
        self._submit_query(query=query, values=list_with_values)
        log.info("Records inserted successfully into %s", table_name)

    def insert_and_return_id(self, tuple_with_columns, values, table_name):
        """
        Insert a record into the specified table based on provided columns and values,
        and return the ID of the last inserted row.
        Args:
            tuple_with_columns: Tuple containing column names
            values: Tuple representing values for insertion
            table_name: Name of the table to insert the record into
        Returns:
            ID of the last inserted row
        """
        if not tuple_with_columns or not values:
            raise ValueError("Column names or data not available")

        columns_str = ",".join(tuple_with_columns)
        placeholder = ",".join(["%s"] * len(tuple_with_columns))

        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholder});"
        self._submit_query(query=query, values=values)
        log.info("Record inserted successfully into %s", table_name)

        # Fetch the last inserted id
        last_inserted_id = self._retrieve_query(f"SELECT MAX(id) from {table_name};")[0][0]
        return last_inserted_id

    def update_component_column(self, table_name: str, new_value: dict, condition: dict) -> None:
        """
        Update a specific column value for a particular identifier in a table.

        Args:
        - table_name (str): The name of the table to update.
        - new_value (dict): Dictionary containing 'column_name' and 'value' for the update.
        - condition (dict): Dictionary containing 'column_name' and 'value' for the condition.

        Returns:
        - None

        """
        update_query = f"""
        UPDATE {table_name} SET {new_value['column_name']} = %s
        WHERE {condition['column_name']} = %s"""

        self._submit_query(query=update_query, values=(new_value["value"], condition["value"]))

    def update_values(self, table_name: str, values: dict, conditions: dict) -> None:
        """
        Update values for conditions in table.

        Args:
        - table_name (str): The name of the table to update.
        - values (dict): Dictionary with column_names as keys and respective values for the update.
        - conditions (dict): Dictionary with column_names as keys and values as conditions.

        Returns:
        - None

        """
        if not values:
            raise ValueError("No values provided for the SET clause in update db")

        if not conditions:
            raise ValueError("No conditions provided for the WHERE clause in update db")
        set_clause = ", ".join(f"{key} = %s" for key in values.keys())
        where_clause = " AND ".join(f"{key} = %s" for key in conditions.keys())

        params = list(values.values()) + list(conditions.values())
        update_query = f"""UPDATE {table_name} SET {set_clause} WHERE {where_clause}"""

        self._submit_query(query=update_query, values=params)

    def delete_values(self, table_name: str, conditions: dict) -> None:
        """
        Delete values for conditions in table.

        Args:
        - table_name (str): The name of the table to delete rows from.
        - conditions (dict): Dictionary containing column_names as keys and values as conditions.

        Returns:
        - None

        """
        if not conditions:
            raise ValueError("No conditions provided for the WHERE clause in update db")
        where_clause = " AND ".join(f"{key} = %s" for key in conditions.keys())
        delete_query = f"""DELETE FROM {table_name} WHERE {where_clause}"""

        self._submit_query(query=delete_query, values=list(conditions.values()))

    def select_component_column(
        self,
        table_name: str,
        column_name: str,
        key_column: str,
        value: str,
    ):
        """Select column value for particular identifier"""
        select_query = f"""
        SELECT {column_name} FROM {table_name}
        WHERE {key_column} = {value}
        """
        return self._retrieve_query(query=select_query)

    def select_document_chunks(self, doc_id: int):
        """Select document chunks table info for particular identifier"""
        select_document_chunks_query = f"""
        SELECT chunk_id, document_id, chunk_content, page, embedding
        FROM combined_document_chunks WHERE document_id = '{doc_id}'
        """
        return self._retrieve_query(query=select_document_chunks_query)

    def close_connection(self):
        """Close the connection."""
        self.__cursor.close()
        self.__conn.close()
        log.info("Postgres connection closed.")

    def select_document_type_summaries(self, document_type: str | list[str]):
        """Select summary chunks table info for a particular document type
        Args:
            document_type (str| list[str]): The document type to filter summary data"""
        not_null_condition = "and summary_embedding IS NOT NULL"
        if isinstance(document_type, list):
            document_type = "', '".join(document_type)
            select_document_type_summaries_query = f"""
                SELECT document_id, summary_embedding
                FROM combined_document_information
                WHERE document_type IN ('{document_type}') {not_null_condition};
            """
        else:
            select_document_type_summaries_query = f"""
                SELECT document_id, summary_embedding
                FROM combined_document_information
                WHERE document_type = '{document_type}' {not_null_condition};
                """

        return self._retrieve_query(query=select_document_type_summaries_query)

    # TODO: Merge it with select_document_chunks after input is updated to a list
    def select_document_chunks_from_doc_list(self, doc_ids: List[str]):
        """Select document chunks table info for list of document ids"""
        select_document_chunks_from_doc_list_query = f"""
            SELECT chunk_content, page, embedding
            FROM combined_document_chunks
            WHERE document_id IN ('{"', '".join(doc_ids)}')
        """
        return self._retrieve_query(query=select_document_chunks_from_doc_list_query)

    def get_data_for_document_from_table(
        self,
        table_name: str,
        columns: List[str],
        doc_id: int,
    ) -> pd.DataFrame:
        """Select columns from table"""
        select_query = (
            f"""SELECT {','.join(columns)} FROM {table_name} WHERE document_id = '{doc_id}'"""
        )
        doc_id_data = self._retrieve_query(query=select_query)
        return pd.DataFrame(doc_id_data, columns=columns)

    def search_by_vector_similarity(
        self,
        table_name: str,
        query_emb: list,
        emb_column_name: str,
        num_records: int | None = None,
        search_type: str = "cosine_distance",
        conditions: dict | str | None = None,
        columns: list[str] | None = None,
    ):
        """
        Perform vector similarity search with pgvector.

        Args:
            table_name: name of table in DB to be queried
            query_emb: query embedding
            emb_column_name: table column name with embeddings
            num_records: number of records to limit response by
            search_type: type of vector comparison, either cosine_distance or l2_distance
            conditions: dict with column_names as keys and values as filtering conditions
            columns: list of columns to select from the table

        Returns:
            search results ordered by distance

        """
        if conditions and isinstance(conditions, dict):
            filtering_str = " AND ".join(f"{key} = %s" for key in conditions.keys())
        if conditions and isinstance(conditions, str):
            filtering_str = conditions

        columns_str = ",".join(columns) if columns else "*"

        if search_type == "cosine_distance":
            search_query = f"""
                SELECT {columns_str}, {emb_column_name} <=> '{str(query_emb)}'::vector AS cosine_distance
                FROM {table_name}
                {f'WHERE {filtering_str}' if conditions else ''}
                ORDER BY cosine_distance
                LIMIT {num_records or 'ALL'};
            """
        elif search_type == "l2_distance":
            search_query = f"""
                SELECT *, {emb_column_name} <-> '{str(query_emb)}'::vector AS l2_distance
                FROM {table_name}
                {f'WHERE {filtering_str}' if conditions else ''}
                ORDER BY l2_distance
                LIMIT {num_records or 'ALL'};
            """
        else:
            raise ValueError("Unknown search type, use cosine_distance or l2_distance.")

        if conditions and isinstance(conditions, dict):
            return self._retrieve_query(query=search_query, values=list(conditions.values()))
        return self._retrieve_query(query=search_query)

    def select_news_chunk_data(
        self,
        source_type: str,
        ksc_name: str,
        date_range=None,
    ) -> list[tuple[int, int, str, str]]:
        """Retrieve news data for a specific source type and date range.
        Args:
            source_type (str): The source type to filter news data (e.g., 'supplier', 'category',
            'keyword').
            ksc_name (str): The name to filter news data.
            date_range (Optional[Dict[str, str]]): A dictionary containing start_date and end_date.
        Returns:
            list[tuple[int, int, str, str]]: DataFrame containing news data for the specified source
            type, name, and date range.
        """
        log.info(
            "KSC name is %s, source is %s, date %s and date %s",
            ksc_name,
            source_type,
            date_range[0],
            date_range[1],
        )
        query = f"""SELECT nc.news_id, nc.chunk_id, nc.news_content_chunk,
                    nc.news_content_chunk_embedding,
                    ns.title, ns.link FROM news_chunks nc JOIN news_store ns ON nc.news_id = ns.id
                    WHERE lower(ns.ksc_name) = lower('{ksc_name}') AND ns.source =
                    '{source_type}'
                    {
            "AND ns.published_date::date BETWEEN '" + date_range[0] + "' AND '" +
            date_range[1] + "'" if date_range else ""
        };"""
        return self._retrieve_query(query=query)

    def select_list_of_ksc_names(self) -> tuple[str, str]:
        """Retrieve distinct values of ksc name column"""
        return self._retrieve_query(query="SELECT distinct KSC_name,source from news_store")

    # sonarignore:start
    def get_tail_spend_supplier_data(
        self,
        table_name: str,
        category: str,
        tail_threshold: float,
        num_records: int,
    ):
        """
        Get tail spend supplier data.

        Args:
            table_name (str): The name of the table containing supplier data.
            category (str): The category name to filter the supplier data.
            tail_threshold (float): The threshold for cumulative percentage to identify tail spend.
            num_records (int): The number of records to retrieve.

        Returns:
            pd.DataFrame: A DataFrame containing the tail spend supplier data.
        """
        tail_spend_query = f"""WITH
        CumulativeSpends AS (
            SELECT
                supplier_name, spend_ytd as spend, reporting_currency,
                percentage_spend_across_category_ytd as percentage_spend_contribution,
                SUM(spend_ytd) OVER (ORDER BY spend_ytd DESC) AS cumulative_spend,
                SUM(spend_ytd) OVER () AS total_spend
                FROM {table_name} WHERE category_name = '{category}' AND
                period = (SELECT MAX(period) FROM {table_name})),
        TailSpend AS (
            SELECT
                supplier_name, reporting_currency,
                spend, percentage_spend_contribution,
                cumulative_spend,
                total_spend,
                cumulative_spend / total_spend AS cumulative_percentage
            FROM CumulativeSpends)
        SELECT
            supplier_name, sum(spend) as spend, 100*sum(percentage_spend_contribution) as percentage_spend_contribution,
              sum(cumulative_percentage) as cumulative_percentage, array_agg(reporting_currency) as currency_symbol
        FROM
            TailSpend
        WHERE
            cumulative_percentage > {tail_threshold} GROUP BY supplier_name
        ORDER BY
            sum(cumulative_percentage) limit {num_records};"""

        return self._retrieve_query(query=tail_spend_query)
    # sonarignore:end

    def execute_query(self, query, return_format="json") -> list[dict] | pd.DataFrame:
        """
        Executes a SQL query and formats the result either as a JSON-like
        list of dict or as a DataFrame.

        Args:
            query (str): The SQL query to be executed.
            return_format (str, optional): The format in which to return the results.
                                    Defaults to "json". If set to "df", returns a Pandas DataFrame.

        Returns:
            list[dict] or pd.DataFrame:
                - If format is "json", returns a list of dict, where each dict
                represents a row of query results.
                - If format is "df", returns the result as a Pandas DataFrame."""
        if return_format == "json":
            if self.__cursor_factory != psycopg2.extras.RealDictCursor:
                raise PGConfigException(
                    """Initialize connection object with real_dict
                                        to get json response""",
                )

        data = self._retrieve_query(query=query)
        if return_format == "df":
            return pd.DataFrame(data)
        return data

    def search_contract_doc_content_user_query(self, questions):
        """
        Executes a vector search query to zero in on any document
          id if the question is related to any contract
        Args:
        qustions list of user queries

        """
        ts_vector_questions_list = []
        for question in questions:
            any_match_query = "|".join(question.split(" "))
            ts_vector_questions_list.append(any_match_query)

        ts_vector_questions = "|".join(ts_vector_questions_list)
        document_id_serach_query = f"""
        SELECT document_id from document_information
        WHERE  lower(document_type)='contract' AND
        to_tsvector('english', content) @@ to_tsquery('{ts_vector_questions.replace("'", '')}') limit 1;
        """
        retrived_document_values = self._retrieve_query(query=document_id_serach_query)

        return (
            (retrived_document_values[0][0])
            if (
                isinstance(retrived_document_values, list)
                and isinstance(retrived_document_values[0], list)
            )
            else None
        )

    def document_exists_by_column(self, col_name: str, document_value: str):
        """
        Checks if the document exists by document name

        Args:
           document_name(str): The name of the doument.
        """
        schema_name = "common." if (self._tenant_id == COMMON_DB_USER) else ""

        document_exists_query = f"""
            SELECT count(1) FROM {schema_name}document_information where {col_name} = %s
        """
        is_document_exists = self._retrieve_query(document_exists_query, (document_value,))[0][0]
        return is_document_exists

    def remove_document_by_column(self, col_name: str, document_value: str):
        """
        Removes the document information from the document information table
        as the doc chunks is the cascaded table it will also remove the data from
        dock chunks table

        Args:
           document_name(str): The name of the doument should be used to delete a document
        """
        schema_name = "common." if (self._tenant_id == COMMON_DB_USER) else ""

        delete_query = f"""
            DELETE FROM {schema_name}document_information where {col_name} = %s
        """
        self._submit_query(delete_query, (document_value,))
