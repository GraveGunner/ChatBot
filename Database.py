import mysql.connector


db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "pizza_menu"
)
cursor = db.cursor()

def pizzaorder(topping, size):
    sql = "SELECT price FROM nonveg WHERE topping = %s AND size = %s"
    var = (topping, size)
    cursor.execute(sql, var)
    result = cursor.fetchall()
    return (result[0][0])