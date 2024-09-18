import calplot
import matplotlib.pyplot as plt
import pandas as pd
import calplot
from datetime import datetime as dt

test_data : dict = {
    '3cc4505f-3678-414c-b544-e26555728b9c':{
        1725993000 : {
        'completed' : ['Go for a walk','Call vasu'],
        'not_completed' : ['dadadadaad'],
        'mood' : 4,
        'productivity' : 5,
        'stress_level' : 1,
        'social_interaction' : 0,
        'energy_level': 4,
        'lessons' : 'do or die',
        'thankful' : ['Still alive','Having lovely parents'],
        'sucks' : 'waking up at 5 am.'    
        },
        1726165800 : {
        'completed' : ['Completed 10000 steps'],
        'not_completed' : ['4554'],
        'mood' : 2,
        'productivity' : 0,
        'stress_level' : 8,
        'social_interaction' : 8,
        'energy_level': 0,
        'lessons' : '555555',
        'thankful' : ['Still alive','Having lovely parents'],
        'sucks' : 'Same as usual, waking up at 5 am.'    
        },
        1726358600 : {
        'completed' : [],
        'not_completed' : ['make Onam Pookalam'],
        'mood' : 4,
        'productivity' : 5,
        'stress_level' : 0,
        'social_interaction' : 5,
        'energy_level': 4,
        'lessons' : 'do or die',
        'thankful' : ['Still alive','Having lovely parents'],
        'sucks' : 'Same Same, waking up at 5 am.'
        }
        
    }
                }

id = '3cc4505f-3678-414c-b544-e26555728b9c'

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
                
def active_data(id,data,days) -> list:
    
    active_dates : list = []
    for i in days:
        slctd_timestamp = int(dt.timestamp(i))
        if slctd_timestamp in data[id]:
            prcnt = completion_calc(slctd_timestamp)
            active_dates.append(prcnt)
        else:
            active_dates.append(0)
    
    return active_dates
            
def cal_heatmap(data : str,id : str):
    """
    function retruns plt
    use pyplot to get figure
    
    """
    days = pd.date_range(start_date, end_date, freq='D')
    active_day = active_data(id,data,days)

    series = pd.Series(active_day, index=days)
    calplot.calplot(series, cmap='YlGn', colorbar=True)
    st.pyplot(plt)
    
    
if __name__ == "__main__":    
    cal_heatmap(test_data,id)
