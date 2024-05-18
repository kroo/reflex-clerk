# Page Setup

::: reflex_clerk.install_pages
    handler: python
    options:
        members:
         - clerk_provider
        show_root_heading: true
        separate_signature: true

::: reflex_clerk.install_signin_page
    handler: python
    options:
        members:
         - clerk_provider
        show_root_heading: true
        separate_signature: true

::: reflex_clerk.install_signup_page
    handler: python
    options:
        members:
         - clerk_provider
        show_root_heading: true
        separate_signature: true
