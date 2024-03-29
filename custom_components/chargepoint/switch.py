"""Switch for ChargePoint Home Assistant Integration"""

import logging
import aiohttp
import asyncio

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import ATTRIBUTION, ATTR_ATTRIBUTION, DOMAIN, CHARGEPOINT_SERVICE
from .pyChargePoint import API

_LOGGER = logging.getLogger(__name__)

CHARGING_STATUS = 'charging_status'

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([ ChargePoint(hass.data[CHARGEPOINT_SERVICE]) ])


class ChargePoint(SwitchEntity):
    """Representation of the charging state of the car."""

    def __init__(self, api ):
        """Initialize the sensor."""
        _LOGGER.debug("INIT!!")

        self._state = None
        self._is_on = False
        self._name = None
        self._current_power_w = None
        self._unique_id = "CPH 25"
        self._device_class = "outlet"

        self._attrs = {
            ATTR_ATTRIBUTION: ATTRIBUTION
        }
        
        # reference to the shared ChargePoint client object       
        self._service = api

        #    parser = configparser.ConfigParser()
        #    parser.read(
        #        '/config/custom_components/chargepoint/pyChargePoint.cfg')

        #    secret = parser.get("DEFAULT", 'secret')
        #    userid = int(parser.get("DEFAULT", 'userid'))
        #    self.api = API(secret, userid)

    @property
    def unique_id(self) -> str:
        # FIXME: should be something truly unique about the device, like the ChargePoint serial number
        return self._unique_id

    @property
    def device_class(self) -> str:
        return self._device_class
    
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def current_power_w(self):
        """Return the current kwh in transfer"""
        return self._current_power_w

    @property
    def is_on(self):
        """Return if the state is charging"""
        return self._state == 'on'
        
    @property
    def should_poll(self) -> bool:
        return True

    async def async_toggle(self):
        _LOGGER.debug("TOGGLE!!")

        if self._is_on == 'off':
            self.turn_on()
        else:
            self.turn_off()

    async def async_turn_on(self):
        _LOGGER.debug("TURNING ON!!")
        try:
            async with aiohttp.ClientSession() as session:
                data = await self._service.action("startsession", session)
                await session.close()

            _LOGGER.debug(data)

            if data["ackid"] > 0:
                self._state = 'on'

        except Exception as e:
            _LOGGER.debug(str(e))

    async def async_turn_off(self):
        _LOGGER.debug("TURNING OFF!!")
        try:
            async with aiohttp.ClientSession() as session:
                data = await self._service.action("stopSession", session)
                await session.close()

            _LOGGER.debug(data)
            if data["ackid"] > 0:
                self._state = 'off'
        except Exception as e:
            _LOGGER.debug(str(e))

    async def async_update(self, **kwargs):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug("UPDATE!!")
        try: 
            async with aiohttp.ClientSession() as session:
                data = await self._service.info(session)
                await session.close()

            _LOGGER.debug(data)

            state = data[CHARGING_STATUS]["current_charging"]

            _LOGGER.debug(f"state:{state}")

            if state == 'done':
                self._state = 'off'
            elif state == 'fully_charged':
                self._state = 'on'
            elif state == 'waiting':
                self._state = 'on'
            elif state == 'not_charging':
                self._state = 'off'
            else :
                self._state = 'on'

            _LOGGER.debug(f"self._is_on:{self._is_on} state: {(self._state)}")

            self._name = data[CHARGING_STATUS]["device_name"]
            self._unique_id = data["charging_status"]["device_id"]
            self._current_power_w = float(data[CHARGING_STATUS]["power_kw_display"]) * 1000
            
        except Exception as e:
            _LOGGER.debug(str(e))

        
    @property
    def extra_state_attributes(self):
        """Return the attributes."""
        return self._attrs
