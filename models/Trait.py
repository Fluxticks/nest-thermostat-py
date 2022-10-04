from abc import abstractclassmethod

from Api import Api

__all__ = [
    "ConnectivityTrait",
    "FanTrait",
    "HumidityTrait",
    "InfoTrait",
    "SettingsTrait",
    "TemperatureTrait",
    "ThermostatEcoTrait",
    "ThermostatHvacTrait",
    "ThermostatModeTrait",
    "ThermostatTemperatureSetpointTrait",
]


class Trait:
    __slots__ = ("trait_name", "device_id")

    def __init__(self, device_id: str):
        self.trait_name = self.domain().split(".")[-1]
        self.device_id = device_id

    @abstractclassmethod
    def domain(cls):
        pass


class ConnectivityTrait(Trait):
    __slots__ = "_status"

    def __init__(self, device_id: str, data: dict):
        if not data:
            self._status = "OFFLINE"
        else:
            self._status = data.get("status")
        super().__init__(device_id)

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.Connectivity"

    @property
    def status(self):
        return self._status

    @property
    def is_connected(self):
        return self._status == "ONLINE"


class FanTrait(Trait):
    __slots__ = ("_timer_mode", "_timer_timeout")

    def __init__(self, device_id: str, data: dict):
        if not data:
            self._timer_mode = None
            self._timer_timeout = None
        else:
            self._timer_mode = data.get("timerMode")
            self._timer_timeout = data.get("timerTimeout")
        super().__init__(device_id)

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.Fan"

    @property
    def mode(self):
        return self._timer_mode

    @property
    def is_on(self):
        return self.mode == "ON"

    @property
    def timeout_string(self):
        return self._timer_timeout

    @property
    def timeout_time(self):
        # TODO: Convert to datetime value
        return self.timeout_string


class HumidityTrait(Trait):
    __slots__ = "_humidity_percentage"

    def __init__(self, device_id: str, data: dict):
        if not data:
            self._humidity_percentage = None
        else:
            try:
                self._humidity_percentage = float(data.get("ambientHumidityPercent"))
            except TypeError:
                self._humidity_percentage = None

        super().__init__(device_id)

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.Humidity"

    @property
    def humidity(self):
        return self._humidity_percentage


class InfoTrait(Trait):
    __slots__ = "_name"

    def __init__(self, device_id: str, data: dict):
        if not data:
            self._name = "Thermostat"
        else:
            self._name = data.get("customName")
            if not self._name:
                self._name = "Thermostat"

        super().__init__(device_id)

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.Info"

    @property
    def name(self):
        return self._name


class SettingsTrait(Trait):
    __slots__ = "_temperature_scale"

    def __init__(self, device_id: str, data: dict):
        if not data:
            self._temperature_scale = "CELSIUS"
        else:
            self._temperature_scale = data.get("temperatureScale")
        super().__init__(device_id)

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.Settings"

    @property
    def temperature_unit(self):
        return self._temperature_scale


class TemperatureTrait(Trait):
    __slots__ = "_ambient_temperature"

    def __init__(self, device_id: str, data: dict):
        if not data:
            self._ambient_temperature = None
        else:
            try:
                self._ambient_temperature = float(data.get("ambientTemperatureCelsius"))
            except TypeError:
                self._ambient_temperature = None
        super().__init__(device_id)

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.Temperature"

    @property
    def room_temperature(self):
        return self._ambient_temperature


class ThermostatEcoTrait(Trait):
    __slots__ = ("_available_modes", "_mode", "_heat_target", "_cool_target")

    def __init__(self, device_id: str, data: dict):
        if not data:
            self._available_modes = []
            self._mode = "OFF"
            self._heat_target = 0
            self._cool_target = 0
        else:
            self._available_modes = data.get("availableModes")
            self._mode = data.get("mode")
            try:
                self._heat_target = float(data.get("heatCelsius"))
            except TypeError:
                self._heat_target = None
            try:
                self._cool_target = float(data.get("coolCelsius"))
            except TypeError:
                self._cool_target = None
        super().__init__(device_id)

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.ThermostatEco"

    @property
    def allowed_modes(self):
        return self._available_modes

    @property
    def mode_value(self):
        return self._mode

    @property
    def eco_mode_on(self):
        return self._mode != "OFF"

    @property
    def heat_target(self):
        return self._heat_target

    @property
    def cool_target(self):
        return self._cool_target


class ThermostatHvacTrait(Trait):
    __slots__ = "_status"

    def __init__(self, device_id: str, data: dict):
        if not data:
            self._status = "OFF"
        else:
            self._status = data.get("status")
        super().__init__(device_id)

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.ThermostatHvac"

    @property
    def is_on(self):
        return self._status != "OFF"

    @property
    def status(self):
        return self._status


class ThermostatModeTrait(Trait):
    __slots__ = ("_mode", "_available_modes")

    def __init__(self, device_id: str, data: dict):
        if not data:
            self._available_modes = []
            self._mode = "OFF"
        else:
            self._available_modes = data.get("availableModes")
            self._mode = data.get("mode")
        super().__init__(device_id)

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.ThermostatMode"

    @property
    def allowed_modes(self):
        return self._available_modes

    @property
    def mode(self):
        return self._mode

    async def set_mode(self, api: Api, new_mode: str):
        if new_mode not in self.allowed_modes:
            raise ValueError(
                f"The given set mode of '{new_mode}' is not in the allowed list of modes: {self.allowed_modes}"
            )

        result = await api.post_command(
            self.device_id,
            "sdm.devices.commands.ThermostatMode.SetMode",
            {"mode": new_mode},
        )
        if result:
            self._mode = new_mode


class ThermostatTemperatureSetpointTrait(Trait):
    __slots__ = ("_heat_target", "_cool_target")

    def __init__(self, device_id: str, data: dict):
        if not data:
            self._heat_target = 0
            self._cool_target = 0
        else:
            try:
                self._heat_target = float(data.get("heatCelsius"))
            except TypeError:
                self._heat_target = None
            try:
                self._cool_target = float(data.get("coolCelsius"))
            except TypeError:
                self._cool_target = None
        super().__init__(device_id)

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.ThermostatTemperatureSetpoint"

    @property
    def heat_temperature(self):
        return self._heat_target

    @property
    def cool_temperature(self):
        return self._cool_target
