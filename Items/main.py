class Item:
    def __init__(self, user, title, expiration, starting_bid, location, description):
    self.user = name
    self.title = title
    self.expiration = expiration
    self.starting_bid = starting_bid
    self.location = location
    self.descriptions = description

    # if price is high enough to add
    def IsOfferAllowed(self, priceOffer):
        return priceOffer > self.starting_bid

    def GetLocation(self):
        return self.location
    
    def SplitDescriptions(self):
        for (dsc in self.descriptions):
            AddAsFilter(dsc)

    def AddAsFilter(self):
        #to handle description and parse into filterable items
        pass