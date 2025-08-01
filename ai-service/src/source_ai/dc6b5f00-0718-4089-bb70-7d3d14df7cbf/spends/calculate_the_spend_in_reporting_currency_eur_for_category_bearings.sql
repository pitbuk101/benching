WITH ReportingCurrencySpend AS (
    SELECT
        rc.TXT_REPORTING_CURRENCY,
        SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM
        Fact invoice position fip
    LEFT OUTER JOIN
        Period p ON fip.Date_dim = p.DIM_DATE
    LEFT OUTER JOIN
        Supplier status ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
    LEFT OUTER JOIN
        Value type vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
    LEFT OUTER JOIN
        Category tree ct ON fip.DIM_SOURCING_TREE = ct.DIM_SOURCING_TREE
    LEFT OUTER JOIN
        Reporting currency rc ON fip.DIM_REPORTING_CURRENCY = rc.DIM_REPORTING_CURRENCY
    WHERE
        p.YEAR_OFFSET = 0 AND
        ss.DIM_SUPPLIER_STATUS = 'E' AND
        vt.DIM_VALUE_TYPE = 'I' AND
        ct.TXT_CATEGORY_LEVEL_2 = 'Bearings' AND
        rc.TXT_REPORTING_CURRENCY = 'EUR'
    GROUP BY
        rc.TXT_REPORTING_CURRENCY
)
SELECT * FROM ReportingCurrencySpend;