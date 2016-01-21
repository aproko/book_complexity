import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np

def graph(input_x, input_y, title_labels):
    x_data = np.asarray(input_x)
    y_data = np.asarray(input_y)
    graph_name = "Number of Unique Words versus Total Word Count"


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
    layout = go.Layout(
                       dict(title=graph_name,
                        hovermode ='closest',
                            # hoverinfo='text',
                        yaxis = dict(title='Number of Unique Words',
                            ticklen=5,
                            gridwidth=2),
                        xaxis = dict(title='Total Number of Words',
                            ticklen=5,
                            gridwidth=2),
                        ),
            annotations=[
                dict(x=215109,
                     y=20612,
                     xref='x',
                     yref='y',
                     text="Moby Dick",
                     showarrow=True,
                     arrowhead=2,
                     arrowsize=1,
                     arrowwidth=2,
                     arrowcolor='#636363',
                     ax=0, 
                     ay=-40),
                dict(x=462033,
                    y=19966,
                     xref='x',
                     yref='y',
                     text="Count of Monte Cristo",
                     showarrow=True,
                     arrowhead=2,
                     arrowsize=1,
                     arrowwidth=2,
                     arrowcolor='#636363',
                     ax=0,
                     ay=-40)
                        ]
            )

    fig = go.Figure(data=data, layout=layout)

    plot_url = py.plot(fig, filename=graph_name)