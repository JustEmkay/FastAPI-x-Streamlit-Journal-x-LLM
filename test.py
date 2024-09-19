from fastapi import FastAPI
from pydantic import BaseModel
import bcrypt
import uuid

app = FastAPI()
# uvicorn test:app --reload

data : dict = {
    '3cc4505f-3678-414c-b544-e26555728b9c':{
        1726056000 : {
        'completed' : ['Go for a walk','Call vasu'],
        'not_completed' : ['Complete Abyss 12'],
        'mood' : 4,
        'productivity' : 5,
        'stress_level' : 1,
        'social_interaction' : 0,
        'energy_level': 4,
        'lessons' : 'do or die',
        'thankful' : ['Still alive','Having lovely parents'],
        'sucks' : 'waking up at 5 am.'    
        },
        1726228800 : {
        'completed' : ['Completed 10000 steps'],
        'not_completed' : ['Call tuttu'],
        'mood' : 2,
        'productivity' : 2,
        'stress_level' : 4,
        'social_interaction' : 1,
        'energy_level': 1,
        'lessons' : 'do or die',
        'thankful' : ['Still alive','Having lovely parents'],
        'sucks' : 'Same as usual, waking up at 5 am.'    
        },
        1726358400 : {
        'completed' : ['Go to temple'],
        'not_completed' : ['make Onam Pookalam'],
        'mood' : 4,
        'productivity' : 5,
        'stress_level' : 0,
        'social_interaction' : 5,
        'energy_level': 4,
        'lessons' : 'do or die',
        'thankful' : ['Still alive','Having lovely parents'],
        'sucks' : 'Same Same, waking up at 5 am.'
        }
        
    }
                }

temp_journal : dict = {
        'completed' : [],
        'not_completed' : [],
        'mood' : 0,
        'productivity' : 0,
        'stress_level' : 0,
        'social_interaction' : 0,
        'energy_level': 0,
        'lessons' : '',
        'thankful' : [],
        'sucks' : ''    
        }

users_data : dict = {
    '123' : {
        'email' : '123@gmail.com',
        'dob' : 976579200000,
        'id': '3cc4505f-3678-414c-b544-e26555728b9c',
        'password': '$2b$12$buI43Y8ggvWzgTyqlLoBxupe/ojPEEKbV/mAofu7pCs/JGQWqn.9G'
    }
}

class JournalData(BaseModel):
    completed: list
    not_completed: list
    mood: int
    productivity: int
    stress_level: int
    social_interaction: int
    energy_level: int
    lessons: str
    thankful: list
    sucks: str

class RegisterData(BaseModel):
    username: str
    email: str
    dob: int
    password: str

def idgen():
    unique_id = uuid.uuid4()
    return unique_id

@app.get("/")
async def read_root():
    return {
        'Framework': 'FastAPI',
        'version':'0.111.0',
        'author':'JustEmkay'
            }
    
@app.get("/admin/{password}")
async def show_everything(password : str):
    if password == '123':
        return {'users_data' : users_data,
            'journals' : data
            }
    return{
        'data' : None
    }

@app.get("/connection/")
async def connection():
    return True

@app.post("/verify/user/{userinput}")
async def verify_user(userinput: str):
    ud = users_data.keys()
    emails = [users_data[i]['email'] for i in ud]
    if userinput in ud or userinput in emails:
        return False
    return True

@app.post("/verify/username/{uname}")
async def verify_username(uname: str):
    if uname in users_data:
        return True
    return False

@app.post("/validate/{email}/{password}")
async def validate(email : str , password : str):
    user_hash = password.encode('utf-8')
    user_og_hash = users_data[email]['password'].encode()
    result : bool = bcrypt.checkpw(user_hash,user_og_hash)
    if result:
        print(f'id:{users_data[email]["id"]}')
        return {
            'auth': True ,
            'user_id':f'{users_data[email]["id"]}'
            }
    else:
        return {
            'auth':False,
            'user_id': None
            }

@app.post("/register/{tstamp}")
async def validate(tstamp : int ,register_data : RegisterData):
    try:
        new_id : str = idgen()  
        users_data.update({
            register_data.username : {
                'id' : new_id,
                'email': register_data.email,
                'dob' : register_data.dob,
                'password' : register_data.password
            }
        })
        
        data.update({
            new_id : {
                tstamp : temp_journal
            }
        })
        
        return {'status':True}
    
    except Exception as e:
        return {'status':False , 'error': e}
         
def check_id(uid) -> bool:
    if data[uid]:
        return True
    return False

def check_timestamp(uid,tstamp) -> bool:
    if tstamp in data[uid].keys():
        return True
    return False

def create_journal(uid,tstamp) -> None:
    try:
        data.update({
            uid : {
            tstamp : temp_journal
            }
            })
    except Exception as e:
        print(f'Creatte_journal Error:{e}')

@app.get("/journal/{uid}/{tstamp}")
async def get_journal(uid : str,tstamp : int):
    if check_id(uid):
        if not check_timestamp(uid,tstamp):
            create_journal(uid,tstamp)
            
    journal : dict = data[uid][tstamp]
    return journal

@app.post("/journal/{uid}/{tstamp}")
async def update_journal(uid : str,tstamp : int, journal_data: JournalData):
    try:
        data[uid][tstamp] = journal_data 
        journal : dict = data[uid][tstamp]
        status : bool = True
        return {'status':status,'data':journal}
    except:
        status : bool = False
        return {'status':status,'data':journal}
    