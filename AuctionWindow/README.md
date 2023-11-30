# ADR: AuctionWindow Microservice Implementation

## Context
* Manages the scheduling, status, and details of auctions on the platform.

## Decision Drivers
* Sellers should be able to schedule auctions with specific start and end times, and the system must accurately reflect the status of ongoing auctions.
* The microservice should handle bid increments, maintain the current highest bid, and update auction status accordingly.
* Seamless integration with other microservices, such as Items and Notifications, is crucial for a cohesive user experience.

## Status
* Accepted

## Consequences
* The microservice accurately manages auction schedules and reflects real-time status changes.
* Efficient bid management ensures a fair bidding process, contributing to the overall success of the auction feature.

## Confirmation
Compliance of this ADR will be ensured through mutual accountability and continued communication as a team.
