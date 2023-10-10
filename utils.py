import base64

import boto3
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def gen_key():
    key = get_random_bytes(32)
    encoded_key = base64.b64encode(key).decode()

    print(encoded_key)


def encrypt(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return base64.b64encode(cipher.nonce + ciphertext)


def decrypt(data: bytes, key: bytes) -> bytes:
    raw = base64.b64decode(data)
    nonce, ciphertext = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext)


def get_encryption_key():
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(
        SecretId="arn:aws:secretsmanager:ap-southeast-1:457349367880:secret:AES_ENC_KEY-rGKnkB"
    )
    secret = response["SecretString"]
    return base64.b64decode(secret)


def get_secretsmanager_by_arn(arn):
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=arn)
    secret = response["SecretString"]
    return secret


def get_database_config(secret_name, region_name="ap-southeast-1"):
    """
    Retrieve the database configuration from AWS Secrets Manager.
    """
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise e

    if "SecretString" in get_secret_value_response:
        secrets = get_secret_value_response["SecretString"]
        return json.loads(secrets)

    return None
