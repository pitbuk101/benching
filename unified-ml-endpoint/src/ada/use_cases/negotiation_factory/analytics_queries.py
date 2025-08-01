from ada.utils.logs.time_logger import log_time

def get_payment_terms_query(supplier_name=None, sku_names=None):
    payment_terms_query = '''SELECT YEAR, QUARTER, MONTH, CATEGORY, SUPPLIER, COUNTRY, PLANT, COMPANY, MATERIAL, 
    INCOTERM, PAYMENT_TERM, PAYMENT_TERM_GROUP, DESIRED_PAYMENT_TERM_DAYS as SELECTED_PAYMENT_TERM_DAYS, WACC, MAXPAYMENTDAYS, SPEND,
      POTENTIAL_SAVINGS FROM DATA.T_C_PAYMENT_TERMS_STANDARDIZATION'''

    conditions = []

    if supplier_name:
        conditions.append(f"SUPPLIER = '{supplier_name}'")

    if sku_names:
        conditions.append(f"MATERIAL IN {sku_names}")

    conditions.append("POTENTIAL_SAVINGS > 0")
    conditions.append("YEAR >= EXTRACT(YEAR FROM CURRENT_DATE) - 1")

    if conditions:
        payment_terms_query += " WHERE " + " AND ".join(conditions)

    payment_terms_query += '''
    ORDER BY YEAR DESC, QUARTER ASC, MONTH ASC, CATEGORY ASC, POTENTIAL_SAVINGS DESC
    '''

    # if not sku_names:
    #     payment_terms_query += '''
    #     LIMIT 5
    #     '''

    return payment_terms_query


@log_time
def get_early_payments_query(supplier_name=None, sku_names=None):
    early_payments_query = '''
    SELECT YEAR, QUARTER, MONTH, CATEGORY, SUPPLIER, COUNTRY, PLANT, COMPANY, MATERIAL, PAYMENT_TERM_GROUP, DIFF_EARLY_PAYMENT, TOTAL_SPENDS, MES_DIFF_INVOICE_PAYMENT_DATE_WEIGHTED, EARLY_PAYMENT_OPPORTUNITY FROM DATA.T_C_EARLY_PAYMENT
    '''

    conditions = []

    if supplier_name:
        conditions.append(f"SUPPLIER = '{supplier_name}'")

    if sku_names:
        # formatted_sku = ", ".join(f"'{sku}'" for sku in sku_names)
        conditions.append(f"MATERIAL IN {sku_names}")
    conditions.append("YEAR >= EXTRACT(YEAR FROM CURRENT_DATE) - 1")
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
    # if not sku_names:
    #     early_payments_query += '''
    #     LIMIT 5
    #     '''
    return early_payments_query

@log_time
def get_unused_discount_query(supplier_name=None, sku_names=None):
    unused_discount_query = '''
    SELECT YEAR, QUARTER, MONTH, CATEGORY, SUPPLIER, COUNTRY, PLANT, INCOTERM, PAYMENT_TERM_GROUP, 
           MATERIAL, TOTAL_SPEND, DISCOUNT_POSSIBLE, DISCOUNT, DISCOUNT_NOT_USED 
    FROM DATA.T_C_UNUSED_DISCOUNT
    '''

    conditions = []

    if supplier_name:
        conditions.append(f"SUPPLIER = '{supplier_name}'")

    if sku_names:
        conditions.append(f"MATERIAL IN {sku_names}")

    conditions.append("DISCOUNT_NOT_USED > 0")
    conditions.append("YEAR >= EXTRACT(YEAR FROM CURRENT_DATE) - 1")

    if conditions:
        unused_discount_query += " WHERE " + " AND ".join(conditions)

    unused_discount_query += '''
    ORDER BY YEAR DESC, QUARTER ASC, MONTH ASC, CATEGORY ASC, DISCOUNT_NOT_USED DESC
    '''

    # if not sku_names:
    #     unused_discount_query += '''
    #     LIMIT 5
    #     '''

    return unused_discount_query

@log_time
def get_parametric_cost_modeling_query(supplier_name=None, sku_names=None):
    query = '''
    SELECT YEAR, QUARTER, MONTH, CATEGORY, MATERIAL, SUPPLIER, PLANT, COUNTRY, SPEND, CLEANSHEET_OPPORTUNITY, 
            DIV0(CLEANSHEET_OPPORTUNITY,SPEND) AS PCM_GAP_PERCENTAGE_PER_UNIT
    FROM DATA.T_C_PARAMETRIC_COST_MODELLING
    '''

    conditions = []

    if supplier_name:
        conditions.append(f"SUPPLIER = '{supplier_name}'")

    if sku_names:
        conditions.append(f"MATERIAL IN {sku_names}")

    conditions.append("CLEANSHEET_OPPORTUNITY > 0")
    conditions.append("YEAR >= EXTRACT(YEAR FROM CURRENT_DATE) - 1")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += '''
    ORDER BY YEAR DESC, QUARTER ASC, MONTH ASC, CLEANSHEET_OPPORTUNITY DESC,
             COUNTRY ASC, PLANT ASC, CATEGORY ASC, SUPPLIER ASC, MATERIAL ASC
    '''

    # if not sku_names:
    #     query += '''
    #     LIMIT 5
    #     '''

    return query


@log_time
def get_price_arbitrage_query(supplier_name=None, sku_names=None):
    price_arbitrage_query = '''
    SELECT YEAR, QUARTER, MONTH, CATEGORY, COUNTRY, PLANT, SUPPLIER, MATERIAL, MATERIAL_ID, INCOTERM,
           SPEND, QUANTITY, MINIMUM_AVERAGE_PRICE, PRICE_AVERAGE, PRICE_ARBITRAGE, PRICE_ARBITRAGE_PERCENTAGE
    FROM DATA.T_C_PRICE_ARBITRAGE
    '''

    conditions = []

    if supplier_name:
        conditions.append(f"SUPPLIER = '{supplier_name}'")

    if sku_names:
        conditions.append(f"MATERIAL IN {sku_names}")

    conditions.append("YEAR >= EXTRACT(YEAR FROM CURRENT_DATE) - 1")
    conditions.append("PRICE_ARBITRAGE > 0")

    if conditions:
        price_arbitrage_query += " WHERE " + " AND ".join(conditions)

    price_arbitrage_query += '''
    ORDER BY YEAR DESC, QUARTER ASC, MONTH ASC, PRICE_ARBITRAGE_PERCENTAGE DESC
    '''

    # if not sku_names:
    #     price_arbitrage_query += '''
    #     LIMIT 5
    #     '''

    return price_arbitrage_query
