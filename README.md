# Log Analytics

Log Analytics is the first project for Udacity's Full Stack Web Developer Nanodegree Program.

## Project Overview

___

This is an internal reporting tool for newspaper site to discover what kind of articles the site's readers like and it also shows the error log for a particular date. This project uses **_Python3_** programming language and **_Postgresql_** as Database. It mainly fulfills three queries.

    1. What are the most popular three articles of all time?
    2. Who are the most popular article authors of all time?
    3. On which days did more than 1% of requests lead to errors?

## Instructions

___

* Download and install [python](https://www.python.org/)
* Download and install [virtual box](https://www.virtualbox.org/)
* Download and install [vagrant](https://www.vagrantup.com/)
* Download this [vagrant configuration file](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) and extract it.
* Now move inside the extracted folder using ```cd``` command in terminal.
* Inside this folder, there is one folder called *vagrant* Run command ```cd vagrant/``` to get in.
* To start virtual machine run command ```vagrant up```, it will take some time so be patience.
* When ```vagrant up``` is finished running you will get your shell prompt back. At this point, you can run ```vagrant ssh``` to log in to your newly installed Linux VM!
* Inside the VM, change directory to ```/vagrant```.
* Now download data file [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and put this file inside *vagrant* folder.
* To load the data, ```cd``` into the ```vagrant``` directory and use the command ```psql -d news -f newsdata.sql```.
* Now run ```psql``` command and create the views given below.

## Views

___

### To run python file without any error, create following views in your database

## 1) popular_articles view

In this view

```sql
create view popular_articles as
select articles.author as author_id, articles.title, count(title) as views from articles, log where log.path like concat('/article/', articles.slug) group by articles.author, articles.title order by views desc;
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
create view popular_authors as select authors.name, sum(views) as total_views from authors, popular_articles where authors.id = popular_articles.author_id group by authors.name order by total_views desc;
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
create view error_log as select time, Total, Error, (Error::float * 100)/Total::float as Percentage from ( select time::date, count(status) as Total, sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Error from log group by time::date ) as result where (Error::float * 100)/Total > 1.0 order by Percentage desc;
```

### The data in error_log view will look like this

|time | total   | error  | percentage |
|-----:|:-------:|:------:|:-------|
| 2016-07-17 | 55907 |  1265 | 2.26268624680273 |
