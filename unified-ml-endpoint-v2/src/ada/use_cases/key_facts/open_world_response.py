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
    1. If the questions are related below mentioned keywords, then it should be classified as `Text2SQL`
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
        - News
        - Cost Drivers
        - Raw Material
        - Price Drivers
        - Contracted Spend
        - Non Contracted Spend
        - Forecasting 

    2. If the questions are related below mentioned keywords, then it should be classified as `GeneralPurpose`
        - Weather
        - Time
        - Date
        - Location
        - Alternate Suppliers
        
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
                "route": "Text2SQL"
            }}
    8. "What is current news for SKF France"
            ### OUTPUT ###
            {{
                "route": "Text2SQL"
            }}


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
    Given the user's query:

    Query {query}

    ### Mandatory Rules ###
    1. If the user's query is general purpose, then answer the user's query directly.
    2. If the user's query is Procurement Domain Related then answer the user's query with respect to the Procurement Domain.
    3. Output should be a Markdown formatted string.

    ### Examples ###
    1. "What is the weather in New York?"
        ### OUTPUT ###
        {{
        "response": "The weather in New York is 25°C"
        }}

    2. "What are my alternate suppliers for bearings category?"
        ### OUTPUT ###
        {{
        "response": "Your alternate suppliers are ..."
        }}

    ### OUTPUT FORMAT ###
        {{
        "response": "..."
        }}
    """, "You are an intelligent system that can understand and answer questions and can also use internet to fetch information."

def generic_link_prompt(query: str, response: list[str]) -> Any:
    return f""" 
    Given the user's query below. Summarize the response received from the links provided post extraction of text from the links.
    ### Mandatory Rules ###
    1. Suummarization should onle contain the relevant information related to the user's query.
    2. Summarization should be in a structured format.
    3. Summarization should be in a Markdown formatted string.
    
    Query 
    {query}
    
    Response:
    {response}
    
    ### OUTPUT FORMAT ###
        {{
        "response": "..."
        }}
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
        model=model,
    )
    return chat_completion.choices[0].message.content


def search_duckduckgo(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)
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
    route = response["route"]
    if route == "GeneralPurpose":
        functions = [
        {
            "name": "search_duckduckgo",
            "description": "Searches the internet for information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query string to search on the internet"
                    }
                },
                "required": ["query"]
            }
        }
    ]
        response = generate_generic_response(query, functions=functions)
        if isinstance(response, list):
            # * extract each link and produce a summary from them
            response_str = ""
            for ind, link in enumerate(response):
                text = extract_text_from_url(link)
                response_str += f"{ind+1}: {link} => {text}\n"
            final_response = generate_generic_summary_response(query, response_str)
            final_response = final_response.replace("json", "").replace("markdown", "").replace("```", "")
            final_response = json.loads(final_response)["response"]
            return final_response  # Return the constructed response string
        response = response.replace("json","").replace("```", "")
        return json.loads(response)["response"]
    
    return route
