WITH OEM_Spend AS (
    SELECT SUM(t1.MES_SPEND_CURR_1) as total_oem_spend, TXT_CONS_SUPPLIER_L1, t2.dim_supplier
    FROM data.VT_FACT_InvoicePosition_multiplied t1
	join data.VT_C_DIM_Supplier t2 on t1.DIM_SUPPLIER = t2.DIM_SUPPLIER
    WHERE t2.TXT_OEM_TYPE = 'OEM'
    group by TXT_CONS_SUPPLIER_L1, t2.dim_supplier
),
total_spend AS (
    SELECT SUM(MES_SPEND_CURR_1) as total_spend, t2.dim_supplier
    FROM data.VT_FACT_InvoicePosition_multiplied t1
    join data.VT_C_DIM_Supplier t2 on t1.DIM_SUPPLIER = t2.DIM_SUPPLIER
    group by t2.dim_supplier
),
base_calculations AS (
    SELECT 
    	TXT_CONS_SUPPLIER_L1 as supplier,
        oe.total_oem_spend,
        ts.total_spend,
        CASE 
            WHEN (oe.total_oem_spend - (ts.total_spend * 0.4)) < 0 THEN 0 
            ELSE (oe.total_oem_spend - (ts.total_spend * 0.4))
        END as oem_benchmark_saving
    FROM OEM_Spend oe
    inner JOIN total_spend ts
    on oe.dim_supplier = ts.dim_supplier
),
benchmark_value AS (
    SELECT 
    	supplier,
        total_oem_spend,
        total_spend,
        oem_benchmark_saving,
        (oem_benchmark_saving * 0.3) as abs_value
    FROM base_calculations
)
SELECT 
0
	supplier,
    ROUND(total_oem_spend,2) as OEM Spend,
    ROUND(total_spend,2) as Total Spend,
    ROUND(oem_benchmark_saving,2) as OEM Benchmark Saving,
    ROUND(abs_value,2) as Absolute Value,
    CONCAT(
        FORMAT(
            ROUND(abs_value / 1000000.0, 1),
            '##,###0.0'
        ),
        'M (',
        CAST(
            ROUND(
                (100 * abs_value / NULLIF(total_spend, 0)), 
                1
            ) 
        AS VARCHAR),
        '%)'
    ) AS OEM Benchmark Value Formatted
FROM benchmark_value
ORDER BY OEM Benchmark Value Formatted DESC;