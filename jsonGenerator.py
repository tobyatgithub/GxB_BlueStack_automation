"""
jsonGenerator.py
author: Toby
date: Aug. 21 2021

Here is a systematic way to generate BlueStack marco for GxB2.

TODO:
- auto excursion explore
- pet training
- pet fighting
"""

import json
from datetime import datetime

FOUR_HOURS = 14400  # in second


class Solution:
    def __init__(self, DEBUG=False):
        self.data = {}
        self.START_TIME = 1000
        self.resolutionX = 900
        self.resolutionY = 1600
        self.DEFAULT_WAIT = 2000  # ms
        self.LONGER_WAIT = 4000  # ms
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
        self, LoopInterval=FOUR_HOURS, LoopType="UntilStopped", RestartPlayerAfterMinutes=60
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

    def addEvent(self, start_timestamp, X, Y, span=100):
        """
        General type for adding an event, which will be
        one mouse down and one mouse up by default.
        start_timestamp: the starting time stamp for this event, in int
        X: x location for the mouse click, float
        Y: y location for the mouse click, float
        span: time between mouse down and mouse up in ms
        """
        if X > 100 or Y > 100:
            local_X = 100 * X / self.resolutionX  # change to 0-100 %
            local_Y = 100 * Y / self.resolutionY
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

    # the specific function blocks
    def openGame(self, timestamp=1400):
        moving_timestamp = timestamp
        self.addEvent(timestamp, 444, 366)

        moving_timestamp += self.LONGER_WAIT * 10
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT
        return moving_timestamp

    def closeAll(self, timestamp):
        moving_timestamp = timestamp
        task = {
            "EventType": "UiRecentApps",
            "Timestamp": moving_timestamp
        }
        self.data["Events"].append(task)
        moving_timestamp += self.LONGER_WAIT

        self.addEvent(moving_timestamp, 83, 5)

    def getCampaignRewards(self, timestamp):
        """
        Get campaign rewards.
        A closed loop from home to home.
        """

        # init
        moving_timestamp = timestamp
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT

        # enter campaign
        self.addEvent(moving_timestamp, 444, 1285)
        moving_timestamp += self.LONGER_WAIT

        # hit collect 5 times
        for _ in range(5):
            self.addEvent(moving_timestamp, 822, 880)
            moving_timestamp += self.DEFAULT_WAIT

        # open the item box
        self.addEvent(moving_timestamp, 814, 1365)
        moving_timestamp += self.LONGER_WAIT

        # hit claim
        self.addEvent(moving_timestamp, 457, 1091)
        moving_timestamp += self.DEFAULT_WAIT

        # go back to the front page
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT

        return moving_timestamp

    def getDormRewards(self, timestamp):
        # init
        moving_timestamp = timestamp
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT

        # go to campus
        self.addEvent(moving_timestamp, 113, 1297)
        moving_timestamp += self.LONGER_WAIT

        # go life tab
        self.addEvent(moving_timestamp, 660, 149)
        moving_timestamp += self.LONGER_WAIT

        # select Dorm
        self.addEvent(moving_timestamp, 668, 437)
        moving_timestamp += self.LONGER_WAIT

        # clicl claim
        self.addEvent(moving_timestamp, 142, 226)
        moving_timestamp += self.LONGER_WAIT

        # hit collect
        self.addEvent(moving_timestamp, 471, 973)
        moving_timestamp += self.LONGER_WAIT

        # hit return
        self.addEvent(moving_timestamp, 838, 55)
        moving_timestamp += self.LONGER_WAIT

        # go back to home page
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT
        return moving_timestamp

    def getExcursionRewards(self, timestamp):
        # init
        moving_timestamp = timestamp
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT

        # go to excursion
        self.addEvent(moving_timestamp, 840, 673)
        moving_timestamp += self.LONGER_WAIT

        # hit claim all
        for _ in range(2):
            self.addEvent(moving_timestamp, 144, 1450)

        # hit return *
        for _ in range(2):
            self.addEvent(moving_timestamp, 838, 55)
            moving_timestamp += self.DEFAULT_WAIT

        # re-init
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT
        return moving_timestamp

    def getFreeRegularCapus(self, timestamp):
        moving_timestamp = timestamp
        # init
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT

        # go to capus
        self.addEvent(moving_timestamp, 522, 1522)
        moving_timestamp += self.DEFAULT_WAIT

        # hit regular pull
        self.addEvent(moving_timestamp, 536, 398)
        moving_timestamp += self.LONGER_WAIT

        # hit OK
        self.addEvent(moving_timestamp, 181, 1025)
        moving_timestamp += self.LONGER_WAIT

        # return to homepage
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT
        return moving_timestamp

    def doOneJuniorLeagueBattle(self, timestamp):
        # init
        moving_timestamp = timestamp
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT

        # go to League
        self.addEvent(moving_timestamp, 800, 1300)
        moving_timestamp += self.DEFAULT_WAIT

        # go to League tab
        for _ in range(2):
            self.addEvent(moving_timestamp, 666, 152)
            moving_timestamp += self.DEFAULT_WAIT

        # go to Junior section
        self.addEvent(moving_timestamp, 455, 350)
        moving_timestamp += self.DEFAULT_WAIT

        self.addEvent(moving_timestamp, 463, 1326)  # hit fight
        moving_timestamp += self.LONGER_WAIT
        self.addEvent(moving_timestamp, 747, 952)  # pick the 3rd opponent
        moving_timestamp += self.LONGER_WAIT
        self.addEvent(moving_timestamp, 455, 924)  # confirm fight
        moving_timestamp += self.LONGER_WAIT
        for _ in range(2):
            self.addEvent(moving_timestamp, 817, 719)  # select reward
            moving_timestamp += self.LONGER_WAIT
        for _ in range(2):
            self.addEvent(moving_timestamp, 444, 1109)  # return *
            moving_timestamp += self.DEFAULT_WAIT
        for _ in range(2):  # back to homepage
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT
        return moving_timestamp

    def getQuizRewards(self, timestamp):
        # init
        moving_timestamp = timestamp
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT

        self.addEvent(moving_timestamp, 844, 430)  # open quiz
        moving_timestamp += self.LONGER_WAIT
        self.addEvent(moving_timestamp, 457, 1365)  # claim all
        moving_timestamp += self.LONGER_WAIT
        self.addEvent(moving_timestamp, 457, 1189)  # OK *
        moving_timestamp += self.LONGER_WAIT
        self.addEvent(moving_timestamp, 457, 1159)  # OK *
        moving_timestamp += self.LONGER_WAIT
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT
        return moving_timestamp

    def getAlchemyRewards(self, timestamp):
        # init
        moving_timestamp = timestamp
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT

        self.addEvent(moving_timestamp, 420, 48.5)  # hit alchemy +
        moving_timestamp += self.LONGER_WAIT
        self.addEvent(moving_timestamp, 275, 953)  # hit free
        moving_timestamp += self.LONGER_WAIT

        # go back to home page
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT
        return moving_timestamp

    def getAllMailRewards(self, timestamp):
        # init
        moving_timestamp = timestamp
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT

        self.addEvent(moving_timestamp, 838, 55)  # hit mail box
        moving_timestamp += self.LONGER_WAIT
        for _ in range(2):
            self.addEvent(moving_timestamp, 442, 1266)  # claim all
            moving_timestamp += self.LONGER_WAIT
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT
        return moving_timestamp

    def getFriendsRewards(self, timestamp, doCoop=True):
        # init
        moving_timestamp = timestamp
        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT

        self.addEvent(moving_timestamp, 828, 170)  # open friends
        moving_timestamp += self.LONGER_WAIT
        for _ in range(2):
            self.addEvent(moving_timestamp, 730, 544)  # cliam and send
            moving_timestamp += self.DEFAULT_WAIT

        if doCoop:
            self.addEvent(moving_timestamp, 744, 442)  # go coop
            moving_timestamp += self.DEFAULT_WAIT
            self.addEvent(moving_timestamp, 454, 1169)  # fight
            moving_timestamp += self.LONGER_WAIT
            self.addEvent(moving_timestamp, 457, 923)  # confirm fight
            moving_timestamp += self.LONGER_WAIT
            self.addEvent(moving_timestamp, 450, 1500)  # OK
            moving_timestamp += self.LONGER_WAIT

        for _ in range(2):
            self.addEvent(moving_timestamp, 54, 1558)
            moving_timestamp += self.DEFAULT_WAIT
        return moving_timestamp


def main():
    app = Solution()
    app.createHeader()

    cur = app.START_TIME  # by default = 1000 ms
    # start the app
    cur = app.openGame(cur)
    cur = app.getCampaignRewards(cur)
    cur = app.getDormRewards(cur)
    cur = app.getExcursionRewards(cur)
    cur = app.doOneJuniorLeagueBattle(cur)
    cur = app.getFreeRegularCapus(cur)
    cur = app.getQuizRewards(cur)
    cur = app.getAlchemyRewards(cur)
    cur = app.getAllMailRewards(cur)
    cur = app.getFriendsRewards(cur)
    app.closeAll(cur)
    app.createFooter(LoopInterval=(FOUR_HOURS - cur//1000))
    app.saveJson()


if __name__ == "__main__":
    main()

# data["people"].append(
#     {"name": "Scott", "website": "stackabuse.com", "from": "Nebraska"}
# )
# data["people"].append({"name": "Larry", "website": "google.com", "from": "Michigan"})
# data["people"].append({"name": "Tim", "website": "apple.com", "from": "Alabama"})

# # print(json.dumps(data, indent=4, sort_keys=True))

# with open("data.json", "w") as outfile:
#     outfile.write(json.dumps(data, indent=4, sort_keys=True))
