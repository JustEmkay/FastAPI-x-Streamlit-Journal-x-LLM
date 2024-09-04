import streamlit as st 
from main import agenda_box


def main() -> None:
    st.header('Settings ⚙',
              divider='red')
    with st.container(border=True):
        if not st.session_state.journal['agenda_done']:
            agenda_box('Set agenda')
    
if __name__ == '__main__':
    main()