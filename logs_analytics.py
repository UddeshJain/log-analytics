#!/usr/bin/env python3

import psycopg2


def execute_query(query):
    try:
        db = psycopg2.connect("dbname=news")
        c = db.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        c.execute(query)
        results = c.fetchall()
        db.close()
        return results


def get_popular_article():
    # Prints the most popular three articles of all time
    query = 'select title, views from popular_articles limit 3'
    results = execute_query(query)
    print('Most popular three articles of all time:')
    for title, views in results:
        print('\t{} - {} views'.format(title, views))


def get_popular_authors():
    # Prints the most popular authors of all time
    query = 'select name, total_views from popular_authors'
    results = execute_query(query)
    print('\n\nMost popular authors of all time:')
    for name, views in results:
        print('\t{} - {} views'.format(name, views))


def get_error_logs():
    # Days when more than 1% of requests lead to errors
    query = "select to_char( time, 'Mon DD, YYYY'), percentage from error_log"
    results = execute_query(query)
    print('\n\ndays when more than 1% of requests lead to errors:')
    for date, percent in results:
        print('\t{} - {} %'.format(date, '%.2f' % percent))


# Function calls
def main():
    """Generate report."""
    get_popular_article()
    get_popular_authors()
    get_error_logs()


if __name__ == '__main__':
    main()
