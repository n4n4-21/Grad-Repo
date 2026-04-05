import os
from dotenv import load_dotenv
from groq import Groq
from model.file_reader import load_rules

load_dotenv()

class GroqModel:
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.model = model
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.conversation_history = []
        rules_file = os.environ.get("RULES_FILE")
        self._load_system_prompt(rules_file)

    def _load_system_prompt(self, rules_file: str):
        rules_content = load_rules(rules_file)

        system_prompt = f"""You are a helpful student assistant for the university.
Your job is to answer students' questions ONLY based on the university rules and laws provided below.
If a question is not covered in the rules, say that you don't have information about it.
Always reply in the same language the user writes in. If they write in Arabic, reply in Arabic. If they write in English, reply in English.

--- UNIVERSITY RULES ---
{rules_content}
------------------------
"""
        self.conversation_history.append({
            "role": "system",
            "content": system_prompt
        })

    def chat(self, user_message: str) -> str:
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        response = self.client.chat.completions.create(
            messages=self.conversation_history,
            model=self.model,
        )

        assistant_message = response.choices[0].message.content

        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def clear_history(self):
        self.conversation_history = self.conversation_history[:1]