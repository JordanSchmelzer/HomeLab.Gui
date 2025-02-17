import requests
import logging


class ApiClient():
  
  def __init__(
    self,
    base_url: str,
    headers=None,
    timeout=10
    ) -> None:
    self.base_url = base_url
    self.headers = headers if headers else {}
    self.timeout = timeout


    def get(self, endpoint, params=None):
      url = f"{self.base_url}/{endpoint}"
      try:
        response = requests.get(
          url, headers=self.headers, params=params, timeout=self.timeout)
        return self._handle_response(response)
      except requests.RequestException as e:
        logging.error(f"GET request failed: {e}")
        return None


    def post(self, endpoint, data=None, json=None):
      url = f"{self.base_url}/{endpoint}"
      try:
        response = requests.post(
          url, headers=self.headers, data=data, json=json, timeout=self.timeout)
        return self._handle_response(response)
      except requests.RequestException as e:
        logging.error(f"POST request failed: {e}")
        return None


    def put(self, endpoint, data=None, json=None):
      url = f"{self.base_url}/{endpoint}"
      try:
        response = requests.put(
          url, headers=self.headers, data=data, json=json, timeout=self.timeout)
        return self._handle_response(response)
      except requests.RequestException as e:
        logging.error(f"PUT request failed: {e}")
        return None


    def delete(self, endpoint, params=None):
      url = f"{self.base_url}/{endpoint}"
      try:
        response = requests.delete(
          url, headers=self.headers, params=params, timeout=self.timeout)
        return self._handle_response(response)
      except requests.RequestException as e:
        logging.error(f"DELETE request failed: {e}")
        return None
        

    def _handle_response(self, response):
      if response.satatus_code == 200:
         return response.json()
      else:
        response.raise_for_status() 
