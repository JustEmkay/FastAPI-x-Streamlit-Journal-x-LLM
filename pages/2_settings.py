import streamlit as st
import time
import requests
from home import URL_API,tstamp_today,ManageJournal

st.set_page_config(
    page_title="Settings",
    page_icon="⚙",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def set_predef_agenda(uid,predef,tstamp) -> dict:
    r = requests.post(URL_API+f'predef/{uid}/{str(tstamp)}',json=predef)
    response = r.status_code
    if response == 200:
        return r.json()
    else:
        return {
            'status' : False,
            'error' : 'dadw'
        }

def delete_predef(uid,predef) -> dict:
    
    r = requests.post(URL_API + f'prdef/delete/{uid}',json=predef)
    response = r.status_code
    if response == 200:
        return r.json()
    return {
            'status' : False,
            'error' : f'Error occured when deleting',
            'datat' : None,
        }
    
    
    

def set_agenda() -> None:

    with st.expander("Set agendas"):

        st.caption('Set predefined agendas as default.')
        agendas : str = st.text_input('agendas',placeholder='Enter agendas',
                                      label_visibility='collapsed',value='')
        if agendas:
            if agendas not in st.session_state.settings['predef']: 
                st.session_state.settings['predef'].append(agendas)
        
        with st.container(border=True):
            chkbx : list[str] = []
            if st.session_state.settings['predef']:
                for task in st.session_state.settings['predef']:
                    if st.checkbox(task):
                        chkbx.append(task)
        
        col1,col2,col3 = st.columns([2,1,1])
        error = st.empty()
        
        if col2.button('delete',use_container_width=True,help='delete selected predefined agenda'):
            if chkbx:
                delete = delete_predef(st.session_state.user_id,chkbx)
                if delete['error'] and not delete['status']:
                    error.error(f'Error:{delete["error"]}')
                if delete['status'] and not delete['error']:
                    st.session_state.settings['predef'] = delete['data']
                    st.rerun()
            else:
                error.warning("Please input minimum one agenda first")

            
        if col3.button('set as default',use_container_width=True,type='primary'):
            if st.session_state.settings['predef']:
                result = set_predef_agenda(st.session_state.user_id,st.session_state.settings['predef'],tstamp_today)
                if result['status']:
                    st.success('Added Sccessful',icon='✔')
                            
                       
                else:
                    st.error(f'Failed to updated : {result["error"]}',icon='❌')
            else:
                error.warning("Enter something bruu!!",icon='🤦‍♂️')
                

def import_journal() -> None:
    with st.expander("Import journals from backup",expanded=True):
        st.subheader('Import Backup',anchor=False,divider=True)
        with st.container(border=True):
            ...
            

def export_journal() -> None:
    with st.expander("Export your journal as backup JSON file"):
        st.subheader('Export & Backup',anchor=False,divider=True)
        with st.container(border=True):
            ...
            
            

def main():
    if not st.session_state.auth:
        login_warning = st.empty()
        login_warning.caption('pleeease login to access settings🙏')
        for i in range(10):
            time.sleep(1)
            login_warning.caption(f'switching to login page in {i}s')
        st.switch_page('home.py')
    
    else:
        
        st.header('settings',divider='red',anchor=False)    
        
        set_agenda()
        
        import_journal()
        
        export_journal()
        
    
if __name__ == '__main__':
    main()