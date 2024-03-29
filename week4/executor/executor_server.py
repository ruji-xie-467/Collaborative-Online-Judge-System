import json
import sys
from flask import Flask
from flask import request
from flask import jsonify
import executor_utils as eu

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World! Heheasdfasdf"


@app.route("/build_and_run", methods=["POST"])
def build_and_run():
    print(json.loads(request.data))
    data = request.get_json()
    if 'code' not in data or 'lang' not in data:
        return "You should provide both 'code' and 'lang'"
    code = data["code"]
    lang = data["lang"]

    print "API got called with code: %s in %s" % (code, lang)

    result = eu.build_and_run(code, lang)
    return jsonify(result)


if __name__ == "__main__":
    eu.load_image()
    port = int(sys.argv[1])
    print "Executor running on: %d" % port
    app.run(port=port, debug=True)
