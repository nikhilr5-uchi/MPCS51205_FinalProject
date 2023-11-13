---
date: {2023-11-12}
deciders: {Summer Long, James Long, Jaswitha Reddy, Christian Urbanek, Torres
Shi, Nikhil Richard}
consulted: {Alan Salkanovic, John Hadidian-Baugher}
informed: {Summer Long, James Long, Jaswitha Reddy, Christian Urbanek, Torres
Shi, Nikhil Richard, Alan Salkanovic, John Hadidian-Baugher, Mark Shacklette}
---

# ADR: Auction Site Implementation

## Context


## Decision Drivers


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

### Confirmation
Compliance of this ADR will be ensured through mutual accountability and
continued communication as a team.
