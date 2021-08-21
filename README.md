# GxB_BlueStack_automation

Using python to generate json marco script for Blue Stack to execute for game GxB2

## Goal

Create a stable method to create and maintain auto marco of BlueStack5 for GxB game. (This method can be shared by any other apps running on BlueStack simulator.)

## Challenges

- (maintainance need) The game UI gets updated frequently
- (easy-to-regenerate) Mannual record has to be perfect in one run, you also need to make sure it covers different situations and responses
- (scale-up need) New functionalities frequently added

## Install

No specific package install required. All library used in this code is python standard.

## Usage

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
