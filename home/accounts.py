import json
# TODO: Fix * imports
from django.shortcuts import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from twitter_ads.client import Client


@login_required
def json_handler(request):
    """
    Returns json_data {"accounts": [account_list]} for given request
    """
    client = Client(
        settings.SOCIAL_AUTH_TWITTER_KEY,
        settings.SOCIAL_AUTH_TWITTER_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET)
    accounts = client.accounts()
    # TODO: Link to Ads API Docs for Account.request
    account_list = []
    for account in accounts:
        name = account.name
        identifier = account.id
        account_list.append({"name": name, "id": identifier})
    return HttpResponse(json.dumps(
        {"accounts": account_list}), content_type="application/json")


@login_required
def handler(request):
    """
    Returns account page handler page for given request
    """
    context = {"request": request}
    return render_to_response(
        'accounts.html',
        context,
        context_instance=RequestContext(request))
