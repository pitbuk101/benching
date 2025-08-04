import os
import json
import time
import logging
from openai import OpenAI, APIError, APITimeoutError, APIConnectionError, RateLimitError
from typing import List, Dict, Union, Tuple, Callable, Any 
from io import StringIO
import csv
import pandas as pd
import importlib
import normalise.env as env


class LLMClient:
    """
    A client for interacting with an LLM service (e.g., OpenAI).
    Handles API calls, prompt formatting, response parsing, retries, and error handling.
    Prompts are now loaded from Python functions.
    """
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.model = env.LLM_MODEL
        self.temperature = env.LLM_TEMPERATURE
        self.api_key = env.LLM_OPENAI_API_KEY
        self.base_url = env.OPENAI_API_BASE
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        import normalise.src.prompts.normalization_prompts as normalization_prompts
        self.prompt_module = normalization_prompts
        self.logger.info("LLMClient initialized.")

    def _get_prompt_function_output(self, prompt_key: str, prompt_args: Dict[str, Any]) -> Dict[str, str]:
        """
        Retrieves and executes a prompt-generating function based on the prompt_key.
        The function is expected to return a dict with "system_message" and "user_template".
        """
        if not hasattr(self.prompt_module, prompt_key):
            self.logger.error(f"Prompt function '{prompt_key}' not found in prompt module.")
            raise ValueError(f"Prompt function '{prompt_key}' not found in prompt module.")

        prompt_function = getattr(self.prompt_module, prompt_key)
        if not callable(prompt_function):
            self.logger.error(f"Prompt function '{prompt_key}' is not callable.")
            raise ValueError(f"Prompt function '{prompt_key}' is not callable.")

        try:
            prompt_components = prompt_function(**prompt_args)
            if not isinstance(prompt_components, dict) or "user_template" not in prompt_components:
                self.logger.error(f"Prompt function '{prompt_key}' did not return a valid dict with 'user_template'. Got: {type(prompt_components)}")
                raise ValueError(f"Prompt function '{prompt_key}' output is malformed.")
            return prompt_components
        except Exception as e:
            self.logger.error(f"Error executing prompt function '{prompt_key}' with args {prompt_args}: {e}", exc_info=True)
            raise


    def _format_prompt_from_components(self, prompt_components: Dict[str, str]) -> List[Dict[str, str]]:
        system_message_content = prompt_components.get("system_message", "You are a helpful assistant.")
        user_message_content = prompt_components["user_template"] 

        messages = [
            {"role": "system", "content": system_message_content},
            {"role": "user", "content": user_message_content}
        ]
        return messages

    def generate_text_completion(self, prompt_key: str, prompt_args: Dict, 
                                 model: str = None, temperature: float = None) -> str:
        if model is None: model = self.model
        if temperature is None: temperature = self.temperature
        
        self.logger.debug(f"Prompt arguments for LLM call (prompt_key: {prompt_key}): {prompt_args}")
        
        try:
            prompt_components = self._get_prompt_function_output(prompt_key, prompt_args)
            messages = self._format_prompt_from_components(prompt_components)
            self.logger.info(f"Messages for LLM (prompt_key: {prompt_key}): {messages}") # Log the messages being sent
        except Exception as e_format: 
            self.logger.error(f"Failed to get or format prompt for key '{prompt_key}': {e_format}", exc_info=True)
            raise 

        retries = env.LLM_MAX_RETRIES
        timeout = env.LLM_TIMEOUT_SECONDS
        last_error = None

        for attempt in range(retries):
            try:
                self.logger.info(f"LLM API Call (Attempt {attempt + 1}/{retries}): Model={model}, Temp={temperature}, PromptKey={prompt_key}")
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    timeout=timeout
                )
                completion_text = response.choices[0].message.content.strip()
                self.logger.info(f"LLM API Call successful. Response received for prompt key '{prompt_key}'.")
                return completion_text
            except APITimeoutError as e:
                self.logger.warning(f"LLM API call timed out (Attempt {attempt + 1}/{retries}): {e}")
                last_error = e
            except APIConnectionError as e:
                 self.logger.warning(f"LLM API connection error (Attempt {attempt + 1}/{retries}): {e}")
                 self.logger.warning(f"Connection Error Details: repr(e)='{repr(e)}', e.args='{e.args}'")
                 last_error = e
            except RateLimitError as e:
                self.logger.warning(f"LLM API rate limit exceeded (Attempt {attempt + 1}/{retries}): {e}. Sleeping before retry...")
                last_error = e
                time.sleep(10 * (attempt + 1)) 
            except APIError as e: 
                self.logger.error(f"LLM API error (Attempt {attempt + 1}/{retries}): {e}")
                last_error = e
            except Exception as e: 
                self.logger.error(f"Unexpected error during LLM call (Attempt {attempt + 1}/{retries}): {e}", exc_info=True)
                last_error = e
            
            if attempt < retries - 1:
                self.logger.info(f"Retrying LLM call in {5 * (attempt + 1)} seconds...")
                time.sleep(5 * (attempt + 1))
            else:
                self.logger.error(f"LLM API call failed after {retries} attempts for prompt key '{prompt_key}'.")
                if last_error:
                    # Re-raise the last encountered error to provide more context
                    raise last_error
                else:
                    # Fallback if no specific error was caught but retries exhausted
                    raise APIError(message=f"LLM call failed after {retries} attempts for {prompt_key} with no specific API error captured.", request=None) # request=None might be an issue if APIError expects it


    def parse_csv_from_llm_output(self, csv_text: str, expected_columns: List[str], 
                                  expected_rows: int = None) -> pd.DataFrame:
        self.logger.debug(f"Attempting to parse CSV from LLM output. Expected columns: {expected_columns}")
        self.logger.debug(f"Raw CSV text from LLM: \n{csv_text}")

        try:
            if csv_text.startswith("```csv"):
                csv_text = csv_text[len("```csv"):]
            if csv_text.startswith("```"): 
                csv_text = csv_text[len("```"):]
            if csv_text.endswith("```"):
                csv_text = csv_text[:-len("```")]
            csv_text = csv_text.strip()

            first_line_cols = []
            try:
                if csv_text and csv_text.splitlines():
                    first_line_reader = csv.reader(StringIO(csv_text.splitlines()[0]))
                    first_line_cols = next(first_line_reader)
                else: 
                    self.logger.warning("CSV text is empty or contains only newlines. Cannot parse header.")
            except StopIteration: 
                pass # No content on first line
            except Exception as e_first_line:
                self.logger.warning(f"Could not parse first line for header check: {e_first_line}")

            if first_line_cols and len(first_line_cols) == len(expected_columns) and \
               all(col_name.strip('"').strip().lower() == exp_col.strip().lower() for col_name, exp_col in zip(first_line_cols, expected_columns)): # Added strip('"')
                 self.logger.info("Detected a header row in LLM output that matches expected columns. Skipping it.")
                 csv_text_lines = csv_text.splitlines()
                 csv_text = "\n".join(csv_text_lines[1:]) if len(csv_text_lines) > 1 else ""


            sio = StringIO(csv_text)
            reader = csv.reader(sio)
            
            parsed_rows = []
            for i, row in enumerate(reader):
                if not row: # Skip empty rows that csv.reader might produce from blank lines
                    continue
                if len(row) == len(expected_columns):
                    parsed_rows.append(row)
                # Robustness: Handle trailing comma if it results in one extra empty field
                elif len(row) == len(expected_columns) + 1 and row[-1] == '':
                    self.logger.warning(
                        f"Row {i+1} has an extra empty column, likely due to a trailing comma. "
                        f"Taking first {len(expected_columns)} column(s). Row: {row}"
                    )
                    parsed_rows.append(row[:len(expected_columns)])
                else:
                    self.logger.warning(
                        f"Row {i+1} has incorrect column count. Expected {len(expected_columns)}, got {len(row)}. Row: {row}. Skipping."
                    )
            
            df = pd.DataFrame(parsed_rows, columns=expected_columns)

            if expected_rows is not None and len(df) != expected_rows:
                self.logger.warning(
                    f"LLM output row count after parsing. Expected {expected_rows}, got {len(df)}. "
                    "Further alignment might be needed in the calling function (e.g., Normalizer)."
                )
            
            self.logger.info(f"Successfully parsed CSV into DataFrame with {len(df)} rows and {len(df.columns)} columns.")
            return df

        except Exception as e:
            self.logger.error(f"Failed to parse CSV from LLM output: {e}", exc_info=True)
            self.logger.error(f"Problematic CSV text was: \n{csv_text[:500]}...") 
            return pd.DataFrame(columns=expected_columns)


    def parse_json_from_llm_output(self, json_text: str, expected_structure_type: type = list) -> Union[List, Dict, None]:
        self.logger.debug("Attempting to parse JSON from LLM output.")

        try:
            if json_text.startswith("```json"):
                json_text = json_text[len("```json"):]
            if json_text.startswith("```"): 
                json_text = json_text[len("```"):]
            if json_text.endswith("```"):
                json_text = json_text[:-len("```")]
            json_text = json_text.strip()
            
            first_brace = json_text.find('{')
            first_bracket = json_text.find('[')
            
            start_index = -1
            if first_brace != -1 and first_bracket != -1:
                start_index = min(first_brace, first_bracket)
            elif first_brace != -1:
                start_index = first_brace
            elif first_bracket != -1:
                start_index = first_bracket

            if start_index != -1:
                end_char = '}' if json_text[start_index] == '{' else ']'
                end_index = json_text.rfind(end_char)

                if end_index > start_index:
                    json_text_cleaned = json_text[start_index : end_index+1]
                    self.logger.debug(f"Extracted JSON substring: {json_text_cleaned[:200]}...")
                    parsed_json = json.loads(json_text_cleaned)
                else: 
                    self.logger.warning("Could not reliably find JSON end character. Attempting to parse as is.")
                    parsed_json = json.loads(json_text) 
            else: 
                 self.logger.warning("No JSON start character ('{' or '[') found. Attempting to parse as is.")
                 parsed_json = json.loads(json_text)


            if not isinstance(parsed_json, expected_structure_type):
                self.logger.warning(f"Parsed JSON is not of the expected type. Expected {expected_structure_type}, got {type(parsed_json)}.")
            
            self.logger.info(f"Successfully parsed JSON from LLM output.")
            return parsed_json

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON from LLM output: {e}")
            self.logger.error(f"Problematic JSON text was: \n{json_text[:500]}...") 
            return None 
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during JSON parsing: {e}", exc_info=True)
            self.logger.error(f"Problematic text: \n{json_text[:500]}...")
            return None