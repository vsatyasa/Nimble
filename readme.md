## Author: Satya Sai Bharath Vemula (vsatyasa@purdue.edu)


## Description

This is the Submission for the inital screen-rounding from Nimble Robotics
This document explains on few aspects on how to navigate the code and run the experiments for checking the 


## Folder Structure



├─ Client **(This Folder Contains all the relevant files to the client)** <br>
│   ├── BallDetector.py <br>
│   ├── BallRecvTrack.py <br>
│   ├── Config.py <br>
│   ├── Dockerfile <br>
│   ├── Utils.py <br>
│   ├── client.py **(This file is the start point to the client)** <br>
│   ├── requirements.txt <br>
│   └── test_BallDetector.py <br>
├─ Server **(This Folder Contains all the relevant files to the Server)** <br>
│   ├── BallGenerator.py <br>
│   ├── Config.py <br>
│   ├── Dockerfile <br>
│   ├── MovingBallTrack.py <br>
│   ├── Utils.py <br>
│   ├── requirements.txt <br>
│   ├── server.py **(This file is the start point to the server)** <br>
│   └── test_BallGenerator.py <br>
├─ build_images.sh **(This file creates the docker images for client and server)** <br>
├─ manifest.yaml  **(This file for kubernetes deployment)** <br>
└─ readme.md <br>


## Running Natively


## Running in Docker


## Running in Kubernetes


## Running the test cases.

Both Server and Client folder has test_<filename>.py which has few test cases.
The tests could directly be run run by running the command `python3 test_<filename>.py`

## References
