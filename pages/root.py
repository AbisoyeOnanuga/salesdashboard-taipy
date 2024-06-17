# import the necessary modules and libraries
import pandas as pd
import taipy.gui.builder as tgb
from taipy.gui import Gui

data = pd.read_csv('data/supermarket_sales.csv')

# Create a page using the correct Taipy GUI builder functions
root_page = tgb.create_page()

with tgb.page() as root_page:
    tgb.toggle(theme= True)
    tgb.text("Sales Insights", class_name="h1")

    with tgb.layout("1 1 1"):
        with tgb.part():
            tgb.text("Total Sales", class_name="h2")
            tgb.text("{int(data['Total'].sum())}", class_name="h3")

        with tgb.part():
            tgb.text("Average Sales", class_name="h2")
            tgb.text("{int(data['Total'].mean())}", class_name="h3")

        with tgb.part():
            tgb.text("Mean Rating", class_name="h2")
            tgb.text("{int(data['Rating'].mean())}", class_name="h3")
    
    tgb.table("{data}")
