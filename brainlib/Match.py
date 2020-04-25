from google.cloud.firestore import (DocumentReference, Client)

from .matches.Time import Time
from .matches.User import User
from .matches.Riddle import Riddle
from .users import struct_users
from .matches.score_function import compute_score

from typing import Union


class Match:
    def __init__(self, raw: dict, db: Client):
        self.match_id = raw.get("match_id", None)
        self.list_users = raw.get("users", [])
        self.close = raw.get("close", False)
        self.__db: Client = db
        self.users = []
        self.time = Time()
        for i in self.list_users:
            self.users.append(User(raw.get(i, {})))

        self.riddles = []
        for i in raw.get("riddles", []):
            self.riddles.append(Riddle(i))

    def to_dict(self) -> dict:

        riddles = []
        for i in self.riddles:
            riddles.append(i.to_dict())
        return {
            "match_id": self.match_id,
            "users": self.list_users,
            "riddles": riddles,
            "close": self.close,
            self.users[0].uid: self.users[0].to_dict(),
            self.users[1].uid: self.users[1].to_dict(),
        }

    def fake_complete(self):
        """
        Questa funzione si occupa della coerenza dei timestamp dei match
        si occupa di aprire e chiudere i round qual'ora questi siano scaduti e sono senza risposta
        :return:
        """
        now = int(self.time.now)
        # per ogni utente
        for user in self.users:

            # per ogni round
            for r in user.rounds:
                if now > r.when_deadline() and r.time_end == 0:
                    r.close(tick=r.when_deadline())
                    # il round è stato chiuso aggiorno il current dell'user
                    user.current_match += 1
                    # controllo se ci sono round successivi
                    if user.current_match <= 2:
                        # se ci sono lo apro
                        self.open_rounds(tick=r.when_deadline())

    def open_rounds(self, tick=None):
        """
        apre il round a entrambi gli utenti
        :return:
        """
        user1 = self.users[0]
        user2 = self.users[1]
        if tick is None:
            tick = int(self.time.now)

        user2.get_current_round().open(tick=tick)
        user1.get_current_round().open(tick=tick)

    def close_match(self):
        """
        Questo metodo di occupa di segnare i punti nell'account degli utenti.
        :return:
        """
        self.fake_complete()
        if self.users[0].current_match > 2 and self.users[1].current_match > 2:
            self.match_score()
            self.close = True
            for user in self.users:
                if self.__get_loser() is not None:
                    if self.__get_loser().uid == user.uid:
                        user.winner = False
                if self.__get_winner() is not None:
                    if self.__get_winner().uid == user.uid:
                        user.winner = True

                if self.__get_winner() is None and self.__get_loser() is None:
                    draw = True
                else:
                    draw = False

                user.points = Match.__get_points(user)
                reference_user: DocumentReference = self.__db.collection("users").document(user.uid)
                user_dict = reference_user.get().to_dict()
                if user_dict is not None:
                    e = struct_users.EnigmiUser(user_dict)
                    won = e.stats.get("won", 0)
                    loss = e.stats.get("loss", 0)
                    # Qui controllo se il match è in pareggio
                    if draw is False:
                        if user.winner:
                            won += 1
                        else:
                            loss += 1
                    reference_user.set({
                        "points": e.points + user.points,
                        "stats": {
                            "won": won,
                            "loss": loss
                        }}, merge=True)

    @staticmethod
    def __get_points(user: User) -> int:
        '''
        computa il punteggio ogni classe User ha una variabile interna points
        e ogni variabile interna points viene calibrata da questa funzione
        :param user:
        :return:
        '''

        fake_round = []
        for r in user.rounds:
            result = r.resolved_in()
            if result is not None and result > 0:
                fake_round.append({"resolved_in": result, "errors": r.errors})

        return compute_score({
            "rounds": fake_round,
            "won": user.winner
        })

    def get_user(self, uid: str):
        for user in self.users:
            if user.uid == uid:
                return user

        return None

    def match_score(self):
        """
        Calcolo lo Score del Match, come score si intente 0-1 1-0
        quindi il punteggio finale dell'incontro questo è importante
        per segnare e decidere il vincitore del match
        :return:
        """
        user1 = self.users[0]
        user2 = self.users[1]
        user1.score = 0
        user2.score = 0
        for i in range(len(self.users[0].rounds)):
            if user1.rounds[i].resolved() or user2.rounds[i].resolved():
                # controllo se l'utente uno ha risolto mentre l'avversario no
                if user1.rounds[i].resolved() and not user2.rounds[i].resolved():
                    user1.score += 1
                    continue
                # controllo se l'utente 2 ha risolto mentre l'avversario no
                if user2.rounds[i].resolved() and not user1.rounds[i].resolved():
                    user2.score += 1
                    continue

                if user1.rounds[i].resolved_in() > 0 and user2.rounds[i].resolved_in() > 0:
                    if user1.rounds[i].resolved_in() > user2.rounds[i].resolved_in():
                        user2.score += 1
                    elif user1.rounds[i].resolved_in() < user2.rounds[i].resolved_in():
                        user1.score += 1
                    else:
                        continue

    def __get_winner(self) -> Union[None, User]:
        """
        Può ritornare l'utente vincitore o None in caso di pareggio
        :return:
        """
        user1 = self.users[0]
        user2 = self.users[1]
        if user1.score > user2.score:
            return user1
        elif user2.score > user1.score:
            return user2
        else:
            return None

    def __get_loser(self) -> Union[None, User]:
        """
        Ha bisogno di match_score()
        Può ritornare l'utente perdente o None in caso di pareggio
        :return:
        """
        user1 = self.users[0]
        user2 = self.users[1]
        if user1.score < user2.score:
            return user1
        elif user2.score < user1.score:
            return user2
        else:
            return None

    def get_opponent(self, uid: str) -> Union[None, User]:
        for u in self.users:
            if u.uid != uid:
                return u

        return None
