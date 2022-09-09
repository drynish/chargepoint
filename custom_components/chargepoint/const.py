from homeassistant.const import (TIME_MINUTES, ENERGY_KILO_WATT_HOUR)

DOMAIN = 'chargepoint'
CHARGEPOINT_DOMAIN = 'chargepoint'
CHARGEPOINT_SERVICE = 'chargepoint_svc'

ATTRIBUTION = "Data by Chargepoint"
ATTR_ATTRIBUTION = 'attribution'

ICON_SENSOR = "mdi:ev-station"
ICON_SWITCH = "mdi:battery-charging"

# FIXME: found these in https://github.com/home-assistant/core/blob/dev/homeassistant/components/openevse/sensor.py
SENSOR_TYPES = {
    "status": ["Charging Status", None],
    "charge_time": ["Charge Time Elapsed", TIME_MINUTES],
    "usage_session": ["Usage this Session", ENERGY_KILO_WATT_HOUR],
    "usage_total": ["Total Usage", ENERGY_KILO_WATT_HOUR],
}
