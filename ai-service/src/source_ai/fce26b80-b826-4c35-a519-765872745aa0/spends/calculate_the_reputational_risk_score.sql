WITH FilteredData AS (
    SELECT 
        MES_RISK, 
        TXT_DESCRIPTION
    FROM 
        Fact supplier risk
    WHERE 
        TXT_DESCRIPTION = 'Reputational risk score' 
        AND MES_RISK IS NOT NULL
),
AggregatedData AS (
    SELECT 
        SUM(MES_RISK) AS TotalRisk, 
        COUNT(*) AS RiskCount
    FROM 
        FilteredData
)
SELECT 
    TotalRisk, 
    RiskCount
FROM 
    AggregatedData;