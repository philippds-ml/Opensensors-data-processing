from datetime import datetime, timedelta, timezone
import time
import operator
from dateutil.parser import parse
import numpy as np
import pandas as pd

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


dictionary = dict({'heat': 'heatmap'})

print(dictionary['heat'][1])

test_string = "0,1,54,7,3,5,4"
test_list = list(map(int, test_string.split(',')))

dictionary.update({'heat': list(map(int, test_string.split(',')))})

df = pd.DataFrame(data = dictionary)
e = df.shape[0]

print(df.iat[2, 0])



test_rand = np.random.randint(0, 10)
print(test_string[3])


list1 = [0,0,0]
list2 = [1,2,3]

aaa = np.array(list1)

aaa += np.array(list2)

aaa = data.iloc[0,1:2]


