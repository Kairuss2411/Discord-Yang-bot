from datetime import datetime
import time

day = datetime.today()

rs = [False, False]

rs[0] = True

if rs[0]:
  print(day.day)
print(day.weekday()==0)
print(day.month)
