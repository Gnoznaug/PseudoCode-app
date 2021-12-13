from flask import Flask
import os
import openai
import json
from flask_cors import CORS, cross_origin
from flask import request
import services
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()


def create_app():
    app = Flask(__name__)
    return app

openai.api_key = os.getenv("OPENAI_API_KEY")

app = create_app()
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/ans', methods=['POST'])
@cross_origin()
@limiter.limit("5/minute")
def sol():
    if request.method =='POST':
        url = request.json['url']
        if services.linkValidation(url):
            response = openai.Completion.create(
                engine="davinci-codex",
                prompt="Solve " + url,
                temperature = 0,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            code = openai.Completion.create(
                engine="davinci-codex",
                prompt="# Python 3\n" + response.choices[0].text + "\n" + "# Explanation of what the code does\n",
                temperature=0,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            return code.choices[0]
        else:
            x = {
                "text": "Please enter a valid LeetCode problem link."
            }
            return json.dumps(x)

        

if __name__ == '__main__':
   app.run()