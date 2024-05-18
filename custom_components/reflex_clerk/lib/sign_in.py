"""Reflex custom component SignIn."""
import typing

import reflex as rx
from reflex.utils.serializers import serializer

from .appearance import Appearance


class SignInInitialValues:
    email_address: str = None
    username: str = None
    phone_number: str = None


@serializer
def serialize_sign_in_initial_values(obj: SignInInitialValues) -> dict:
    return {
        "emailAddress": obj.email_address,
        "username": obj.username,
        "phoneNumber": obj.phone_number,
    }


class SignIn(rx.Component):
    """SignIn component."""

    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "SignIn"

    appearance: Appearance = None
    """
    The appearance of the component.
    """

    routing: typing.Literal['hash', 'path', 'virtual'] = None
    """The routing strategy for your pages.
    
    Defaults to 'path' in Next.js and Remix applications. Defaults to hash for all other SDK's.
    """

    path: str = None
    """
    The path where the component is mounted on when routing is set to path.
    It is ignored in hash- and virtual-based routing.

    For example: /sign-in.
    """

    sign_up_url: str = None
    """
    Full URL or path to the sign up page. Use this property to provide the target of the 
    'Sign Up' link that's rendered. It's recommended to use the environment variable instead.
    """

    force_redirect_url: str = None
    """
    If provided, this URL will always be redirected to after the user signs in. Takes priority
    over deprecated props such as after_sign_in_url and redirect_url. It's recommended to use
    the environment variable instead.
    """

    fallback_redirect_url: str = None
    """
    The fallback URL to redirect to after the user signs in, if there's no redirect_url in the
    path already. Defaults to /. Takes priority over deprecated props such as after_sign_in_url
    and redirect_url. It's recommended to use the environment variable instead.
    """

    sign_up_force_redirect_url: str = None
    """
    If provided, this URL will always be redirected to after the user signs up. Takes priority
    over deprecated props such as afterSignInUrl and redirectUrl. It's recommended to use the
    environment variable instead.
    """

    sign_up_fallback_redirect_url: str = None
    """
    The fallback URL to redirect to after the user signs up, if there's no redirect_url in the 
    path already. Defaults to /. Takes priority over deprecated props such as after_sign_in_url
    and redirect_url. It's recommended to use the environment variable instead.
    """

    initial_values: typing.Optional[SignInInitialValues] = None
    """The values used to prefill the sign-in fields with."""


class SignInButton(rx.Component):
    """SignInButton component."""

    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "SignInButton"

    force_redirect_url: str = None
    """
    If provided, this URL will always be redirected to after the user signs in. Takes priority
    over deprecated props such as after_sign_in_url and redirect_url. It's recommended to use
    the environment variable instead.
    """

    fallback_redirect_url: str = None
    """
    The fallback URL to redirect to after the user signs in, if there's no redirect_url in the
    path already. Defaults to /. Takes priority over deprecated props such as after_sign_in_url
    and redirect_url. It's recommended to use the environment variable instead.
    """

    sign_up_force_redirect_url: str = None
    """
    If provided, this URL will always be redirected to after the user signs up. Takes priority
    over deprecated props such as afterSignInUrl and redirectUrl. It's recommended to use the
    environment variable instead.
    """

    sign_up_fallback_redirect_url: str = None
    """
    The fallback URL to redirect to after the user signs up, if there's no redirect_url in the 
    path already. Defaults to /. Takes priority over deprecated props such as after_sign_in_url
    and redirect_url. It's recommended to use the environment variable instead.
    """

    mode: typing.Literal['redirect', 'modal'] = None
    """
    Determines what happens when a user clicks on the <SignInButton>. Setting this to 'redirect'
    will redirect the user to the sign-in route. Setting this to 'modal' will open a modal on 
    the current route.
    
    Defaults to 'redirect'.
    """


# sign_in_button = SignInButton.create
def sign_in_button(
        *children: rx.Component,
        force_redirect_url: typing.Optional[str] = None,
        fallback_redirect_url: typing.Optional[str] = None,
        sign_up_force_redirect_url: typing.Optional[str] = None,
        sign_up_fallback_redirect_url: typing.Optional[str] = None,
        mode: typing.Literal['redirect', 'modal'] = 'redirect'
) -> SignInButton:
    """
    The <SignInButton> component is a button that links to the sign-in page or displays the sign-in modal.

    This button is un-styled, and is intended to wrap around an rx.button component.

    Examples:
        ```python
        import reflex_clerk as clerk

        def page():
            clerk.clerk_provider(
                rx.box(
                    clerk.sign_in_button(
                        rx.button("Sign In")
                    )
                ),
                publishable_key="pk_my_publishable_key"
            )
        ```

    Args:
        *children: Zero or more child components that will be rendered inside the sign-in button.
        force_redirect_url: The URL to redirect to after the user successfully signs in. Defaults to None.
        fallback_redirect_url: The URL to redirect to if an error occurs during the sign-in process. Defaults to None.
        sign_up_force_redirect_url: The URL to redirect to after the user successfully signs up. Defaults to None.
        sign_up_fallback_redirect_url: The URL to redirect to if an error occurs during the sign-up process. Defaults to None.
        mode: The mode of the sign-in button. It can be either 'redirect' or 'modal'. Defaults to None.

    Returns:
        A SignInButton component instance that can be rendered.
    """
    return SignInButton.create(
        *children,
        force_redirect_url=force_redirect_url,
        fallback_redirect_url=fallback_redirect_url,
        sign_up_force_redirect_url=sign_up_force_redirect_url,
        sign_up_fallback_redirect_url=sign_up_fallback_redirect_url,
        mode=mode
    )


# sign_in = SignIn.create
def sign_in(
        *children: rx.Component,
        appearance: Appearance = None,
        routing: typing.Literal['hash', 'path', 'virtual'] = None,
        path: str = None,
        sign_up_url: str = None,
        force_redirect_url: str = None,
        fallback_redirect_url: str = None,
        sign_up_force_redirect_url: str = None,
        sign_up_fallback_redirect_url: str = None,
        initial_values: typing.Optional[SignInInitialValues] = None
) -> SignIn:
    """
    The <SignIn> component renders a sign-in form.

    Instead of using this component directly, consider using the pre-configured sign-in
    page configured with [`reflex_clerk.install_signin_page`][].

    This form can be styled and configured with various routing and redirection options.

    Examples:
        ```python
        import reflex_clerk as clerk

        def page():
            clerk.clerk_provider(
                rx.box(
                    rx.heading("Welcome, please sign in!"),
                    clerk.sign_in()
                ),
                publishable_key="pk_my_publishable_key"
            )
        ```

    Args:
        appearance: The appearance configuration for the sign-in form.
        routing: The routing strategy for the pages. Can be 'hash', 'path', or 'virtual'. Defaults to None.
        path: The path where the component is mounted when routing is set to 'path'. Ignored for 'hash' and 'virtual' routing.
        sign_up_url: Full URL or path to the sign-up page.
        force_redirect_url: URL to redirect to after sign-in. Takes priority over deprecated props.
        fallback_redirect_url: Fallback URL to redirect to after sign-in if no redirect URL is provided in the path. Defaults to '/'.
        sign_up_force_redirect_url: URL to redirect to after sign-up. Takes priority over deprecated props.
        sign_up_fallback_redirect_url: Fallback URL to redirect to after sign-up if no redirect URL is provided in the path. Defaults to '/'.
        initial_values: Prefilled values for the sign-in fields. Defaults to None.

    Returns:
        A SignIn component instance that can be rendered.
    """
    return SignIn.create(
        *children,
        appearance=appearance,
        routing=routing,
        path=path,
        sign_up_url=sign_up_url,
        force_redirect_url=force_redirect_url,
        fallback_redirect_url=fallback_redirect_url,
        sign_up_force_redirect_url=sign_up_force_redirect_url,
        sign_up_fallback_redirect_url=sign_up_fallback_redirect_url,
        initial_values=initial_values
    )
