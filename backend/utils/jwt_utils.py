from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app


def generate_jwt(payload: dict, expires_minutes: int | None = None) -> str:
  """
  Generate a JWT token using the app's JWT_SECRET_KEY.
  """
  if expires_minutes is None:
      expires_minutes = current_app.config.get("JWT_EXPIRATION_MINUTES", 60)

  secret = current_app.config.get("JWT_SECRET_KEY") or current_app.config.get("JWT_SECRET")
  algorithm = current_app.config.get("JWT_ALGORITHM", "HS256")

  to_encode = payload.copy()
  # PyJWT validates that registered claim "sub" is a string (RFC 7519).
  if "sub" in to_encode and to_encode["sub"] is not None:
      to_encode["sub"] = str(to_encode["sub"])
  exp = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
  to_encode["exp"] = exp

  token = jwt.encode(to_encode, secret, algorithm=algorithm)
  return token


def decode_jwt(token: str) -> dict | None:
  """
  Decode and validate a JWT token.
  Returns the payload dict if valid, otherwise None.
  """
  secret = current_app.config.get("JWT_SECRET_KEY") or current_app.config.get("JWT_SECRET")
  algorithm = current_app.config.get("JWT_ALGORITHM", "HS256")

  try:
      payload = jwt.decode(token, secret, algorithms=[algorithm])
      return payload
  except jwt.ExpiredSignatureError:
      return None
  except jwt.InvalidTokenError:
      return None

