from flask import Flask, Response
from models.market_type import MarketType
import json

app = Flask(__name__)


@app.route('/api/v1.0/items')
def hello_world():
    types = [{'id': type.external_id, 'name': type.name} for type in
             MarketType.scan(page_size=1000)]

    json_string = json.dumps({'items': types})
    return Response(json_string, mimetype='application/json')


if __name__ == '__main__':
    app.run()
