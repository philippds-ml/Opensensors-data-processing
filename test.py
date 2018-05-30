
from datetime import datetime, timedelta, timezone
import time

from_date = datetime.strptime('2018-02-02', "%Y-%m-%d")
to_date = datetime.strptime('2018-03-14', "%Y-%m-%d")

to_date = to_date + timedelta(days=20)


print(from_date)


dif_date = to_date - from_date





epoch = 1522710000
to_human = datetime.fromtimestamp(epoch)
to_human = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)



epoch = int(time.mktime(to_date.timetuple()))


to_date = to_date + timedelta(hours = 1)


x = 1
y = 4

if x == y:
    print("equal")

