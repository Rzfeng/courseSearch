import web

db = web.database(dbn='sqlite',
        db='CourseBase'
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#     t.rollback()
#     print str(e)
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    # TODO: update the query string to match
    # the correct column and table name in your database

    #FINISHED TODO
    query_string = 'select Time from CurrentTime'
    results = query(query_string)
    # alternatively: return results[0]['currenttime']
    return results[0].Time # TODO: update this as well to match the
                                  # column name

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    try:
        query_string = 'select * from Items where ItemID = $itemID'
        result = query(query_string, {'itemID': item_id})
    except Exception as e:
        print str(e) #ask TA whether we print or return None
        return None
    else:
        return result[0]

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time


#def updateBid(item_id, price):


#def winBid

def getBidsByID(item_id):
    try:
        query_string = 'select UserID, Amount, Time from Bids where ItemID = $itemID'
        result = query(query_string, {'itemID': item_id})
    except Exception as e:
        print str(e)
        return None
    else:
        return result[0]


def getUserById(user_id):
    try:
        queryString = 'select * from Users where UserID = $userID'
        result = query(queryString, {'userID': user_id})
    except Exception as e:
        print str(e)
        return None
    else:
        return result[0]


def updateTime(current_time):
    query_string = 'update CurrentTime set Time = $time'
    t = db.transaction()
    try:
        db.query(query_string, {'time': current_time})
    except Exception as e:
        t.rollback()
        print str(e)
    else:
        t.commit()





def getCourseInfo(subject = '', courseID = '', sectionID = '', year = ''):
    base_query = 'SELECT * FROM Courses '
    query_string = 'SELECT * FROM Courses WHERE'

    #User is search the whole course database
    if (subject == '' and courseID == '' and sectionID == '' and year == ''):
        query_string = base_query
        return query(query_string)

    if subject != '':
        query_string = base_query + 'WHERE Subject = $_subject_'


    if courseID != '':
        if subject != '':
            query_string = query_string + ' AND CourseID = $_courseID_'
        else:
            query_string = query_string + ' CourseID = $_courseID_'

    if sectionID != '':
        if subject != '' or courseID != '':
            query_string = query_string + ' AND SectionID = $_sectionID_'
        else:
            query_string = query_string + ' SectionID = $_sectionID_'

    if year != '':
        if subject != '' or courseID != '' or sectionID != '':
            query_string = query_string + ' AND Year = $_year_'
        else:
            query_string = query_string + ' Year = $_year_'


    return query(query_string, {'_subject_': subject, '_courseID_': courseID, '_sectionID_': sectionID, '_year_': year})





def getAllItems(itemID = '', userID = '', category = '', description = '', minPrice = '', maxPrice = '', status = '', current_time = ''):
    base_query = 'SELECT * FROM Items '

    query_string = 'SELECT * FROM Items WHERE'

    #If they search the whole Items Table
    if (itemID == '' and category == '' and description == '' and minPrice == '' and maxPrice == '' and status == ''):
        query_string = base_query
        #print query_string

    if itemID != '':
        query_string = base_query + 'WHERE ItemID = $_itemID_'
        #print query_string

    if userID != '':
    	if itemID != '':
    		query_string = query_string + ' AND Seller_UserID = $_userID_'
    	else:
    		query_string = query_string + ' Seller_UserID = $_userID_'


    #do we need to use "like" for category? i.e. should category be an exact match
    if category != '':
        if itemID != '' or userID != '':
            query_string = query_string +  ' AND ItemID in (select ItemID from Categories where Category = $_category_)'
            #print query_string
        else:
            query_string = query_string + ' ItemID in (select ItemID from Categories where Category = $_category_)'
            #print query_string

    if description != '':
        if itemID != '' or category != '' or userID != '':
            query_string = query_string + ' AND Description LIKE \'% _description_ %\''
            #print query_string
        else:
            query_string = query_string + ' Description LIKE \'% _description_%\''
            #print query_string

    if minPrice != '':
    	if itemID != '' or category != '' or userID != '' or description != '':
    		query_string = query_string + ' AND Currently >= $_minPrice_'
    	else:
    		query_string = query_string + ' Currently >= $_minPrice_'

    if maxPrice != '':
    	if itemID != '' or category != '' or userID != '' or description != '' or minPrice != '':
    		query_string = query_string + ' AND Currently <= $_maxPrice_'
    	else:
    		query_string = query_string + ' Currently <= $_maxPrice_'


    if status != '':
    	if status == 'open':
    		if itemID != '' or category != '' or userID != '' or description != '' or minPrice != '' or maxPrice != '':
    			query_string = query_string + ' AND Ends >= $_current_time_ AND Started <= $_current_time_ and (Buy_Price is NULL or Currently is NULL or Buy_Price > Currently)'
    		else:
    			query_string = query_string + ' Ends >= $_current_time_ AND Started <= $_current_time_ and (Buy_Price is NULL or Currently is NULL or Buy_Price > Currently)'
    	if status == 'close':
    		if itemID != '' or category != '' or userID != '' or description != '' or minPrice != '' or maxPrice != '':
    			query_string = query_string + ' AND (Ends < $_current_time_ OR (Ends == $_current_time_ and Buy_Price IS NOT NULL AND Currently IS NOT NULL AND Buy_Price <= Currently))'
    		else:
    			query_string = query_string + ' (Ends < $_current_time_ OR (Ends == $_current_time_ and Buy_Price IS NOT NULL AND Currently IS NOT NULL AND Buy_Price <= Currently))'

    	if status == 'notStarted':
    		if itemID != '' or category != '' or userID != '' or description != '' or minPrice != '' or maxPrice != '':
    			query_string = query_string + ' AND $_current_time_ < Started'
    		else:
    			query_string = query_string + ' $_current_time_ < Started'

      	if status == 'all':
    		query_string = query_string

    return query(query_string, {'_itemID_': itemID, '_userID_': userID, '_category_': category, '_description_': description, '_minPrice_': minPrice, '_maxPrice_': maxPrice, '_status_': status, '_current_time_': current_time })
