---
date: {2023-11-12}
deciders: {Summer Long, James Long, Jaswitha Reddy, Christian Urbanek, Torres
Shi, Nikhil Richard}
consulted: {Alan Salkanovic, John Hadidian-Baugher}
informed: {Summer Long, James Long, Jaswitha Reddy, Christian Urbanek, Torres
Shi, Nikhil Richard, Alan Salkanovic, John Hadidian-Baugher, Mark Shacklette}
---

# How to start Up Site In Order

## 1. Start MongoDB

#### Start Server 
`mongosh`

#### Create Users 

> use users
switched to db users
> db.createUser({
...   user: "appUser",
...   pwd: "appPassword",
...   roles: ["readWrite"]
... })

## 2. Start MySql

#### Start server
mysql -u root -p
enter password for root (may be local machine's password)
execute commands in mysql terminal:

#### Change Perms
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
mysql> FLUSH PRIVILEGES;

#### Create Database and Tables

mysql> CREATE DATABASE IF NOT EXISTS auction_site;

mysql> CREATE TABLE IF NOT EXISTS bid (
        id INT AUTO_INCREMENT PRIMARY KEY,
        bid_amount INT
      );

mysql> CREATE TABLE IF NOT EXISTS listing (
        id INT AUTO_INCREMENT PRIMARY KEY,
        userID INT,
        product_title varchar(64),
        imageName     varchar(64),
        min_bid         float,
        expiration_date datetime,
        location        varchar(64),
        description     varchar(255),
        buy_now_enabled bit,
        buy_now_price   float
      );

## 3. Start RabbitMQ Server

If container is not running then ` docker run -d --hostname my-wabbit --name MyWabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management `

Now ` python rpcConsumer.py `
This is to have the server start consuming data to communicated when items are being added

## 4. Add Test Data

Create a script to add test data under different user
` python inserttestdata.py `

## 5. Start Flask app
run
`export FLASK_APP=UserAccount`
then
 `flask run`


# ADR: Auction Site Implementation

## Context
* The Auction Site Implementation ADR outlines the key decisions made regarding the technology stack for developing the Auction Site modeled on eBay.

## Decision Drivers
* The programming language should be easily readable among team members to facilitate collaboration and understanding of the codebase.
* The chosen backend technology should seamlessly connect with frontend services and support Web API calls.
* The data format chosen should be intuitive, compatible with the programming language, and facilitate efficient data processing.
* The selected data storage solution should be easy to set up in the chosen programming environment and meet the project's requirements.
* The overall technology stack should offer ease of implementation, balancing simplicity with functionality to meet project goals.

## Considered Options
* Flask for backend API functionality
* MongoDB for data storage
* MySQL for data storage
* Python as the programming language
* JSON as the data format
* HTML, CSS, and JavaScript for frontend integration

## Decision Outcome
* We chose Python using Flask (since they go hand in hand).
* We chose JSON as the data format.
* We chose MongoDB over MySQL, since it was more intuitive to set up in the Python environment.
* We chose HTML, CSS, and Javascript for frontend development as they provide a good solid foundation.

## Status
* Accepted

## Consequences
* Python makes it so that our programming is easily readable among different group members. We all understand the language and it is very readable.
* Flask is the best option for creating backend services that connect to frontend and Web API calls.
* JSON is also a good outcome here because it is the most intuitive of the data formats as well. It works really well with Python.
* The data store is a bit more convoluted in decision. We now are locked into unordered data storage as opposed to a relational database, which could make the data more cluttered and convoluted.
* Overall, we found that the ease of implementing MongoDB in Python made it easier to use.

## Confirmation
Compliance of this ADR will be ensured through mutual accountability and
continued communication as a team.


## Start up

#### Start up rabbitmq server
` docker run -d --hostname my-wabbit --name MyWabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management `

#### Run home page
` python auctionwindow.py `

#### Test Sending Item
` python item.py `
Make sure dependenices installed

#### Refresh page
