import os

from flask import Flask
from server.util.EnvironmentReader import EnvironmentReader

from server.Pinger import Pinger

# set directories
templateDir = os.path.join(os.path.dirname(__file__), "client//templates")
staticDir = os.path.join(os.path.dirname(__file__), "client//static")
app = Flask(__name__, template_folder=templateDir, static_folder=staticDir)

if __name__ == "__main__":

    test = Pinger.ping("8.8.8.8")
    print(test)

    if EnvironmentReader.get("TEST_ENVIRONMENT") == "True":
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0", port=80)
