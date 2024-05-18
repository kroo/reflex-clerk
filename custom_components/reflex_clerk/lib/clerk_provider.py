import json
import logging
import os
import typing
from typing import List, Union

import reflex as rx
from authlib.jose import jwt, JoseError, JWTClaims
from reflex import Component, ImportVar
from reflex.utils.serializers import serializer

from reflex_clerk.clerk_client import clerk_client, clerk_response_models
from reflex_clerk.clerk_client.clerk_client import ClerkAPIClient


@serializer
def serialize_exception(e: Exception) -> dict:
    return {"error": str(e)}


@serializer
def serialize_clerk_user(user: clerk_response_models.User) -> dict:
    return user.dict()


class ClerkState(rx.State):
    """
    A Reflex state object representing the current authenticated session and user;
    use this state to render details about the currently logged in user.

    Example:
        ```python
        import reflex_clerk as clerk

        clerk.signed_in(
            rx.cond(
                ClerkState.user.has_image,
                rx.chakra.avatar(
                    src=ClerkState.user.image_url,
                    name=ClerkState.user.first_name,
                    size="xl",
                ),
            )
        )
        ```

    Example:
        ```python
        import reflex_clerk as clerk

        clerk.protect(
            rx.fragment("You are logged in as ", clerk.ClerkState.user.first_name),
            fallback=rx.text("You need to sign in first!"),
        )
        ```


    """

    is_signed_in: bool = False
    """
    True if the user is signed in, False otherwise.
    
    This field is only set to true after server-side validation of the session is complete.
    Check if this is true before returning sensitive user state from other states.
    
    Example:
        ```python
        rx.cond(
            clerk.ClerkState.is_signed_in,
            rx.text("You are signed in"),
            rx.text("You are signed out")
        )
        ```
        
        _Consider using [reflex_clerk.signed_in][] and [reflex_clerk.signed_out][] instead
        to render different information based on if the user is signed in or not on the client
        side instead of on the server._

    """

    auth_error: typing.Optional[Exception] = None
    """
    Non-None if the user authentication process failed.
    
    This should be quite rare, and likely indicates an expired session.
    """

    claims: typing.Optional[JWTClaims] = None
    """
    This field contains the decoded JWT Session claims once server-side validation
    of the session is complete.  You can use
    [Clerk JWT Templates](https://clerk.com/docs/backend-requests/making/jwt-templates)
    to return additional information about the session to this field.
    """

    user_id: typing.Optional[str] = None
    """
    A variable representing the Clerk User ID of the currently logged in user.
    
    This field is only set to true after server-side validation of the session is complete.
    """

    user: typing.Optional[clerk_response_models.User] = None
    """
    A variable representing the Clerk User of the currently logged in user.

    This field is only set to true after server-side validation of the session is complete,
    and can be disabled for performance reasons using [set_fetch_user_on_auth][reflex_clerk.ClerkState.set_fetch_user_on_auth].
    """

    # static class variables
    _jwt_public_keys: List[typing.Dict[str, str]] = []
    _secret_key: str = None
    _clerk_api_client: ClerkAPIClient = None
    _fetch_user: bool = True

    # noinspection PyPropertyDefinition
    @classmethod
    @property
    def secret_key(cls) -> str:
        if cls._secret_key is None:
            if 'CLERK_SECRET_KEY' in os.environ:
                cls._secret_key = os.environ['CLERK_SECRET_KEY']

        return cls._secret_key

    # noinspection PyPropertyDefinition
    @classmethod
    @property
    def jwt_public_keys(cls) -> typing.List[typing.Dict[str, str]]:
        if not cls._jwt_public_keys:
            if 'CLERK_JWT_PUBLIC_KEYS' in os.environ:
                cls._jwt_public_keys = list(map(json.loads, os.environ['CLERK_JWT_PUBLIC_KEYS'].split(',')))
            if cls.secret_key and cls.clerk_api_client:
                cls._jwt_public_keys = cls._clerk_api_client.get_jwks().dict()['keys']
        return cls._jwt_public_keys

    # noinspection PyPropertyDefinition
    @classmethod
    @property
    def clerk_api_client(cls) -> clerk_client.ClerkAPIClient:
        if cls._clerk_api_client is None:
            cls._clerk_api_client = clerk_client.get_client(cls.secret_key)
        return cls._clerk_api_client

    @classmethod
    def set_fetch_user_on_auth(cls, fetch_user: bool):
        """
        This method is used to control whether the authenticating user should be
        fetched from Clerk upon successful authentication.

        Defaults to true; set this to False if the Clark User object is not being
        used, as it saves a backend call to Clark every time a user authenticates.

        Note:
            Setting this to True only fetches ClerkState.user once at the time of
            user authentication. This implementation doesn't automatically detect
             and update any changes in the underlying user object data, such as
            email address modifications. Therefore, to ensure you have the latest
            user data while logged in, especially if changes have been made, you
            should use the ClerkState.fetch_user reflex event to manually refresh
            the user data.

        Args:
            fetch_user (bool): Indicates whether the user should be fetched.
        """
        cls._fetch_user = fetch_user

    def set_clerk_session(self, token: str) -> None:
        """
        Validates a Clerk session token and optionally fetches the associated
        user object.  This is used internally by reflex_clerk to manage the
        current auth state of users: it is called by the frontend whenever
        the Clerk isSignedIn auth state changes from false to true.

        Args:
            token: A JWT token used to authenticate and authorize the user.
        """
        if not ClerkState._jwt_public_keys:
            print(f"No Clerk JWT public keys found. Skipping Clerk session set.")
            return

        try:
            decoded: JWTClaims = jwt.decode(token, {"keys": ClerkState.jwt_public_keys})
            self.is_signed_in = True
            self.claims = decoded
            self.user_id = decoded.get('sub')

            if self._fetch_user:
                self.fetch_user()

        except JoseError as e:
            self.auth_error = e
            logging.warning(f"Auth error: {e}")

    def clear_clerk_session(self):
        """
        Clears the clerk session by setting the sign-in status to False,
        resetting the claims to None, and clearing any authentication errors.

        This is used internally by reflex_clerk to manage the
        current auth state of users: it is called by the frontend whenever
        the Clerk isSignedIn auth state changes from true to false.


        :param self: The current instance of the class.
        """
        self.is_signed_in = False
        self.claims = None
        self.auth_error = None

    def clear_clerk_auth_error(self):
        """
        Clears the clerk authentication error.

        This method sets the `auth_error` attribute of the current instance to `None`.
        """
        self.auth_error = None

    def fetch_user(self):
        """
        Fetches ClerkState.user from the clerk backend API, using
        ClerkState.user_id.  Use this Reflex event if you want to force
        update the clerk user data after a user logs in (such as after modifying
        their account profile).
        """
        if self.user_id:
            user = self.clerk_api_client.get_user(self.user_id)
            self.set_user(user)


class ClerkSessionSynchronizer(rx.Component):
    """ClerkSessionSynchronizer component."""
    tag = "ClerkSessionSynchronizer"

    def add_imports(self) -> dict[str, Union[str, ImportVar, list[Union[str, ImportVar]]]]:
        addl_imports = {
            "@clerk/clerk-react": ["useAuth"],
            "react": ["useContext", "useEffect"],
            "/utils/context": ["EventLoopContext"],
            "/utils/state": ["Event"]
        }
        return addl_imports

    def add_custom_code(self) -> list[str]:
        return [
            """
function ClerkSessionSynchronizer({ children }) {
  const { getToken, isLoaded, isSignedIn } = useAuth()
  const [ addEvents, connectErrors ] = useContext(EventLoopContext)

  useEffect(() => {
      if (isLoaded && !!addEvents) {
        if (isSignedIn) {
          getToken().then(token => {
            addEvents([Event("state.clerk_state.set_clerk_session", {token})])
          })
        } else {
          addEvents([Event("state.clerk_state.clear_clerk_session")])
        }
      }
  }, [isSignedIn])      

  return (
      <>{children}</>
  )
}
"""
        ]


class ClerkProvider(rx.Component):
    """ClerkProvider component."""

    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "ClerkProvider"

    publishable_key: str = None
    """
    The Clerk publishable key for your instance. This can be found in your
    Clerk Dashboard on the [API Keys][1] page.
    
    https://dashboard.clerk.com/last-active?path=api-keys
    """

    secret_key: str = None
    """
    The Clerk publishable key for your instance. This can be found in your
    Clerk Dashboard on the [API Keys][1] page.  This key should never be
    exposed to the client, and will be stripped from this tag's props before
    rendering.
    
    https://dashboard.clerk.com/last-active?path=api-keys
    """

    router_push: rx.EventHandler[lambda e: [e]]
    """A function which takes the destination path as an argument and performs a "push" navigation."""

    router_replace: rx.EventHandler[lambda e: [e]]
    """A function which takes the destination path as an argument and performs a "replace" navigation."""

    clerk_j_s_url: str = None
    """Define the URL that @clerk/clerk-react should hot-load @clerk/clerk-js from."""

    clerk_j_s_variant: str = None
    """
    If your web application only uses Control components, you can set this value to
    headless and load a minimal ClerkJS bundle for optimal page performance.
    """

    clerk_j_s_version: str = None
    """Define the npm version for @clerk/clerk-js."""

    support_email: str = None
    """
    Optional support email for display in authentication screens. Will only affect
    Clerk Components and not Account Portal pages
    """

    appearance: dict = None
    """
    Optional object to style your components. Will only affect Clerk Components
    and not Account Portal pages.
    """

    localization: dict = None
    """
    Optional object to localize your components. Will only affect Clerk Components
    and not Account Portal pages.
    """

    allowed_redirect_origins: typing.List[str] = None
    """
    Optional array of domains used to validate against the query param of an auth
    redirect. If no match is made, the redirect is considered unsafe and the default
    redirect will be used with a warning passed to the console.
    """

    sign_in_force_redirect_url: str = None
    """
    If provided, this URL will always be redirected to after the user signs in. It's
    recommended to use the environment variable instead.
    """

    sign_up_force_redirect_url: str = None
    """
    If provided, this URL will always be redirected to after the user signs up. It's
    recommended to use the environment variable instead.
    """

    sign_in_fallback_redirect_url: str = None
    """
    The fallback URL to redirect to after the user signs in, if there's no redirect_url
    in the path already. Defaults to /. It's recommended to use the environment variable
    instead.
    """

    sign_up_fallback_redirect_url: str = None
    """
    The fallback URL to redirect to after the user signs up, if there's no redirect_url
    in the path already. Defaults to /. It's recommended to use the environment variable
    instead.
    """

    is_satellite: bool = None
    """This option defines that the application is a satellite application"""

    domain: str = None
    """
    This option sets the domain of the satellite application. If your application is a
    satellite application, this option is required.
    """

    sign_in_url: str = None
    """
    This URL will be used for any redirects that might happen and needs to point to
    your primary application. This option is optional for production instances and
    required for development instances. It's recommended to use the environment variable
    instead.
    """

    telemetry: bool = None
    """Controls whether or not Clerk will collect telemetry data."""

    @classmethod
    def create(cls, *children, **props) -> 'ClerkProvider':
        # Copy secret key to ClerkState, then remove it from the props to
        # avoid passing it to the client.
        if props.get('secret_key'):
            ClerkState._secret_key = props['secret_key']
            del props['secret_key']

        # Check that at this point we have a secret key either passed as a
        # prop or set as an environment variable.
        if not ClerkState.secret_key:
            raise ValueError(
                "ClerkProvider requires a secret_key.  You can set this by passing "
                "it as a keyword argument to the clerk_provider component or by "
                "setting the CLERK_SECRET_KEY environment variable.\n\nThis can "
                "be found in your Clerk Dashboard on the API Keys page:\n"
                "https://dashboard.clerk.com/last-active?path=api-keys")

        if not props.get('publishable_key'):
            props['publishable_key'] = os.environ.get('CLERK_PUBLISHABLE_KEY')

        if not props['publishable_key']:
            raise ValueError(
                "ClerkProvider requires a publishable_key.  You can set this by passing "
                "it as a keyword argument to the clerk_provider component or by "
                "setting the CLERK_PUBLISHABLE_KEY environment variable.\n\nThis can "
                "be found in your Clerk Dashboard on the API Keys page:\n"
                "https://dashboard.clerk.com/last-active?path=api-keys")

        # Create a synchronizer and wrap it in a ClerkProvider.
        synchronizer = ClerkSessionSynchronizer.create(*children)
        clerk_provider = super().create(synchronizer, **props)

        # Wrap the ClerkProvider in a Fragment, as otherwise the outer provider component
        # seems to be removed occasionally.
        return rx.fragment(clerk_provider)


def clerk_provider(
        *children,
        publishable_key: typing.Optional[str] = None,
        secret_key: typing.Optional[str] = None,
        clerk_j_s_url: typing.Optional[str] = None,
        clerk_j_s_variant: typing.Optional[str] = None,
        clerk_j_s_version: typing.Optional[str] = None,
        support_email: typing.Optional[str] = None,
        appearance: typing.Optional[dict] = None,
        localization: typing.Optional[dict] = None,
        allowed_redirect_origins: typing.Optional[typing.List[typing.Optional[str]]] = None,
        sign_in_force_redirect_url: typing.Optional[str] = None,
        sign_up_force_redirect_url: typing.Optional[str] = None,
        sign_in_fallback_redirect_url: typing.Optional[str] = None,
        sign_up_fallback_redirect_url: typing.Optional[str] = None,
        is_satellite: typing.Optional[bool] = None,
        domain: typing.Optional[str] = None,
        sign_in_url: typing.Optional[str] = None,
        telemetry: typing.Optional[bool] = None,
) -> Component:
    """
    A component which wraps your application and provides a context for Clerk to function.

    This component must be rendered at the root of your application, before any other
    reflex_clerk components.

    Example:
        ```python
        import reflex as rx
        import reflex_clerk as clerk

        @rx.page("/")
        def index(request):
            return clerk.clerk_provider(

                # ... Child components...

                publishable_key="pk_test_123",
                secret_key="sk_test_123",
            )
        ```

    Args:
        publishable_key: The publishable key used to initialize Clerk. This can be passed either as a prop or set as the `CLERK_PUBLISHABLE_KEY` environment variable.
        secret_key: The secret key used to call out to the clerk API from the backend. This can be passed either as a prop or set as the `CLERK_SECRET_KEY` environment variable.

    Other Args:
        clerk_j_s_url: The URL that @clerk/clerk-react should hot-load @clerk/clerk-js from.
        clerk_j_s_variant: The variant of @clerk/clerk-js to load. Defaults to the latest version.
        clerk_j_s_version: The version of @clerk/clerk-js to load. Defaults to the latest version.
        support_email: Optional support email for display in authentication screens. Will only affect Clerk Components and not Account Portal pages.
        appearance: Optional object to style your components. Will only affect Clerk Components and not Account Portal pages.
        localization: Optional object to localize your components. Will only affect Clerk Components and not Account Portal pages.
        allowed_redirect_origins: Optional array of domains used to validate against the query param of an auth redirect. If no match is made, the redirect is considered unsafe and the default redirect will be used with a warning passed to the console.
        sign_in_force_redirect_url: If provided, this URL will always be redirected to after the user signs in. It's recommended to use the environment variable instead.
        sign_up_force_redirect_url: If provided, this URL will always be redirected to after the user signs up. It's recommended to use the environment variable instead.
        sign_in_fallback_redirect_url: The fallback URL to redirect to after the user signs in, if there's no redirect_url in the path already. Defaults to /. It's recommended to use the environment variable instead.
        sign_up_fallback_redirect_url: The fallback URL to redirect to after the user signs up, if there's no redirect_url in the path already. Defaults to /. It's recommended to use the environment variable instead.
        is_satellite: This option defines that the application is a satellite application.
        domain: This option sets the domain of the satellite application. If your application is a satellite application, this option is required.
        sign_in_url: This URL will be used for any redirects that might happen and needs to point to your primary application. This option is optional for production instances and required for development instances. It's recommended to use the environment variable instead.
        telemetry: Controls whether or not Clerk will collect telemetry data.

    Returns:
        ClerkProvider: A new instance of ClerkProvider.
    """
    return ClerkProvider.create(
        *children,
        publishable_key=publishable_key,
        secret_key=secret_key,
        clerk_j_s_url=clerk_j_s_url,
        clerk_j_s_variant=clerk_j_s_variant,
        clerk_j_s_version=clerk_j_s_version,
        support_email=support_email,
        appearance=appearance,
        localization=localization,
        allowed_redirect_origins=allowed_redirect_origins,
        sign_in_force_redirect_url=sign_in_force_redirect_url,
        sign_up_force_redirect_url=sign_up_force_redirect_url,
        sign_in_fallback_redirect_url=sign_in_fallback_redirect_url,
        sign_up_fallback_redirect_url=sign_up_fallback_redirect_url,
        is_satellite=is_satellite,
        domain=domain,
        sign_in_url=sign_in_url,
        telemetry=telemetry)
