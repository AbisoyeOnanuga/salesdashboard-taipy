import pandas  as pd
import plotly.express as px
import taipy.gui.builder as tgb

data = pd.read_csv('../data/supermarket_sales.csv')

# convert the list of data to a pandas DataFrame
data = pd.DataFrame(data)

with tgb.page()  as page:
    tgb.text("Sales Insights", class_name="h1")
    tgb.table("{data}")