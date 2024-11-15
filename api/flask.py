from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/api/getClubSuggestion', methods=['POST'])
def get_club_suggestion():
    try:
        user_input = request.json.get('userInput')
        if not user_input:
            return jsonify({'error': 'No userInput provided'}), 400
        
        # Sending the request to OpenAI API
        response = requests.post(
            'https://api.openai.com/v1/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {OPENAI_API_KEY}'
            },
            json={
                'model': 'text-davinci-003',
                'prompt': f"Suggest a club for anyone interested in {user_input}.",
                'max_tokens': 100
            }
        )

        if response.status_code != 200:
            return jsonify({'error': 'OpenAI API request failed', 'details': response.text}), response.status_code

        data = response.json()
        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

vercel_app = app
