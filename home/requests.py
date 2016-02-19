from gnip_search.gnip_search_api import GnipSearchAPI
from gnip_search.gnip_search_api import QueryError as GNIPQueryError
from timeframe import Timeframe
from django.conf import settings
import datetime
from errors import ApiError
import json
import logging
logging.info('Starting logger for ' + __name__)
gnip_logger = logging.getLogger(__name__)
gnip_logger.setLevel("INFO")

class GNIP:
    """
    Container wrapper for the GNIPSearchAPI
    """
    DEFAULT_TIMEFRAME = 90
    DATE_FORMAT = "%Y-%m-%d %H:%M"
    TIMEDELTA_DEFAULT_TIMEFRAME = datetime.timedelta(days=DEFAULT_TIMEFRAME)

    def __init__(self, request, query, query_count=None):
        self.api_request = self.api()
        self.request = request
        self.timeframe = self.request_timeframe(self.request)
        self.query = query
        self.query_count = query_count
        self.interval = self.request.GET.get("interval", "hour")
        # TODO: FIX THIS
        self.days = self.timeframe.days
        self.start = self.timeframe.start
        self.end = self.timeframe.end

    def request_timeframe(self, request):
        """
        Returns a timeframe to use in the API query
        """
        gnip_logger.info("Received request for timeline")
        request_timeframe = Timeframe(
            start=request.GET.get(
                "start", None), end=request.GET.get(
                "end", None), interval=request.GET.get(
                "interval", "hour"))
        return request_timeframe

    def api(self):
        """
        Returns GNIPSearchAPI
        """
        return GnipSearchAPI(settings.GNIP_USERNAME,
                             settings.GNIP_PASSWORD,
                             settings.GNIP_SEARCH_ENDPOINT,
                             paged=False)

    def get_timeline(self):
        """
        Returns a timeline of tweets e.g. Date > Tweet Count etc.
        """
        timeline = None
        try:
            timeline = self.api().query_api(
                pt_filter=str(
                    self.query),
                max_results=0,
                use_case="timeline",
                start=self.timeframe.start.strftime(
                    self.DATE_FORMAT),
                end=self.timeframe.end.strftime(
                    self.DATE_FORMAT),
                count_bucket=self.timeframe.interval,
                csv_flag=False)
        except GNIPQueryError as e:
            gnip_logger.error("%s (%s, %s)" % (e.message,
                                               e.payload,
                                               e.response))
            raise ApiError(json.dumps(e.message))

        return timeline

    def get_tweets(self):
        """
        Returns tweets in a list object
        """
        if (self.timeframe.start < datetime.datetime.now() -
            self.timeframe.TIMEDELTA_DEFAULT_TIMEFRAME) and (self.timeframe.start +
                                                             self.timeframe.TIMEDELTA_DEFAULT_TIMEFRAME > self.timeframe.end):
            end = self.timeframe.start + self.timeframe.TIMEDELTA_DEFAULT_TIMEFRAME
        query_nrt = self.query
        not_rt = "-(is:retweet)"
        if (not_rt not in query_nrt):
            query_nrt = query_nrt.replace("is:retweet", "")
            query_nrt = "%s %s" % (query_nrt, not_rt)
        tweets = None
        try:
            tweets = self.api().query_api(
                query_nrt,
                self.query_count,
                use_case="tweets",
                start=self.timeframe.start.strftime(
                    self.DATE_FORMAT),
                end=self.timeframe.end.strftime(
                    self.DATE_FORMAT))
        except GNIPQueryError as e:
                gnip_logger.error("%s (%s, %s)" % (e.message,
                                                   e.payload,
                                                   e.response))
        return tweets
