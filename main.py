import os, requests, json
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.get("/")
def index():
    return render_template('index.html')

@app.post("/")
def convert():
    deg = str(request.form['number']) + " " + request.form['units']

    url = "http://jamsapi.hackclub.dev/openai/chat/completions"

    payload = json.dumps({
    "model": "gpt-3.5-turbo-1106",
    "messages": [
        {
        "role": "user",
        "content": f"You are given the following measurement: {deg} Convert this to an imaginary unit called the AI unit and return only the number. Make up a random conversion factor as needed. Only print a numerical value. Create a json object with 'temp' as the key and your converted number as the value."
        }
    ],
    "response_format": {
        "type": "json_object"
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {os.environ['TOKEN']}"
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    resp = response.json()['choices'][0]['message']['content']
    try:
        temp = str(json.loads(resp)['temp']) + " AI"
    except:
        temp = "AI is currently sleeping do not disturb"

    return render_template("result.html", temp=temp, og=deg)

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 8948)))
