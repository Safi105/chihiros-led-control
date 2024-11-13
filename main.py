import time
import custom_components.chihiros.chihiros_led_control.chihirosctl as ctl

ctl.list_devices()

#ctl.turn_on("01136E3F-16B8-5759-DC3C-8F3911B7240C")
#time.sleep(5)
#ctl.turn_off("01136E3F-16B8-5759-DC3C-8F3911B7240C")

ctl.get_device_from_address("01136E3F-16B8-5759-DC3C-8F3911B7240C")