import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
"""
A pretty simple wrapper around request.
Added support for retrying X times when using 'get' or 'post'.
"""
class AhRequest():    
    def __init__(self, retries=3, backoff_factor=0.3):
        self.retries = retries
        self.backoff_factor = backoff_factor
        
    def requests_retry_session(self,session=None):
        session = session or requests.Session()
        retry = Retry(
            total=self.retries,
            read=self.retries,
            connect=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=(400,401,403,404,500,501,502,503,504),
            method_whitelist=frozenset(['GET', 'POST'])
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def get(self,url,timeout=None):
        return self.requests_retry_session().get(url,timeout=timeout)
    
    def post(self,url,data={},timeout=None):
        return self.requests_retry_session().post(url,data=data,timeout=timeout)