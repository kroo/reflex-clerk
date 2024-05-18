"""Reflex custom component SignIn."""
import typing

import reflex as rx
from reflex.utils.serializers import serializer

from .appearance import Appearance


class SignUpInitialValues:
    email_address: str = None
    username: str = None
    phone_number: str = None
    first_name: str = None
    last_name: str = None


@serializer
def serialize_sign_up_initial_values(obj: SignUpInitialValues) -> dict:
    return {
        "emailAddress": obj.email_address,
        "username": obj.username,
        "phoneNumber": obj.phone_number,
        "firstName": obj.first_name,
        "lastName": obj.last_name,
    }


class SignUp(rx.Component):
    """ClerkProvider component."""

    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "SignIn"

    appearance: Appearance = None
    """Optional object to style your components. Will only affect Clerk Components and not Account Portal pages."""

    routing: typing.Literal['hash', 'path', 'virtual'] = None
    """The routing strategy for your pages.
    
    Defaults to 'path' in Next.js and Remix applications. Defaults to hash for all other SDK's.
    """

    path: str = None
    """
    The path where the component is mounted on when routing is set to path.
    It is ignored in hash- and virtual-based routing.

    For example: /sign-up.
    """

    sign_in_url: str = None
    """
    Full URL or path to the sign in page. Use this property to provide the target of the 
    'Sign In' link that's rendered. It's recommended to use the environment variable instead.
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

    sign_in_force_redirect_url: str = None
    """
    If provided, this URL will always be redirected to after the user signs up. Takes priority
    over deprecated props such as after_sign_up_url and redirect_url. It's recommended to use the
    environment variable instead.
    """

    sign_in_fallback_redirect_url: str = None
    """
    The fallback URL to redirect to after the user signs up, if there's no redirect_url in the 
    path already. Defaults to /. Takes priority over deprecated props such as after_sign_up_url
    and redirect_url. It's recommended to use the environment variable instead.
    """

    initial_values: typing.Optional[SignUpInitialValues] = None
    """The values used to prefill the sign-in fields with."""


class SignUpButton(rx.Component):
    """SignUpButton component."""

    library = "@clerk/clerk-react"
    """The React library to wrap."""

    tag = "SignUpButton"
    """The React component tag."""

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

    sign_in_force_redirect_url: str = None
    """
    If provided, this URL will always be redirected to after the user signs up. Takes priority
    over deprecated props such as after_sign_up_url and redirect_url. It's recommended to use the
    environment variable instead.
    """

    sign_in_fallback_redirect_url: str = None
    """
    The fallback URL to redirect to after the user signs up, if there's no redirect_url in the 
    path already. Defaults to /. Takes priority over deprecated props such as after_sign_up_url
    and redirect_url. It's recommended to use the environment variable instead.
    """

    mode: typing.Literal['redirect', 'modal'] = None
    """
    Determines what happens when a user clicks on the <SignInButton>. Setting this to 'redirect'
    will redirect the user to the sign-in route. Setting this to 'modal' will open a modal on 
    the current route.

    Defaults to 'redirect'.
    """


# sign_up_button = SignUpButton.create
def sign_up_button(
        *children: rx.Component,
        force_redirect_url: str = None,
        fallback_redirect_url: str = None,
        sign_in_force_redirect_url: str = None,
        sign_in_fallback_redirect_url: str = None,
        mode: typing.Literal['redirect', 'modal'] = 'redirect'
) -> SignUpButton:
    """
    The <SignUpButton> component is a button that links to the sign-up page
    or displays the sign-up modal.

    This button is un-styled, and is intended to wrap around an rx.button component.

    Examples:
        ```python
        import reflex_clerk as clerk

        def page():
            clerk.clerk_provider(
                rx.box(
                    clerk.sign_up_button(
                        rx.button("Sign Up")
                    )
                ),
                publishable_key="pk_my_publishable_key"
            )
        ```

    Args:
        force_redirect_url: The URL to redirect to after the user successfully signs in. Defaults to None.
        fallback_redirect_url: The URL to redirect to if an error occurs during the sign-in process. Defaults to None.
        sign_in_force_redirect_url: The URL to redirect to after the user successfully signs up. Defaults to None.
        sign_in_fallback_redirect_url: The URL to redirect to if an error occurs during the sign-up process. Defaults to None.
        mode: The mode of the sign-up button. It can be either 'redirect' or 'modal'. Defaults to 'redirect'.

    Returns:
        A SignUpButton component instance that can be rendered.
    """
    return SignUpButton.create(
        *children,
        force_redirect_url=force_redirect_url,
        fallback_redirect_url=fallback_redirect_url,
        sign_in_force_redirect_url=sign_in_force_redirect_url,
        sign_in_fallback_redirect_url=sign_in_fallback_redirect_url,
        mode=mode
    )


# sign_up = SignUp.create
def sign_up(
        *children: rx.Component,
        appearance: Appearance = None,
        routing: typing.Literal['hash', 'path', 'virtual'] = None,
        path: str = None,
        sign_in_url: str = None,
        force_redirect_url: str = None,
        fallback_redirect_url: str = None,
        sign_in_force_redirect_url: str = None,
        sign_in_fallback_redirect_url: str = None,
        initial_values: typing.Optional[SignUpInitialValues] = None
) -> SignUp:
    """
    The <SignUp> component renders a sign-up form.

    Instead of using this component directly, consider using the pre-configured sign-in
    page configured with [`reflex_clerk.install_signup_page`][].

    This form can be styled and configured with various routing and redirection options.

    Examples:
        ```python
        import reflex_clerk as clerk

        def page():
            clerk.clerk_provider(
                rx.box(
                    rx.heading("Welcome, please sign up!"),
                    clerk.sign_up()
                ),
                publishable_key="pk_my_publishable_key"
            )
        ```

    Args:
        appearance: The appearance configuration for the sign-up form.
        routing: The routing strategy for the pages. Can be 'hash', 'path', or 'virtual'. Defaults to None.
        path: The path where the component is mounted when routing is set to 'path'. Ignored for 'hash' and 'virtual' routing.
        sign_in_url: Full URL or path to the sign-in page.
        force_redirect_url: URL to redirect to after sign-in. Takes priority over deprecated props.
        fallback_redirect_url: Fallback URL to redirect to after sign-in if no redirect URL is provided in the path. Defaults to '/'.
        sign_in_force_redirect_url: URL to redirect to after sign-up. Takes priority over deprecated props.
        sign_in_fallback_redirect_url: Fallback URL to redirect to after sign-up if no redirect URL is provided in the path. Defaults to '/'.
        initial_values: Prefilled values for the sign-up fields. Defaults to None.

    Returns:
        A SignUp component instance that can be rendered.
    """
    return SignUp.create(
        *children,
        appearance=appearance,
        routing=routing,
        path=path,
        sign_in_url=sign_in_url,
        force_redirect_url=force_redirect_url,
        fallback_redirect_url=fallback_redirect_url,
        sign_in_force_redirect_url=sign_in_force_redirect_url,
        sign_in_fallback_redirect_url=sign_in_fallback_redirect_url,
        initial_values=initial_values
    )
