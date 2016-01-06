import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np

def graph(input_x, input_y, title_labels, graph_name):
    x_data = np.asarray(input_x)
    y_data = np.asarray(input_y)


# Creates a trace
    trace = go.Scatter(
                x = x_data,
                y = y_data,
                mode = 'markers',
                marker = dict(
                    size = 12,
                              #color = genres,
                              #colorscale='Viridis',
                    color = 'rgba(255,182,193, .9',
                    line = dict(width = 1)),
                text=title_labels,
                       )

    data = [trace]
    layout = dict(title = graph_name,
                  hovermode ='closest',
                  yaxis = dict(title='Average TF-IDF',
                               ticklen=5,
                               gridwidth=2),
                  #zeroline = False),
                  xaxis = dict(title='Length',
                               ticklen=5,
                               gridwidth=2),
                  #zeroline = True)
                  )

    fig = go.Figure(data=data, layout=layout)

# Plot and embed in ipython notebook!
#py.plot(data, filename='basic-scatter')

# or plot with:
    plot_url = py.plot(fig, filename=graph_name)