WITH IncotermSpend AS (
    SELECT
        i.TXT_INCOTERM,
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM
        Fact invoice position fip
    JOIN
        Period p ON fip.Date_dim = p.DIM_DATE
    JOIN
        Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    JOIN
        Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    JOIN
        Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    JOIN
        Incoterm i ON fip.DIM_INCOTERM = i.DIM_INCOTERM
    JOIN
        Reporting currency rc ON fip.DIM_REPORTING_CURRENCY = rc.DIM_REPORTING_CURRENCY
    WHERE
        p.YEAR_OFFSET = 0
        AND ss.DIM_SUPPLIER_STATUS = 'E'
        AND vt.DIM_VALUE_TYPE = 'I'
        AND ct.TXT_CATEGORY_LEVEL_2 = 'Bearings'
        AND i.TXT_INCOTERM = 'Delivered at Place'
        AND rc.DIM_REPORTING_CURRENCY = 'CURR_1'
    GROUP BY
        i.TXT_INCOTERM
)
SELECT * FROM IncotermSpend;