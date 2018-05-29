
from datetime import datetime, timedelta


from_date = datetime.strptime('2018-02-02', "%Y-%m-%d")
to_date = datetime.strptime('2018-02-04', "%Y-%m-%d")

from_date = from_date + timedelta(days=10)


print(from_date)


dif_date = to_date - from_date

