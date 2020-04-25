from google.cloud.firestore import Client, DocumentReference
from typing import List


class _BaseUser:
    uid: str

    def reporting_user(self, db: Client):
        reference: DocumentReference = db.collection("settings").document("users")
        document: dict = reference.get().to_dict()
        if document is not None:
            list_of_users: list = document.get("reporting_users", [])
            if self.uid not in list_of_users:
                list_of_users.append(self.uid)
                reference.set({"reporting_users": list_of_users}, merge=True)


class PublicEnigmiUser(_BaseUser):
    def __init__(self, raw_user: dict):
        self.uid = raw_user.get('uid', None)
        self.fbid = raw_user.get('fbid', None)
        self.username = raw_user.get('username', None)
        self.stats = raw_user.get('stats', {'won': 0, 'loss': 0})
        self.points = raw_user.get('points', 0)
        self.avatar = raw_user.get("avatar", None)
        self.position = raw_user.get("position", 0)

    def to_dict(self):
        return {
            "avatar": self.avatar,
            "fbid": self.fbid,
            "uid": self.uid,
            "points": self.points,
            "stats": self.stats,
            "username": self.username,
            "position": self.position
        }

    def __str__(self):
        return self.username

    def __ge__(self, other):
        return self.points >= other.points

    def __gt__(self, other):
        return self.points > other.points

    def __lt__(self, other):
        return self.points < other.points

    def __eq__(self, other):
        return self.points == self.points

    def __le__(self, other):
        return self.points <= other.points


class EnigmiUser(PublicEnigmiUser):
    devices: List[str] = []

    def __init__(self, raw_user: dict, db=Client()):
        super().__init__(raw_user)
        self.__db = db
        self.email = raw_user.get('email', None)
        self.devices: List[str] = list(raw_user.get('devices', []))

    def save(self, ):
        self.__db.collection("users").document(self.uid).set(self.to_dict(), merge=True)

    # def coins_plus(self, save=False):
    #     """
    #     Aggiunge semplicemente uno ai coins dell'utente, è stata fatta una funzione per fare questo
    #     lavoro semplicemente perché si prevedono "poteri" e aggiunte di comportamento,
    #     questa funzione non si occupa del salvattagio dell'utente se non espresso nel parametro
    #     "save=True"
    #     :return:
    #     """
    #     plus_coins = 1
    #     self.coins += plus_coins
    #     if save:
    #         self.save()
    #     return plus_coins

    def to_dict(self):
        public_user_dict = super().to_dict()
        public_user_dict.update({
            "devices": self.devices,
            "email": self.email,
        })
        return public_user_dict


class FirebaseUser(_BaseUser):
    """
    Firebase User.
    """
    def __init__(self, user_dict: dict):
        self.email = user_dict.get('email', None)
        self.email_check = user_dict.get('email_verified', None)
        self.uid = user_dict.get('uid', None)
        self.original = user_dict

    def to_dict(self):
        return self.original


class FacebookUser(PublicEnigmiUser):

    def __init__(self, raw_user: dict):
        super().__init__(raw_user)
        self.name = raw_user.get("name", None)
        self.won = raw_user.get("stats", {}).get("won", 0)
        self.loss = raw_user.get("stats", {}).get("loss", 0)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "name": self.name,
            "won": self.won,
            "loss": self.loss,
        })
        return result
