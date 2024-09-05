import streamlit as st 
from quote import quote
from datetime import datetime
import time
import app_config
import json
from dbModes.sModes import sModes

#session stuffs

def session_validation():
    if 'first_time' not in st.session_state:
        st.session_state.first_time = False 
    
    if 'mode_of_storage' not in st.session_state:
        st.session_state.mode_of_storage = 0
    
    if 'quote' not in st.session_state:
        try:
            raise Exception("Error Occured")
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
                'id' : 1 ,
                'productivity' : 0,
                'mood' : 0,
                'agenda_not_done' : [],
                'agenda_done' : [],
                'thankful' : [],
                'lessons' : "",
                'sucks' : 'sleep early/ wake up at 5am',
                'created_date' : today
            }

        # path : str = st.session_state.journal_path
        # with open(path) as fp:
        #     journal_stored_data = json.load(fp)
        #     if journal_stored_data:
        #         if journal_stored_data[-1]['created_date'] < today :
        #             st.session_state.journal = {
        #                     'productivity' : 0,
        #                     'mood' : 0,
        #                     'agenda_not_done' : [],
        #                     'agenda_done' : [],
        #                     'thankful' : [],
        #                     'lessons' : "",
        #                     'sucks' : 'sleep early/ wake up at 5am',
        #                     'created_date' : today
        #                 }
        #         if journal_stored_data[-1]['created_date'] == today :
        #             st.session_state.journal = journal_stored_data[-1]
     
    if 'journal_path' not in st.session_state :
        st.session_state.journal_path = r'C:\Users\USER\Downloads\journal.json'
                
#functions 
        
def update_agenda(type : str, id : int) -> None:
    
    if type == 'completed':
        print("\nCompeted Function running.")
        try:
            selctd = st.session_state.journal['agenda_not_done'][id]
            print(f"{selctd}")
            st.session_state.journal['agenda_done'].append(selctd)
            st.session_state.journal['agenda_not_done'].pop(id)
            st.toast(f':green-background[Task Completed]')
            time.sleep(1)
        except Exception as e:
            print(f'Error Occured:{e}')
        finally:
            st.rerun()
                
    if type == 'not_completed':
        print("\nNot_Competed Function running.")
        try:
            selctd = st.session_state.journal['agenda_done'][id]
            print(f"{selctd}")
            st.session_state.journal['agenda_not_done'].append(selctd)
            st.session_state.journal['agenda_done'].pop(id)
            st.toast(f':red-background[Task not Completed]')
            time.sleep(1)
        except Exception as e:
            print(f'Error Occured:{e}')
        finally:
            st.rerun()

#tab containers
    
def mood_box(tab_name : str) -> None:
    st.header(tab_name,anchor=False)
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

def agenda_box(tab_name : str) -> None:
    
    head_c, bttn_c = st.columns([3,1],vertical_alignment='center')
    head_c.subheader(tab_name,anchor=False)
    
    if bttn_c.button('clear',
                     use_container_width=True,
                     help=':red[Clear all completed agendas]'):
        st.session_state.journal['agenda_done'] = []
        st.toast(':green-background[All Completed Agenda cleared]')
    
    if len(st.session_state.journal['agenda_not_done'] + 
           st.session_state.journal['agenda_done']) != 5:
        
        col1, col2 = st.columns([3,1],vertical_alignment='center') 
        agenda_input : str = col1.text_input('Enter agenda',
                                             placeholder='Example: walk min.10000 steps',
                                             label_visibility='collapsed')
        if col2.button("create",
                       type='primary',
                       use_container_width=True):
            st.session_state.journal['agenda_not_done'].append(agenda_input)
            st.toast(":green-background[added successfully]")
    
    
    
    for index,agenda in enumerate(st.session_state.journal['agenda_not_done']):
        if st.checkbox(f'{agenda}',value=False,key=f'nc_{index}'):
            update_agenda('completed',index)
                
    for index_d,agenda_d in enumerate(st.session_state.journal['agenda_done']):
        if not st.checkbox(f'{agenda_d}',value=True,key=f'c_{index_d}'):
            update_agenda('not_completed',index_d)
            
def thankful_box(tab_name : str) -> None:
    st.header(tab_name,anchor=False)
    col1, col2 = st.columns([3,1],
                            vertical_alignment='center')
    thankful_input : str = col1.text_input("Enter here",
                                           label_visibility='collapsed')
    
    if col2.button("Submit",
                   type='primary',
                   use_container_width=True):
        if len(st.session_state.journal['thankful']) !=4:
            st.session_state.journal['thankful'].append(thankful_input)
    
    for index, i in enumerate(st.session_state.journal['thankful']):
        if st.checkbox(i,
                       help="Check to delete",
                       value=False):
            try:
                st.session_state.journal['thankful'].pop(index)
            except Exception as e:
                print("\nError:",e)
            finally:
                st.rerun()
                
def lesson_box(tab_name : str) -> None:
    col1, col2 = st.columns([3,1],
                            vertical_alignment='center')
    col1.header(tab_name,anchor=False)
    if col2.button('clear',
                   help=':red[Clear inputed lessons]',
                   use_container_width=True):
        st.session_state.journal['lessons'] = ""
        st.rerun()
    
    if not st.session_state.journal['lessons']:
        lesson_input : str = st.text_area("lesson",
                                        label_visibility='collapsed',
                                        height=100)
        if st.button("Submit",
                     key='lesson_submit',
                     type='primary'):
            ...
    else:
        st.session_state.journal['lessons']

@st.dialog("Cast your vote")
def setup_local():
    st.write('hello')
    ...

#---------------------------------------------              


def main() -> None:
    sm = sModes(st.session_state.journal['id'],
                st.session_state.journal['productivity'],
                st.session_state.journal['mood'],
                st.session_state.journal['agenda_not_done'],
                st.session_state.journal['agenda_done'],
                st.session_state.journal['thankful'],
                st.session_state.journal['lessons'],
                st.session_state.journal['sucks'],
                st.session_state.journal['created_date'],)
    
    sm.test()
    # sm.update_to_local(st.session_state.journal_path)
    
    

    with st.container(border=True,height=610):
        
        st.write(f":green[{datetime.today().strftime('%d:%m:%y')}] | day:d")
        with st.container(border=True):
            st.write(f':grey-background[" {st.session_state.quote["quote"]} "]')
            st.write(f'by {st.session_state.quote["author"]} | :grey[{st.session_state.quote["book"]}]')
        
        tab_names : list[str] = [
            "Rate Today",
            "Today's Agenda",
            "Today, I'm Thankful for",
            "Today's Lessons"]
         
        if len(st.session_state.journal['agenda_done'] + 
               st.session_state.journal['agenda_not_done']) != 0 :
        
            tab1, tab2, tab3, tab4 = st.tabs(tab_names)
            with tab1:
                mood_box(tab_names[0])
                
            with tab2:
                agenda_box(tab_names[1])
                
            with tab3:
                thankful_box(tab_names[2])

            with tab4:
                lesson_box(tab_names[3])
    
        else:
            st.info("You need to set min one agenda",icon='❕')
            st.page_link(page='pages/settings.py',
                label=':green[Add agenda >>]',
                icon="🛠️")
    

#---------MAIN--------------------------------  
if __name__ == "__main__":
    session_validation()
    if not st.session_state.first_time:
        # welcome_popover()
        st.switch_page('pages/2_about.py')
        # first_setup()
    elif st.session_state.first_time:
        main()