# Some columns might be duplicate such as prev.standing

# Result only for specific season
SELECT t.name                          AS TeamName,
       prev.standing                   AS Standing_Previous,
       curr.standing                   AS Standing_Current,
       (prev.standing - curr.standing) AS Improvement,
       CASE
           WHEN curr.standing - prev.standing <= -5 THEN 'High Progress'
           WHEN curr.standing - prev.standing >= 4 THEN 'Regression'
           WHEN ABS(curr.standing - prev.standing) <= 3 THEN 'No Change'
           ELSE 'Other (diff = -4)'
           END                         AS Category,
       curr.*,
       prev.*
FROM TeamSeasonStats AS prev
         JOIN TeamSeasonStats AS curr
              ON prev.team_id = curr.team_id
                  AND prev.season = '2024'
                  AND curr.season = '2025'
         JOIN Teams AS t ON t.team_id = curr.team_id
ORDER BY Improvement DESC;

# Result for all seasons.
SELECT t.name                          AS TeamName,
       prev.season                     AS PrevSeason,
       curr.season                     AS CurrSeason,
       prev.standing                   AS Standing_Previous,
       curr.standing                   AS Standing_Current,
       (prev.standing - curr.standing) AS Improvement,
       CASE
           WHEN curr.standing - prev.standing <= -4 THEN 'High Progress'
           WHEN curr.standing - prev.standing >= 4 THEN 'Regression'
           WHEN ABS(curr.standing - prev.standing) < 4 THEN 'No Change'
           ELSE 'Other'
           END                         AS Category,
       curr.*,
       prev.*
FROM TeamSeasonStats AS prev
         JOIN TeamSeasonStats AS curr
              ON prev.team_id = curr.team_id
                  AND CAST(curr.season AS UNSIGNED) = CAST(prev.season AS UNSIGNED) + 1
         JOIN Teams AS t ON t.team_id = curr.team_id
ORDER BY curr.season, Improvement DESC;