ΔΙΟΝΥΣΙΟΣ ΜΠΕΝΤΟΎΡ 1115201300115 Σε κάποια το formatting (χρησιμοποίησα formatting VSCode) μπορεί να είναι διαφορετικό.Αυτό συνέβαινε διότι όταν έκανα copy paste sto terminal δεν δούλευε εάν υπήρχαν πολλά tabs.Στο workbench δουλεύει ανεξαρτήτως.use flights;

#1---------------------------------------------------------------
SELECT
    distinct airplanes.number
FROM
    airplanes,
    airlines,
    airlines_has_airplanes
WHERE
    airplanes.id = airlines_has_airplanes.airplanes_id
    AND airplanes.manufacturer = 'Airbus'
    AND airlines_id = airlines.id
    AND airlines.name = 'Lufthansa';

#2--------------------------------------------------------------
SELECT
    distinct airlines.name
FROM
    airlines,
    routes,
    airports
WHERE
    airlines.id = routes.airlines_id
    AND routes.id IN (
        SELECT
            distinct routes.id
        FROM
            routes,
            airports
        WHERE
            routes.destination_id IN (
                SELECT
                    routes.destination_id
                FROM
                    routes,
                    airports
                WHERE
                    routes.destination_id = airports.id
                    AND airports.city = 'Prague'
            )
            AND routes.source_id IN (
                SELECT
                    routes.source_id
                FROM
                    routes,
                    airports
                WHERE
                    routes.source_id = airports.id
                    AND airports.city = 'Athens'
            )
    );

#3
SELECT
    count(distinct passengers_id)
FROM
    flights_has_passengers,
    flights,
    routes,
    airlines
WHERE
    flights_has_passengers.flights_id = flights.id
    AND flights.date = '2012-02-19'
    AND flights.routes_id = routes.id
    AND routes.airlines_id = airlines.id
    AND airlines.name = 'Aegean Airlines';

#4------------------------------------------------------------
SELECT
    "yes" AS answer
WHERE
    EXISTS(
        SELECT
            flights.id
        FROM
            flights
        WHERE
            EXISTS(
                SELECT
                    distinct routes.id
                FROM
                    routes,
                    airports
                WHERE
                    flights.routes_id = routes.id
                    AND flights.date = '2014-12-12'
                    AND routes.destination_id IN (
                        SELECT
                            routes.destination_id
                        FROM
                            routes,
                            airports
                        WHERE
                            routes.destination_id = airports.id
                            AND airports.name = 'London Gatwick'
                    )
                    AND routes.source_id IN (
                        SELECT
                            routes.source_id
                        FROM
                            routes,
                            airports
                        WHERE
                            routes.source_id = airports.id
                            AND airports.name = 'Athens El. Venizelos'
                    )
            )
    )
UNION
SELECT
    "no" AS answer
WHERE
    NOT EXISTS(
        SELECT
            flights.id
        FROM
            flights
        WHERE
            EXISTS(
                SELECT
                    distinct routes.id
                FROM
                    routes,
                    airports
                WHERE
                    flights.routes_id = routes.id
                    AND flights.date = '2014-12-12'
                    AND routes.destination_id IN (
                        SELECT
                            routes.destination_id
                        FROM
                            routes,
                            airports
                        WHERE
                            routes.destination_id = airports.id
                            AND airports.name = 'London Gatwick'
                    )
                    AND routes.source_id IN (
                        SELECT
                            routes.source_id
                        FROM
                            routes,
                            airports
                        WHERE
                            routes.source_id = airports.id
                            AND airports.name = 'Athens El. Venizelos'
                    )
            )
    );

#5------------------------------------------------------------
SELECT
    YEAR(CURDATE()) - AVG(passengers.year_of_birth)
FROM
    passengers
WHERE
    passengers.id IN (
        SELECT
            passengers.id
        FROM
            flights_has_passengers,
            flights
        WHERE
            passengers.id = flights_has_passengers.passengers_id
            AND flights_has_passengers.flights_id IN (
                SELECT
                    flights_has_passengers.flights_id
                FROM
                    routes,
                    airports
                WHERE
                    flights_has_passengers.flights_id = flights.id
                    AND flights.routes_id = routes.id
                    AND routes.destination_id = airports.id
                    AND airports.city = 'Berlin'
            )
    );

#6------------------------------------------------------------
SELECT
    passengers.name,
    passengers.surname
FROM
    passengers
WHERE
    exists (
        SELECT
            passengers.id
        FROM
            flights_has_passengers,
            flights
        WHERE
            passengers.id = flights_has_passengers.passengers_id
            AND flights_has_passengers.flights_id = flights.id
        GROUP BY
            passengers.id
        HAVING
            COUNT(distinct flights.airplanes_id) = 1
    );

#7------------------------------------------------------------
SELECT
    airportSource.city AS source,
    airportDestination.city AS destination
FROM
    airports airportSource,
    airports airportDestination,
    routes,
    flights,
    flights_has_passengers
WHERE
    flights.routes_id = routes.id
    AND flights.id = flights_has_passengers.flights_id
    AND flights.date >= '2010-03-01'
    AND flights.date <= '2014-07-17'
    AND routes.source_id = airportSource.id
    AND routes.destination_id = airportDestination.id
GROUP BY
    flights.id
HAVING
    COUNT(flights_has_passengers.passengers_id) > 5;

#8------------------------------------------------------------
SELECT
    airlines.name,
    airlines.code,
    COUNT(routes.airlines_id)
FROM
    airlines,
    routes
WHERE
    airlines.id = routes.airlines_id
    AND not exists(
        SELECT
            airlines.id
        FROM
            airlines_has_airplanes
        WHERE
            airlines.id = airlines_has_airplanes.airlines_id
        GROUP BY
            airlines_has_airplanes.airlines_id
        HAVING
            COUNT(airlines_has_airplanes.airplanes_id) <> 4
    )
GROUP BY
    airlines.id;

#9------------------------------------------------------------
SELECT
    distinct passengers.name,
    passengers.surname
FROM
    passengers
WHERE
    not exists(
        SELECT
            airlines.id
        FROM
            airlines
        WHERE
            airlines.active = 'Y'
            AND not exists (
                SELECT
                    passengers.id
                FROM
                    flights_has_passengers,
                    flights,
                    routes
                WHERE
                    passengers.id = flights_has_passengers.passengers_id
                    AND flights_has_passengers.flights_id = flights.id
                    AND flights.routes_id = routes.id
                    AND routes.airlines_id = airlines.id
            )
    );

#10------------------------------------------------------------
SELECT
    distinct passengers.name,
    passengers.surname,
    passengers.id
FROM
    passengers
WHERE
    not exists(
        SELECT
            passengers.id
        FROM
            flights,
            routes,
            airlines,
            flights_has_passengers
        WHERE
            passengers.id = flights_has_passengers.passengers_id
            AND flights_has_passengers.flights_id = flights.id
            AND flights.routes_id = routes.id
            AND exists (
                SELECT
                    airlines.id
                WHERE
                    routes.airlines_id = airlines.id
                GROUP BY
                    airlines.id
                HAVING
                    airlines.name <> 'Aegean Airlines'
            )
    )
    AND exists (
        SELECT
            passengers.id
        FROM
            flights_has_passengers
        WHERE
            passengers.id = flights_has_passengers.passengers_id
    )
UNION
SELECT
    distinct passengers.name,
    passengers.surname,
    passengers.id
FROM
    passengers
WHERE
    exists(
        SELECT
            passengers.id
        FROM
            flights_has_passengers,
            flights
        WHERE
            passengers.id = flights_has_passengers.passengers_id
            AND flights_has_passengers.flights_id = flights.id
            AND flights.date >= '2011-01-02'
            AND flights.date <= '2013-12-31'
        GROUP BY
            passengers.id
        HAVING
            COUNT(flights.id) > 1
    );

SELECT
    flights.id,
    airlines.alias,
    airports.name,
    airplanes.model
FROM
    flights,
    airlines,
    airports sourc,
    airports dest,
    airplanes,
    airports,
    routes
WHERE
    flights.date = "2014-11-03"
    AND flights.routes_id = routes.id
    AND routes.destination_id = dest.id
    AND dest.city = "Dubai"
    AND routes.source_id = sourc.id
    AND sourc.city = "Male"
    AND airports.id = routes.destination_id
    AND routes.airlines_id = airlines.id
    AND airlines.active = "Y"
    AND flights.airplanes_id = airplanes.id;




SELECT
    airlines.name,
    airlines.id,
    count(distinct airplanes.id) as num_of_airplanes,
    count(distinct flights.id)
FROM
    airlines,
    airlines_has_airplanes,
    airplanes,
    flights,
    routes
WHERE
    airlines.id = airlines_has_airplanes.airlines_id
    AND airlines_has_airplanes.airplanes_id = airplanes.id
    AND routes.airlines_id = airlines.id
    AND flights.routes_id = routes.id
GROUP BY
    airlines.id

    ANA All Nippon Airways

    Fukuoka

    select
	airports.name
from 
	airports,
    routes
where
	routes.id = 42848 and
    routes.destination_id = airports.id;


     airlinesName_List = list(filter(airlinesName_List[0].__ne__, airlinesName_List))


sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
 LAST_NAME, AGE, SEX, INCOME)
 VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""


 try:
 # Execute the SQL command
 cursor.execute(sql)
 # Commit your changes in the database
 db.commit()
except:
 # Rollback in case there is any error
 db.rollback()