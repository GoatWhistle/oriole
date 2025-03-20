from fastapi_users.authentication import BearerTransport

bearer_transport = BearerTransport(
    # TODO: обновить url
    tokenUrl="auth/jwt/login",
)
