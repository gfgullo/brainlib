from .Round import Round


class User:
    def __init__(self, raw: dict):
        self.current_match = raw.get("current_match", 0)
        self.username = raw.get("username")
        self.rounds = []
        for i in raw.get("rounds", []):
            self.rounds.append(Round(i))
        self.uid = raw.get("uid")
        self.points: int = 0
        self.winner: bool = False
        self.score: int = 0

    def to_dict(self) -> dict:

        rounds = []
        for i in self.rounds:
            rounds.append(i.to_dict())

        return {
            "current_match": self.current_match,
            "username": self.username,
            "uid": self.uid,
            "rounds": rounds
        }

    def get_current_round(self) -> Round:
        """
        Questo metodo ritorna il current_round, il current round è studiato apposta
        per evitare index_overflow. Quindi se il round è completato per l'utente
        il get_current_round tornerà sempre 2
        :return:
        """
        if self.current_match > 2:
            return self.rounds[2]
        else:
            return self.rounds[self.current_match]

