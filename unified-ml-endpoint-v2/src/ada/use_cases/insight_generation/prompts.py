"""
Prompts for Insight Generation 
"""

from langchain_core.prompts import PromptTemplate
import pandas as pd
import json


def base_insights_query_prompt():
    """ Base prompt for generating insight queries"""

    base_prompt = """ You are an expert in procurement analytics. Your task is to analyze procurement and sourcing data columns to 
    generate actionable insight queries across multiple dimensions that can help procurement managers make data-driven decisions.
    The insight queries should focus on uncovering opportunities for cost reduction, supplier optimization, payment term improvements, and 
    procurement efficiency.

    """

    return base_prompt

def generate_insights_query_prompt(analytics_name: str, segment:list[str], cols:list[str]) -> PromptTemplate:
    """
    Takes the analytic name and gives the prompts for generating the insight queries 
    Args:   
        analytics_name: (str): Name of the analytics (Supplier Consolidation, OEM, Parametric Cost Modeling etc.)
        segment (list(str)): List of segments for the analytics (Supplier, SKU, Plant, Region)
        cols (list(str)): List of columns to be considered for generating the insight queries
    Returns
        (PromptTemplate): LLM prompt for generating the insight queries
    """
    try:

        base_prompt = base_insights_query_prompt()
        cols = ", ".join(cols)

        if analytics_name == "Supplier Consolidation":
            
            temp_prompt = f"""
            
            Supplier Consolidation is a strategic procurement initiative that aims to reduce the number of suppliers
            and consolidate the spend with fewer suppliers. 
            
            As an expert in procurement analytics, you are tasked with
            analyzing the given procurement data columns and generate essential insight queries which can eventually be translated into SQL and 
            identifies crucial opportunities for supplier consolidation. 
            You need to analyze and consider the given columns -  {cols} to identify and generate insight queries.
            Your insight queries should focus on the following segments: {segment}.
            You need to generate 10 actionable, unique and **non-overlapping** insight queries on supplier consolidation.
            You must generate a json output with keys insight_query,analytics_name and segment it belongs to. You must only use the given segments.
            You must include examples given below in the final output if you are not able to generate any relevant insight query.
            You MUST keep the analytics_name as {analytics_name} in the final output.

            Example:
            ```json

            [{{{{
                "insight_query": "Identify top 3 suppliers by spend.",
                "analytics_name": "Supplier Consolidation",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Identify top 3 suppliers with highest difference between the ideal supplier spend percentage and actual spend percentage.",
                "analytics_name": "Supplier Consolidation",
                "segment": "Supplier"
            }}}},
            {{{{ 
                "insight_query": "What are the top 3 business units purchasing the highest number of multi-source SKUs?",
                "analytics_name": "Supplier Consolidation",
                "segment": "Supplier"
            }}}},
            {{{{ 
                "insight_query": "Find the top 3 suppliers with consolidation savings opportunities.",
                "analytics_name": "Supplier Consolidation",
                "segment": "Supplier"
            }}}},
            {{{{ 
                "insight_query": "Find the total count of vendors covering the bottom 20% of the spend this year, and what is the average spend per tail vendor?",
                "analytics_name": "Supplier Consolidation",
                "segment": "Supplier"
            }}}},
            {{{{ 
                "insight_query": "Find is the number of vendors covering the top 80% of the spend this year, and what is the spend per key vendor?",
                "analytics_name": "Supplier Consolidation",
                "segment": "Supplier"
            }}}},
            {{{{ 
                "insight_query": "Determine the top 5 materials with consolidation savings opportunities.",
                "analytics_name": "Supplier Consolidation",
                "segment": "Material"
            }}}},
            ]
            ```
            """

        elif analytics_name == "OEM-Non-OEM Opportunity":

            temp_prompt = f"""

            OEM vs Non-OEM Opportunity analysis helps organizations evaluate procurement efficiencies by comparing Original Equipment 
            Manufacturer (OEM) purchases against Non-OEM alternatives. The goal is to identify cost-saving opportunities, supply chain 
            diversification, and risk mitigation.

            As an expert in procurement analytics, your task is to analyze the given procurement data columns and generate 
            essential insight queries which can eventually be translated into SQL and identify key opportunities for optimizing OEM vs 
            Non-OEM sourcing. 
            You need to analyze and consider the given columns - {cols} to identify and generate quantifiable insight queries.
            Your insight queries should focus on the following segments: {segment}.

            You need to generate 10 actionable, unique and **non-overlapping** quantifiable insight queries on OEM vs Non-OEM Opportunity.
            You must generate a JSON output with keys: insight_query, analytics_name, and segment it belongs to.  
            You must only use the given segments. You may include examples given below in the final output.

            Example: 
            ```json
            [
            [
            {{{{
                "insight_query": "Find the count of OEM and Non-OEM suppliers.",
                "analytics_name": "OEM vs Non-OEM Opportunity",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Give the total amount spent on OEM and Non-OEM materials sepaertely.",
                "analytics_name": "OEM vs Non-OEM Opportunity",
                "segment": "Material"
            }}}},
            {{{{
                "insight_query": "Find my top 3 OEM suppliers on which I have spent the most amount.",
                "analytics_name": "OEM vs Non-OEM Opportunity",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Find top 3 materials where Non-OEM alternatives exist with most cost savings.",
                "analytics_name": "OEM vs Non-OEM Opportunity",
                "segment": "Material"
            }}}},
            {{{{
                "insight_query": "What is the total opportunity via transferring OEM spend to Non-OEM spend?",
                "analytics_name": "OEM vs Non-OEM Opportunity",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "What are the 5 single sourced SKUs from OEM vendors?",
                "analytics_name": "OEM vs Non-OEM Opportunity",
                "segment": "Material"
            }}}},
            {{{{
                "insight_query": "Identify top 3 materials with the most Non-OEM cost savings potential.",
                "analytics_name": "OEM vs Non-OEM Opportunity",
                "segment": "Material"
            }}}},
            {{{{
                "insight_query": "Identify top 3 materials procured exclusively from OEMs.",
                "analytics_name": "OEM vs Non-OEM Opportunity",
                "segment": "Material"
            }}}},
            {{{{
                "insight_query": "Determine the percentage of total spend on oem suppliers versus non-oem suppliers",
                "analytics_name": "OEM vs Non-OEM Opportunity",
                "segment": "Supplier"
            }}}}
            ]
            ```
        """
            
        elif analytics_name == "Parametric Cost Modelling":

            temp_prompt = f"""
            
            Parametric Cost Modeling (PCM) Opportunity Analysis helps organizations evaluate procurement 
            cost efficiency by analyzing parametric cost factors such as should-cost variance, market volatility, 
            and supplier pricing trends. The objective is to identify cost-saving opportunities, cost deviations, and procurement optimizations.
            
            As an expert in cost analytics, your task is to analyze the given procurement data columns and generate unique and **non-overlapping**
            insight queries, which can eventually be translated into SQL, to identify key opportunities for optimizing cost efficiency 
            through Parametric Cost Modeling.

            You need to analyze and consider the given columns - {cols} to identify and generate quantifiable insight queries.
            Your insight queries should focus on the following segments: {segment}

            You need to generate 10 actionable quantifiable insight queries related to Parametric Cost Modelling Analysis.
            You must generate a JSON output with keys: insight_query, analytics_name, and segment.
            You must only use the given segments. You may include examples given below in the final output.
            You MUST keep the analytics_name as {analytics_name} in the final output.

            Example:

            ```json
            [
            {{{{
                "insight_query": "What is the total opportunity via parametric cost modelling?",
                "analytics_name": "Parametric Cost Modelling",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Which suppliers have the highest should-cost variance compared to the actual purchase price?",
                "analytics_name": "Parametric Cost Modelling",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Find the top 3 material/SKU with the highest parametric cost modelling opportunity.",
                "analytics_name": "Parametric Cost Modelling",
                "segment": "Material"
            }}}},
            {{{{
                "insight_query": "Which material or SKU has the biggest cost-saving opportunity, based on the difference between its estimated price and what we actually paid?",
                "analytics_name": "Parametric Cost Modeling",
                "segment": "Material"
            }}}},
            {{{{
                "insight_query": "Determine the suppliers with the largest gap percentage between the first should-cost and the last should-cost.",
                "analytics_name": "Parametric Cost Modelling",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Find the top 5 materials with the highest parametric cost modelling gap per unit",
                "analytics_name": "Parametric Cost Modelling",
                "segment": "Material"
            }}}},
            {{{{
                "insight_query": "Which materials have the largest difference between the previous purchase price and the selected purchase price?",
                "analytics_name": "Parametric Cost Modeling",
                "segment": "Material"
            }}}}
            ]
            ```
            """

        elif analytics_name == "LCC-HCC-Opportunity":

            temp_prompt = f"""

            HCC-LCC (High-Cost Country to Low-Cost Country) opportunity analysis helps organizations evaluate sourcing efficiencies by 
            identifying materials, suppliers, and categories where procurement can be shifted from high-cost regions to low-cost regions. 
            The goal is to identify cost-saving opportunities, optimize supplier selection, and improve overall procurement efficiency.
            
            As an expert in procurement analytics, your task is to analyze the given procurement data columns and generate essential insight queries that can 
            eventually be translated into SQL. These queries should help identify key opportunities for optimizing HCC to LCC sourcing.
            You need to analyze and consider the given columns - {cols} to identify and generate quantifiable insight queries.
            Your insight queries should focus on the following segments: {segment}.
            You need to generate 10 actionable, unique and **non-overlapping** quantifiable insight queries on HCC vs. LCC Opportunity.
            You must generate a JSON output with keys: insight_query, analytics_name, and segment it belongs to.
            You must only use the given segments. You may include examples given below in the final output.

            Example:

            ```json

            [
            {{{{
                "insight_query": "Identify the top 3 suppliers with the highest HCC to LCC opportunity.",
                "analytics_name": "HCC-LCC Opportunity",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "What is the total opportunity via transferring High cost country spend to Low cost country spend?",
                "analytics_name": "HCC-LCC Opportunity",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "List the top 5 SKUs that are currently purchased from both HCC and LCC vendors.",
                "analytics_name": "HCC-LCC Opportunity",
                "segment": "Material"
            }}}},
            {{{{
                "insight_query": "Find the top 5 materials where the highest cost savings can be achieved by switching from HCC to LCC vendors.",
                "analytics_name": "HCC-LCC Opportunity",
                "segment": "Material"
            }}}}
            ]
            ```
        """

        elif analytics_name == "Payment Term Standardization":
            temp_prompt = f"""

            Payment term standardization helps organizations optimize cash flow, reduce financial risk, and identify cost-saving opportunities 
            by analyzing variations in payment terms across suppliers, plants, and categories. 
            The goal is to identify discrepancies, negotiate better terms, and ensure consistency in payment policies.
            As an expert in procurement analytics, your task is to analyze the given procurement data columns and generate essential insight queries 
            that can eventually be translated into SQL. These queries should help identify key opportunities for optimizing payment term standardization.
            
            You need to analyze and consider the given columns - {cols} to identify and generate quantifiable insight queries.
            Your insight queries should focus on the following segments: {segment}.
            You need to generate 10 actionable, unique and **non-overlapping** quantifiable insight queries on Payment Term Standardization Opportunity. 
            You must generate a JSON output with keys: insight_query, analytics_name, and segment it belongs to.
            You must only use the given segments. You may include examples given below in the final output.
            You MUST keep the analytics_name as {analytics_name} in the final output.

            Example:

            ```json
            
            [
            {{{{
                "insight_query": "Find the count of suppliers with respect to different payment terms.",
                "analytics_name": "Payment Term Standardization",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Find the top 3 opportunity when payment terms are moved from 30 or 60 days to 90 days.",
                "analytics_name": "Payment Term Standardization",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "List the top 5 suppliers with the highest potential savings if payment terms were standardized.",
                "analytics_name": "Payment Term Standardization",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Identify the top 5 materials where aligning payment terms with wacc could lead to financial gains",
                "analytics_name": "Payment Term Standardization",
                "segment": "Material"
            }}}},
            {{{{
                "insight_query": "What are the top 3 business units with the highest payment terms standardization opportunity?",
                "analytics_name": "Payment Term Standardization",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Find the top 5 suppliers with the highest number of different payment terms used.",
                "analytics_name": "Payment Term Standardization",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Retrieve the top 5 suppliers where aligning payment terms with WACC could lead to financial gains.",
                "analytics_name": "Payment Term Standardization",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Identify suppliers with the highest discrepancies in payment terms across different plants.",
                "analytics_name": "Payment Term Standardization",
                "segment": "Supplier"
            }}}}
            ]

            """

        elif analytics_name == "Price Arbitrage":
            temp_prompt = f"""

            Price arbitrage analysis helps organizations identify opportunities where the same materials or 
            categories are priced differently across suppliers, regions, or purchasing conditions. 
            The goal is to optimize procurement costs by leveraging lower-cost sources while ensuring supply chain efficiency.

            As an expert in procurement analytics, your task is to analyze the given procurement data columns and generate 
            essential insight queries that can eventually be translated into SQL. These queries should help identify key opportunities for optimizing price arbitrage.
            You need to analyze and consider the given columns - {cols} to identify and generate quantifiable insight queries.
            Your insight queries should focus on the following segments: {segment}.
            You need to generate 10 actionable, unique and **non-overlapping** quantifiable insight queries on Price Arbitrage Opportunity. 
            You must generate a JSON output with keys: insight_query, analytics_name, and segment it belongs to.
            You must only use the given segments. You may include examples given below in the final output.
            You MUST keep the analytics_name as {analytics_name} in the final output.

            Example:

            ```json

            [
            {{{{
                "insight_query": "Identify the top 5 suppliers offering the lowest average price for the most frequently purchased materials.",
                "analytics_name": "Price Arbitrage",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Find the top 3 materials with the highest price arbitrage opportunity across suppliers.",
                "analytics_name": "Price Arbitrage",
                "segment": "Material"
            }}}},
            {{{{
                "insight_query": "Find the top 5 materials where the price difference between minimum and average price is highest.",
                "analytics_name": "Price Arbitrage",
                "segment": "Material"
            }}}},
            {{{{
                "insight_query": "Find the suppliers with the highest variance in pricing based on order volume.",
                "analytics_name": "Price Arbitrage",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Identify the top 3 suppliers with the lowest minimum average price for high-spend materials",
                "analytics_name": "Price Arbitrage",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Identify 3 suppliers with the most significant price differences for the same material across different plants.",
                "analytics_name": "Price Arbitrage",
                "segment": "Supplier"
            }}}}
            ]
        ```
        """

        elif analytics_name == "Early Payments":

            temp_prompt = f"""

            Early Payment Opportunity analysis helps organizations optimize cash flow by identifying potential savings and discounts 
            associated with early payments to suppliers. The goal is to maximize financial efficiency, strengthen supplier relationships, 
            and improve working capital management.

            As an expert in procurement and finance analytics, your task is to analyze the given procurement data columns and generate 
            essential insight queries that can eventually be translated into SQL to identify key opportunities for optimizing early payments.  
            You need to analyze and consider the given columns - {cols} to identify and generate quantifiable insight queries.  
            Your insight queries should focus on the following segments: {segment}.

            You need to generate 10 actionable, unique and **non-overlapping** quantifiable insight queries on Early Payment Opportunity. You must have at least 3 queries for each segment.  
            You must generate a JSON output with keys: insight_query, analytics_name, and segment it belongs to.  
            You must only use the given segments. You may include examples given below in the final output.

            You MUST keep the analytics_name as {analytics_name} in the final output.

            Example:  
            ```json
            [
            [
            {{{{
                "insight_query": "Find the top 5 suppliers with the highest early payment opportunity value.",
                "analytics_name": "Early Payments",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Find the top 3 business units with the highest early payment opportunity value.",
                "analytics_name": "Early Payments",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Find top 3 suppliers where early payment discounts have increased the most.",
                "analytics_name": "Early Payments",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "List the top 5 materials where early payment could generate the most savings.",
                "analytics_name": "Early Payments",
                "segment": "Material"
            }}}}
            {{{{
                "insight_query": "Identify the top 5 quarters with the highest early payment discount adoption rate.",
                "analytics_name": "Early Payments",
                "segment": "Time Period"
            }}}},
            {{{{
                "insight_query": "Find the years where early payment adoption had the highest growth rate.",
                "analytics_name": "Early Payments",
                "segment": "Time Period"
            }}}},
            {{{{
                "insight_query": "Retrieve the top 3 months with the highest total early payment savings achieved.",
                "analytics_name": "Early Payments",
                "segment": "Time Period"
            }}}}
            ]
            ```
            """


        elif analytics_name == "Unused Discounts":

            temp_prompt = f"""

            Unused Discounts analysis helps organizations identify missed savings opportunities by analyzing available discounts that were not 
            utilized. The goal is to maximize cost savings, enhance procurement efficiency, and improve supplier negotiation strategies.

            As an expert in procurement analytics, your task is to analyze the given procurement data columns and generate 
            essential insight queries which can eventually be translated into SQL to identify key opportunities for reducing unused discounts.  
            You need to analyze and consider the given columns - {cols} to identify and generate quantifiable insight queries.  
            Your insight queries should focus on the following segments: {segment}.

            You need to generate 10 actionable, unique and **non-overlapping** quantifiable insight queries on Unused Discounts.  
            You must generate a JSON output with keys: insight_query, analytics_name, and segment it belongs to.  
            You must only use the given segments. You may include examples given below in the final output.

            You MUST keep the analytics_name as {analytics_name} in the final output.

            Example:  
            ```json
            [
            {{{{
                "insight_query": "Find the total opportunity via unused discounts.",
                "analytics_name": "Unused Discounts",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Identify the top 5 suppliers with the highest unused discount value.",
                "analytics_name": "Unused Discounts",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "What the top 3 business units with the highest unused discounts?",
                "analytics_name": "Unused Discounts",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Retrieve the top 3 suppliers where the gap between possible and utilized discounts is the highest.",
                "analytics_name": "Unused Discounts",
                "segment": "Supplier"
            }}}},
            {{{{
                "insight_query": "Find top 3 materials where more than 50% of possible discounts were left unused.",
                "analytics_name": "Unused Discounts",
                "segment": "Material"
            }}}},
            {{{{
                "insight_query": "Identify the top 5 quarters where unused discounts reached their peak.",
                "analytics_name": "Unused Discounts",
                "segment": "Time Period"
            }}}},
            {{{{
                "insight_query": "Find the top 3 years where unused discounts increased the most.",
                "analytics_name": "Unused Discounts",
                "segment": "Time Period"
            }}}},
            {{{{
                "insight_query": "Retrieve the top 3 months with the highest total unused discount value.",
                "analytics_name": "Unused Discounts",
                "segment": "Time Period"
            }}}}
            ]
            ```
            """

        else:
            raise ValueError("Invalid analytics type.")

        prompt = base_prompt + temp_prompt

        return PromptTemplate.from_template(prompt)
    
    except Exception as e:
        print("Error",e)
        return None

def generate_insights_prompt(data: dict) -> PromptTemplate:

    """
    Takes the insight query alongwith data retrieved from Snowflake and generates the prompt for generating insights
    Args:   
        data: (dict): Data retrieved from Snowflake
    Returns
        (PromptTemplate): LLM prompt for generating the insights
    """

    try: 
        prompt = f"""
                
        You are an expert in procurement analytics with deep expertise in analyzing procurement and sourcing data to generate a single valuable insight. 
        Your task is to provide a concise, high-value insight that help procurement managers to make data-driven decisions using given 
        insight query and data only. Your insight must only answer query based on given supporting data and should not be your interpretation. You may include 
        any extra information eg: days, prior payment term to standard payment term etc. present in the given data to generate a more impactful and complete insight.

        Data: {data}

        Focus Areas:
        Your insight should uncover opportunities related to cost reduction, supplier optimization, payment term improvements, and 
        procurement efficiency.

        Guidelines for Response:

        1. You must understand the given entire data and insight query properly and then present an insight which is logical, easy to understand and complete. 
        2. The insight should be accurate, complete and concise (4 lines max) but highly valuable using the given insight query and data only.  
        3. Your insight **must contain associated numbers**, percentages wherever necessary (MUST mention against what they have been calculated) and **must contain analytic used to formulate the insight**.
        4. Whenever including percentages, you MUST mention what they are calculated against for better clarity.
        5. VERY IMPORTANT: **You must NEVER include any absurd percentages in the output - like greater than 100% or 100% or 0% or negative percentages, else you will be penalized and lead to termination.**
        6. If there is any calculation involved based on provided data, you will do it and provide the insight. 
        7. You will not leave any placeholders in the insight. 
        8. You will represent millions with M, thousands with K and billions with B to represent currency scale. 
        9. Currency scale by default is EUR.
        10. VERY IMPORTANT: **Do not make up any number, only used the provided data and insight query to generate the output.**
        11. Your language must be simple,clearly understandable and actionable for procurement managers.
        
        You MUST refer the below example insight language while generating output.
        
        Example insight language: 

        The top three suppliers collectively account for 75.68% of the total category spend, indicating a high level of supplier concentration. 
        SKF FRANCE dominates the Bearings category with a spend of EUR 18.76M (44.47%), nearly double that of the second-largest supplier, 
        GBM SARL (EUR 10.36M, 24.55%). ERIKS GmbH follows at a distant third with EUR 2.81M (6.66%), highlighting potential opportunities for supplier diversification 
        or negotiation leverage with SKF FRANCE.

        You must ALWAYS use data-backed reasoning to support the insight.
        Ensure the insight is practical, immediately actionable, and specific to procurement.
        Avoid generic statements—each insight must deliver clear value to procurement managers.
        **You must generate the insight by answering the insight query using the data provided.**
        Important: You must only add the insight key and value in the dictionary and not modify anything else.

        Format the response strictly in the following dictionary as follows:

        ```dict
        {{{{
        
            "insight_query": "Your insight here"
            "analytics_name": "Name of the analytics",
            "segment": "Segment it belongs to"
            "category": "Category it belongs to"
            "sql": "SQL query to generate the insight"
            "data": "Data used to generate the insight"
            "insight": "Your insight here"
        }}}}
        ```
        
        """

        return PromptTemplate.from_template(prompt)

    except Exception as e:
        print("Error",e)
        return None


def generate_top_ideas_prompt(insight:str,linked_insights:list,analytics_name:str):
    '''
    Takes insight and associated linked insights and create a top idea for the group using LLM.
    Args:
        insights (json): List of insights generated 
    Returns:
        (PromptTemplate): LLM prompt for generating the top ideas

    '''

    try: 
        prompt = f"""
                
        You are a procurement domain expert with deep knowledge of procurement strategies, cost optimization, and supplier management. You will 
        receive a set of procurement insights based on {analytics_name} analytics. Your task is to process these related insights and 
        generate 2-3 structured and unique refined ideas providing distinct strategic approaches, ensuring clarity, impact, and business relevance for Category Managers based on following
        data. You must make sure that the ideas provide unique and impactful strategic approaches for procurement managers to implement.

        Insight: {insight}
        Linked Insight: {linked_insights}
        Analytics: {analytics_name}

        # Instructions for Generating the "Title"

        1. Make it a concise, actionable one-liner (5-15 words) capturing the most critical action.
        2. Prioritize ideas involving direct supplier engagement (example, negotiation or consolidation).
        3. Keep the title crisp and to the point—avoid unnecessary words.
        4. Do not use generic phrases like “Optimize Procurement Costs through…”
        5. Do not mention category name in the title. Eg: Bearings,Batteries, Chemicals etc.

        # Instructions for Generating the "Description":

        1. Define what the idea aims to achieve (e.g., cost reduction, risk mitigation, efficiency). Avoid phrases like "The objective is..." or "The goal is...".
        2. Utilize insights and linked insights to provide spend distribution, trend analysis, and relevant procurement details. Quantify impact where possible (percentages, cost savings, efficiency gains).
        3. Actionable steps - provide step-by-step actions in a logical sequence ensuring steps are business-specific and avoid generic recommendations.

        Example Input:

        Insight: "The top 3 business units with the highest payment terms standardization opportunity are Complex Assembly SAS (1.03M EUR ), Complex Assembly GmbH (1.01M EUR ), Complex Assembly Intercambiadores (772.48K EUR )."
        Linked Insights: ["For the year 2023, 167 payment terms can be standardized.","The top 3 suppliers with the highest payment terms standardization opportunity are CNC MANUFACTURING TECHNOLOGY FRIEDEMANN (465.81K EUR ), AB SKF (292.87K EUR ), GBM (260.94K EUR )."]
        Analytics: Payment Terms Standardization
        
        Example Output:

        ```json
        [
        {{{{
        "idea": "Focus on Business Units with High Standardization Opportunities",
        "description": "Target the top three business units with the highest payment terms standardization opportunity: Complex Assembly SAS, Complex Assembly GmbH, and Complex Assembly Intercambiadores. Standardizing payment terms across these units can drive significant cost savings by reducing inefficiencies and improving cash flow management. Currently, 167 payment terms can be standardized in 2023, highlighting a strong opportunity. The key step involves identifying suppliers associated with these business units and engaging in negotiations to establish uniform payment terms. A structured implementation will involve assessing existing agreements, securing supplier alignment, and ensuring compliance for long-term financial optimization."
        }}}},
        {{{{
            "idea": "Centralize Payment Terms Governance",
            "description": "Establish a cross-functional payment terms task force responsible for overseeing and enforcing standardization across business units and suppliers. A centralized governance model ensures consistency, prevents ad-hoc deviations, and enhances negotiation leverage with suppliers. The key step involves forming a dedicated team that includes finance, procurement, and legal representatives to assess current agreements and drive policy enforcement. A structured rollout will focus on defining clear standardization policies, monitoring compliance, and continuously optimizing payment terms based on financial data insights."
        }}}},
        {{{{
            "idea": "Leverage Early Payment Discounts",
            "description": "Capitalize on opportunities to optimize cash flow by introducing early payment discounts and dynamic discounting models. This approach allows the company to negotiate discounts with suppliers in exchange for faster payments, generating cost savings while maintaining flexibility. The key step involves identifying suppliers open to discount arrangements, assessing the financial viability of early payments, and implementing an automated system to manage discount-based transactions. A structured rollout will include supplier engagement, financial impact analysis, and phased implementation to balance liquidity management with cost savings."
        }}}}
        ]
        ```

        """

        return PromptTemplate.from_template(prompt)

    except Exception as e:
        print("Error",e)
        return None



def generate_rca_prompt(analytics:str,insight:str,linked_insights:list,related_insights:list) -> PromptTemplate:
    """
    Prompt for generating RCA given the insight's and linked insight

    Args:
        insight_context (dict): Data dictionary containing insight.
    Returns:
        PromptTemplate: PromptTemplate object with a system prompt
    """

    try:

        related_insights = "\n".join(related_insights)
        linked_insights = "\n".join(linked_insights)

        prompt = f"""

        You are a procurement domain expert with deep expertise in analytics and root cause analysis. 
        Your task is to analyze the provided main insight alongwith supporting linked and additional insights step by step and derive key root causes for the main insights.

        You have been provided with the following information:

        Analytics: {analytics}
        Main Insight: {insight}
        Supporting Linked Insights: {linked_insights}
        Additional Insights: {related_insights}

        Step-by-Step Analysis Approach

        Step 1: Clearly understand the main intent of the insight and the context it provides.
        Step 2: Examine the main insight in detail and break it down into key contributing factors.
        Step 3: Analyze the linked and related insights, but only extract the useful information that contributes to the root cause analysis.
        Step 4: Based on the above understanding and procurement domain knowledge, conduct a root cause analysis.

        Output Format & Guidelines

        1. Summarize findings in 2-3 concise points, ensuring no duplication.
        2. Include derived metrics where applicable (e.g., total opportunity value, percentages, averages).
        3. Structure output as follows:

        ```dict
        {{{{
            "heading": "Root Cause Analysis",
            "description": ["root cause 1","root cause 2","root cause 3" ...]
        }}}}

        ```

        Example Output:

        ```dict
        {{{{
            "heading": "Root Cause Analysis",
            "description": ["High Price Variance in Top SKUs: The top 3 SKUs with the highest price variance contribute significantly to procurement inefficiencies.", "Supplier and Geographic Disparities: Multiple suppliers and varied locations lead to pricing inconsistencies.",...]
        }}}}

        """

        return PromptTemplate.from_template(prompt)

    except Exception as e:
        print("Error",e)
        return None
    


def extract_supplier_sku_prompt(insight:str) -> PromptTemplate:
    """
    Generates a prompt template for extracting supplier and SKU names from given text data.

    Args:
        insight (str): LLM generated insight

    Returns:
        PromptTemplate: A template for the prompt to extract supplier and SKU names.
    """

    try:

        sys_prompt = f"""

        You are an intelligent name-entity-extraction assistant bot.
        Your task is to extract the supplier and sku names from the text user gives you
        by following the below instructions -

        Extraction-Instructions:
            1. Supplier and SKU names may or may not be present in the text.
            2. You need to extract all the Supplier and SKU names
            3. If the text doesn't contains Supplier and SKU names, give an empty list as value for supplier and sku key in the final output.

        Output Instructions:
            1. You must return the output in the dictionary format as shown below:
            ```dict
            {{{{
            "supplier": ["supplier1", "supplier2",..],
            "sku": ["sku1", "sku2", "sku3",..],
            }}}}
            ```
            3. You must ONLY return the dictionary in PROPER FORMAT as the final output.

        You can refer to the below examples:

        Examples :
            Input: "Faber Industries - Analysis: Contract payment terms are 15 days less than the benchmark value"
            Output: 
            ```dict
            {{{{
            "supplier": ["Faber Industries"], 
            "sku": []
            }}}}
            ```

            Input: "The material/SKU with the third-highest Price Variance is FORGED RING SA-105N with a value of 99.1K EUR."
            Output: 
            ```dict
            {{{{
            "supplier": [], 
            "sku": ["FORGED RING SA-105N"]
            }}}}

            Input: "For the latest year, the top 5 vendors by OEM spend are Nanjing Dingyang Mechanical and electrical equipment co., LTD, NSI PLASTIC, Faber Industrietechnik GmbH, SKF FRANCE, PTP INDUSTRY SAS."
            Output: ```dict
            {{{{
            "supplier": ["Nanjing Dingyang Mechanical and electrical equipment co., LTD", "NSI PLASTIC", "Faber Industrietechnik GmbH", "SKF FRANCE", "PTP INDUSTRY SAS"], 
            "sku": []
            }}}}

            User : Extract the Supplier and SKU from - {insight}

        """

        return PromptTemplate.from_template(sys_prompt)


    except Exception as e:
        print("Error",e)
        return None
    


def extract_impact_prompt(insight: str) -> PromptTemplate:
    """
    Generates a prompt template for extracting impact from given insight.

    Args:
        insight (str): LLM generated insight

    Returns:
        PromptTemplate: A template for the prompt to extract impact amounts.
    """

    sys_prompt = f"""

    You are an intelligent name-entity-extraction assistant bot.
    Your task is to extract impact amounts (monetary values, cost savings, financial figures) from the text user gives you
    by following the below instructions -

    Extraction Instructions:
        1. Impact amounts may or may not be present in the text.
        2. You need to extract all numerical values that represent financial impact (e.g., savings, costs, price variances, expenditures).
        3. Ensure that extracted amounts retain their currency symbols (if mentioned) and units (e.g., EUR, USD, K, M).
        4. If the text does not contain any impact amounts, return an empty list for the "impact" key in the final output.

    Output Instructions:
        1. You must return the output in the dictionary format as shown below:
        ```dict
        {{{{
        "impact": ["amount1", "amount2", ...]
        }}}}
        ```
        2. You must ONLY return the dictionary in PROPER FORMAT as the final output.

    You can refer to the below examples:

    Examples :
        Input: "The cost savings achieved from this initiative is 1.2M USD."
        Output: 
        ```dict
        {{{{
        "impact": ["1.2M USD"]
        }}}}
        ```

        Input: "The material with the third-highest Price Variance is FORGED RING SA-105N with a value of 99.1K EUR."
        Output: 
        ```dict
        {{{{
        "impact": ["99.1K EUR"]
        }}}}

        Input: "For the latest year, total OEM expenditure reached 450M EUR."
        Output: 
        ```dict
        {{{{
        "impact": ["450M EUR"]
        }}}}

        Input: "No significant cost fluctuations were observed."
        Output: 
        ```dict
        {{{{
        "impact": []
        }}}}

        User: Extract the impact amount from - {insight}

    """

    return PromptTemplate.from_template(sys_prompt)