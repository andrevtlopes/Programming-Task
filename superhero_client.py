#!/usr/bin/env python

import requests
import logging
import os
import sys

from requests.adapters import HTTPAdapter, Retry

base_url = 'https://akabab.github.io/superhero-api/api'
headers = {'Content-Type': 'application/json'}

# Set up basic logger
logger = logging.getLogger('superhero.client')

# Setup stdout logger
soh = logging.StreamHandler(sys.stdout)
logger.addHandler(soh)

# Get log level from env vars
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
if os.environ.get('DEBUG'):
    if log_level:
        logger.warn("Overriding LOG_LEVEL setting with DEBUG")
    log_level = 'DEBUG'

try:
    logger.setLevel(log_level)
except ValueError:
    logger.setLevel(logging.INFO)
    logger.warn("LOG_LEVEL is not valid - Log Level set to INFO")


class SuperHeroClient(object):
    """A Class to handle the client of the superhero-api

    Attributes
    ----------
    base_url : str
        the base url from the api
    session : Session
        the current request session

    Methods
    -------
    from_api(hero)
        Initialize super hero from API object
    """
    def __init__(self):
        """Set up client for API communications"""
        # Setup Host here
        self.base_url = base_url
        # Setup Session object for all future API calls
        self.session = requests.Session()

        retries = Retry(total=5, backoff_factor=1,
                        status_forcelist=[502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

        if headers:
            self.session.headers.update(headers)

    def _make_request(self, route, method, params=None, body=None):
        """Handles all requests to the Super Hero API

        Parameters
        ----------
        route : str
            the api route
        method : str
            the method of request
        params : dict
            params to send in the request call
        body : dict
            message body to be sent in the request call

        Raises
        ------
        HTTPError
            Raises HTTP error if response status code is 4XX or 5XX

        Returns
        -------
        dict
            Super Hero information
        """
        url = self.base_url + route
        req = requests.Request(method, url, params=params, json=body)
        prepped = self.session.prepare_request(req)

        # Make request to endpoint
        r = self.session.send(prepped)

        if r.status_code == requests.codes.ok:
            try:
                res_json = r.json()
                logger.debug('Response: {}'.format(res_json))
                return res_json
            except ValueError:
                return r.text

        elif r.status_code == 404:
            logger.debug('{} not found!'.format(route))

        # Raises HTTP error if status_code is 4XX or 5XX
        elif r.status_code >= 400:
            logger.error('Received a ' + str(r.status_code) + ' error!')
            try:
                logger.debug('Details: ' + str(r.json()))
            except ValueError:
                pass
            r.raise_for_status()

    def make_request(
        self,
        route,
        method='GET',
        params=None,
        body=None
    ):
        """Make Request for the API with a route, params and body if needed

        Parameters
        ----------
        route : str
            the api route
        method : str
            the method of request
        params : dict
            params to send in the request call
        body : dict
            message body to be sent in the request call

        Raises
        ------
        HTTPError
            Raises HTTP error if response status code is 4XX or 5XX

        Returns
        -------
        dict
            Super Hero information
        """
        return self._make_request(route, method, params, body)

    def get_biography(self, hero_id):
        """Make Request to get biography of a specific super hero

        Parameters
        ----------
        hero_id : int
            the super hero id

        Raises
        ------
        HTTPError
            Raises HTTP error if response status code is 4XX or 5XX

        Returns
        -------
        dict
            Super Hero information
        """
        route = '/biography/{}.json'.format(hero_id)
        res = self._make_request(route, 'GET')
        return res

    def get_super_hero(self, hero_id):
        """Make Request to get all information of a specific super hero

        Parameters
        ----------
        hero_id : int
            the super hero id

        Raises
        ------
        HTTPError
            Raises HTTP error if response status code is 4XX or 5XX

        Returns
        -------
        dict
            Super Hero information
        """
        endpoint = '/id/{}.json'.format(hero_id)
        return self._make_request(endpoint, 'GET')
