import requests

from .clerk_request_models import *
from .clerk_response_models import *


class ClerkAPIClient(object):
    def __init__(self, base_url: str, secret_key: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.secret_key = secret_key
        self.headers = headers if headers else {}
        self.headers["Authorization"] = f"Bearer {self.secret_key}"

    def _get_url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def _handle_response(self, response: requests.Response, response_model: Any):
        if response.status_code >= 400:
            response.raise_for_status()
        try:
            data = response.json()
            return response_model.parse_obj(data)
        except ValueError:
            raise ValueError(f"Failed to parse response '{response.text}' as {response_model.__name__}")

    def get_public_interstitial(self, params: Optional[GetPublicInterstitialParams] = None) -> InterstitialResponse:
        url = self._get_url("/public/interstitial")
        response = requests.get(url, headers=self.headers, params=params.dict() if params else None)
        return self._handle_response(response, InterstitialResponse)

    def get_jwks(self) -> JWKSResponse:
        url = self._get_url("/jwks")
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response, JWKSResponse)

    def get_client_list(self, params: Optional[GetClientListParams] = None) -> ClientListResponse:
        url = self._get_url("/clients")
        response = requests.get(url, headers=self.headers, params=params.dict() if params else None)
        return self._handle_response(response, ClientListResponse)

    def verify_client(self, data: VerifyClientRequest) -> ClientResponse:
        url = self._get_url("/clients/verify")
        response = requests.post(url, headers=self.headers, json=data.dict())
        return self._handle_response(response, ClientResponse)

    def get_client(self, client_id: str) -> ClientResponse:
        url = self._get_url(f"/clients/{client_id}")
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response, ClientResponse)

    def create_email_address(self, data: CreateEmailAddressRequest) -> EmailAddressResponse:
        url = self._get_url("/email_addresses")
        response = requests.post(url, headers=self.headers, json=data.dict())
        return self._handle_response(response, EmailAddressResponse)

    def get_email_address(self, email_address_id: str) -> EmailAddressResponse:
        url = self._get_url(f"/email_addresses/{email_address_id}")
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response, EmailAddressResponse)

    def delete_email_address(self, email_address_id: str) -> DeletedObjectResponse:
        url = self._get_url(f"/email_addresses/{email_address_id}")
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response, DeletedObjectResponse)

    def update_email_address(self, email_address_id: str, data: UpdateEmailAddressRequest) -> EmailAddressResponse:
        url = self._get_url(f"/email_addresses/{email_address_id}")
        response = requests.patch(url, headers=self.headers, json=data.dict())
        return self._handle_response(response, EmailAddressResponse)

    def create_phone_number(self, data: CreatePhoneNumberRequest) -> PhoneNumberResponse:
        url = self._get_url("/phone_numbers")
        response = requests.post(url, headers=self.headers, json=data.dict())
        return self._handle_response(response, PhoneNumberResponse)

    def get_phone_number(self, phone_number_id: str) -> PhoneNumberResponse:
        url = self._get_url(f"/phone_numbers/{phone_number_id}")
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response, PhoneNumberResponse)

    def delete_phone_number(self, phone_number_id: str) -> DeletedObjectResponse:
        url = self._get_url(f"/phone_numbers/{phone_number_id}")
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response, DeletedObjectResponse)

    def update_phone_number(self, phone_number_id: str, data: UpdatePhoneNumberRequest) -> PhoneNumberResponse:
        url = self._get_url(f"/phone_numbers/{phone_number_id}")
        response = requests.patch(url, headers=self.headers, json=data.dict())
        return self._handle_response(response, PhoneNumberResponse)

    def get_session_list(self, params: Optional[GetSessionListParams] = None) -> SessionListResponse:
        url = self._get_url("/sessions")
        response = requests.get(url, headers=self.headers, params=params.dict() if params else None)
        return self._handle_response(response, SessionListResponse)

    def get_session(self, session_id: str) -> SessionResponse:
        url = self._get_url(f"/sessions/{session_id}")
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response, SessionResponse)

    def revoke_session(self, session_id: str) -> SessionResponse:
        url = self._get_url(f"/sessions/{session_id}/revoke")
        response = requests.post(url, headers=self.headers)
        return self._handle_response(response, SessionResponse)

    def verify_session(self, session_id: str, data: VerifySessionRequest) -> SessionResponse:
        url = self._get_url(f"/sessions/{session_id}/verify")
        response = requests.post(url, headers=self.headers, json=data.dict())
        return self._handle_response(response, SessionResponse)

    def create_session_token_from_template(self, session_id: str, template_name: str) -> Dict[str, str]:
        url = self._get_url(f"/sessions/{session_id}/tokens/{template_name}")
        response = requests.post(url, headers=self.headers)
        return self._handle_response(response, Dict[str, str])

    def get_template_list(self, template_type: str) -> TemplateListResponse:
        url = self._get_url(f"/templates/{template_type}")
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response, TemplateListResponse)

    def get_template(self, template_type: str, slug: str) -> TemplateResponse:
        url = self._get_url(f"/templates/{template_type}/{slug}")
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response, TemplateResponse)

    def upsert_template(self, template_type: str, slug: str, data: UpsertTemplateRequest) -> TemplateResponse:
        url = self._get_url(f"/templates/{template_type}/{slug}")
        response = requests.put(url, headers=self.headers, json=data.dict())
        return self._handle_response(response, TemplateResponse)

    def revert_template(self, template_type: str, slug: str) -> TemplateResponse:
        url = self._get_url(f"/templates/{template_type}/{slug}/revert")
        response = requests.post(url, headers=self.headers)
        return self._handle_response(response, TemplateResponse)

    def preview_template(self, template_type: str, slug: str, data: PreviewTemplateRequest) -> Dict[str, Any]:
        url = self._get_url(f"/templates/{template_type}/{slug}/preview")
        response = requests.post(url, headers=self.headers, json=data.dict())
        return self._handle_response(response, Dict[str, Any])

    def toggle_template_delivery(self, template_type: str, slug: str,
                                 data: ToggleTemplateDeliveryRequest) -> TemplateResponse:
        url = self._get_url(f"/templates/{template_type}/{slug}/toggle_delivery")
        response = requests.post(url, headers=self.headers, json=data.dict())
        return self._handle_response(response, TemplateResponse)

    def get_user_list(self, params: Optional[GetUserListParams] = None) -> UserListResponse:
        url = self._get_url("/users")
        response = requests.get(url, headers=self.headers, params=params.dict() if params else None)
        return self._handle_response(response, UserListResponse)

    def create_user(self, data: CreateUserRequest) -> User:
        url = self._get_url("/users")
        response = requests.post(url, headers=self.headers, json=data.dict())
        return self._handle_response(response, User)

    def get_users_count(self, params: Optional[GetUsersCountParams] = None) -> UserCountResponse:
        url = self._get_url("/users/count")
        response = requests.get(url, headers=self.headers, params=params.dict() if params else None)
        return self._handle_response(response, UserCountResponse)

    def get_user(self, user_id: str) -> User:
        url = self._get_url(f"/users/{user_id}")
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response, User)

    def update_user(self, user_id: str, data: UpdateUserRequest) -> User:
        url = self._get_url(f"/users/{user_id}")
        response = requests.patch(url, headers=self.headers, json=data.dict())
        return self._handle_response(response, User)


BASE_URL = "https://api.clerk.com/v1"


def get_client(secret_key) -> ClerkAPIClient:
    """
    Returns an instance of the ClerkAPIClient using the provided secret key.

    :param secret_key: The secret key used to authenticate the client.
    :type secret_key: str
    :return: An instance of the ClerkAPIClient.
    :rtype: ClerkAPIClient
    """
    return ClerkAPIClient(BASE_URL, secret_key)
