import streamlit as st
import requests,time,pytz
from datetime import datetime as dt, time as t
from rich.console import Console
import bcrypt

console = Console()

URL_API : str = "http://127.0.0.1:8000/"

if 'api_connect' not in st.session_state: st.session_state.api_connect = False
if 'error' not in st.session_state: st.session_state.error = False
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user_id' not in st.session_state: st.session_state.user_id = None
if 'user_journal' not in st.session_state: st.session_state.user_journal = None
tstamp_today : int  = dt.combine(dt.now(pytz.timezone('Asia/Calcutta')),t.min).timestamp()


def connect_api() -> bool:
    r = requests.get(URL_API+'connection')
    response = r.status_code
    if response == 200:
        return r.json()
    return False
        
def send_get():
    r = requests.get(URL_API)
    response = r.status_code
    if response == 200:
        return r.json()
    return 'error occured'

def verify_email(username) -> bool:
    r = requests.post(URL_API+f'verify/{username}')
    response = r.status_code
    if response == 200:
        st.session_state.error = r.json()

def pass_hashing(password : str) -> str:
     
    bytes = password.encode('utf-8') 
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt) 
    
    print("pass:",hash)
    return hash

def data_hashing() -> str:
    ...
 
def login_req(username,password) -> dict:
    r = requests.post(URL_API+f'validate/{username}/{password}')
    response = r.status_code
    if response == 200:
        return r.json()

class ManageJournal:
    def __init__(self,user_id,tstamp_today) -> None:
        self.id : int = user_id
        self.timestmp : int = tstamp_today

    def load_data(self) -> dict:
        r = requests.get(URL_API+f'journal/{self.id}/{self.timestmp}')
        response = r.status_code
        if response == 200:
            return r.json()
        return {}

def homepage() -> None:
    mj : object = ManageJournal(st.session_state.user_id,tstamp_today)
    if not st.session_state.user_journal:
        st.session_state.user_journal = mj.load_data()
        st.spinner("Updating journal....")
        time.sleep(2)
        st.rerun()
    if st.button('rerun'):
        st.rerun()

def main() -> None:
    
    st.session_state
    
    console.print(f'\n[ Executed: [bold magenta]{dt.today().time().strftime("%H:%M:%S")}[/bold magenta] ]')
    st.header('Test FastAPI',anchor=False,divider='rainbow')
    
    if not st.session_state.api_connect:
        with st.status("Sending Request to Server...") as status: 
            time.sleep(1)
            st.session_state.api_connect = connect_api()
            status.update(
                label="Waiting for response", state="running", expanded=False
            )
            time.sleep(1)
            if st.session_state.api_connect:
                status.update(label=":green[Connected]",
                              state="complete", expanded=True)
                time.sleep(1)
                st.success('Connection to API successful',icon='✔')
                st.rerun()
                
            status.update(label=":red[Not Connected]",
                            state="error", expanded=True)
            time.sleep(1)
            st.error('Failed Connection to API',icon='🚫')

    else:
        st.success('Connection to API successful',icon='✔')
        
        if st.session_state.auth and st.session_state.user_id:
            
            homepage()
            
        else:
            #login form
            with st.container(border=True):
                st.subheader('Login',anchor=False,divider=True)
                username =st.text_input("Username:",
                                            placeholder="Enter your username",
                                            label_visibility='collapsed')
                password : str =st.text_input("Password:",
                                            placeholder="Enter your password",
                                            label_visibility='collapsed',
                                            type='password')
                if username : verify_email(username)
                log_btn : bool = False
                if st.session_state.error:
                    st.warning('Email not found',icon='⚠')
                    log_btn : bool = True
                
                blank_col,reg_col,log_col = st.columns([2,1,1])
                if reg_col.button('register',use_container_width=True):
                    ...
                if log_col.button('login',use_container_width=True,
                                type='primary',disabled=log_btn):
                    if username and password:
                        login_response : dict = login_req(username,password)
                        if login_response['auth'] : 
                            st.session_state.auth = login_response['auth']
                            st.session_state.user_id = login_response['user_id']
                            st.spinner("Loading Homepage....")
                            time.sleep(2)
                            st.rerun()
            
    
if __name__ == "__main__":
    main()
