"""Reflex custom control_components.md components for Clerk."""
import typing
from typing import Union

import reflex as rx
from reflex import ImportVar
from reflex.utils.serializers import serializer


class Javascript(str):
    pass


@serializer
def serialize_javascript(obj: Javascript) -> str:
    return f"{{{obj}}}"


class ClerkLoaded(rx.Component):
    """ClerkLoaded component."""

    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "ClerkLoaded"


class ClerkLoading(rx.Component):
    """ClerkLoading component."""

    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "ClerkLoading"


class Protect(rx.Component):
    """Protect component."""

    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "Protect"

    condition: Javascript = None
    """
    Optional conditional logic that renders the children if it returns true.
    """

    fallback: typing.Union[rx.Component, str] = None
    """
    An optional snippet of JSX to show when a user doesn't have the role or permission 
    to access the protected content.
    """

    permission: str = None
    """
    Optional string corresponding to a Role's Permission in the format org:<resource>:<action>
    """

    role: str = None
    """
    Optional string corresponding to an Organization's Role in the format org:<role>
    """

    # Make sure imports for the fallback component are included in the dependencies.
    def add_imports(self) -> dict[str, Union[str, ImportVar, list[Union[str, ImportVar]]]]:
        if isinstance(self.fallback, rx.Component):
            return self.fallback._get_all_imports()
        return {}


class MultisessionAppSupport(rx.Component):
    """
    The <MultisessionAppSupport> provides a wrapper for your React application
    that guarantees a full rerendering cycle everytime the current session and
    user changes.
    """

    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "MultisessionAppSupport"


class RedirectToSignIn(rx.Component):
    """
    The <RedirectToSignIn /> component will navigate to the sign in URL which has
    been configured in your application instance. The behavior will be just like a
    server-side (3xx) redirect, and will override the current location in the history
    stack.
    """
    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "RedirectToSignIn"


class RedirectToSignUp(rx.Component):
    """
    The <RedirectToSignUp /> component will navigate to the sign in URL which has
    been configured in your application instance. The behavior will be just like a
    server-side (3xx) redirect, and will override the current location in the history
    stack.
    """
    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "RedirectToSignUp"


class RedirectToUserProfile(rx.Component):
    """
    The <RedirectToUserProfile /> component will navigate to the sign in URL which has
    been configured in your application instance. The behavior will be just like a
    server-side (3xx) redirect, and will override the current location in the history
    stack.
    """
    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "RedirectToUserProfile"


class RedirectToOrganizationProfile(rx.Component):
    """
    The <RedirectToOrganizationProfile /> component will navigate to the sign in URL which has
    been configured in your application instance. The behavior will be just like a
    server-side (3xx) redirect, and will override the current location in the history
    stack.
    """
    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "RedirectToOrganizationProfile"


class RedirectToCreateOrganization(rx.Component):
    """
    The <RedirectToCreateOrganization /> component will navigate to the sign in URL which has
    been configured in your application instance. The behavior will be just like a
    server-side (3xx) redirect, and will override the current location in the history
    stack.
    """
    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "RedirectToCreateOrganization"


class SignedIn(rx.Component):
    """
    The <SignedIn> component offers authentication checks as a cross-cutting concern. Any
    children components wrapped by a <SignedIn> component will be rendered only if there's
    a User with an active Session signed in your application.
    """
    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "SignedIn"


class SignedOut(rx.Component):
    """
    The <SignedOut> component offers authentication checks as a cross-cutting concern. Any
    children components wrapped by a <SignedOut> component will be rendered only if there's
    a User with an active Session signed in your application.
    """
    # The React library to wrap.
    library = "@clerk/clerk-react"

    # The React component tag.
    tag = "SignedOut"


def clerk_loaded(*children: rx.Component) -> ClerkLoaded:
    """
    The <ClerkLoaded> component indicates that Clerk is fully loaded.

    Args:
        *children: Zero or more child components that will be rendered inside the ClerkLoaded component.

    Returns:
        A ClerkLoaded component instance that can be rendered.
    """
    return ClerkLoaded.create(*children)


def clerk_loading(*children: rx.Component) -> ClerkLoading:
    """
    The <ClerkLoading> component indicates that Clerk is still loading.

    Args:
        *children: Zero or more child components that will be rendered inside the ClerkLoading component.

    Returns:
        A ClerkLoading component instance that can be rendered.
    """
    return ClerkLoading.create(*children)


def protect(
        *children: rx.Component,
        condition: Javascript = None,
        fallback: typing.Union[rx.Component, str] = None,
        permission: str = None,
        role: str = None
) -> Protect:
    """
    The <Protect> component conditionally renders its children based on the provided logic.

    Args:
        *children: Zero or more child components that will be rendered inside the Protect component.
        condition: Optional conditional logic that renders the children if it returns true.
        fallback: An optional snippet of JSX to show when a user doesn't have the role or permission to access the protected content.
        permission: Optional string corresponding to a Role's Permission in the format org:<resource>:<action>.
        role: Optional string corresponding to an Organization's Role in the format org:<role>.

    Returns:
        A Protect component instance that can be rendered.
    """
    return Protect.create(
        *children,
        condition=condition,
        fallback=fallback,
        permission=permission,
        role=role
    )


def multisession_app_support(*children: rx.Component) -> MultisessionAppSupport:
    """
    The <MultisessionAppSupport> provides a wrapper for your React application that guarantees a full rerendering cycle everytime the current session and user changes.

    Args:
        *children: Zero or more child components that will be rendered inside the MultisessionAppSupport component.

    Returns:
        A MultisessionAppSupport component instance that can be rendered.
    """
    return MultisessionAppSupport.create(*children)


def redirect_to_sign_in() -> RedirectToSignIn:
    """
    The <RedirectToSignIn /> component navigates to the sign-in URL configured in your application instance.

    Returns:
        A RedirectToSignIn component instance that can be rendered.
    """
    return RedirectToSignIn.create()


def redirect_to_sign_up() -> RedirectToSignUp:
    """
    The <RedirectToSignUp /> component navigates to the sign-up URL configured in your application instance.

    Returns:
        A RedirectToSignUp component instance that can be rendered.
    """
    return RedirectToSignUp.create()


def redirect_to_user_profile() -> RedirectToUserProfile:
    """
    The <RedirectToUserProfile /> component navigates to the user profile URL configured in your application instance.

    Returns:
        A RedirectToUserProfile component instance that can be rendered.
    """
    return RedirectToUserProfile.create()


def redirect_to_organization_profile() -> RedirectToOrganizationProfile:
    """
    The <RedirectToOrganizationProfile /> component navigates to the organization profile URL configured in your application instance.

    Returns:
        A RedirectToOrganizationProfile component instance that can be rendered.
    """
    return RedirectToOrganizationProfile.create()


def redirect_to_create_organization(*children: rx.Component) -> RedirectToCreateOrganization:
    """
    The <RedirectToCreateOrganization /> component navigates to the create organization URL configured in your application instance.

    Args:
        *children: Zero or more child components that will be rendered inside the RedirectToCreateOrganization component.

    Returns:
        A RedirectToCreateOrganization component instance that can be rendered.
    """
    return RedirectToCreateOrganization.create(*children)


def signed_in(*children: rx.Component) -> SignedIn:
    """
    The <SignedIn> component renders its children only if there's a User with an active Session signed in your application.

    Args:
        *children: Zero or more child components that will be rendered inside the SignedIn component.

    Returns:
        A SignedIn component instance that can be rendered.
    """
    return SignedIn.create(*children)


def signed_out(*children: rx.Component) -> SignedOut:
    """
    The <SignedOut> component renders its children only if there's no User with an active Session signed in your application.

    Args:
        *children: Zero or more child components that will be rendered inside the SignedOut component.

    Returns:
        A SignedOut component instance that can be rendered.
    """
    return SignedOut.create(*children)
