
WITH
  "July2023Spends" AS
  (
    SELECT
      "s"."TXT_SUPPLIER",
      TO_DATE("p"."DIM_DATE", 'YYYYMMDD') "DIM_DATE",
      SUM("f"."MES_SPEND_CURR_1") AS "TotalSpend"
    FROM
      "DATA"."VT_C_FACT_INVOICEPOSITION_MULTIPLIED" AS "f"
      JOIN "DATA"."VT_DIM_PERIOD" AS "p" ON "f"."DIM_DATE" = "p"."DIM_DATE"
      JOIN "DATA"."VT_C_DIM_SUPPLIER" AS "s" ON "f"."DIM_SUPPLIER" = "s"."DIM_SUPPLIER"
    WHERE
      YEAR(TO_DATE("p"."DIM_DATE", 'YYYYMMDD')) = 2023
      AND MONTH(TO_DATE("p"."DIM_DATE", 'YYYYMMDD')) = 7
    GROUP BY
      "s"."TXT_SUPPLIER",
      "p"."DIM_DATE"
  ),
  "MinSpendsPerSupplier" AS
  (
    SELECT
      "a"."TXT_SUPPLIER",
      "a"."MIN_DIM_DATE",
      "b"."TotalSpend" AS "MinSpend"
    FROM
    (
      SELECT
        "TXT_SUPPLIER",
        MIN("DIM_DATE") AS "MIN_DIM_DATE"
      FROM
        "July2023Spends"
      GROUP BY
        "TXT_SUPPLIER"
    ) as "a"
    JOIN "July2023Spends" as "b" ON "a"."TXT_SUPPLIER" = "b"."TXT_SUPPLIER" and "a"."MIN_DIM_DATE" = "b"."DIM_DATE"
  ),
  "MaxSpendsPerSupplier" AS
  (
    SELECT
      "a"."TXT_SUPPLIER",
      "a"."MAX_DIM_DATE",
      "b"."TotalSpend" AS "MaxSpend"
    FROM
    (
      SELECT
        "TXT_SUPPLIER",
        MAX("DIM_DATE") AS "MAX_DIM_DATE"
      FROM
        "July2023Spends"
      GROUP BY
        "TXT_SUPPLIER"
    ) as "a"
    JOIN "July2023Spends" as "b" ON "a"."TXT_SUPPLIER" = "b"."TXT_SUPPLIER" and "a"."MAX_DIM_DATE" = "b"."DIM_DATE"
  ),
"ChangeInSpendTable" AS (
	SELECT
	  "a"."TXT_SUPPLIER" "SupplierName",
	  "a"."MIN_DIM_DATE" AS "MinSpendDate",
	  ROUND("a"."MinSpend",2) "MinimumSpend",
	  "b"."MAX_DIM_DATE" AS "MaxSpendDate",
	  ROUND("b"."MaxSpend",2) "MaximumSpend",
	  ROUND(((("b"."MaxSpend" - "a"."MinSpend") /"a"."MinSpend"))*100 ,2) AS "ChangeInSpend"
	FROM
	  "MinSpendsPerSupplier" as "a"
	JOIN "MaxSpendsPerSupplier" as "b" ON "a"."TXT_SUPPLIER" = "b"."TXT_SUPPLIER"
	WHERE "a"."MinSpend" > 0
)
SELECT
	"SupplierName",
	"MinSpendDate",
	"MinimumSpend",
	"MaxSpendDate",
	"MaximumSpend",
	CONCAT(CAST("ChangeInSpend" AS VARCHAR ), ' %') AS "PercentageChangeInSpend"
FROM "ChangeInSpendTable"
ORDER BY "ChangeInSpend" DESC