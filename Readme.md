#Project Plan for Gaming Platform
## Client-Server Overview
We will be creating a client-server game platform. We will follow a Model-View-Controller (MVC/MTV) pattern in Django for developing the server side. The key components in this system will be:
  * Database: We will store relevant raw data/information about our users and our developers in a database.
  * Backend Server: The server will be implemented in Django. It will access the database for raw data and communicate with the client for sending and receiving data requests/responses.

##Features
All the mandatory functions such as basic player functionalities and developer functionalities listed in WSD Project Description will be implemented. Furthermore, we are planning to implement following features to our game platform:
1. Save/Load feature
2. Third party login
3. A JavaScript game similar to Diamond Dash
4. RESTful API
5. Mobile friendly
6. Social media sharing

###Extra features
We will add graphical statistics like charts to developers’ panel for demonstration of sales over time.

##Implementation plan
###DataBase Schema

![alt text][mtv]
[mtv]: (db.jpg)

###Project Management
- we will meet each other regularly. In addition, we will use Google drive as an online collaboration tool to communicate with each other. Our estimated group workload time is 20 hours in total and the individual workload time for each member is nearly 14 hours weekly for a month. 
- We will break down the tasks to seperated parts, but we have not decided yet how to do that exactly

#Final Submission
##names and student IDs
- Navid Shamsizadeh (466929)
- Ligia Gaspar (464507)

##What features you implemented and how much points you would like to give to yourself from those?
- We almost implemented all of the mandatory functions including for example e-mail validation, search options, and etc.
 In addition, we prepared a game, we did save/load feature, and responsive design and a documentation which is in the
 'static' folder. Also we have a backlog of what we did individually, and it is in an excel file in static folder.
 Navid: I think that we should get major points of what we implemented, since they are working good and well designed.
And we had many problems with the whole concept of django, and that's why one of our teammates couldn't contribute
to the project. The hardest part about this project is the group management, because we are students coming from
different backgrounds and it is not a good idea to the a hard project like this in a group. I think it would be better
to do a smaller or even equal project individually.

##How you divided the work between the team members - who did what?
First we decided to meet in early January to divide the work and come up with a single viewpoint of the project. Then
we decided to start working on features that we can do. The detailed work break is included in a spreadsheet file in
static folder.

##Instructions how to use your application and link to Heroku where it is deployed.
Link: http://peaceful-cliffs-8403.herokuapp.com/
-we have an admin:
    username:'admin'
    password:ASK ME
-so it is very simple, you just need to login to the system by clicking on 'Hello Guest'. In order to make a new user
whether Player or a Developer you need to provide the system with an email which you should also validate.
Based on the type of user you can do different things as mentioned in project description.














