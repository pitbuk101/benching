SELECT 
    TXT_COUNTRY As Country, 
    COUNT(*) AS CountryCount
FROM 
    data.vt_dim_suppliercountry
WHERE txt_low_cost_country = 'High cost country'
GROUP BY 
    Country;