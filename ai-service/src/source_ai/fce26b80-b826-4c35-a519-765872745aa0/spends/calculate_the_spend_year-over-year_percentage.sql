WITH Period_CTE AS (
    SELECT DIM_DATE
    FROM Period
),
Value_Type_CTE AS (
    SELECT DIM_VALUE_TYPE
    FROM Value type
),
Reporting_Currency_CTE AS (
    SELECT DIM_REPORTING_CURRENCY
    FROM Reporting currency
),
Fact_Invoice_Position_CTE AS (
    SELECT SUM(MES_SPEND_CURR_1) AS Total_Spend
    FROM Fact invoice position
    LEFT OUTER JOIN Period ON Fact invoice position.Date_dim = Period.DIM_DATE
    WHERE Period.DIM_DATE IN (44905, 44946, 44987, 45028, 45069, 45110, 45151, 44577, 44618, 44659)
)
SELECT Total_Spend
FROM Fact_Invoice_Position_CTE;