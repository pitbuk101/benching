WITH FactInvoicePosition AS (
    SELECT
        Date_dim,
        DIM_CURRENCY_COMPANY,
        DIM_MATERIAL,
        DIM_UOM,
        MPV_flag,
        MES_SPEND_CURR_1,
        MES_QUANTITY
    FROM
        Fact invoice position
),
Period AS (
    SELECT
        DIM_DATE,
        TXT_YEAR
    FROM
        Period
),
FilteredFactInvoicePosition AS (
    SELECT
        fip.Date_dim,
        fip.DIM_CURRENCY_COMPANY,
        fip.DIM_MATERIAL,
        fip.DIM_UOM,
        fip.MES_SPEND_CURR_1,
        fip.MES_QUANTITY,
        p.TXT_YEAR
    FROM
        FactInvoicePosition fip
    JOIN
        Period p ON fip.Date_dim = p.DIM_DATE
    WHERE
        fip.MPV_flag = 'Y'
),
AggregatedData AS (
    SELECT
        TXT_YEAR,
        DIM_CURRENCY_COMPANY,
        DIM_MATERIAL,
        DIM_UOM,
        SUM(MES_SPEND_CURR_1) AS TotalSpend,
        SUM(MES_QUANTITY) AS TotalQuantity
    FROM
        FilteredFactInvoicePosition
    GROUP BY
        TXT_YEAR,
        DIM_CURRENCY_COMPANY,
        DIM_MATERIAL,
        DIM_UOM
)
SELECT
    TXT_YEAR,
    DIM_CURRENCY_COMPANY,
    DIM_MATERIAL,
    DIM_UOM,
    TotalSpend,
    TotalQuantity
FROM
    AggregatedData
AggregatedData        -- Add more tuples as needed
    );
