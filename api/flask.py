from flask import Flask, request, jsonify
import requests
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/api/getClubSuggestion', methods=['POST'])
def get_club_suggestion():
    try:
        user_input = request.json.get('userInput')
        if not user_input:
            app.logger.error('No user input provided')
            return jsonify({'error': 'No userInput provided'}), 400

        app.logger.debug(f"Received user input: {user_input}")

        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {OPENAI_API_KEY}'
            },
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'user', 'content': f"Suggest a club for anyone interested in {user_input}."}
                ],
                'max_tokens': 200
            }
        )

        app.logger.info(f"OpenAI API Response: {response.status_code} {response.text}")
        if response.status_code != 200:
            app.logger.error(f"OpenAI API request failed: {response.text}")
            return jsonify({'error': 'OpenAI API request failed', 'details': response.text}), response.status_code

        data = response.json()
        assistant_message = data.get("choices", [{}])[0].get("message", {}).get("content", "No suggestion found.")
        return jsonify({'suggestion': assistant_message})

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

vercel_app = app
