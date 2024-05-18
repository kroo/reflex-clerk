from typing import Optional, List, Dict, Any, Literal

from pydantic import BaseModel


class ClerkError(BaseModel):
    """
    Represents an error response from the Clerk API.
    """
    message: str
    code: Optional[int] = None


class DeletedObjectResponse(BaseModel):
    """
    Represents the response for a successfully deleted object.
    """
    deleted: bool
    object: str


class PaginationMeta(BaseModel):
    """
    Metadata for pagination.
    """
    total_count: int
    limit: int
    offset: int


class Verification(BaseModel):
    """
    Represents the verification details of an email address or phone number.

    Attributes:
        strategy: The strategy pertaining to the parent sign-up or sign-in attempt.
        status: The state of the verification.
        attempts: The number of attempts related to the verification.
        expire_at: The time the verification will expire at.
    """
    strategy: Optional[
        Literal[
            "oauth_google", "oauth_mock", "admin",
            "phone_code", "email_code", "reset_password_email_code",
            "web3_metamask_signature"
        ]]
    status: Optional[Literal['unverified', 'verified', 'transferable', 'failed', 'expired']]
    nonce: Optional[str] = None
    attempts: Optional[int] = None
    expire_at: Optional[int] = None
    error: Optional[ClerkError] = None
    external_verification_redirect_url: Optional[str] = None


class IdentificationLink(BaseModel):
    """
    Represents a link between an email address or phone number and another identification type.

    Attributes:
        type: One of "oauth_google", "oauth_mock", or "saml"
        id: A unique identifier for this link.
    """
    type: Literal["oauth_google", "oauth_mock", "saml"]
    id: str


class EmailAddress(BaseModel):
    """
    Represents an email address associated with a user.

    Attributes:
        id: A unique identifier for this email address.
        email_address: The value of this email address.
        verification: An object holding information on the verification of this email address.
        linked_to: An array of objects containing information about any identifications that might be linked to this email address.
        created_at: Unix timestamp of creation
        updated_at: Unix timestamp of latest update
    """
    id: str
    object: Literal['email_address']
    email_address: str
    reserved: bool
    verification: Optional[Verification] = None
    linked_to: List[IdentificationLink]
    created_at: int
    updated_at: int


class EmailAddressResponse(BaseModel):
    """
    Represents the response containing an email address.
    """
    data: EmailAddress


class PhoneNumber(BaseModel):
    """
    Represents a phone number associated with a user.

    Attributes:
        id: A unique identifier for this phone number.
        phone_number: The value of this phone number, in [E.164 format](https://en.wikipedia.org/wiki/E.164).
        reserved_for_second_factor: Set to true if this phone number is reserved for multi-factor authentication (2FA). Set to false otherwise.
        default_second_factor: Marks this phone number as the default second factor for multi-factor authentication(2FA). A user can have exactly one default second factor.
        verification: An object holding information on the verification of this phone number.
        linked_to: An object containing information about any other identification that might be linked to this phone number.
        created_at: Unix timestamp of creation
        updated_at: Unix timestamp of latest update
    """
    id: str
    object: Literal['phone_number']
    phone_number: str
    reserved_for_second_factor: Optional[bool]
    default_second_factor: Optional[bool]
    reserved: bool
    verification: Optional[Verification] = None
    linked_to: List[IdentificationLink]
    backup_codes: Optional[List[str]] = None
    created_at: int
    updated_at: int


class PhoneNumberResponse(BaseModel):
    """
    Represents the response containing a phone number.
    """
    data: PhoneNumber


class Session(BaseModel):
    """
    Represents a session object.
    """
    id: str
    object: str
    status: str
    user_id: str
    client_id: str
    created_at: int
    updated_at: int
    last_active_at: Optional[int] = None


class SessionListResponse(BaseModel):
    """
    Represents the response containing a list of sessions.
    """
    data: List[Session]
    meta: PaginationMeta


class SessionResponse(BaseModel):
    """
    Represents the response containing a session.
    """
    data: Session


class Client(BaseModel):
    """
    Represents a client object.
    """
    id: str
    object: str
    created_at: int
    updated_at: int
    last_sign_in_at: Optional[int] = None
    sign_in_attempt_id: Optional[str] = None
    session_ids: Optional[List[str]] = None
    sign_up_attempt_id: Optional[str] = None
    status: Optional[str] = None


class ClientListResponse(BaseModel):
    """
    Represents the response containing a list of clients.
    """
    data: List[Client]
    meta: PaginationMeta


class ClientResponse(BaseModel):
    """
    Represents the response containing a client.
    """
    data: Client


class Template(BaseModel):
    """
    Represents a template object for email or SMS.
    """
    id: str
    object: str
    name: str
    subject: Optional[str] = None
    markup: Optional[str] = None
    body: str
    delivered_by_clerk: bool
    from_email_name: Optional[str] = None
    reply_to_email_name: Optional[str] = None


class TemplateListResponse(BaseModel):
    """
    Represents the response containing a list of templates.
    """
    data: List[Template]
    meta: PaginationMeta


class TemplateResponse(BaseModel):
    """
    Represents the response containing a template.
    """
    data: Template


class Web3Wallet(BaseModel):
    """
    Represents a Web3 wallet address associated with a user.

    The address can be used as a proof of identification for users.

    Web3 addresses must be verified to ensure that they can be assigned
    to their rightful owners. The verification is completed via Web3 wallet
    browser extensions, such as [Metamask][1]. The Web3Wallet3 object holds all
    the necessary state around the verification process.

    [1]: https://metamask.io/

    Attributes:
        id: A unique identifier for this web3 wallet.
        web3_wallet: In [Ethereum](https://docs.metamask.io/guide/common-terms.html#address-public-key),
                     the address is made up of 0x + 40 hexadecimal characters.
        created_at: The date and time when the passkey was created.
        updated_at: The date and time when the passkey was updated.
    """
    id: str
    web3_wallet: str
    created_at: int
    updated_at: int
    verification: Optional[Verification] = None


class SAMLAccount(BaseModel):
    """
    Represents a SAML account associated with a user.

    Attributes:
        id: A unique identifier for the SAML account.
        object: The type of object, typically 'saml_account'.
        provider: The SAML provider associated with the account.
        active: A boolean indicating whether the SAML account is active.
        email_address: The email address associated with the SAML account.
        first_name: The first name of the user associated with the SAML account.
        last_name: The last name of the user associated with the SAML account.
        provider_user_id: An optional identifier for the user within the SAML provider.
        public_metadata: Metadata for the SAML account.
        verification: An optional verification object associated with the SAML account.
    """
    id: str
    object: str
    provider: str
    active: bool
    email_address: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    provider_user_id: Optional[str] = None
    public_metadata: Dict[str, Any]
    verification: Optional[Verification] = None


class PasskeyResource(BaseModel):
    """
    Represents a passkey associated with a user response.

    Attributes:
        id: The passkey's unique ID generated by Clerk.
        verification: Verification details for the passkey.
        name: The passkey's name.
        created_at: The date and time when the passkey was created.
        updated_at: The date and time when the passkey was updated.
        last_used_at: The date and time when the passkey was last used.

    """

    id: str
    """The passkey's unique ID generated by Clerk."""

    verification: Verification
    """Verification details for the passkey."""

    name: str
    """The passkey's name."""

    created_at: str
    """The date and time when the passkey was created."""

    updated_at: str
    """The date and time when the passkey was updated."""

    last_used_at: str
    """The date and time when the passkey was last used."""


class User(BaseModel):
    """
    Represents a user object with various attributes related to their profile, authentication, and metadata.

    See the [Clerk documentation][1] for more details.

    [1]: https://clerk.com/docs/users/overview

    Attributes:
        id: A unique identifier for the user.
        object: The type of object, typically 'user'.
        external_id: An optional external identifier for the user.
        primary_email_address_id: The unique identifier for the EmailAddress that the user has set as primary.
        primary_phone_number_id: The unique identifier for the PhoneNumber that the user has set as primary.
        primary_web3_wallet_id: The unique identifier for the Web3Wallet that the user signed up with.
        username: The user's username.
        first_name: The user's first name.
        last_name: The user's last name.
        profile_image_url: Holds the default avatar or user's uploaded profile image. Compatible with Clerk's Image Optimization.
        image_url: The URL of the user's profile image.
        passkeys: An array of passkeys associated with the user's account.
        has_image: A boolean to check if the user has uploaded an image or one was copied from OAuth. Returns false if Clerk is displaying an avatar for the user.
        public_metadata: Metadata that can be read from the Frontend API and Backend API and can be set only from the Backend API.
        private_metadata: Metadata that can be read and set only from the Backend API.
        unsafe_metadata: Metadata that can be read and set from the Frontend API. Often used for custom fields attached to the User object.
        email_addresses: An array of all the EmailAddress objects associated with the user, including the primary.
        phone_numbers: An array of all the PhoneNumber objects associated with the user, including the primary.
        web3_wallets: An array of all the Web3Wallet objects associated with the user, including the primary.
        saml_accounts: An experimental list of SAML accounts associated with the user.
        password_enabled: A boolean indicating whether the user has a password on their account.
        two_factor_enabled: A boolean indicating whether the user has enabled two-factor authentication.
        totp_enabled: A boolean indicating whether the user has enabled TOTP by generating a TOTP secret and verifying it via an authenticator app.
        backup_code_enabled: A boolean indicating whether the user has enabled Backup codes.
        last_sign_in_at: The date when the user last signed in, may be empty if the user has never signed in.
        banned: A boolean indicating whether the user is banned.
        locked: A boolean indicating whether the user is locked.
    """

    id: str
    """A unique identifier for the user."""

    object: str
    """The type of object, typically 'user'."""

    external_id: Optional[str] = None
    """An optional external identifier for the user."""

    primary_email_address_id: Optional[str] = None
    """The unique identifier for the EmailAddress that the user has set as primary."""

    primary_phone_number_id: Optional[str] = None
    """The unique identifier for the PhoneNumber that the user has set as primary."""

    primary_web3_wallet_id: Optional[str] = None
    """The unique identifier for the Web3Wallet that the user signed up with."""

    username: Optional[str] = None
    """The user's username."""

    first_name: Optional[str] = None
    """The user's first name."""

    last_name: Optional[str] = None
    """The user's last name."""

    profile_image_url: Optional[str] = None
    """Holds the default avatar or user's uploaded profile image. Compatible with Clerk's Image Optimization."""

    image_url: Optional[str] = None
    """The URL of the user's profile image."""

    passkeys: Optional[List[PasskeyResource]] = None
    """An array of passkeys associated with the user's account."""

    has_image: bool
    """
    A boolean to check if the user has uploaded an image or one was copied from OAuth.
     Returns false if Clerk is displaying an avatar for the user.
     """

    public_metadata: Dict[str, Any]
    """Metadata that can be read from the Frontend API and Backend API and can be set only from the Backend API."""

    private_metadata: Optional[Dict[str, Any]] = None
    """Metadata that can be read and set only from the Backend API."""

    unsafe_metadata: Dict[str, Any]
    """
    Metadata that can be read and set from the Frontend API. Often used
    for custom fields attached to the User object.
    """

    email_addresses: List[EmailAddress]
    """An array of all the EmailAddress objects associated with the user, including the primary."""

    phone_numbers: List[PhoneNumber]
    """An array of all the PhoneNumber objects associated with the user, including the primary."""

    web3_wallets: List[Web3Wallet]
    """An array of all the Web3Wallet objects associated with the user, including the primary."""

    saml_accounts: List[SAMLAccount]
    """An experimental list of SAML accounts associated with the user."""

    password_enabled: bool
    """A boolean indicating whether the user has a password on their account."""

    two_factor_enabled: bool
    """A boolean indicating whether the user has enabled two-factor authentication."""

    totp_enabled: bool
    """
    A boolean indicating whether the user has enabled TOTP by generating a TOTP secret
    and verifying it via an authenticator app.
    """

    backup_code_enabled: bool
    """A boolean indicating whether the user has enabled Backup codes."""

    last_sign_in_at: Optional[int] = None
    """The date when the user last signed in, may be empty if the user has never signed in."""

    banned: bool
    """A boolean indicating whether the user is banned."""

    locked: bool
    """A boolean indicating whether the user is locked."""


class UserListResponse(BaseModel):
    """
    Represents the response containing a list of users.
    """
    data: List[User]
    meta: PaginationMeta


class UserCountResponse(BaseModel):
    """
    Represents the response containing the count of users.
    """
    count: int


class InterstitialResponse(BaseModel):
    """
    Represents the response containing the interstitial HTML.
    """
    html: str


class Key(BaseModel):
    """
    Represents a key in the JSON Web Key Set (JWKS).
    """
    kty: str
    use: str
    kid: str
    n: str
    e: str


class JWKSResponse(BaseModel):
    """
    Represents the response containing the JSON Web Key Set (JWKS).
    """
    keys: List[Key]
