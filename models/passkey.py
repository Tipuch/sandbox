from typing import Dict, Optional
import uuid
from webauthn.helpers.structs import (
    AttestationConveyancePreference,
    PublicKeyCredentialType,
)
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class AuthenticatorResponse(SQLModel):
    attestationObject: str
    authenticatorData: str
    clientDataJSON: str
    publicKey: Optional[str]
    publicKeyAlgorithm: int
    transports: list[str]


class PasskeyRegistration(SQLModel):
    authenticatorAttachment: Optional[str]
    clientExtensionResults: Dict[str, str]
    id: str
    rawId: str
    response: AuthenticatorResponse
    type: str


class Passkey(SQLModel, table=True):
    id: bytes = Field(primary_key=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    user_id: uuid.UUID = Field(index=True, foreign_key="user.id", nullable=False)
    attestation: bytes
    credential_type: str = Field(
        default=PublicKeyCredentialType.PUBLIC_KEY, nullable=False
    )
    format: str
    aaguid: str
    public_key: bytes
    sign_count: int = Field(default=0, nullable=False)
