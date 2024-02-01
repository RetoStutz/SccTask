

class Employee:

    def __init__(self, fullName):
        self.fullName = fullName
        #self.name = str(fullName).split()[0]
        #self.firstName = str(fullName).split()[1]

        self.work = []


    # def getName(self):
    #     return self.name
    #
    # def getFirstName(self):
    #     return self.firstName

    def getFullName(self):
        return self.fullName

    def addItem(self, item):
        self.work.append(item)



class Work:
    def __init__(self, date, time, shortText):
        self.date = date
        self.time = time
        self.shortText = shortText

    def getDate(self):
        return self.date

    def getTime(self):
        return self.time

    def getShortText(self):
        return self.shortText

