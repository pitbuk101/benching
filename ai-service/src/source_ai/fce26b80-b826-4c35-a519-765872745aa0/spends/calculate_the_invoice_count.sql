WITH InvoiceCount AS (
    SELECT COUNT(*) AS mes_count_invoice
    FROM Fact invoice position
)
SELECT mes_count_invoice
FROM InvoiceCount;