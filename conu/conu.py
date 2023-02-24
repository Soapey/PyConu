import sys
from conu.db.SQLiteConnection import init_db


if __name__ == "__main__":
    try:
        clean = bool(int(sys.argv[1]))
    except:
        print("First parameter must be database 'clean' boolean.")
        sys.exit()

    init_db(clean=clean)
