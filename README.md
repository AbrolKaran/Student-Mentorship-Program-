# SMP Mentor Selection Application

A fully responsive platform for the student mentorship programme at IIIT Delhi to nominate student mentors built using Python's Flask.


Table of contents
1. [About the project](#about-the-project)
    - [Built With](#built-with)
2. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)


## About the Project

Preview:


https://user-images.githubusercontent.com/59598251/177497211-af48dca1-7a32-42a3-9ef8-b12c872b06f0.mov


This project introduces an innovative approach for evaluation students that focuses on micro-expresssion monitoring and time-based evaluations in addition to response accuracy. 

Features:
- Login and Register to give a test
- Micro-expression monitoring based on 7 distinct human emotions. 
- Gradient scoring for questions
- Time based evaluations
- View Your scores immediately
- Uses SQLite for faster performance

Known Bugs:
- Nothing so far!

## Built With
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- Basic HTML and CSS

## Getting Started

### Prerequisites

- Python: [Python Installation](https://www.python.org/downloads/)
- Flask: [Flask installation](https://flask.palletsprojects.com/en/2.0.x/installation/)

## Installation


```bash
# clone this repo
$ git clone https://github.com/rsus4/Student-Mentorship-Program-

# go to the directory
$ cd Student-Mentorship-Program-

# use virtual env if you want
$ virtualenv ENV && source ENV/bin/activate

# generate static project
$ pip install -r requirements.txt

# export flask app and run
$ set FLASK_APP=main.py
$ flask run

# generate static project
$ npm run generate
```

Distributed under the MIT License. See LICENSE for more information.

## Contact

Name: Rishit Gupta - rishit19091@iiitd.ac.in
ProjectLink: https://github.com/rsus4/Student-Mentorship-Program-


