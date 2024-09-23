import streamlit as st
import requests
from web import URL_API,ManageJournal
from pages.function.journal_graph import cal_heatmap
from datetime import datetime as dt


if 'journals' not in st.session_state: st.session_state.journals = {}


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
        return r.json()
    else:
        return st.error(f"Error : {r.json()}")



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
                                st.session_state.temp_journal = mj.load_data()
                                if st.session_state.temp_journal:
                                    
                                    if sum_opt == 'off':
                                        preview.write(st.session_state.temp_journal)

                                    else:
                                        preview.write(get_summeriztion(st.session_state.user_id,j))
    
if __name__ == '__main__':
    main()