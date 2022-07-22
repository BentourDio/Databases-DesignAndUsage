import pymysql

# Open database connection
db = pymysql.connect(host='localhost',
                             user='root',
                             password='Password123#@!',
                             database='testdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)# prepare a cursor object using cursor() method
cursor = db.cursor()
# Drop table if it already exist using execute() method.
sql = "SELECT * FROM EMPLOYEE WHERE INCOME > '%d'" % (1000)

try:
    cursor.execute(sql)
    
    results = cursor.fetchall()
    
    for row in results:
       
        fname = row[0]
        print("here")
        lname = row[1]
        print("here")
        age = row[2]
        sex = row[3]
        income = row[4]
        
        print ("fname = %s,lname = %s,age = %d,sex = %s,income = %d" % (fname, lname, age, sex, income))
except:
    print("Error: unbale to fetch data")
print("gamw ton 8eo")
db.close