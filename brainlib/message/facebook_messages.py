
class FacebookError:
    no_token = ({"error": "facebook token not exists"}), 403
    error_response_facebook = ({"error": "facebook response error"}), 403
    json_decode = ({"error": "json decode error"}), 403