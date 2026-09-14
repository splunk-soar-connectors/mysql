# File: mysql_tls.py
#
# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

import pymysql
from pymysql.constants import CLIENT, CR


def require_tls_capability(server_capabilities):
    """Reject a server that cannot negotiate TLS before authentication begins."""
    if not server_capabilities & CLIENT.SSL:
        raise pymysql.err.OperationalError(
            CR.CR_SSL_CONNECTION_ERROR,
            "The MySQL server did not advertise required TLS support",
        )


class TlsRequiredConnection(pymysql.connections.Connection):
    """PyMySQL connection that refuses plaintext authentication fallback."""

    def _get_server_information(self):
        super()._get_server_information()
        if self.ssl:
            require_tls_capability(self.server_capabilities)
