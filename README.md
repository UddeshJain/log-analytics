# Log Analytics

Log Analytics is the first project for Udacity's Full Stack Web Developer Nanodegree Program.

## Project Overview

This is an internal reporting tool for newspaper site to discover what kind of articles the site's readers like and it also shows the error log for a particular date. This project uses **_Python3_** programming language and **_Postgresql_** as Database. It mainly fulfills three queries.

    1. What are the most popular three articles of all time?
    2. Who are the most popular article authors of all time?
    3. On which days did more than 1% of requests lead to errors?

## Instructions

* Download and install [python](https://www.python.org/)
* Download and install [virtual box](https://www.virtualbox.org/)
* Download and install [vagrant](https://www.vagrantup.com/)
* Clone this repository and navigate inside it.
* To start virtual machine run command ```vagrant up``` in the terminal, it will take some time so be patience.
* When ```vagrant up``` is finished running you will get your shell prompt back. At this point, you can run ```vagrant ssh``` to log in to your newly installed Linux VM!
* Inside the VM, change directory to ```/vagrant```.
* Now download data file from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and put this file inside your working directory.
* To load the data run command ```psql -d news -f newsdata.sql```.
* Now run ```psql news``` command to directly connect to the database and create the views given below.

## Views

 You don't need to create these views manually, There is a ```create_views.sql``` file in the repository that you cloned, it will automatically create the view. You just need to run ```psql -d news -f create_views.sql``` command.

## 1) popular_articles view

```sql
CREATE VIEW popular_articles AS
SELECT articles.author as author_id,
    articles.title,
    count(title) as views
FROM articles, log
WHERE log.path = concat('/article/', articles.slug)
GROUP BY articles.author, articles.title
ORDER BY views DESC;
```

### The data in popular_articles view will look like this

|author_id |               title                | views|  
|-----------|:------------------------------------:|:--------:|
|2 | Candidate is jerk, alleges rival   | 338647|
|1 | Bears love berries, alleges bear   | 253801|
| 3 | Bad things gone, say good people   | 170098|
| 1 | Goats eat Google's lawn            |  84906|
| 2 | Trouble for troubled troublemakers |  84810|
| 4 | Balloon goons doomed               |  84557|
| 1 | There are a lot of bears           |  84504|
| 1 | Media obsessed with bears          |  84383|

## 2) popular_authors view

```sql
CREATE VIEW popular_authors AS
SELECT authors.name,
    sum(views) AS total_views
FROM authors, popular_articles
where authors.id = popular_articles.author_id
GROUP BY authors.name
ORDER BY total_views DESC;
```

### The data in popular_authors view will look like this

|               name                | total_views |
|----------------------------|:-------------:|
|Ursula La Multa               |      507594 |
| Rudolf von Treppenwitz  |      423457 |
| Anonymous Contributor  |      170098 |
| Markoff Chaney               |       84557  |

## 3) error_log view

```sql
CREATE VIEW error_log AS
SELECT time, Total, Error, (Error::float * 100)/Total::float as Percentage FROM
    ( select time::date,
        count(status) as Total,
        sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Error from log
    GROUP BY time::date ) as result
WHERE (Error::float * 100)/Total > 1.0
ORDER BY Percentage DESC;
```

### The data in the error_log view will look like this

|time | total   | error  | percentage |
|-----:|:-------:|:------:|:-------|
| Jul 17, 2016 | 55907 |  1265 | 2.26268624680273 |

## How to run the python file

* Navigate to the cloned directory and run ```ls``` command to make sure ```logs_analytics.py``` file is there.
* Open terminal and run ```python logs_analytics.py``` command.
* That's it, You will get the result in the terminal.