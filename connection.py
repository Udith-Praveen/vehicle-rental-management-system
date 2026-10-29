import sys
from db_config import get_connection, setup_tables
from main import main

connect_db = get_connection

if __name__ == '__main__':
    main()
