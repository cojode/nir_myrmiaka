"""CAS authentication service.

Handles CAS ticket validation and CAS-based user login.
"""

import secrets
from datetime import datetime
from typing import Dict
from xml.etree import ElementTree

import httpx

from nir_myrmiaka.db.database import Database
from nir_myrmiaka.db.models.user_profile import UserProfile
from nir_myrmiaka.db.repositories.user_profile import UserProfileRepository
from nir_myrmiaka.exceptions.abc import DomainError
from nir_myrmiaka.log import logger
from nir_myrmiaka.services.auth.security import hash_password
from nir_myrmiaka.settings import settings

CAS_NAMESPACE = "http://www.yale.edu/tp/cas"


class CasAuthenticationError(DomainError):
    """Exception raised when CAS authentication fails at the protocol level."""

    def __init__(self, message: str, detail: Dict | None = None) -> None:
        super().__init__(message=message, detail=detail)


class CasTicketInvalidError(CasAuthenticationError):
    """Exception raised when the CAS ticket is invalid or expired."""

    def __init__(self, ticket: str, code: str | None = None) -> None:
        detail: Dict = {"ticket": ticket}
        if code:
            detail["code"] = code
        super().__init__(
            message="CAS ticket is invalid or expired",
            detail=detail,
        )


class CasService:
    """Service for CAS-based authentication workflow."""

    def __init__(self, db: Database) -> None:
        self.db = db
        self.repo = UserProfileRepository(session=db)

    def _build_cas_validate_url(self, ticket: str, service_path: str) -> str:
        """Build the full CAS serviceValidate URL."""
        base = settings.cas_server_url.rstrip("/")
        full_service = settings.cas_public_base_url.rstrip("/") + service_path
        return (
            f"{base}/serviceValidate"
            f"?ticket={ticket}"
            f"&service={full_service}"
        )

    async def validate_ticket(self, ticket: str, service_path: str) -> str:
        """Validate a CAS ticket and return the user's username.

        Calls CAS /serviceValidate and parses the XML response.
        """
        url = self._build_cas_validate_url(ticket, service_path)
        logger.info("Validating CAS ticket at: %s", url)

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=httpx.Timeout(10.0))
                response.raise_for_status()
            except httpx.HTTPError as exc:
                raise CasAuthenticationError(
                    message=f"CAS server request failed: {exc}",
                ) from exc

        xml_text = response.text
        logger.debug("CAS response: %s", xml_text)

        try:
            root = ElementTree.fromstring(xml_text)
        except ElementTree.ParseError as exc:
            raise CasAuthenticationError(
                message="Failed to parse CAS XML response",
            ) from exc

        ns = {"cas": CAS_NAMESPACE}

        failure = root.find(".//cas:authenticationFailure", ns)
        if failure is not None:
            code = failure.attrib.get("code", "UNKNOWN")
            raise CasTicketInvalidError(ticket=ticket, code=code)

        success = root.find(".//cas:authenticationSuccess", ns)
        if success is None:
            raise CasAuthenticationError(
                message="Unexpected CAS response: no success or failure element",
            )

        user_element = success.find("cas:user", ns)
        if user_element is None or not user_element.text:
            raise CasAuthenticationError(
                message="CAS authenticationSuccess missing cas:user element",
            )

        username = user_element.text.strip()
        if not username:
            raise CasAuthenticationError(
                message="CAS returned empty username",
            )

        logger.info("CAS ticket validated for user: %s", username)
        return username

    async def cas_login(self, ticket: str, service_path: str) -> Dict:
        """Perform full CAS login: validate ticket, find or create user.

        Args:
            ticket: The CAS service ticket (ST-...).
            service_path: The callback path string from request body.

        Returns:
            Dictionary with user profile data.
        """
        username = await self.validate_ticket(ticket, service_path)

        existing_user: UserProfile | None = await self.repo.find_one(
            username=username,
        )

        if existing_user:
            existing_user.last_login = datetime.now()
            saved_user = await self.repo.save(existing_user)
            logger.info(
                "Existing CAS user logged in: %s (id=%d)",
                username,
                saved_user.id,
            )
            return saved_user.to_dict()

        random_password = secrets.token_urlsafe(16)
        now = datetime.now()

        new_user = await self.repo.create(
            username=username,
            password=hash_password(random_password),
            role="Student",
            is_active=True,
            date_joined=now,
            last_login=now,
        )
        logger.info(
            "Created new CAS user: %s (id=%d)",
            username,
            new_user.id,
        )
        return new_user.to_dict()