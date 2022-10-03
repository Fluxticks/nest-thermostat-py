from models.Trait import (
    ConnectivityTrait,
    FanTrait,
    HumidityTrait,
    InfoTrait,
    SettingsTrait,
    TemperatureTrait,
    ThermostatEcoTrait,
    ThermostatHvacTrait,
    ThermostatModeTrait,
    ThermostatTemperatureSetpointTrait,
)


THERMOSTAT_TYPE = "sdm.devices.types.THERMOSTAT"


class Thermostat:
    __slots__ = (
        "_device_id",
        "_connectivity",
        "_fan",
        "_humidity",
        "_info",
        "_settings",
        "_temperature",
        "_thermostat_eco",
        "_thermostat_hvac",
        "_thermostat_mode",
        "_thermostat_temperature",
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
        self._connectivity = ConnectivityTrait(traits.get(ConnectivityTrait.domain()))
        self._fan = FanTrait(traits.get(FanTrait.domain()))
        self._humidity = HumidityTrait(traits.get(HumidityTrait.domain()))
        self._info = InfoTrait(traits.get(InfoTrait.domain()))
        self._settings = SettingsTrait(traits.get(SettingsTrait.domain()))
        self._temperature = TemperatureTrait(traits.get(TemperatureTrait.domain()))
        self._thermostat_eco = ThermostatEcoTrait(
            traits.get(ThermostatEcoTrait.domain())
        )
        self._thermostat_hvac = ThermostatHvacTrait(
            traits.get(ThermostatHvacTrait.domain())
        )
        self._thermostat_mode = ThermostatModeTrait(
            traits.get(ThermostatModeTrait.domain())
        )
        self._thermostat_temperature = ThermostatTemperatureSetpointTrait(
            traits.get(ThermostatTemperatureSetpointTrait.domain())
        )

    @property
    def device_id(self):
        return self._device_id

    @property
    def is_connected(self):
        return self._connectivity.is_connected

    @property
    def fan_timer_mode(self):
        return self._fan.is_on

    @property
    def fan_timer_timeout(self):
        return self._fan.stop_time

    @property
    def humidity(self):
        return self._humidity.humidity

    @property
    def device_name(self):
        return self._info.name

    @property
    def temperature_unit(self):
        return self._settings.temperature_unit

    @property
    def room_temperature(self):
        return self._temperature.room_temperature

    @property
    def eco_mode(self):
        return self._thermostat_eco.eco_mode_on

    @property
    def eco_heat_target(self):
        return self._thermostat_eco.heat_target

    @property
    def eco_cool_target(self):
        return self._thermostat_eco.cool_target

    @property
    def hvac_mode(self):
        return self._thermostat_hvac.is_on

    @property
    def thermostat_mode(self):
        return self._thermostat_mode.mode

    @property
    def thermostat_heat_target(self):
        return self._thermostat_temperature.heat_temperature

    @property
    def thermostat_cool_target(self):
        return self._thermostat_temperature.cool_temperature
