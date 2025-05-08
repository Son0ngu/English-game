from flask import Flask
from flask_cors import CORS
from api_gateway.gateway_service import gateway_service

app = Flask(__name__)
CORS(app)

@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def request(path):
    return gateway_service.new_request(path)


if __name__ == '__main__':
    app.run()
