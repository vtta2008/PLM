# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import requests

from pyPLM.damg import DAMG


class NetworkInfo(DAMG):

    key                             = 'NetworkInfo'

    info = requests.get('https://api.ipdata.co?api-key=test').json()

    def __init__(self, parent=None):
        super(NetworkInfo, self).__init__()

        self._parent                = parent

        self._ip                    = self.info['ip']
        self._city                  = self.info['city']
        self._country               = self.info['country_name']
        self._latitude              = self.info['latitude']
        self._longtitude            = self.info['longtitude']

    def cityInfo(self):
        return {'latitude': self.info['latitude'], 'longitude': self.info['longitude'],
                'city': self.info['city'], 'country': self.info['country_name'], }

    def networkInfo(self):
        asn = self.info['asn']
        return {'ip': self.info['ip'], 'asn': asn['asn'], 'provider': asn['name'],
                'domain': asn['domain'], 'route': asn['route'], 'type': asn['type']}

    def performanceInfo(self):
        data = self.info['threat']
        return {'torrent': data['is_tor'], 'proxy': data['is_proxy'], 'anoymous': data['is_anonymous'],
                'attacker': data['is_known_attacker'], 'abuser': data['is_known_abuser'], 'threat': data['threat'],
                'bogon': data['is_bogon']}


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
