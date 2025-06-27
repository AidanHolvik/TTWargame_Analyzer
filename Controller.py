from Model import Unit, Model, Database

"""
The controller is responsible for:
    - Receiving user input and interpreting it
    - Updating the Model based on user actions (using CRUD operations)
    - Selecting and displaying the appropriate View
"""

db = Database('test')

# temp = Unit('testName_1')
# temp = Unit('testName_2', 10)
# db.createUnit(temp)

# temp = db.readUnit('testName_1')
# print(temp.asTuple())
# temp = db.readUnit('testName_2')
# print(temp.asTuple())

# temp.name = 'testName_2b'
# temp.cost = 67
# print(db.updateUnit('testName_2b', temp))

temp = db.listUnits()
for i in temp:
    print(i)
print('')

# db.deleteUnit('testName_2b')

temp = db.listUnits()
for i in temp:
    print(i)
print('')




