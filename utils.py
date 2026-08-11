"""
This is meant to all be configured to meet the end users needs.
"""
import bcrypt


def save_token(token: str) -> None:
    """Use this to save the hashed token somewhere for later reference"""
    pass


def ingest(data: str) -> None:
    """Use this to directly ingest data into a database"""
    pass


def authenticate(request) -> bool:
    """Use this to authenticate the user. Use request.authentication.token for the token used.
        You can also use data from the json itself if you want, ie steam id"""
    # bcrypt.checkpw(request.authenticate.token, my_hashed_token) -> bool
    return True
