from taipy.gui import Gui
import taipy as tp

from taipy import Core
from pages import Analysis, Overview, Predictions
from pages.root import root

pages = {
    "/": root,
    "overview": Overview,
    "Analysis": Analysis,
    "predictions": Predictions
}

if __name__ == "__main__":
    gui = Gui(pages)
    gui.run(title="Sales Dashboard", port=3000)