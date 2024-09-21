import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import calplot
from datetime import datetime as dt


# test_data : dict = {
#     '3cc4505f-3678-414c-b544-e26555728b9c':{
#         1725993000 : {
#         'completed' : ['Go for a walk','Call vasu'],
#         'not_completed' : ['dadadadaad'],
#         'mood' : 4,
#         'productivity' : 5,
#         'stress_level' : 1,
#         'social_interaction' : 0,
#         'energy_level': 4,
#         'lessons' : 'do or die',
#         'thankful' : ['Still alive','Having lovely parents'],
#         'sucks' : 'waking up at 5 am.'    
#         },
#         1726165800 : {
#         'completed' : ['Completed 10000 steps'],
#         'not_completed' : ['4554'],
#         'mood' : 2,
#         'productivity' : 0,
#         'stress_level' : 8,
#         'social_interaction' : 8,
#         'energy_level': 0,
#         'lessons' : '555555',
#         'thankful' : ['Still alive','Having lovely parents'],
#         'sucks' : 'Same as usual, waking up at 5 am.'    
#         },
#         1726358600 : {
#         'completed' : [],
#         'not_completed' : ['make Onam Pookalam'],
#         'mood' : 4,
#         'productivity' : 5,
#         'stress_level' : 0,
#         'social_interaction' : 5,
#         'energy_level': 4,
#         'lessons' : 'do or die',
#         'thankful' : ['Still alive','Having lovely parents'],
#         'sucks' : 'Same Same, waking up at 5 am.'
#         }      
#     }
#                 }

# id = '3cc4505f-3678-414c-b544-e26555728b9c'




def radar_graph(kwargs):
    """
    input rating as dict and return Radar graph
    
    """
    
    labels = list(kwargs.keys())
    ratings = list(kwargs.values())

    ratings += ratings[:1]
    labels += labels[:1]

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


crrnt_yr = dt.now().year
start_date = dt(crrnt_yr,1,1,0,0,0)
end_date = dt(crrnt_yr,12,31,0,0,0)

def completion_calc(timestamp : int ,data:dict) -> int:
    """
    Returns completion percentage of each journal
    """
    
    count : int = 0
    slctd_jurnl = data[id][timestamp]
    
    for content in slctd_jurnl:
        if type(slctd_jurnl[content]) == list:
            if content == 'completed' or content == 'thankful' and slctd_jurnl[content]:
                count+=1
        elif type(slctd_jurnl[content]) == str:
            if slctd_jurnl[content]:
                count+=1
        elif type(slctd_jurnl[content]) == int:
            if slctd_jurnl[content] > 0:
                count+=1
           
    percentage : int = (count/(len(data[id][timestamp])-1))*100    
         
    return int(percentage)
                
def active_data(data : list ,days) -> list:
    
    active_dates : list = []
    for i in days:
        start_date = dt(i.year,i.month,i.day,00,00,00)
        slctd_timestamp = int(start_date.timestamp())
        
        if str(slctd_timestamp) in data:
            print(f'{slctd_timestamp} is in data')
            prcnt = 100
            active_dates.append(prcnt)
        else:
            active_dates.append(0)    
            
    return active_dates
                       
def cal_heatmap(data : list):
    """
    function retruns plt
    use pyplot to get figure
    """
    
    days = pd.date_range(start_date, end_date, freq='D')
    active_day = active_data(data,days)

    series = pd.Series(active_day, index=days)
    calplot.calplot(series, colorbar=True)
    
    return plt

def main():
    # cal_heatmap(test_data,id)
    # fig = cal_heatmap(test_data,id)
    # st.pyplot(fig)
    pass

if __name__ == '__main__':
    main()