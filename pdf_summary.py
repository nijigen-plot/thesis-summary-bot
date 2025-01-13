import json
import os

import boto3
from dotenv import load_dotenv

load_dotenv()

class Summary:
    def __init__(self):
        
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        
        self.model_id = os.getenv("AWS_BEDROCK_MODEL_ID")
        self.system = [{"text": "添付されたPDFファイルを要約し、内容を日本語で返してください。要約については、多くて最大10000文字程度で纏めてください。"}]

    def generate_message(self, pdf_data):
        
        inferenceConfig ={
            "temperature": 0.5,
            "topP": 0.9
        }
        user_message = [{
                "role":"user", 
                "content": [
                    {
                        "document" : {
                            "name": "PDF Document",
                            "format": "pdf",
                            "source": {"bytes": pdf_data},
                        }
                    },
                    {"text": "PDF Documentの内容を要約して"}
                ]
            }]
        response = self.bedrock_runtime.converse(
            modelId=self.model_id,
            messages=user_message,
            inferenceConfig=inferenceConfig,
            system=self.system
        )
        # response_body = response["output"]["message"]["content"][0]["text"]
        return response