from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/test')
def test():
    return "CORS OK"

if __name__ == "__main__":
    app.run(debug=True, port=5001)
