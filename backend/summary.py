def summarize_basic(results):
    """
    Simple summary logic:
    - cheapest flight
    - fastest flight
    - best overall (same as cheapest)
    """

    if not results:
        return None, None, None

    cheapest = min(results, key=lambda x: x.get("price", 999999))
    fastest = min(results, key=lambda x: x.get("total_duration", 999999))
    best = cheapest  # basic rule for now

    return cheapest, fastest, best
