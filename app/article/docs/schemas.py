from drf_yasg import openapi

from ..serializers import ArticleSerializer, ListArticleSerializer

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

admin_create = dict(
    tags=["articles"],
    request_body=ArticleSerializer,
    responses={
        201: openapi.Response(description="Created", schema=ArticleSerializer),
        400: bad_request,
        401: unauthorized,
        403: forbidden,
    },
)

admin_retrive = dict(
    tags=["articles"],
    responses={
        200: openapi.Response(description="Ok", schema=ArticleSerializer),
        400: bad_request,
        401: unauthorized,
        403: forbidden,
        404: not_found,
    },
)

admin_update = dict(
    tags=["articles"],
    request_body=ArticleSerializer,
    responses={
        200: openapi.Response(description="Ok", schema=ArticleSerializer),
        400: bad_request,
        401: unauthorized,
        403: forbidden,
        404: not_found,
    },
)

admin_delete = dict(
    tags=["articles"],
    responses={
        204: openapi.Response(description="No Content"),
        400: bad_request,
        401: unauthorized,
        403: forbidden,
        404: not_found,
    },
)


list = dict(
    tags=["articles"],
    manual_parameters=[
        openapi.Parameter(
            "category",
            openapi.IN_QUERY,
            description="article category",
            type=openapi.TYPE_STRING,
        )
    ],
    responses={
        200: openapi.Response(
            description="Ok", schema=ListArticleSerializer(many=True)
        ),
        400: bad_request,
    },
)
detail = dict(
    tags=["articles"],
    responses={
        200: openapi.Response(description="Ok", schema=ArticleSerializer),
        400: bad_request,
        404: not_found,
    },
)
