from flask import Flask
from api_gateway.gateway_service import gateway_service
app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def request(path):
    gateway_service.new_request(path)

if __name__ == '__main__':
    app.run()
