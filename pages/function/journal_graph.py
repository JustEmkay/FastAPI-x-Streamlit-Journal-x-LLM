import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

# def radar_graph(kwargs):
#     """
#     input rating as dict and return Radar graph
    
#     Return: Figure
#     """
    
#     # journal_data = {
#     #     'mood': 3,
#     #     'productivity': 4,
#     #     'energy_level': 2,
#     #     'stress_level': 3,
#     #     'social_interaction': 5,
#     #     'dadadadad' : 8
#     # }

#     labels = list(kwargs.keys())
#     ratings = list(kwargs.values())

#     num_vars = len(labels)
#     print("\n numvar: ", num_vars)

#     angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

#     ratings += ratings[:1]
#     angles += angles[:1]

#     fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

#     ax.fill(angles, ratings, color='blue', alpha=0.25)
#     ax.plot(angles, ratings, color='blue', linewidth=2)

#     ax.set_xticks(angles[:-1])
#     ax.set_xticklabels(labels)

#     return fig


def radar_graph(kwargs):
    """
    input rating as dict and return Radar graph
    
    Return:
    """
    
    # Extract labels and data
    labels = list(kwargs.keys())
    ratings = list(kwargs.values())

    # Add the first value to the end to close the radar graph
    ratings += ratings[:1]
    labels += labels[:1]

    # Create radar chart using plotly
    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=ratings,
                theta=labels,
                fill='toself',
                name='Ratings',
                line=dict(color='blue')
            )
        ],
        layout=go.Layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5])
            ),
            showlegend=False
        )
    )

    # Display the chart in Streamlit
    return fig