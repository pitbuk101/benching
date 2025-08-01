from ada.utils.logs.time_logger import log_time
@log_time
def get_payment_terms_query(supplier_name=None, sku_names=None):
    payment_terms_query = '''
    WITH PAYMENTDETAILS AS (
        SELECT
            YEAR(TO_DATE(P.DIM_DATE, 'YYYYMMDD')) AS YEAR,
            QUARTER(TO_DATE(P.DIM_DATE, 'YYYYMMDD')) AS QUARTER,
            MONTHNAME(TO_DATE(P.DIM_DATE, 'YYYYMMDD')) AS MONTH,
            T2.TXT_SUPPLIER AS SUPPLIER,
            ST.TXT_CATEGORY_LEVEL_2 AS CATEGORY,
            COM.TXT_LEVEL_4 AS COMPANY,
            SC.TXT_COUNTRY,
            --F.TXT_INCOTERM,
            --G.TXT_PLANT,
            C.TXT_MATERIAL,
            SUM(FP.MES_SPEND_PAID_CURR_1) AS SPEND,
            SUM(FP.MES_DIFF_INVOICE_PAYMENT_DATE) AS TOTAL_PAYMENT_DATE_DIFF,
            COUNT(FP.MES_INTEGER) AS PAYMENT_COUNT,
            PT.TXT_PAYMENT_TERM_TYPE AS PAYMENT_TERM,
            MAX(PT.NUM_DAYS_NET) AS NUM_DAYS,
            SUM(FP.MES_DIFF_INVOICE_PAYMENT_DATE) / COUNT(FP.MES_INTEGER) AS PAYMENT_DAYS,
            GREATEST(
                (
                    SUM(FP.MES_DIFF_INVOICE_PAYMENT_DATE) / COUNT(FP.MES_INTEGER)
                ),
                MAX(PT.NUM_DAYS_NET)
            ) AS MAX_PAYMENT_DAYS
        FROM
            DATA.VT_C_FACT_INVOICEPOSITION_PAYMENT FP
            JOIN DATA.VT_DIM_PAYMENTTERM PT ON FP.DIM_PAYMENT_TERM = PT.DIM_PAYMENT_TERM
            JOIN DATA.VT_C_DIM_VALUETYPE VDV ON VDV.DIM_VALUE_TYPE = FP.DIM_VALUE_TYPE
            JOIN DATA.VT_C_DIM_MATERIAL_TEMP C ON FP.DIM_MATERIAL = C.DIM_MATERIAL
            JOIN DATA.VT_C_DIM_SUPPLIER T2 ON FP.DIM_SUPPLIER = T2.DIM_SUPPLIER
            JOIN DATA.VT_C_DIM_SOURCINGTREE_TECHCME ST ON FP.DIM_SOURCING_TREE = ST.DIM_SOURCING_TREE
            JOIN DATA.VT_DIM_PERIOD P ON FP.DIM_DATE = P.DIM_DATE 
            JOIN DATA.VT_DIM_SUPPLIERCOUNTRY SC ON FP.DIM_COUNTRY=SC.DIM_COUNTRY 
            JOIN DATA.VT_DIM_INCOTERM F ON FP.DIM_INCOTERM = F.DIM_INCOTERM
            JOIN DATA.VT_DIM_PLANT G ON FP.DIM_PLANT = G.DIM_PLANT
            JOIN DATA.VT_DIM_COMPANY COM ON FP.DIM_COMPANY=COM.DIM_COMPANY
        WHERE
            VDV.DIM_VALUE_TYPE = 'P'
        GROUP BY
            PT.TXT_PAYMENT_TERM_TYPE,
            C.TXT_MATERIAL,
            YEAR(TO_DATE(P.DIM_DATE, 'YYYYMMDD')),
            QUARTER(TO_DATE(P.DIM_DATE, 'YYYYMMDD')),
            MONTHNAME(TO_DATE(P.DIM_DATE, 'YYYYMMDD')),
            T2.TXT_SUPPLIER,
            ST.TXT_CATEGORY_LEVEL_2,
            SC.TXT_COUNTRY,
            --F.TXT_INCOTERM,
            --G.TXT_PLANT,
            COM.TXT_LEVEL_4
    )
    SELECT
            PD.YEAR,
            PD.QUARTER,
            PD.MONTH,
            PD.CATEGORY,
            PD.TXT_COUNTRY AS COUNTRY,
            -- PD.TXT_INCOTERM AS INCOTERM,
            --PD.TXT_PLANT AS PLANT,
            PD.SUPPLIER,
            PD.TXT_MATERIAL AS MATERIAL,
            PD.SPEND,
        -- PD.TOTAL_PAYMENT_DATE_DIFF,
            -- PAYMENT_COUNT,
        -- PAYMENT_TERM,
        -- NUM_DAYS,
        -- PAYMENT_DAYS,
        -- MAX_PAYMENT_DAYS,
            COALESCE(MAX_PAYMENT_DAYS, 90) AS SELECTED_PAYMENT_TERM_DAYS,
            --(0.1/365) AS WACC,
            CASE
            WHEN (90 - MAX_PAYMENT_DAYS) > 0 THEN (
                PD.SPEND * (90 - COALESCE(MAX_PAYMENT_DAYS, 90)) * (0.1 / 365)
            )
            ELSE ( 
            0
            )
        END AS POTENTIAL_SAVINGS
    FROM
        PAYMENTDETAILS PD
    '''
    # WHERE
    #     PD.SUPPLIER = '{supplier}' AND MATERIAL in {sku_names} AND PD.YEAR >= EXTRACT(YEAR FROM CURRENT_DATE) - 1 AND POTENTIAL_SAVINGS > 0
        
    conditions = []
    
    if supplier_name:
        conditions.append(f"SUPPLIER = '{supplier_name}'")
    
    if sku_names:
        conditions.append(f"MATERIAL IN {sku_names}")
    
    conditions.append("POTENTIAL_SAVINGS > 0")  # Always required
    conditions.append("PD.YEAR >= EXTRACT(YEAR FROM CURRENT_DATE) - 1")

    # If there are any conditions, append them to the query
    if conditions:
        payment_terms_query += " WHERE " + " AND ".join(conditions)

    payment_terms_query += '''
    ORDER BY YEAR DESC, QUARTER ASC, MONTH ASC, CATEGORY ASC, POTENTIAL_SAVINGS DESC
    '''
    if not sku_names:
        payment_terms_query += '''
        LIMIT 5
        '''

    return payment_terms_query

@log_time
def get_early_payments_query(supplier_name=None, sku_names=None):
    early_payments_query = '''
    WITH DIFFPAYMENT AS (
        SELECT
            SUP.TXT_SUPPLIER,
            C.TXT_MATERIAL,
    --     SC.TXT_COUNTRY,
        --   F.TXT_INCOTERM,
        --  G.TXT_PLANT,
            YEAR(TO_DATE(P.DIM_DATE, 'YYYYMMDD')) AS YEAR,
            QUARTER(TO_DATE(P.DIM_DATE, 'YYYYMMDD')) AS QUARTER,
            MONTHNAME(TO_DATE(P.DIM_DATE, 'YYYYMMDD')) AS MONTH,
            ST.TXT_CATEGORY_LEVEL_2 AS CATEGORY,
    --      NULLIF(COUNT(MES_INTEGER), 0) AS COUNT_MES_INTEGER,
            SUM(MES_DIFF_EARLY_PAYMENT) AS MES_DIFF_EARLY_PAYMENT,
            SUM(IP.MES_SPEND_PAID_CURR_1) AS TOTAL_SPEND,
            SUM(MES_DIFF_EARLY_PAYMENT) / NULLIF(COUNT(MES_INTEGER), 0) AS DIFF_EARLY_PAYMENT
        FROM
            DATA.VT_C_FACT_INVOICEPOSITION_PAYMENT AS IP
            JOIN DATA.VT_C_DIM_SUPPLIER AS SUP ON IP.DIM_SUPPLIER = SUP.DIM_SUPPLIER
            JOIN DATA.VT_C_DIM_MATERIAL C ON IP.DIM_MATERIAL = C.DIM_MATERIAL
            JOIN DATA.VT_DIM_PaymentTerm AS PT ON PT.DIM_PAYMENT_TERM = IP.DIM_PAYMENT_TERM
            JOIN DATA.VT_C_DIM_SOURCINGTREE_TECHCME ST ON IP.DIM_SOURCING_TREE = ST.DIM_SOURCING_TREE
            JOIN DATA.VT_DIM_PERIOD P ON IP.DIM_DATE = P.DIM_DATE
            JOIN DATA.VT_DIM_SUPPLIERCOUNTRY SC ON IP.DIM_COUNTRY = SC.DIM_COUNTRY
            JOIN DATA.VT_DIM_INCOTERM F ON IP.DIM_INCOTERM = F.DIM_INCOTERM
            JOIN DATA.VT_DIM_PLANT G ON IP.DIM_PLANT = G.DIM_PLANT
        WHERE
            IP.DIM_VALUE_TYPE = 'P'
            and LOWER(PT.TXT_PAYMENT_TERM_TYPE) = LOWER('Net Payment')
        GROUP BY
            SUP.TXT_SUPPLIER,
            C.TXT_MATERIAL,
        --   SC.TXT_COUNTRY,
        --  F.TXT_INCOTERM,
        -- G.TXT_PLANT,
            YEAR(TO_DATE(P.DIM_DATE, 'YYYYMMDD')),
            MONTHNAME(TO_DATE(P.DIM_DATE, 'YYYYMMDD')),
            QUARTER(TO_DATE(P.DIM_DATE, 'YYYYMMDD')),
            ST.TXT_CATEGORY_LEVEL_2
    )
    SELECT
        DP.YEAR AS YEAR,
        DP.QUARTER AS QUARTER,
        DP.MONTH AS MONTH,
        TRIM(DP.CATEGORY) AS CATEGORY,
    -- TRIM(DP.TXT_COUNTRY) AS COUNTRY,
    -- TRIM(DP.TXT_PLANT) AS PLANT,
        TRIM(DP.TXT_SUPPLIER) AS SUPPLIER,
        TRIM(DP.TXT_MATERIAL) AS MATERIAL,
    -- TRIM(DP.TXT_INCOTERM) AS INCOTERM,
        DP.MES_DIFF_EARLY_PAYMENT AS MES_DIFF_EARLY_PAYMENT,
    -- DP.COUNT_MES_INTEGER AS MES_COUNT,
        DP.TOTAL_SPEND AS TOTAL_SPENDS,
        DP.DIFF_EARLY_PAYMENT AS DIFF_EARLY_PAYMENT,
        ROUND(
            CASE
                WHEN DP.MES_DIFF_EARLY_PAYMENT < -3 THEN (DP.TOTAL_SPEND * DP.DIFF_EARLY_PAYMENT * -1) / 365
                ELSE 0
            END,
            2
        ) AS EARLY_PAYMENT_OPPORTUNITY
    FROM
        DIFFPAYMENT AS DP
    '''
        # WHERE
        # SUPPLIER = '{supplier}' AND MATERIAL in {sku_names} AND DP.YEAR >= EXTRACT(YEAR FROM CURRENT_DATE) - 1 AND EARLY_PAYMENT_OPPORTUNITY > 0

    conditions = []

    if supplier_name:
        conditions.append(f"SUPPLIER = '{supplier_name}'")

    if sku_names:
        # formatted_sku = ", ".join(f"'{sku}'" for sku in sku_names)
        conditions.append(f"MATERIAL IN {sku_names}")
    conditions.append("DP.YEAR >= EXTRACT(YEAR FROM CURRENT_DATE) - 1")
    conditions.append("EARLY_PAYMENT_OPPORTUNITY > 0")  # Always required

    # If there are any conditions, append them to the query
    if conditions:
        early_payments_query += " WHERE " + " AND ".join(conditions)

    early_payments_query += '''

    ORDER BY
        YEAR DESC,
        QUARTER ASC,
        MONTH ASC,
        CATEGORY ASC,
    -- COUNTRY ASC,
        --PLANT ASC,
        SUPPLIER ASC,
        MATERIAL ASC,
        --INCOTERM ASC,
        EARLY_PAYMENT_OPPORTUNITY DESC
    '''
    if not sku_names:
        early_payments_query += '''
        LIMIT 5
        '''
    return early_payments_query

@log_time
def get_unused_discount_query(supplier_name=None, sku_names=None):
    unused_discount_query = '''
    WITH DISCOUNTSUMMARY AS (
        SELECT
            S.TXT_SUPPLIER,
            C.TXT_MATERIAL,
        --  SC.TXT_COUNTRY,
        --  F.TXT_INCOTERM,
        --  G.TXT_PLANT,
            YEAR(TO_DATE(P.DIM_DATE, 'YYYYMMDD')) AS YEAR,
            QUARTER(TO_DATE(P.DIM_DATE, 'YYYYMMDD')) AS QUARTER,
            MONTHNAME(TO_DATE(P.DIM_DATE, 'YYYYMMDD')) AS MONTH,
            ST.TXT_CATEGORY_LEVEL_2 AS CATEGORY,
            SUM(FP.MES_DISCOUNT_POSSIBLE_CURR_1) AS DISCOUNT_POSSIBLE,
            SUM(FP.MES_DISCOUNT_CURR_1) AS DISCOUNT
        FROM
            DATA.VT_C_FACT_INVOICEPOSITION_PAYMENT FP
            JOIN DATA.VT_DIM_PAYMENTTERM AS PT ON FP.DIM_PAYMENT_TERM = PT.DIM_PAYMENT_TERM
            JOIN DATA.VT_C_DIM_VALUETYPE AS VT ON FP.DIM_VALUE_TYPE = VT.DIM_VALUE_TYPE
            JOIN DATA.VT_C_DIM_SUPPLIER AS S ON FP.DIM_SUPPLIER = S.DIM_SUPPLIER
            JOIN DATA.VT_C_DIM_MATERIAL_TEMP C ON FP.DIM_MATERIAL = C.DIM_MATERIAL
            JOIN DATA.VT_C_DIM_SOURCINGTREE_TECHCME ST ON FP.DIM_SOURCING_TREE = ST.DIM_SOURCING_TREE
            JOIN DATA.VT_DIM_PERIOD P ON FP.DIM_DATE = P.DIM_DATE
            JOIN DATA.VT_DIM_SUPPLIERCOUNTRY SC ON FP.DIM_COUNTRY = SC.DIM_COUNTRY
            JOIN DATA.VT_DIM_INCOTERM F ON FP.DIM_INCOTERM = F.DIM_INCOTERM
            JOIN DATA.VT_DIM_PLANT G ON FP.DIM_PLANT = G.DIM_PLANT
        WHERE
            VT.DIM_VALUE_TYPE = 'P'
            AND LOWER(PT.TXT_PAYMENT_TERM_TYPE) = LOWER('Discount')
        GROUP BY
            S.TXT_SUPPLIER,
            C.TXT_MATERIAL,
            ST.TXT_CATEGORY_LEVEL_2,
            YEAR(TO_DATE(P.DIM_DATE, 'YYYYMMDD')),
            QUARTER(TO_DATE(P.DIM_DATE, 'YYYYMMDD')),
            MONTHNAME(TO_DATE(P.DIM_DATE, 'YYYYMMDD'))
        --  SC.TXT_COUNTRY,
        --  F.TXT_INCOTERM,
        --  G.TXT_PLANT
    )
    SELECT
        DS.YEAR,
        DS.QUARTER,
        DS.MONTH,
        TRIM(DS.CATEGORY) AS CATEGORY,
    --   TRIM(DS.TXT_COUNTRY) AS COUNTRY,
    --  TRIM(DS.TXT_PLANT) AS PLANT,
        TRIM(DS.TXT_SUPPLIER) AS SUPPLIER,
        --TRIM(DS.TXT_INCOTERM) AS INCOTERM,
        TRIM(DS.TXT_MATERIAL) AS MATERIAL,
        ROUND(DS.DISCOUNT_POSSIBLE, 2) AS DISCOUNT_POSSIBLE,
        ROUND(DS.DISCOUNT, 2) AS DISCOUNT,
        ROUND(
            CASE
                WHEN (DS.DISCOUNT_POSSIBLE - DS.DISCOUNT) < 0 THEN 0
                ELSE (DS.DISCOUNT_POSSIBLE - DS.DISCOUNT)
            END,
            2
        ) AS DISCOUNT_NOT_USED
    FROM
        DISCOUNTSUMMARY DS
    '''
    # WHERE
    #     SUPPLIER = '{supplier}' AND MATERIAL in {sku_names} AND DISCOUNT_NOT_USED >0
    conditions = []

    if supplier_name:
        conditions.append(f"SUPPLIER = '{supplier_name}'")

    if sku_names:
        conditions.append(f"MATERIAL IN {sku_names}")
        

    conditions.append("DISCOUNT_NOT_USED > 0")  # Always required
    conditions.append("DS.YEAR >= EXTRACT(YEAR FROM CURRENT_DATE) - 1")

    # If there are any conditions, append them to the query
    if conditions:
        unused_discount_query += " WHERE " + " AND ".join(conditions)

    unused_discount_query += '''
    ORDER BY
        DS.YEAR DESC,
        DS.QUARTER ASC,
        DS.MONTH ASC,
        DS.CATEGORY ASC,
        DISCOUNT_NOT_USED DESC
    '''
    if not sku_names:
        unused_discount_query += '''
        LIMIT 5
        '''
    return unused_discount_query

@log_time
def get_parametric_cost_modeling_query(supplier_name=None, sku_names=None):

    parametric_cost_modeling_query = '''
    WITH SELECTED_PERIOD_DATA AS (
        SELECT
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            MIN(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS MIN_DATE,
            MAX(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS MAX_DATE
        FROM
            DATA.VT_DIM_PERIOD AS PER
        WHERE
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) = 2024
        GROUP BY
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD'))
    ),
    PURCHASE_PRICE_DATA AS (
        SELECT
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS YEAR,
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS QUARTER,
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS MONTH,
            ST.TXT_CATEGORY_LEVEL_2 AS CATEGORY,
            CON.TXT_COUNTRY AS COUNTRY,
            PL.TXT_PLANT AS PLANT,
            SUP.TXT_SUPPLIER AS SUPPLIER,
            MAT.TXT_MATERIAL AS MATERIAL,
            SUM(FIP.MES_SPEND_CURR_1) AS SPENDS,
            SUM(FIP.MES_QUANTITY) AS QUANTITY,
            CASE
                WHEN SUM(FIP.MES_SPEND_CURR_1) * SUM(FIP.MES_QUANTITY) > 0 THEN ABS(SUM(FIP.MES_SPEND_CURR_1)) / ABS(SUM(FIP.MES_QUANTITY))
                ELSE 0
            END AS PURCHASE_PRICE
        FROM
            DATA.VT_C_FACT_INVOICEPOSITION_MULTIPLIED FIP
            JOIN DATA.VT_DIM_PERIOD PER ON PER.DIM_DATE = FIP.DIM_DATE
            JOIN DATA.VT_C_DIM_MATERIAL MAT ON MAT.DIM_MATERIAL = FIP.DIM_MATERIAL
            JOIN DATA.VT_C_DIM_SUPPLIER SUP ON SUP.DIM_SUPPLIER = FIP.DIM_SUPPLIER
            JOIN DATA.VT_C_DIM_SOURCINGTREE_TECHCME ST ON ST.DIM_SOURCING_TREE = FIP.DIM_SOURCING_TREE
            JOIN DATA.VT_DIM_SUPPLIERCOUNTRY CON ON CON.DIM_COUNTRY = FIP.DIM_COUNTRY
            JOIN DATA.VT_DIM_PLANT PL ON PL.DIM_PLANT = FIP.DIM_PLANT
        WHERE
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) IN (
                SELECT
                    YEAR(MIN_DATE)
                FROM
                    SELECTED_PERIOD_DATA
            )
            AND QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) IN (
                SELECT
                    QUARTER(MIN_DATE)
                FROM
                    SELECTED_PERIOD_DATA
            )
        GROUP BY
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            CON.TXT_COUNTRY,
            PL.TXT_PLANT,
            ST.TXT_CATEGORY_LEVEL_2,
            MAT.TXT_MATERIAL,
            SUP.TXT_SUPPLIER
    ),
    SHOULD_COST_DATA AS (
        SELECT
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS YEAR,
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS QUARTER,
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS MONTH,
            ST.TXT_CATEGORY_LEVEL_2 AS CATEGORY,
            MAT.TXT_MATERIAL AS MATERIAL,
            COMP.TXT_COMPONENT AS COMPONENT,
            SUM(FIS.MES_SHOULD_COST) AS SHOULD_COST
        FROM
            DATA.VT_FACT_ICM_SHOULDCOST FIS
            JOIN DATA.VT_DIM_PERIOD PER ON PER.DIM_DATE = FIS.DIM_DATE
            JOIN DATA.VT_DIM_ICM_ARCHETYPE_INDEX_MAPPING IAIM ON IAIM.DIM_COMBINATION_KEY = FIS.DIM_COMBINATION_KEY
            JOIN DATA.VT_DIM_ICM_COMPONENT COMP ON COMP.DIM_COMPONENT_KEY = IAIM.DIM_COMPONENT_KEY
            JOIN DATA.VT_DIM_ICM_MAPPING ICM ON ICM.DIM_ARCHETYPE = IAIM.DIM_ARCHETYPE
            JOIN DATA.VT_C_DIM_MATERIAL MAT ON MAT.DIM_MATERIAL = ICM.DIM_MATERIAL
            JOIN DATA.VT_C_DIM_SOURCINGTREE_TECHCME ST ON ST.DIM_SOURCING_TREE = ICM.DIM_SOURCING_TREE
        WHERE
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) IN (
                SELECT
                    YEAR(MIN_DATE)
                FROM
                    SELECTED_PERIOD_DATA
            )
            AND QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) IN (
                SELECT
                    QUARTER(MIN_DATE)
                FROM
                    SELECTED_PERIOD_DATA
            )
        GROUP BY
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            ST.TXT_CATEGORY_LEVEL_2,
            MAT.TXT_MATERIAL,
            COMP.TXT_COMPONENT
    ),
    CLEANSHEET_DATA AS (
        SELECT
            PPD.YEAR,
            PPD.QUARTER,
            PPD.MONTH,
            PPD.CATEGORY,
            SCD.COMPONENT,
            PPD.PLANT,
            PPD.COUNTRY,
            PPD.MATERIAL,
            PPD.SUPPLIER,
            SUM(SPENDS) AS SPENDS,
            (SUM(PPD.PURCHASE_PRICE) - SUM(SCD.SHOULD_COST)) * SUM(PPD.QUANTITY) AS CLEANSHEET_OPPORTUNITY
        FROM
            PURCHASE_PRICE_DATA PPD
            JOIN SHOULD_COST_DATA SCD ON PPD.YEAR = SCD.YEAR
            AND PPD.MATERIAL = SCD.MATERIAL
        GROUP BY
            PPD.YEAR,
            PPD.QUARTER,
            PPD.MONTH,
            PPD.PLANT,
            PPD.COUNTRY,
            PPD.CATEGORY,
            SCD.COMPONENT,
            PPD.MATERIAL,
            PPD.SUPPLIER
    ),
    PCM_GAP_PERCENT AS (
        SELECT
            YEAR,
            QUARTER,
            MONTH,
            CATEGORY,
            COMPONENT,
            MATERIAL,
            SUPPLIER,
            PLANT,
            COUNTRY,
            CLEANSHEET_OPPORTUNITY,
            DIV0(CLEANSHEET_OPPORTUNITY, SPENDS) AS PCM_GAP_PER_UNIT,
            DIV0(CLEANSHEET_OPPORTUNITY * 100, SPENDS) AS GAP_PERCENTAGE
        FROM
            CLEANSHEET_DATA
        ORDER BY
            YEAR DESC,
            QUARTER DESC,
            MONTH ASC,
            CATEGORY DESC
    ),
    SELECTED_QUARTER_MONTH_SHOULD_COST_DATA AS (
        SELECT
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS YEAR,
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS QUARTER,
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS MONTH,
            TXT_CATEGORY_LEVEL_2,
            MAT.TXT_MATERIAL AS MATERIAL,
            ARCH.TXT_ARCHETYPE AS ARCHTYPE,
            SUM(FIS.MES_SHOULD_COST) AS SELECTED_PERIOD_SHOULD_COST
        FROM
            DATA.VT_FACT_ICM_SHOULDCOST FIS
            JOIN DATA.VT_DIM_PERIOD PER ON PER.DIM_DATE = FIS.DIM_DATE
            JOIN DATA.VT_DIM_ICM_ARCHETYPE_INDEX_MAPPING IAIM ON IAIM.DIM_COMBINATION_KEY = FIS.DIM_COMBINATION_KEY
            JOIN DATA.VT_DIM_ICM_ARCHETYPE ARCH ON ARCH.DIM_ARCHETYPE = IAIM.DIM_ARCHETYPE
            JOIN DATA.VT_DIM_ICM_MAPPING ICM ON IAIM.DIM_ARCHETYPE = ICM.DIM_ARCHETYPE
            JOIN DATA.VT_C_DIM_MATERIAL MAT ON MAT.DIM_MATERIAL = ICM.DIM_MATERIAL
            JOIN DATA.VT_C_DIM_SOURCINGTREE_TECHCME ST ON ST.DIM_SOURCING_TREE = ICM.DIM_SOURCING_TREE
        WHERE
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) IN (
                SELECT
                    YEAR(MIN_DATE)
                FROM
                    SELECTED_PERIOD_DATA
            )
            AND MONTH(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) IN (
                SELECT
                    MONTH(MIN_DATE)
                FROM
                    SELECTED_PERIOD_DATA
            )
        GROUP BY
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            TXT_CATEGORY_LEVEL_2,
            MAT.TXT_MATERIAL,
            ARCH.TXT_ARCHETYPE
    ),
    PREVIOUS_YEAR_LAST_MONTH_SHOULD_COST_DATA AS (
        SELECT
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS YEAR,
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS MONTH,
            TXT_CATEGORY_LEVEL_2,
            MAT.TXT_MATERIAL AS MATERIAL,
            ARCH.TXT_ARCHETYPE AS ARCHTYPE,
            SUM(FIS.MES_SHOULD_COST) AS PREVIOUS_PERIOD_SHOULD_COST
        FROM
            DATA.VT_FACT_ICM_SHOULDCOST FIS
            JOIN DATA.VT_DIM_PERIOD PER ON PER.DIM_DATE = FIS.DIM_DATE
            JOIN DATA.VT_DIM_ICM_ARCHETYPE_INDEX_MAPPING IAIM ON IAIM.DIM_COMBINATION_KEY = FIS.DIM_COMBINATION_KEY
            JOIN DATA.VT_DIM_ICM_ARCHETYPE ARCH ON ARCH.DIM_ARCHETYPE = IAIM.DIM_ARCHETYPE
            JOIN DATA.VT_DIM_ICM_MAPPING ICM ON IAIM.DIM_ARCHETYPE = ICM.DIM_ARCHETYPE
            JOIN DATA.VT_C_DIM_MATERIAL MAT ON MAT.DIM_MATERIAL = ICM.DIM_MATERIAL
            JOIN DATA.VT_C_DIM_SOURCINGTREE_TECHCME ST ON ST.DIM_SOURCING_TREE = ICM.DIM_SOURCING_TREE
        WHERE
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) IN (
                SELECT
                    YEAR(MIN_DATE) -1
                FROM
                    SELECTED_PERIOD_DATA
            )
            AND MONTH(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) = 12
        GROUP BY
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            TXT_CATEGORY_LEVEL_2,
            MAT.TXT_MATERIAL,
            ARCH.TXT_ARCHETYPE
    ),
    MARKET_VOLATILITY AS (
        SELECT
            SMSC.YEAR,
            SMSC.QUARTER,
            SMSC.MONTH,
            SMSC.TXT_CATEGORY_LEVEL_2 AS CATEGORY,
            SMSC.MATERIAL AS MATERIAL,
            SMSC.ARCHTYPE,
            SMSC.SELECTED_PERIOD_SHOULD_COST,
            PMSC.PREVIOUS_PERIOD_SHOULD_COST,
            ROUND(
                (
                    SMSC.SELECTED_PERIOD_SHOULD_COST - PMSC.PREVIOUS_PERIOD_SHOULD_COST
                ),
                2
            ) AS DIFF_SHOULD_COST,
            ROUND(
                (
                    (
                        (
                            PMSC.PREVIOUS_PERIOD_SHOULD_COST - SMSC.SELECTED_PERIOD_SHOULD_COST
                        ) * 100
                    ) / SMSC.SELECTED_PERIOD_SHOULD_COST
                ),
                5
            ) AS MARKET_VOLATILITY_PERCENTAGE
        FROM
            SELECTED_QUARTER_MONTH_SHOULD_COST_DATA SMSC
            JOIN PREVIOUS_YEAR_LAST_MONTH_SHOULD_COST_DATA PMSC ON SMSC.ARCHTYPE = PMSC.ARCHTYPE
            AND SMSC.TXT_CATEGORY_LEVEL_2 = PMSC.TXT_CATEGORY_LEVEL_2
            AND SMSC.MATERIAL = PMSC.MATERIAL
        ORDER BY
            SMSC.YEAR,
            SMSC.QUARTER,
            SMSC.MONTH,
            SMSC.TXT_CATEGORY_LEVEL_2
    ),
    OVERALL_SPENDS_SHARE AS (
        SELECT
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS SELECTED_YEAR,
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS SELECTED_QUARTER,
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS SELECTED_MONTH,
            (
                SELECT
                    SUM(FIP2.MES_SPEND_CURR_1)
                FROM
                    DATA.VT_C_FACT_INVOICEPOSITION_MULTIPLIED FIP2
            ) AS TOTAL_SPEND,
            SUM(FIP.MES_SPEND_CURR_1) AS SPEND_BY_YEAR,
            SUM(FIP.MES_QUANTITY) AS TOTAL_QUANTITY
        FROM
            DATA.VT_C_FACT_INVOICEPOSITION_MULTIPLIED FIP
            JOIN DATA.VT_DIM_PERIOD PER ON PER.DIM_DATE = FIP.DIM_DATE
        WHERE
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) IN (
                SELECT
                    YEAR(MIN_DATE)
                FROM
                    SELECTED_PERIOD_DATA
            )
            AND MONTH(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) IN (
                SELECT
                    MONTH(MIN_DATE)
                FROM
                    SELECTED_PERIOD_DATA
            )
        GROUP BY
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD'))
    ),
    SELECTED_PURCHASE_PRICE AS (
        SELECT
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS SELECTED_YEAR,
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS SELECTED_QUARTER,
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS SELECTED_MONTH,
            SC.TXT_COUNTRY AS COUNTRY,
            PL.TXT_PLANT AS PLANT,
            ST.TXT_CATEGORY_LEVEL_2 AS CATEGORY,
            MAT.TXT_MATERIAL AS MATERIAL,
            SUP.TXT_SUPPLIER AS SUPPLIER,
            SUM(FIP.MES_SPEND_CURR_1) AS SPENDS,
            SUM(FIP.MES_QUANTITY) AS QUANTITY,
            CASE
                WHEN SUM(FIP.MES_SPEND_CURR_1) * SUM(FIP.MES_QUANTITY) > 0 THEN ABS(SUM(FIP.MES_SPEND_CURR_1)) / ABS(SUM(FIP.MES_QUANTITY))
                ELSE 0
            END AS SELECTED_PURCHASE_PRICE
        FROM
            DATA.VT_C_FACT_INVOICEPOSITION_MULTIPLIED FIP
            JOIN DATA.VT_DIM_PERIOD PER ON PER.DIM_DATE = FIP.DIM_DATE
            JOIN DATA.VT_C_DIM_MATERIAL MAT ON MAT.DIM_MATERIAL = FIP.DIM_MATERIAL
            JOIN DATA.VT_C_DIM_SUPPLIER SUP ON SUP.DIM_SUPPLIER = FIP.DIM_SUPPLIER
            JOIN DATA.VT_C_DIM_SOURCINGTREE_TECHCME ST ON FIP.DIM_SOURCING_TREE = ST.DIM_SOURCING_TREE
            JOIN DATA.VT_DIM_PLANT PL ON PL.DIM_PLANT = FIP.DIM_PLANT
            JOIN DATA.VT_DIM_SUPPLIERCOUNTRY SC ON SC.DIM_COUNTRY = FIP.DIM_COUNTRY
        WHERE
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) IN (
                SELECT
                    YEAR(MIN_DATE)
                FROM
                    SELECTED_PERIOD_DATA
            )
            AND MONTH(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) IN (
                SELECT
                    MONTH(MIN_DATE)
                FROM
                    SELECTED_PERIOD_DATA
            )
        GROUP BY
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            SC.TXT_COUNTRY,
            PL.TXT_PLANT,
            ST.TXT_CATEGORY_LEVEL_2,
            MAT.TXT_MATERIAL,
            SUP.TXT_SUPPLIER
    ),
    PREVIOUS_PURCHASE_PRICE AS (
        SELECT
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS PREVIOUS_YEAR,
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS PREVIOUS_QUARTER,
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) AS PREVIOUS_MONTH,
            ST.TXT_CATEGORY_LEVEL_2 AS CATEGORY,
            SC.TXT_COUNTRY AS COUNTRY,
            PL.TXT_PLANT AS PLANT,
            MAT.TXT_MATERIAL AS MATERIAL,
            SUP.TXT_SUPPLIER AS SUPPLIER,
            SUM(FIP.MES_SPEND_CURR_1) AS SPENDS,
            SUM(FIP.MES_QUANTITY) AS QUANTITY,
            CASE
                WHEN SUM(FIP.MES_SPEND_CURR_1) * SUM(FIP.MES_QUANTITY) > 0 THEN ABS(SUM(FIP.MES_SPEND_CURR_1)) / ABS(SUM(FIP.MES_QUANTITY))
                ELSE 0
            END AS PREVIOUS_PURCHASE_PRICE
        FROM
            DATA.VT_C_FACT_INVOICEPOSITION_MULTIPLIED FIP
            JOIN DATA.VT_DIM_PERIOD PER ON PER.DIM_DATE = FIP.DIM_DATE
            JOIN DATA.VT_C_DIM_MATERIAL MAT ON MAT.DIM_MATERIAL = FIP.DIM_MATERIAL
            JOIN DATA.VT_C_DIM_SUPPLIER SUP ON SUP.DIM_SUPPLIER = FIP.DIM_SUPPLIER
            JOIN DATA.VT_C_DIM_SOURCINGTREE_TECHCME ST ON FIP.DIM_SOURCING_TREE = ST.DIM_SOURCING_TREE
            JOIN DATA.VT_DIM_PLANT PL ON PL.DIM_PLANT = FIP.DIM_PLANT
            JOIN DATA.VT_DIM_SUPPLIERCOUNTRY SC ON SC.DIM_COUNTRY = FIP.DIM_COUNTRY
        WHERE
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) IN (
                SELECT
                    YEAR(MIN_DATE) -1
                FROM
                    SELECTED_PERIOD_DATA
            )
            AND MONTH(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')) = 12
        GROUP BY
            YEAR(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            QUARTER(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            MONTHNAME(TO_DATE(PER.DIM_DATE, 'YYYYMMDD')),
            SC.TXT_COUNTRY,
            PL.TXT_PLANT,
            ST.TXT_CATEGORY_LEVEL_2,
            MAT.TXT_MATERIAL,
            SUP.TXT_SUPPLIER
    ),
    PRICE_AVERAGE_DATA AS (
        SELECT
            SELECTED_YEAR,
            SELECTED_QUARTER,
            SELECTED_MONTH,
            SPP.PLANT,
            SPP.COUNTRY,
            SPP.CATEGORY,
            SPP.MATERIAL,
            SPP.SUPPLIER,
            ROUND(SELECTED_PURCHASE_PRICE, 2) AS SELECTED_PURCHASE_PRICE,
            ROUND(PREVIOUS_PURCHASE_PRICE, 2) AS PREVIOUS_PURCHASE_PRICE,
            ROUND(
                (
                    (SELECTED_PURCHASE_PRICE - PREVIOUS_PURCHASE_PRICE) / PREVIOUS_PURCHASE_PRICE
                ),
                2
            ) AS PRICE_AVERAGE_CHANGE
        FROM
            SELECTED_PURCHASE_PRICE SPP
            JOIN PREVIOUS_PURCHASE_PRICE PPP ON SPP.CATEGORY = PPP.CATEGORY
            AND SPP.PLANT = PPP.PLANT
            AND SPP.COUNTRY = PPP.COUNTRY
            AND SPP.MATERIAL = PPP.MATERIAL
            AND SPP.SUPPLIER = PPP.SUPPLIER
        WHERE
            PREVIOUS_PURCHASE_PRICE > 0
    ),
    PRICE_VOLATILITY AS (
        SELECT
            PRI.SELECTED_YEAR,
            PRI.SELECTED_QUARTER,
            PRI.SELECTED_MONTH,
            COUNTRY,
            PLANT,
            CATEGORY,
            MATERIAL,
            SUPPLIER,
            SELECTED_PURCHASE_PRICE,
            PREVIOUS_PURCHASE_PRICE,
            PRICE_AVERAGE_CHANGE,
            ROUND(
                (
                    (PRICE_AVERAGE_CHANGE * 100) /(SPEND_BY_YEAR / TOTAL_SPEND)
                ),
                5
            ) AS PRICE_VOLATILITY
        FROM
            PRICE_AVERAGE_DATA PRI
            JOIN OVERALL_SPENDS_SHARE OSS ON PRI.SELECTED_YEAR = OSS.SELECTED_YEAR
            AND PRI.SELECTED_QUARTER = OSS.SELECTED_QUARTER
            AND PRI.SELECTED_MONTH = OSS.SELECTED_MONTH
        ORDER BY
            PRICE_VOLATILITY DESC
    )
    SELECT
        PGP.YEAR,
        PGP.QUARTER,
        PGP.MONTH,
        TRIM(PGP.COUNTRY) AS COUNTRY,
        TRIM(PGP.PLANT) AS PLANT,
        TRIM(PGP.CATEGORY) AS CATEGORY,
        TRIM(PGP.SUPPLIER) AS SUPPLIER,
        TRIM(PGP.COMPONENT) AS COMPONENT,
        TRIM(PGP.MATERIAL) AS MATERIAL,
        --TRIM(MV.ARCHTYPE) AS ARCHTYPE,
        PGP.CLEANSHEET_OPPORTUNITY,
        PGP.PCM_GAP_PER_UNIT AS PCM_GAP_PERCENTAGE_PER_UNIT,
        --PGP.GAP_PERCENTAGE,
        --COALESCE(MV.SELECTED_PERIOD_SHOULD_COST, 0) AS LAST_SHOULD_COST,
        --COALESCE(MV.PREVIOUS_PERIOD_SHOULD_COST, 0) AS FIRST_SHOULD_COST,
        --COALESCE(MV.DIFF_SHOULD_COST, 0) AS DIFF_SHOULD_COST,
        --COALESCE(MV.MARKET_VOLATILITY_PERCENTAGE, 0) AS MARKET_VOLATILITY_PERCENTAGE,
        --COALESCE(PV.SELECTED_PURCHASE_PRICE, 0) AS SELECTED_PURCHASE_PRICE,
        --COALESCE(PV.PREVIOUS_PURCHASE_PRICE, 0) AS PREVIOUS_PURCHASE_PRICE,
        --COALESCE(PV.PRICE_AVERAGE_CHANGE, 0) AS PRICE_AVERAGE_CHANGE,
        --COALESCE(PV.PRICE_VOLATILITY, 0) AS PRICE_VOLATILITY_PERCENTAGE
    FROM
        PCM_GAP_PERCENT PGP
        LEFT JOIN MARKET_VOLATILITY MV ON MV.YEAR = PGP.YEAR
        AND MV.QUARTER = PGP.QUARTER
        AND PGP.CATEGORY = MV.CATEGORY
        AND PGP.MATERIAL = MV.MATERIAL
        LEFT JOIN PRICE_VOLATILITY PV ON PV.SELECTED_YEAR = PGP.YEAR
        AND PV.SELECTED_QUARTER = PGP.QUARTER
        AND PV.SELECTED_MONTH = PGP.MONTH
        AND PV.PLANT = PGP.PLANT
        AND PV.COUNTRY = PGP.COUNTRY
        AND PV.CATEGORY = PGP.CATEGORY
        AND PV.MATERIAL = PGP.MATERIAL
        AND PV.SUPPLIER = PGP.SUPPLIER
    '''
    # WHERE
    #     PGP.SUPPLIER = '{supplier}' 
    #     AND PGP.MATERIAL in {sku_names} 
    #     AND CLEANSHEET_OPPORTUNITY >0
    
    conditions = []
    
    if supplier_name:
        conditions.append(f"PGP.SUPPLIER = '{supplier_name}'")
    
    if sku_names:
        # formatted_sku = ", ".join(f"'{sku}'" for sku in sku_names)
        conditions.append(f"PGP.MATERIAL IN {sku_names}")
    
    conditions.append("CLEANSHEET_OPPORTUNITY > 0")  # Always required
    conditions.append("PGP.YEAR >= EXTRACT(YEAR FROM CURRENT_DATE) - 1")

    # If there are any conditions, append them to the query
    if conditions:
        parametric_cost_modeling_query += " WHERE " + " AND ".join(conditions)

    parametric_cost_modeling_query += '''
    ORDER BY
        YEAR DESC,
        QUARTER ASC,
        MONTH ASC,
        PGP.CLEANSHEET_OPPORTUNITY DESC,
        COUNTRY ASC,
        PLANT ASC,
        CATEGORY ASC,
        SUPPLIER ASC,
        MATERIAL ASC
    '''
    if not sku_names:
        parametric_cost_modeling_query += '''
        LIMIT 5
        '''
    return parametric_cost_modeling_query


@log_time
def get_price_arbitrage_query(supplier_name=None, sku_names=None):

    price_arbitrage_query = '''
        WITH BASE_TABLE AS (
        SELECT
            YEAR(TO_DATE(B.DIM_DATE, 'YYYYMMDD')) AS YEAR_,
            QUARTER(TO_DATE(B.DIM_DATE, 'YYYYMMDD')) AS QUARTER,
            MONTHNAME(TO_DATE(B.DIM_DATE, 'YYYYMMDD')) AS MONTH,
            SC.TXT_CATEGORY_LEVEL_2 AS CATEGORY,
            C.TXT_MATERIAL TXT_MATERIAL,
            A.DIM_MATERIAL DIM_MATERIAL,
            A.DIM_SUPPLIER,
            D.TXT_SUPPLIER,
            E.TXT_COUNTRY,
            A.DIM_COUNTRY,
            F.TXT_INCOTERM,
            A.DIM_INCOTERM,
            A.DIM_PLANT,
            G.TXT_PLANT,
            SUM(A.MES_SPEND_CURR_1) AS SPEND,
            SUM(A.MES_QUANTITY) AS QUANTITY,
            CASE
                WHEN SUM(A.MES_QUANTITY) > 0 THEN SUM(A.MES_SPEND_CURR_1) / SUM(A.MES_QUANTITY)
                ELSE 0
            END AS PRICE_AVG
        FROM
            DATA.VT_C_FACT_INVOICEPOSITION_MULTIPLIED A
            JOIN  DATA.VT_DIM_PERIOD B ON B.DIM_DATE = A.DIM_DATE
            JOIN DATA.VT_C_DIM_MATERIAL_TEMP C ON C.DIM_MATERIAL = A.DIM_MATERIAL
            JOIN DATA.VT_C_DIM_SUPPLIER D ON D.DIM_SUPPLIER = A.DIM_SUPPLIER
            JOIN DATA.VT_DIM_SUPPLIERCOUNTRY E ON E.DIM_COUNTRY = A.DIM_COUNTRY
            JOIN DATA.VT_DIM_INCOTERM F ON F.DIM_INCOTERM = A.DIM_INCOTERM
            JOIN DATA.VT_DIM_PLANT G ON G.DIM_PLANT = A.DIM_PLANT
            JOIN DATA.VT_C_DIM_SOURCINGTREE_TECHCME SC ON SC.DIM_SOURCING_TREE = A.DIM_SOURCING_TREE
        GROUP BY
            C.TXT_MATERIAL,
            A.DIM_MATERIAL,
            A.DIM_SUPPLIER,
            D.TXT_SUPPLIER,
            E.TXT_COUNTRY,
            F.TXT_INCOTERM,
            G.TXT_PLANT,
            A.DIM_COUNTRY,
            A.DIM_INCOTERM,
            A.DIM_PLANT,
            SC.TXT_CATEGORY_LEVEL_2,
            YEAR(TO_DATE(B.DIM_DATE, 'YYYYMMDD')),
            MONTHNAME(TO_DATE(B.DIM_DATE, 'YYYYMMDD')),
            QUARTER(TO_DATE(B.DIM_DATE, 'YYYYMMDD'))
    ),
    MIN_PRICE_TABLE AS (
        SELECT
            YEAR_,
            QUARTER,
            MONTH,
            DIM_MATERIAL,
            TXT_COUNTRY,
            DIM_INCOTERM,
            DIM_PLANT,
            DIM_COUNTRY,
            MIN(PRICE_AVG) AS MIN_AVG_PRICE
        FROM
            BASE_TABLE
        GROUP BY
        YEAR_,
        QUARTER,
            MONTH,
            DIM_MATERIAL,
            TXT_COUNTRY,
            DIM_COUNTRY,
            DIM_INCOTERM,
            DIM_PLANT
    ),
    MIN_PRICE_AVG AS (
        SELECT
            A.YEAR_ AS YEAR,
            A.QUARTER,
            A.MONTH,
            A.CATEGORY,
            A.TXT_MATERIAL,
            A.DIM_MATERIAL,
            A.DIM_SUPPLIER,
            A.TXT_SUPPLIER,
            A.TXT_COUNTRY,
            A.TXT_INCOTERM,
            A.TXT_PLANT,
            A.DIM_COUNTRY,
            A.DIM_INCOTERM,
            A.DIM_PLANT,
            SPEND,
            QUANTITY,
            PRICE_AVG AS PRICE_AVERAGE,
            B.MIN_AVG_PRICE
        FROM
            BASE_TABLE A
            JOIN MIN_PRICE_TABLE B ON B.YEAR_ = A.YEAR_ AND B.QUARTER =  A.QUARTER AND B.MONTH = A.MONTH AND B.DIM_MATERIAL = A.DIM_MATERIAL
            AND B.DIM_COUNTRY = A.DIM_COUNTRY AND A.DIM_INCOTERM=B.DIM_INCOTERM AND A.DIM_PLANT=B.DIM_PLANT
    )
    SELECT
        YEAR,
        QUARTER,
        MONTH,
        TRIM(CATEGORY) AS CATEGORY,
        TRIM(TXT_COUNTRY) AS COUNTRY,
        TRIM(TXT_PLANT) AS PLANT,
        TRIM(TXT_SUPPLIER) AS SUPPLIER,
        TRIM(TXT_MATERIAL) AS MATERIAL,
        TRIM(TXT_INCOTERM) AS INCOTERM,
        SPEND,
        QUANTITY,
        ROUND(MIN_AVG_PRICE, 2) AS MINIMUM_AVERAGE_PRICE,
        ROUND(PRICE_AVERAGE,2) AS PRICE_AVERAGE,
        ROUND((SPEND - (QUANTITY * MIN_AVG_PRICE)), 2) PRICE_ARBITRAGE,
            ROUND(
                (
                    (SPEND - (QUANTITY * MIN_AVG_PRICE)) * 100 / SPEND
                ),
                2
            )PRICE_ARBITRAGE_PERCENTAGE
    FROM MIN_PRICE_AVG'''
    # WHERE
    #     SUPPLIER = '{supplier}' 
    #     AND MATERIAL in {sku_names} 
    #     AND CLEANSHEET_OPPORTUNITY >0
    
    conditions = []
    
    if supplier_name:
        conditions.append(f"TRIM(TXT_SUPPLIER) = '{supplier_name}'")
    
    if sku_names:
        # formatted_sku = ", ".join(f"'{sku}'" for sku in sku_names)
        conditions.append(f"TRIM(TXT_MATERIAL) IN {sku_names}")
    
    conditions.append("YEAR >= EXTRACT(YEAR FROM CURRENT_DATE) - 1")

    # If there are any conditions, append them to the query
    if conditions:
        price_arbitrage_query += " WHERE " + " AND ".join(conditions)

    price_arbitrage_query += '''
    ORDER BY
        YEAR DESC,
        QUARTER ASC,
        MONTH ASC,
        PRICE_ARBITRAGE_PERCENTAGE DESC
    '''
    if not sku_names:
        price_arbitrage_query += '''
        LIMIT 5
        '''
    return price_arbitrage_query
