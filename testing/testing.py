import json,os.path

PATHS : tuple = ('../database/users_data.json','../database/journal_data.json')
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
        1726056000 : {
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




def main():
    ...
    
    
if __name__ == "__main__":    
    main()
