from os import environ
import urllib

from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView


gatherer_uri = 'http://gatherer.wizards.com/Handlers/Image.ashx?type=card'


class RootView(APIView):
    """
    Nothing here but me.
    """
    def get(self, request):
        print 'wtf this is a get'
        return Response({'root': 'Nothing here but me'})


class SlackMagicCardView(APIView):
    """
    Slack webhook interface for returning details of magic card.
    """
    def post(self, request):
        if 'token' not in request.data:
            raise PermissionDenied
        if request.data['token'] != environ['SLACK_HOOK_TOKEN'] or request.data['token'] != environ['SLACK_SLASH_TOKEN']:
            raise PermissionDenied

        if 'text' not in request.data:
            raise ParseError

        if request.data['text'].startswith('magicbot:'):
            card_name = request.data['text'][9:].strip(' ')
        else:
            card_name = request.data['text'].strip(' ')
        card_img_uri = '{}&name={}'.format(gatherer_uri, urllib.quote_plus(card_name))

        return Response({
            'text': card_img_uri
        })

