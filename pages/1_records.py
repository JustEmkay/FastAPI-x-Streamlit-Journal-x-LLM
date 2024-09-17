import streamlit as st
import requests,time,pytz

if 'journals' not in st.session_state: st.session_state.journals = {}

def main() -> None: 
    if not st.session_state.auth:
        st.caption("🔏 pleeeease login")
    else:
        st.header('Journal Records',divider=True)
    
    
if __name__ == '__main__':
    main()