import statements
import functions3
import data
import db
from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash, jsonify

def get_total_user_productions(cursor, username):
    cursor.execute("""select productions.stype, sum(productions.value) from productions join cities on cities.cityname=productions.cityname  
	            where cities.username=%s  group by stype""",(username,))

    prd = cursor.fetchall()
    prdDict = data.sourcesDict
    for (stype, value) in prd:
        prdDict[stype] = value
    
    return prdDict


def user_inform(cursor, username):    
    limitsDct = statements.get_user_source_limits(cursor, username)
    userSources = statements.get_sources_of_user(cursor, username)
    cities = statements.get_cities_of_user(cursor, username)
    total_production = get_total_user_productions(cursor, username)
    resDict = {"limitsDct": limitsDct, "userSources": userSources, "cities": cities, "total_production": total_production}
    return resDict
            # for (stype, value)        

#####NOT FINISHED FUNCTION 

    # print("total: ", total_production)
    # resDict = {"limitsDct": jsonify(limitsDct), 
    # "userSources": jsonify(userSources),
    #  "cities": jsonify(cities), 
    #  "total_production": jsonify(total_production)}