#!/usr/bin/python3
from flask import Flask, jsonify, render_template, make_response
from flask import abort
#from models import storage

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def this_status():
    return jsonify({"status": "Ok"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, debug=True)
