from abc import abstractclassmethod


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
