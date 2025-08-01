from langchain_openai import ChatOpenAI, OpenAIEmbeddings, AzureChatOpenAI, AzureOpenAIEmbeddings
from src.env import OPENAI_API_KEY, OPENAI_BASE_URL
from openai import OpenAI
model = ChatOpenAI(
    openai_api_base=OPENAI_BASE_URL,
    openai_api_key=OPENAI_API_KEY,
    model_name="gpt-4o",
    temperature=0,
    n=1,
    seed=42,
    verbose=True
)


model_mini = ChatOpenAI(
    openai_api_base=OPENAI_BASE_URL,
    openai_api_key=OPENAI_API_KEY,
    model_name="gpt-4.1-mini",
    temperature=0,
    seed=42,
    verbose=True
)

recomendation_model = ChatOpenAI(
    openai_api_base=OPENAI_BASE_URL,
    openai_api_key=OPENAI_API_KEY,
    model_name="gpt-4o",
    temperature=1,
    n=1,
)

openai_client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

# def model_with_internet_search(system_prompt: str, user_prompt: str,  model="gpt-4o", functions=[]):
#     client = OpenAI(api_key=LLM_OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
#     # Create a chat completion
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "system",
#                 "content": system_prompt
#             },
#             {
#                 "role": "user",
#                 "content": user_prompt
#             }
#         ],
#             seed=42,
#             temperature=0,
#             functions=functions,
#             function_call="auto",
#             model=model,
#     )
#     return chat_completion

openai_embeddings_model = OpenAIEmbeddings(
    openai_api_base=OPENAI_BASE_URL,
    openai_api_key=OPENAI_API_KEY,
    model="text-embedding-3-large",
    # verbose=True
)

# # Azure OpenAI LangChain chat model
# azure_model = AzureChatOpenAI(
#     openai_api_base=OPENAI_BASE_URL,
#     openai_api_key=LLM_OPENAI_API_KEY,
#     deployment_name="gpt-4o",  # or your Azure deployment name
#     temperature=0,
#     n=1,
#     seed=42,
#     verbose=True
# )

# # Azure OpenAI LangChain recommendation model
# azure_recommendation_model = AzureChatOpenAI(
#     openai_api_base=OPENAI_BASE_URL,
#     openai_api_key=LLM_OPENAI_API_KEY,
#     deployment_name="gpt-4o",  # or your Azure deployment name
#     temperature=1,
#     n=1,
# )

# # Azure OpenAI LangChain embeddings model
# azure_openai_embeddings_model = AzureOpenAIEmbeddings(
#     openai_api_base=OPENAI_BASE_URL,
#     openai_api_key=LLM_OPENAI_API_KEY,
#     deployment_name="text-embedding-3-large",  # or your Azure embedding deployment name
# )