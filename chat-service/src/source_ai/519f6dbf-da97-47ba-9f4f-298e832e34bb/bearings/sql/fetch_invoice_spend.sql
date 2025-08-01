SELECT SUM(MES_SPEND_CURR_1)
FROM "{{database}}"."{{schema}}"."{{table}}"
WHERE DIM_MATERIAL = '{{sku}}'
    AND DIM_SUPPLIER_STATUS = 'E'
    AND DIM_CONTRACT_REFERENCE='y'
    AND DIM_VALUE_TYPE = 'I'
    AND DIM_DATE >= {{start_date}}
    AND DIM_DATE <= {{end_date}}