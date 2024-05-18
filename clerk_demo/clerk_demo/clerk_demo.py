"""Welcome to Reflex! This file showcases the custom component in a basic app."""

import reflex as rx

import reflex_clerk as clerk
import reflex_clerk.clerk_client


class State(rx.State):
    """The app state."""
    pass


def index() -> rx.Component:
    return (
        clerk.clerk_provider(
            rx.flex(

                clerk.user_button(),
                width="100%",
                spacing="7",
                margin_top="0.75rem",
                padding_right="0.75rem",
                direction="column",
                align="end",

            ),
            rx.center(
                rx.vstack(
                    clerk.signed_in(
                        rx.cond(
                            clerk.ClerkState.user.has_image,
                            rx.chakra.avatar(
                                src=clerk.ClerkState.user.image_url,
                                name=clerk.ClerkState.user.first_name,
                                size="xl",
                            ),
                        )
                    ),
                    rx.heading("Welcome to Reflex!", size="9"),
                    clerk.signed_out(
                        rx.button(
                            clerk.sign_in_button(),
                            size="4",
                            color_scheme="gray",
                            background="black"
                        ),
                    ),
                    clerk.signed_in(
                        rx.button(
                            clerk.sign_out_button(),
                            size="4",
                            color_scheme="gray",
                            background="black"
                        )
                    ),
                    clerk.clerk_loaded(
                        rx.cond(
                            clerk.ClerkState.is_signed_in,
                            rx.box(
                                rx.text(
                                    "You are currently logged in as ",
                                    clerk.ClerkState.user.first_name
                                ),
                            ),
                            rx.text("you are currently logged out"))),

                    align="center",
                    spacing="7",
                ),
                height="100vh",

            ),
        )
    )


def signin_page() -> rx.Component:
    return clerk.clerk_provider(
        rx.center(
            rx.vstack(
                clerk.sign_in(
                    path="/signin",
                ),
                align="center",
                spacing="7",
            ),
            height="100vh",
        ),
    )


def auth_required_page():
    return clerk.clerk_provider(
        rx.center(
            rx.container(
                rx.heading("Auth required test"),
                clerk.protect(
                    rx.fragment("You are logged in as ", clerk.ClerkState.user.first_name),
                    fallback=clerk.redirect_to_sign_in()
                ),
            )
        ),
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.add_page(auth_required_page, route="/test-auth")
reflex_clerk.install_signin_page(app)
