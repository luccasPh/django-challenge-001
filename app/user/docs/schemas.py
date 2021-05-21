from drf_yasg import openapi

from ..serializers import LoginSerializer, SignUpSerializer

login = dict(
    tags=["users"],
    security=[],
    request_body=LoginSerializer,
    responses={
        200: openapi.Response(
            description="Ok",
            schema=openapi.Schema(
                title="Token",
                type=openapi.TYPE_OBJECT,
                properties={"token": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        ),
        400: openapi.Response(
            description="Bad request",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                title="Errors",
                properties={
                    "field": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
        ),
    },
)


signup = dict(
    tags=["users"],
    security=[],
    request_body=SignUpSerializer,
    responses={
        201: openapi.Response(
            description="Created",
            schema=openapi.Schema(
                title="User",
                type=openapi.TYPE_OBJECT,
                properties={
                    "email": openapi.Schema(
                        type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL
                    )
                },
            ),
        ),
        400: openapi.Response(
            description="Bad request",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                title="Errors",
                properties={
                    "field": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                    )
                },
            ),
        ),
    },
)
