import openai
import threading
from datetime import datetime
import os
from dataclasses import dataclass
from openai.types.beta.threads.run import Run
from ada.use_cases.quick_nego import fetch_supplier
from ada.components.db.sf_connector import SnowflakeClient
from ada.utils.logs.logger import get_logger
from typing import Dict, Optional
import json
import time
from ada.use_cases.quick_nego.prompt import ProcurementAdvisorSystem
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = os.environ.get("OPENAI_API_BASE")
API_KEY = os.environ.get("LLM_OPENAI_API_KEY")

logger = get_logger("Quick Nego Agent")


class ProcurementAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)
        self.advisor = ProcurementAdvisorSystem()
    def create_or_get_assistant(self) -> str:
        """Create or retrieve the McKinsey procurement assistant"""
        try:
            response = self.client.beta.assistants.create(
                name="Enhanced Procurement Negotiation Specialist",
                instructions=self.advisor.get_complete_instruction,
                tools=[{"type": "code_interpreter"}],
                model="gpt-4.1"
            )
            self.assistant_id = response.id
            return self.assistant_id
        except Exception as e:
            logger.error(f"Error creating assistant: {e}")
            raise
    
    def create_thread(self):
        thread = self.client.beta.threads.create()
        return thread.id
    
    def get_supplier_information(self, supplier_name: str, tenant_id: str,category:str,skus:list) -> Dict:
        """Get information about the supplier - OPTIMIZED with better threading"""
        start_time = time.time()
        logger.info(f"Starting database queries for supplier: {supplier_name}")
        
        sf_client = SnowflakeClient(tenant_id=tenant_id)
        
        # Use optimized ThreadPoolExecutor with proper error handling
        with ThreadPoolExecutor(max_workers=3, thread_name_prefix="db") as executor:
            # Submit all queries immediately
            insights_future = executor.submit(fetch_supplier.get_supplier_insight, sf_client, supplier_name, category, skus)
            batna_future = executor.submit(fetch_supplier.get_batna_details, sf_client, supplier_name, category)
            zopa_future = executor.submit(fetch_supplier.get_zopa_details, sf_client, supplier_name, category)
            
            # Collect results with error handling
            try:
                supplier_insights = insights_future.result(timeout=15)
            except Exception as e:
                logger.error(f"Insights query failed: {e}")
                supplier_insights = []
            
            try:
                batna = batna_future.result(timeout=15)
            except Exception as e:
                logger.error(f"BATNA query failed: {e}")
                batna = "[]"
            
            try:
                zopa = zopa_future.result(timeout=15)
            except Exception as e:
                logger.error(f"ZOPA query failed: {e}")
                zopa = "[]"
        
        results = {
            "supplier_insights": supplier_insights,
            "batna": batna,
            "zopa": zopa
        }
        
        db_time = time.time() - start_time
        logger.info(f"Database queries completed in {db_time:.2f} seconds")
        return results
    
    def generate_insights_and_objective_parallel(self, supplier_name: str, information: dict) -> Dict:
        """Generate insights and objectives in TRUE parallel - FIXED version with detailed timing"""
        
        # Use ThreadPoolExecutor for parallel LLM calls
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="llm") as executor:
            # Submit both LLM tasks IMMEDIATELY
            logger.info("Submitting insights task...")
            logger.info("Submitting objective task...")
            objective_future = executor.submit(self._generate_objective_optimized, supplier_name=supplier_name,information=information)
            
            # Use as_completed to track progress
            futures = {objective_future: "objective"}
            results_dict = {}
            for future in as_completed(futures, timeout=50):  # Increased timeout
                task_name = futures[future]
                
                try:
                    result = future.result()
                    
                    #logger.info(f"{task_name} retrieved in {task_duration:.2f}s, total time: {completion_times[task_name]:.2f}s")
                    results_dict[task_name] = result
                    
                except Exception as e:
                    logger.error(f"{task_name} generation failed: {e}")
                    if task_name == "insights":
                        results_dict[task_name] = "Analysis unavailable - proceeding with available data"
                    else:
                        results_dict[task_name] = {"objectives": []}
             
        return {
            # "insights": results_dict.get("insights", "Analysis unavailable"),
            "objective": results_dict.get("objective", {"objectives": []})
        }
    
    def _generate_insights_optimized(self, supplier_name: str, information: dict, ) -> str:
        """Optimized insights generation with detailed timing"""
        logger.info(f"INSIGHTS TASK STARTED for {supplier_name}")
        
        try:
            supplier_insights = information.get("supplier_insights")
            prompts = self.advisor.generate_supplier_analysis_prompt(supplier_insights=supplier_insights)
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": prompts.get("system")
                    },
                    {
                        "role": "user",
                        "content": prompts.get("user")
                    }
                ],
                max_tokens=1000,  # Further reduced for speed
                temperature=0.1,
                timeout=20  # Reduced timeout
            )
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Execution failed: {e}")
            return "## Research Unavailable\n\nUnable to gather supplier intelligence at this time. Proceed with standard negotiation approach."
    
    def _generate_objective_optimized(self, supplier_name: str, information: dict, currency_symbol: str = '€') -> dict:
        """Optimized objective generation with detailed timing"""
        logger.info(f"OBJECTIVE TASK STARTED for {supplier_name}")
        
        try:
            prompt = self.advisor.get_objective_prompt(
                supplier_all_insights=information,
                currency_symbol=currency_symbol,
                supplier=supplier_name,
                category="Bearings"
            )
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior procurement analyst. Return valid JSON only with concise objectives."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,  # Further reduced for speed
                temperature=0.1,
                timeout=20  # Reduced timeout
            )
            # Try to parse as JSON
            try:

                result = json.loads(response.choices[0].message.content)
                return result
            except json.JSONDecodeError:
                logger.warning("Objective response was not valid JSON")
                return {"objectives": response.choices[0].message.content}
            
        except Exception as e:
            logger.error(f"Error: {e}")
    def log_agent_token_utilisation(self, thread_id: str, run: Run):
        token_usage = {
            "timestamp": datetime.now().isoformat(),
            "thread_id": thread_id,
            "run_id": run.id,
            "status": run.status
        }
        if hasattr(run, 'usage') and run.usage:
            token_usage.update({
                "prompt_tokens": run.usage.prompt_tokens,
                "completion_tokens": run.usage.completion_tokens,
                "total_tokens": run.usage.total_tokens
            })
        else:
            # Token usage might not be available immediately
            print(f"Warning: Token usage not available for run {run.id}")
            token_usage.update({
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "note": "Token usage not available"
            })
        
        # Read existing data or create empty list
        try:
            with open("Token.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        
        # Append new token usage and write back
        data.append(token_usage)
        with open("Token.json", "w") as file:
            json.dump(data, file, indent=2)
    def wait_for_run_completion(self,thread_id: str, run_id: str, timeout: int = 60) -> str:
        """Wait for OpenAI assistant run to complete with better error handling"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                run = self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
                if run.status in ["completed", "failed", "expired", "cancelled"]:
                    logger.info(f"Run {run_id} completed with status: {run.status}")
                    # Track token usage in the JSON file
                    # log_agent_token_utlisation(thread_id,run)
                    return run.status
                elif run.status == "requires_action":
                    logger.warning(f"Run {run_id} requires action - this shouldn't happen with current setup")
                    return "failed"
            except Exception as e:
                logger.error(f"Error checking run status: {e}")
                return "error"
        
        logger.warning(f"Run {run_id} timed out after {timeout}s")
        return "timeout"

# DEBUG: Add timing wrapper function
def time_function(func):
    """Decorator to time function execution"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

