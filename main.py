#!/bin/python

from pyChargePoint import API
import configparser
import asyncio

async def main():
    parser = configparser.ConfigParser()
    parser.read('pyChargePoint.cfg')
                    
    secret = parser.get("DEFAULT",'secret')
    userid = int(parser.get("DEFAULT",'userid'))

    print (secret)
    api = API("YzExYTU4NTUtMmY5ZC00MjIyLWE2ODMtNTgxMTg0YjFkNTAz#D135394d#RNA-CA", userid)    

    print (await api.action("stopSession"))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
