# Third Eye
SDSLabs Internal Hackathon - September 2022

## About

This is a ML-based Flask web application which analyses how attentive the participants are in a Google Meet and comes with a visual interface which shows each participant's inattentiveness over the whole meet period as well as the inattentiveness of all the participants as a whole over time.

## Setup / Installation

- Clone this repository this cd into it.
- Install all required dependencies using the following steps:

  - If you are on Linux OS follow the following steps:
    Firstly, remove matplotlib==3.6.0 from requirements.txt. After that, try to install it using `sudo apt-get install python-matplotlib`
    Then execute the following command in your terminal:
    ```Bash
    pip3 install -r requirements.txt
    ```
  - If you are on Windows, follow the following steps:
    ```powershell
    python -m pip install -U pip setuptools
    python -m pip install matplotlib
    ```

- Start your development server by executing the following command into the terminal: `python server.py` or `python3 server.py`.
- Load up your browser and go to `https://localhost:5000` where your server has been set-up

## Usage

You fill land on the main page where you can start the Analysis

Run:
   On clicking the button, the Model which calculates the attentiveness and the negligience of all participants will start.
   Head towards your Google Meet Tab, and continue the meet.
   When you are about to stop the meeting, just press "<kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>L</kbd>" to stop the script from running. The page will redirect to show the results!


## Contributors

- [Shreya Bhagat](https://github.com/yashre-bh)
- [Parth Mittal](https://github.com/parth-nebula)
- [Pradnya Shimpi](https://github.com/Pradnya2203)
- [Avnish Chauhan](https://github.com/LunaticFrisbee)
