from uuid import uuid4

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import render

from .forms import UrlForm
from .serializers import UrlSerializer, UrlWatchResultSerializer
from .models import Url, UrlWatchResult


def url_home(request):
    """
    The home page of the url watch application
    """
    # add a UUID to session
    uuid = request.session.get("client_uuid", None)
    if uuid is None:
        uuid = str(uuid4())
        request.session["client_uuid"] = uuid

    url_form = UrlForm()

    return render(request, 'home.html', {"url_form": url_form, "uuid": uuid})


def url_list(request):
    """
    The list page of the url watch application
    """
    # add a UUID to session
    uuid = request.session.get("client_uuid", None)
    if uuid is None:
        uuid = str(uuid4())
        request.session["client_uuid"] = uuid

    return render(request, 'list.html', {"uuid": uuid})


class UrlView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request, format=None):

        serializer = UrlSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UrlListView(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, format=None):
        creator_uuid = request.session.get('client_uuid')
        if creator_uuid is None:
            return Response(
                'UnregistredUserError',
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            urls = Url.objects.filter(
                creator_uuid=creator_uuid
            ).order_by('url')

            print(urls)

            serializer = UrlSerializer(urls, many=True)

            return Response(
                serializer.data
            )
        except Exception as ex:
            return Response(
                str(ex),
                status=status.HTTP_400_BAD_REQUEST
            )


class UrlWatcherListView(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, id, format=None):
        creator_uuid = request.session.get('client_uuid')
        if creator_uuid is None:
            return Response(
                "UnregistredUserError",
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            watches = UrlWatchResult.objects.filter(
                creator_uuid=creator_uuid,
                url=Url.objects.get(
                    creator_uuid=creator_uuid,
                    id=id
                )
            ).order_by('-id')[:10]

            serializer = UrlWatchResultSerializer(watches, many=True)

            return Response(
                serializer.data
            )
        except Exception as ex:
            return Response(
                str(ex),
                status=status.HTTP_400_BAD_REQUEST
            )
