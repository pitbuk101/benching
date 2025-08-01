import os

tenant_ids_region = {'519f6dbf-da97-47ba-9f4f-298e832e34bb':'US',
             '6566983b-2977-4deb-9bb4-2d3ba7b7ac8c':'EU',
             '048ee4ca-43b3-48e5-b95a-bd442ba15c91':'EU'}

conn_params: dict = {
        "US":{
            "user": os.environ.get('US_SF_USERNAME'),
            "password": os.environ.get('US_SF_PASSWORD'),
            "account": os.environ.get('US_SF_ACCOUNT'),
            "database": os.environ.get('US_SF_DATABASE'),
            "warehouse": os.environ.get('US_SF_WAREHOUSE'),
            "role": os.environ.get('US_SF_ROLE')
            },
        "EU":{
            "user": os.environ.get('EU_SF_USERNAME'),
            "password": os.environ.get('EU_SF_PASSWORD'),
            "account": os.environ.get('EU_SF_ACCOUNT'),
            "database": os.environ.get('EU_SF_DATABASE'),
            "warehouse": os.environ.get('EU_SF_WAREHOUSE'),
            "role": os.environ.get('EU_SF_ROLE')
            }
    }