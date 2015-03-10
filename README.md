# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This project is a web-application around Tellstick and enables some controls over devices.
JARVIS aims to be the central nerve in all communication with Tellstick

### Multiple hubs
If you want to use one hub as a frontend and another as a backend use the setting
MAIN_HUB_URL on the frontend-hub.
This can be useful if you want to have a hub in the cloud and one on-site. in that way the cloud-hub
can communicate with the on-site hub. To achieve communication you can set up a SSH-tunnel like so:
(from your local, on-site, machine)
$ ssh -R 9999:localhost:80 remote-machine

Then set the MAIN_HUB_URL to go through your tunnel at 9999
MAIN_HUB_URL = "http://localhost:9999/api/"

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
Run runtests.sh

* Deployment instructions


### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact
