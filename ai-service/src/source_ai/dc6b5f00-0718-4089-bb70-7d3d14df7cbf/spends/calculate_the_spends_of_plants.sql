SELECT 
        Plant.TXT_PLANT, 
        COUNT(DIM_INVOICE_POSITION) AS CountInvoicePosition,
        SUM(FactInvoicePosition.MES_SPEND_CURR_1) AS TotalSpend 
    FROM data.VT_C_FACT_INVOICEPOSITION_MULTIPLIED AS FactInvoicePosition 
    JOIN data.VT_DIM_Plant AS Plant ON FactInvoicePosition.DIM_PLANT = Plant.DIM_PLANT 
    GROUP BY Plant.TXT_PLANT 