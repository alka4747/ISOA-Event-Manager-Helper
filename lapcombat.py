import xml.etree.ElementTree as ET
import datetime as dt
import csv
import statistics
import copy

# # File version: 0.5
# # 18.10.21

# # Insert the IOF V.3.0 result file path here.
# # resultFile = '/public/Nivut_CD/Lapcombat/XML_Results/ben_shemen_east_21_result_list_Family_First.xml'
# # resultFile = '/public/Nivut_CD/Lapcombat/shoham_2018_result_list_Family_First.xml'
# # resultFile = '/public/Nivut_CD/Lapcombat/Shoham_2021_results-IOFv3.xml'
# # resultFile = '/public/Nivut_CD/Lapcombat/Holon_2021_results-IOFv3.xml'
# # resultFile = '/public/Nivut_CD/Lapcombat/XML_Results/Shimshit_SI_Droid_results-IOFv3.xml'
# # resultFile = '/public/Nivut_CD/Lapcombat/XML_Results/Kfar_Hahoresh_SI_Droid_results-IOFv3.xml'
# # resultFile = '/public/Nivut_CD/Lapcombat/XML_Results/Nazareth_SI_Droid_results-IOFv3_Original.xml'
# # resultFile = '/public/Nivut_CD/Lapcombat/Ramat_Hanadiv_2021_results-IOFv3.xml'
# # resultFile = '/public/Nivut_CD/Lapcombat/Hasolelim_2022_results-IOFv3.xml'
# # resultFile = '/public/Nivut_CD/Lapcombat/Elyaqim_2022_results-IOFv3.xml'
# resultFile = '/public/Nivut_CD/Lapcombat/Kfar_Saba_Hayeruka_2022_results-IOFv3.xml'
# # resultFile = '/public/Nivut_CD/Hasharon_Website/Github/hasharonoc.github.io/events/Caesaria_2022/caesaria_22_result_list.xml'
# # resultFile = '/public/Nivut_CD/Hasharon_Website/Github/hasharonoc.github.io/events/Ben_Shemen_2022/ben_shemen_22_result_list.xml'
# xmlns = '{http://www.orienteering.org/datastandard/3.0}'  # Required for identifying xml tags in the results file.
# mulkaDatetimeStrptimeString = "%Y-%m-%dT%H:%M:%S%z"
# SIDroidDatetimeStrptimeString = "%Y-%m-%dT%H:%M:%S.%f%z"
# SIDroidTimeStampsDatetimeStrptimeString = "%Y-%m-%dT%H:%M:%S"
# classes = []

# tree = ET.parse(resultFile)
# root = tree.getroot()
# app = root.attrib.get('creator')  # Find the application that created the results file.
# fileCreationTime = root.get('createTime')  # Get the file creation time. This will serve as a base for time events
# defaultStartTime = dt.datetime(2021, 1, 1)
# luckyControlThresholdSeconds = 10  # This is the time threshold for calculating whether the runner saw someone punching
# # the control, thus revealing its location.
# numberOfControlsForGroupOrienteeringThreshold = 5  # This is the number of consecutive joint punches threshold for
# # considering two runners as tracking each other.
# mulka = False
# if app[0:5] == 'Mulka':
#     mulka = True  # Check if the results came from Mulka or not
# if mulka:
#     datetimeStrptimeString = mulkaDatetimeStrptimeString
#     fct = dt.datetime.strptime(fileCreationTime, datetimeStrptimeString)  # Convert to datetime object
#     # Make a copy of the file creation time in order to establish an arbitrary event start time
#     baseEventStart = dt.datetime(fct.year, fct.month, fct.day, hour=6, minute=0, second=0)
# else:
#     datetimeStrptimeString = SIDroidDatetimeStrptimeString
#     fct = dt.datetime.strptime(fileCreationTime, datetimeStrptimeString)  # Convert to datetime object
#     # Make a copy of the file creation time in order to establish an arbitrary event start time
#     baseEventStart = dt.datetime(fct.year, fct.month, fct.day, hour=6, minute=0, second=0)


class Competitor:
    firstName = ""
    lastName = ""
    club = ""
    country = ""
    ID = 0
    SINumber = 0
    place = 999
    place_Text = ''
    startTime = "09:00:00"
    startTimeAsDateTime = dt.datetime(2021, 1, 1)
    startTimeOffsetFromEventStartSeconds = -1
    finishTime = "10:00:00"
    finishTimeAsDateTime = dt.datetime(2021, 1, 2)
    controlList = []
    cumulativeLegTimesSeconds = []
    cumulativeLegTimes_Text = []
    legSplitsSeconds = []
    legSplits_Text = []
    legTimesTimeOfDay = []
    totalTimeSeconds = 0
    totalTime_Text = ''
    disq = False
    dns = False
    dnf = False
    cruisingSpeeds = []
    cruisingSpeeds_Text = []
    placeInLeg = []
    placeInLeg_Text = []
    interimPlace = []
    interimPlace_Text = []
    numberOfMissingLegs = 0
    missingLegsList = []
    missingLegsWeight = 0.0
    legMistakeTimes = []
    legMistakeTimes_Text = []
    nominalCruisingSpeed = 0.0
    nominalCruisingSpeed_Text = ''
    totalMistakeTime = 0.0
    totalMistakeTime_Text = ''
    mistakeTimeAverage = 0.0
    mistakeTimeStdDeviation = 0.0
    cruisingSpeedMean = 0.0
    cruisingSpeedStdDeviation = 0.0
    stabilityValue = 0.0
    mistakeRatioPercent = 100.0
    mistakeRatioPercent_Text = ''
    idealFinishTimeSeconds = 0
    idealFinishTime_Text = ''
    numberOfLuckyControls = 0
    luckyControlsList = []
    luckyControlsSpeedIndices = []
    # lossDueToAccuracy = 0
    gainOrLossDueToAccuracy = 0
    groupOrienteering = False
    status = 'OK'


class Course:
    def __init__(self, length=0, climb=0):
        self.length = length
        self.climb = climb

    name = ""
    controls = []
    legList = []
    trains = []
    # length = 0
    # climb = 0


class Category:
    def __init__(self, name):
        self.categoryName = name

    # categoryName = ""
    course = Course()
    competitors = []
    controlPunches = [[]]
    legWeights = []
    legStandardTimeSeconds = []
    idealFinishTimeSeconds = 0.0
    biggestGainer = []
    biggestLoser = []
    biggestGainer_Text = ''
    biggestLoser_Text = ''
    theRoadrunner = ''
    theSwissClock = ''
    theRock = ''
    possibleTrains = []
    trains = []
    trainsByControls = []

    def populateControlPunches(self):
        None

    def getCompetitorPunches(self, id):
        return self.controlPunches[id]


class Event:
    def __init__(self, resFile, xml_tree, xml_root, is_mulka, baseEventStart):
        self.resFile = resFile
        self.tree = xml_tree
        self.root = xml_root
        self.mulka = is_mulka
        self.baseEventStart = baseEventStart

    xmlns = '{http://www.orienteering.org/datastandard/3.0}'  # Required for identifying xml tags in the results file.
    mulkaDatetimeStrptimeString = "%Y-%m-%dT%H:%M:%S%z"
    SIDroidDatetimeStrptimeString = "%Y-%m-%dT%H:%M:%S.%f%z"
    SIDroidTimeStampsDatetimeStrptimeString = "%Y-%m-%dT%H:%M:%S"
    eventName = ""
    categoryList = []
    splitsTable = [[]]
    elapsedTimesTable = [[]]
    legSpeedIndexTable = [[]]
    legMistakeTimeTable = [[]]

    def getCategoryNames(self, resFile):
        categories = []
        print(resFile)
        classes = self.root.findall(Event.xmlns + 'ClassResult')
        for x in classes:
            categories.append(x[0][0].text)
        return categories

    def getCategories(self, resFile):

        def category_sort_criterion(e):
            return e.categoryName

        def competitor_sort_criterion(e):
            return e.place

        categories = []
        print(resFile)
        classes = self.root.findall(Event.xmlns + 'ClassResult')  # Collect all categories/classes
        for x in classes:
            if (x[0][0].text != 'עממי') and (x[0][0].text != 'No course'):  # Exclude non-competitive classes
                currentCategory = Category(x[0][0].text)  # Get the category name.
                categories.append(currentCategory)  # Add the category name to the list of category names.
                currentCategory.course = Course(x[1][0].text, x[1][1].text)  # Add the category's course details.
                currentCategory.course.controls = []  # Initialize various arrays.
                currentCategory.course.legList = []
                currentCategory.course.trains = []
                currentCategory.competitors = []
                currentCategory.legWeights = []
                currentCategory.legStandardTimeSeconds = []
                competitors = x.findall(Event.xmlns + 'PersonResult')
                firstCompetitor = True  # The first competitor in the list is used to collect the list of controls
                fakeId = 30000  # This is a fake ID number given for competitors registered on-site without a
                # valid ISOA ID number.
                for p in competitors:
                    person = p.find(Event.xmlns + 'Person')
                    org = p.find(Event.xmlns + 'Organisation')
                    currentCompetitor = Competitor()
                    currentCompetitor.club = org.find(Event.xmlns + 'Name').text
                    country = org.find(Event.xmlns + 'Country')
                    if not country is None:
                        if country.text:
                            currentCompetitor.country = country.text
                        else:
                            currentCompetitor.country = ""
                    else:
                        currentCompetitor.country = ""
                    if ((person.find(Event.xmlns + 'Name')).find(Event.xmlns + 'Family')).text is not None:
                        currentCompetitor.lastName = ((person.find(Event.xmlns + 'Name')).find(Event.xmlns + 'Family')).text
                    else:
                        currentCompetitor.lastName = ""
                    if ((person.find(Event.xmlns + 'Name')).find(Event.xmlns + 'Given')).text is not None:
                        currentCompetitor.firstName = ((person.find(Event.xmlns + 'Name')).find(Event.xmlns + 'Given')).text
                    else:
                        currentCompetitor.firstName = ""
                    currentCompetitor.cumulativeLegTimesSeconds = []  # Initialize the competitor's various arrays.
                    currentCompetitor.cumulativeLegTimes_Text = []
                    currentCompetitor.legSplitsSeconds = []
                    currentCompetitor.legSplits_Text = []
                    currentCompetitor.cruisingSpeeds = []
                    currentCompetitor.cruisingSpeeds_Text = []
                    currentCompetitor.legMistakeTimes = []
                    currentCompetitor.legMistakeTimes_Text = []
                    currentCompetitor.placeInLeg = []
                    currentCompetitor.placeInLeg_Text = []
                    currentCompetitor.interimPlace = []
                    currentCompetitor.interimPlace_Text = []
                    currentCompetitor.luckyControlsList = []
                    currentCompetitor.controlList = []
                    currentCompetitor.luckyControlsSpeedIndices = []
                    currentCompetitor.missingLegsList = []
                    if not self.mulka:  # Retrieve the runner's ID on SI Droid.
                        idField = person.find(Event.xmlns + 'Id')
                        if idField is not None:
                            currentCompetitor.ID = idField.text
                        else:
                            currentCompetitor.ID = str(fakeId)
                            fakeId += 1
                    punches = p.findall(Event.xmlns + 'Result')
                    for res in punches:  # Collect all the control punch details for the runner.
                        if self.mulka:  # Retrieve the runner's ID on Mulka.
                            idField = res.find(Event.xmlns + 'BibNumber')
                            currentCompetitor.ID = idField.text
                        splits = res.findall(Event.xmlns + 'SplitTime')
                        if res[3].text == 'DidNotStart' or res[2].text == 'DidNotStart':
                            currentCompetitor.dns = True
                        if res[2].text == 'Disqualified':
                            currentCompetitor.disq = True
                        if res[2].text == 'DidNotFinish':
                            currentCompetitor.dnf = True
                        siNumberField = res.find(Event.xmlns + 'ControlCard')
                        if not siNumberField is None and not siNumberField.text is None:
                            currentCompetitor.SINumber = siNumberField.text
                        else:
                            currentCompetitor.SINumber = ''
                        if len(splits) > 0:
                            currentCompetitor.legTimes = []
                            st = res.findall(Event.xmlns + 'StartTime')
                            if len(st) > 0:  # and currentCompetitor.legSplitsSeconds[0] > 0:
                                currentCompetitor.startTime = st[0].text
                                # if mulka:
                                #     currentCompetitor.startTimeAsDateTime = dt.datetime.strptime(currentCompetitor.startTime,
                                #                                                           mulkaDatetimeStrptimeString)
                                #     currentCompetitor.startTimeAsDateTime = dt.datetime(
                                #         currentCompetitor.startTimeAsDateTime.year,
                                #         currentCompetitor.startTimeAsDateTime.month,
                                #         currentCompetitor.startTimeAsDateTime.day,
                                #         hour=currentCompetitor.startTimeAsDateTime.hour,
                                #         minute=currentCompetitor.startTimeAsDateTime.minute,
                                #         second=currentCompetitor.startTimeAsDateTime.second)
                                # else:
                                #     currentCompetitor.startTimeAsDateTime = dt.datetime.strptime(currentCompetitor.startTime,
                                #                                                           SIDroidTimeStampsDatetimeStrptimeString)
                                #
                            ft = res.findall(Event.xmlns + 'FinishTime')
                            if len(ft) > 0:
                                currentCompetitor.finishTime = ft[0].text
                                # if mulka:
                                #     currentCompetitor.finishTimeAsDateTime = dt.datetime.strptime(
                                #         currentCompetitor.finishTime, mulkaDatetimeStrptimeString)
                                #     currentCompetitor.finishTimeAsDateTime = dt.datetime(
                                #         currentCompetitor.finishTimeAsDateTime.year,
                                #     currentCompetitor.finishTimeAsDateTime.month,
                                #         currentCompetitor.finishTimeAsDateTime.day,
                                #     hour=currentCompetitor.finishTimeAsDateTime.hour,
                                #         minute=currentCompetitor.finishTimeAsDateTime.minute,
                                #     second=currentCompetitor.finishTimeAsDateTime.second)
                                # else:
                                #     currentCompetitor.finishTimeAsDateTime = dt.datetime.strptime(
                                #         currentCompetitor.finishTime, SIDroidTimeStampsDatetimeStrptimeString)
                                # currentCompetitor.startTimeOffsetFromEventStartSeconds = \
                                #     round((currentCompetitor.startTimeAsDateTime - baseEventStart).seconds)
                            time = res.findall(Event.xmlns + 'Time')
                            if len(time) > 0:
                                currentCompetitor.totalTimeSeconds = time[0].text
                            else:
                                currentCompetitor.dnf = True
                            # currentCompetitor.finishTime = res[2].text
                            # currentCompetitor.totalTimeSeconds = res[3].text
                            status = res.findall(Event.xmlns + 'Status')
                            if status[0].text == 'MissingPunch':
                                currentCompetitor.disq = True
                            for sp in splits:
                                if firstCompetitor and not (currentCompetitor.dns):
                                    currentCategory.course.controls.append(sp[0].text)
                                if not currentCompetitor.dns:
                                    if sp.attrib.get('status') != 'Missing' and sp.attrib.get('status') != 'Additional':
                                        splitTime = sp.find(Event.xmlns + 'Time')
                                        controlCode = sp.find(Event.xmlns + 'ControlCode')
                                        # currentCompetitor.cumulativeLegTimesSeconds.append(int(sp[1].text))
                                        currentCompetitor.cumulativeLegTimesSeconds.append(int(splitTime.text))
                                        currentCompetitor.controlList.append(controlCode.text)
                                    else:
                                        currentCompetitor.cumulativeLegTimesSeconds.append(-1)
                            if firstCompetitor and not currentCompetitor.dns:
                                currentCategory.course.controls.append('F')
                            if not currentCompetitor.dns and not currentCompetitor.dnf:
                                currentCompetitor.cumulativeLegTimesSeconds.append(
                                    int(currentCompetitor.totalTimeSeconds))
                            elif currentCompetitor.dnf:
                                currentCompetitor.cumulativeLegTimesSeconds.append(-1)
                            if len(currentCategory.course.controls) > 0:
                                firstCompetitor = False
                        if not currentCompetitor.dns and len(currentCompetitor.cumulativeLegTimesSeconds) > 0 and \
                                not currentCompetitor.startTime is None:
                            if self.mulka:
                                currentCompetitor.startTimeAsDateTime = dt.datetime.strptime(
                                    currentCompetitor.startTime,
                                    Event.mulkaDatetimeStrptimeString)
                                currentCompetitor.startTimeAsDateTime = dt.datetime(
                                    currentCompetitor.startTimeAsDateTime.year,
                                    currentCompetitor.startTimeAsDateTime.month,
                                    currentCompetitor.startTimeAsDateTime.day,
                                    hour=currentCompetitor.startTimeAsDateTime.hour,
                                    minute=currentCompetitor.startTimeAsDateTime.minute,
                                    second=currentCompetitor.startTimeAsDateTime.second)
                            else:
                                currentCompetitor.startTimeAsDateTime = dt.datetime.strptime(
                                    currentCompetitor.startTime,
                                    Event.SIDroidTimeStampsDatetimeStrptimeString)
                        if not currentCompetitor.dns and len(currentCompetitor.cumulativeLegTimesSeconds) > 0 and \
                                not currentCompetitor.finishTime is None and not currentCompetitor.dnf:
                            if self.mulka:
                                currentCompetitor.finishTimeAsDateTime = dt.datetime.strptime(
                                    currentCompetitor.finishTime, Event.mulkaDatetimeStrptimeString)
                                currentCompetitor.finishTimeAsDateTime = dt.datetime(
                                    currentCompetitor.finishTimeAsDateTime.year,
                                    currentCompetitor.finishTimeAsDateTime.month,
                                    currentCompetitor.finishTimeAsDateTime.day,
                                    hour=currentCompetitor.finishTimeAsDateTime.hour,
                                    minute=currentCompetitor.finishTimeAsDateTime.minute,
                                    second=currentCompetitor.finishTimeAsDateTime.second)
                            else:
                                currentCompetitor.finishTimeAsDateTime = dt.datetime.strptime(
                                    currentCompetitor.finishTime, Event.SIDroidTimeStampsDatetimeStrptimeString)
                            currentCompetitor.startTimeOffsetFromEventStartSeconds = \
                                round((currentCompetitor.startTimeAsDateTime - self.baseEventStart).seconds)
                            CC = res.findall(Event.xmlns + 'ControlCard')
                        currentCompetitor.SINumber = CC[0].text
                        pos = res.findall(Event.xmlns + 'Position')
                        if len(pos) > 0:
                            currentCompetitor.place = int(pos[0].text)
                    lastSplitSeconds = 0
                    controlSequentialNumber = 0
                    lastLegMissing = False
                    for cont in currentCategory.course.controls:
                        if not currentCompetitor.dns and len(currentCompetitor.cumulativeLegTimesSeconds) > 0:
                            if currentCompetitor.cumulativeLegTimesSeconds[controlSequentialNumber] > 0:
                                if not lastLegMissing:
                                    currentCompetitor.legSplitsSeconds.append(
                                        currentCompetitor.cumulativeLegTimesSeconds[controlSequentialNumber] -
                                        lastSplitSeconds)
                                    lastSplitSeconds = currentCompetitor.cumulativeLegTimesSeconds[
                                        controlSequentialNumber]
                                if lastLegMissing:
                                    lastLegMissing = False
                                    currentCompetitor.legSplitsSeconds.append(-1)
                                    lastSplitSeconds = currentCompetitor.cumulativeLegTimesSeconds[
                                        controlSequentialNumber]
                            else:
                                currentCompetitor.legSplitsSeconds.append(-1)
                                lastLegMissing = True
                            controlSequentialNumber += 1
                    if not currentCompetitor.dns and len(currentCompetitor.legSplitsSeconds) > 0:
                        currentCategory.competitors.append(currentCompetitor)
                currentCategory.competitors.sort(key=competitor_sort_criterion)
                # Calculate place in leg for each runner by collecting all valid split times for each leg, indexing them
                # by the competitor's place in the category array, sorting the indices according to the split times and
                # then updating the competitor's own array of place in leg with the index of his split time (or -1, if
                # there was no split time for that leg).
                indices = []
                splits = []
                sortedSplits = []
                indices.clear()
                indices = list(range(len(currentCategory.competitors)))
                for leg in range(len(currentCategory.course.controls)):
                    splits.clear()
                    sortedSplits.clear()
                    for comp in currentCategory.competitors:
                        if not comp.dns and len(comp.legSplitsSeconds) > 0:
                            if int(comp.legSplitsSeconds[leg]) > 0:
                                splits.append(int(comp.legSplitsSeconds[leg]))
                            else:
                                splits.append(10000)
                        else:
                            splits.append(10000)
                    indices.sort(key=splits.__getitem__)
                    for i in splits:
                        sortedSplits.append(i)
                    sortedSplits.sort()
                    for comp in range(len(currentCategory.competitors)):
                        if splits[comp] < 10000:
                            currentCategory.competitors[comp].placeInLeg.append(indices.index(comp) + 1)
                        else:
                            currentCategory.competitors[comp].placeInLeg.append(-1)
                    # Adjust place in leg for tie splits by scanning each leg splits, marking tie splits and choosing the better
                    # place for all tied runners.
                    for i in range(len(sortedSplits) - 1):
                        if sortedSplits[i] == sortedSplits[i + 1]:
                            currentCategory.competitors[indices[i + 1]].placeInLeg[leg] = \
                                currentCategory.competitors[indices[i]].placeInLeg[leg]
                # Calculate overall place in each leg for each runner by collecting all valid times for each leg, indexing
                # them by the competitor's place in the category array, sorting the indices according to the times and
                # then updating the competitor's own array of place in leg with the index of his split time (or -1, if
                # there was no time for that leg, or the runner was disqualified).
                indices = []
                times = []
                sortedTimes = []
                indices.clear()
                indices = list(range(len(currentCategory.competitors)))
                for leg in range(len(currentCategory.course.controls)):
                    times.clear()
                    sortedTimes.clear()
                    for comp in currentCategory.competitors:
                        # Add fake timestamp for last leg of disqualified runners so they are not included in final standings
                        if leg == int(len(currentCategory.course.controls) - 1):
                            if comp.disq or comp.dnf:
                                times.append(10000)
                            else:
                                if not comp.dns and len(comp.legSplitsSeconds) > 0:
                                    if int(comp.cumulativeLegTimesSeconds[leg]) > 0:
                                        times.append(int(comp.cumulativeLegTimesSeconds[leg]))
                                    else:
                                        times.append(10000)
                                else:
                                    times.append(10000)

                        else:
                            if not comp.dns and len(comp.legSplitsSeconds) > 0:
                                if int(comp.cumulativeLegTimesSeconds[leg]) > 0:
                                    times.append(int(comp.cumulativeLegTimesSeconds[leg]))
                                else:
                                    times.append(10000)
                            else:
                                times.append(10000)
                    indices.sort(key=times.__getitem__)
                    for i in times:
                        sortedTimes.append(i)
                    sortedTimes.sort()
                    for comp in range(len(currentCategory.competitors)):
                        if times[comp] < 10000:
                            currentCategory.competitors[comp].interimPlace.append(indices.index(comp) + 1)
                        else:
                            currentCategory.competitors[comp].interimPlace.append(-1)
                    # Adjust place in leg for tie times by scanning each leg time, marking tie times and choosing the better
                    # place for all tied runners.
                    for i in range(len(sortedTimes) - 1):
                        if sortedTimes[i] == sortedTimes[i + 1]:
                            currentCategory.competitors[indices[i + 1]].interimPlace[leg] = \
                                currentCategory.competitors[indices[i]].interimPlace[leg]
                # Fill the legs' text description for the web page (i.e. "S -> 1 \n 31")
                currentCategory.course.legList.clear()
                firstLeg = 0
                lastLeg = len(currentCategory.course.controls) - 1
                numberOfLegs = len(currentCategory.course.controls)
                for leg in range(numberOfLegs):
                    if leg == firstLeg:
                        currentCategory.course.legList.append('S -> ' + str(leg + 1) + '\n' + '(' +
                                                              currentCategory.course.controls[leg] + ')')
                    elif leg == lastLeg:
                        currentCategory.course.legList.append(str(leg) + ' -> F' + '\n' + '(F)')
                    else:
                        currentCategory.course.legList.append(str(leg) + ' -> ' + str(leg + 1) + '\n' + '(' +
                                                              currentCategory.course.controls[leg] + ')')
        categories.sort(key=category_sort_criterion)
        return categories

    def getEventName(self):
        return self.root[0][0].text

    def getCompetitors(self):
        competitors = []
        classes = self.root.findall(Event.xmlns + 'ClassResult')
        for x in classes:
            competitors.append(x[2][0][1][0].text)
        return competitors

    # Event.eventName = getEventName(self)


def calculateLapCombat(ev):
    categoryIndex = 0
    for cat in ev.categoryList:
        controlSequentialNumber = 0
        cat.legStandardTimeSeconds = []
        ev.categoryList[categoryIndex].legStandardTimeSeconds = []
        # For each leg, collect the splits from all competitors
        for leg in cat.course.controls:
            validSplitsCounter = 0
            validSplits = []
            runningTotal = 0
            for comp in cat.competitors:
                if len(comp.legSplitsSeconds) > 0:
                    if comp.legSplitsSeconds[controlSequentialNumber] > 0:
                        validSplits.append(comp.legSplitsSeconds[controlSequentialNumber])
                        validSplitsCounter += 1
            # Sort the splits in order to get the three fastest ones (or less if there are less than three).
            validSplits.sort()
            # Calculate the average of the three (or less) fastest times. This is the "standard" for the leg.
            if len(validSplits) > 0:  # Make sure that there are splits for the leg (maybe a control is missing)
                counter = 0
                sumOfSplits = 0
                for i in range(len(validSplits)):
                    sumOfSplits += validSplits[counter]
                    if counter == 2: break
                    counter += 1
                cat.legStandardTimeSeconds.append(round(sumOfSplits / (counter + 1), 2))
                ev.categoryList[categoryIndex].legStandardTimeSeconds.append(round(sumOfSplits / (counter + 1), 2))
            controlSequentialNumber += 1
        # Calculate the "gold standard" finishing time for the course (category).
        ev.categoryList[categoryIndex].idealFinishTimeSeconds = \
            round(sum(ev.categoryList[categoryIndex].legStandardTimeSeconds), 2)
        # Calculate the weight of each leg and store it in the course.
        legWeigths = [x / ev.categoryList[categoryIndex].idealFinishTimeSeconds for x
                      in ev.categoryList[categoryIndex].legStandardTimeSeconds]
        zz = ev.categoryList[categoryIndex].legWeights
        for item in legWeigths:
            zz.append(item)
            # ev.categoryList[categoryIndex].legWeights.append(item)
        # print('Category leg weights sum: ' + str(round(sum(ev.categoryList[categoryIndex].legWeights), 2)))
        # For each competitor in the category, calculate the speed index for each leg.
        cruisingSpeeds = []
        indices = []
        for comp in ev.categoryList[categoryIndex].competitors:
            cruisingSpeeds.clear()
            indices.clear()
            indices = list(range(len(comp.legSplitsSeconds)))
            if not comp.dns and len(comp.legSplitsSeconds) > 0:
                controls = ev.categoryList[categoryIndex].course.controls
                splits = comp.legSplitsSeconds
                for leg in range(len(controls)):
                    cruisingSpeeds.append(splits[leg] / ev.categoryList[categoryIndex].
                                          legStandardTimeSeconds[leg])
                cs = comp.cruisingSpeeds
                for item in cruisingSpeeds:
                    cs.append(item)
            # Sort the cruising speeds in an ascending order while keeping track of the leg indices.
            copyOfCruisingSpeeds = []
            for i in range(len(comp.cruisingSpeeds)):
                if comp.cruisingSpeeds[i] < 0:
                    copyOfCruisingSpeeds.append(10000)
                else:
                    copyOfCruisingSpeeds.append(comp.cruisingSpeeds[i])
            indices.sort(key=copyOfCruisingSpeeds.__getitem__)
            # Add the best legs' time until the sum of the leg weights is more than 0.5 - This is the better half...
            accumulatedLegWeights = 0.0
            timeAccumulator = 0.0
            numberOfLegsConsideredForCruisingSpeedCalculation = 0
            if not comp.dns and len(comp.legSplitsSeconds) > 0:
                while accumulatedLegWeights < 0.5:
                    print(numberOfLegsConsideredForCruisingSpeedCalculation)
                    print(indices)
                    print(comp.firstName + " " + comp.lastName)
                    accumulatedLegWeights += ev.categoryList[categoryIndex].legWeights[indices \
                        [numberOfLegsConsideredForCruisingSpeedCalculation]]
                    timeAccumulator += comp.legSplitsSeconds[indices[numberOfLegsConsideredForCruisingSpeedCalculation]]
                    numberOfLegsConsideredForCruisingSpeedCalculation += 1
                # Calculate the nominal cruising speed by dividing the normalized time of the better half by the ideal
                # finish time. If the runner failed to complete enough of the course legs, no result is possible (-1)
                comp.nominalCruisingSpeed = timeAccumulator / accumulatedLegWeights \
                                            / ev.categoryList[categoryIndex].idealFinishTimeSeconds
                if comp.legSplitsSeconds[indices[numberOfLegsConsideredForCruisingSpeedCalculation - 1]] < 0:
                    comp.nominalCruisingSpeed = -1.0
            else:
                comp.nominalCruisingSpeed = -1.0
            # Calculate leg mistake times for the runner by multiplying each leg ideal time with the nominal cruising
            # speed index and subtracting it from the runner's leg time.
            comp.numberOfMissingLegs = 0
            comp.missingLegsWeight = 0.0
            comp.missingLegsList.clear()
            if not comp.dns and not comp.dnf and not comp.disq:
                for leg in range(len(comp.legSplitsSeconds)):
                    if comp.legSplitsSeconds[leg] > 0:
                        comp.legMistakeTimes.append(comp.legSplitsSeconds[leg] - comp.nominalCruisingSpeed *
                                                    ev.categoryList[categoryIndex].legStandardTimeSeconds[leg])
                    else:
                        comp.legMistakeTimes.append(-10000)
                        comp.numberOfMissingLegs += 1
                        comp.missingLegsList.append(leg)
                        comp.missingLegsWeight += ev.categoryList[categoryIndex].legWeights[leg]

                # Calculate the total time due to mistakes by summing only the positive values from the leg mistake time
                # list.
                totalMistakeTime = 0.0
                for leg in range(len(comp.legSplitsSeconds)):
                    if comp.legMistakeTimes[leg] > 0.0:
                        totalMistakeTime += comp.legMistakeTimes[leg]
                comp.totalMistakeTime = totalMistakeTime
                # Calculate the mistake free time for the runner by subtracting the total mistake time from the result.
                comp.idealFinishTimeSeconds = int(comp.totalTimeSeconds) - round(totalMistakeTime)
                # Calculate the mistake ratio: 100 * total mistake time divided by result.
                comp.mistakeRatioPercent = round(100 * totalMistakeTime / ((1.0 - comp.missingLegsWeight) *
                                                                           int(comp.totalTimeSeconds)), 2)
            #     comp.mistakeRatioPercent = round(100 * totalMistakeTime / int(comp.totalTimeSeconds), 2)
            else:
                comp.totalMistakeTime = -1.0
                comp.mistakeRatioPercent = -1.0
                comp.idealFinishTimeSeconds = -1.0
            legalLegsSpeeds = []
            legalLegsSpeeds.clear()
            for item in comp.cruisingSpeeds:
                if item > 0 and item < 10000:
                    legalLegsSpeeds.append(item)
            if len(legalLegsSpeeds) > 1:
                comp.cruisingSpeedMean = statistics.mean(legalLegsSpeeds)
                comp.cruisingSpeedStdDeviation = statistics.stdev(legalLegsSpeeds)
                comp.stabilityValue = comp.cruisingSpeedStdDeviation / comp.cruisingSpeedMean
            else:
                comp.cruisingSpeedMean = 10000.0
                comp.cruisingSpeedStdDeviation = 10000.0
                comp.stabilityValue = 100.0
        # For each competitor calculate the nominal cruising speed
        categoryIndex += 1


def formatLapCombatItems(ev):
    for cat in ev.categoryList:
        for currentCompetitor in cat.competitors:
            currentCompetitor.cumulativeLegTimes_Text.clear()
            for t in currentCompetitor.cumulativeLegTimesSeconds:
                if t > 0:
                    currentCompetitor.cumulativeLegTimes_Text.append(str(dt.timedelta(seconds=t)))
                else:
                    currentCompetitor.cumulativeLegTimes_Text.append('X')
            currentCompetitor.interimPlace_Text.clear()
            for ip in currentCompetitor.interimPlace:
                if ip > 0:
                    currentCompetitor.interimPlace_Text.append(str(ip))
                else:
                    currentCompetitor.interimPlace_Text.append('X')
            currentCompetitor.legSplits_Text.clear()
            for ls in currentCompetitor.legSplitsSeconds:
                if ls > 0:
                    currentCompetitor.legSplits_Text.append(str(dt.timedelta(seconds=ls)))
                else:
                    currentCompetitor.legSplits_Text.append('X')
            currentCompetitor.placeInLeg_Text.clear()
            for pil in currentCompetitor.placeInLeg:
                if pil > 0:
                    currentCompetitor.placeInLeg_Text.append(str(pil))
                else:
                    currentCompetitor.placeInLeg_Text.append('X')
            if not currentCompetitor.dns:
                if not currentCompetitor.dnf and not currentCompetitor.disq:
                    currentCompetitor.totalTime_Text = str(dt.timedelta(seconds=
                                                                        int(currentCompetitor.totalTimeSeconds)))
                elif currentCompetitor.dnf:
                    currentCompetitor.totalTime_Text = 'DNF'
                elif currentCompetitor.disq:
                    currentCompetitor.totalTime_Text = 'DISQ'
            if not currentCompetitor.dns:
                if not currentCompetitor.dnf and not currentCompetitor.disq:
                    currentCompetitor.idealFinishTime_Text = str(dt.timedelta(seconds=
                                                                              int(currentCompetitor.idealFinishTimeSeconds)))
                elif currentCompetitor.dnf:
                    currentCompetitor.idealFinishTime_Text = 'DNF'
                elif currentCompetitor.disq:
                    currentCompetitor.idealFinishTime_Text = 'DISQ'
            if not currentCompetitor.dns:
                if not currentCompetitor.dnf and not currentCompetitor.disq:
                    currentCompetitor.totalMistakeTime_Text = str(dt.timedelta(seconds=
                    int(round(
                        currentCompetitor.totalMistakeTime))))
                elif currentCompetitor.dnf:
                    currentCompetitor.totalMistakeTime_Text = 'DNF'
                elif currentCompetitor.disq:
                    currentCompetitor.totalMistakeTime_Text = 'DISQ'
            if not currentCompetitor.dns:
                if not currentCompetitor.dnf and not currentCompetitor.disq:
                    currentCompetitor.place_Text = str(currentCompetitor.place)
                elif currentCompetitor.dnf:
                    currentCompetitor.place_Text = 'DNF'
                elif currentCompetitor.disq:
                    currentCompetitor.place_Text = 'DISQ'
            if not currentCompetitor.dns:
                if not currentCompetitor.dnf and not currentCompetitor.disq:
                    currentCompetitor.nominalCruisingSpeed_Text = str(round(100 *
                                                                            currentCompetitor.nominalCruisingSpeed, 1))
                elif currentCompetitor.dnf:
                    currentCompetitor.place_Text = 'DNF'
                elif currentCompetitor.disq:
                    currentCompetitor.place_Text = 'DISQ'
            if not currentCompetitor.dns:
                if not currentCompetitor.dnf and not currentCompetitor.disq:
                    currentCompetitor.status = 'OK'
                elif currentCompetitor.dnf:
                    currentCompetitor.status = 'DNF'
                elif currentCompetitor.disq:
                    currentCompetitor.status = 'DISQ'
            if not currentCompetitor.dns:
                if not currentCompetitor.dnf and not currentCompetitor.disq:
                    currentCompetitor.mistakeRatioPercent_Text = str(currentCompetitor.mistakeRatioPercent)
                elif currentCompetitor.dnf:
                    currentCompetitor.mistakeRatioPercent_Text = 'DNF'
                elif currentCompetitor.disq:
                    currentCompetitor.mistakeRatioPercent_Text = 'DISQ'
            currentCompetitor.cruisingSpeeds_Text.clear
            for cs in currentCompetitor.cruisingSpeeds:
                if cs > 0:
                    currentCompetitor.cruisingSpeeds_Text.append(str(round(cs * 100.0, 1)))
                else:
                    currentCompetitor.cruisingSpeeds_Text.append('X')
            currentCompetitor.legMistakeTimes_Text.clear
            for lmt in currentCompetitor.legMistakeTimes:
                if currentCompetitor.legSplitsSeconds[currentCompetitor.legMistakeTimes.index(lmt)] > 0:
                    if lmt > 0:
                        currentCompetitor.legMistakeTimes_Text.append(str(dt.timedelta(seconds=round(lmt))))
                    else:
                        currentCompetitor.legMistakeTimes_Text.append('-' + str(dt.timedelta(seconds=round(abs(lmt)))))
                else:
                    currentCompetitor.legMistakeTimes_Text.append('X')


def getLucky(ev, luckyControlThreshold):  # Calculate
    allEventControls = []  # The list of all event controls.
    # Collect all event controls by scanning each category and adding to the list if it is not already there.
    for cat in ev.categoryList:
        for cont in cat.course.controls:
            if cont not in allEventControls:
                allEventControls.append(cont)
    # Establish a list for collection of each punch of each runner of each category at each control. The punch time
    # tag is adjusted with the offset of the runner's start time relative to the event start. This way there is a
    # uniform time base to calculate if punches occurred within a certain time frame from each other. Each entry in
    # the list is a list itself of the following form:[control, category, competitor, adjusted punch time].
    punchList = []
    for cont in allEventControls:
        punchList.append([])
        for cat in ev.categoryList:
            if cont in cat.course.controls:
                for comp in cat.competitors:
                    if comp.cumulativeLegTimesSeconds[cat.course.controls.index(cont)] > 0 and \
                            not comp.startTimeOffsetFromEventStartSeconds < 0:
                        punchList[allEventControls.index(cont)].append([cont, cat, comp, comp.cumulativeLegTimesSeconds
                        [cat.course.controls.index(cont)] + comp.startTimeOffsetFromEventStartSeconds])
    for cont in punchList:
        if cont[0][0] != 'F':
            cont.sort(key=lambda x: x[3])
            for item in cont:
                # for item in punchList[punchList.index(cont)]:
                if cont.index(item) == 0:
                    previousTimeTag = item[3]
                else:
                    if item[3] - previousTimeTag <= luckyControlThreshold:
                        item[2].numberOfLuckyControls += 1
                        item[2].luckyControlsList.append(item[0])
                        item[2].luckyControlsSpeedIndices.append(item[2].cruisingSpeeds[item[2].controlList.index(
                            item[0])])
                    previousTimeTag = item[3]


def trainSpotting(ev, trainThreshold):  # Calculate
    allEventControls = []  # The list of all event controls.
    # Collect all event controls by scanning each category and adding to the list if it is not already there.
    for cat in ev.categoryList:
        for cont in cat.course.controls:
            if cont not in allEventControls:
                allEventControls.append(cont)
    # Establish a list for collection of each punch of each runner of each category at each control. The punch time
    # tag is adjusted with the offset of the runner's start time relative to the event start. This way there is a
    # uniform time base to calculate if punches occurred within a certain time frame from each other. Each entry in
    # the list is a list itself of the following form:[control, category, competitor, adjusted punch time].
    punchList = []
    for cont in allEventControls:
        punchList.append([])
        for cat in ev.categoryList:
            if cont in cat.course.controls:
                for comp in cat.competitors:
                    if comp.cumulativeLegTimesSeconds[cat.course.controls.index(cont)] > 0 and \
                            not comp.startTimeOffsetFromEventStartSeconds < 0:
                        punchList[allEventControls.index(cont)].append([cont, cat, comp, comp.cumulativeLegTimesSeconds
                        [cat.course.controls.index(cont)] + comp.startTimeOffsetFromEventStartSeconds])
    # Establish a list for clusters (groups of punches that were made close to each other) for each control. These
    # clusters form the base for detecting trains of runners - a train is a subgroup of the cluster that is detected in
    # N consecutive controls.
    clusters = []
    for cont in punchList:
        if cont[0][0] != 'F':
            cont.sort(key=lambda x: x[3])  # Sort the punches according to their time stamp.
            clusters.append(detectClusters(cont, trainThreshold))
    # For each category, scan the controls in sequence and detect trains of various sizes.
    for cat in ev.categoryList:
        cat.isTrainCalculated = list()
        cat.possibleTrains = calculatePossibleTrains(cat)
        for item in cat.possibleTrains:
            cat.isTrainCalculated.append(False)
        # cat.isTrainCalculated = copy.deepcopy(cat.possibleTrains)
        # for item in cat.isTrainCalculated:
        #     item.append(False)
        # for currentTrainLength in range(len(cat.course.controls)):
        #     cat.trains.append([])
        cat.trainsByControls = list()
        # cat.trainsByControls = getTrains(clusters, cat, cat.possibleTrains[-1])  # Get all the trains recursively from the
        getTrains(clusters, cat, cat.possibleTrains[-1], trainThreshold)  # Get all the trains recursively from the
        # longest train possible in the course.
        realTrains = list()
        for train in cat.trainsByControls:
            if len(train[0]) > 1 and len(train) > 1:
                realTrains.append(train)
        # Extract the trains in which the competitor is a part of
        for comp in cat.competitors:
            comp.trains = list()
            comp.filteredTrains = list()
            for train in realTrains:
                for car in train:  # Traverse all "train cars" for the current course segment.
                    if train.index(car) > 0:  # Skip the first item in the train - the controls defining the segment.
                        for punch in car:  # Check each punch for the competitor.
                            try:
                                if comp in punch:
                                    comp.trains.append(train)
                                    break
                            except:
                                pass
            for compTrain in comp.trains:
                temp_train = list()
                for car in compTrain:
                    if compTrain.index(car) == 0:
                        temp_train.append(car)
                    else:
                        for punch in car:
                            if comp in punch:
                                temp_train.append(car)
                                break
                comp.filteredTrains.append([])
                for i in temp_train:
                    comp.filteredTrains[-1].append(i)
            comp.filteredTrains.sort(key=lambda x: [len(x[0])], reverse=True)
            trueTrains = list()
            comp.trueTrains = list()
            for index in range(len(comp.filteredTrains)):
                found = False
                if index == 0:
                    trueTrains.append(comp.filteredTrains[index])
                else:
                    for item in trueTrains:
                        if comp.filteredTrains[index][0][0] in item[0]:
                            found = True
                            break
                    if not found:
                        trueTrains.append(comp.filteredTrains[index])
            for item in trueTrains:
                comp.trueTrains.append(item)
    pass

    #         for item in cont:
    #             # for item in punchList[punchList.index(cont)]:
    #             if cont.index(item) == 0:
    #                 previousTimeTag = item[3]
    #             else:
    #                 if item[3] - previousTimeTag <= trainThreshold:
    #                     item[2].numberOfLuckyControls += 1
    #                     item[2].luckyControlsList.append(item[0])
    #                     item[2].luckyControlsSpeedIndices.append(item[2].cruisingSpeeds[item[2].controlList.index(
    #                         item[0])])
    #                 previousTimeTag = item[3]
    # pass


def getTrains(clusters, cat, train, trainThreshold):
    # if cat.trains[len(train)].index(train)[0] == True:
    #     return cat.trains[len(train)]
    print("Incoming Train: ", train)
    if cat.isTrainCalculated[cat.possibleTrains.index(train)] is True:
        print("Outgoing Train (True): ", cat.trainsByControls[getIndex(cat.trainsByControls, train)][0][0])
        return cat.trainsByControls[getIndex(cat.trainsByControls, train)]
    # return cat.possibleTrains[cat.possibleTrains.index(train)]
    if len(train) == 1:
        # cat.possibleTrains[cat.possibleTrains.index(train)].append(clusters[getIndex(clusters, (train[0:1]))])
        cat.trainsByControls.append(clusters[getIndex(clusters, (train[0:1]))])
        cat.isTrainCalculated[cat.possibleTrains.index(train)] = True
        print("Outgoing Train (len=1): ", cat.trainsByControls[-1][0][0])
        return cat.trainsByControls[-1]
        # return cat.possibleTrains[cat.possibleTrains.index(train)]
        # cat.trains[len(train)] = clusters[getClusterIndex(clusters, train[0])]
        # return cat.trains[len(train)]
    else:
        cat.isTrainCalculated[cat.possibleTrains.index(train)] = True
        # cat.possibleTrains[cat.possibleTrains.index(train)].append(
        #     intersection(intersection(getTrains(clusters, cat, train[0:1]), getTrains(clusters, cat, train[1:])),
        #                  intersection(getTrains(clusters, cat, train[:len(train)]), getTrains(clusters, cat, train[-1:]))
        #                  )
        # )
        print("Big train, have to split...")
        littleLeftTrain = getTrains(clusters, cat, train[0:1], trainThreshold)
        print("Little left Train (len>1): ", littleLeftTrain[0][0])
        bigRightTrain = getTrains(clusters, cat, train[1:], trainThreshold)
        print("Big Right Train (len>1): ", bigRightTrain[0][0])
        print("Insering from left.")
        left = True
        leftIntersection = intersection(littleLeftTrain, bigRightTrain, trainThreshold)
        print("Left intersection: ", leftIntersection[0])
        bigLeftTrain = getTrains(clusters, cat, train[:(len(train) - 1)], trainThreshold)
        print("Big left Train (len>1): ", bigLeftTrain[0][0])
        littleRightTrain = getTrains(clusters, cat, train[-1:], trainThreshold)
        print("Little Right Train (len>1): ", littleRightTrain[0][0])
        print("Appending from right.")
        left = False
        rightIntersection = intersection(bigLeftTrain, littleRightTrain, trainThreshold)
        print("Right intersection: ", rightIntersection[0])
        cat.trainsByControls.append(intersection(leftIntersection, rightIntersection, trainThreshold))
        return cat.trainsByControls[-1]

        # cat.trains[len(train)].append(intersection(getTrains(clusters, cat, train[0]),
        #                                            getTrains(clusters, cat, train[1:])))
        # cat.trains[len(train)].append(intersection(getTrains(clusters, cat, train[:len(train)],
        #                                                      getTrains(clusters, cat, train[-1]))))
        # cat.trains[len(train)][cat.trains[len(train)].index(train)].insert(0, True)
        # return cat.trains[len(train)]


def getIndex(twoDList, item):
    for x in twoDList:
        if x[0] == item:
            return twoDList.index(x)
    print("getIndex failed for: ", twoDList, item)
    return None


def intersection(trainLeft, trainRight, trainThreshold):
    """This function takes two clusters (trains) and outputs a single combined cluster (train) consisting of punches
    that belong in both clusters (trains) """
    resultingTrain = [[]]  # This will store the resulting train
    for ctll in trainLeft[0]:  # Collect all the control numbers from the left train
        resultingTrain[0].append(ctll)
    for ctlr in trainRight[0]:  # Add the control numbers that are not in the left train from the right train
        if ctlr not in resultingTrain[0]:
            resultingTrain[0].append(ctlr)
    tagLeft = True  # This marks the first item in the left train - the control number list
    for leftCluster in trainLeft:  # Go over all the clusters in the left train
        if tagLeft:  # If this is the control number list, then skip it
            tagLeft = False
            continue
        else:  # Otherwise, for each left cluster, go over the right clusters
            tagRight = True  # This marks the first item in the right train - the control number list
            for rightCluster in trainRight:  # Go over all the clusters in the left train
                matches = list()  # Establish a list for competitors that exist in both left and right clusters
                tempCluster = list()  # Establish a list of punches that belong to competitors with a match
                if tagRight:  # If this is the control number list, then skip it
                    tagRight = False
                    continue
                else:  # Otherwise, for each punch in the left cluster, try to match a punch in the right cluster
                    # belonging to the same competitor
                    for leftPunch in leftCluster:
                        for rightPunch in rightCluster:
                            try:
                                if leftPunch[2] == rightPunch[2]:  # If the punches belong to the same competitor
                                    if leftPunch[2] not in matches:  # and, if a match was not detected yet for this
                                        # competitor,
                                        matches.append(leftPunch[2])  # Then, add the competitor to the matches list
                                    tempCluster.append(leftPunch)  # Add the punch from the left cluster to the list
                                    tempCluster.append(rightPunch)  # Add the punch from the right cluster to the list
                            except:
                                print("Right cluster:", rightCluster)
                                print("Left cluster:", leftCluster)
                if len(matches) > 1:  # If the matches list contains more than one competitor, then there is a train
                    resultingTrain.append([])  # Initialize the punches list for the train
                    for punch in tempCluster:  # Go over the punches that were collected
                        if punch not in resultingTrain[-1]:  # and, if the punch is not already in the list,
                            try:
                                resultingTrain[-1].append(punch)  # then add the punch to the train
                            except:
                                pass
    return validateTrain(resultingTrain, trainThreshold)  # Make sure that the resulting train is valid in terms of a
    # consistent time difference among the competitors allegedly in the train


def validateTrain(incomingTrain, trainThreshold):
    trainLength = len(incomingTrain[0])
    tempTrain = list()
    earlyCluster = list()
    lateCluster = list()
    earlyClusterCompetitors = list()
    lateClusterCompetitors = list()
    # subCluster = list()
    splitDetected = False
    # subCluster.append([])
    controlCluster = True  # Marks the first list which consists of the control numbers of the train
    # tempTrain.append(incomingTrain[0])
    for cluster in incomingTrain:
        splitDetected = False
        earlyCluster.clear()
        lateCluster.clear()
        earlyClusterCompetitors.clear()
        lateClusterCompetitors.clear()
        if controlCluster:
            tempTrain.append(cluster)  # Set the train's identification (controls list).
            controlCluster = False
        else:
            subCluster = list() ###################################
            tempCluster = list()  # This is the cluster that has the punches without the controls list
            for punch in cluster:  # Add all the punches in the cluster to a temporary list
                tempCluster.append(punch)
            # tempCluster.sort(key=lambda x: (x[0], x[3]))    # Sort by control number and then by punch time.
            tempCluster.sort(key=lambda x: x[3])  # Sort by punch time.
            currentControl = tempCluster[0][0]  # Establish the current control
            currentTimeTag = tempCluster[0][3]  # Establish the current time tag to which others are compared to
            for punch in tempCluster:  # Go over each punch in the cluster
                if punch[3] - currentTimeTag <= trainThreshold:  # If the punch is within the threshold
                    # subCluster[-1].append(punch)
                    subCluster.append(punch)  # Add the punch to the current subcluster
                    earlyClusterCompetitors.append(punch[2])
                    currentTimeTag = punch[3]  # Move the time tag to the current one
                else:   # If the time tag is too far apart, check if we are now on a different control
                    if punch[0] == currentControl:  # If still on the same control, split the cluster and recheck it
                        # tempTrain.append(validateCluster(stripCompetitor(cluster, punch[2]), trainThreshold,
                        #                                  trainLength))
                        tempTrain.append(validateCluster(buildCluster(cluster, earlyClusterCompetitors, early=True),
                                                         trainThreshold, trainLength))
                        tempTrain.append(validateCluster(buildCluster(cluster, earlyClusterCompetitors, early=False),
                                                         trainThreshold, trainLength))
                        splitDetected = True
                        break   # There is no more point in checking the cluster
                    else:   # If we are on a different control, append the punch to the cluster and reset the control
                        # and time tag
                        subCluster.append(punch)
                        earlyClusterCompetitors.clear()
                        lateClusterCompetitors.clear()
                        earlyClusterCompetitors.append(punch[2])
                        currentControl = punch[0]
                        currentTimeTag = punch[3]
            if splitDetected:
                continue
            else:
                tempTrain.append(tempCluster)


def validateCluster(cluster, trainThreshold, trainLength):
    returnedClusters = list()
    valid = True
    if containsSingleCompetitor(cluster):
        return []
    else:
        cluster.sort(key=lambda x: x[3])  # Make sure that the cluster is sorted according to the time tag
        previousTimeTag = cluster[0][3]  # Establish a baseline for time comparisons
        currentControl = cluster[0][0]  # Establish a base control
        earlyClusterCompetitors = list()  # Initialize a list of competitors up to a comparison failure
        earlyCluster = list()  # Initialize a list of punches that belong to competitors up to the comparison failure
        lateCluster = list()  # Initialize a list of punches that belong to competitors from the comparison failure
        # onwards
        for punch in cluster:
            if punch[3] - previousTimeTag <= trainThreshold:
                previousTimeTag = punch[3]
                # if punch[2] not in earlyClusterCompetitors:
                earlyClusterCompetitors.append(punch[2])
                # continue
            else:
                if punch[0] == currentControl:
                    valid = False
                    earlyCluster = buildCluster(cluster, earlyClusterCompetitors, early=True)
                    returnedClusters.append(validateCluster(earlyCluster, trainThreshold))
                    lateCluster = buildCluster(cluster, earlyClusterCompetitors, early=False)
                    returnedClusters.append(validateCluster(lateCluster, trainThreshold))
                    # for item in cluster:
                    #     if item not in earlyCluster:
                    #         lateCluster.append(item)
                    # return validateCluster(stripCompetitor(cluster, punch[2]), trainThreshold)
                else:
                    currentControl = punch[0]
                    previousTimeTag = punch[3]
                    earlyClusterCompetitors.clear()
                    earlyClusterCompetitors.append(punch[2])
                    earlyCluster.clear()
                    lateCluster.clear()
        if valid:
            return cluster
        else:
            return cleaned(returnedClusters, trainLength)


def cleaned(clusters, trainLength):
    result = list()
    for cluster in clusters:
        if len(cluster) < 2 * trainLength:
            continue
        else:
            result.append(cluster)
    return result


def buildCluster(cluster, competitorList, early):
    updatedCluster = list()
    isRelevantPunch = list()
    for item in cluster:
        isRelevantPunch.append(True)
    if early:
        for comp in competitorList:
            for punch in cluster:
                if punch[2] == comp:
                    updatedCluster.append(punch)
    else:
        for punch in cluster:
            for comp in competitorList:
                if punch[2] == comp:
                    isRelevantPunch[cluster.index(punch)] = False
                # updatedCluster.append(punch)
        for punch in cluster:
            if isRelevantPunch[cluster.index(punch)]:
                updatedCluster.append(punch)
    return updatedCluster


def containsSingleCompetitor(cluster):
    if len(cluster) == 0:  # Check to see if the cluster is empty. If so, return True
        return True
    else:  # Otherwise, if the competitor has not been added previously to the list, add it.
        listOfCompetitors = list()
        for punch in cluster:
            if punch[2] not in listOfCompetitors:
                listOfCompetitors.append(punch[2])
        if len(listOfCompetitors) > 1:  # Check to see how many competitors are in the list.
            return False
        else:
            return True


def stripCompetitor(cluster, competitor):
    if len(cluster) == 0:  # Not likely, but in case there is an empty cluster...
        return []
    else:
        modifiedCluster = list()  # Create a list that keeps the other competitors
        for punch in cluster:  # Scan the punches
            if punch[2] == competitor:  # If the punch belongs to the competitor that is to be stripped, skip it
                continue
            else:
                modifiedCluster.append(punch)  # Otherwise, add the punch to the modified cluster.
    return modifiedCluster


def getClusterIndex(clusters, controlNumber):
    for item in range(clusters.len):
        if clusters[item][0] == controlNumber:
            return item
    return None


def detectClusters(controlPunchList, trainThreshold):
    """ This function scans consecutive punches at a control and groups punches made within the train threshold of
    each other. The function returns the detected clusters. """
    clusters = [[controlPunchList[0][0]]]  # Initialize the cluster list by appending the control number.
    currentCluster = [controlPunchList[0]]  # Initialize the current cluster with the first punch.
    for punch in controlPunchList:  # Go over the list of punches and test for punches made close to each other.
        if controlPunchList.index(punch) == 0:  # If this is the first punch in the list, then it is the first reference
            lastPunch = punch
        else:
            if punch[3] - lastPunch[3] <= trainThreshold:  # Test if the current punch is within trainThreshold seconds
                # of the last punch.
                currentCluster.append(punch)  # If so, add the current punch to the current cluster.
                lastPunch = punch  # Establish a new refernce for the next punch.
            else:  # If the current punch is too far away, then this means that the current cluster has ended.
                if len(currentCluster) <= 1:  # If the current cluster only contains one punch, then it should be
                    # discarded and a new cluster should be started.
                    currentCluster.clear()  # Establish a new clean cluster.
                    currentCluster.append(punch)  # Insert the current punch as the first in the new cluster.
                    lastPunch = punch  # Establish a new reference for time of punch.
                else:  # If the current cluster includes more than one punch, then it is a valid cluster.
                    temp = list()  # Establish a temporary list for copying puroposes.
                    clusters.append(myDeepCopy(temp, currentCluster))  # Deep copy the current cluster into the
                    # cluster list.
                    currentCluster.clear()  # Reset the current cluster.
                    currentCluster.append(punch)  # Start a new current cluster with the current punch.
                    lastPunch = punch  # Establish a new reference for time of punch.
    return clusters


def myDeepCopy(targetList, sourceList):
    for punch in sourceList:
        targetList.append(punch)
    # targetList = copy.deepcopy(sourceList)
    return targetList


def calculatePossibleTrains(cat):
    # This function provides the list of all possible trains for the control list relevant to the category course. It
    # takes the list of controls from the course and, for each possible train length moves a window of that length
    # across the control list, taking the slice of controls inside that window and adding it to the list.
    maxCarts = len(cat.course.controls) - 1
    possibleTrains = list()
    for trainLength in range(1, maxCarts):
        # possibleTrains.append([])
        first = 0
        while first + trainLength - 1 < maxCarts:
            possibleTrains.append(cat.course.controls[first:(first + trainLength)])
            first += 1
    possibleTrains.append(cat.course.controls[:-1])  # Append the entire control list sans the final control.
    # for item in possibleTrains:
    #     item.insert(0, False)
    return possibleTrains


def biggestGainersLosers(ev):  # Calculate the biggest gainerOrLosers and losers
    categoryCruisingSpeedsList = []
    # Collect and sort the valid cruising speeds for the category
    for cat in ev.categoryList:
        categoryCruisingSpeedsList.clear()
        for comp in cat.competitors:
            if not comp.dns and not comp.dnf and not comp.disq and (float(comp.nominalCruisingSpeed) > 0.0):
                categoryCruisingSpeedsList.append(float(comp.nominalCruisingSpeed))
        categoryCruisingSpeedsList.sort()
        # Scan the sorted cruising speeds list and compare each runner's cruising speed to each cruising speed. After
        # establishing the theoretical place in the category, subtract it from the actual runner's place.
        for comp in cat.competitors:
            if not comp.dnf and not comp.dns and not comp.disq and (float(comp.nominalCruisingSpeed) > 0.0):
                for crSpeed in categoryCruisingSpeedsList:
                    if comp.nominalCruisingSpeed <= crSpeed:
                        comp.gainOrLossDueToAccuracy = categoryCruisingSpeedsList.index(crSpeed) - comp.place + 1
                        break

        # Scan the competitor list and find the biggest winner and loser
        biggestWinner = []
        biggestLoser = []
        gainOrLossIndices = []
        gainerOrLoser = []
        biggestWinner.clear()
        biggestLoser.clear()
        gainOrLossIndices.clear()
        gainerOrLoser.clear()
        for comp in cat.competitors:
            if not comp.dns and not comp.dnf and not comp.disq:
                gainerOrLoser.append(comp.gainOrLossDueToAccuracy)
                gainOrLossIndices.append(cat.competitors.index(comp))
        gainOrLossIndices.sort(key=gainerOrLoser.__getitem__)
        cat.biggestGainer = [cat.competitors[gainOrLossIndices[-1]], cat.competitors[gainOrLossIndices[-1]].
            gainOrLossDueToAccuracy]
        cat.biggestLoser = [cat.competitors[gainOrLossIndices[0]], cat.competitors[gainOrLossIndices[0]].
            gainOrLossDueToAccuracy]
        cat.biggestGainer_Text = cat.competitors[gainOrLossIndices[-1]].firstName + ' ' + \
                                 cat.competitors[gainOrLossIndices[-1]].lastName + \
                                 " ממקום: " + str(cat.competitors[gainOrLossIndices[-1]].place + \
                                                  cat.competitors[
                                                      gainOrLossIndices[-1]].gainOrLossDueToAccuracy) + " למקום " + \
                                 str(cat.competitors[gainOrLossIndices[-1]].place)
        cat.biggestLoser_Text = cat.competitors[gainOrLossIndices[0]].firstName + ' ' + \
                                cat.competitors[gainOrLossIndices[0]].lastName + \
                                " ממקום: " + str(cat.competitors[gainOrLossIndices[0]].place + \
                                                 cat.competitors[
                                                     gainOrLossIndices[0]].gainOrLossDueToAccuracy) + " למקום " + \
                                str(cat.competitors[gainOrLossIndices[0]].place)
        pass


def roadrunnerAndSwissClock(ev):
    mistakeRatios = []
    mistakeIndices = []
    cruisingSpeeds = []
    cruisingIndices = []
    stabilityValues = []
    stabilityIndices = []
    for cat in ev.categoryList:
        mistakeRatios.clear()
        cruisingSpeeds.clear()
        mistakeIndices.clear()
        cruisingIndices.clear()
        stabilityValues.clear()
        stabilityIndices.clear()
        for comp in cat.competitors:
            if not comp.dns and not comp.dnf and not comp.disq and comp.nominalCruisingSpeed < 1000:
                mistakeRatios.append(comp.mistakeRatioPercent)
                cruisingSpeeds.append(comp.nominalCruisingSpeed)
                stabilityValues.append(comp.stabilityValue)
                mistakeIndices.append(cat.competitors.index(comp))
                cruisingIndices.append(cat.competitors.index(comp))
                stabilityIndices.append(cat.competitors.index(comp))
        cruisingIndices.sort(key=cruisingSpeeds.__getitem__)
        index = 0
        while cat.competitors[cruisingIndices[index]].nominalCruisingSpeed < 0.0:
            index += 1
        roadRunner = cruisingIndices[index]
        mistakeIndices.sort(key=mistakeRatios.__getitem__)
        index = 0
        while cat.competitors[mistakeIndices[index]].nominalCruisingSpeed < 0.0:
            index += 1
        swissClock = mistakeIndices[index]
        stabilityIndices.sort(key=stabilityValues.__getitem__)
        theRock = stabilityIndices[0]
        cat.theRoadrunner = 'הטוחן: ' + cat.competitors[roadRunner].firstName + ' ' + cat.competitors[roadRunner]. \
            lastName + ': ' + str(round(cat.competitors[roadRunner].nominalCruisingSpeed * 100, 1))
        cat.theSwissClock = 'השעון השוויצרי: ' + cat.competitors[swissClock].firstName + ' ' + cat.competitors[
            swissClock]. \
            lastName + ': ' + str(cat.competitors[swissClock].mistakeRatioPercent)
        cat.theRock = 'הסלע: ' + cat.competitors[theRock].firstName + ' ' + cat.competitors[theRock]. \
            lastName + ': ' + str(cat.competitors[theRock].stabilityValue)
    pass


def prepareDataForGraphing(ev):
    luckyControls = []
    startTime = []
    mistakRatios = []
    cruisingSpeeds = []
    names = []
    mistakeVsSpeed_fileName = '/public/Nivut_CD/Lapcombat/mistakeVspeed.csv'
    luckVsMistake_fileName = '/public/Nivut_CD/Lapcombat/luckVmistake.csv'
    luckVsStartTime_fileName = '/public/Nivut_CD/Lapcombat/luckVstart.csv'
    luckyControls.clear()
    startTime.clear()
    mistakRatios.clear()
    cruisingSpeeds.clear()
    names.clear()
    for cat in ev.categoryList:
        for comp in cat.competitors:
            if (not comp.dns) and (not comp.dnf) and (not comp.disq) and (comp.nominalCruisingSpeed > 0) and \
                    (comp.nominalCruisingSpeed < 2.0) and (comp.startTimeOffsetFromEventStartSeconds > 0) and \
                    (comp.nominalCruisingSpeed > 0.7):
                luckyControls.append(comp.numberOfLuckyControls)
                mistakRatios.append(comp.mistakeRatioPercent)
                cruisingSpeeds.append(comp.nominalCruisingSpeed * 100)
                names.append(comp.firstName + " " + comp.lastName)
                startTime.append(comp.startTimeOffsetFromEventStartSeconds)
    with open(mistakeVsSpeed_fileName, 'w') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(names)
        csvWriter.writerow(cruisingSpeeds)
        csvWriter.writerow(mistakRatios)
    with open(luckVsMistake_fileName, 'w') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(names)
        csvWriter.writerow(mistakRatios)
        csvWriter.writerow(luckyControls)
    with open(luckVsStartTime_fileName, 'w') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(names)
        csvWriter.writerow(startTime)
        csvWriter.writerow(luckyControls)

def calculateEvent(resultsFile):
    mulkaDatetimeStrptimeString = "%Y-%m-%dT%H:%M:%S%z"
    SIDroidDatetimeStrptimeString = "%Y-%m-%dT%H:%M:%S.%f%z"
    SIDroidTimeStampsDatetimeStrptimeString = "%Y-%m-%dT%H:%M:%S"
    classes = []
    tree = ET.parse(resultsFile)
    root = tree.getroot()
    app = root.attrib.get('creator')  # Find the application that created the results file.
    fileCreationTime = root.get('createTime')  # Get the file creation time. This will serve as a base for time events
    defaultStartTime = dt.datetime(2021, 1, 1)
    luckyControlThresholdSeconds = 10  # This is the time threshold for calculating whether the runner saw someone punching
    # the control, thus revealing its location.
    numberOfControlsForGroupOrienteeringThreshold = 5  # This is the number of consecutive joint punches threshold for
    # considering two runners as tracking each other.
    mulka = False
    if app[0:5] == 'Mulka':
        mulka = True  # Check if the results came from Mulka or not
    if mulka:
        datetimeStrptimeString = mulkaDatetimeStrptimeString
        fct = dt.datetime.strptime(fileCreationTime, datetimeStrptimeString)  # Convert to datetime object
        # Make a copy of the file creation time in order to establish an arbitrary event start time
        baseEventStart = dt.datetime(fct.year, fct.month, fct.day, hour=6, minute=0, second=0)
    else:
        datetimeStrptimeString = SIDroidDatetimeStrptimeString
        fct = dt.datetime.strptime(fileCreationTime, datetimeStrptimeString)  # Convert to datetime object
        # Make a copy of the file creation time in order to establish an arbitrary event start time
        baseEventStart = dt.datetime(fct.year, fct.month, fct.day, hour=6, minute=0, second=0)
    event = Event(resultsFile, tree, root, mulka, baseEventStart)
    # competitors = event.getCompetitors()
    # categories = event.getCategoryNames()
    # print("Event name: " + event.eventName)
    event.categoryList = event.getCategories(resultsFile)
    calculateLapCombat(event)
    biggestGainersLosers(event)
    roadrunnerAndSwissClock(event)
    getLucky(event, luckyControlThresholdSeconds)
    formatLapCombatItems(event)
    # prepareDataForGraphing(event)
    # clus = trainSpotting(event, 15)
    # for i in range(len(event.categoryList[3].course.legList)):
    #     print(event.categoryList[3].course.legList[i])
    # print('Done!')
    return event

# event = Event(resultFile)
# # competitors = event.getCompetitors()
# # categories = event.getCategoryNames()
# print("Event name: " + event.eventName)
# event.categoryList = event.getCategories()
# calculateLapCombat(event)
# biggestGainersLosers(event)
# roadrunnerAndSwissClock(event)
# getLucky(event, luckyControlThresholdSeconds)
# formatLapCombatItems(event)
# prepareDataForGraphing(event)
# # clus = trainSpotting(event, 15)
# # for i in range(len(event.categoryList[3].course.legList)):
# #     print(event.categoryList[3].course.legList[i])
# print('Done!')
# # a = event.getCategories()
# # print (a)
# # print(competitors[0])
