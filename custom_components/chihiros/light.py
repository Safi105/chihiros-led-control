from __future__ import annotations
import logging
from typing import Any, Optional

from homeassistant.components.light import ATTR_BRIGHTNESS, ATTR_RGB_COLOR, ATTR_COLOR_TEMP, ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .chihiros_led_control.device import BaseDevice
from .const import DOMAIN, MANUFACTURER
from .coordinator import ChihirosDataUpdateCoordinator
from .models import ChihirosData

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the light platform for Chihiros LED with dynamic channel detection."""
    chihiros_data: ChihirosData = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.debug("Setting up Chihiros RGBW light with dynamic channel support")
    async_add_entities([ChihirosLightEntity(chihiros_data.coordinator, chihiros_data.device, entry)])

class ChihirosLightEntity(LightEntity, RestoreEntity):
    """Representation of a Chihiros light device with dynamic channel support."""

    def __init__(self, coordinator: ChihirosDataUpdateCoordinator, device: BaseDevice, config_entry: ConfigEntry) -> None:
        """Initialize the light entity."""
        super().__init__()
        self._device = device
        self._address = coordinator.address
        self._attr_name = f"{self._device.name} Light"
        self._attr_unique_id = f"{self._address}_light"
        self._attr_device_info = DeviceInfo(
            connections={(dr.CONNECTION_BLUETOOTH, self._address)},
            manufacturer=MANUFACTURER,
            model=self._device.model_name,
            name=self._device.name,
        )
        self._channels = len(device.colors)  # Number of light channels
        self._set_supported_color_modes()

    def _set_supported_color_modes(self):
        """Set supported color modes based on channel count."""
        if self._channels == 2:
            self._attr_supported_color_modes = {ColorMode.COLOR_TEMP}
            self._attr_color_mode = ColorMode.COLOR_TEMP
        elif self._channels == 3:
            self._attr_supported_color_modes = {ColorMode.RGB}
            self._attr_color_mode = ColorMode.RGB
        elif self._channels == 4:
            self._attr_supported_color_modes = {ColorMode.RGBW}
            self._attr_color_mode = ColorMode.RGBW
        else:
            _LOGGER.warning("Unsupported channel count: %s", self._channels)

    @property
    def brightness(self) -> int | None:
        return self._attr_brightness

    @property
    def rgb_color(self) -> tuple[int, int, int] | None:
        return self._attr_rgb_color

    @property
    def color_temp(self) -> int | None:
        return self._attr_color_temp

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light with dynamic channel handling."""
        self._attr_is_on = True
        if ATTR_BRIGHTNESS in kwargs:
            self._attr_brightness = kwargs[ATTR_BRIGHTNESS]

        if self._channels == 2 and ATTR_COLOR_TEMP in kwargs:
            self._attr_color_temp = kwargs[ATTR_COLOR_TEMP]
            await self._device.set_color_temp(self._attr_color_temp)

        elif self._channels == 3 and ATTR_RGB_COLOR in kwargs:
            self._attr_rgb_color = kwargs[ATTR_RGB_COLOR]
            await self._device.set_rgb(self._attr_rgb_color, self._attr_brightness)

        elif self._channels == 4 and ATTR_RGB_COLOR in kwargs:
            self._attr_rgb_color = kwargs[ATTR_RGB_COLOR]
            await self._device.set_rgbw(self._attr_rgb_color, self._attr_brightness)

        self.schedule_update_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        _LOGGER.debug("Turning off light: %s", self.name)
        await self._device.turn_off()
        self._attr_is_on = False
        self.schedule_update_ha_state()
