WITH
  Last4MonthsSpends AS
  (
    SELECT
      s.TXT_CONS_SUPPLIER_L1,
      to_date(p.DIM_DATE,'YYYYMMDD') AS DIM_DATE,
      SUM(f.MES_SPEND_CURR_1) AS TotalSpend
    FROM
      DATA.VT_C_FACT_INVOICEPOSITION_MULTIPLIED AS f
      JOIN DATA.VT_DIM_Period AS p ON f.DIM_DATE = p.DIM_DATE
      JOIN DATA.VT_C_DIM_Supplier AS s ON f.DIM_SUPPLIER = s.DIM_SUPPLIER
    WHERE
      year(to_date(p.DIM_DATE,'YYYYMMDD')) = '2022'
      AND to_date(p.DIM_DATE,'YYYYMMDD') >= '2022-09-01'
      AND to_date(p.DIM_DATE,'YYYYMMDD') <= '2022-12-31'
    GROUP BY
      s.TXT_CONS_SUPPLIER_L1,
      p.DIM_DATE
  ),
  MinSpendsPerSupplier AS
  (
    SELECT
      a.TXT_CONS_SUPPLIER_L1,
      a.MIN_DIM_DATE,
      b.TotalSpend AS MinSpend
    FROM
      (
        SELECT
          TXT_CONS_SUPPLIER_L1,
          MIN(DIM_DATE) AS MIN_DIM_DATE
        FROM
          Last4MonthsSpends
        GROUP BY
          TXT_CONS_SUPPLIER_L1
      ) AS a
      JOIN Last4MonthsSpends AS b ON a.TXT_CONS_SUPPLIER_L1 = b.TXT_CONS_SUPPLIER_L1
      AND a.MIN_DIM_DATE = b.DIM_DATE
  ),
  MaxSpendsPerSupplier AS
  (
    SELECT
      a.TXT_CONS_SUPPLIER_L1,
      a.MAX_DIM_DATE,
      b.TotalSpend AS MaxSpend
    FROM
      (
        SELECT
          TXT_CONS_SUPPLIER_L1,
          MAX(DIM_DATE) AS MAX_DIM_DATE
        FROM
          Last4MonthsSpends
        GROUP BY
          TXT_CONS_SUPPLIER_L1
      ) AS a
      JOIN Last4MonthsSpends AS b ON a.TXT_CONS_SUPPLIER_L1 = b.TXT_CONS_SUPPLIER_L1
      AND a.MAX_DIM_DATE = b.DIM_DATE
  ),
  ChangeInSpendTable AS
  (
    SELECT
      a.TXT_CONS_SUPPLIER_L1 AS SupplierName,
      a.MIN_DIM_DATE AS MinSpendDate,
      ROUND(a.MinSpend, 2) AS MinimumSpend,
      b.MAX_DIM_DATE AS MaxSpendDate,
      ROUND(b.MaxSpend, 2) AS MaximumSpend,
      ROUND(
        (
          (b.MaxSpend - a.MinSpend) / a.MinSpend
        ) * 100,
        2
      ) AS ChangeInSpend
    FROM
      MinSpendsPerSupplier AS a
      JOIN MaxSpendsPerSupplier AS b ON a.TXT_CONS_SUPPLIER_L1 = b.TXT_CONS_SUPPLIER_L1
    WHERE
      a.MinSpend > 0
  )
SELECT
  SupplierName,
  MinSpendDate,
  MinimumSpend,
  MaxSpendDate,
  MaximumSpend,
  CONCAT(CAST(ChangeInSpend AS VARCHAR), ' %') AS PercentageChangeInSpend
FROM
  ChangeInSpendTable
ORDER BY
  ChangeInSpend DESC;
