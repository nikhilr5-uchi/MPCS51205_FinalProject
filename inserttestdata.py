

def add_to_auction(body):
    item_dict = json.loads(body)
    data = item_dict
    print("DATAAA: ", data)
    insert_stmt = (
        "INSERT INTO listing (userID, product_title, imageName, min_bid, expiration_date, location, description, buy_now_enabled, buy_now_price) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    userId = int(data['user'])
    min_bid = float(data['starting_bid'])
    sqlValues = (userId, data['title'], data['filenameImg'], min_bid, datetime.date(2012, 3, 23) ,data['location'], data['descriptions'], True, 15)
    mycursor.execute(insert_stmt, sqlValues)
    mydb.commit()

if __name__ == '__main__':
    start_consumer_queue()