import pymongo

connection = pymongo.Connection('127.0.0.1', 27017)
db = connection.test
print db.test.update({'z': 'x'}, {'c': 'd'}, True, False, True)