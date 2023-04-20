#!/usr/bin/env python3

import sqlite3
import sys

def main():
    if len(sys.argv) < 2:
        print("error: my-cr-report.py <Cosmic-Ray sqlite db file>")
        print("Example: my-cr-report.py /home/auri/temp/lucca/python_experiments/binarySearchTree1/RANDOM/cosmic-ray/binarySearchTree1.sqlite")
        sys.exit(1)

    db_filename = sys.argv[1]

    # Create a SQL connection to our SQLite database
    con = sqlite3.connect(db_filename)

    cur = con.cursor()

    # The result of a "cursor.execute" can be iterated over by row
    cur.execute('SELECT count(*) FROM work_results WHERE test_outcome is "SURVIVED";')
    row = cur.fetchone()
    print("Survived: %d" %row[0])

    cur.execute('SELECT count(*) FROM work_results WHERE output is not "timeout" and test_outcome is "KILLED";')
    row = cur.fetchone()
    print("Killed by output: %d" %row[0])

    cur.execute('SELECT count(*) FROM work_results WHERE output is "timeout" and test_outcome is "KILLED";')
    row = cur.fetchone()
    print("Killed by timeout: %d" %row[0])

    # Be sure to close the connection
    con.close()

if __name__ == "__main__":
    main()