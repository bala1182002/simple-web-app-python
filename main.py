from flask import Flask
import os
app = Flask(__name__)

@app.route("/")
def hello():
    hostinfo = os.uname()
    return "Hello from "+ str(hostinfo)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
