WITH Early_Payments AS (
    SELECT 
        Fact payment.MES_DIFF_EARLY_PAYMENT,
        SUM(CASE WHEN PFDATAID(Fact payment.MES_INTEGER) <> 2 THEN 1 ELSE 0 END) AS Measure0,
        SUM(Fact payment.MES_DIFF_EARLY_PAYMENT) AS Measure1
    FROM 
        Fact payment
    LEFT OUTER JOIN 
        Period ON Fact payment.Date_dim = Period.DIM_DATE
    LEFT OUTER JOIN 
        Supplier status ON Fact payment.dim_supplier_status = Supplier status.DIM_SUPPLIER_STATUS
    LEFT OUTER JOIN 
        Value type ON Fact payment.dim_value_type = Value type.DIM_VALUE_TYPE
    LEFT OUTER JOIN 
        Category tree ON Fact payment.DIM_SOURCING_TREE = Category tree.DIM_SOURCING_TREE
    LEFT OUTER JOIN 
        Payment term ON Fact payment.dim_payment_term = Payment term.DIM_PAYMENT_TERM
    WHERE 
        Period.YEAR_OFFSET = 0 AND
        Supplier status.DIM_SUPPLIER_STATUS = 'E' AND
        Value type.DIM_VALUE_TYPE = 'P' AND
        Category tree.TXT_CATEGORY_LEVEL_2 = 'Bearings' AND
        Payment term.TXT_PAYMENT_TERM_TYPE = 'Net payment'
    GROUP BY 
        Fact payment.MES_DIFF_EARLY_PAYMENT
)
SELECT 
    MES_DIFF_EARLY_PAYMENT,
    Measure0,
    Measure1
FROM 
    Early_Payments;