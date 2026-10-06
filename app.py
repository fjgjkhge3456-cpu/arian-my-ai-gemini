import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app) # اجازه دسترسی از ظاهر برنامه

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = "پاسخ را به زبان فارسی روان و صمیمی همراه با ایموجی بنویس."

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "پیامی وارد نشده است"}), 400

        model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=SYSTEM_INSTRUCTION)
        res = model.generate_content(user_message)
        
        if res and hasattr(res, 'text'):
            return jsonify({"response": res.text}), 200
        else:
            return jsonify({"error": "پاسخی از جمنای دریافت نشد"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
