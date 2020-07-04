Settings
========

BMA_ACCESS_TOKEN
----------------

type: ``str``

default: ``''``

The BMA API access token to grant access to the APIs.

BMA_API_CLASS
-------------

type: ``bmaclient.MonitoringAPI``

default: ``None``

The BMA monitoring API custom class. This useful if you want to customize
default monitoring API class in the bmaclient library.

BMA_API_HOST
------------

type: ``str``

default ``''``

The BMA API host name. For example, DNS-based ``bma.cendana15.com`` or IP
address-based ``192.168.0.43:8080``.

BMA_API_KEY
-----------

type: ``str``

default: ``''``

The BMA API key to grant access to the APIs.

BMA_API_PROTOCOL
----------------

type: ``str``

default: ``''``

The BMA API HTTP protocol. Use either ``http`` or ``https``.


IGNORE_BMA_REQUEST_CACHE
------------------------

type: ``bool``

default: ``False``

Ignore BMA API request server cache. By default, BMA API will cache subsequent
request if query parameters are same. If True, KomaPy will append query
parameter with a random value to ignore server cache.


TIME_ZONE
---------

type: ``str``

default: ``Asia/Jakarta``

Default time zone name to use in the chart.
