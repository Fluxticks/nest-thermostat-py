from abc import abstractclassmethod

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
    __slots__ = ("_domain", "name")

    def __init__(self, domain: str):
        self._domain = domain
        self.name = self._domain.split(".")[-1]

    @abstractclassmethod
    def domain(cls):
        pass


class ConnectivityTrait(Trait):
    __slots__ = "_status"

    def __init__(self, data: dict):
        if not data:
            self._status = "OFFLINE"
        else:
            self._status = data.get("status")
        super().__init__(self.domain())

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

    def __init__(self, data: dict):
        if not data:
            self._timer_mode = None
            self._timer_timeout = None
        else:
            self._timer_mode = data.get("timerMode")
            self._timer_timeout = data.get("timerTimeout")
        super().__init__(self.domain())

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
    def stop_time(self):
        # TODO: Convert to datetime value
        return self._timer_timeout


class HumidityTrait(Trait):
    __slots__ = "_humidity_percentage"

    def __init__(self, data: dict):
        if not data:
            self._humidity_percentage = 0
        else:
            self._humidity_percentage = float(data.get("ambientHumidityPercent"))

        super().__init__(self.domain())

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.Humidity"

    @property
    def humidity(self):
        return self._humidity_percentage


class InfoTrait(Trait):
    __slots__ = "_name"

    def __init__(self, data: dict):
        if not data:
            self._name = "Thermostat"
        else:
            self._name = data.get("customName")

        super().__init__(self.domain())

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.Info"

    @property
    def name(self):
        return self._name


class SettingsTrait(Trait):
    __slots__ = "_temperature_scale"

    def __init__(self, data: dict):
        if not data:
            self._temperature_scale = "Celcius"
        else:
            self._temperature_scale = data.get("temperatureScale")
        super().__init__(self.domain())

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.Settings"

    @property
    def temperature_unit(self):
        return self._temperature_scale


class TemperatureTrait(Trait):
    __slots__ = "_ambient_temperature"

    def __init__(self, data: dict):
        if not data:
            self._ambient_temperature = 0
        else:
            self._ambient_temperature = float(data.get("ambientTemperatureCelsius"))
        super().__init__(self.domain())

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.Temperature"

    @property
    def room_temperature(self):
        return self._ambient_temperature


class ThermostatEcoTrait(Trait):
    __slots__ = ("_available_modes", "_mode", "_heat_target", "_cool_target")

    def __init__(self, data: dict):
        if not data:
            self._available_modes = []
            self._mode = "OFF"
            self._heat_target = 0
            self._cool_target = 0
        else:
            self._available_modes = data.get("availableModes")
            self._mode = data.get("mode")
            self._heat_target = float(data.get("heatCelsius"))
            self._cool_target = float(data.get("coolCelsius"))
        super().__init__(self.domain())

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

    def __init__(self, data: dict):
        if not data:
            self._status = "OFF"
        else:
            self._status = data.get("status")
        super().__init__(self.domain())

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

    def __init__(self, data: dict):
        if not data:
            self._available_modes = []
            self._mode = "OFF"
        else:
            self._available_modes = data.get("availableModes")
            self._mode = data.get("mode")
        super().__init__(self.domain())

    @classmethod
    def domain(cls):
        return "sdm.devices.traits.ThermostatMode"

    @property
    def allowed_modes(self):
        return self._available_modes

    @property
    def mode(self):
        return self._mode


class ThermostatTemperatureSetpointTrait(Trait):
    __slots__ = ("_heat_target", "_cool_target")

    def __init__(self, data: dict):
        if not data:
            self._heat_target = 0
            self._cool_target = 0
        else:
            self._heat_target = float(data.get("heatCelsius"))
            self._cool_target = float(data.get("coolCelsius"))
        super().__init__(self.domain())

    @classmethod
    def domain(cls):
        return "ThermostatTemperatureSetpoint"

    @property
    def heat_temperature(self):
        return self._heat_target

    @property
    def cool_temperature(self):
        return self._cool_target
