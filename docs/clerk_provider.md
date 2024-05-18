# Clerk Provider Component

In order to provide clerk context to the other
components in the reflex_clerk library, and to
power the state logic in ClerkState, pages that
contain any clerk components need to be wrapped
in a ClerkProvider component.

```python
import reflex_clerk as clerk

clerk.clerk_provider(
    
    ...,  # this is where you put the rest of your page
    
    publishable_key="pk_my_publishable_key",
    secret_key="sk_my_secret_key"
)
```

The `publishable_key` and `secret_key` parameters are used to authenticate
with Clerk, and can be set by either passing both to the clerk_provider component
or by setting the `CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY` environment variables.

Note that while it appears to be added to the underlying component, the `secret_key`
should never be shared publicly, and is stripped before being rendered -- it is used
only to populate the secret key used by [ClerkState][reflex_clerk.ClerkState] to verify
session tokens.

Both of these keys can be found in your Clerk Dashboard on the [Clerk API Keys][1] page.

[1]: https://dashboard.clerk.com/last-active?path=api-keys


::: reflex_clerk.clerk_provider
    handler: python
    options:
        members:
         - clerk_provider
        separate_signature: true
        show_root_heading: true
        annotations_path: brief
        show_signature_annotations: true
        signature_crossrefs: true
        modernize_annotations: true
        line_length: 80
        docstring_section_style: list
