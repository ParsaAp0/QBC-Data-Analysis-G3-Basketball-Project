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

     team_normalized AS (SELECT *,
                                (standing - AVG(standing) OVER (PARTITION BY season)) /
                                NULLIF(STDDEV_POP(standing) OVER (PARTITION BY season), 0)    AS zStanding,
                                (`W/L%` - AVG(`W/L%`) OVER (PARTITION BY season)) /
                                NULLIF(STDDEV_POP(`W/L%`) OVER (PARTITION BY season), 0)      AS zWL,
                                (ORtg - AVG(ORtg) OVER (PARTITION BY season)) /
                                NULLIF(STDDEV_POP(ORtg) OVER (PARTITION BY season), 0)        AS zOR,
                                (DRtg - AVG(DRtg) OVER (PARTITION BY season)) /
                                NULLIF(STDDEV_POP(DRtg) OVER (PARTITION BY season), 0)        AS zDR,
                                ((ORtg - DRtg) - AVG(ORtg - DRtg) OVER (PARTITION BY season)) /
                                NULLIF(STDDEV_POP(ORtg - DRtg) OVER (PARTITION BY season), 0) AS zNet
                         FROM TeamSeasonStats),

     team_scores AS (SELECT *, (-0.35 * zStanding + 0.30 * zWL + 0.15 * zOR - 0.15 * zDR + 0.05 * zNet) AS team_score
                     FROM team_normalized), # KPI for evaluating teams

     team_starters AS (SELECT *
                       FROM (SELECT r.*,
                                    ROW_NUMBER() OVER (
                                        PARTITION BY season, team_id, position
                                        ORDER BY raw_score DESC
                                        ) AS rn
                             FROM raw_scores r) as x
                       WHERE rn = 1)

SELECT p.season,
       Players.name                                                  AS player_name,
       p.position,
       Teams1.name                                                   AS current_team,
       Teams2.name                                                   AS destination_team,
       cur.standing                                                  AS current_standing,
       dst.standing                                                  AS destination_standing,
       ROUND(p.raw_score, 3)                                         AS player_rating,
       ROUND(s.raw_score, 3)                                         AS destination_player_rating,
       ROUND(dst.team_score - cur.team_score, 3)                     AS team_improvement,
       ROUND(GREATEST(s.raw_score - p.raw_score, 0), 3)              AS player_gap,
        # AcceptanceScore=e^(−0.15×max(Gap,0))
       # 0 < AcceptanceScore <= 1 ---> تفسیر ساده
       ROUND(EXP(-0.15 * GREATEST(s.raw_score - p.raw_score, 0)), 3) AS acceptance_score,

       # recommendation_score = 0.60 * team_improvement + 0.4 * acceptance_score
       # Higher recommendation_score --> better choice
       ROUND(
               0.60 * (dst.team_score - cur.team_score)
                   + 0.40 * EXP(-0.15 * GREATEST(s.raw_score - p.raw_score, 0)),
               3
       )                                                             AS recommendation_score

FROM raw_scores p
         JOIN team_scores cur
              ON cur.team_id = p.team_id
                  AND cur.season = p.season
         JOIN team_starters s
              ON s.season = p.season
                  AND s.position = p.position
                  AND s.team_id != p.team_id
         JOIN team_scores dst
              ON dst.team_id = s.team_id
                  AND dst.season = s.season
         JOIN Players
              ON Players.player_id = p.player_id
         JOIN Teams Teams1
              ON Teams1.team_id = p.team_id
         JOIN Teams Teams2
              ON Teams2.team_id = s.team_id

WHERE dst.team_score > cur.team_score and p.season = 2025
ORDER BY p.season,
         Players.name,
         recommendation_score DESC;