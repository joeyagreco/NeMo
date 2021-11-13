from flask import Flask

from server.Pinger import Pinger
from util.EnvironmentReader import EnvironmentReader

app = Flask(__name__)

if __name__ == "__main__":
    from views.admin import *
    from views.device import *

    test = Pinger.ping("8.8.8.8")
    print(test)

    if EnvironmentReader.get("TEST_ENVIRONMENT") == "True":
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0", port=80)
