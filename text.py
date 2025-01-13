import json
import os

import boto3
from dotenv import load_dotenv

load_dotenv()




def generate_message(bedrock_runtime, model_id, system_prompt, messages, max_tokens):
    
    inferenceConfig ={
        "temperature": 0.5,
        "topP": 0.9,
        "maxTokens": max_tokens,
    }

    response = bedrock_runtime.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig=inferenceConfig
    )
    # response_body = response["output"]["message"]["content"][0]["text"]
    return response

def main():
    
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    model_id = os.getenv("AWS_BEDROCK_MODEL_ID")
    system_prompt = "これはテストです。適当な答えを日本語で返してください"
    max_tokens = 200

    user_message = {"role":"user", "content": [{"text": "こんにちは～"}]}
    messages = [user_message]
    
    response = generate_message(
        bedrock_runtime,
        model_id,
        system_prompt,
        messages,
        max_tokens
    )

    print('User turn only.')
    print(json.dumps(response, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()