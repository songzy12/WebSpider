import json
from flask import Flask, request

from utils import search_exactqa

app = Flask(__name__)


@app.route("/search_exactqa")
def hello():
    wd = request.args.get('wd', '')
    return json.dumps(search_exactqa(wd), ensure_ascii=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
