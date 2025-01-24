import json
import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

class Summary:
    def __init__(self):
        
        if os.getenv("ANTHROPIC_API_KEY") is None:
            raise KeyError("ANTHROPIC_API_KEY is not set.")
        if os.getenv("ANTHROPIC_MODEL_NAME") is None:
            raise KeyError("ANTHROPIC_MODEL_NAME is not set.")
        self.client = anthropic.Anthropic() # デフォルトでANTHROPIC_API_KEY環境変数を読む
        self.model_name = os.getenv("ANTHROPIC_MODEL_NAME")
        self.system_text = "添付されたPDFファイルを要約し、内容を日本語で返してください。要約については、多くて最大10000文字程度で纏めてください。"
        
    def generate_message(self, pdf_data):
        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=4096,
            messages=[
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "document",
                            "source": {
                                "type": "base64",
                                "media_type": "application/pdf",
                                "data": pdf_data
                            },
                            "cache_control": {"type": "ephemeral"}
                        },
                        {
                            "type": "text",
                            "text": "PDF Documentの内容を要約して"
                        }
                    ]
                }
            ],
            system=self.system_text,
            temperature=0.5
        )
        if message.type == 'error':
            raise Exception(f"Error: {message['error']}")
        # Messageクラスをdictに変換
        result = {
            "id": message.id,
            "text": message.content[0].text,
            "model": message.model,
            "role": message.role,
            "stop_reason": message.stop_reason,
            "stop_sequence": message.stop_sequence,
            "type": message.type,
            "cache_creation_input_tokens": message.usage.cache_creation_input_tokens,
            "cache_read_input_tokens": message.usage.cache_read_input_tokens,
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens
        }
        return result