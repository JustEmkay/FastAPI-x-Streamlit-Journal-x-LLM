import streamlit as st 
from quote import quote
from datetime import datetime
import time

def session_validation():
    if 'quote' not in st.session_state:
        try:
            res = quote('positive',limit=1)
            st.session_state.quote = res[0]
        except:
            print("\nURLError occured.")
            st.session_state.quote = {
                "author": "emkay",
                "book" : "Emotional Damage" ,
                "quote" : "Try not to worry about things you dont have control over."
            }
    
    if 'journal' not in st.session_state:
        today = int(datetime.today().timestamp())
        st.session_state.journal = {
                'id' : 1,
                'productivity' : 0,
                'mood' : 0,
                'agenda_not_done' : ['read 20 pages','walk 10k steps',
                                 'shop thorzhill vartha', 'practice english 20min'],
                'agenda_done' : [],
                'thankful' : [],
                'lessons' : "try not to worry about things you don't have control over",
                'sucks' : 'sleep early/ wake up at 5am',
                'created_date' : today
            }
        

def update_agenda(type : str, id : int):
    
    if type == 'completed':
        print("\nCompeted Function running.")
        try:
            selctd = st.session_state.journal['agenda_not_done'][id]
            print(f"{selctd}")
            st.session_state.journal['agenda_done'].append(selctd)
            st.toast(f':green-background[Task Completed]')
            time.sleep(2)
            st.rerun()
            
        except Exception as e:
            print(f'Error Occured:{e}')
        
                
    if type == 'not_completed':
        print("\nNot_Competed Function running.")
    


def mood_box():
    st.caption("Rate your today's productivity and mood")
    
    col1,col2,col3 = st.columns([1,1,1],vertical_alignment='bottom')
    col4,col5,col6 = st.columns([1,1,1],vertical_alignment='bottom')
    
    selctd_mood = ['Poor','Very Bad','Medium','Good','Excellent']    
    
    col1.text("Productivity:")
    productivity = col2.feedback(options='stars')
    if productivity is not None:
        col3.text(f"{selctd_mood[productivity]}")        
    
    col4.text("Mood:")
    mood = col5.feedback(options='faces')
    if mood is not None:
        col6.text(f"{selctd_mood[mood]}")            

def agenda_box():
    for index,agenda in enumerate(st.session_state.journal['agenda_not_done']):
        if st.checkbox(f'{agenda}',value=False,key=f'nc_{index}'):
            update_agenda('completed',index)  

            
    for index,agenda in enumerate(st.session_state.journal['agenda_done']):
        if not st.checkbox(f'{agenda}',value=True,key=f'c_{index}'):
            update_agenda('not_completed',index)
            
              
def main():
    with st.container(border=True,height=600):
        
        st.write(f":green[{datetime.today().strftime('%d:%m:%y')}] | day:d")
        with st.container(border=True):
            st.write(f':grey-background["{st.session_state.quote["quote"]}"]')
            st.write(f'by {st.session_state.quote["author"]} | :grey[{st.session_state.quote["book"]}]')
        
        tab_names : list[str] = [
            "Rate Today",
            "Today's Agenda",
            "Today, I'm Thankful for",
            "Today's Lessons"]
        
        tab1, tab2, tab3, tab4 = st.tabs(tab_names)
        with tab1:
            st.header(tab_names[0],anchor=False)
            mood_box()
            
        with tab2:
            st.header(tab_names[1],anchor=False)
            agenda_box()
            
        with tab3:
            st.header(tab_names[2],anchor=False)

        with tab4:
            st.header(tab_names[3],anchor=False)
        
    
if __name__ == "__main__":
    session_validation()
    main()