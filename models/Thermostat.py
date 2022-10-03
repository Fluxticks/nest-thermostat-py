class Thermostat:

    def __init__(self, data):
        self._raw_data = data

    @property
    def is_connected(self):
        return self._connectivity

    @property
    def fan_timer_mode(self):
        return self._fan.get("timerMode")

    @property
    def fan_timer_timeout(self):
        return self._fan.get("timerTimeout")

    @property
    def humidity(self):
        return self._humidity

    @property
    def device_name(self):
        return self._info

    @property
    def temperature_unit(self):
        return self._settings

    @property
    def current_temperature(self):
        return self._temperature

    @property
    def eco_mode(self):
        return self._thermostat_eco.get("mode")

    @property
    def eco_heat_target(self):
        return self._thermostat_eco.get("heatCelcius")

    @property
    def eco_cool_target(self):
        return self._thermostat_eco.get("coolCelcius")

    @property
    def hvac_mode(self):
        return self._thermostat_hvac

    @property
    def thermostat_mode(self):
        return self._thermostat_mode

    @property
    def thermostat_heat_target(self):
        return self._thermostat_temperature_setpoint.get("heatCelcius")

    @property
    def thermostat_cool_target(self):
        return self._thermostat_temperature_setpoint.get("coolCelcius")