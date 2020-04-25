from google.cloud.firestore import Client as FirestoreClient
from google.cloud.error_reporting import Client as ReporterClient
from .users.struct_users import EnigmiUser
from firebase_admin import messaging
from .matches.Time import Time
import re
import sys
import flask
from typing import Dict, Tuple

MAX_CHALLENGE_FOR_ACCOUNT = 14


class ReportError:
    def __init__(self, client: ReporterClient):
        self.__reporter = client

    def report(self, value):
        print(str(value), file=sys.stderr)
        self.__reporter.report(message=str(value))


class UtilsUsers:
    __error: ReporterClient = None

    def __init__(self, db: FirestoreClient, timer=Time(), error_reporting: ReporterClient = None):
        self.__db = db
        self.__time = timer
        self.__error = error_reporting

    def is_outside_challenge(self, uid: str) -> int:
        """
        Questa funzione si occupa di verificare dato un uID il numero di sfide in corso.
        evitanto l'invio e restituendo un messaggio di errore nel caso che uno dei
        due giocatori è andato oltre il limite di Challenge previste, di default 15
        ma con possibilità di cambiare questo valore settando DEADLINE_REQUEST vedi doc. completa.

        :param uid:
        :return:
        """
        total = 0
        db = self.__db
        for _ in db.collection("matches")\
                .where("users", "array_contains", uid)\
                .where("time_end", ">", self.__time.now).stream():
            total += 1
        for _ in db.collection("requests_matches").where("users", "array_contains", uid).stream():
            total += 1

        return total > int(MAX_CHALLENGE_FOR_ACCOUNT)

    def send_notification(self, uid: str, title: str, text: str):
        user = self.__db.collection("users").document(uid).get().to_dict()
        if user is not None:
            __enigmi_user = EnigmiUser(user, db=self.__db)
            notification = messaging.Notification(title=title, body=text)
            for token in user.get("devices", []):
                message = messaging.Message(notification=notification, token=token)
                try:
                    messaging.send(message=message)
                except Exception as e:
                    if str(e) == "Requested entity was not found." or str(e) == "SenderId mismatch":
                        print("Sto togliendo questo token: {}\n da questo utente: {} con questo errore:".format(
                            __enigmi_user.uid, token, str(e)))
                        __enigmi_user.devices.remove(token)
                        __enigmi_user.save()
                    else:
                        mess = "Error: {}  Uid:{}  token: {}".format(e, uid, token)
                        if self.__error is not None:
                            self.__error.report(mess)
                        print(mess, file=sys.stderr)


def username_is_correct(username: str) -> bool:
    """
    Questa funzione rispetta le regole dell'usrname e ritorna True|False
    :param username:
    :return:
    """
    username = username.lower()
    if 3 > len(username) < 20:
        return False

    if username.startswith(".") or username.endswith("."):
        return False

    r = re.match("[a-z0-9_]", username)
    if r is None:
        return False
    return True


def generate_response(data: Tuple[Dict, int]) -> Tuple[flask.Response, int]:
    return flask.jsonify(data[0]), data[1]