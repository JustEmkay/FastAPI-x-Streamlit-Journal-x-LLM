import streamlit as st
import requests,time,pytz
from datetime import datetime as dt, time as t
from rich.console import Console
import bcrypt
import streamlit.components.v1 as components


console = Console()

URL_API : str = "http://127.0.0.1:8000/"

if 'api_connect' not in st.session_state: st.session_state.api_connect = False
if 'error' not in st.session_state: st.session_state.error = False
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user_id' not in st.session_state: st.session_state.user_id = None
if 'user_journal' not in st.session_state: st.session_state.user_journal = None
tstamp_today : int  = dt.combine(dt.now(pytz.timezone('Asia/Calcutta')),t.min).timestamp()


def connect_api() -> bool:
    try:
        r = requests.get(URL_API+'connection')
        response = r.status_code
        if response == 200:
            return r.json()
        return False
        
    except requests.ConnectionError:
        st.error("Connection Error : API not running",icon='❗')
        if st.button("Retry"):
            st.rerun()
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

@st.dialog('Preview')
def journal_preview() -> None:
    st.session_state.user_journal  

def add_agenda() -> None:
    task_col, addBtn_col = st.columns([3,1])
    new_task : str = task_col.text_input('Task',value='',
                               label_visibility='collapsed',
                               placeholder='What you want to accomplish?',
                               help="Example: Go for a walk")
    with addBtn_col.popover('options',use_container_width=True):
        
        if st.button('Add',use_container_width=True,type='primary') and new_task:
            st.session_state.user_journal['not_completed'].append(new_task)
            st.rerun()
            
        
        if st.button('Delete',use_container_width=True,
                     help=':red-background[Delete all completed task]'):
            st.session_state.user_journal['completed'] = []
            st.rerun()

def add_thankful() -> None:
    thankful_col, add_col = st.columns([3,1])
    thankful : str = thankful_col.text_input('Thankful',value='',
                               label_visibility='collapsed',
                               placeholder='Today, I am thankful for .....',
                               help="Example: That im still alive 🙏")
    if add_col.button("add",use_container_width=True,
                      type='primary') and thankful:
        st.session_state.user_journal['thankful'].append(thankful)
        st.rerun()

def add_lessons() -> None:
    with st.container(border=True):
        lessons : str = st.text_area("lesssons learned",
                                     value=st.session_state.user_journal['lessons'],
                                     label_visibility='collapsed')
        sucks : str = st.text_input('still sucks',
                                    value=st.session_state.user_journal['sucks'],
                                    label_visibility='collapsed')
        
        if st.session_state.user_journal['lessons'] and st.session_state.user_journal['sucks']:
            bttn_name = 'update'
        else: 
            bttn_name = 'add'
        black_col, bttn_col = st.columns([3,1])
        if bttn_col.button(bttn_name,use_container_width=True,
                           type='primary',key='lesson_btn'):
            st.session_state.user_journal['lessons'] = lessons
            st.session_state.user_journal['sucks'] = sucks
            time.sleep(1)
            st.rerun()

def update_agenda(task_action : list ,task_id : int) -> bool:
    st.session_state.user_journal[task_action[0]].append(st.session_state.user_journal[task_action[1]][task_id])
    st.session_state.user_journal[task_action[1]].pop(task_id)
    return True

def agenda_box():
    add_agenda()
    cmpltd_col, ncmpltd_col = st.columns(2)
    ncmpltd : list = st.session_state.user_journal['not_completed']
    cmpltd : list = st.session_state.user_journal['completed']

    #---LEFT-AGENDA.CONTAINER---
    with cmpltd_col.container(border=True,height=400):
        st.write(':red-background[Not Completed ❎]')
        if ncmpltd:
            for nid,ntask in enumerate(ncmpltd):
                if st.checkbox(ntask,key='n'+str(nid),value=False):
                    if update_agenda(['completed','not_completed'],nid):    
                        st.rerun()
        else:
            st.text('--Empty--')        
    #---RIGHT-AGENDA.CONTAINER---
    with ncmpltd_col.container(border=True,height=400):
        st.write(':green-background[Yes Completed ✅]')
        if cmpltd: 
            for cid,ctask in enumerate(cmpltd):
                if not st.checkbox(ctask,key='c'+str(cid),value=True):
                    if update_agenda(['not_completed','completed'],cid):    
                        st.rerun()
        else:
            st.text('--Empty--') 
    
def thankful_box() -> None:
    add_thankful()
    
    thankful : dict = st.session_state.user_journal['thankful']
    
    with st.container(border=True):
        if thankful:
            for idx, thank in enumerate(thankful):
                if st.checkbox(f'{idx+1}.'+thank,key=idx,value=False):
                    with st.spinner('delete this note in 3s...'):
                        time.sleep(3)
                        st.session_state.user_journal['thankful'].pop(idx)
                        st.toast(':green-background[Deleted selected thank note]')
                        time.sleep(1)
                        st.rerun()
        else:
            st.text('--Empty--')

def lesson_box() -> None:
    lessons : str = st.session_state.user_journal['lessons']
    sucks : str = st.session_state.user_journal['sucks']
    add_lessons()
    

def homepage() -> None:
    mj : object = ManageJournal(st.session_state.user_id,tstamp_today)
    if not st.session_state.user_journal:
        st.session_state.user_journal = mj.load_data()
        st.spinner("Updating journal....")
        time.sleep(2)
        st.rerun()
    
    #---JOURNAL-CONTAINER---
    with st.container(border=True,height=600):
        date_col, preview_col = st.columns([3,1])
        date_col.write(f'Date : {dt.fromtimestamp(tstamp_today).strftime("%d-%m-%Y")}',
                 anchor=False)
        if preview_col.button('preview',use_container_width=True):
            journal_preview()
        
        tabs : list[str] = ['Agenda','Thankful','Lessons','Rate']
        tab1, tab2, tab3, tab4 = st.tabs(tabs)
        
        with tab1:
            agenda_box()
        
        with tab2:
            thankful_box()
        
        with tab3:
            lesson_box()
        
        with tab4:
            ...
        
#--MAIN----
def main() -> None:
    
    # st.session_state.user_journal
    
    console.print(f'\n[ Executed: [bold magenta]{dt.today().time().strftime("%H:%M:%S")}[/bold magenta] ]')
    st.header('Journal',anchor=False,divider='rainbow')
    
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
    components.html("""
    <script>
    window.onbeforeunload = function() {
        return 'Are you sure you want to leave? You might lose unsaved data.';
    };
    </script>
    """, height=0)
