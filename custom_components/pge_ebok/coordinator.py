from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD
from .api import PGEEbokAPI

_LOGGER = logging.getLogger(__name__)

class PGEDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(days=1),
        )
        self.api = PGEEbokAPI(entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])

    async def _async_update_data(self):
        try:
            return await self.api.fetch_data()
        except Exception as err:
            raise UpdateFailed(f"Błąd komunikacji z PGE eBok: {err}")
