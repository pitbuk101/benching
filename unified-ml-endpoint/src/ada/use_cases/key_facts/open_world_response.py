import datetime
from typing import Any
import os
import json
import openai
from ada.utils.logs.logger import get_logger
import requests
from bs4 import BeautifulSoup
import re
from duckduckgo_search import DDGS

log = get_logger("key_facts-v3")
# from loguru import logger as log

BASE_URL = os.environ.get("OPENAI_BASE_URL")
API_KEY = os.environ.get("LLM_OPENAI_API_KEY")

def routing_prompt(query: str) -> Any:
    """
        Prompt for routing user query to Text2SQL or GeneralPurpose

    Args:
        query (str): User's query

    Returns:
        str
    """
    return f"""
    You will be provided with a user's query.You need classify user's query into two of the following categories:
    1. Text2SQL: "Queries which need to go to the text2sql model"
    2. GeneralPurpose: "Queries which can be answered by the general purpose model"

    ### MANDATORY RULES ###
    1. If the questions are related to or similar to below mentioned keywords, then it should be classified as `Text2SQL`
        - Spends
        - Suppliers
        - Market Price
        - Savings
        - Top Suppliers
        - Top Spends
        - Current Spends
        - Tail Spends
        - Key Suppliers
        - Savings
        - Oppurtunities
        - Total Oppurtunities
        - HCC LCC
        - Price Arbitrage
        - Rate Harmonization
        - OEM Non OEM
        - Supplier Consolidation
        - Clean Sheet
        - Payment Term Standardization
        - Unused Discount
        - Cost Drivers
        - Raw Material
        - Price Drivers
        - Contracted Spend
        - Non Contracted Spend
        - Forecasting
        - SKU
        - SKUS
        - Materials
        - Purchase Orders
        - PO
        - Cost
        - Unit of Measure
        - Purchase
        - Invoice
        - Market Size
        - Buyer Power
        - Supplier Power
        - Market Volatility
        - Parametric Cost Modeling
        - Rate Harmonization
        - Agency Fees Benchmark
        - Agency Fees Benchmarking
        - Agency Cleansheet Benchmark
        - Agency Cleansheet Benchmarking
        - Agency Cleansheet
        - Agency Fees
        - Agency Fees Spend Benchmark
        - Technology Benchmarks 
        - Working Benchmarks 
        - Non Working Benchmarks 
        - Single Operating Unit Supplier Elimination opportunity
        - Bill Rate Benchmarks 
        - Media Price Benchmarks 
        - Deliverable Benchmarks 
        - Labour Rate Benchmarks 
        - Media Commission Benchmarks 
        - Working vs Non Working Benchmarks
        - Low Price Procurement
        - LPP
        - Cost Efficiency
        - Available Net Demand
        - Available Net Supply
        - Optimise
        - Savings
        - Reduce Cost
        - Saved

    2. If the questions are related to below mentioned keywords, then it should be classified as `GeneralPurpose`
        - Weather
        - Time
        - Date
        - Location
        - Alternate Suppliers
        - News
        - Internet
        - Open World
        - Email
        - Greetings
        - Salutations
        
    3. If the question is not related to any of the above mentioned keywords, then it should be classified as `GeneralPurpose`
    4. Questions could be a 'GeneralPurpose' question also even with the above mentioned keywords. In that case, it should be classified as `GeneralPurpose` if the question is very generic for example
        - "How is Price Arbitage calculated?"
        - "What is the meaning of Key Suppliers?"
    5. Questions should be classified to 'GeneralPurpose' if the question is very open ended for example 'How to calculate Payment term standardization ?'

    Query: {query}

    ### Examples ###
    1. "What is my current spends?"
        ### OUTPUT ###
        {{
            "route": "Text2SQL"
        }}
    2. "What is the weather in New York?"
        ### OUTPUT ###
        {{
            "route": "GeneralPurpose"
        }}
    3. "What are top 5 suppliers"
        ### OUTPUT ###
        {{
            "route": "Text2SQL"
        }}
    4. "Alternate Suppliers"
        ### OUTPUT ###
        {{
            "route": "GeneralPurpose"
        }}
    5. "What is my market price of Stainless Steel?"
        ### OUTPUT ###
        {{
            "route": "Text2SQL"
        }}
    6. "What is price arbitrage for SKU"
        ### OUTPUT ###
        {{
            "route": "Text2SQL"
        }}
    7. "What is news for SKF France"
        ### OUTPUT ###
        {{
            "route": "GeneralPurpose"
        }}
    8. "What is current news for SKF France"
        ### OUTPUT ###
        {{
            "route": "GeneralPurpose"
        }}
    9. "Agency Fees Benchmark"
        ### OUTPUT ###
        {{
            "route": "Text2SQL"
        }}

    ### Current Date & Time ###
    {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    ### Output Format ###
        {{
            "route": "..."
        }}
        """, "You are an expert at understanding and structuring natural language queries."
    

def generic_answering_prompt(query: str) -> Any:
    """

    Args:
        query (str): User's query

    Returns:
        str
    """

    return f"""
    Given the user's query answer the questions appropriately. You can also use the internet to search for the latest information if you do not have the latest information.
    
    Query {query}

    ### Mandatory Rules ###
    1. If the user's query is general purpose, then answer the user's query directly.
    2. If the user's query is Procurement Domain Related then answer the user's query with respect to the Procurement Domain.
    3. If the user's query is for writing an email only then write the email in a structured format with proper salutation and closing.
    4. Output should be a MARKDOWN FORMATTED STRING.
    5. Output should be in a STRUCTURED FORMAT.
    6. IF using internet for search ALWAYS provide the category name and search latest information in the internet search query.
    7. IF the user's query is contains greetings or salutations for example "Hi, for category Marketing Svcs" then answer with greetings and salutations in a chat.
    8. IF the user's query is for definitions or full forms, respond with the appropriate definition related to PROCUREMENT DOMAIN.
    
    ### DOMAIN KNOWLEDGE ###
    1. IBC (Intermediate Bulk Container) or CIBC (Intermediate Bulk Container). Do not confuse these terms with other possible meanings. 
        - IBC: Intermediate Bulk Container (a type of container used in supply chains, which includes Composite IBCs, Rigid IBCs (also called Tote Tanks), Flexible IBCs (FIBCs), Stainless Steel IBCs, etc.)
        - CIBC: Composite Intermediate Bulk Container (specific to supply chain and procurement context)

        Specific Examples:
        - "What is the full form of IBC?" (INTERMEDIATE BULK CONTAINER with explanation about types of IBCs in the supply chain)
        - "Tell me about Composite IBC" (provide detailed description of COMPOSITE INTERMEDIATE BULK CONTAINER in supply chain).
        - "What is a CIBC?" (define COMPOSITE INTERMEDIATE BULK CONTAINER)
        - "How are Composite IBCs used in supply chain?" (explain the use of COMPOSITE IBCs in logistics and supply chain operations)
    2. MRO (Maintenance, Repair and Operations)
        MRO refers to the activities and materials necessary to maintain and repair equipment, machinery, or systems in an operational state. This includes a wide range of categories and items used to ensure the smooth operation of industrial and manufacturing systems.

        Specific Examples:
        - "What are the types of MRO categories?" (provide details about the types of MRO categories).
        - "Tell me about bearings in MRO." (provide a detailed explanation of BEARINGS in MRO).
        - "What is HVAC in MRO?" (define HVAC & REFRIGERATION in MRO).
        - "What is the function of pumps in MRO?" (explain the role of PUMPS in MRO).

    ### Examples ###
    1. "What is the weather in New York?"
        ### OUTPUT ###
        "The weather in New York is 25°C"

    2. "What are my alternate suppliers for bearings category?"
        ### OUTPUT ###
        "Your alternate suppliers are ..."
    
    3. "Draft an email for category bearings"
        ### OUTPUT ###
        "Subject: Inquiry and Request for Quotations for Bearings\n\nDear [Supplier's Name],\n\nI hope this message finds you well. I am reaching out to inquire about the availability and pricing of bearings for our ongoing projects. We are currently in the process of evaluating our procurement options and would appreciate it if you could provide us with your latest catalog and any relevant specifications for the bearings you offer.\n\nCould you also include information on bulk purchase discounts, delivery timelines, and any customization options you might have?\n\nThank you for your assistance. Looking forward to your prompt response.\n\nBest regards,\n\n[Your Name]\n[Your Position]\n[Your Company]\n[Contact Information]\n"

    ### CURRENT DATE AND TIME ###
    {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    ### OUTPUT FORMAT ###
        "..."

    """, "You are an intelligent system in procurement domain that can understand and answer questions and can also use internet to fetch information."

def generic_link_prompt(query: str, response: list[str]) -> Any:
    return f""" 
    Given the user's query below. Summarize the response received from the links provided post extraction of text from the links.
    ### Mandatory Rules ###
    1. SUMMARIZATION should only contain the RELEVANT INFORMATION related to the user's query.
    2. SUMMARIZATION should be in a STRUCTURED FORMAT.
    3. SUMMARIZATION should be done for STAKEHOLDER PERSPECTIVE.
    4. Provide ALL links in the response as reference links from where the information is extracted. Provide them in a numbered format in the end.
    5. SUMMARIZATION should be in a MARKDOWN FORMATTED STRING.
    6. ALWAYS mention the source of the information in the response and their date of publication.
    7. ALWAYS convert all the text to ENGLISH LANGUAGE.
    8. SUMMARY should always contain information from each valid link.
    9. SUMMARY should be GRAMMATICALLY CORRECT and should not contain any spelling mistakes.
    10. SUMMARY should be accordance to the user's `query` context.

    Query 
    {query}
    
    Response:
    {response}
    """, "You are an intelligent data summarization system. Given the text and user's query you can summarize and present data in an organised manner."

def generate_generic_summary_response(query: str, response: list[str], model="gpt-4o") -> str:
    prompt, system_prompt = generic_link_prompt(query, response)
    client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)
    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": system_prompt
            },
            {
            "role": "user",
            "content": prompt}],
            seed=42,
            temperature=0,
        model=model,
    )
    return chat_completion.choices[0].message.content


def search_duckduckgo(query):
    log.info(f"Searching DuckDuckGo for query: {query}")
    # query = f"{query} current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    with DDGS() as ddgs:
        results = ddgs.text(query, timelimit="m", safesearch="off", max_results=20)
        # log.info(f"Results: {results}")
        if results:
            return [f"{res['title']} - {res['href']}" for res in results]
        else:
            return "No relevant results found."

def extract_url(text: str) -> str:
    match = re.search(r'https?://\S+', text)
    return match.group(0) if match else ''

def extract_text_from_url(url: str) -> str:
    
    try:
        url = extract_url(url)
        response = requests.get(url, timeout=100)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove scripts and styles
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        # Get text and clean it
        text = soup.get_text(separator=' ', strip=True)
        return text

    except requests.RequestException as e:
        log.info(f"Request failed: {e}")
        return f"Request failed: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


def generate_routing_response(query: str, model="gpt-4o") -> str:
    routing_prompt_output, routing_system_prompt = routing_prompt(query)
    #Initialize a client
    client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)
    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": routing_system_prompt
            },
            {
            "role": "user",
            "content": routing_prompt_output}],
            seed=42,
            temperature=0,
        model=model,
    )
    return chat_completion.choices[0].message.content

def generate_generic_response(query: str, model="gpt-4o", functions=[]) -> str:
        
        generic_prompt_output, generic_system_prompt = generic_answering_prompt(query)
        client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)
        
        response = client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": generic_system_prompt
            },
            {
            "role": "user",
            "content": generic_prompt_output}],
        model="gpt-4o",
        seed=42,
        temperature=0,
        functions=functions,
        function_call="auto"
        )
        # Check if the model wants to call a function
        if response.choices[0].message.function_call:
            function_name = response.choices[0].message.function_call.name
            arguments = response.choices[0].message.function_call.arguments
            
            if function_name == "search_duckduckgo":
                search_results = search_duckduckgo(json.loads(arguments)["query"])
                return search_results
        else:
            return response.choices[0].message.content
        
def open_world_response_generation(query: str) -> str:
    """
    Generate response for the user's query

    Args:
        query (str): User's query

    Returns:
        str
    """
    response = generate_routing_response(query).replace("json", "").replace("```", "")
    response = json.loads(response)
    log.info(f"Routing Response: {response}")
    route = response["route"]
    if route == "GeneralPurpose":
    #     functions = [
    #     {
    #         "name": "search_duckduckgo",
    #         "description": "Searches the internet for information.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "query": {
    #                     "type": "string",
    #                     "description": "The query string to search on the internet"
    #                 }
    #             },
    #             "required": ["query"]
    #         }
    #     }
    # ]
    #     response = generate_generic_response(query, functions=functions)
    #     # log.info(f"Generic Response: {response}")
    #     if isinstance(response, list):
    #         # * extract each link and produce a summary from them
    #         response_str = ""
    #         total_token_count = 0
    #         max_token_count = 128000
    #         # for ind, link in enumerate(response):
    #         valid_link_count = 0
    #         iterator = 0
    #         length = len(response)
    #         log.info(f"Response length: {length}")
    #         while  total_token_count <= max_token_count and iterator < len(response):
    #             log.info(f"Valid link count: {iterator}")
    #             link = response[iterator]
    #             log.info(f"Extracting text from link: {link}")
    #             text = extract_text_from_url(link)
    #             temp_str = f"{iterator+1}: {link} => {text}\n"
    #             token_count = len(temp_str)//4
    #             log.info(f"Token count for this link: {token_count}")
    #             iterator += 1
    #             if token_count >= max_token_count or total_token_count + token_count >= max_token_count:
    #                 log.warning(f"Skipping: {link}")
    #                 log.warning(f"Token limit exceeded. Current token count: {total_token_count + token_count}, max token count: {max_token_count}")
    #                 continue
    #             response_str += temp_str
    #             total_token_count += token_count
    #             valid_link_count += 1
                
    #             log.info(f"Total token count: {total_token_count}")
    #         # log.info(f"Response string: {response_str}")
    #         final_response = generate_generic_summary_response(query, response_str)
    #         final_response = final_response.replace("json", "").replace("markdown", "").replace("```", "")
    #         # final_response = json.loads(final_response)["response"]
    #         return final_response  # Return the constructed response string
        prompt =  f"""
        You are a domain expert assistant in industrial procurement.
        Your job is to answer the question or search the internet for the latest information and provide a structured response.
        
        This includes items across industries such as:
            - IBC / CIBC (Intermediate Bulk Containers) used for transporting and storing bulk liquids and granulated substances.
            - Valves such as gate valves, ball valves, butterfly valves for controlling the flow of liquids or gases in pipelines.
            - Bearings including ball bearings, roller bearings used in rotating machinery to reduce friction and support load.
        
        Your responsibilities include:
            - Interpreting procurement requests (e.g., "Need 100 IBCs for chemical storage").
            - Resolving ambiguous product names or short forms to full, known industry terms (e.g., "LU - Packmittel" could refer to a specific packaging material or plant).
            - Classifying items into categories such as packaging, fluid control systems, mechanical parts, etc.
            - Extracting entities such as item name, quantity, specifications, manufacturer, and application.
            - Understanding domain-specific procurement patterns, such as preferred suppliers, item codes, and quality standards.
        
        Instructions
            - Always clarify ambiguous or shorthand references using domain knowledge or prior known entity mappings.
            - When presented with a partial or noisy query (e.g., “Need 20 LU valves for the new site”), infer the likely meaning based on industry context.
            - Recognize when the query refers to a specific industry vertical like pharmaceuticals, chemicals, or manufacturing, and adjust terminology accordingly.
            - Provide normalized outputs for downstream processing (e.g., procurement automation or ERP system ingestion).
        
        💬 Example Queries
        - “Requesting 500 CIBC containers for ethanol shipment, UN certified.”
        - “Urgent need for SS ball valves, 2-inch size, 10 bar pressure, PN16.”
        - “Need SKF 6203 bearings for maintenance of pump line 3.”
        - “Looking to procure LU Packmittel for plant G102—urgent requirement.”

        Query {query}

        ### MANDATORY RULES
        1. If the user's query is general purpose, then answer the user's query directly.
        2. If the user's query is Procurement Domain Related then answer the user's query with respect to the Procurement Domain.
        3. Avoid providing any extra text except for the answer to the user's query.
        """
        client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)
        response = client.responses.create(
            model="gpt-4.1",
            tools=[{ "type": "web_search_preview" }],
            input=prompt,
        )
        if response.output[0].type == "message":
            message = response.output[0].content[0].text
            log.info(f"GPT Response: {message}")
            return message
        else:
            message = response.output[1].content[0].text
            log.info(f"Internet search results: {message}")
            # log.info(f"Response: {response}")
        log.info(f"Response: {message}")
        return message
        # output = json.loads(response)["response"]
        
        # try:

        #     output = json.loads(response)["response"]
        # except json.JSONDecodeError as e:
        #     output = json.loads(response.replace("\n", "_"))['response'].replace("_", "\n")
    
    return route



if __name__ == "__main__":
    query = "Write me an email, for category 'Marketing Svcs'"
    response = open_world_response_generation(query)
    print(f"Response: {response}")