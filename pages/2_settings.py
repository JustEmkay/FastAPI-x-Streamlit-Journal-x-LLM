import streamlit as st
import time

st.set_page_config(
    page_title="Settings",
    page_icon="⚙",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def set_agenda() -> None:

    with st.expander("Set agendas"):

        st.caption('Set predefined agendas as default.')
        agendas : str = st.text_input('agendas',placeholder='Enter agendas',
                                      label_visibility='collapsed')
        if agendas:
            st.session_state.settings['predef'].append(agendas)
        
        with st.container(border=True):
            if st.session_state.settings['predef']:
                st.session_state.settings['predef']
        
        col1,col2,col3 = st.columns([2,1,1])
        
        if col2.button('clear',use_container_width=True):
            st.session_state.settings['predef'] = []
            
        if col3.button('set as default',use_container_width=True,type='primary'):
            ...


def import_export() -> None:
    with st.expander("Import and Export"):
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
        
        import_export()
        
    
if __name__ == '__main__':
    main()