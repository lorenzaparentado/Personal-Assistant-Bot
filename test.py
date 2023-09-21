import datetime

now = datetime.datetime.now()

target = now.replace(hour= 7, minute= 30, second= 0, microsecond= 0)

tester = False
if now > target:
    tester = True
    target += datetime.timedelta(days=1)

delay = (target - now).total_seconds()


