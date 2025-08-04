def generic_normalization_prompt(**kwargs) -> dict:
    """
    A general-purpose prompt for product/service normalisation, returning 7 columns with additional attribute extraction.
    kwargs: Expected to contain 'item_count' and 'batch_items_string'.
    """
    item_count = kwargs.get("item_count", "UNKNOWN_COUNT")
    batch_items_string = kwargs.get("batch_items_string", "NO_ITEMS_PROVIDED")

    system_message = (
        "You are an expert data normalization assistant. You will process raw text and return structured, clean data according to the specified format and instructions."
    )

    user_template = f"""You will receive exactly {item_count} input descriptions.
You must return exactly {item_count} rows. No more, no less.

Each row must contain the following seven columns:
Respond strictly in CSV format with **NO HEADER**:
"Type","Extracted_Quantity","Normalized Description","B2B Query","Attribute_1","Attribute_2","Attribute_3"

Instructions:
- "Type" must be either "Product" or "Service".
- If "Type" is "Service":
    - All other columns ➝ "N/A"
- If "Type" is "Product":
    - "Extracted_Quantity": Extract quantity from the description if clear (e.g., "x10" ➝ 10). If unclear, set to "1".
    - "Normalized Description": Provide a clean, professional normalized description.
    - "B2B Query": Short, precise 10–12 word search query suitable for B2B platforms. Do not include words like 'sourcing' or 'supplier'.
    - "Attribute_1", "Attribute_2", "Attribute_3": Extract clear, structured attributes like "Capacity: 33Ah", "Voltage: 3.7V", "Material: SS304", "Power: 0.5kW". If attributes are not found, return "N/A".

Examples:
Input : "LOWARA HORIZONTAL PUMP-5HMO4S05M, 0.5 KW, 0.60HP, 1 PH FLOW RATE  5.5 M3H @ 21.1 MTRS SS 304. DISCHARGE OUTLET  1 1/4\"X 1\""
Output : "Product","1","Lowara horizontal pump 5HMO4S05M 0.5kW 0.6HP 1-phase 5.5 m³/h at 21.1m SS304 discharge 1 1/4 inch x 1 inch","Lowara SS304 Pump 0.5kW 5.5 m3h 1 phase","Power: 0.5kW","Flow Rate: 5.5 m³/h","Material: SS304"

Input : "REFILLING OF ACETYLENE GAS (GAS CONTENT:5.5KG@200CFT/CYLINDER)"
Output : "Service","N/A","N/A","N/A","N/A","N/A","N/A"

Input : "Manufacturer Rechargeable 3.7V 33Ah Li Ion Battery Pack"
Output : "Product","1","Rechargeable 3.7V 33Ah lithium-ion battery pack","Rechargeable 3.7V 33Ah lithium battery pack","Voltage: 3.7V","Capacity: 33Ah","Type: Li-Ion"

---

Input Descriptions:
{batch_items_string}

---
Now, generate the CSV output of {item_count} rows for the {item_count} descriptions provided above.
"""

    return {"system_message": system_message, "user_template": user_template}


def benchmarking_match_prompt(**kwargs) -> dict:
    """
    A prompt for benchmarking product matching between client queries and scraped products.
    kwargs: Expected to contain 'client_list_str' and 'scraped_list_str'.
    """
    client_list_str = kwargs.get("client_list_str", "NO_CLIENT_QUERIES")
    scraped_list_str = kwargs.get("scraped_list_str", "NO_SCRAPED_PRODUCTS")

    system_message = "You are an expert in matching multilingual product descriptions and translating any non-english product titles to clear, professional English."
    user_template = f"""You are an expert in multilingual product matching for procurement.
Your task is to find the best match from the 'Scraped Products' list for EACH query in the 'Client Queries' list.

**Client Queries:**
{client_list_str}

**Scraped Products:**
{scraped_list_str}

**Instructions:**
1. For each Client Query, find the single best matching Scraped Product.
2. Assign a cosine-like similarity score from 0.0 (no match) to 1.0 (perfect match) with strict caution and precision.
3. **CRITICAL**: Translate the matched Scraped Product's title into clear, professional English:
   - If the title is in Japanese, provide a proper English translation
   - If the title is already in English, keep it as is
   - Focus on the core product name, brand, specifications, and key features
   - Remove promotional text, shipping info, and marketing language
   - Maintain important technical specifications (size, quantity, model numbers)
   - Use proper English grammar and product terminology

**Translation Examples:**
- "【伊藤園】お～いお茶 緑茶 PET 280ml x 48本 （24本入 x 2ケース） 【送料無料】" → "Itoen Oi Ocha Green Tea PET 280ml x 48 bottles (24 bottles x 2 cases)"
- "FLEXTAILGEAR MAX VACUUM PUMP エアポンプ 電動ポンプ 携帯ポンプ 10kpa 2500mah" → "Flextailgear Max Vacuum Pump 10kPa 2500mAh portable electric pump"
- "【送料無料】伊藤園 お〜いお茶 緑茶 280ml×24本" → "Itoen Oi Ocha Green Tea 280ml x 24 bottles"

4. If no good match exists for a client query, you can omit it from the result.

**Output Format:**
Return a single JSON object. This object must contain a key (e.g., "matches") whose value is a JSON array of objects. Each object in the array MUST contain:
- "client_query_id": The original ID of the client query.
- "matched_product_index": The original index of the best matching scraped product.
- "score": The similarity score (0.0 to 1.0).
- "translated_title": The professional English translation of the matched product title.

Example Response:
{{
  "matches": [
    {{"client_query_id": 0, "matched_product_index": 15, "score": 0.83, "translated_title": "Itoen Oi Ocha Green Tea PET 280ml x 48 bottles"}},
    {{"client_query_id": 1, "matched_product_index": 2, "score": 0.65, "translated_title": "Flextailgear Max Vacuum Pump 10kPa 2500mAh"}}
  ]
}}
"""
    return {"system_message": system_message, "user_template": user_template}