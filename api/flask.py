from flask import Flask, request, jsonify
from openai import OpenAI
import requests
import os
import logging
import time

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID ='asst_1E1eHUlfA7Cq6Gk5HSafBw2K'

client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/api/getClubSuggestion', methods=['POST'])
def get_club_suggestion():
    try:
        user_input = request.json.get('userInput')
        if not user_input:
            app.logger.error('No user input provided')
            return jsonify({'error': 'No userInput provided'}), 400

        app.logger.debug(f"Received user input: {user_input}")

        thread = client.beta.threads.create(
            messages=[{"role": "user", "content": f"Suggest a club for anyone interested in {user_input}."}]
        )

        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
        app.logger.debug(f"Run created: {run.id}")

        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            app.logger.debug(f"Run status: {run.status}")
            time.sleep(1)

        message_response = client.beta.threads.messages.list(thread_id=thread.id)
        messages = message_response.data
        if not messages:
            app.logger.error("No response from the assistant.")
            return jsonify({'error': 'No response from the assistant'}), 500

        latest_message = messages[0]
        assistant_message = latest_message.content[0].text.value
        app.logger.info(f"Assistant response: {assistant_message}")

        return jsonify({'suggestion': assistant_message})

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
        app.run(debug=True)

vercel_app = app
