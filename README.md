# ChargePoint for Home Assistant

![beta_badge](https://img.shields.io/badge/maturity-Alpha-red.png)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

## Installation

### Manual

Clone it in custom_components in your config folder. It should appears as an entity in your config (please it could takes as long as 30 secs before being accessible).

Also, it might be slow activating / deactivating since it's reverse engineered and slow as well on your phone. Please be patient (about 30 secs before the operation is updated). Meaning, if you activate from deactivation state, you will see the "button turning blue" as activated and couples of seconds afterwards going back to grey (deactivated), just wait 30 secs and it will update as blue. The ChargePoint API is slow too.

### Using Home Assistant Community Store (HACS)

The easiest way to install (and ensure you are always running the latest version), first setup [Home Assistant Community Store (HACS)](https://github.com/custom-components/hacs), and then add the "Integration" repository: **drynish/chargepoint**

#### Config Example

```yaml
chargepoint:
  email: your@email.com
  password: SECRET
  userid: 0000000
  secret: 'AAAAAAA'
```

## Known Issues

My first custom_component for Home Assistant. I've been testing it for two days and it seems to work, however as I'm not totally aware of ChargePoint api. I needed to get some secret passphrase using mitmproxy.

If you want to use that module, you have to complete the following:

* Create a pyChargePoint.cfg file like this:
```
[DEFAULT]
secret = AAAAAAA
userid = 0000000
```

DO NOT PUT apostrophies around secret ... it won't work!!!

The CP-Session-Token is a token sent with each transmission through your phone, so you'll have to proxy your phone to your computer and analyze packets sent when opening chargepoint app. (mitmweb) 

Search for it when you see connection to https://mc-ca.chargepoint.com/map-prod/v2. You need to look for userid too.

I will continue to look forward trying to find ways to obtain those without requiring to install mitmproxy but for now it's the only way

That's all... Good luck! :)

Michel

## Future

* replace the MITM credential mechanism
* YAML based Home Assistant configuration not yet implemented

## See Also

* [ChargePoint HA Support Thread](https://community.home-assistant.io/t/chargepoint-support/65353/7)
* [ChargePoint](https://www.chargepoint.com/)
