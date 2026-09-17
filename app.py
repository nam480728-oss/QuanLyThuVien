from flask import Flask, render_template

app = Flask(__name__)

# Route trang chủ
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Bật debug=True để server tự khởi động lại khi bạn sửa code
    app.run(debug=True, port=5000)
