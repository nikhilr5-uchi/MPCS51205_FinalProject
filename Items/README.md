#ADR for Items microservice

#Decisions

1. Planning to have an item microservice that tracks everything about an item

2. The item microservice will have functionality that will make sure a bid is valid
    - The offer is greater than starting_bid, user offering is a student, etc

3. Will keep track of expiration of item
    - Other microservices will pull data from item to see when it expires in order to priortize the items

4. The microservice will parse of the description for filter
    - Other services will use the function to parse of the description and figure out how to filter item and place in correct categories