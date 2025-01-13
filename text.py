import json
import os

import boto3
from dotenv import load_dotenv

load_dotenv()




def generate_message(bedrock_runtime, model_id, system_prompt, messages, max_tokens):
    
    body=json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens" : max_tokens,
            "system": system_prompt,
            "messages": messages
        }
    )

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id
    )
    response_body = json.loads(response.get('body').read())

    return response_body

def main():
    
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    model_id = os.getenv("AWS_BEDROCK_MODEL_ID")
    system_prompt = "これはテストです。適当な答えを日本語で返してください"
    max_tokens = 200000

    user_message = {"role":"user", "content": "こんにちは~"}
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
    
    assistant_message = {"role":"assistant", "content": "<emoji>"}
    messages = [user_message, assistant_message]
    response = generate_message(bedrock_runtime, model_id, system_prompt, messages, max_tokens)
    print('User turn and p@refilled assistant response.')
    print(json.dumps(response, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()