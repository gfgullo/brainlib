
class RequestMatchError:
    user_not_found = ({"status": "user not found"}), 404
    challenge_yourself = ({"status": "challenges with yourself are not allowed"}), 403
    already_challenge = ({"status": "already there is a challenge"}), 400
    not_found_challenge = ({"status": "not found challenge"}), 404

    @staticmethod
    def over_challenge(username=None):
        if username:
            return ({"status": "over", "message": "{} ha troppe sfide!".format(username)}), 403
        else:
            return ({"status": "over", "message": "hai troppe sfide!"}), 403


class RequestMatchMessage:
    @staticmethod
    def create_match(match: dict):
        match.update({"status": "success"})
        return match, 200

    abort_request_match = ({"status": "abort"}), 200
    avoid_request_match = ({"status": "avoid"}), 200
