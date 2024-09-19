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
            
        

    check_file_exists()
    # data : dict = retrive_data(PATHS[0])
    # print("\ndata:",data)
    # data['123'].update({'email':'1234@gmail.com'})
    # print("\nnew_data:",data)
    # update_data(PATHS[0],data)
    
    
if __name__ == "__main__":    
    main()
