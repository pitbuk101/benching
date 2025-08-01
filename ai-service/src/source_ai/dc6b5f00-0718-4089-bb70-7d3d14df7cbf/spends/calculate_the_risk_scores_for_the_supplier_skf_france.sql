WITH RiskScores AS (
    SELECT 
        s.TXT_SUPPLIER AS Supplier,
        SUM(CASE WHEN f.TXT_DESCRIPTION = 'Overall risk score' THEN f.MES_RISK ELSE 0 END) AS Overall_risk_score,
        SUM(CASE WHEN f.TXT_DESCRIPTION = 'Financial risk score' THEN f.MES_RISK ELSE 0 END) AS Financial_risk_score,
        SUM(CASE WHEN f.TXT_DESCRIPTION = 'Reputational risk score' THEN f.MES_RISK ELSE 0 END) AS Reputational_risk_score,
        SUM(CASE WHEN f.TXT_DESCRIPTION = 'Structural risk score' THEN f.MES_RISK ELSE 0 END) AS Structural_risk_score
    FROM 
        Fact supplier risk f
    JOIN 
        Period p ON f.DIM_DATE = p.Date_date
    JOIN 
        Supplier s ON f.DIM_SUPPLIER = s.DIM_SUPPLIER
    WHERE 
        p.YEAR_OFFSET = 0
        AND s.TXT_SUPPLIER = 'SKF FRANCE'
        AND f.TXT_DESCRIPTION IN ('Overall risk score', 'Financial risk score', 'Structural risk', 'Reputational risk score')
    GROUP BY 
        s.TXT_SUPPLIER
)
SELECT 
    Supplier,
    Overall_risk_score,
    Financial_risk_score,
    Reputational_risk_score,
    Structural_risk_score
FROM 
    RiskScores;