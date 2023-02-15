
class Tracker:

    def __init__(self, trackerTitle, trackerId, trackerType):
        self.trackerTitle = trackerTitle
        self.trackerId = trackerId
        self.trackerType = trackerType
        self.isPrinted = False

        self.parrentTrackers = []
        self.childTrackers = []

    def getName(self):
        return self.trackerTitle

    def getNumber(self):
        return self.trackerId

    def getTrackerType(self):
        return self.trackerType

    def getParentTrackerFromNumber(self, trackerNumber):
        return self.parrentTrackers.index(trackerNumber)

    def getChildTrackerFromNumber(self, trackerNumber):
        return self.childTrackers.index(trackerNumber)

    def getParrentTrackers(self):
        return self.parrentTrackers

    def getChildTrackers(self):
        return self.childTrackers

    def addParrentTracker(self, fromTracker):
        self.parrentTrackers.append(fromTracker)

    def addChildTracker(self, toTracker):
        self.childTrackers.append(toTracker)

    def infoVariables(self):
        return str(self.trackerTitle) + ", " + str(self.trackerId) + ", " + str(self.trackerType)

    def infoParrentTrackers(self):
        info = "start info parrentTracker:"
        for tracker in self.parrentTrackers:
            info += tracker.infoVariables()

        info += "end info parrentTracker:"
        return info

    def infoTChildTrackers(self):
        info = "start info childTracker:"
        for tracker in self.childTrackers:
            info += tracker.infoVariables()

        info += "end info childTracker:"
        return info
