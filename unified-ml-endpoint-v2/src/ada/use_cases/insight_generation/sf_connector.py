import snowflake.connector
import pandas as pd
import os

from typing import Any, Dict, List

class SnowflakeClient:
    def __init__(self, secret_name='Snowflake_sourceai_creds'):
        """
        Initialize the SnowflakeClient with credentials retrieved from secrets.
        """
        self.secret_name = secret_name
        self.conn = self.create_connection()

    def create_connection(self):
        """
        Establish a connection to Snowflake.
        """
        conn = snowflake.connector.connect(
                user= os.environ.get("SF_USERNAME"),
                password=os.environ.get("SF_PASSWORD"),
                account=os.environ.get("SF_ACCOUNT"),
                warehouse=os.environ.get("warehouse"),
                database=os.environ.get("market_database"),
                role=os.environ.get("SF_ROLE"),
                schema=os.environ.get("schema")
        )
        return conn

    def execute_query(self, query,values=None):
        """
        Execute a SQL query on Snowflake and return the result set.
        """
        cursor = self.conn.cursor()
        try:
            if values:
                result = cursor.execute(query,values)
            else:
                cursor.execute(query)
                result = cursor.fetchall()  
            return result
        finally:
            cursor.close()

    def fetch_dataframe(self, query):
        """
        Executes a query on Snowflake and returns the result as a DataFrame.
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            # Fetch the result into a DataFrame
            df = cursor.fetch_pandas_all()
            return df
        finally:
            cursor.close()

    def close_connection(self):
        """
        Close the Snowflake connection.
        """
        self.conn.close()
        
    def select_records_with_filter(
            self, table_name: str,    
            num_records: int = None,
            filtered_columns: list = None,
            filter_condition: str = None,
            distinct: bool = False,
            distinct_on: list[str] = None,
            group_by: list[str] = None,
            order_by: tuple[str, str] = None,
            ) -> tuple[Any] | dict[str, Any]:
     
        """
        Select rows from a table with optional filters and conditions.

        Args:
            table_name (str): Name of the table in the database to query.
            num_records (int, optional): Number of records to limit the response to.
            filtered_columns (list, optional): Columns to select from the table.
            filter_condition (str, optional): SQL string containing a filter condition (e.g., 'id IS NOT NULL').
            distinct (bool, optional): Whether to select distinct records.
            distinct_on (list[str], optional): Columns to apply distinct on.
            group_by (list[str], optional): Columns to group by.
            order_by (tuple[str, str], optional): Column and order direction to sort the output.

        Returns:
            tuple[Any] | dict[str, Any]: Query output.
        """
        if distinct and distinct_on:
            raise ValueError("Parameters 'distinct' and 'distinct_on' cannot be used together.")

        if distinct_on and not order_by:
            raise ValueError("Parameter 'distinct_on' requires 'order_by' to be specified.")

        # Construct the SELECT clause
        select_clause = "SELECT "
        if distinct:
            select_clause += "DISTINCT "
        select_clause += ", ".join(filtered_columns) if filtered_columns else "*"

        # Construct the FROM clause
        from_clause = f"FROM {table_name}"

        # Construct the WHERE clause
        where_clause = f"WHERE {filter_condition}" if filter_condition else ""

        # Construct the GROUP BY clause
        group_by_clause = f"GROUP BY {', '.join(group_by)}" if group_by else ""

        # Construct the ORDER BY clause
        order_by_clause = f"ORDER BY {order_by[0]} {order_by[1]}" if order_by else ""

        # Construct the LIMIT clause
        limit_clause = f"LIMIT {num_records}" if num_records else ""

        # Handle DISTINCT ON using ROW_NUMBER() and QUALIFY in Snowflake
        if distinct_on:
            partition_by = ", ".join(distinct_on)
            order_by_column = order_by[0] if order_by else distinct_on[0]
            order_direction = order_by[1] if order_by else "ASC"
            row_number_clause = (
                f"ROW_NUMBER() OVER (PARTITION BY {partition_by} ORDER BY {order_by_column} {order_direction}) AS row_num"
            )
            select_clause = select_clause.replace("SELECT ", f"SELECT {row_number_clause}, ")
            qualify_clause = "QUALIFY row_num = 1"
        else:
            qualify_clause = ""

        # Combine all clauses into the final query
        query = f"""
            {select_clause}
            {from_clause}
            {where_clause}
            {group_by_clause}
            {order_by_clause}
            {qualify_clause}
            {limit_clause};
        """
        return self.fetch_dataframe(query=query)
    

    def get_tail_spend_supplier_data(  # NOSONAR
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
        table_name  = "DATA.NEGO_SUPPLIER_MASTER"
        tail_spend_query = f"""WITH
            TotalSpends AS (
            SELECT
            SUPPLIER as supplier_name,
            spend_ytd as spend,
            COALESCE(CURRENCY_SYMBOL,'€') AS CURRENCY_SYMBOL,
            percentage_spend_across_category_ytd as percentage_spend_contribution,
            RANK() OVER (
                ORDER BY
                spend_ytd ASC
            ) AS Supplier_Rank,
            SUM(spend_ytd) OVER () AS total_spend
            FROM {table_name} WHERE LOWER(category) = LOWER('{category}') AND
                        YEAR = (SELECT MAX(YEAR) FROM {table_name})),
            CumulativeSpends AS (
            SELECT
            supplier_name,
            spend,
            CURRENCY_SYMBOL,
            percentage_spend_contribution,
            SUM(spend) OVER (
                ORDER BY
                Supplier_Rank ASC
            ) AS cumulative_spend,
            total_spend
            from TotalSpends  
            ),
                TailSpend AS (
                    SELECT
                        supplier_name, CURRENCY_SYMBOL,
                        spend, percentage_spend_contribution,
                        cumulative_spend,
                        total_spend,
                        (cumulative_spend / total_spend) AS cumulative_percentage
                    FROM CumulativeSpends)
        
                SELECT
                    supplier_name, sum(spend) as spend, 100*sum(percentage_spend_contribution) as percentage_spend_contribution,
                    sum(cumulative_percentage) as cumulative_percentage,MAX(CURRENCY_SYMBOL) AS currency_symbol
                FROM
                    TailSpend
                WHERE cumulative_percentage > {tail_threshold}  
                GROUP BY supplier_name 
                ORDER BY cumulative_percentage limit {num_records};"""

        return self.fetch_dataframe(query=tail_spend_query)
    
  
    def get_condition_string(self, cond: tuple[str, str, Any]) -> str:  # NOSONAR
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