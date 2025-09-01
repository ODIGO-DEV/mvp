from authlib.integrations.flask_client import OAuth
from flask import current_app, url_for

from .base import OAuthSignIn

oauth = OAuth(current_app)


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super().__init__("google")
        self.service = oauth.register(
            name="google",
            client_id=current_app.config.get("GOOGLE_CLIENT_ID"),
            client_secret=current_app.config.get("GOOGLE_CLIENT_SECRET"),
            access_token_url="https://accounts.google.com/o/oauth2/token",
            access_token_params=None,
            authorize_url="https://accounts.google.com/o/oauth2/auth",
            authorize_params=None,
            api_base_url="https://www.googleapis.com/oauth2/v1/",
            client_kwargs={"scope": "openid email profile"},
        )

    def authorize(self):
        redirect_uri = url_for("auth.callback", provider="google", _external=True)
        return self.service.authorize_redirect(redirect_uri)

    def callback(self):
        token = self.service.authorize_access_token()
        user_info = self.service.parse_id_token(token)
        return user_info
