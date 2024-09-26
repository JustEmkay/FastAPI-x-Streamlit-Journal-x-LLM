import streamlit as st
import time

def main()->None:
    st.title("Logout",anchor=False)
    st.divider()
    
    if 'auth' not in st.session_state:
        st.switch_page('web.py')
    
    if st.session_state.auth:
        st.markdown("### Are you sure?")
        st.caption('Do you want to logout?')
        
        st.divider()
        col1, col2, col3 = st.columns([2,1,1])
        if col2.button("cancel",use_container_width=True):
            st.switch_page('web.py')
        if col3.button("Yep, I'm Positive",use_container_width=True,
                    type='primary'):
            st.session_state.update(
            {
            'user_journal' : None,
            'auth' : False,
            'hash_journal' : None,
            'user_id' : None,
            'journals' : {
                            'status' : False ,
                            'data' : [],
                            'error' : 'Empty '
                        },
            'temp_journal' : {},
            'settings' : {
                'predef' : []
            }
             }
        )
            st.rerun()
    
    else:
        st.caption('pleeease login to logout🤦‍♂️')
        login_warning = st.empty()
        login_warning.caption('pleeease login to access settings🙏')
        for i in range(1,15):
            time.sleep(1)
            login_warning.caption(f'switching to login page in {10-i}s')
        st.switch_page('home.py')

if __name__ == '__main__':
    
    st.set_page_config(
    page_title="Logout",
    page_icon="😢",
    layout="centered",
    initial_sidebar_state="collapsed",
)

    
    
    main()