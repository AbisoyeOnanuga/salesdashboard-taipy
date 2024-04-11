from taipy.gui import Markdown
import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb

data = pd.read_csv('data/supermarket_sales.csv')

data['Date'] = pd.to_datetime(data['Date'])
data['Month_Year'] = data['Date'].dt.to_period('M').dt.to_timestamp()

def create_perc_fig(df, group_column):
    # Group, sum, and convert to percentage
    df = df.groupby(['Month_Year', group_column])['Total'].sum().unstack(fill_value=0)
    df = df.div(df.sum(axis=1), axis=0).reset_index().melt(id_vars='Month_Year', var_name=group_column, value_name='Percentage')
    df['Percentage'] = (df.loc[:, 'Percentage'].round(3) * 100)
    
    # Create and return the plot
    fig = px.bar(df, x='Month_Year', y='Percentage', color=group_column, title=f"Evolution of Sales by {group_column} over Time", labels={'Percentage': '% of Total'}, text_auto=True)
    return fig

customer_type = ["Normal", "Member"]
gender = ["Male", "Female"]
city = ["Yangon", "Naypyitaw", "Mandalay"]
filtered_data = data.loc[
    data["City"].isin(city)
]

fig_product_line_perc = create_perc_fig(filtered_data, 'Product_line')
fig_city_perc = create_perc_fig(filtered_data, 'City')
fig_gender_perc = create_perc_fig(filtered_data, 'Gender')
fig_customer_type_perc = create_perc_fig(filtered_data, 'Customer_type')

def on_selector(state):
    filtered_data = state.data.loc[
        state.data["City"].isin(state.city)
    ]

    state.fig_product_line_perc = create_perc_fig(filtered_data, 'Product_line')
    state.fig_city_perc = create_perc_fig(filtered_data, 'City')
    state.fig_gender_perc = create_perc_fig(filtered_data, 'Gender')
    state.fig_customer_type_perc = create_perc_fig(filtered_data, 'Customer_type')


with tgb.Page() as Analysis:
    tgb.text("Analysis", class_name="h2")
    with tgb.layout(columns="1 1 1"):
        tgb.selector(value="{customer_type}", lov=customer_type, multiple=True, dropdown=True, class_name="fullwidth", label="Customer Type")
        tgb.selector(value="{gender}", lov=gender, multiple=True, dropdown=True, class_name="fullwidth", label="Gender")
        tgb.selector(value="{city}", lov=["Yangon", "Naypyitaw", "Mandalay"], dropdown=True, multiple=True, label="Select cities", class_name="fullwidth", on_change=on_selector)

    with tgb.layout("1 1"):
        tgb.chart(figure="{fig_product_line_perc}")
        tgb.chart(figure="{fig_city_perc}")
        tgb.chart(figure="{fig_gender_perc}")
        tgb.chart(figure="{fig_customer_type_perc}")