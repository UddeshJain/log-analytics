CREATE VIEW popular_articles AS
SELECT articles.author as author_id,
    articles.title,
    count(title) as views
FROM articles, log
WHERE log.path = concat('/article/', articles.slug)
GROUP BY articles.author, articles.title
ORDER BY views DESC;


CREATE VIEW popular_authors AS
SELECT authors.name,
    sum(views) AS total_views
FROM authors, popular_articles
where authors.id = popular_articles.author_id
GROUP BY authors.name
ORDER BY total_views DESC;


CREATE VIEW error_log AS
SELECT time, Total, Error, (Error::float * 100)/Total::float as Percentage FROM
    ( select time::date,
        count(status) as Total,
        sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Error from log
    GROUP BY time::date ) as result
WHERE (Error::float * 100)/Total > 1.0
ORDER BY Percentage DESC;