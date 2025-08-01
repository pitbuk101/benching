
WITH
  July2023Spends AS
  (
    SELECT
      "s"."TXT_CONS_SUPPLIER_L1",
      CAST("p"."DIM_DATE" AS DATE) "DIM_DATE",
      SUM("f"."MES_SPEND_CURR_1") AS "TotalSpend"
    FROM
      "DATA"."VT_FACT_InvoicePosition" AS "f"
      JOIN "DATA"."VT_DIM_Period" AS "p" ON "f"."DIM_DATE" = "p"."DIM_DATE"
      JOIN "DATA"."VT_DIM_Supplier" AS "s" ON "f"."DIM_SUPPLIER" = "s"."DIM_SUPPLIER"
    WHERE
      "p"."DIM_YEAR" = '2023'
      AND "p"."MONTH_NUMBER" = 7
    GROUP BY
      "s"."TXT_CONS_SUPPLIER_L1",
      "p"."DIM_DATE"
  ),
  MinSpendsPerSupplier AS
  (
    SELECT
      "a"."TXT_CONS_SUPPLIER_L1",
      "a"."MIN_DIM_DATE",
      "b"."TotalSpend" AS "MinSpend"
    FROM
    (
      SELECT
        "TXT_CONS_SUPPLIER_L1",
        MIN("DIM_DATE") AS "MIN_DIM_DATE"
      FROM
        "July2023Spends"
      GROUP BY
        "TXT_CONS_SUPPLIER_L1"
    ) as "a"
    JOIN "July2023Spends" as "b" ON "a"."TXT_CONS_SUPPLIER_L1" = "b"."TXT_CONS_SUPPLIER_L1" and "a"."MIN_DIM_DATE" = "b"."DIM_DATE"
  ),
  MaxSpendsPerSupplier AS
  (
    SELECT
      "a"."TXT_CONS_SUPPLIER_L1",
      "a"."MAX_DIM_DATE",
      "b"."TotalSpend" AS "MaxSpend"
    FROM
    (
      SELECT
        "TXT_CONS_SUPPLIER_L1",
        MAX("DIM_DATE") AS "MAX_DIM_DATE"
      FROM
        "July2023Spends"
      GROUP BY
        "TXT_CONS_SUPPLIER_L1"
    ) as "a"
    JOIN "July2023Spends" as "b" ON "a"."TXT_CONS_SUPPLIER_L1" = "b"."TXT_CONS_SUPPLIER_L1" and "a"."MAX_DIM_DATE" = "b"."DIM_DATE"
  ),
ChangeInSpendTable AS (
	SELECT
	  "a"."TXT_CONS_SUPPLIER_L1" "SupplierName",
	  "a"."MIN_DIM_DATE" AS "MinSpendDate",
	  ROUND("a"."MinSpend",2) "MinimumSpend",
	  "b"."MAX_DIM_DATE" AS "MaxSpendDate",
	  ROUND("b"."MaxSpend",2) "MaximumSpend",
	  ROUND(((("b"."MaxSpend" - "a"."MinSpend") /"a"."MinSpend"))*100 ,2) AS "ChangeInSpend"
	FROM
	  "MinSpendsPerSupplier" as "a"
	JOIN "MaxSpendsPerSupplier" as "b" ON "a"."TXT_CONS_SUPPLIER_L1" = "b"."TXT_CONS_SUPPLIER_L1"
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
ORDER BY ChangeInSpend DESC
LIMIT 1