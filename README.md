# VScouterPit
<img src="https://github.com/VihaanChhabria/VScouter/blob/main/website/public/VScouterLogo.png" alt="drawing" width="40%"/>

##  Overview

VScouterPit is a pit scouting app designed for FRC teams to efficiently collect and view data on competing robots. Built using [KoboToolbox](https://www.kobotoolbox.org/), the app allows teams to gather  information about robot design, mechanisms, and capabilities directly in the pits.

To enhance accessibility, the GitHub repository includes modifications that enable offline functionality, ensuring that data can be collected and stored even without an internet connection. Additionally, the repository provides a data viewer, allowing teams to easily analyze and reference collected scouting data during competitions.

VScouterPit is designed to be a lightweight, user-friendly, and adaptable solution for FRC teams looking to optimize their pit scouting process.

##  Features

- Pit Scouting Form – Structured survey to collect key robot details (drivetrain, scoring mechanisms, strategy, etc.).
- Offline Functionality – Modified KoboToolbox setup allows data collection without internet access.
- Data Viewer – Easily browse and analyze collected scouting data.
- Export & Backup – Store and retrieve scouting data as needed.

## Prerequisites

Before getting started with VScouterPit, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python
- **Operating System:** Windows

## The Process

Before you start scouting you need the form made. See this section for more info. Using this app, the process is to allow your scouts to collect data in the pits and then intruct them to go to an area with internet. Once this is completed, you will have the data online. You would then download this data and run the parsing python file as described in this section. Lastly when you want to use the data, you can use the visulizer python code as described in this section.
  
## Designing Your UI

**this version does not yet have support for custimizability.**

As this project uses KoboToolbox as its UI, you have to make a form and custimize it to your needs.

The way KoboToolbox works is that the data is collected on an individuals device and then stored until internet is available. Once connnected to the internet, it will push its data to the KoboToolbox serves.

Some suggestions on what to scout can be the scouters name, the team their are scouting, a picture of their robot, drivetrain, weight, scoring abilities, or how many auto combinations they are able to have. Make an account on [KoboToolbox](https://www.kobotoolbox.org/) and create a form. For reference find our implementation [here](https://vscouter-pit.netlify.app/).

## Parsing data

To ensure that you are able to access images in any enviroment (like you having no internet), you need to parse and download the images the scouts take. First put your data in the  data/pit_data folder. You can put as many files of data in the folder. If a team is scouted more than once, the program automatically joins them together.

To do this you first need to run the main.py file in the parsing directory to generate the .env file where you can put your credentials:
1. `cd parsing`
2. `python main.py`

This will generate a .env file inside of the parsing folder with the following contents:
``
USERNAME = your_username_here
PASSWORD = your_password_here
``
Fill in your credentials here like this:
``
USERNAME = thisismyuser
PASSWORD = password123
``

Now you need to run the code again to download the pictures onto your device:
1. `cd parsing`
2. `python main.py`

This will download the pictures in the data/robot_images folder.

## Viewing Data

Before viewing data look at parsing your data to use it offline. Once this is done, to run the visulization code do the following:
1. `cd viewer`
2. `python main.py`

This will start a TKinter python application where you can enter the team you want data on.

![image](https://github.com/user-attachments/assets/e37a932b-95b6-4441-a6e0-33b9fa065171)
