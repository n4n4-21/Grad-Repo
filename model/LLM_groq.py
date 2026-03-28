import os
from groq import Groq
from dotenv import load_dotenv
#llama-3.1-8b-instant

load_dotenv()

class GroqModel:
    def __init__(self, model: str = "llama-3.3-70b-versatile", rules_file: str = "rules.txt"):
        self.model = model
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.conversation_history = []
        self._load_system_prompt(rules_file)  # Auto-loads on startup

    def _load_system_prompt(self, rules_file: str):
        """Reads rules.txt and sets it as the system prompt."""
        try:
            with open(rules_file, "r", encoding="utf-8") as f:
                rules_content = f.read()

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

        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find '{rules_file}'. Make sure it's in the project root.")

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
        """Clears chat history but keeps the system prompt."""
        self.conversation_history = self.conversation_history[:1]
