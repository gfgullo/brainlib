
class ErrorMessage:
    """
    Errori di network, o intestazioni errate
    """
    bad_request = ({"error": "Bad Request, please read documentation"}), 400
    method_not_allowed = ({"error": "Method not Allowed"}), 405
    error_no_token = ({"error": "Authorization in header is empty or expired"})
    you_are_in_await_area = ({"error": "you are in await area"})


class ErrorSinginMessage:
    you_are_banned = ({"error": "you are banned!"}), 403


class ErrorUserName:
    username_already = ({"error": "username already exists!!", "result": False}), 403
    username_not_correct = ({"error": "username not correct", "result": False}), 403


class ErrorUserInfo:
    user_not_exist = ({"error": "user not exist"}), 404
