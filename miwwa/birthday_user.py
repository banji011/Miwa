import MySQLdb
from datetime import datetime
import requests

conn = MySQLdb.connect("localhost", "root", "Olabanji011", "miwadb")

cursor = conn.cursor()

today = datetime.utcnow().strftime("%Y-%m-%d")

query = "SELECT first_name, last_name, phone, email, dob FROM users"
cursor.execute(query)

def send_birthday_msg():
    for user in cursor:
        if user[4] == today:
            print(user[4])
            requests.post(f"http://www.smsmobile24.com/index.php?option=com_spc&comm=spc_api&username=MZYF&password=MZYFS&sender=MIWA Admin&recipient={user[2]}&message=Happy birthday {user[0]} {user[1]}. From all of us at Miwa  &")
           

        
        
    
        


send_birthday_msg()
conn.commit()
conn.close()
