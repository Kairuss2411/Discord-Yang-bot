import schedule
import time
import json
import threading
import datetime
import pytz

#Define local time
local_tz = pytz.timezone('Asia/Ho_Chi_Minh')
def utc_to_local(utc_dt):
  local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
  return local_tz.normalize(local_dt)
  
def run_continuously(interval=1):
  cease_continuous_run = threading.Event()

  class ScheduleThread(threading.Thread):
      @classmethod
      def run(cls):
          while not cease_continuous_run.is_set():
              schedule.run_pending()
              time.sleep(interval)

  continuous_thread = ScheduleThread()
  continuous_thread.start()
  return cease_continuous_run

def daily_reset():
  print("Daily Reset")
  try:
    with open('users.json', 'r') as f:
        file = json.load(f)
        users_list = file['users_list']
        f.close()
        rs_func = [False, False]
        today = datetime.today()
        if(today.weekday() == 6): 
          rs_func[0] = True
        if(today.day == 1):
          rs_func[1] = True
        if users_list:
          for user in users_list:
            user['day_learning'] = 0
            print('=============Day reset!=============')
            if(rs_func[0]):
              user['week_learning'] = 0
              print('=============Week reset!=============')
            if(rs_func[1]):
              print('=============Month reset!=============')
              user['month_learning'] = 0
            # backup
            with open('users_backup.json','w') as b:
              b.seek(0)
              json.dump(f, b, indent=4)
              b.close()
          with open('users.json',
                    'w') as f:
            #Save to json file
            f.seek(0)
            json.dump(file, f, indent=4)
            f.close()
  except Exception as e:
      print(f"Error at: {e}")

def backup():
  try:
    with open('users.json', 'r') as f:
      file = json.load(f)
      users_list = file['users_list']
      f.close()
      if users_list:
        with open('users_backup.json','w') as f:
          f.seek(0)
          json.dump(file, f, indent=4)
          f.close()
  except Exception as e:
      print(f"Error at: {e}")
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()
#=====Set Time for scheduler=======
# schedule.every(60).seconds.do(daily_reset)
schedule.every().day.at("17:01").do(run_threaded, daily_reset)

def Data_Reset_Schedule():
  print("Start Scheduler")
  stop_run_continuously = run_continuously()