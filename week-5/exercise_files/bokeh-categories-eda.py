from bokeh.io import show, curdoc
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure
from bokeh import layouts
import pandas as pd
import os

# Load previously saved data
df = pd.read_csv(os.path.join('df_categories.csv'))
category_types = ['High-Level Category', 'Mid-Level Category', 'Subcategory']

# Init data source
group = df.groupby(category_types[0])

col1 = group.groups.keys()
print(group.Value.count())
print('Type: ' + str(type(group.Value.count())))

data = pd.DataFrame(group.Value.count())

source = ColumnDataSource(data)

# Create plot and widgets
plot = figure(y_range=group, title='Health Care Service Category Counts')
menu = Select(options=category_types, value=category_types[0], title='Category Type')
plot.hbar(y=menu.value, right='Value', height=0.5, source=source)

print("*** source.data: ***")
print(source.data)

print("\n*** group.describe(): *** \n")
print(group.describe())
print("\n")

# Callback
def callback(attr, old, new):
    print('New menu value: ' + menu.value)
    group = df.groupby(menu.value)
    data = pd.DataFrame(group.Value.count())
    source = ColumnDataSource(data)



    # TODO here: either update properties of plot, or hbar of create new object
    
menu.on_change('value', callback)

# Layout
layout = layouts.row(plot, menu)
curdoc().add_root(layout)


