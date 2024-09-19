from fastapi import FastAPI
from pydantic import BaseModel
import bcrypt,uuid
import pytz,json,os.path
from datetime import datetime as dt , time as t

tstamp_today : int  = int(dt.combine(dt.now(pytz.timezone('Asia/Calcutta')),t.min).timestamp())

PATHS : tuple = ('database/users_data.json','database/journal_data.json')
PATH_TEMP_DATAS : tuple = {
    PATHS[0] : {
    '123' : {
        'email' : '123@gmail.com',
        'dob' : 976579200000,
        'id': '3cc4505f-3678-414c-b544-e26555728b9c',
        'password': '$2b$12$buI43Y8ggvWzgTyqlLoBxupe/ojPEEKbV/mAofu7pCs/JGQWqn.9G'
    }
},
    PATHS[1] : {
        '3cc4505f-3678-414c-b544-e26555728b9c':{
        tstamp_today : {
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
        },
    }
}
}


app = FastAPI()
# uvicorn test:app --reload

def check_file_exists() -> None:
    count : int = 0
    for path in PATHS:
        if not os.path.exists(path):        
            try:
                with open(path,"w") as outfile:
                    json.dump(PATH_TEMP_DATAS[path],outfile)                        
            except Exception as e:
                print(f'Error: {e}')
        else:
            try:
                with open(path,"r") as outfile:
                    outfile.seek(0, os.SEEK_END)
                    file_size = outfile.tell()
                    if (file_size == 0):
                        with open(path,"w") as outfile:
                            json.dump(PATH_TEMP_DATAS[path],outfile)  
            except Exception as e:
                print(f'Error: {e}')
            finally:
                count+=1
    print(f"\nFound:{count}/{len(PATHS)}")
    if count != len(PATHS):
        check_file_exists()

def retrive_data(path) -> dict:
    check_file_exists()
    with open(path,'r') as f:
        d = json.load(f)
        return d

def update_data(path,data) -> dict:
    check_file_exists()
    with open(path,'w') as f:
        json.dump(data,f)

check_file_exists() #<- check DB exist 

users_data : dict = retrive_data(PATHS[0])
data : dict = retrive_data(PATHS[1])
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


# data : dict = {
#     '3cc4505f-3678-414c-b544-e26555728b9c':{
#         1726056000 : {
#         'completed' : ['Go for a walk','Call vasu'],
#         'not_completed' : ['Complete Abyss 12'],
#         'mood' : 4,
#         'productivity' : 5,
#         'stress_level' : 1,
#         'social_interaction' : 0,
#         'energy_level': 4,
#         'lessons' : 'do or die',
#         'thankful' : ['Still alive','Having lovely parents'],
#         'sucks' : 'waking up at 5 am.'    
#         },
#         1726228800 : {
#         'completed' : ['Completed 10000 steps'],
#         'not_completed' : ['Call tuttu'],
#         'mood' : 2,
#         'productivity' : 2,
#         'stress_level' : 4,
#         'social_interaction' : 1,
#         'energy_level': 1,
#         'lessons' : 'do or die',
#         'thankful' : ['Still alive','Having lovely parents'],
#         'sucks' : 'Same as usual, waking up at 5 am.'    
#         },
#         1726358400 : {
#         'completed' : ['Go to temple'],
#         'not_completed' : ['make Onam Pookalam'],
#         'mood' : 4,
#         'productivity' : 5,
#         'stress_level' : 0,
#         'social_interaction' : 5,
#         'energy_level': 4,
#         'lessons' : 'do or die',
#         'thankful' : ['Still alive','Having lovely parents'],
#         'sucks' : 'Same Same, waking up at 5 am.'
#         }
        
#     }
#                 }

# users_data : dict = {
#     '123' : {
#         'email' : '123@gmail.com',
#         'dob' : 976579200000,
#         'id': '3cc4505f-3678-414c-b544-e26555728b9c',
#         'password': '$2b$12$buI43Y8ggvWzgTyqlLoBxupe/ojPEEKbV/mAofu7pCs/JGQWqn.9G'
#     }
# }

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
    print("verify:",users_data)
    
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

@app.post("/validate/{user_input}/{password}")
async def validate(user_input : str , password : str):
    
    ud = users_data.keys() # <- username as key 
    emails = [users_data[i]['email'] for i in ud]
    if user_input in ud:
        user_input_un = users_data[user_input]
    else:
        user_input_un = users_data[ud[emails.index(user_input)]]["email"]
    
    user_hash = password.encode('utf-8')
    user_og_hash = users_data[user_input_un]['password'].encode()
    result : bool = bcrypt.checkpw(user_hash,user_og_hash)
    if result:
        print(f'id:{users_data[user_input_un]["id"]}')
        return {
            'auth': True ,
            'user_id':f'{users_data[user_input_un]["id"]}'
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
        
        update_data(PATHS[0],users_data) #<-- update to JSON file
        users_data = retrive_data(PATHS[0])
        
        data.update({
            new_id : {
                tstamp : temp_journal
            }
        })
        
        update_data(PATHS[1],data) #<-- update to JSON file
        data = retrive_data(PATHS[1])
        
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
        
        update_data(PATHS[1],data) #<-- update to JSON file
        data = retrive_data(PATHS[1])
        
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
        
        update_data(PATHS[1],data) #<-- update to JSON file
        data = retrive_data(PATHS[1])
        
        return {'status':status,'data':journal}
    except:
        status : bool = False
        return {'status':status,'data':journal}
    