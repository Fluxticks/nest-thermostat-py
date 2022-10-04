from Api import Api
from models.Trait import *


THERMOSTAT_TYPE = "sdm.devices.types.THERMOSTAT"


class Thermostat:
    __traits__ = [
        "Connectivity",
        "Fan",
        "Humidity",
        "Info",
        "Settings",
        "Temperature",
        "ThermostatEco",
        "ThermostatHvac",
        "ThermostatMode",
        "ThermostatTemperatureSetpoint",
    ]
    __slots__ = (
        "_raw_data",
        "_device_id",
        *__traits__,
    )

    def __init__(self, data: dict):
        self._raw_data = data
        self.set_values()

    def set_values(self, data: dict = None):
        if not data:
            data = self._raw_data
        else:
            self._raw_data = data

        if data.get("type") != THERMOSTAT_TYPE:
            raise ValueError(
                f"Expected device type to be {THERMOSTAT_TYPE} but got {data.get('type')} instead"
            )

        self._device_id = data.get("name", "").split("/")[-1]

        traits = data.get("traits")

        for trait in self.__traits__:
            cls = globals()[f"{trait}Trait"]
            setattr(self, trait, cls(traits.get(cls.domain())))

    async def update_device(self, api: Api):
        data = await api.get_exact_device(self.device_id)
        self.set_values(data)

    @property
    def device_id(self):
        return self._device_id
