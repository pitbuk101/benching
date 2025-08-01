import os

#Not to be used moving Forward
tenant_ids_region = {'519f6dbf-da97-47ba-9f4f-298e832e34bb':'US',
             '6566983b-2977-4deb-9bb4-2d3ba7b7ac8c':'EU',
             '048ee4ca-43b3-48e5-b95a-bd442ba15c91':'EU',
             '920a2f73-c7db-405f-98ea-f768c6da864f':'EU',
             'fce26b80-b826-4c35-a519-765872745aa0':'EU',
             'dc6b5f00-0718-4089-bb70-7d3d14df7cbf':'EU'
             }

#connection to snowflake will be as per tenant id and connection params to be fetched from env variables as per the tenant id
conn_params: dict = {
        "519f6dbf-da97-47ba-9f4f-298e832e34bb":{
            "user": os.environ.get('SF_USERNAME_519f6dbf'),
            "password": os.environ.get('SF_PASSWORD_519f6dbf'),
            "account": os.environ.get('SF_ACCOUNT_519f6dbf'),
            "database": os.environ.get('SF_DATABASE_519f6dbf'),
            "warehouse": os.environ.get('SF_WAREHOUSE_519f6dbf'),
            "role": os.environ.get('SF_ROLE_519f6dbf')
            },
         "6566983b-2977-4deb-9bb4-2d3ba7b7ac8c":{
            "user": os.environ.get('SF_USERNAME_6566983b'),
            "password": os.environ.get('SF_PASSWORD_6566983b'),
            "account": os.environ.get('SF_ACCOUNT_6566983b'),
            "database": os.environ.get('SF_DATABASE_6566983b'),
            "warehouse": os.environ.get('SF_WAREHOUSE_6566983b'),
            "role": os.environ.get('SF_ROLE_6566983b')
            },
         "048ee4ca-43b3-48e5-b95a-bd442ba15c91":{
            "user": os.environ.get('SF_USERNAME_048ee4ca'),
            "password": os.environ.get('SF_PASSWORD_048ee4ca'),
            "account": os.environ.get('SF_ACCOUNT_048ee4ca'),
            "database": os.environ.get('SF_DATABASE_048ee4ca'),
            "warehouse": os.environ.get('SF_WAREHOUSE_048ee4ca'),
            "role": os.environ.get('SF_ROLE_048ee4ca')
            },
        "fce26b80-b826-4c35-a519-765872745aa0":{
            "user": os.environ.get('EU_SF_USERNAME'),
            "password": os.environ.get('EU_SF_PASSWORD'),
            "account": os.environ.get('EU_SF_ACCOUNT'),
            "database": 'fce26b80-b826-4c35-a519-765872745aa0',
            "warehouse": os.environ.get('EU_SF_WAREHOUSE'),
            "role": os.environ.get('EU_SF_ROLE')
         },
         "920a2f73-c7db-405f-98ea-f768c6da864f":{
            "user": os.environ.get('EU_SF_USERNAME'),
            "password": os.environ.get('EU_SF_PASSWORD'),
            "account": os.environ.get('EU_SF_ACCOUNT'),
            "database": '920a2f73-c7db-405f-98ea-f768c6da864f',
            "warehouse": os.environ.get('EU_SF_WAREHOUSE'),
            "role": os.environ.get('EU_SF_ROLE')
        },
         "dc6b5f00-0718-4089-bb70-7d3d14df7cbf":{
            "user": os.environ.get('EU_SF_USERNAME'),
            "password": os.environ.get('EU_SF_PASSWORD'),
            "account": os.environ.get('EU_SF_ACCOUNT'),
            "database": 'dc6b5f00-0718-4089-bb70-7d3d14df7cbf',
            "warehouse": os.environ.get('EU_SF_WAREHOUSE'),
            "role": os.environ.get('EU_SF_ROLE')
        }
    }


