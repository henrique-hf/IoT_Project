import json

from RegisterPackage import RegisterPackage

def testRead():
    test = RegisterPackage()
    test.POST()

    read = test.read()
    check = test.checkData()

    return read, check

#print testRead()
#a = testRead()
test = RegisterPackage()
a = test.GET()
b = json.loads(a)
print a
print b
print b[0]['id']

