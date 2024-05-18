import typing

import pydantic


class AppearanceVariables(pydantic.BaseModel):
    """Variables for the appearance."""

    colorPrimary: str = None
    # todo: flush this out


class Appearance(pydantic.BaseModel):
    """Appearance configuration for the ClerkProvider component."""

    baseTheme: typing.Union[typing.Literal["default", "dark", "shadesOfPurple", "neobrutalism"], typing.List[
        typing.Literal["default", "dark", "shadesOfPurple", "neobrutalism"]]] = None

    signIn: "Appearance" = None
    signUp: "Appearance" = None
    variables: AppearanceVariables = None
    elements: typing.Dict[str, typing.Any] = None
