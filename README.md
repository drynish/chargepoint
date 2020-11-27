# ChargePoint EV charger integrated in home_assistant #

My first custom_components for home_assistant. I've been testing it for two days and it seems to work, however as I'm not totally aware of ChargePoint api. I needed to get some secret passphrase using mitmproxy.

If you want to use that module, you have to complete the following:

* Create a pyChargePoint.cfg file like this:

[DEFAULT]
secret = 'AAAAAAA'
userid = 0000000

The secret is a cookie sent with each transmission through your phone, so you'll have to proxy your phone to your computer and analyze packets sent when opening chargepoint app.

If you open some transmission going to https://mc-ca.chargepoint.com/map-prod/v2, you should have what is needed for my software to access the API. I will continue to look forward trying to find ways to obtain those without requiring to install mitmproxy but for now it's the only way

That's all...

Good luck! :)

Michel
