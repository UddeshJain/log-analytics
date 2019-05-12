#!/usr/bin/env python3

import psycopg2

try:
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
except:
    print('Can not connect to database.')


def get_popular_article():
    # Prints the most popular three articles of all time
    query = 'select title, views from popular_articles limit 3'
    c.execute(query)
    result = c.fetchall()
    print('Most popular three articles of all time:')
    for i in range(len(result)):
        print("\t" + result[i][0] + " - " + str(result[i][1]) + " views")


def get_popular_authors():
    # Prints the most popular authors of all time
    query = 'select name, total_views from popular_authors'
    c.execute(query)
    result = c.fetchall()
    print('\n\nMost popular authors of all time:')
    for i in range(len(result)):
        print("\t" + result[i][0] + " - " + str(result[i][1]) + " views")


def get_error_logs():
    # Days when more than 1% of requests lead to errors
    query = 'select time, percentage from error_log'
    c.execute(query)
    result = c.fetchall()
    print('\n\ndays when more than 1% of requests lead to errors:')
    for i in range(len(result)):
        print("\t" + str(result[i][0]) + " - " + str('%.2f'%result[i][1]) + " %")

# Function calls
get_popular_article()
get_popular_authors()
get_error_logs()
