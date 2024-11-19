import time
import custom_components.chihiros.chihiros_led_control.chihirosctl as ctl

import asyncio

#ctl.list_devices()

CHIHIROS = "01136E3F-16B8-5759-DC3C-8F3911B7240C"

ctl.turn_on(CHIHIROS)
#ctl.set_brightness(CHIHIROS,25)

#time.sleep(5)
#ctl.turn_off(CHIHIROS)

#asyncio.run(ctl.get_device_from_address("01136E3F-16B8-5759-DC3C-8F3911B7240C"))