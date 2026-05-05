import csv

from app import app
from app import app, db, weather_data


def import_csv_to_db(file_path):
    with app.app_context():
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                data = weather_data(
                    area=row['area'],
                    date=row['date'],
                    am1=float(row['am1']),
                    am2=float(row['am2']),
                    pm1=float(row['pm1']),
                    pm2=float(row['pm2'])
                )

                db.session.add(data)

            db.session.commit()
        

import_csv_to_db('C:\\Users\\ajlxs\\OneDrive\\Documents\\Unit_9\\unit_9\\unit_9_code\\9_weather_data(Sheet1).csv')