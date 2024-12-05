import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display

#extract year columns

ANA23.columns = ANA23.columns.str.strip()
Current.columns = Current.columns.str.strip()

year_columns = [str(year) for year in range(1997,2023)]

for year in year_columns:
    if year in ANA23.columns:
       # print(year)
        
        ANA23[year] = pd.to_numeric(ANA23[year],errors = 'coerce').astype(float)
    if year in Current.columns:
        #print("current",year)

        Current[year] = pd.to_numeric(Current[year],errors = 'coerce').astype(float)
#Dropdowns to select the filter widgets

Sector_dropdown = widgets.Dropdown(options = ANA23['Sector'].unique(), description = 'Sector')
Industry_dropdown = widgets.Dropdown(options = ANA23['Industry'].unique(), description = 'Industry')
product_dropdown = widgets.Dropdown(options = ANA23['Product'].unique(), description = 'Product')
Transaction_dropdown = widgets.Dropdown(options = ANA23['Transaction'].unique(), description = 'Transaction')

def plot_filtered_data(sector,industry,product,transaction):
    #filter data based on selection
    filtered_ANA23 = ANA23[(ANA23['Sector'] == sector) &
                            (ANA23['Industry'] == industry) &
                            (ANA23['Product'] == product) &
                            (ANA23['Transaction'] == transaction)]
                            
    filtered_current = Current[(Current['Sector'] == sector) &
                        (Current['Industry'] == industry) &
                        (Current['Product'] == product) &
                        (Current['Transaction'] == transaction)]





    if filtered_ANA23.empty or filtered_current.empty:
                print("No data avaialable for selected combination")
                return

    #Handle null values by replacing them with zeros

    filtered_ANA23[year_columns] = filtered_ANA23[year_columns].fillna(0)
    filtered_current[year_columns] = filtered_current[year_columns].fillna(0)

    #Access row values safely

    ana23_values = filtered_ANA23[year_columns].iloc[0]
    current_values = filtered_current[year_columns].iloc[0]

    #Create line chart
    fig = go.Figure

    #add line for ANA23

    fig.add_trace(go.Scatter(x=year_columns, y = ana23_values,
                             mode = 'lines+markers', name = 'ANA23'))

    fig.add_trace(go.Scatter(x=year_columns, y = current_values,
                             mode = 'lines+markers',name = 'Current'))

    #Update the layout of the chart
    fig.update_layout(title = 'Yearly comparison for selected filter',
                      xaxis_title = 'Year',
                      yaxis_title = 'Values',
                      xaxis_tickangle = -45)
    #Display the chart
    fig.show()

ui = widgets.VBox([Sector_dropdown, Industry_dropdown, product_dropdown, Transaction_dropdown])
out = widgets.interactive_output(plot_filtered_data,{
    'sector': Sector_dropdown,
    'industry':Industry_dropdown,
    'product':product_dropdown,
    'transaction':Transaction_dropdown})

#Display the widgets and the output
display(ui, out)



---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
File ~\Anaconda3\envs\streamlit\lib\site-packages\ipywidgets\widgets\interaction.py:67, in interactive_output.<locals>.observer(change)
     65 with out:
     66     clear_output(wait=True)
---> 67     f(**kwargs)
     68     show_inline_matplotlib_plots()

Cell In[112], line 23, in plot_filtered_data(sector, industry, product, transaction)
     19             return
     21 #Handle null values by replacing them with zeros
---> 23 filtered_ANA23[year_columns] = filtered_ANA23[year_columns].fillna(0)
     24 filtered_current[year_columns] = filtered_current[year_columns].fillna(0)
     26 #Access row values safely

File ~\Anaconda3\envs\streamlit\lib\site-packages\pandas\core\frame.py:4108, in DataFrame.__getitem__(self, key)
   4106     if is_iterator(key):
   4107         key = list(key)
-> 4108     indexer = self.columns._get_indexer_strict(key, "columns")[1]
   4110 # take() does not accept boolean indexers
   4111 if getattr(indexer, "dtype", None) == bool:

File ~\Anaconda3\envs\streamlit\lib\site-packages\pandas\core\indexes\base.py:6200, in Index._get_indexer_strict(self, key, axis_name)
   6197 else:
   6198     keyarr, indexer, new_indexer = self._reindex_non_unique(keyarr)
-> 6200 self._raise_if_missing(keyarr, indexer, axis_name)
   6202 keyarr = self.take(indexer)
   6203 if isinstance(key, Index):
   6204     # GH 42790 - Preserve name from an Index

File ~\Anaconda3\envs\streamlit\lib\site-packages\pandas\core\indexes\base.py:6252, in Index._raise_if_missing(self, key, indexer, axis_name)
   6249     raise KeyError(f"None of [{key}] are in the [{axis_name}]")
   6251 not_found = list(ensure_index(key)[missing_mask.nonzero()[0]].unique())
-> 6252 raise KeyError(f"{not_found} not in index")

KeyError: "['2022'] not in index"








