import streamlit as st
import requests
from home import URL_API,ManageJournal
from pages.function.journal_graph import cal_heatmap
from datetime import datetime as dt


if 'journals' not in st.session_state: st.session_state.journals = {}
scale : tuple = ('worst', 'poor', 'average', 'good', 'excellent')

def get_journals(uid) -> dict:
    r = requests.get(URL_API+f'records/{uid}')
    response = r.status_code
    if response == 200:
        st.session_state.journals = r.json()
        st.rerun()

def get_summeriztion(uid, slct_stamp) -> str:
    r = requests.get(URL_API+f'summerize/{uid}/{slct_stamp}')
    response = r.status_code
    if response == 200:
        return st.write(r.json())
    else:
        error : dict = r.json()
        return st.error(f"{error['detail']}")

def perview_model(slctd_journal) -> None:
    
    with st.expander("Agendas Completed and not completed"):
        
        if slctd_journal['completed']:
            for c in slctd_journal['completed']:
                st.write(f'~~:grey[{c}]~~')
        else:
            st.write('***---Lazyyyyy---***')

        if slctd_journal['not_completed']:
            for nc in slctd_journal['not_completed']:
                st.write(nc)
        elif slctd_journal['completed'] and not slctd_journal['not_completed']:
            st.write('***---Welldone👏---***')

    with st.expander("Rating of that day!"):
        st.write(f"Your mood ? {scale[slctd_journal['mood']-1]}")
        st.write(f"How much productivity ? {scale[slctd_journal['productivity']-1]}")
        st.write(f"productivity ? {scale[slctd_journal['stress_level']-1]}")
        st.write(f"productivity ? {scale[slctd_journal['social_interaction']-1]}")
        st.write(f"productivity ? {scale[slctd_journal['energy_level']-1]}")


    with st.expander("Lesson Learned :"):
        if slctd_journal['lessons']:
            st.write(f"{slctd_journal['lessons']}")
        else:
            st.write("***:gray[---None---]***")

    with st.expander("One thing that i did, sucked:"):
        if slctd_journal['sucks']:
            st.write(f"{slctd_journal['sucks']}")
        else:
            st.write("***:gray[---None---]***")

def main() -> None: 
    if not st.session_state.auth:
        st.caption("🔏 pleeeease login")
    else:
        col1,col2 = st.columns([0.8,0.2],vertical_alignment='bottom')
        col1.header('Journal Records',divider=True,anchor=False)
        if col2.button("reload",use_container_width=True):
            get_journals(st.session_state.user_id)
            
        error_records = st.empty()
        
        if not st.session_state.journals['status']:
            error_records.error(st.session_state.journals['error'])
            get_journals(st.session_state.user_id)
        else:    
            error_records.success(st.session_state.journals['error'])
            st.pyplot(cal_heatmap(st.session_state.journals['data']))
        
        mnths : list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']
        current_mnt = dt.now().month

        preview_col, list_col = st.columns([0.6,0.4])
        
        with preview_col.container(border=True,height=450):
            st.subheader('Preview:',divider=True,anchor=False)
            preview = st.empty()
            
           
        sum_opt = list_col.radio('🤖Get AI summerization:',['on','off'],
                    horizontal=True,index=1)
        
        with list_col.container(border=True,height=370):
            for index,i in enumerate(mnths):
                expndr : bool = False
                color : str = 'grey'
                if (index+1) == current_mnt:
                    expndr = True
                    color = 'green'
                    
                with st.expander(f'**:{color}[{i}]**',expanded=expndr):
                    for j in st.session_state.journals['data']:
                        if dt.fromtimestamp(int(j)).month == (index+1):
                            if st.checkbox(dt.fromtimestamp(int(j)).strftime('%d-%m-%Y')):
                                mj = ManageJournal(st.session_state.user_id,j)
                                try: 
                                    st.session_state.temp_journal = mj.load_data()
                                    st.session_state.temp_journal.sort(reverse = True)
                                except ConnectionError as e:
                                    st.error(f'Error : {e}')
                                
                                if st.session_state.temp_journal:
                                    
                                    if sum_opt == 'off':
                                        with preview.container():
                                            perview_model(st.session_state.temp_journal)                                        
                                    else:
                                        with preview:
                                            get_summeriztion(st.session_state.user_id,j)
    
if __name__ == '__main__':
    main()