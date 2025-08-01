WITH
  PlantSpend AS
  (
    SELECT
      p.TXT_PLANT AS PlantName,
      TO_DATE(pr.DIM_DATE, 'YYYYMMDD') AS DIM_DATE,
      SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM
      data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED AS fip
      JOIN data.VT_DIM_Plant AS p ON fip.DIM_PLANT = p.DIM_PLANT
      JOIN data.VT_DIM_Period AS pr ON fip.DIM_DATE = pr.DIM_DATE
    WHERE
      TO_DATE(pr.DIM_DATE, 'YYYYMMDD') BETWEEN TO_DATE('20221001', 'YYYYMMDD') AND TO_DATE('20221231', 'YYYYMMDD')
    GROUP BY
      p.TXT_PLANT,
      TO_DATE(pr.DIM_DATE, 'YYYYMMDD')
  ),
  LastQuarterSpend AS
  (
    SELECT
      p.TXT_PLANT AS PlantName,
      TO_DATE(pr.DIM_DATE, 'YYYYMMDD') AS DIM_DATE,
      SUM(fip.MES_SPEND_CURR_1) AS TotalSpend
    FROM
      data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED AS fip
      JOIN data.VT_DIM_Plant AS p ON fip.DIM_PLANT = p.DIM_PLANT
      JOIN data.VT_DIM_Period AS pr ON fip.DIM_DATE = pr.DIM_DATE
    WHERE
      TO_DATE(pr.DIM_DATE, 'YYYYMMDD') BETWEEN DATEADD(MONTH, -3, TO_DATE('20221001', 'YYYYMMDD')) AND DATEADD(MONTH, -3, TO_DATE('20221231', 'YYYYMMDD'))
    GROUP BY
      p.TXT_PLANT,
      TO_DATE(pr.DIM_DATE, 'YYYYMMDD')
  ),
  PlantSpendChange AS
  (
    SELECT
      ps.PlantName,
      ps.DIM_DATE AS CurrentSpendDate,
      ps.TotalSpend - COALESCE(lq.TotalSpend, 0) AS SpendChange,
      lq.DIM_DATE AS LastQuarterSpendDate
    FROM
      PlantSpend AS ps
      LEFT JOIN LastQuarterSpend AS lq ON ps.PlantName = lq.PlantName
  )
SELECT
  PlantName,
  CurrentSpendDate,
  LastQuarterSpendDate,
  SpendChange
FROM
  PlantSpendChange
ORDER BY
  SpendChange DESC;
