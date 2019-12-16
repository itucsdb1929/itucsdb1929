def get_column(cursor, tablename, keyname, key, column):
    cursor.execute("""
        select %s from %s
        where %s=%s
        """(column, tablename, keyname, key))
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
    UPDATE %s		
    SET %s = %s		
    WHERE(%s = %s)		
    """, (tablename, column, value, keyname, key))

def delete_row(cursor, tablename, keyname, key):
    cursor.execute("""		
    DELETE from %s		
    WHERE(%s = %s)		
    """, (tablename, column, value, keyname, key))


def initializer(cursor,tablename, key):		
    cursor.execute("""		
        INSERT INTO %s values(		
        %s,		
        0		
        0		
        0		
        0		
        0		
        )		
        """,(tablename, key))		