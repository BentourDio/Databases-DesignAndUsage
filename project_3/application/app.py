#Askhsh 2 SXBD 
# Dionysios Bentour (11151300115) and Anna Gogoula (1115201800305)

# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
from warnings import catch_warnings
import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db
import random

def connection():
    ''' User this function to create your connections '''
    con = db.connect(host=settings.mysql_host, 
        user=settings.mysql_user, 
        password=settings.mysql_passwd, 
        database=settings.mysql_schema)
    
    return con

def findAirlinebyAge(x,y):
    
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()


    sql = """SELECT distinct passengers.id FROM passengers, flights_has_passengers 
            WHERE passengers.id = flights_has_passengers.passengers_id 
                AND 2022- passengers.year_of_birth < %s AND 2022- passengers.year_of_birth > %s """ % (x,y)

    cur.execute(sql)
    passengersID= cur.fetchall()

    # I have the distinct passengers in passengersID tuple. Now for every passenger
    # I will find the airline he used and all those airlines in a single tuple (duplicates will be involved)
    
    flag = 0
    airlinesName_add = () # this tuple will have all the occurences of airlines which
    
    # have a passenger of this age group
    for row in passengersID:
        
        sql = """SELECT airlines.name FROM airlines, flights, routes, flights_has_passengers
                WHERE flights_has_passengers.passengers_id = %s AND flights_has_passengers.flights_id = flights.id
                    AND flights.routes_id = routes.id AND routes.airlines_id = airlines.id""" % (row[0])

        cur.execute(sql)
        airlinesName = cur.fetchall()
        airlinesName_add = airlinesName_add + airlinesName

    # printing the whole tuple
    count=0

    # for row in airlinesName_add:
    #     airname = row[0]
    #     print("airline's Name: %s" % (airname))
    #     count = count + 1
    # print("the count is %d"%(count))

    airlinesName_List = list(airlinesName_add) # convert the tuple to a list to be able to modify it

    count_temp = 0; # temporary counter
    count_final = 0; # final counter
    count = 0
    airline_final = ""
    while airlinesName_List:
        # iterate the list, count the occurence of an airline and then remove all instances of that airline
        count_temp = airlinesName_List.count(airlinesName_List[0])
        if count_temp > count_final:
            count_final = count_temp
            airline_final = airlinesName_List[0]        
        airlinesName_List = list(filter(airlinesName_List[0].__ne__, airlinesName_List))
        count = count + 1
        
    
    sql = """SELECT airlines_has_airplanes.airplanes_id FROM airlines, airlines_has_airplanes 
            WHERE airlines.name = '%s' AND airlines.id = airlines_has_airplanes.airlines_id""" % (airline_final)
    
    cur.execute(sql)
    airplanes_count = cur.fetchall()

    # print("Final Airline =%s with [%d] passengers of that age group with AirplaneCount =%d" % (airline_final,count_final,(len(airplanes_count))))
    con.close()

    return [("airline_name","num_of_passengers", "num_of_aircrafts",) ,(airline_final[0], str(count_final) , str(len(airplanes_count)),) ]


def findAirportVisitors(x,a,b):
    
   # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    sql = """SELECT airports.name, count(passengers.id)
            FROM passengers, flights_has_passengers, flights,
                routes, airports, airlines
            WHERE passengers.id = flights_has_passengers.passengers_id 
                AND flights_has_passengers.flights_id = flights.id 
                AND flights.date >= '%s' AND flights.date <= '%s' 
                AND flights.routes_id = routes.id AND routes.destination_id = airports.id 
                AND routes.airlines_id = airlines.id AND airlines.name = "%s"
            GROUP BY airports.name;""" % (a,b,x)
    
    cur.execute(sql)
    query = cur.fetchall()
    # for row in query:
    #     airportName = row[0]
    #     visitsCount = row[1]
    #     print("Airport:{:<30} Count={:<30}" .format(airportName,visitsCount))

    return [("aiport_name", "number_of_visitors")] + list(query)

def findFlights(x,a,b):
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()

    sql ="""SELECT flights.id, airlines.alias, airports.name, airplanes.model
            FROM flights, airlines, airports sourc, airports dest,
                airplanes, airports, routes
            WHERE flights.date = "%s" AND flights.routes_id = routes.id
                AND routes.destination_id = dest.id AND dest.city = "%s"
                AND routes.source_id = sourc.id AND sourc.city = "%s"
                AND airports.id = routes.destination_id
                AND routes.airlines_id = airlines.id AND airlines.active = "Y"
                AND flights.airplanes_id = airplanes.id;""" % (x,b,a)

    cur.execute(sql)

    results = cur.fetchall()
    # for row in results:

    #     flightID = row[0]
    #     airlinesAlias = row[1]
    #     airportName = row[2]
    #     airplaneModel = row[3]
    #     print("%s %s %s %s" % (flightID,airlinesAlias,airportName,airplaneModel))
    
    return [("flight_id", "alt_name", "dest_name", "aircraft_model")] + list(results)
    

def findLargestAirlines(N):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
    sql="""SELECT airlines.name, airlines.id, count(distinct airplanes.id), count(distinct flights.id)
            FROM airlines, airlines_has_airplanes, airplanes, flights, routes
            WHERE airlines.id=airlines_has_airplanes.airlines_id 
                AND airlines_has_airplanes.airplanes_id=airplanes.id
                AND routes.airlines_id=airlines.id AND flights.routes_id=routes.id
            GROUP BY airlines.id"""

    cur.execute(sql)
    results = cur.fetchall() #type tuple
    sorted_list = list(results)
    sorted_list = sorted(results, key=lambda row: row[3], reverse=True) # type list
   
    tobeReturned = sorted_list[:int(N)]

    # i=0
    # for row in sorted_list:
    #     if i == N:
    #         break
    #     print("%s %s %s %s" % (row[0],row[1],row[2],row[3]))
    #     tobeReturned = tobeReturned + sorted_list[i]
    #     i = i +1

    return [("name", "id", "num_of_aircrafts", "num_of_flights")] + tobeReturned
    
def insertNewRoute(x,y): # x = airlines alias & y = source airport
    # Create a new connection
    con=connection()
    
    # Checking if alias exists
    sql = """SELECT airlines.id FROM airlines WHERE airlines.alias = "%s" """ % x
    
    # Create a cursor on the connection
    cur=con.cursor()
    
    cur.execute(sql)
    airline_id = cur.fetchall()
    if not airline_id:
        print("Alias doesn't exist. Try another alias.")
        return[("Alias doesn't exist. Try another alias.",)]

    # prwta briskw ean uparxei estw kai mia ptisi apo to source airport

    sql = """SELECT routes.id
            FROM routes, airlines, airports
            WHERE airlines.alias = "%s" AND airlines.id = routes.airlines_id 
            AND routes.source_id = airports.id AND airports.name = "%s";""" % (x,y)
    
    cur.execute(sql)
    result = cur.fetchall()
    if len(result) == 0:
        print("Airline doesn't have any flights with that airport as source")
        return[("Airline doesn't have any flights with that airport as source",)]

    i = 0
    # prepei na brw ola ta aerodromia ta opoia kataligoyn ta routes kai 8a ta exw se ena tuple
    # meta briskw ola ta aerodromia pou den kataligoun apo to source airport kai afairw apo auta
    # ekeina pou kataligoun. Epilegw tuxaia ena apo auta.
    airportsRouteExists = () # declaring a tuple that will be extended
    # for row in result:
    #     print("THE RESULT IS %s" % row[0])

    while i < len(result):
        sql ="""SELECT airports.name FROM airports, routes
            WHERE routes.id = %s AND routes.destination_id = airports.id;""" % result[i]
        
        cur.execute(sql)
        temp = cur.fetchall()
        # print("The temp is %s" % temp[0])
        airportsRouteExists = airportsRouteExists + temp
        i = i + 1
    
    # for row in airportsRouteExists:
    #     print("The airport is %s" % row[0])
    
    # I choose all the airports that they are not route's destination in result[0] 
    sql ="""SELECT airports.name FROM airports, routes
            WHERE routes.id = %s AND routes.destination_id <> airports.id;""" % result[0]
    
    cur.execute(sql)
    airportsRest = cur.fetchall()
    
    # if airportsRest tuple is empty then that means that there is no route to be added. Returning
    if not airportsRest:
        return[("airline capacity full",)]

    airportRest_List = list(airportsRest) # so I can remove the airports that routes have as destination

    i = 0
    while i < len(result):
        airportRest_List = list(filter(result[i].__ne__, airportRest_List)) # filtering the list and i have only yet unreached airports
        i = i + 1

    # choosing a random element from airportRest_list and selecting it's id code from database
    randomAirport = random.choice(airportRest_List)
    sql = """SELECT airports.id FROM airports WHERE airports.name = "%s" """ % (randomAirport)
    
    cur.execute(sql)
    airportID_Destination = cur.fetchall()
    # print("THE AIRPORT TO BE INSERTED IS %s = %s" % (airportID_Destination[0][0],randomAirport[0]))
    
    # need to create a new route_id so i just take the max route.id from db and increment it by 1
    # the incrementation occurs inside the insertion sql query in line 327
    sql = """SELECT max(routes.id) FROM routes"""
    cur.execute(sql)
    newRoute = cur.fetchall()

    # need to fetch the airport source id
    sql = """SELECT airports.id FROM airports
            WHERE airports.name = "%s" """ % y

    cur.execute(sql)
    airportID_Source = cur.fetchall()
    # preparing to Insert in database
    #
    sql  = """INSERT INTO routes(id,airlines_id,source_id,destination_id)
            VALUES (%s+1,%s,%s,%s)""" % (newRoute[0][0], airline_id[0][0], airportID_Source[0][0], airportID_Destination[0][0])
    
    try:
        cur.execute(sql)
        con.commit()
    except:
        con.rollback()
    
    con.close()

    return [("ΟΚ",)]

