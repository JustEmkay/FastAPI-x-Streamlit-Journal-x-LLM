from typing import Union
from fastapi import FastAPI
import bcrypt

app = FastAPI()
# uvicorn test:app --reload

data : dict = {
    '3cc4505f-3678-414c-b544-e26555728b9c':{
        'created' : 1726056000,
        'completed' : ['Go for a walk','Call Juhi'],
        'not_completed' : ['Complete Abyss 12'],
    },
    '3cc4505f-3678-414c-b544-e26555728b9c':{
        'created' : 1726228800,
        'completed' : ['Completed 10000 steps'],
        'not_completed' : ['Call Juhi'],
    },
    '3cc4505f-3678-414c-b544-e26555728b9c':{
        'created' : 1726358400,
        'completed' : ['Go to temple'],
        'not_completed' : ['make Onam Pookalam'],
    },
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
async def verify_email(email: str):
    if email in users_data:
        print(users_data[email])
        return False
    return True

@app.post("/validate/{email}/{password}")
async def validate(email : str , password : str):
    user_hash = password.encode('utf-8')
    user_og_hash = users_data[email]['password'].encode()
    result : bool = bcrypt.checkpw(user_hash,user_og_hash)
    if result:
        return {
            'auth': True ,
            'user_id':f'{users_data[email]["id"]}'
            }
    else:
        return {
            'auth':False,
            'user_id': None
            }

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

