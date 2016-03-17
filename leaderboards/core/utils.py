from memoize import memoize
from django.apps import apps


@memoize(timeout=60)
def rank_flea_teams_by_league(league):
    clsFleaTeam = apps.get_model('teams.FleaTeam')
    raw_query = clsFleaTeam.objects.raw(
        """
        SELECT id, overall_pts, RANK() OVER(ORDER BY overall_pts DESC) AS overall_rank,
          rank_fgpct100, rank_ftpct100, rank_3pt, rank_reb, rank_stl, rank_blk, rank_ast, rank_to, rank_pts
        FROM
        (
          SELECT *,
            COALESCE(rank_fgpct100, 0) +
            COALESCE(rank_ftpct100, 0) +
            COALESCE(rank_3pt, 0) +
            COALESCE(rank_reb, 0) +
            COALESCE(rank_stl, 0) +
            COALESCE(rank_blk, 0) +
            COALESCE(rank_ast, 0) +
            COALESCE(rank_to, 0) +
            COALESCE(rank_pts, 0) as overall_pts
          FROM
          (
            SELECT *,
              RANK() OVER(ORDER BY stat_fgpct100 ASC) AS rank_fgpct100,
              RANK() OVER(ORDER BY stat_ftpct100 ASC) AS rank_ftpct100,
              RANK() OVER(ORDER BY stat_3pt ASC) AS rank_3pt,
              RANK() OVER(ORDER BY stat_reb ASC) AS rank_reb,
              RANK() OVER(ORDER BY stat_stl ASC) AS rank_stl,
              RANK() OVER(ORDER BY stat_blk ASC) AS rank_blk,
              RANK() OVER(ORDER BY stat_ast ASC) AS rank_ast,
              RANK() OVER(ORDER BY stat_to DESC) AS rank_to,
              RANK() OVER(ORDER BY stat_pts ASC) AS rank_pts
            FROM teams_fleateam
            WHERE league_id = %s::uuid
          ) AS statrank
        ) AS overallrank""",
        [league])
    ret = {}
    for ft in raw_query:
        ret.update({ft.id: ft})
    return ret


@memoize(timeout=60)
def rank_flea_teams_by_division(division):
    clsFleaTeam = apps.get_model('teams.FleaTeam')
    raw_query = clsFleaTeam.objects.raw(
        """
        SELECT id, overall_pts, RANK() OVER(ORDER BY overall_pts DESC) AS overall_rank,
          rank_fgpct100, rank_ftpct100, rank_3pt, rank_reb, rank_stl, rank_blk, rank_ast, rank_to, rank_pts
        FROM
        (
          SELECT *,
            COALESCE(rank_fgpct100, 0) +
            COALESCE(rank_ftpct100, 0) +
            COALESCE(rank_3pt, 0) +
            COALESCE(rank_reb, 0) +
            COALESCE(rank_stl, 0) +
            COALESCE(rank_blk, 0) +
            COALESCE(rank_ast, 0) +
            COALESCE(rank_to, 0) +
            COALESCE(rank_pts, 0) as overall_pts
          FROM
          (
            SELECT *,
              RANK() OVER(ORDER BY stat_fgpct100 ASC) AS rank_fgpct100,
              RANK() OVER(ORDER BY stat_ftpct100 ASC) AS rank_ftpct100,
              RANK() OVER(ORDER BY stat_3pt ASC) AS rank_3pt,
              RANK() OVER(ORDER BY stat_reb ASC) AS rank_reb,
              RANK() OVER(ORDER BY stat_stl ASC) AS rank_stl,
              RANK() OVER(ORDER BY stat_blk ASC) AS rank_blk,
              RANK() OVER(ORDER BY stat_ast ASC) AS rank_ast,
              RANK() OVER(ORDER BY stat_to DESC) AS rank_to,
              RANK() OVER(ORDER BY stat_pts ASC) AS rank_pts
            FROM teams_fleateam
            WHERE id IN (
              SELECT "teams_fleateam"."id"
              FROM "teams_fleateam"
              INNER JOIN "leagues_flealeague"
              ON ("teams_fleateam"."league_id" = "leagues_flealeague"."id")
              WHERE "leagues_flealeague"."division_id" = %s::uuid
            )
          ) AS statrank
        ) AS overallrank""",
        [division])
    ret = {}
    for ft in raw_query:
        ret.update({ft.id: ft})
    return ret


def get_team_from_division_list(division, team_id):
    teams = rank_flea_teams_by_division(division)
    return teams[team_id]


def get_team_from_league_list(league, team_id):
    teams = rank_flea_teams_by_league(league)
    return teams[team_id]
