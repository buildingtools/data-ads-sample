import json
# TODO: Fix * imports
from django.shortcuts import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from twitter_ads.client import Client
from twitter_ads.campaign import Campaign
from twitter_ads.error import Error
import datetime


@login_required
def json_handler(request):
    """
    Returns json_data {"campaigns": [campaign_list} for given request
    """

    client = Client(
        settings.SOCIAL_AUTH_TWITTER_KEY,
        settings.SOCIAL_AUTH_TWITTER_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET)
    account_id = request.GET.get("account_id", "")
    account = client.accounts(account_id)
    # TODO: Link to Ads API Docs for Campaign.rst
    campaigns = account.campaigns()
    campaign_list = []
    for campaign in campaigns:
        name = campaign.name
        identifier = campaign.id
        campaign_list.append({"name": name, "id": identifier})
    return HttpResponse(json.dumps(
        {"account_id": account_id, "campaigns": campaign_list}), content_type="application/json")


@login_required
def new(request):
    """
    Returns a new campaign
    """
    client = Client(
        settings.SOCIAL_AUTH_TWITTER_KEY,
        settings.SOCIAL_AUTH_TWITTER_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET)
    account_id = request.GET.get("account_id", "")
    campaign_name = request.GET.get("campaign", "")
    daily_budget = request.GET.get("daily_budget", "")
    account = client.accounts(account_id)
    # create your campaign
    json_data = {}
    try:
        campaign = Campaign(account)
        campaign.funding_instrument_id = account.funding_instruments().next().id
        campaign.daily_budget_amount_local_micro = int(daily_budget) * 1000
        campaign.name = campaign_name
        campaign.paused = True
        campaign.start_time = datetime.datetime.utcnow()
        campaign.save()
        json_data = {
            "valid": True,
            "account_id": account_id,
            "campaign_name": campaign_name,
            "campaign_id": campaign.id}
    except Error as e:
        json_data["response"] = e.details
        json_data["valid"] = False
        # passing as we send the json_data
        pass
    return HttpResponse(json.dumps(json_data), content_type="application/json")


@login_required
def handler(request):
    """
    Returns account page handler page for given request
    """
    account_id = request.GET.get("account_id", "")
    context = {"request": request, "account_id": account_id}
    return render_to_response(
        'campaigns.html',
        context,
        context_instance=RequestContext(request))
