# Reflex Clerk Component Library Documentation

A Reflex custom component library for [Clerk](https://clerk.com/), a
User Management Platform.

<div class="grid" markdown>

<figure markdown="span">
[![SignIn](https://clerk.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2F_docs%2Fmain%2Fui-components%2Fsign-in.svg&w=1080&q=75){ align=left }][reflex_clerk.sign_in]
</figure>

<figure markdown="span">
[![UserButton](https://clerk.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2F_docs%2Fmain%2Fui-components%2Fuser-button.svg&w=1080&q=75){ align=right }][reflex_clerk.user_button]
</figure>

</div>

## Getting Started

Install with pip install:

```bash
pip install reflex-clerk
```

Import the custom component:

```python
import reflex_clerk as clerk
```

Install signup and login pages:

```python
import reflex as rx
import reflex_clerk as clerk

app = rx.App()
clerk.install_pages(
    app,
    publishable_key="pk_my_publishable_key",
    signin_route="/signin",
    signup_route="/signup"
)
```

Wrap any pages that use clerk auth components in a
[`clerk_provider`][reflex_clerk.clerk_provider].

```python
import reflex_clerk as clerk
import reflex as rx


@rx.page("/")
def homepage():
    clerk.clerk_provider(
        ...,  # the rest of my homepage

        publishable_key="pk_my_publishable_key",
        secret_key="sk_my_secret_key"
    )
```

... and now use one of over a dozen components provided by
the Clerk SDK, and access the current user with
[ClerkState][reflex_clerk.ClerkState].

``` { .python .annotate }
import reflex_clerk as clerk
import reflex as rx

...
clerk.clerk_provider(
    ...,

    clerk.signed_in(  # (1) 
        rx.cond(
            clerk.ClerkState.user.has_image,  # (2)
            rx.chakra.avatar(
                src=clerk.ClerkState.user.image_url,  # (3)
                name=clerk.ClerkState.user.first_name,
                size="xl",
            ),
        )
    ),

    ...
)
```

1. The [clerk.signed_in()][reflex_clerk.signed_in] control component hides child components unless the user is actively
   logged in. See also [clerk.signed_out()][reflex_clerk.signed_out] and [clerk.protect][reflex_clerk.protect].
2. [ClerkState][reflex_clerk.ClerkState] provides a reflex [State][reflex.State] that holds the current authentication
   state, as well as the reflex user itself.
3. [ClerkState.user][reflex_clerk.User] contains the Clerk user object for the currently logged in user -- including
   email and phone number info, name information, and an
   avatar image.

## Components

 - [`<ClerkProvider />`][reflex_clerk.clerk_provider]: Provides session management context to child components
 - [`<SignInButton />`][reflex_clerk.sign_in_button]: Wrap a button or link with this component to make it a sign-in link!
 - [`<SignOutButton />`][reflex_clerk.sign_out_button]: Logs the current user out.
 - [`<SignUpButton />`][reflex_clerk.sign_up_button]: Wrap a button or link to take the user to the signup page. 
 - [`<UserButton />`][reflex_clerk.user_button]: A navbar element for the current logged in user, with user switching capabilities.
 - [`<SignUp />`][reflex_clerk.sign_up]: A full user registration card
 - [`<SignIn />`][reflex_clerk.sign_in]: A login card
 - [`<UserProfile />`][reflex_clerk.user_profile]: A full page component for user profile management
 - [`<SignedIn />`][reflex_clerk.signed_in]: Hides child components unless the user is signed in
 - [`<SignedOut />`][reflex_clerk.signed_out]: Hides child components unless the user is signed out
 - [`<RedirectToUserProfile />`][reflex_clerk.redirect_to_user_profile]: Redirects to the user profile page, if rendered 
 - [`<RedirectToSignIn />`][reflex_clerk.redirect_to_sign_in]: Redirects to the user sign in page, if rendered 
 - [`<RedirectToSignUp />`][reflex_clerk.redirect_to_sign_up]: Redirects to the user registration page, if rendered
 - [`<RedirectToOrganizationProfile />`][reflex_clerk.redirect_to_organization_profile]: Redirects to the organization profile page, if rendered
 - [`<RedirectToCreateOrganization />`][reflex_clerk.redirect_to_create_organization]: Redirects to the organization creation page, if rendered
 - [`<MultisessionAppSupport />`][reflex_clerk.multisession_app_support]: Ensures child components are rerendered after a session switches users in a multi-user session context
 - [`<ClerkLoading />`][reflex_clerk.clerk_loading]: Renders child components only if Clerk has not yet initialized
 - [`<ClerkLoaded />`][reflex_clerk.clerk_loading]: Renders child components only if Clerk has fully initialized
 - [`<Protect />`][reflex_clerk.protect]: Renders child components only if the user has the specified role or permissions

## Reflex State Management

 - [`ClerkState.is_logged_in`][reflex_clerk.ClerkState]: true if we can verify the current reflex session contains an authenticated Clerk user
 - [`ClerkState.user`][reflex_clerk.User]: a copy of the Clerk user object retrieved at the time of authentication

## Reflex Auth Pages

 - [`clerk.install_pages`][reflex_clerk.install_pages]: Installs /signup and /signin pages preconfigured for Clerk
 - [`clerk.install_signin_page`][reflex_clerk.install_signin_page]: Installs /signin page preconfigured for Clerk
 - [`clerk.install_signup_page`][reflex_clerk.install_signup_page]: Installs /signup page preconfigured for Clerk