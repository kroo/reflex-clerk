"""Reflex custom component SignIn."""

import reflex as rx
from reflex.utils.serializers import serializer


class SignOutOptions:
    session_id: str = None
    """
    The ID of a specific session to sign out of. Useful for multi-session applications.
    """
    redirect_url: str = None
    """
    The redirect URL to navigate to after sign out is complete.
    """


@serializer
def serialize_sign_out_options(obj: SignOutOptions) -> dict:
    return {
        "sessionId": obj.session_id,
        "redirectUrl": obj.redirect_url,
    }


class SignOutButton(rx.Component):
    """SignOutButton component."""

    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "SignOutButton"

    options: SignOutOptions = None
    """Options for the sign out button."""

    redirect_url: str = None
    """
    The redirect URL to navigate to after sign out is complete.
    """


# sign_out_button = SignOutButton.create
def sign_out_button(
        *children: rx.Component,
        options: SignOutOptions = None,
        redirect_url: str = None
) -> SignOutButton:
    """
    The <SignOutButton> component is a button that signs out the user and redirects them to a specified URL.

    This button is un-styled, and is intended to wrap around an rx.button component.

    Examples:
        ```python
        import reflex_clerk as clerk

        def page():
            clerk.clerk_provider(
                rx.box(
                    clerk.sign_out_button(
                        rx.button("Sign Out")
                    )
                ),
                publishable_key="pk_my_publishable_key"
            )
        ```

    Args:
        *children: Zero or more child components that will be rendered inside the sign-out button.
        options: Options for the sign-out button. Defaults to None.
        redirect_url: The URL to redirect to after sign-out. Defaults to None.

    Returns:
        A SignOutButton component instance that can be rendered.
    """
    return SignOutButton.create(
        *children,
        options=options,
        redirect_url=redirect_url
    )
