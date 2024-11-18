import requests
from rest_framework import status
from rest_framework.response import Response

url = 'https://autoplaner.ir'
def response_request():
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        return Response({'data': 'it is valid'}, status=status.HTTP_200_OK)
    else:
        return Response({'data': 'it is invalid'}, status=status.HTTP_400_BAD_REQUEST)
