import os

from flask import Flask

from server.Pinger import Pinger
from server.util.EnvironmentReader import EnvironmentReader

# set directories
templateDir = os.path.join(os.path.dirname(__file__), EnvironmentReader.get("TEMPLATE_DIR_RELATIVE_PATH"))
staticDir = os.path.join(os.path.dirname(__file__), EnvironmentReader.get("STATIC_DIR_RELATIVE_PATH"))
app = Flask(__name__, template_folder=templateDir, static_folder=staticDir)

if __name__ == "__main__":
    from server.controllers.adminController import *
    from server.controllers.deviceController import *
    from server.controllers.pageController import *
    from server.controllers.settingsController import *

    test = Pinger.ping("8.8.8.8")
    print(test)

    if EnvironmentReader.get("TEST_ENVIRONMENT") == "True":
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0", port=80)
