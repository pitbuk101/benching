import os
from pydantic import BaseModel
# from dotenv import load_dotenv
# load_dotenv(".env", verbose=True, override=True)
class Settings(BaseModel):
    EXTERNAL_API_URL: str = f"{os.environ.get('EXTERNAL_API_URL')}/v1"
    headers: dict = {
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    # "Origin": os.environ.get('EXTERNAL_API_URL'),
    # "Referer": f"{os.environ.get('EXTERNAL_API_URL')}/home",
    "accept": "*/*",
    "content-type": "application/json",
    # This is empty as we are setting this up dynamically
    "authorization": ""
    }
    conn_params: dict = {
        # uhg
        "519f6dbf-da97-47ba-9f4f-298e832e34bb":{
            "user": os.environ.get('SF_USERNAME_519f6dbf', None),
            "password": os.environ.get('SF_PASSWORD_519f6dbf', None),
            "account": os.environ.get('SF_ACCOUNT_519f6dbf', None),
            "database": os.environ.get('SF_DATABASE_519f6dbf', None),
            "warehouse": os.environ.get('SF_WAREHOUSE_519f6dbf', None),
            "role": os.environ.get('SF_ROLE_519f6dbf', None),
            "region": "us",
            "temp_tenant_id": os.environ.get('SF_DATABASE_519f6dbf', None)
            },
        # ega
        "6566983b-2977-4deb-9bb4-2d3ba7b7ac8c":{
            "user": os.environ.get('SF_USERNAME_6566983b', None),
            "password": os.environ.get('SF_PASSWORD_6566983b', None),
            "account": os.environ.get('SF_ACCOUNT_6566983b', None),
            "database": os.environ.get('SF_DATABASE_6566983b', None),
            "warehouse": os.environ.get('SF_WAREHOUSE_6566983b', None),
            "role": os.environ.get('SF_ROLE_6566983b', None),
            "region": "eu",
            "temp_tenant_id": os.environ.get('SF_DATABASE_6566983b', None)

            },
        # zxd
        "048ee4ca-43b3-48e5-b95a-bd442ba15c91":{
            "user": os.environ.get('SF_USERNAME_048ee4ca', None),
            "password": os.environ.get('SF_PASSWORD_048ee4ca', None),
            "account": os.environ.get('SF_ACCOUNT_048ee4ca', None),
            "database": os.environ.get('SF_DATABASE_048ee4ca', None),
            "warehouse": os.environ.get('SF_WAREHOUSE_048ee4ca', None),
            "role": os.environ.get('SF_ROLE_048ee4ca', None),
            "region": "eu",
            "temp_tenant_id": os.environ.get('SF_DATABASE_048ee4ca', None)
            },
        # demo-prod
        "fce26b80-b826-4c35-a519-765872745aa0":{
            "user": os.environ.get('EU_SF_USERNAME', None),
            "password": os.environ.get('EU_SF_PASSWORD', None),
            "account": os.environ.get('EU_SF_ACCOUNT', None),
            "database": os.environ.get('EU_SF_DATABASE', None),
            "warehouse": os.environ.get('EU_SF_WAREHOUSE', None),
            "role": os.environ.get('EU_SF_ROLE', None),
            "region": "eu",
            "temp_tenant_id": "fce26b80-b826-4c35-a519-765872745aa0",
            },
        # demo-dev
        "920a2f73-c7db-405f-98ea-f768c6da864f":{
            "user": os.environ.get('EU_SF_USERNAME', None),
            "password": os.environ.get('EU_SF_PASSWORD', None),
            "account": os.environ.get('EU_SF_ACCOUNT', None),
            "database": os.environ.get('EU_SF_DATABASE', None),
            "warehouse": os.environ.get('EU_SF_WAREHOUSE', None),
            "role": os.environ.get('EU_SF_ROLE', None),
            "region": "eu",
            "temp_tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f"
            },
        #demo-stg
        "dc6b5f00-0718-4089-bb70-7d3d14df7cbf":{
            "user": os.environ.get('EU_SF_USERNAME', None),
            "password": os.environ.get('EU_SF_PASSWORD', None),
            "account": os.environ.get('EU_SF_ACCOUNT', None),
            "database": os.environ.get('EU_SF_DATABASE', None),
            "warehouse": os.environ.get('EU_SF_WAREHOUSE', None),
            "role": os.environ.get('EU_SF_ROLE', None),
            "region": "eu",
            "temp_tenant_id": "dc6b5f00-0718-4089-bb70-7d3d14df7cbf"
            }
    }

config = Settings()
