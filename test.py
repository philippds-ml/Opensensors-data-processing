
from datetime import datetime, timedelta
import time

from_date = datetime.strptime('2018-02-02', "%Y-%m-%d")
to_date = datetime.strptime('2018-03-14', "%Y-%m-%d")

to_date = to_date + timedelta(days=20)


print(from_date)


dif_date = to_date - from_date




epoch = int(time.mktime(to_date.timetuple()))


to_date = to_date + timedelta(hours = 1)