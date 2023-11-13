class Bid:
    def __init__(self, amount, Item, userID, userName, auctionID):
        self.amount = amount
        self.Item = Item
        self.userID = userID
        self.userName = userName
        self.auctionID = auctionID

    def getAmount(self):
        return self.amount
    
    def getItem(self):
        return self.Item
    
    def getUserID(self):
        return self.userID
    
    def getUserName(self):
        return self.userName
    
    def getAuctionID(self):
        return self.auctionID
    
    def setAmount(self, amount): 
        self.amount = amount

    def setItem(self, Item): 
        self.Item = Item

    def setUserID(self, userID): 
        self.userID = userID

    def setUserName(self, userName): 
        self.userName = userName

    def setAuctionID(self, auctionID): 
        self.auctionID = auctionID