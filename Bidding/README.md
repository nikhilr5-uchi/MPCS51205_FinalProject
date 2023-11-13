---
status: accepted
date: {2023-11-12}
deciders: {Summer Long, James Long, Jaswitha Reddy, Christian Urbanek, Torres
Shi, Nikhil Richard}
consulted: {Alan Salkanovic, John Hadidian-Baugher}
informed: {Summer Long, James Long, Jaswitha Reddy, Christian Urbanek, Torres
Shi, Nikhil Richard, Alan Salkanovic, John Hadidian-Baugher, Mark Shacklette}
---

# ADR 1: Implementation Choice for University of Chicago
## Context and Problem Statement
In order to implement factors of conveinence such as dormitory pick-up and
filtering, it is necessary to contextualize our implementation to a particular school.
So, which one?
## Decision Drivers
* In order to make our auction site stand-out, we need to have more specialized
features
* Specialization of features requires knowledge of campus and neighborhood that
isn't easily gleamed online
* Different needs of the users of the auction site - geared towards late teens/20s
demographic
## Considered Options
* University of Chicago
## Decision Outcome
Chosen option: "University of Chicago", because it is the school we have the most
knowledge of as a team.
### Consequences
* Good, because it simplifies the amount of outside research required, allowing
more time for creating the services themselves
* Bad, because it could encourage hard coding of options instead of utilizing other
methods such as scraping that would encourage expandability later
* Bad, narrow scope - uchicago can be vastly different compared to other
campuses

### Confirmation
Compliance of this ADR will be ensured through mutual accountability and
continued communication as a team.
## More Information
This decision is a child decision of ADR 0, as it is focusing on one particular school
in our implementation of a Higher Education auction site.
