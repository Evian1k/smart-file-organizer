# Script to initialize the database
from lib.db.connection import engine
from lib.db.models import Base

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    print('Database tables created.')
