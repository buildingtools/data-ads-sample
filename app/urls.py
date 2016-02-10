from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from app import settings
from home import views, accounts,campaigns, lineitems, audiences

urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^home$', views.home, name='home'),
    url(r'^logout$', views.logout, name='logout'),

    # Queries for Graphing
    url(r'^query/chart', views.query_chart, name='query_chart'),
    url(r'^query/tweets', views.query_tweets, name='query_tweets'),
    url(r'^query/frequency', views.query_frequency, name='query_frequency'),

    # ADS API Handlers
    url(r'^ads/accounts', accounts.handler, name='ads_accounts'),
    url(r'^ads/api/accounts', accounts.json_handler, name='ads_api_accounts'),

    # ADS API Campaigns
    url(r'^ads/campaigns', campaigns.handler, name='ads_campaigns'),
    url(r'^ads/api/campaigns', campaigns.json_handler, name='ads_api_campaigns'),
    url(r'^ads/api/campaign/new', campaigns.new, name='ads_api_campaign_new'),

    # ADS API LineItems
    url(r'^ads/line_items', lineitems.handler, name='ads_line_items'),
    url(r'^ads/api/line_items', lineitems.json_handler, name='ads_api_line_items'),
    url(r'^ads/api/line_item/new', lineitems.new, name='ads_api_line_item_new'),

    # ADS API Targeting
    url(r'^ads/api/targeting/new', lineitems.new_targeting, name='ads_api_new_targeting'),

    # ADS API Audiences
    url(r'^ads/audiences', audiences.handler, name='ads_audiences'),
    url(r'^ads/api/audiences/new', audiences.new, name='ads_audiences_new'),
    url(r'^ads/api/audiences/change', audiences.change, name='ads_audiences_change'),

    # Login setup with Twitter
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
)

urlpatterns += patterns('',
 (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
 )
