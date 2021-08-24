# GxB_BlueStack_automation

Using python to generate json marco script for Blue Stack to execute for game GxB2

## Goal

Create a stable method to create and maintain auto marco of BlueStack5 for GxB game. (This method can be shared by any other apps running on BlueStack simulator.)

## Update Logs

-v1.0 can performing basic functions as campaign collect, excursion collect, dorm collect, etc.
-v1.1 taking refactor suggestion from kekw#0204

## Challenges

- (maintainance need) The game UI gets updated frequently
- (easy-to-regenerate) Mannual record has to be perfect in one run, you also need to make sure it covers different situations and responses
- (scale-up need) New functionalities frequently added

## Install

No specific package install required. All library used in this code is python standard.

## Usage

You can use the `DailyTask_v3.json` directly (by importing it into your marco manager.)

OR:

1. Clone this repo (make sure you have `git` in your terminal)

```bash
git clone https://github.com/tobyatgithub/GxB_BlueStack_automation.git
cd GxB_BlueStack_automation
```

2. Generate the json marco script

```bash
python jsonGenerator.py
```

3. The default result will be called `data.json` in the same folder. You can import this script directly as a marco in BlueStacks:
   -> open marco manager -> import -> select this json file

## Parameters

Right now the script is set to run every 4 hours (the whole script shall take about 4-5 mins).  
Each time, it will open the game, do all the collects, and close the game.  
TODO: more about the detailed parameters and how to change it.
