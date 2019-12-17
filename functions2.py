import statements
import functions3
import data
import db
from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash, jsonify

def get_total_user_productions(cursor, username):
    cursor.execute("""select wood, stone, metal, food, population from userproductions 
	            where username=%s""",(username,))

    prd = cursor.fetchone()
    prdDict = data.sourcesDict.copy()
    if prd==None:
        return prdDict

    prdDict["wood"] = prd[0]
    prdDict["stone"] = prd[1]
    prdDict["metal"] = prd[2]
    prdDict["food"] = prd[3]
    prdDict["population"] = prd[4]

    
    return prdDict

#####TODO
def user_inform(cursor, username):    
    limitsDct = statements.get_user_source_limits(cursor, username)
    userSources = statements.get_sources_of_user(cursor, username)
    cities = statements.get_cities_of_user(cursor, username)
    userproductions = get_user_productions(cursor, username)
    resDict = {"limitsDct": limitsDct, "userSources": userSources, "cities": cities, "userproductions": userproductions}
    return resDict
            # for (stype, value)        
