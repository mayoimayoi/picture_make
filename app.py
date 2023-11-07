from flask import Flask, render_template, request, session
from datetime import timedelta
from dotenv import load_dotenv
import openai
import requests
import os

# .envファイルから環境変数を読み込む
load_dotenv()
# API_KEY = os.getenv('DALL_E_API_KEY')
openai.api_key = os.getenv('DALLE_API_KEY')

app = Flask(__name__)
# client = OpenAI()
app.secret_key = 'your_secret_key'  # セッション管理用の秘密鍵
# セッションの有効期限を設定
app.permanent_session_lifetime = timedelta(days=1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'request_count' not in session:
            session['request_count'] = 0
        print(session['request_count'])
        if session['request_count'] < 15:
            session['request_count'] += 1
            session.permanent = True  # セッションの有効期限をリセット
            prompt = request.form['prompt']
            # headers = {'Authorization': f'Bearer {API_KEY}'}
            # DALL-E APIのリクエストURL
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            # if response.status_code == 200:
                # image_url = response.json()['image_url']
            image_url = response.data[0].url
            return render_template('index.html', image_url=image_url)
            # else:
            #     error_message = 'APIリクエストに失敗しました。'
            #     return render_template('index.html', error_message=error_message)
        else:
            error_message = '本日のリクエスト上限に達しました。'
            return render_template('index.html', error_message=error_message)

    # GETリクエストまたはリクエスト数が上限に達した場合の処理
    return render_template('index.html')

if __name__ == '__main__':
    print(openai.api_key)
    app.run(debug=True, port=8080)