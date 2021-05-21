from drf_yasg import openapi

from ..serializers import AuthorSerializer, PictureAuthorSerializer

bad_request = openapi.Response(
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
)

not_found = openapi.Response(
    description="Not found",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        title="Message",
        properties={
            "detail": openapi.Schema(
                type=openapi.TYPE_STRING,
            )
        },
    ),
)

unauthorized = openapi.Response(
    description="Unauthorized",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        title="Message",
        properties={
            "detail": openapi.Schema(
                type=openapi.TYPE_STRING,
            )
        },
    ),
)


forbidden = openapi.Response(
    description="Forbidden",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        title="Message",
        properties={
            "detail": openapi.Schema(
                type=openapi.TYPE_STRING,
            )
        },
    ),
)

create = dict(
    tags=["authors"],
    request_body=AuthorSerializer,
    responses={
        201: openapi.Response(description="Created", schema=AuthorSerializer),
        400: bad_request,
        401: unauthorized,
        403: forbidden,
    },
)

retrive = dict(
    tags=["authors"],
    responses={
        200: openapi.Response(description="Ok", schema=AuthorSerializer),
        400: bad_request,
        401: unauthorized,
        403: forbidden,
        404: not_found,
    },
)

update = dict(
    tags=["authors"],
    request_body=AuthorSerializer,
    responses={
        200: openapi.Response(description="Ok", schema=AuthorSerializer),
        400: bad_request,
        401: unauthorized,
        403: forbidden,
        404: not_found,
    },
)

delete = dict(
    tags=["authors"],
    responses={
        204: openapi.Response(description="No Content"),
        400: bad_request,
        401: unauthorized,
        403: forbidden,
        404: not_found,
    },
)

picture = dict(
    tags=["authors"],
    request_body=PictureAuthorSerializer,
    responses={
        200: openapi.Response(description="Ok", schema=PictureAuthorSerializer),
        400: bad_request,
        401: unauthorized,
        403: forbidden,
        404: not_found,
    },
)
