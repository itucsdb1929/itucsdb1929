def get_column(cursor, tablename, keyname, key, column):
    cursor.execute("""
        select """+ column+ """ from """+ tablename + """
        where """+ keyname +"""=%s
        """ , (key, ))
    column = cursor.fetchone()
    column = column[0]
    return column

def update_column(cursor, 
                tablename, 
                keyname, 
                key, 
                column, 
                value):		
    cursor.execute("""		
    UPDATE """+ tablename + """	
    SET """+ column+ """= %s		
    WHERE("""+ keyname +""" = %s)		
    """ , (value, key))

def delete_row(cursor, tablename, keyname, key):
    cursor.execute("""		
    DELETE from """+ tablename + """			
    WHERE( """+ keyname +""" = %s)		
    """ , (key,))


def initializer(cursor,tablename, key):		
    cursor.execute("""		
        INSERT INTO """+ tablename + """ values(		
        %s,		
        0,		
        0,		
        0,		
        0,		
        0		
        )		
        """ , (key,))		