# nest-thermostat-py

A simple Python wrapper for the Nest Thermostat API

Covers all the API endpoints required to interact with a Nest Thermostat through the google cloud API.
The available endpoints for a themostat are bound to their respective traits, ie FanTrait.set_mode() is bound to the SetMode endpoint of the Fan trait.
Each trait can be accessed simply by `Thermostat.<TraitName>`, eg Thermostat.Fan, Thermostat.Info, Thermostat.Temperature, etc.
Thermostat endppints coverage is as follows:

- Fan SetMode - `Fan.set_mode(api_object, mode, time_in_seconds)`
- ThermostatEco SetMode - `ThermostatEco.set_mode(api_object, mode)`
- ThermostatMode SetMode - `ThermostatMode.set_mode(api_object, mode)`
- ThermostatTemperatureSetpoint SetHeat - `ThermostatTemperatureSetpoint.set_heat(api_object, heat_in_celsius)`
- ThermostatTemperatureSetpoint SetCool - `ThermostatTemperatureSetpoint.set_cool(api_object, cool_in_celsius)`
- ThermostatTemperatureSetpoint SetRange - `ThermostatTemperatureSetpoint.set_range(api_object, heat_in_celsius, cool_in_celsius)`

There are also two helper API access calls:

- Get Device List - `api_object.get_devices()`
- Get Specific Device - `api_object.get_exact_device(device_id)`

## Still TODO

- If possible implement the Google Cloud pub/sub methods as it would allow Thermostat instances to be updated when they are updated externally.
