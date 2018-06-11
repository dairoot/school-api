import requests
import inspect
import logging
from school_api.client.api.base import BaseSchoolAPI
from bs4 import BeautifulSoup, SoupStrainer

logger = logging.getLogger(__name__)


def _is_api_endpoint(obj):
    return isinstance(obj, BaseSchoolAPI)


class BaseSchoolClient(object):
    BASE_URL = None
    _http = requests.Session()

    def __new__(cls, *args, **kwargs):
        self = super(BaseSchoolClient, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self):
        self._http.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/62.0.3202.89 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        })

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            url = '{base}{endpoint}'.format(
                base=self.BASE_URL,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint
        res = self._http.request(
            method=method,
            url=url,
            **kwargs
        )
        return res

    def get(self, url, **kwargs):
        return self._request(
            method='GET',
            url_or_endpoint=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self._request(
            method='POST',
            url_or_endpoint=url,
            **kwargs
        )

    def _get_view_state(self, url_suffix):
        res = self.get(url_suffix, allow_redirects=False)
        if res.status_code != 200:
            return None
        pre_soup = BeautifulSoup(res.text, "html.parser")
        _view_state = pre_soup.find(
            attrs={"name": "__VIEWSTATE"})['value']
        return _view_state

    def _update_headers(self, headers_dict):
        self._http.headers.update(headers_dict)
