"""Reflex custom component SignIn."""
import typing

import reflex as rx

from .appearance import Appearance


class UserButton(rx.Component):
    """UserButton component."""

    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "UserButton"

    appearance: Appearance = None
    """
    Optional object to style your components. Will only affect Clerk Components 
    and not Account Portal pages.
    """

    show_name: bool = None
    """
    Controls if the user name is displayed next to the user image button.
    """

    sign_in_url: str = None
    """
    The full URL or path to navigate to when the Add another account button is clicked.
    It's recommended to use the environment variable instead.
    """

    user_profile_mode: typing.Literal['modal', 'navigation'] = None
    """
    Controls whether clicking the Manage your account button will cause the 
    <UserProfile /> component to open as a modal, or if the browser will navigate 
    to the userProfileUrl where <UserProfile /> is mounted as a page. Defaults to: 'modal'.
    """

    user_profile_url: str = None
    """
    The full URL or path leading to the user management interface.
    """

    after_sign_out_url: str = None
    """
    The full URL or path to navigate to after signing out from all accounts 
    (applies to both single-session and multi-session apps). Default is /.
    """

    after_multi_session_single_sign_out_url: str = None
    """
    The full URL or path to navigate to after signing out from currently active account 
    (multi-session apps).
    """

    after_switch_session_url: str = None
    """
    The full URL or path to navigate to after a successful account change (multi-session apps).
    """

    default_open: bool = None
    """
    Controls whether the <UserButton /> should open by default during the first render.
    """

    user_profile_props: dict = None
    """
    Specify options for the underlying <UserProfile /> component. 
    For example: {additionalOAuthScopes: {google: ['foo', 'bar'], github: ['qux']}}.
    """


class UserProfile(rx.Component):
    """UserProfile component."""

    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "UserProfile"

    appearance: Appearance = None
    """
    Optional object to style your components. Will only affect Clerk Components 
    and not Account Portal pages.
    """

    additional_oauth_scopes: dict = None
    """
    Specify additional scopes per OAuth provider that your users would like to
    provide if not already approved.
    
    For example: {"google": ['foo', 'bar'], "github": ['qux']}.
    """


# user_button = UserButton.create
def user_button(
        *children: rx.Component,
        appearance: Appearance = None,
        show_name: bool = None,
        sign_in_url: str = None,
        user_profile_mode: typing.Literal['modal', 'navigation'] = 'modal',
        user_profile_url: str = None,
        after_sign_out_url: str = None,
        after_multi_session_single_sign_out_url: str = None,
        after_switch_session_url: str = None,
        default_open: bool = None,
        user_profile_props: dict = None
) -> UserButton:
    """
    The <UserButton> component displays a user image button that can be configured with various options.

    Examples:
        ```python
        import reflex_clerk as clerk

        def page():
            clerk.clerk_provider(
                rx.box(
                    clerk.user_button()
                ),
                publishable_key="pk_my_publishable_key"
            )
        ```

    Args:
        appearance: Optional object to style the component. Will only affect Clerk Components and not Account Portal pages.
        show_name: Controls if the user name is displayed next to the user image button. Defaults to False.
        sign_in_url: Full URL or path to navigate to when the Add another account button is clicked.
        user_profile_mode: Controls whether clicking the Manage your account button will open the <UserProfile /> component as a modal or navigate to the userProfileUrl. Defaults to 'modal'.
        user_profile_url: Full URL or path leading to the user management interface.
        after_sign_out_url: Full URL or path to navigate to after signing out from all accounts. Defaults to '/'.
        after_multi_session_single_sign_out_url: Full URL or path to navigate to after signing out from the currently active account in multi-session apps.
        after_switch_session_url: Full URL or path to navigate to after a successful account change in multi-session apps.
        default_open: Controls whether the <UserButton /> should open by default during the first render. Defaults to None.
        user_profile_props: Options for the underlying <UserProfile /> component.

    Returns:
        A UserButton component instance that can be rendered.
    """
    return UserButton.create(
        *children,
        appearance=appearance,
        show_name=show_name,
        sign_in_url=sign_in_url,
        user_profile_mode=user_profile_mode,
        user_profile_url=user_profile_url,
        after_sign_out_url=after_sign_out_url,
        after_multi_session_single_sign_out_url=after_multi_session_single_sign_out_url,
        after_switch_session_url=after_switch_session_url,
        default_open=default_open,
        user_profile_props=user_profile_props
    )


# user_profile = UserProfile.create
def user_profile(
        *children: rx.Component,
        appearance: Appearance = None,
        additional_oauth_scopes: dict = None
) -> UserProfile:
    """
    The <UserProfile> component displays the user profile interface with various configuration options.

    Examples:
        ```python
        import reflex_clerk as clerk

        def page():
            clerk.clerk_provider(
                rx.box(
                    clerk.user_profile()
                ),
                publishable_key="pk_my_publishable_key"
            )
        ```

    Args:
        *children: Zero or more child components that will be rendered inside the user profile component.
        appearance: Optional object to style the component. Will only affect Clerk Components and not Account Portal pages.
        additional_oauth_scopes: Specify additional scopes per OAuth provider that your users would like to provide if not already approved. Defaults to None.

    Returns:
        A UserProfile component instance that can be rendered.
    """
    return UserProfile.create(
        *children,
        appearance=appearance,
        additional_oauth_scopes=additional_oauth_scopes
    )
