from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities([
        PGESaldoIndexSensor(coordinator, entry),
        PGETerminSensor(coordinator, entry),
        PGEPowidomieniaSensor(coordinator, entry),
        PGESumaFinanseSensor(coordinator, entry),
        PGEDokumentySensor(coordinator, entry),
        PGEZuzycieStrefa1Sensor(coordinator, entry),
        PGEZuzycieStrefa2Sensor(coordinator, entry)
    ])

class PGEBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.entry = entry

    @property
    def device_info(self):
        account_id = self.coordinator.data.get("account_id", "Konto")
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": f"PGE eBOK ({account_id})",
            "manufacturer": "PGE",
        }

class PGESaldoIndexSensor(PGEBaseSensor):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_name = "PGE Saldo bieżące"
        self._attr_unique_id = f"{entry.entry_id}_saldo_index"
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_native_unit_of_measurement = "PLN"
        self._attr_icon = "mdi:cash-multiple"

    @property
    def native_value(self):
        return self.coordinator.data.get("saldo_index")

class PGETerminSensor(PGEBaseSensor):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_name = "PGE Dni do terminu płatności"
        self._attr_unique_id = f"{entry.entry_id}_termin_za_dni"
        self._attr_icon = "mdi:calendar-clock"
        self._attr_native_unit_of_measurement = "dni"

    @property
    def native_value(self):
        return self.coordinator.data.get("termin_za_dni")

# NOWOŚĆ: Klasa sensora powiadomień
class PGEPowidomieniaSensor(PGEBaseSensor):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_name = "PGE Liczba nowych powiadomień"
        self._attr_unique_id = f"{entry.entry_id}_powiadomienia_liczba"
        self._attr_icon = "mdi:bell-alert"
        self._attr_native_unit_of_measurement = "szt"

    @property
    def native_value(self):
        return self.coordinator.data.get("powiadomienia_liczba")

class PGESumaFinanseSensor(PGEBaseSensor):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_name = "PGE Finanse W sumie"
        self._attr_unique_id = f"{entry.entry_id}_w_sumie_finanse"
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_native_unit_of_measurement = "PLN"
        self._attr_icon = "mdi:wallet"

    @property
    def native_value(self):
        return self.coordinator.data.get("w_sumie_finanse")

class PGEDokumentySensor(PGEBaseSensor):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_name = "PGE Liczba dokumentów"
        self._attr_unique_id = f"{entry.entry_id}_dokumenty_liczba"
        self._attr_icon = "mdi:file-document-multiple"
        self._attr_native_unit_of_measurement = "szt"

    @property
    def native_value(self):
        return self.coordinator.data.get("dokumenty_liczba")

class PGEZuzycieStrefa1Sensor(PGEBaseSensor):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_name = "PGE Zużycie Strefa 1"
        self._attr_unique_id = f"{entry.entry_id}_zuzycie_strefa_1"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_native_unit_of_measurement = "kWh"
        self._attr_icon = "mdi:lightning-bolt"

    @property
    def native_value(self):
        return self.coordinator.data.get("zuzycie_strefa_1")

    @property
    def extra_state_attributes(self):
        return {"okres_rozliczenia_do": self.coordinator.data.get("zuzycie_data_aktualizacji")}

class PGEZuzycieStrefa2Sensor(PGEBaseSensor):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_name = "PGE Zużycie Strefa 2"
        self._attr_unique_id = f"{entry.entry_id}_zuzycie_strefa_2"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_native_unit_of_measurement = "kWh"
        self._attr_icon = "mdi:lightning-bolt-outline"

    @property
    def native_value(self):
        return self.coordinator.data.get("zuzycie_strefa_2")

    @property
    def extra_state_attributes(self):
        return {"okres_rozliczenia_do": self.coordinator.data.get("zuzycie_data_aktualizacji")}