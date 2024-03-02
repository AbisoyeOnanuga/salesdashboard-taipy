# import the necessary modules and libraries
from taipy.gui import Gui, Markdown
import pandas as pd
import taipy as tp
import plotly.express as px
import taipy.gui.builder as tgb
import numpy

data = pd.read_csv('data/supermarket_sales.csv')

def create_pie_fig(data, group_by: str):
    grouped_data = data.groupby(group_by)['Total'].sum().reset_index()
    grouped_data['Total'] = grouped_data['Total'].round(2)
    fig = px.pie(grouped_data, names=group_by, values='Total', title=f"Sales Performance by {group_by}", hole=0.3)
    return fig

def create_bar_figure(data, group_by: str):
    sales_over_time = data.groupby(group_by)['Total'].sum().reset_index()
    fig = px.bar(sales_over_time, x=group_by, y='Total', title='Sales Trends Over Time', color='Total')
    return fig

data["size"] = numpy.interp(data["Total"], [data["Total"].min(), data["Total"].max()], [8, 60])

# Add a column holding the bubble hover texts
# Format is "<Location> [<Stage of Control>]"
data["text"] = data.apply(lambda row: f"Location: {row['City']}<br> Branch: [{row['Branch']}]<br> Quantity: {row['Quantity']}<br> Date: {row['Month_Year']}", axis=1)

hoverlabel = {
    # Use a transparent grey color for the background
    "bgcolor": "rgba(128, 128, 128, 0.5)",
    # Use a black color for the border
    "bordercolor": "black",
    # Use a black color and a 12px size for the font
    "font": {"color": "black", "size": 12},
    # Use a left alignment for the text
    "align": "left"
}

marker = {
    # Use the "size" column to set the bubble size
    "size": "size",
    # Use the "stageOfControlCode" column to set the marker color
    "color": "stage of Control",
    # Use a discrete color map to assign different colors to different stages of control
    "color_discrete_map": {"Out of Control": "red", "Being Held": "orange", "Under Control": "green"},
    "text": "text",
    # Use the "hoverlabel" parameter to customize the hover text box
    "hoverlabel": "hoverlabel"
}

layout = {
    "geo": {
        "showland": False,
        "showocean": False,
        "scope": "canada",
        "subunitcolor": "lightgrey",
        "subunitwidth": 2,
        "coastlinewidth": 1,
        "center": {"lat": 54.5, "lon": -125.5},
        "fitbounds": "locations",
        "projection_scale": 1,
        "showcountries": True,
        "countrycolor": "white",
        "countrywidth": 2,
        "showsubunits": True,
        "showcoastlines": True,
        "showlakes": True,
        "showrivers": True,
        "resolution": 100,
        "projection": "van der grinten"
    }
}

def create_perc_fig(df, group_column):
    # Group, sum, and convert to percentage
    df = df.groupby(['Month)Year', group_column])['Total'].sum().unstack(fill_value=0)
    df = df.div(df.sum(axis=1), axis=0).reset_index().melt(id_vars='Month_Year', var_name=group_column, value_name='Percentage')
    df['Percentage'] = (df.loc[:, 'Percentage'].round(3) * 100)

    # Create and return the plot
    fig = px.bar(df, x='Month_Year', y='Percentage', color=group_column, title=f"Evolution of Sales by {group_column} over Time", labels={'Percentage': '% of Total'}, text_auto=True)
    return fig

# fig_map = create_sales_by_city_map(data)

with tgb.Page() as page:
    tgb.text("Sales Insights", class_name="h1")

    with tgb.layout("1 1 1"):
        with tgb.part():
            tgb.text("Toatal Sales", class_name="h1")
            tgb.text("{int(data['Total'].sum())}", class_name="h3")
   
        with tgb.part():
            tgb.text("Average Sales", class_name="h1")
            tgb.text("{int(data['Total'].mean())}", class_name="h3")
        
        with tgb.part():
            tgb.text("Mean Rating", class_name="h1")
            tgb.text("{int(data['Rating'].mean())}", class_name="h3")

    tgb.chart(figure="{layout}")

    tgb.table("{data}")

if __name__ == '__main__':
    gui = Gui(page)
    gui.run(title="Sales Dashboard", port=3000)