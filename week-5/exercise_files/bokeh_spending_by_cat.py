from bokeh.io import show, curdoc
from bokeh.models import ColumnDataSource, Select, FactorRange
from bokeh.transform import factor_cmap
from bokeh.palettes import Category10_9
from bokeh.plotting import figure
from bokeh import layouts
import pandas as pd

# Load previously saved data
df = pd.read_csv('rx_df_tidy.csv', index_col=0)


def get_data(year):
    """ Grab data from the DataFrame as the graph expects it. """
    df_sorted = df[df['Year'] == int(year)].groupby('Subcategory').mean().sort_values('Spending per person')
    df_sorted.reset_index(inplace=True)
    return {'x': df_sorted['Spending per person'].tolist(), 'y': df_sorted['Subcategory'].tolist()}


# Init data source
years = df['Year'].unique().astype(str)
data = get_data(years[0])
source = ColumnDataSource(data=data)

# Create plot and widgets
plot = figure(title='Spending by Healthcare Subcategory',
              y_range=FactorRange(factors=data['y']))
plot.hbar(y='y', right='x', left=0, height=0.5, source=source,
          fill_color=factor_cmap('y', palette=Category10_9, factors=data['y']))
menu = Select(options=list(years), value=years[0], title='Year')


def callback(attr, old, new):
    """ Bokeh component callback. """
    print('New menu value: ' + menu.value)
    fresh_data = get_data(menu.value)
    source.data = fresh_data
    plot.y_range.factors = fresh_data['y']


menu.on_change('value', callback)

# Layout
layout = layouts.row(plot, menu)
curdoc().add_root(layout)


