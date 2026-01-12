from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


MY_SQL = "mysql+pymysql://root:bvc24@localhost:3306"

DB_NAME = "weighbridge"

engine = create_engine(MY_SQL,echo=True)

db_status = False

try:
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        db_status=True
        print(f"Database created successfully or already exist")
except Exception as e:
    print(f"error creating database{str(e)}")
    
if db_status == True:
    MY_SQL = f"mysql+pymysql://root:bvc24@localhost:3306/{DB_NAME}"
    engine = create_engine(MY_SQL,echo=True)
    SessionLocal=sessionmaker(bind=engine)
    print("Database created and ready to work")
    
else:
    print("Error creating database and connection failed")