import csv
import secrets
from app import app
from app import app, db, weather_data
from app import app, db, admin_key
from app import app, db, user_info
from datetime import datetime


def import_csv_to_db(file_path):
    with app.app_context():
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                data = weather_data(
                    id=row['id'],
                    area=row['area'],
                    date=row['date'],
                    am1=float(row['am1']),
                    am2=float(row['am2']),
                    pm1=float(row['pm1']),
                    pm2=float(row['pm2'])
                )

                db.session.add(data)

            db.session.commit()

import_csv_to_db(r"C:\Users\ajlxs\OneDrive\Documents\weather_data_files\weather_data.csv")

        
keys = []
def add_admin_key():
    with app.app_context():
        key = secrets.token_urlsafe(32)
        db.session.add(admin_key(key))
        db.session.commit()
        print(f"key {key}")
        
for i in range(5):
    add_admin_key()

print("done")




