import re

import re
count = 0
s = input().split(',')
res = []
for i in s:
    count = 0
    count += bool(6<=len(i)<=12)
    count += bool(re.search('[a-z]',i))
    count += bool(re.search('[0-9]',i))
    count += bool(re.search('[A-Z]',i))
    count += bool(re.search('[$#@]',i))
    if count == 5:
        res.append(i)
print(res)

