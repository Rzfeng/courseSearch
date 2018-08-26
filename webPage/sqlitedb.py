import web

db = web.database(dbn='sqlite',
        db='CourseBase'
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
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


# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################




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
