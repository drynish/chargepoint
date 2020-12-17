"""ChargePoint Home Assistant Integration"""

import logging

import voluptuous as vol

from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_SCAN_INTERVAL
from homeassistant.helpers import config_validation as cv, discovery

from .pyChargePoint import API

from .const import CHARGEPOINT_DOMAIN, CHARGEPOINT_SERVICE

LOG = logging.getLogger(__name__)

# FIXME: temporary until username/password authentication works
CONF_SECRET = 'secret'
CONF_USERID = 'userid'

# Example config:
#
# chargepoint:
#   username: your@email.com
#   password: SECRET
CONFIG_SCHEMA = vol.Schema({
        CHARGEPOINT_DOMAIN: vol.Schema({
#            vol.Required(CONF_USERNAME): cv.string,
#            vol.Required(CONF_PASSWORD): cv.string
            vol.Required(CONF_SECRET): cv.string,
            vol.Required(CONF_USERID): cv.string
        })
    }, extra=vol.ALLOW_EXTRA
)

SUPPORTED_PLATFORMS = [ 'switch' ]

def setup(hass, config):
    """Initialize the ChargePoint integration"""
    conf = config[CHARGEPOINT_DOMAIN]

    # initialize the ChargePoint service client
    try:
        #username = conf.get(CONF_USERNAME)
        #password = conf.get(CONF_PASSWORD)
        
        hass.data[CHARGEPOINT_SERVICE] = API( conf.get(CONF_SECRET), conf.get(CONF_USERID))
    except Exception as e:
        LOG.error("Failed connecting to ChargePoint service %s", str(e))
        return False
   
    # configure and initialize all the integrations for ChargePoint devices
    #  ... each component shares the hass.data[CHARGEPOINT_DOMAIN] service object
    for platform in SUPPORTED_PLATFORMS:
        discovery.load_platform(hass, platform, CHARGEPOINT_DOMAIN, {}, config)

    return True
