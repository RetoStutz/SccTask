import pandas as pd

from employee import Employee, Work
from tracker import Tracker


def createList():
    print("create all lists")
    df = pd.read_csv('data/workitemsExport.csv')

    for ind in df.index:
        Scc.trackerlist.append(Tracker(df[Scc.NAME_TRACKER_Title][ind], df[Scc.NAME_TRACKER_ID][ind],
                                       df[Scc.NAME_TRACKER_TYPE][ind]))


def createLinkToParrent():
    print("create link to parrent tracker")
    df = pd.read_csv('data/workitemsExport.csv')

    # iterate all lines in csv file
    for ind in df.index:

        # if tracker in current line has tracker
        if not (pd.isnull(df[Scc.NAME_TRACKER_LINKED][ind])):
            # get tracker list
            tupleTrackerId = getTupleLinkedTrackerId(df[Scc.NAME_TRACKER_LINKED][ind])[0]
            # check if list has parent tracker
            if tupleTrackerId:
                # iterate all tracker in trackerlist
                for parentTrackerId in tupleTrackerId:
                    for tracker in Scc.trackerlist:
                        # if tracker in trackerlist has same number as referenc in csv file
                        if str(tracker.trackerId) == parentTrackerId:
                            # find tracker from csv file in trackerList and ad tracker from above to fromTracker from Tracker
                            # from csv File
                            getTrackerByNumber(df[Scc.NAME_TRACKER_ID][ind]).addParrentTracker(tracker)


def createLinkToChild():
    print("create link to child tracker")
    df = pd.read_csv('data/workitemsExport.csv')

    # iterate all lines in csv file
    for ind in df.index:

        # if tracker in current line has tracker
        if not (pd.isnull(df[Scc.NAME_TRACKER_LINKED][ind])):
            # get tracker list
            tupleTrackerId = getTupleLinkedTrackerId(df[Scc.NAME_TRACKER_LINKED][ind])[1]
            # check if list has parent tracker
            if tupleTrackerId:
                # iterate all tracker in trackerlist
                for childTrackerId in tupleTrackerId:
                    for tracker in Scc.trackerlist:
                        # if tracker in trackerlist has same number as referenc in csv file
                        if str(tracker.trackerId) == childTrackerId:
                            # find tracker from csv file in trackerList and ad tracker from above to fromTracker from Tracker
                            # from csv File
                            getTrackerByNumber(df[Scc.NAME_TRACKER_ID][ind]).addChildTracker(tracker)


def getTrackerByNumber(trackerNumber):
    for e in Scc.trackerlist:
        if e.trackerId == trackerNumber:
            return e

def getTrackerByName(name):
    for e in Scc.trackerlist:
        if e.getName() == name:
            return e

def printTrackerList():
    for tracker in Scc.trackerlist:
        print(tracker.infoVariables())
        print(tracker.infoParrentTrackers())
        print(tracker.infoTChildTrackers())


def printTrackerTree():
    # get list of epics
    print("---------------epics------------------------------")
    epicList = []
    for tracker in Scc.trackerlist:
        if tracker.getTrackerType() == Scc.NAME_EPIC:
            epicList.append(tracker)

    # print all epics, stories and task in epiclist
    for epic in epicList:
        if not epic.isPrinted:
            print("Epic: " + epic.getNumber() + epic.getName())
            epic.isPrinted = True

        if epic.getChildTrackers():
            for enhancementChild in epic.getChildTrackers():
                if enhancementChild.getTrackerType() == Scc.NAME_STORY:
                    if not enhancementChild.isPrinted:
                        print("---Story: " + enhancementChild.getNumber() + enhancementChild.getName())
                        enhancementChild.isPrinted = True
                    if enhancementChild.getChildTrackers():
                        for storyChild in enhancementChild.getChildTrackers():
                            if storyChild.getTrackerType() == Scc.NAME_ENHANCEMENT:
                                print("-----Enh: " + storyChild.getNumber() + storyChild.getName())
                                storyChild.isPrinted = True
                            else:
                                if not storyChild.isPrinted:
                                    print("-----Task: " + storyChild.getNumber() + storyChild.getName())
                                    storyChild.isPrinted = True
                elif enhancementChild.getTrackerType() == Scc.NAME_ENHANCEMENT:
                    if not enhancementChild.isPrinted:
                        print("---Enh: " + enhancementChild.getNumber() + enhancementChild.getName())
                        enhancementChild.isPrinted = True


    #get list of stories
    print("---------------stories without epics------------------------------")
    storiesList = []
    for tracker in Scc.trackerlist:
        if tracker.getTrackerType() == Scc.NAME_STORY:
            storiesList.append(tracker)

    # print all stories and task in storieList
    for enhancementChild in storiesList:
        if not enhancementChild.isPrinted:
            print("---" + enhancementChild.getNumber() + enhancementChild.getName())
            enhancementChild.isPrinted = True
        if enhancementChild.getChildTrackers():
            for storyChild in enhancementChild.getChildTrackers():
                if not storyChild.isPrinted:
                    print("------" + storyChild.getNumber() + storyChild.getName())
                    storyChild.isPrinted = True

    #get list of stories
    print("---------------enhancement without epics or stories------------------------------")
    enhancementList = []
    for tracker in Scc.trackerlist:
        if tracker.getTrackerType() == Scc.NAME_ENHANCEMENT:
            enhancementList.append(tracker)

    # print all stories and task in storieList
    for enhancementChild in enhancementList:
        if not enhancementChild.isPrinted:
            print("Enh:" + enhancementChild.getNumber() + enhancementChild.getName())
            enhancementChild.isPrinted = True




def getTupleLinkedTrackerId(linkString):
    x = str(linkString).split(", ")

    parrent = []
    child = []

    for text in x:
        pair = []

        tupleText = text.split(": ")

        pair.append(tuple(tupleText))

        for p in pair:
            # if p is link to parrent
            if p[0] == Scc.NAME_STORY_TO_EPIC or p[0] == Scc.NAME_TASK_TO_STORY or p[0] == Scc.NAME_TRACKER_TO_PARENT:
                parrent.append(p[1])
            else:
                child.append(p[1])
    return (parrent, child)

def createEmployeeList():
    print("create all employee lists")
    df = pd.read_csv('data/EXPORT.csv')

    for ind in df.index:

        fullName = df[Scc.NAME_NAME_FIRSTNAME][ind]
        if fullName:
            employeeExist = False
            for employee in Scc.employeeList:
                if employee.getFullName() == fullName:
                    employeeExist = True
                    employee.addItem(Work(df[Scc.NAME_DATE][ind], df[Scc.NAME_TIME][ind], df[Scc.NAME_SHORT_TEXT][ind]))
            if not employeeExist:
                newEmployee = Employee(df[Scc.NAME_NAME_FIRSTNAME][ind])
                newEmployee.addItem(Work(df[Scc.NAME_DATE][ind], df[Scc.NAME_TIME][ind], df[Scc.NAME_SHORT_TEXT][ind]))
                Scc.employeeList.append(newEmployee)


def printEmployeeList():
    for employee in Scc.employeeList:
        print("--- " + employee.fullName)
        for work in employee.work:
            print("------ " + str(work.date) + " " + str(work.time) + " " + str(work.shortText))


class Scc:
    NAME_EPIC = "Epic"
    NAME_STORY = "User Story"
    NAME_TASK = "Task"
    NAME_ENHANCEMENT = "Enhancement Request"
    NAME_BUG = "Bug Report"
    NAME_TRACKER_TYPE = "Type"
    NAME_TRACKER_Title = "Title"
    NAME_TRACKER_ID = "ID"
    NAME_TRACKER_LINKED = "Linked Work Items"
    # relations between trackers
    # to parent trackers
    NAME_STORY_TO_EPIC = "specifies"
    NAME_TASK_TO_STORY = "implements"
    NAME_TRACKER_TO_PARENT = "relates to"

    #employee
    NAME_NAME_FIRSTNAME = "Name of employee or applicant"
    NAME_DATE = "Date"
    NAME_TIME = "Number (unit)"
    NAME_SHORT_TEXT = "Short Text"

    # to child trackers
    NAME_EPIC_TO_STORY = "is specified by"
    NAME_STORY_TO_TASK = "is implemented by"
    NAME_TRACKER_TO_CHILD = "is related to"

    trackerlist = []
    employeeList = []

    def __init__(self):
        print("call constructor")

        #createList()
        #createLinkToParrent()
        #createLinkToChild()
        #printTrackerList()
        #printTrackerTree()

        createEmployeeList()
        printEmployeeList()

