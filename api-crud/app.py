from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)

data_store = {}

# Swagger UI configuration
SWAGGER_URL = '/apidocs'
API_URL = '/static/swagger.yml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/items', methods=['POST'])
def create_item():
    item_id = request.json.get('id')
    item_data = request.json.get('data')
    if item_id in data_store:
        return jsonify({'error': 'Item already exists'}), 400
    data_store[item_id] = item_data
    return jsonify({'message': 'Item created'}), 201


@app.route('/items/<item_id>', methods=['GET'])
def read_item(item_id):
    item_data = data_store.get(item_id)
    if item_data is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify({'id': item_id, 'data': item_data}), 200


@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    if item_id not in data_store:
        return jsonify({'error': 'Item not found'}), 404
    item_data = request.json.get('data')
    data_store[item_id] = item_data
    return jsonify({'message': 'Item updated'}), 200


@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id not in data_store:
        return jsonify({'error': 'Item not found'}), 404
    del data_store[item_id]
    return jsonify({'message': 'Item deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)
