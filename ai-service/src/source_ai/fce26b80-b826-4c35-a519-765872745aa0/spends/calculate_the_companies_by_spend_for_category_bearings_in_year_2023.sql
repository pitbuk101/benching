WITH CompanySpend AS(
SELECT
  c.TXT_LEVEL_4 AS Company,
  SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
FROM
  data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED AS fip
  JOIN data.VT_DIM_Company AS c ON fip.DIM_COMPANY = c.DIM_COMPANY
  JOIN data.VT_DIM_Period AS p ON fip.DIM_DATE = p.DIM_DATE
  JOIN data.VT_DIM_SupplierStatus AS ss ON fip.DIM_SUPPLIER_STATUS = ss.DIM_SUPPLIER_STATUS
  JOIN data.VT_C_DIM_ValueType AS vt ON fip.dim_value_type = vt.DIM_VALUE_TYPE
  JOIN data.VT_C_DIM_SourcingTree_TECHCME vcdstt  ON vcdstt.DIM_SOURCING_TREE = fip.DIM_SOURCING_TREE 
WHERE  LOWER(ss.DIM_SUPPLIER_STATUS) = LOWER('E')
  AND LOWER(vt.DIM_VALUE_TYPE) = LOWER('I')
  AND LOWER(vcdstt.TXT_CATEGORY_LEVEL_2) = lower('Bearings')
  AND YEAR(p.DIM_DATE) = '2023'
GROUP BY
  c.TXT_LEVEL_4
)
SELECT 
  Company,
  TotalSpend
FROM
  CompanySpend
ORDER BY
  TotalSpend DESC