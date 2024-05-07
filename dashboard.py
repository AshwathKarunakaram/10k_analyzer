# Ashwath Karunakaram
# 5/7/24
# DARPA Research App Submission
# Frontend using graphs imported from datascrape.py

import panel as pn
from datascrape import main

pn.extension('plotly')

# Get data from datascrape module
aapl_line_sscore, nvda_line_sscore, aapl_line_stock, nvda_line_stock = main()

#--------------------------------------------------------------------------    
# Callback function to switch between displaying Apple and NVIDIA charts. 
# Parameters: event (Event): The event triggered by dropdown selection.
# Returns: None
#--------------------------------------------------------------------------

def select_chart(event):
    
    if event.new == 'Apple':
        layout[1] = aapl_line_sscore
        layout[2] = aapl_line_stock
    elif event.new == 'NVIDIA':
        layout[1] = nvda_line_sscore
        layout[2] = nvda_line_stock

# Create the dropdown widget
dropdown = pn.widgets.Select(options=['Apple', 'NVIDIA'], name='Select Company')

# Watch for changes in the dropdown selection and trigger the callback function
dropdown.param.watch(select_chart, 'value')

# Define the layout
layout = pn.Column(
    dropdown,
    None,  # Initial chart display
    None
)

# Panel app
layout.servable()

# Create a template instance
template = pn.template.FastListTemplate(
    title='Sentiment Analysis of 2 Companies from 1995-2024',
    main=[pn.Row(pn.Column(pn.Row(layout)))],
    header_background="#c0b9dd",
)

# Show the template
template.show()
