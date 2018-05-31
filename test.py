
from datetime import datetime, timedelta, timezone
import time
import operator
from dateutil.parser import parse

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



dictionary = dict({0:'000000',1:'11111',3:'333333',4:'444444'})

for k in dictionary:
    print(k)


dictionary.keys()

dictionary = sorted(dictionary.items(), key = operator.itemgetter(1), reverse = True)

print(list(dictionary.keys()))


print(to_date.isoweekday())

test_date = parse('2018-02-02 00:00:00').date()
test_date = test_date.date()

con = datetime.strptime(test_date, "%Y-%m-%d")