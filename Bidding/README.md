# ADR: Bidding Microservice Implementation

## Context
* A large piece of functionaity in the auction site is placing bidding. 
* This is arguably the most crucial user interaction, as they are spening their real money and bids can be very time-sensitive.
* As such, we need to make a relatively simple yet effective approach to coding a microservice that handles this task.

## Decision Drivers
* We know that this microservice will connect to the front end, as well as that it needs to have its own data store.
* We need to have a bid data object that is stored in some data format. This is then used to catalog information in a data store.
* We also need this program to be able to run as a backend functionality to our frontend service, since end goal of the product we are making is to be a webiste
feature.

## Status
* Accepted
easier to use.

### Confirmation
Compliance of this ADR will be ensured through mutual accountability and
continued communication as a team.
