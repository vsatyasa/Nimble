## Author: Satya Sai Bharath Vemula (vsatyasa@purdue.edu)


## Description

This is the Submission for the inital screen-rounding from Nimble Robotics
This document explains on few aspects on how to navigate the code and run the experiments for checking the 


## Folder Structure

This section shows the folder structure and highlights the important file / folders with description

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

** This section how can the user run the server and client on the native machine / baremetal without any virtualization (ex: Docker )**

Firstly install all the dependencies in requirements.txt in Server/Client Folder 
*** Make sure  / cross check the version of the dependencies mentioned are rightly installed ***

_Running Server_

Navigate to Server folder and run

`python Server.py`

_Running Client_

`python Client.py`

This will display ball image on the client side and display the following log on the server side 

Current Coordinates: [312, 332] Client Coordinates: [317, 337] Error: 7.0710678118654755 <br>
Current Coordinates: [310, 330] Client Coordinates: [315, 334] Error: 6.4031242374328485 <br>
Current Coordinates: [308, 328] Client Coordinates: [312, 333] Error: 6.4031242374328485 <br>
Current Coordinates: [306, 326] Client Coordinates: [311, 330] Error: 6.4031242374328485 <br>
Current Coordinates: [304, 324] Client Coordinates: [309, 329] Error: 7.0710678118654755 <br>
Current Coordinates: [302, 322] Client Coordinates: [307, 327] Error: 7.0710678118654755 <br>

Which shows the current positions, detected position and error (Catesian Distance)


## Running in Docker




## Running the test cases.

Both Server and Client folder has test_<filename>.py which has few test cases.
The tests could directly be run run by running the command `python3 test_<filename>.py`

## References
