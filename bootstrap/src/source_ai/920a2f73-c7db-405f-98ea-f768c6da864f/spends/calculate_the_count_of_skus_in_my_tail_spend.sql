WITH
  TotalSpend AS (
    SELECT
      SUM(MES_SPEND_CURR_1) AS TotalSpend
    FROM
      data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
    JOIN data.VT_DIM_Period per
    ON per.DIM_DATE = fip.DIM_DATE
    WHERE YEAR(TO_DATE(per.DIM_DATE, 'YYYYMMDD'))=YEAR(CAST('2023' AS DATE))
  ),
  RankedSuppliers AS
  (
    SELECT
      DIM_SUPPLIER,
      DIM_MATERIAL,
      COUNT(DIM_MATERIAL) AS MaterialCount,
      SUM(MES_SPEND_CURR_1) AS SupplierSpend,
      RANK() OVER (
        ORDER BY
          SUM(MES_SPEND_CURR_1) ASC
      ) AS SupplierRank
    FROM data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED fip
    JOIN data.VT_DIM_Period per
    ON per.DIM_DATE = fip.DIM_DATE
    WHERE YEAR(TO_DATE(per.DIM_DATE, 'YYYYMMDD'))=YEAR(CAST('2023' AS DATE))
    GROUP BY
      DIM_SUPPLIER,
      DIM_MATERIAL
  ),
  CumulativeSpend AS
  (
    SELECT
      DIM_SUPPLIER,
      DIM_MATERIAL,
      SupplierSpend,
      MaterialCount,
      SUM(SupplierSpend) OVER (
        ORDER BY
          SupplierRank ASC
      ) AS CumulativeSpend
    FROM
      RankedSuppliers
  ),
tail_spend AS (SELECT
  DIM_SUPPLIER,
  DIM_MATERIAL,
  MaterialCount,
  SupplierSpend
FROM
  CumulativeSpend,
  TotalSpend
WHERE
  CumulativeSpend.CumulativeSpend <= 0.2 * TotalSpend.TotalSpend
)
SELECT sup.TXT_CONS_SUPPLIER_L1 AS Supplier,
	m.TXT_MATERIAL AS Material,
      MaterialCount,
      SupplierSpend
FROM tail_spend AS ts
JOIN data.VT_C_DIM_Supplier AS sup
ON sup.DIM_SUPPLIER = ts.DIM_SUPPLIER
JOIN data.VT_C_DIM_Material  AS m
ON m.DIM_MATERIAL = ts.DIM_MATERIAL