import json,pytz
from datetime import datetime,time


class sModes:
    def __init__(self,id,productive,mood,agenda_not_done,
                 agenda_done,thankful,lessons,
                 sucks,created_date) -> None:
        self.id : int = id
        self.productive : int = productive
        self.mood : int = mood 
        self.agenda_not : list = agenda_not_done
        self.agenda_done : list = agenda_done
        self.thankful : list = thankful
        self.lessons : str = lessons
        self.sucks : str = sucks
        self.created : int = created_date
        self.today : int = datetime.combine(datetime.now(pytz.timezone('Asia/Calcutta')),time.min).timestamp()
                
    def test(self) -> None:
        print("\n----------------------------------------")
        print("sMode class called")
        print(f"time : {datetime.today().time()}")
        print("----------------------------------------")
        
    def test2() -> None:
        print("\nsMode class's test2 called")

    def check_last() -> None:
        ...
        
    def update_to_local(self,path : str) -> None:
        path : str = path
        j_data : dict = {
        'productive' :  self.productive,
        'mood' : self.mood, 
        'agenda_not_done' : self.agenda_not,
        'agenda_done' : self.agenda_done,
        'thankful' :  self.thankful,
        'lessons' : self.lessons,
        'sucks' : self.sucks,
        'created_date' : self.created
        }

        try: 
            with open(path) as fp:
                journal_stored_data = json.load(fp)
                # print('journal_stored_data: ',journal_stored_data)
                print('journal_stored_data date: ',journal_stored_data[-1]['created_date'])
                print('j_data date: ',j_data['created_date'])
                if journal_stored_data:
                    if journal_stored_data[-1]['created_date'] != j_data['created_date']:
                        journal_stored_data.append(j_data)
                        ...
                    elif journal_stored_data[-1]['created_date'] != j_data['created_date']:
                        journal_stored_data.append(j_data)
                
                
        except Exception as e:
            print(f'\nError : {e}')
                        # journal_page = {
                        #     'productivity' : 0,
                        #     'mood' : 0,
                        #     'agenda_not_done' : [],
                        #     'agenda_done' : [],
                        #     'thankful' : [],
                        #     'lessons' : "",
                        #     'sucks' : 'sleep early/ wake up at 5am',
                        #     'created_date' : today
                        # }

 
    
    def update_to_database(self) -> None:
        ...