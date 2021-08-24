"""
jsonGenerator.py
author: Toby
date: Aug. 21 2021

Here is a systematic way to generate BlueStack marco for GxB2.

TODO:
- auto excursion explore [DONE]
- pet training [DONE]
- pet fighting
"""

import json
from datetime import datetime

RESOLUTION_X = 900
RESOLUTION_Y = 1600
FOUR_HOURS = 14400  # in second
SECOND = 1000
MINUTE = SECOND * 60

# Locations
CLEARALL = (83, 5)
GAME_ENTRANCE = (444, 366)
HOMEPAGE_TAB = (54, 1558)
CAPSULE_TAB = (522, 1522)
GUILD_TAB = (666, 1525)
ALCHEMY_BUTTON = (420, 48.5)
CAMPAIGN_BUTTON = (444, 1285)
EXCURSION_BUTTON = (840, 673)
QUIZ_BUTTON = (844, 430)
RETURN_AND_MAILBOX_BUTTON = (838, 55)
FRIENDS_BUTTON = (828, 170)
SERVANT_BUTTON = (841, 545)


class Solution:
    def __init__(self, START_TIME=1000, DEBUG=False):
        self.data = {}
        self.moving_timestamp = START_TIME
        self.DEFAULT_WAIT = 2 * SECOND  # ms
        self.LONGER_WAIT = 4 * SECOND  # ms
        self.DEBUG = DEBUG

    # the basic blocks
    def saveJson(self, filename="data.json"):
        """
        Save the json dictionary to file.
        """
        text_content = json.dumps(self.data, indent=4, sort_keys=False)
        if self.DEBUG:
            print(text_content)
        with open(filename, "w") as outfile:
            outfile.write(text_content)

    def createHeader(self):
        """
        Create header for the json file.
        """
        self.data["Acceleration"] = 1
        self.data["CreationTime"] = datetime.now().strftime("%Y%m%dT%H%M%S")
        self.data["DoNotShowWindowOnFinish"] = False
        self.data["Events"] = []

    def createFooter(
        self,
        LoopInterval=FOUR_HOURS,
        LoopType="UntilStopped",
        RestartPlayerAfterMinutes=60,
    ):
        """
        Create footer for the json file.
        """
        self.data["LoopDuration"] = 0
        self.data["LoopInterval"] = LoopInterval
        self.data["LoopIterations"] = 1
        self.data["LoopType"] = LoopType
        self.data["MacroSchemaVersion"] = 2
        self.data["RestartPlayer"] = False
        self.data["RestartPlayerAfterMinutes"] = RestartPlayerAfterMinutes

    # def addEvent(self, start_timestamp, X, Y, span=100):
    def addEvent(self, start_timestamp, coordinateXY, span=100):
        """
        General type for adding an event, which will be
        one mouse down and one mouse up by default.
        start_timestamp: the starting time stamp for this event, in int
        coordinateXY: a tuple (int, int) for (X, Y) location
        span: time between mouse down and mouse up in ms
        """
        X, Y = coordinateXY
        if X > 100 or Y > 100:
            local_X = 100 * X / RESOLUTION_X  # change to 0-100 %
            local_Y = 100 * Y / RESOLUTION_Y
        else:
            local_X = X
            local_Y = Y

        mouseDown = {
            "Delta": 0,
            "EventType": "MouseDown",
            "Timestamp": start_timestamp,
            "X": local_X,
            "Y": local_Y,
        }
        mouseUp = {
            "Delta": 0,
            "EventType": "MouseUp",
            "Timestamp": start_timestamp + span,
            "X": local_X,
            "Y": local_Y,
        }
        self.data["Events"].append(mouseDown)
        self.data["Events"].append(mouseUp)

    def returnHomepage(self):
        for _ in range(2):
            self.addEvent(self.moving_timestamp, HOMEPAGE_TAB)
            self.moving_timestamp += 2 * SECOND

    # the specific function blocks
    def openGame(self, timestamp=1400):
        self.moving_timestamp += timestamp
        self.addEvent(self.moving_timestamp, GAME_ENTRANCE)
        # wait for 30 seconds in case of update
        self.moving_timestamp += 30 * SECOND

    def closeAll(self):
        task = {"EventType": "UiRecentApps", "Timestamp": self.moving_timestamp}
        self.data["Events"].append(task)
        self.moving_timestamp += 5 * SECOND
        self.addEvent(self.moving_timestamp, CLEARALL)

    def getCampaignRewards(self):
        """
        Get campaign rewards.
        A closed loop from home to home.
        """
        self.returnHomepage()

        # enter campaign
        self.addEvent(self.moving_timestamp, CAMPAIGN_BUTTON)
        self.moving_timestamp += self.LONGER_WAIT

        # hit collect 5 times
        for _ in range(5):
            self.addEvent(self.moving_timestamp, (822, 880))
            self.moving_timestamp += self.DEFAULT_WAIT

        # open the item box
        self.addEvent(self.moving_timestamp, (814, 1365))
        self.moving_timestamp += self.LONGER_WAIT

        # hit claim
        self.addEvent(self.moving_timestamp, (457, 1091))
        self.moving_timestamp += self.DEFAULT_WAIT

        # go back to the front page
        self.returnHomepage()

    def getDormRewards(self):
        self.returnHomepage()

        # go to campus
        self.addEvent(self.moving_timestamp, (113, 1297))
        self.moving_timestamp += self.LONGER_WAIT

        # go life tab
        self.addEvent(self.moving_timestamp, (660, 149))
        self.moving_timestamp += self.LONGER_WAIT

        # select Dorm
        self.addEvent(self.moving_timestamp, (668, 437))
        self.moving_timestamp += self.LONGER_WAIT

        # clicl claim
        self.addEvent(self.moving_timestamp, (142, 226))
        self.moving_timestamp += self.LONGER_WAIT

        # hit collect
        self.addEvent(self.moving_timestamp, (471, 973))
        self.moving_timestamp += self.LONGER_WAIT

        # hit return
        self.addEvent(self.moving_timestamp, (838, 55))
        self.moving_timestamp += self.LONGER_WAIT

        # go back to home page
        self.returnHomepage()

    def getExcursionRewards(self):
        self.returnHomepage()

        # go to excursion
        self.addEvent(self.moving_timestamp, EXCURSION_BUTTON)
        self.moving_timestamp += self.LONGER_WAIT

        # hit claim all
        for _ in range(2):
            self.addEvent(self.moving_timestamp, (144, 1450))
            self.moving_timestamp += self.DEFAULT_WAIT

        # hit auto explore
        self.addEvent(self.moving_timestamp, (702, 1336))
        self.moving_timestamp += self.DEFAULT_WAIT
        self.addEvent(self.moving_timestamp, (450, 1238))
        self.moving_timestamp += 10 * SECOND

        # hit return *
        for _ in range(4):
            self.addEvent(self.moving_timestamp, (838, 55))
            self.moving_timestamp += self.DEFAULT_WAIT

        # re-init
        self.returnHomepage()

    def getFreeRegularCapus(self):
        self.returnHomepage()

        # go to capsule
        self.addEvent(self.moving_timestamp, CAPSULE_TAB)
        self.moving_timestamp += self.DEFAULT_WAIT

        # hit regular pull
        self.addEvent(self.moving_timestamp, (536, 398))
        self.moving_timestamp += self.LONGER_WAIT

        # hit OK
        self.addEvent(self.moving_timestamp, (181, 1025))
        self.moving_timestamp += self.LONGER_WAIT

        self.returnHomepage()

    def doOneJuniorLeagueBattle(self):
        self.returnHomepage()

        # go to League
        self.addEvent(self.moving_timestamp, (800, 1300))
        self.moving_timestamp += self.DEFAULT_WAIT

        # go to League tab
        for _ in range(2):
            self.addEvent(self.moving_timestamp, (666, 152))
            self.moving_timestamp += self.DEFAULT_WAIT

        # go to Junior section
        self.addEvent(self.moving_timestamp, (455, 350))
        self.moving_timestamp += self.DEFAULT_WAIT

        self.addEvent(self.moving_timestamp, (463, 1326))  # hit fight
        self.moving_timestamp += self.LONGER_WAIT
        self.addEvent(self.moving_timestamp, (747, 952))  # pick the 3rd opponent
        self.moving_timestamp += self.LONGER_WAIT
        self.addEvent(self.moving_timestamp, (455, 924))  # confirm fight
        self.moving_timestamp += self.LONGER_WAIT
        for _ in range(2):
            self.addEvent(self.moving_timestamp, (817, 719))  # select reward
            self.moving_timestamp += self.LONGER_WAIT
        for _ in range(2):
            self.addEvent(self.moving_timestamp, (444, 1109))  # return *
            self.moving_timestamp += self.DEFAULT_WAIT
        self.returnHomepage()

    def getQuizRewards(self):
        self.returnHomepage()

        self.addEvent(self.moving_timestamp, QUIZ_BUTTON)  # open quiz
        self.moving_timestamp += self.LONGER_WAIT
        self.addEvent(self.moving_timestamp, (457, 1365))  # claim all
        self.moving_timestamp += self.LONGER_WAIT
        self.addEvent(self.moving_timestamp, (457, 1189))  # OK *
        self.moving_timestamp += self.LONGER_WAIT
        self.addEvent(self.moving_timestamp, (457, 1159))  # OK *
        self.moving_timestamp += self.LONGER_WAIT
        self.returnHomepage()

    def getAlchemyRewards(self):
        self.returnHomepage()

        self.addEvent(self.moving_timestamp, ALCHEMY_BUTTON)  # hit alchemy +
        self.moving_timestamp += self.LONGER_WAIT
        self.addEvent(self.moving_timestamp, (275, 953))  # hit free
        self.moving_timestamp += self.LONGER_WAIT
        self.returnHomepage()

    def getAllMailRewards(self):
        self.returnHomepage()

        self.addEvent(self.moving_timestamp, RETURN_AND_MAILBOX_BUTTON)  # hit mail box
        self.moving_timestamp += self.LONGER_WAIT
        for _ in range(2):
            self.addEvent(self.moving_timestamp, (442, 1266))  # claim all
            self.moving_timestamp += self.LONGER_WAIT
        self.returnHomepage()

    def takeServantClass(self):
        self.returnHomepage()

        self.addEvent(self.moving_timestamp, SERVANT_BUTTON)
        self.moving_timestamp += self.LONGER_WAIT
        for _ in range(2):
            self.addEvent(self.moving_timestamp, (450, 887))
            self.moving_timestamp += self.LONGER_WAIT
        for _ in range(3):
            self.addEvent(self.moving_timestamp, (810, 223))
            self.moving_timestamp += self.DEFAULT_WAIT
        for _ in range(3):
            self.addEvent(self.moving_timestamp, (512, 927))
            self.moving_timestamp += self.LONGER_WAIT
        self.returnHomepage()

    def getFriendsRewards(self, doCoop=True):
        self.returnHomepage()

        self.addEvent(self.moving_timestamp, FRIENDS_BUTTON)  # open friends
        self.moving_timestamp += self.LONGER_WAIT
        for _ in range(2):
            self.addEvent(self.moving_timestamp, (730, 544))  # cliam and send
            self.moving_timestamp += self.DEFAULT_WAIT

        if doCoop:
            self.addEvent(self.moving_timestamp, (744, 442))  # go coop
            self.moving_timestamp += self.DEFAULT_WAIT
            self.addEvent(self.moving_timestamp, (454, 1169))  # fight
            self.moving_timestamp += self.LONGER_WAIT
            self.addEvent(self.moving_timestamp, (457, 923))  # confirm fight
            self.moving_timestamp += self.LONGER_WAIT
            self.addEvent(self.moving_timestamp, (450, 1500))  # OK
            self.moving_timestamp += self.LONGER_WAIT

        self.returnHomepage()

    def getGuildRewards(self):
        self.returnHomepage()

        # sign-in
        self.addEvent(self.moving_timestamp, GUILD_TAB)
        self.moving_timestamp += self.LONGER_WAIT

        for _ in range(2):
            self.addEvent(self.moving_timestamp, (457, 380))
            self.moving_timestamp += self.DEFAULT_WAIT

        for _ in range(2):
            self.addEvent(self.moving_timestamp, (711, 772))
            self.moving_timestamp += self.DEFAULT_WAIT

        # return to guild page and do caffee
        for _ in range(3):
            self.addEvent(self.moving_timestamp, GUILD_TAB)
            self.moving_timestamp += self.DEFAULT_WAIT

        for _ in range(4):
            self.addEvent(self.moving_timestamp, (758, 443))
            self.moving_timestamp += self.DEFAULT_WAIT

        for _ in range(2):
            self.addEvent(self.moving_timestamp, (454, 1180))
            self.moving_timestamp += self.DEFAULT_WAIT

        self.addEvent(self.moving_timestamp, (184, 856))  # task 1
        self.moving_timestamp += self.DEFAULT_WAIT
        self.addEvent(self.moving_timestamp, (455, 856))  # task 2
        self.moving_timestamp += self.DEFAULT_WAIT
        self.addEvent(self.moving_timestamp, (716, 856))  # task 3
        self.moving_timestamp += self.DEFAULT_WAIT
        self.addEvent(self.moving_timestamp, (184, 1276))  # task 4
        self.moving_timestamp += self.DEFAULT_WAIT
        self.addEvent(self.moving_timestamp, (455, 1276))  # task 5
        self.moving_timestamp += self.DEFAULT_WAIT

        self.returnHomepage()


def main():
    app = Solution()
    app.createHeader()

    # start the app
    app.openGame()
    app.getCampaignRewards()
    app.getDormRewards()
    app.getExcursionRewards()
    app.doOneJuniorLeagueBattle()
    app.getFreeRegularCapus()
    app.getGuildRewards()
    app.getQuizRewards()
    app.getAlchemyRewards()
    app.getAllMailRewards()
    app.takeServantClass()
    app.getFriendsRewards()
    app.closeAll()
    app.createFooter(
        LoopInterval=(FOUR_HOURS - app.moving_timestamp // SECOND)
    )  # time calculated in seconds
    app.saveJson()


if __name__ == "__main__":
    main()
