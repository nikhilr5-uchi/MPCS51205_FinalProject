# ADR: AuctionWindow Microservice Implementation

## Context
* Manages item details, expiration, offers, and other aspects crucial to the auction process.

## Decision Drivers
* The microservice must efficiently handle the listing of items, including setting starting bids, expiration dates, and managing auction offers.
* The system should keep track of important item details provided by the seller, such as age, condition, and description.
* Users (sellers) should have the option to set a "Buy Now" price for their items, allowing for an immediate sale without going through the bidding process.
* Users can set a location for item pickup, and sellers can choose to meet at an agreed-upon location on campus.
* The item microservice will have functionality that will make sure a bid is valid.
    - The offer is greater than starting_bid, user offering is a student, etc
* Will keep track of expiration of item
    - Other microservices will pull data from item to see when it expires in order to priortize the items
* The microservice will parse of the description for filter
    - Other services will use the function to parse of the description and figure out how to filter item and place in correct categories

## Status
* Accepted

## Confirmation
Compliance of this ADR will be ensured through mutual accountability and continued communication as a team.
