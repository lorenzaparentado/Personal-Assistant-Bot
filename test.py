import datetime

now = datetime.datetime.now()
print(now)
target = now.replace(hour= 7, minute= 30, second= 0, microsecond= 0)
print(target)
tester = False
if now > target:
    tester = True
    target += datetime.timedelta(days=1)

print(tester)
delay = (target - now).total_seconds()
print(delay)

