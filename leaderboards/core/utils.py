import ranking


def calculate_rankings(data, reverse=False):
    """Return the rankings dict of the given unsorted {id, points} dict"""

    sorted_ids = sorted(data, key=data.__getitem__, reverse=reverse)
    sorted_points = sorted(data.values(), reverse=reverse)
    rankings = list(ranking.Ranking(sorted_points, start=1, reverse=not reverse))

    flat_rankings = [rank for (rank, _) in rankings]

    return dict(zip(sorted_ids, flat_rankings))
