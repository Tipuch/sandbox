import uuid
from webauthn.helpers.structs import AttestationConveyancePreference
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Passkey(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    user_id: uuid.UUID = Field(index=True, foreign_key="user.id", nullable=False)
    challenge: str = Field(default="", nullable=False)
    timeout: int = Field(default=60000, nullable=False)
    attestation: str = Field(default=AttestationConveyancePreference.NONE)
    public_key: bytes
    sign_count: int = Field(default=0, nullable=False)
