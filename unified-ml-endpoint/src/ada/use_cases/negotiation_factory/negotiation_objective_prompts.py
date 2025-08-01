import pandas as pd
from typing import Dict, List

from ada.use_cases.negotiation_factory.prompts import create_objectives_prompt_v2, classify_prompt , generate_objective_summary_prompt, generate_price_reduction_prompt, generate_payment_terms_prompt
from ada.components.llm_models.generic_calls import (
    generate_chat_response_with_chain,
    run_conversation_chat,
)
from ada.utils.logs.logger import get_logger
from ada.utils.logs.time_logger import log_time
from datetime import datetime
from ada.utils.config.config_loader import read_config


log = get_logger("Negotiation objective prompts")
negotiation_conf = read_config("use-cases.yml")["negotiation_factory"]
model_conf = read_config("models.yml")

@log_time
def generate_payment_terms_objective(analytics_data, supplier_name, category, sku_names, supplier_profile):
    print("Generating payment terms objective")
    log.info("Generating payment terms objective")
    analytic_name = "payment terms standardization"
    df = analytics_data.get("Payment Terms Standardization")

    df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce")
    df["QUARTER"] = pd.to_numeric(df["QUARTER"], errors="coerce")
    df = df[df['YEAR'] == df['YEAR'].max()]
    if df is None or df.empty:
        log.warning("No data available for Payment Terms Standardization.")
        return []

    

    required_cols = {"POTENTIAL_SAVINGS", "DESIRED_PAYMENT_TERM_DAYS", "SPEND"}
    if not required_cols.issubset(df.columns):
        log.warning("Missing required columns for Payment Terms.")
        return []

    df = df.rename(columns={
        "SPEND": "Total Spend",
        "DESIRED_PAYMENT_TERM_DAYS": "Avg Payment Term Days",
        "POTENTIAL_SAVINGS": "Potential Cost Savings"
    })

    df["Avg Payment Term Days"] = pd.to_numeric(df["Avg Payment Term Days"], errors="coerce")
    df["Potential Cost Savings"] = pd.to_numeric(df["Potential Cost Savings"], errors="coerce")

    df = df[df["Potential Cost Savings"] > 1000].copy()
    if df.empty:
        return []

    df.sort_values(by=["YEAR", "Potential Cost Savings"], ascending=[False, False], inplace=True)

    summary_text = build_payment_terms_prompt(df, supplier_profile, {
        "supplier": supplier_name,
        "category": category
    }, sku_names)

    prompt = generate_payment_terms_prompt({
        "objective": "Payment Terms",
        "supplier": supplier_name,
        "category": category,
        "supplier_profile": supplier_profile,
        "data": {analytic_name: df.to_dict(orient="records")},
        "summary": summary_text
    }, supplier_profile)

    summary = generate_chat_response_with_chain(prompt=prompt, model='gpt-4o', temperature=0.7).replace('*', '')

    return [{
        "id": 0,
        "objective": summary,
        "objective_type": "Payment Terms",
        "objective_reinforcements": [],
        "list_of_skus": sku_names,
        "analytics_names": [analytic_name]
    }]

@log_time
def build_payment_terms_prompt(df: pd.DataFrame, supplier_profile: Dict, context_dict: Dict, sku_names) -> str:
    log.info("Building payment terms prompt.")
    log.info(f"Data being passed in payment terms: {df}")

    supplier = context_dict.get("supplier", "")
    category = context_dict.get("category", "")

    supplier_avg_raw = supplier_profile.get("payment_term_avg", 0)
    supplier_avg = int(round(float(supplier_avg_raw or 0)))

    df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce")
    df["QUARTER"] = pd.to_numeric(df["QUARTER"], errors="coerce")
    df["Avg Payment Term Days"] = pd.to_numeric(df["Avg Payment Term Days"], errors="coerce")
    df["Potential Cost Savings"] = pd.to_numeric(df["Potential Cost Savings"], errors="coerce")

    df = df[df["Potential Cost Savings"] > 1000]
    df.sort_values(by=["YEAR", "Potential Cost Savings"], ascending=[False, False], inplace=True)

    # Calculate total potential savings
    total_savings = df["Potential Cost Savings"].sum()

    # Handle multiple SKUs in the summary
    if sku_names:
        sku_count = len(sku_names)
        if sku_count == 1:
            summary = f"The current average payment term for the selected SKU based on the {df['YEAR'].max()} YTD data is "
        elif sku_count == 2:
            summary = f"The current average payment terms for the selected SKUs based on the {df['YEAR'].max()} YTD data are "
        else:
            avg_payment_days = df.groupby('MATERIAL')['Avg Payment Term Days'].mean()
            min_avg = int(round(avg_payment_days.min()))
            max_avg = int(round(avg_payment_days.max()))
            summary = f"The current average payment terms for the selected SKUs range from {min_avg} to {max_avg} days based on the {df['YEAR'].max()} YTD data."
    else:
        avg_payment_days = df.groupby('MATERIAL')['Avg Payment Term Days'].mean()
        min_avg = int(round(avg_payment_days.min()))
        max_avg = int(round(avg_payment_days.max()))
        summary = f"The current average payment terms for the selected SKUs range from {min_avg} to {max_avg} days based on the {df['YEAR'].max()} YTD data."

    # Add SKU-specific terms if small count
    if sku_names and len(sku_names) < 3 or len(df["MATERIAL"].unique()) < 3:
        sku_terms = []
        for sku in df["MATERIAL"].unique():
            sku_df = df[df["MATERIAL"] == sku]
            latest_year = sku_df["YEAR"].max()
            year_df = sku_df[sku_df["YEAR"] == latest_year]
            avg_days = int(round(year_df["Avg Payment Term Days"].mean()))
            sku_terms.append(f"{avg_days} days for {sku} (YTD)")
        summary += " and ".join(sku_terms) + ". "

    # Add savings & optimization message
    summary += (
        f"The estimated total working capital benefit from aligning terms is approximately €{int(round(total_savings)):,}.\n"
        "There is a significant opportunity to optimize cash flow and unlock working capital "
        "by aligning payment terms to a common industry benchmark of 90 days.\n"
    )

    # DETAILS Section
    details = []
    for sku in df["MATERIAL"].unique():
        details.append("")
        details.append(f"{sku}")
        sku_df = df[df["MATERIAL"] == sku]

        for year in sorted(sku_df["YEAR"].unique(), reverse=True):
            year_data = sku_df[sku_df["YEAR"] == year]
            total_benefit = int(round(year_data["Potential Cost Savings"].sum()))
            avg_year_term = int(round(year_data["Avg Payment Term Days"].mean()))

            details.append(
                f"- For year {int(year)} YTD, the average payment term is {avg_year_term} days, "
                f"resulting in an unrealized working capital benefit of approximately €{total_benefit:,}."
            )

    # ACTIONS Section (Consolidated)
    action_lines = [
        f"To capitalize on working capital benefits, extend the payment term for {supplier} to 90 days. "
        f"This adjustment could have yielded estimated benefits of €{int(round(total_savings)):,} in 2025 YTD."
    ]

    full_prompt = (
        f"Summary:\n{summary}\n"
        f"Details:\n\n" + "\n".join(details) + "\nActions:\n" + "\n".join(action_lines)
    )

    return full_prompt


@log_time
def generate_price_reduction_objective(analytics_data, supplier_name, category, sku_names, supplier_profile):
    """
    Generates the Price Reduction objective using pre-loaded analytics data.
    """
    
    analytic_name_map = {
        "early payments": "Early Payments",
        "unused discount": "Unused Discount",
        "Total Saving Achieved": "Parametric Cost Modeling",
        "price arbitrage query": "Price Arbitrage"
    }

    context_dict = {
        "objective": "Price Reduction",
        "supplier": supplier_name,
        "category": category,
        "supplier_profile": supplier_profile,
        "data": {}
    }

    analytics_names = []
    total_savings = 0

    # breakpoint()
    for display_name, data_key in analytic_name_map.items():
        df = analytics_data.get(data_key)
        # breakpoint()
        if df is not None and not df.empty:
            context_dict["data"][display_name] = df.to_dict(orient="records")
            analytics_names.append(display_name)

            # Attempt to add up potential savings if the column is present
            for col in ["EARLY_PAYMENT_OPPORTUNITY", "DISCOUNT_NOT_USED", "CLEANSHEET_OPPORTUNITY", "PRICE_ARBITRAGE"]:
                if col in df.columns:
                    total_savings += df[col].fillna(0).sum()
                
            if total_savings < 1000:
                log.warning(f"Total savings for {col} is less than 1000. Current value: {total_savings}")
                return []
            
    if not context_dict["data"]:
        log.warning("No analytics found for Price Reduction objective.")
        return []

    # Optionally include total savings in the context for summary generation
    context_dict["total_savings"] = total_savings

    prompt = generate_price_reduction_prompt(context_dict)
    summary = generate_chat_response_with_chain(prompt=prompt, temperature=0.7).replace('*', '')

    return [{
        "id": 1,
        "objective": summary,
        "objective_type": "Price Reduction",
        "objective_reinforcements": [],
        "list_of_skus": sku_names,
        "analytics_names": analytics_names
    }]
