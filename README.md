Updated November 11th, 2022

# Introduction

The aim of the extension we are building is to provide information on 3 different types of  metrics whenever we visit a webpage which will aid us in network monitoring and troubleshooting.  

The extension application is divided as so:  

* User interface in the form of a pop-up 
* Manifest file called manifest.json that is used by extensions in order to start properly
* Main script file that handles the calls to the different APIs (Chrome APIs, Network  Information API, Performance Navigation Timing, etc.) and retrieves the necessary  information 
* Server script to communicate with the extension as well as the MongoDB database 

# Getting Started

1. Run **npm install** to install the necessary librairies and dependencies
2. Run **npm start** to run the server
3. Run **python automation.py _your url.txt file_** to start the automation process of going through the list of websites of your choosing 
