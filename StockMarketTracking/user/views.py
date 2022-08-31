from rest_framework import permissions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializer import UserSerializer


class RegisterView(APIView):
    """
    Handles request related to user account creation.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request: Request):
        """
        Creates user account.

        :param request: contains data got from the client
        :return: data and status code
        """

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
