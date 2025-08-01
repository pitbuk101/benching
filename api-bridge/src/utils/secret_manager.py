from loguru import logger
import boto3
import json
import base64
import os

session = boto3.session.Session()
def get_secrets(secret_id, type = 'string'):
    if secret_id == None:
        raise Exception('secret_id is required', 400)
    # Create a Secrets Manager client 
    client = session.client(
        service_name='secretsmanager',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    secret = None
    get_secret_value_response = client.get_secret_value(SecretId=secret_id)
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    elif 'SecretBinary' in get_secret_value_response:
        secret = base64.b64decode(get_secret_value_response['SecretBinary']) 
    if type == 'json' and secret is not None:
        return json.loads(secret)
    logger.info(f"Success Get Secret {secret_id}, {type}")
    return secret


if __name__ == "__main__":
    secret_id = os.environ.get('SNOWFLAKE_SECRET_ID')
    secret = get_secrets(secret_id, type='json')
    print(secret)