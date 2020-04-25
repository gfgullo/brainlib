
class MatchesMessage:
    """
    Errori generli di match usati molto su random_match
    """
    random_await_match = {"status": "await"}, 200
    random_create_match = {"status": "create_with_fbid_or_uid_or_username"}, 200
    random_avoid_match = {"status": "avoid"}, 200
    abort_avoid_match = {"status": "abort_avoid"}, 200

    @staticmethod
    def create_random_match(doc_id=False):
        """
        Questo metodo provvedde a creare il match, in questo caso torna anche l'id passato.
        :param doc_id:
        :return:
        """
        return {"status": "create_with_fbid_or_uid_or_username", "id": doc_id}, 200


class ErrorRounds:
    match_not_exist = {"error": "Match not found"}, 404
    no_uid_found = {"error": "your uid is not found"}, 404
    riddle_not_fount = {"error": "riddle is not found"}, 404
    no_help_found = {"error": "help is not found"}, 404
    help_used = {"error": "the help is not available"}, 403
    match_close = {"error": "match closed or you in await zone"}, 403