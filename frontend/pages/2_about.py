import streamlit as st
from main import agenda_box
from pathlib import Path
import json

img_url = "https://images.unsplash.com/photo-1620034949504-339c43e9cd56?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

def check_for_file(j_path) -> bool:
    my_file = Path(j_path)
    if my_file.is_file():
        return True
    return False

def create_file(j_path) -> None:
    with open(j_path, 'w') as fp:
        json.dump([], fp)


@st.dialog("Storage Mode")
def setup_local(optn):
    
    if optn == 'Local':
        st.caption(f'Selected mode : :green[**{optn}**]')
        j_path : str = st.text_input('Paste Path',
                                     placeholder=r'Example : C:\Users\vasu\Documents',
                                     label_visibility='collapsed') 
        if not j_path:
            downloads_path = str(Path.home() / "Downloads")
            st.write(f':grey[Default location:] {downloads_path}') 
            st.session_state.journal_path = downloads_path + '\journal.json'
            if not check_for_file(st.session_state.journal_path):
                create_file(st.session_state.journal_path)
            
        else:
            st.session_state.journal_path = j_path + '\journal.json'
            if not check_for_file(st.session_state.journal_path):
                create_file(st.session_state.journal_path)
            
        if st.button('set as storage mode'):
            st.session_state.first_time = True
            st.switch_page('main.py')
    

def main():

    st.header("Journal",divider=True,anchor=False)
    col1,col2 = st.columns([3,1])
    col1.image(img_url)
    col2.write(r'"Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."\
"There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain..."')
    
    st.divider()
    
    st.subheader("First setup",divider=True,anchor=False)
    col3, col4 = st.columns([1,3])
    col3.write(r'"Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."\
"There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain..."')
    with col4.container(border=True,
                        height=300):
       agenda_box('create agendas')
       
    st.divider()
    
    st.subheader("Mode of Storage",divider=True,anchor=False)
    col5, col6 = st.columns([3,1])
    
    storage_modes : list[str] = [
            'Local',
            'Database',
        ]
    
    col5.image('https://images.unsplash.com/photo-1691458594782-2cef9a152bb3?q=80&w=1931&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
    with col6.container(border=True,height=250):
        slctd_optn = st.radio(f"Selected mode of storage : :green[{storage_modes[st.session_state.mode_of_storage]}]",
                 storage_modes,
                 index=st.session_state.mode_of_storage,
                 horizontal=True)
        if st.button(f'Set **{slctd_optn}** as storage mode',
                     type='primary',use_container_width=True):
            setup_local(slctd_optn)
    
    st.write(r'"Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."\
"There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain..."')

    
    
if __name__ == '__main__':
    main()