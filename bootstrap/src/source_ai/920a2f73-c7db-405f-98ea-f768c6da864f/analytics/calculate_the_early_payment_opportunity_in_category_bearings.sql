    (
        WITH DIFFPAYMENT AS (
            SELECT
                YEAR(TO_DATE(VDP.DIM_DATE, 'YYYYMMDD')) AS YEAR,
                QUARTER(TO_DATE(VDP.DIM_DATE, 'YYYYMMDD')) AS QUARTER,
                MONTH(TO_DATE(VDP.DIM_DATE, 'YYYYMMDD')) AS MONTH,
                SOUR.TXT_CATEGORY_LEVEL_2 AS CATEGORY,
                SC.TXT_COUNTRY AS COUNTRY,
                G.TXT_PLANT AS PLANT,
                com.TXT_LEVEL_4 AS COMPANY,
                SUP.TXT_CONS_SUPPLIER_L1 AS SUPPLIER,
                C.TXT_MATERIAL AS MATERIAL,
                PT.TXT_CONS_PAYMENT_TERM as PAYMENT_TERM_GROUP,
                NULLIF(COUNT(MES_INTEGER), 0) AS MES_COUNT,
                SUM(IP.MES_DIFF_EARLY_PAYMENT) AS MES_DIFF_EARLY_PAYMENT,
                SUM(IP.MES_SPEND_PAID_CURR_1) AS TOTAL_SPEND,
                SUM(IP.mes_diff_invoice_payment_date_weighted) AS Mes_diff_invoice_payment_date_weighted,
                CASE
                    WHEN COUNT(MES_INTEGER) > 0 THEN SUM(MES_DIFF_EARLY_PAYMENT) / COUNT(MES_INTEGER)
                    ELSE 0
                END AS Diff_Early_Payment,
                10 as WACC
            FROM
                DATA.VT_C_FACT_INVOICEPOSITION_PAYMENT AS IP
                JOIN DATA.VT_C_DIM_SUPPLIER AS SUP ON SUP.DIM_SUPPLIER = IP.DIM_SUPPLIER
                JOIN DATA.VT_C_DIM_MATERIAL AS C ON C.DIM_MATERIAL = IP.DIM_MATERIAL
                JOIN DATA.VT_C_DIM_SOURCINGTREE_TECHCME AS SOUR ON SOUR.DIM_SOURCING_TREE = IP.DIM_SOURCING_TREE
                JOIN DATA.VT_DIM_PERIOD VDP ON VDP.DIM_DATE = IP.DIM_DATE
                JOIN DATA.VT_DIM_SupplierCountry SC ON IP.DIM_COUNTRY = SC.DIM_COUNTRY
                JOIN DATA.VT_DIM_COMPANY COM on IP.DIM_COMPANY = COM.DIM_COMPANY
                JOIN data.VT_DIM_PLANT G ON IP.DIM_PLANT = G.DIM_PLANT
                JOIN DATA.VT_DIM_PAYMENTTERM AS PT ON PT.DIM_PAYMENT_TERM = IP.DIM_PAYMENT_TERM
            WHERE
                LOWER(IP.DIM_VALUE_TYPE) = LOWER('P')
                AND LOWER(PT.TXT_PAYMENT_TERM_TYPE) = LOWER('NET PAYMENT')
                AND G.TXT_PLANT <> '#'
            GROUP BY
                YEAR(TO_DATE(VDP.DIM_DATE, 'YYYYMMDD')),
                QUARTER(TO_DATE(VDP.DIM_DATE, 'YYYYMMDD')),
                MONTH(TO_DATE(VDP.DIM_DATE, 'YYYYMMDD')),
                SUP.TXT_CONS_SUPPLIER_L1,
                SOUR.TXT_CATEGORY_LEVEL_2,
                sc.TXT_COUNTRY,
                g.TXT_PLANT,
                c.TXT_MATERIAL,
                pt.txt_cons_payment_term,
                com.txt_level_4
        )
        SELECT
            YEAR,
            CATEGORY,
            SUPPLIER,
            COUNTRY,
            PLANT,
            COMPANY,
            MATERIAL,
            PAYMENT_TERM_GROUP,
            ROUND(SUM(Diff_Early_Payment), 2) as Diff_Early_Payment,
            ROUND(SUM(TOTAL_SPEND), 2) as Total_Spend,
            ROUND(SUM(Mes_diff_invoice_payment_date_weighted), 2) AS Mes_diff_invoice_payment_date_weighted,
            ROUND(
                SUM(
                    CASE
                        WHEN MES_DIFF_EARLY_PAYMENT < -3 THEN (TOTAL_SPEND * DIFF_EARLY_PAYMENT * 0.1 * -1) / 365
                        ELSE 0
                    END
                ),
                2
            ) AS EARLY_PAYMENT
        FROM
            DiffPayment
        WHERE YEAR = YEAR(CURRENT_DATE)
        GROUP BY
            Year,
            CATEGORY,
            SUPPLIER,
            COUNTRY,
            PLANT,
            COMPANY,
            MATERIAL,
            PAYMENT_TERM_GROUP
        ORDER BY
            Early_Payment DESC
    ) 