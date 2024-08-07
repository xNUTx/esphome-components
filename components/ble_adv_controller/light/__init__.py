import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import light, output
from esphome.cpp_helpers import setup_entity
from esphome.const import (
    CONF_CONSTANT_BRIGHTNESS,
    CONF_COLD_WHITE_COLOR_TEMPERATURE,
    CONF_WARM_WHITE_COLOR_TEMPERATURE,
    CONF_MIN_BRIGHTNESS,
    CONF_OUTPUT_ID,
    CONF_DEFAULT_TRANSITION_LENGTH,
)

from .. import (
    bleadvcontroller_ns,
    ENTITY_BASE_CONFIG_SCHEMA,
    entity_base_code_gen,
    BleAdvEntity,
)

from ..const import (
    CONF_BLE_ADV_SECONDARY,
    CONF_BRIGHTNESS_AFTER_COLOR_CHANGE,
)

BleAdvLight = bleadvcontroller_ns.class_('BleAdvLight', light.LightOutput, BleAdvEntity)
BleAdvSecLight = bleadvcontroller_ns.class_('BleAdvSecLight', light.LightOutput, BleAdvEntity)

CONFIG_SCHEMA = cv.All(
    cv.Any(
        light.RGB_LIGHT_SCHEMA.extend(
            {
                cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(BleAdvLight),
                cv.Optional(CONF_COLD_WHITE_COLOR_TEMPERATURE, default="167 mireds"): cv.color_temperature,
                cv.Optional(CONF_WARM_WHITE_COLOR_TEMPERATURE, default="333 mireds"): cv.color_temperature,
                cv.Optional(CONF_CONSTANT_BRIGHTNESS, default=False): cv.boolean,
                cv.Optional(CONF_MIN_BRIGHTNESS, default=0.21): cv.percentage,
                # override default value of default_transition_length to 0s as mostly not supported by those lights
                cv.Optional(CONF_DEFAULT_TRANSITION_LENGTH, default="0s"): cv.positive_time_period_milliseconds,
                cv.Optional(CONF_BRIGHTNESS_AFTER_COLOR_CHANGE, default=False): cv.boolean,
            }
        ).extend(ENTITY_BASE_CONFIG_SCHEMA),
        light.RGB_LIGHT_SCHEMA.extend(
            {
                cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(BleAdvSecLight),
                cv.Required(CONF_BLE_ADV_SECONDARY): cv.one_of(True),
            }
        ).extend(ENTITY_BASE_CONFIG_SCHEMA),
    ),    
    cv.has_none_or_all_keys(
        [CONF_COLD_WHITE_COLOR_TEMPERATURE, CONF_WARM_WHITE_COLOR_TEMPERATURE]
    ),
    light.validate_color_temperature_channels,
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_OUTPUT_ID])
    await entity_base_code_gen(var, config)
    await light.register_light(var, config)
    if not CONF_BLE_ADV_SECONDARY in config:
        cg.add(var.set_cold_white_temperature(config[CONF_COLD_WHITE_COLOR_TEMPERATURE]))
        cg.add(var.set_warm_white_temperature(config[CONF_WARM_WHITE_COLOR_TEMPERATURE]))
        cg.add(var.set_constant_brightness(config[CONF_CONSTANT_BRIGHTNESS]))
        cg.add(var.set_min_brightness(config[CONF_MIN_BRIGHTNESS]))
        cg.add(var.set_brightness_after_color_change(config[CONF_BRIGHTNESS_AFTER_COLOR_CHANGE]))
