import pandas as pd
from taipy.gui import Markdown
import pandas  as pd
import plotly.express as px

data = pd.read_csv('../data/supermarket_sales.csv')

# convert the list of data to a pandas DataFrame
data = pd.DataFrame(data)

# select only the desired columns in order
data = data.loc[:, ['location', 'lastUpdatedTimestamp', 'incidentLocation', 'stageOfControlCode', 'incidentSizeEstimatedHa']]


'''
selected_location = 'North Arm Stuart Lake'
data_location = None

def initialize_case_evolution(data, selected_location='China'):
    # Aggregation of the dataframe to erase the regions that will not be used here
    data_location = data.groupby(["Location",'Discovery Date'])\
                            .sum()\
                            .reset_index()
    
    # a location is selected, here North Arm Stuart Lake by default
    data_location = data_location.loc[data_location['Location']==selected_location]
    return data_location

data_location = initialize_case_evolution(data)

def on_change_location(state):
    # state contains all the Gui variables and this is through this state variable that we can update the Gui
    # state.selected_location, state.data_location, ...
    # update data_location with the right location (use initialize_case_evolution)
    print("Chosen location: ", state.selected_location)
    state.data_location = initialize_case_evolution(data, state.selected_location)'''
    

dashboard_md = Markdown("pages/dashboard/dashboard.md")