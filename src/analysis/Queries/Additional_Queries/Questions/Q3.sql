# Start from the last one. Others are just for help.

WITH RankedPlayers AS (SELECT player_id,
                              team_id,
                              season,
                              position,
                              per,
                              RANK() OVER (PARTITION BY position ORDER BY per DESC)                as rank_position,
                              ROW_NUMBER() OVER (PARTITION BY team_id, position ORDER BY per DESC) as team_position_rank
                       FROM PlayerSeasonStats
                       WHERE season = '2025')
SELECT Teams.name             as `Team Name`,
       season                 as Season,
       RankedPlayers.position as Position,
       Players.name           as `Player Name`,
       rank_position          as Rank,
       per                    as PER
FROM RankedPlayers
         join Teams on RankedPlayers.team_id = Teams.team_id
         join Players on Players.player_id = RankedPlayers.player_id
# where team_position_rank = 1      #   --> If you want to see only one player for each position and team
ORDER BY Teams.team_id, position, rank_position;


# Another formula for ranking
# Score = 0.40 PER + 0.30 Pts + 0.15 Ast + 0.10 Reb + 0.05 Stl

WITH RankedPlayers AS (SELECT player_id,
                              team_id,
                              season,
                              position,
                              per,
                              (0.40 * PSS.per + 0.30 * PSS.pts + 0.15 * PSS.ast + 0.10 * PSS.trb + 0.05 * stl)          AS score,
                              RANK() OVER (PARTITION BY position ORDER BY (0.40 * PSS.per + 0.30 * PSS.pts +
                                                                           0.15 * PSS.ast + 0.10 * PSS.trb + 0.05 *
                                                                                                             stl) DESC) AS rank_position,
                              ROW_NUMBER() OVER (PARTITION BY team_id, position ORDER BY (0.40 * PSS.per +
                                                                                          0.30 * PSS.pts +
                                                                                          0.15 * PSS.ast +
                                                                                          0.10 * PSS.trb + 0.05 *
                                                                                                           stl) DESC)   AS team_position_rank
                       FROM PlayerSeasonStats as PSS
                       WHERE season = '2025')
SELECT Teams.name             AS `Team Name`,
       season                 AS Season,
       RankedPlayers.position AS Position,
       Players.name           AS `Player Name`,
       rank_position          AS `Rank`,
       score                  AS `Score`
FROM RankedPlayers
         JOIN Teams ON RankedPlayers.team_id = Teams.team_id
         JOIN Players ON Players.player_id = RankedPlayers.player_id
# WHERE team_position_rank = 1
ORDER BY Teams.team_id, position, rank_position;


# We can use different weights (formula) for different positions
WITH normalized AS (SELECT *,
                           (pts - AVG(pts) OVER (PARTITION BY position)) /
                           NULLIF(STDDEV_POP(pts) OVER (PARTITION BY position), 0) AS z_pts,
                           (ast - AVG(ast) OVER (PARTITION BY position)) /
                           NULLIF(STDDEV_POP(ast) OVER (PARTITION BY position), 0) AS z_ast,
                           (trb - AVG(trb) OVER (PARTITION BY position)) /
                           NULLIF(STDDEV_POP(trb) OVER (PARTITION BY position), 0) AS z_trb,
                           (stl - AVG(stl) OVER (PARTITION BY position)) /
                           NULLIF(STDDEV_POP(stl) OVER (PARTITION BY position), 0) AS z_stl,
                           (blk - AVG(blk) OVER (PARTITION BY position)) /
                           NULLIF(STDDEV_POP(blk) OVER (PARTITION BY position), 0) AS z_blk,
                           (efg - AVG(efg) OVER (PARTITION BY position)) /
                           NULLIF(STDDEV_POP(efg) OVER (PARTITION BY position), 0) AS z_efg,
                           (per - AVG(per) OVER (PARTITION BY position)) /
                           NULLIF(STDDEV_POP(per) OVER (PARTITION BY position), 0) AS z_per,
                           (tov - AVG(tov) OVER (PARTITION BY position)) /
                           NULLIF(STDDEV_POP(tov) OVER (PARTITION BY position), 0) AS z_tov
                    FROM PlayerSeasonStats),
     raw_scores AS (SELECT *,
                           CASE position
                               WHEN 'PG' THEN
                                   0.18 * z_pts + 0.22 * z_per + 0.12 * z_efg + 0.30 * z_ast + 0.08 * z_stl -
                                   0.10 * z_tov
                               WHEN 'SG' THEN
                                   0.32 * z_pts + 0.22 * z_per + 0.20 * z_efg + 0.08 * z_ast + 0.10 * z_stl -
                                   0.08 * z_tov
                               WHEN 'SF' THEN
                                   0.23 * z_pts + 0.18 * z_per + 0.09 * z_efg + 0.15 * z_ast + 0.15 * z_trb +
                                   0.10 * z_stl + 0.10 * z_blk
                               WHEN 'PF' THEN
                                   0.20 * z_pts + 0.18 * z_per + 0.12 * z_efg + 0.06 * z_ast + 0.20 * z_trb +
                                   0.08 * z_stl + 0.16 * z_blk
                               WHEN 'C' THEN
                                   0.18 * z_pts + 0.20 * z_per + 0.14 * z_efg + 0.26 * z_trb + 0.22 * z_blk
                               END AS raw_score
                    FROM normalized)
SELECT raw_scores.season                                                                                    as Season,
       raw_scores.position                                                                                  as Position,
       Players.name                                                                                         as `Player Name`,
       RANK() OVER (PARTITION BY raw_scores.season, raw_scores.position ORDER BY raw_scores.raw_score DESC) AS rank_position,
       ROUND(
               100 * (raw_score - MIN(raw_score) OVER ()) / NULLIF(MAX(raw_score) OVER () - MIN(raw_score) OVER (), 0),
               2
       )                                                                                                    AS Score,
       Teams.name                                                                                           as `Team Name`,
       raw_scores.*
FROM raw_scores
         join Players on Players.player_id = raw_scores.player_id
         join Teams on Teams.team_id = raw_scores.team_id
ORDER BY raw_scores.season, raw_scores.position, rank_position;

# Fast query. almost same as above
WITH stats AS (SELECT season,
                      position,
                      AVG(pts)        AS avg_pts,
                      STDDEV_POP(pts) AS std_pts,
                      AVG(ast)        AS avg_ast,
                      STDDEV_POP(ast) AS std_ast,
                      AVG(trb)        AS avg_trb,
                      STDDEV_POP(trb) AS std_trb,
                      AVG(stl)        AS avg_stl,
                      STDDEV_POP(stl) AS std_stl,
                      AVG(blk)        AS avg_blk,
                      STDDEV_POP(blk) AS std_blk,
                      AVG(efg)        AS avg_efg,
                      STDDEV_POP(efg) AS std_efg,
                      AVG(per)        AS avg_per,
                      STDDEV_POP(per) AS std_per,
                      AVG(tov)        AS avg_tov,
                      STDDEV_POP(tov) AS std_tov
               FROM PlayerSeasonStats
               GROUP BY season, position),

     normalized AS (SELECT p.*,
                           (p.pts - s.avg_pts) / NULLIF(s.std_pts, 0) AS z_pts,
                           (p.ast - s.avg_ast) / NULLIF(s.std_ast, 0) AS z_ast,
                           (p.trb - s.avg_trb) / NULLIF(s.std_trb, 0) AS z_trb,
                           (p.stl - s.avg_stl) / NULLIF(s.std_stl, 0) AS z_stl,
                           (p.blk - s.avg_blk) / NULLIF(s.std_blk, 0) AS z_blk,
                           (p.efg - s.avg_efg) / NULLIF(s.std_efg, 0) AS z_efg,
                           (p.per - s.avg_per) / NULLIF(s.std_per, 0) AS z_per,
                           (p.tov - s.avg_tov) / NULLIF(s.std_tov, 0) AS z_tov

                    FROM PlayerSeasonStats p
                             JOIN stats s ON p.season = s.season AND p.position = s.position),
     raw_scores AS (SELECT *,
                           CASE position
                               WHEN 'PG' THEN
                                   0.18 * z_pts + 0.22 * z_per + 0.12 * z_efg + 0.30 * z_ast + 0.08 * z_stl - 0.10 * z_tov
                               WHEN 'SG' THEN
                                   0.32 * z_pts + 0.22 * z_per + 0.20 * z_efg + 0.08 * z_ast + 0.10 * z_stl - 0.08 * z_tov
                               WHEN 'SF' THEN
                                   0.23 * z_pts + 0.18 * z_per + 0.09 * z_efg + 0.15 * z_ast + 0.15 * z_trb + 0.10 * z_stl + 0.10 * z_blk
                               WHEN 'PF' THEN
                                   0.20 * z_pts + 0.18 * z_per + 0.12 * z_efg + 0.06 * z_ast + 0.20 * z_trb + 0.08 * z_stl + 0.16 * z_blk
                               WHEN 'C' THEN
                                   0.18 * z_pts + 0.20 * z_per + 0.14 * z_efg + 0.26 * z_trb + 0.22 * z_blk
                               END AS raw_score
                    FROM normalized),

     bounds AS (SELECT MIN(raw_score) AS min_score, MAX(raw_score) AS max_score
                FROM raw_scores)

SELECT rs.season   AS Season,
       rs.position AS Position,
       p.name      AS `Player Name`,

       RANK() OVER (
           PARTITION BY rs.season, rs.position
           ORDER BY rs.raw_score DESC
           )       AS rank_position,

       ROUND(100 * (rs.raw_score - b.min_score) / NULLIF(b.max_score - b.min_score, 0),
             2
       )           AS Score,
       t.name      AS `Team Name`,
       rs.*
FROM raw_scores rs
         CROSS JOIN bounds b
         JOIN Players p ON p.player_id = rs.player_id
         JOIN Teams t ON t.team_id = rs.team_id
ORDER BY rs.season, rs.position, rank_position;
