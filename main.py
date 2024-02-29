# import the necessary modules and libraries
from taipy.gui import Gui
import taipy as tp

from pages.dashboard.dashboard import dashboard_md #import dashboard
from pages.root import root, selected_location, selector_location

pages = {
    '/':root,
}


gui_multi_pages = Gui(pages=pages)

if __name__ == '__main__':
    tp.Core().run()
    
    gui_multi_pages.run(title="Sales Dashboard")