import json
import os

import boto3
from dotenv import load_dotenv

load_dotenv()

def generate_message(bedrock_runtime, model_id, system, messages):
    
    inferenceConfig ={
        "temperature": 0.5,
        "topP": 0.9
    }

    response = bedrock_runtime.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig=inferenceConfig,
        system=system
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
    system_prompt = {"text": "添付されたPDFファイルを要約し、内容を日本語で返してください。要約については、多くて最大10000文字程度で纏めてください。"}
    system = [system_prompt]

    with open("./2501.06121v1.pdf", "rb") as f:
        pdf = f.read()

    user_message = {
        "role":"user", 
        "content": [
            {
                "document" : {
                    "name": "PDF Document",
                    "format": "pdf",
                    "source": {"bytes": pdf},
                }
            },
            {"text": "PDF Documentの内容を要約して"}
        ]
    }
    messages = [user_message]
    
    response = generate_message(
        bedrock_runtime,
        model_id,
        system,
        messages
    )

    print('User turn only.')
    print(json.dumps(response, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()