"""Platform for chargepoint integration."""
from homeassistant.components.switch import SwitchEntity
from .pyChargePoint import API

import configparser
import subprocess
import json
import logging
import aiohttp
import asyncio


_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([ChargePoint()])


class ChargePoint(SwitchEntity):
    """Representation of the charging state of the car."""

    def __init__(self, **kwargs):
        """Initialize the sensor."""

        _LOGGER.debug("INIT!!")
        self._state = None
        self._is_on = False
        self._name = None
        self._current_power_w = None
        self._unique_id = "CPH 25"
        self._device_class = "outlet"

        try:
            parser = configparser.ConfigParser()
            parser.read(
                '/config/custom_components/chargepoint/pyChargePoint.cfg')

            secret = parser.get("DEFAULT", 'secret')
            userid = int(parser.get("DEFAULT", 'userid'))
            self.api = API(secret, userid)

        except Exception as e:
            _LOGGER.debug(str(e))

    @property
    def unique_id(self) -> str:
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
                data = await self.api.action("startsession", session)
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
                data = await self.api.action("stopSession", session)
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
                data = await self.api.info(session)
                await session.close()

            # As funny as it might be, this state is the power off state.
            self._state = data["charging_status"]["current_charging"]
            if self._state == 'done':
                self._state = 'off'
            elif self._state == 'fully_charged':
                self._state = 'on'
            elif self._state == 'waiting':
                self._state = 'on'
            elif self._state == 'not_charging':
                self._state = 'off'
            else:
                self._state = 'on'

            _LOGGER.debug("self._is_on:" + str(self._is_on) +
                          " state: " + str(self._state))

            self._name = data["charging_status"]["device_name"]
            # self._unique_id = data["charging_status"]["device_id"]
            self._current_power_w = float(
                data["charging_status"]["power_kw_display"]) * 1000

        except Exception as e:
            _LOGGER.debug(str(e))
