# clerk

A Reflex custom component clerk.

## Installation

```bash
pip install reflex-clerk
```

## Usage

```python
import reflex as rx
from reflex_clerk import clerk_provider, sign_in_button, install_signin_page

publishable_key = "your_clerk_publishable_key"


def index() -> rx.Component:
    return clerk_provider(
        rx.vstack(
            sign_in_button(),
            align="center",
            spacing="7",
        ),
        publishable_key=publishable_key,
    )


app = rx.App()
app.add_page(index)
install_signin_page(app)
```

In this example:

1. We import the necessary components from Reflex and the `reflex_clerk` library.
2. We define the `publishable_key` for our Clerk instance.
3. We create a function index that returns a Reflex component.
4. Inside the index function, we use the `clerk_provider` component from reflex_clerk. This component sets up the Clerk
   context for the rest of the components within it.
5. Within the `clerk_provider`, we create a vertical stack (rx.vstack) that contains the sign_in.sign_in_button()
   component from reflex_clerk. This component renders a sign-in button for Clerk.
6. We pass the `publishable_key` to the `clerk_provider` component.

With this setup, you'll have a page that displays a sign-in button powered by Clerk. You can then add more Clerk
components, such as user profile information, sign-out buttons, and more, within the clerk_provider.

Further documentation can be found in [the reference docs](docs/)

## License

Apache-2.0

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- [Reflex](https://github.com/reflexjs/reflex)
- [Clerk](https://clerk.dev/)
