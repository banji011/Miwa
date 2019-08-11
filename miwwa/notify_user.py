import sqlite3
from datetime import datetime
import requests

conn = sqlite3.connect('miwwa_project.db')

cursor = conn.cursor()

today = datetime.utcnow().strftime("%Y-%m-%d")

a = cursor.execute("SELECT phone FROM users WHERE verified=0")

def notify_unverified_user():
    for phone in a:
        # requests.post(f"http://www.smsmobile24.com/index.php?option=com_spc&comm=spc_api&username=MZYF&password=MZYFS&sender=MIWA Admin&recipient={phone}&message=Please complete your registration and get verified !  &")
        print(phone)
        print(type(a))
        


notify_unverified_user()
conn.commit()
conn.close()
