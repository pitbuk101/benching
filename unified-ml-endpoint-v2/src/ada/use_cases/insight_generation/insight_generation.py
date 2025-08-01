import sys
import pathlib
from pathlib import Path
import re
from insight_utils import json_to_excel, extract_json,process_insight_queries, get_linked_insights, find_related_insights, objective_mapping, insert_insights_master, insert_negotiation_insights
import json
import ast
import uuid
from datetime import datetime
from sf_connector import SnowflakeClient

current_file = Path(__file__)
sys.path.append(str(current_file.parents[3]))

import asyncio
from ada.use_cases.key_facts_chatbot.kf_chatbot import kf_chatbot
from ada.use_cases.key_facts_chatbot.datamodels import QueryRequest


from prompts import generate_insights_query_prompt,generate_insights_prompt,generate_top_ideas_prompt,extract_impact_prompt, generate_rca_prompt,extract_supplier_sku_prompt
from ada.components.llm_models.generic_calls import generate_chat_response_with_chain
from ada.utils.config.config_loader import read_config

insight_generation_conf = read_config("use-cases.yml")["insight_generation"]
insight_model_conf = read_config("use-cases.yml")["insight_generation"]["model"]
analytics_conf = insight_generation_conf["analytics"]

sf_client = SnowflakeClient()

def generate_insights_query():

    '''
    Generates insights query for every combination of analytics,segment and category in configuration file.
    Args:
        None
    Returns:
        processed_data: List of dictionaries containing analytics_name,segment,cols,insight_query and category.
    '''
    
    insight_queries = []
    processed_data = []

    for analytics in analytics_conf:
        prompt = generate_insights_query_prompt(analytics, segment=analytics_conf[analytics]["segments"], cols=analytics_conf[analytics]["cols"])
        response = generate_chat_response_with_chain(prompt,temperature=insight_model_conf["temperature"],model=insight_model_conf["model_name"])
        
        response = extract_json(response)
        insight_queries.extend(response)

    processed_data = process_insight_queries(insight_queries, insight_generation_conf)

    dumped_json = json.dumps(processed_data, indent=5)

    with open(f"{current_file.parent}/checkpoint1.json", "w") as file:
        file.write(dumped_json)
    
    return processed_data


def generate_insights():

    '''
    Generates insights for every insight query.
    Args:
        None
    Returns:
        insights: List of dictionaries containing analytics_name,segment,cols,insight_query,category,sql and data.
    '''

    insights = []
    processed_data = generate_insights_query()

    # with open (f"{current_file.parent}/checkpoint1fix.json", "r") as file:
    #     processed_data = json.load(file)

    processed_data = process_insight_queries(processed_data, insight_generation_conf)

    for item in processed_data: 

        # if item["category"] == "Bearings":
        # Send query to key facts chatbot and get response data and generated SQL

        query = f"""{item["insight_query"]}"""
        request = QueryRequest(query=query)
        kf_response = asyncio.run(kf_chatbot(request))

        try:
            
            item["data"] = kf_response['result']['data']
            item['sql'] = kf_response['sql']
        
            if len(kf_response['result']['data']) == 0 or kf_response['result']['data'] == [[None]]:
                item["insight"] = "NULL"
                insights.append(item)
            else:
                item = str(item).replace("{", "{{").replace("}", "}}")

                insight_prompt = generate_insights_prompt(data=str(item))
                response = generate_chat_response_with_chain(insight_prompt,temperature=insight_model_conf["temperature"],model=insight_model_conf["model_name"])
                print(response)
                match = re.search(r"```dict(.*?)```", response, re.DOTALL)
                if match:
                    dict_str = match.group(1).strip()  
                    data_dict = ast.literal_eval(dict_str)

                    data_dict["data"] = kf_response['result']['data']
                    data_dict['sql'] = kf_response['sql']

                    insights.append(data_dict)     

            with open(f"{current_file.parent}/checkpoint2.json", "w") as file:
                json.dump(insights, file, indent=4)

        except Exception as e:
            print("Error:",e)    

    return insights


def generate_rca(insights:dict):
    """
    Generate RCA for each insights using analytics, linked insights and related insights
    Args:
        insights (dict): Insights to generate RCA for
    Returns
        insights: List of dictionaries containing rca,top_idea,category,analytic_name,title,description,impact,update_info and linked_insights.
    """

    output = []


    insights = find_related_insights(insights)

    for insight in insights:
        if insight["insight"] == "NULL":
            insight["rca"] = {}
            output.append(insight)
            continue

        prompt = generate_rca_prompt(insight["analytics_name"],insight["insight"],insight["linked_insights"],insight["related_insights"])
        response = generate_chat_response_with_chain(prompt,temperature=insight_model_conf["temperature"],model =insight_model_conf["model_name"])

        match = re.search(r"```dict(.*?)```", response, re.DOTALL)
        if match:
            dict_str = match.group(1).strip()  
            data_dict = ast.literal_eval(dict_str)
            insight["rca"] = data_dict 

        output.append(insight)   

        with open(f"{current_file.parent}/checkpoint3.json", "w") as file:
            json.dump(output, file, indent=4)

    return output


def extract_supplier_sku_details(insights:json):

    all_insights = []

    for insight in insights:

        try:
            
            if insight["insight"] == "NULL":
                insight["supplier_sku_information"] = {"supplier": [], "sku": []}
                insight["id"] = str(uuid.uuid4())
                insight["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                all_insights.append(insight)
                continue 

            prompt = extract_supplier_sku_prompt(insight["insight"])

            response = generate_chat_response_with_chain(prompt,temperature=insight_model_conf["temperature"],model=insight_model_conf["model_name"])
            match = re.search(r"```dict(.*?)```", response, re.DOTALL)
            if match:
                dict_str = match.group(1).strip()  
                data_dict = ast.literal_eval(dict_str)
                insight["supplier_sku_information"] = data_dict 
                insight["id"] = str(uuid.uuid4())
                insight["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                all_insights.append(insight)
            else:
                insight["supplier_sku_information"] = {"supplier": [], "sku": []}
                insight["id"] = str(uuid.uuid4())
                insight["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                all_insights.append(insight)

            with open (f"{current_file.parent}/insights.json", "w") as file:
                json.dump(all_insights, file, indent=4, ensure_ascii=False)

        except Exception as e:
            insight["supplier_sku_information"] = {"supplier": [], "sku": []}
            insight["id"] = str(uuid.uuid4())
            insight["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            all_insights.append(insight)
            print("Error",e)

    return all_insights


def extract_impact(insights:json):

    all_insights = []

    for insight in insights:

        try:
            
            if insight["insight"] == "NULL":
                insight["impact"] = []
                all_insights.append(insight)
                continue 

            prompt = extract_impact_prompt(insight["insight"])
            response = generate_chat_response_with_chain(prompt,temperature=insight_model_conf["temperature"],model=insight_model_conf["model_name"])
            match = re.search(r"```dict(.*?)```", response, re.DOTALL)
            if match:
                dict_str = match.group(1).strip()  
                data_dict = ast.literal_eval(dict_str)
                insight.update(data_dict)
                all_insights.append(insight)
            else:
                insight["impact"] = []
                all_insights.append(insight)

            # with open (f"{current_file.parent}/updated_results.json", "w") as file:
            #     json.dump(all_insights, file, indent=4, ensure_ascii=False)

        except Exception as e:
            insight["impact"] = []
            all_insights.append(insight)
            print("Error",e)

    return all_insights


def generate_top_ideas():
    '''
    Generates top ideas for every insight.
    Args:
        None
    Returns:
        top_ideas: List of dictionaries containing top_idea_id,category,analytic_name,title,description,impact,update_info,linked_insights.
    '''

    data = generate_insights()

    insights = get_linked_insights(data)
    insights = generate_rca(insights)
    
    insights = extract_impact(insights)
    insights = objective_mapping(insights)
    insights = extract_supplier_sku_details(insights)

    with open (f"{current_file.parent}/insights.json", "r") as file:
        insights = json.load(file)
        
    processed_insights = set()
    all_insights = []

    for insight in insights:
        if insight["insight"] in processed_insights:
            continue 
        
        if insight["insight"] == "NULL":
            insight["top_ideas"] = []
            all_insights.append(insight)
            continue 

        prompt = generate_top_ideas_prompt(insight["insight"],insight["linked_insights"],insight["analytics_name"])
        response = generate_chat_response_with_chain(prompt,temperature=insight_model_conf["temperature"],model=insight_model_conf["model_name"])
        response = extract_json(response)
        insight["top_ideas"] =  response

        for linked_insight_key in insight["linked_insights"]:
            linked_insight = next((item for item in insights if item["insight"] == linked_insight_key), None)
            if linked_insight:
                linked_insight["top_ideas"] = response  
                all_insights.append(linked_insight)
                processed_insights.add(linked_insight_key)

        all_insights.append(insight)
        processed_insights.add(insight["insight"])
          
        with open (f"{current_file.parent}/topIdeas.json", "w") as file:
            json.dump(all_insights, file, indent=4, ensure_ascii=False)

    return all_insights


if __name__ == "__main__":
    insights = generate_top_ideas()
    
    # json_to_excel("/Users/Rishabh_Mohata/Desktop/Mckinsey/orp-genai/src/ada/use_cases/insight_generation/topIdeas.json","/Users/Rishabh_Mohata/Desktop/Mckinsey/orp-genai/src/ada/use_cases/insight_generation/topIdeas.xlsx")
    # with open (f"{current_file.parent}/topIdeas.json", "r") as file:
    #     insights = json.load(file)

    for insight in insights:
        insert_insights_master(sf_client,insight)
        insert_negotiation_insights(sf_client,insight)

            



















