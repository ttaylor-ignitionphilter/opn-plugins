"""
    Copyright (c) 2025 Treg Taylor <tech@ignitionphilter.com>
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
    AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
    OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
    ----------------------------------------------------------------------------------------------------
    Internetbs updater
    ApiKey should be set via the username field
"""
import syslog
import requests
from . import BaseAccount


class Internetbs(BaseAccount):
    _services = ['internetbs']

    def __init__(self, account: dict):
        super().__init__(account)

    @staticmethod
    def known_services():
        return  Internetbs._services

    @staticmethod
    def match(account):
        return account.get('service') in Internetbs._services

    def execute(self):
        """ Internetbs DNS update
        """
        if super().execute():
            zone = self.settings.get('zone')
          
          req_opts = {
                'url': 'https://api.internet.bs/Domain/Host/Update',
                'params': {
                  'ApiKey': self.settings.get('apikey'),
                  'Password': self.settings.get('password'),
                  'Host': zone,
                  'ResponseFormat': 'JSON',
                  'IP_List': self.current_address
                },
                'headers': {
                    'User-Agent': 'OPNsense-dyndns'
                }
            }
            
            response = requests.post(**req_opts)
            
            if response.status_code != 200:
                syslog.syslog(
                    syslog.LOG_ERR,
                    "Account %s zone: %s error posting  response: [%d - %s]" % (self.description, zone, response.status_code, response.text)
                )
                return None

            try:
                payload = response.json()
            except requests.exceptions.JSONDecodeError:
                syslog.syslog(
                    syslog.LOG_ERR,
                    "Account %s zone: %s error parsing JSON response: %s" % (self.description, zobe, response.text)
                )
                return None
          
            if response.status_code not in [200] or payload.status = 'FAILURE':
              raise RuntimeError(
                  f"Account {self.description} zone: {zone} Internetbs update failed with ip {self.current_address} response: {response.text}")
              except Exception as e:
                syslog.syslog(syslog.LOG_ERR, str(e))
              return False

            syslog.syslog(
                syslog.LOG_NOTICE,
                "Account %s zone: %s Internetbs status %s new ip %s % (self.description, zone, payload.status, self.current_address)
            )
      
            self.update_state(address=self.current_address)
      
            return True
