from typing import Union
from fastapi import FastAPI
import bcrypt

app = FastAPI()
# uvicorn test:app --reload

data : dict = {
    '3cc4505f-3678-414c-b544-e26555728b9c':{
        1726056000 : {
        'completed' : ['Go for a walk','Call Juhi'],
        'not_completed' : ['Complete Abyss 12'],
        'mood' : 4,
        'productivity' : 5,
        'lessons' : 'do or die',
        'thankful' : ['Still alive','Having lovely parents'],
        'sucks' : 'waking up at 5 am.'    
        },
        1726228800 : {
        'completed' : ['Completed 10000 steps'],
        'not_completed' : ['Call Juhi'],
        'mood' : 2,
        'productivity' : 2,
        'lessons' : 'do or die',
        'thankful' : ['Still alive','Having lovely parents'],
        'sucks' : 'Same as usual, waking up at 5 am.'    
        },
        1726358400 : {
        'completed' : ['Go to temple'],
        'not_completed' : ['make Onam Pookalam'],
        'mood' : 4,
        'productivity' : 5,
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
        'lessons' : '',
        'thankful' : [],
        'sucks' : ''    
        }

users_data : dict = {
    '123@gmail.com' : {
        'id': '3cc4505f-3678-414c-b544-e26555728b9c',
        'password': '$2b$12$buI43Y8ggvWzgTyqlLoBxupe/ojPEEKbV/mAofu7pCs/JGQWqn.9G'
    }
}


@app.get("/")
def read_root():
    return {
        'Framework': 'FastAPI',
        'version':'0.111.0',
        'author':'JustEmkay'
            }

@app.get("/connection/")
def connection():
    return True

@app.post("/verify/{email}")
def verify_email(email: str):
    if email in users_data:
        return False
    return True

@app.post("/validate/{email}/{password}")
def validate(email : str , password : str):
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
def get_journal(uid : str,tstamp : int):
    if check_id(uid):
        if not check_timestamp(uid,tstamp):
            create_journal(uid,tstamp)
            
    journal : dict = data[uid][tstamp]
    return journal
