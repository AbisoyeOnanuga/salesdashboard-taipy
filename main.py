from taipy.gui import Gui

from configuration import scenario_cfg
from taipy import Core
from pages import *

from pages.Overview import Overview
from pages.Analysis import Analysis
from pages.Predictions import Predictions
from pages.root import root_page

pages = {
    "/": root_page,
    "overview": Overview,
    "Analysis": Analysis,
    "predictions": Predictions
}

if __name__ == "__main__":
    gui = Gui(pages)
    gui.run(title="Sales Dashboard", port=3000)