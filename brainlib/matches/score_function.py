
def compute_score(match, debug=False) -> int:
    score = 0

    for r in match["rounds"]:

        t = r["resolved_in"]

        if t is None:
            if debug:
                print("Round not resolved")
            continue

        t_norm = t / 3600

        if t < 10:
            multiplier = 3  # se ha impiegato meno di 10 secondi
        elif t < 60:
            multiplier = 2.  # se ha impiegato meno di un minuto
        elif t < 3600:
            multiplier = 1.5  # se ha impiegato meno di un'ora
        else:
            multiplier = 1.  # se ha impiegato più di un'ora

        r_score = (100 - t_norm) * multiplier - 10 * r["errors"]

        if r_score > 0:
            score += r_score

        if debug:
            print("Score for round = %d" % r_score)

    if match["won"]:
        score *= 2

    return round(score)

