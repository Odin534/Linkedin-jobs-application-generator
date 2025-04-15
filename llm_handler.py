from openai import OpenAI
import requests
import json
from groq import Groq


class llm_agent:
    def __init__(self):
        # self.api_key = self.load_config()
        # self.model = self.openAI_model(self.api_key)
        self.client = Groq(
            # base_url="https://openrouter.ai/api/v1",
            api_key=self.get_api_key()
        )


    def get_api_key(self):
        with open("config.json", "r") as f:
            config = json.load(f)
        return config["groq_key"]
    
    # def openAI_model(self,api_key):
    #     model = OpenAI(api_key=api_key)
    #     return model
    
    def refine_job_description(self, job_description_text):
        prompt = f""""
        Extract the key tasks and requirements from the following job description:
        
        Job Description:
        {job_description_text}
        
        Provide the output in the following JSON format:
        {{
            "key_tasks": ["Task 1", "Task 2", "Task 3"],
            "requirements": ["Requirement 1", "Requirement 2", "Requirement 3"]
        }}
        """
        print(prompt)
        try:
            # response = requests.post(
            #     url = "https://openrouter.ai/api/v1/chat/completions",
            #     headers= {
            #         "Authorization": f"Bearer {self.get_api_key()}",
            #         "Content-type": "application/json"
            #     },
            #     data = json.dumps({
            #         "model" : "meta-llama/llama-4-maverick:free",
            #         "messages" : [
            #         {
            #             "role":"user",
            #             "content": [
            #                 {
            #                     "type":"text",
            #                     "text": prompt
            #                 }
            #             ]
            #         }
            #     ]
            #     })
            # )





            response = self.client.chat.completions.create(
                model = "llama3-70b-8192",
                messages= [
                    {
                        "role":"user",
                        "content": prompt
                    }
                ],
                temperature=1,
                max_tokens=8192
            )
            refined_description = response.choices[0].message.content
            return eval(refined_description)
        except Exception as e:
            print(f"Error in LLM processing: {e}")
            return {"key_tasks": None, "requirements": None}
