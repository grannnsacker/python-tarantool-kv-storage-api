import datetime
from ..models.credential import UserCredential
from ..security.conf import ACCESS_TOKEN_EXPIRE_MINUTES
from ..security.utility import authenticate_user, create_access_token


async def login_controller(credential: UserCredential, user_repository):

    """
    Asynchronous controller function for handling user login.

    :param credential: UserCredential object containing the username and password
    provided by the user attempting to log in.
    :param user_repository: UserRepository instance used to interact with the database
                            for user authentication.

    :return: A dictionary containing either an error message or a token upon successful authentication.
    """

    user = await authenticate_user(user_repository, credential.username, credential.password)
    token = create_access_token({"username": user.username}, datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"token": token}
