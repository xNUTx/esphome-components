import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import fan

from esphome.const import (
    CONF_OUTPUT_ID,
)

from .. import (
    bleadvcontroller_ns,
    ENTITY_BASE_CONFIG_SCHEMA,
    entity_base_code_gen,
    BleAdvEntity,
)

from ..const import (
    CONF_BLE_ADV_SPEED_COUNT,
    CONF_BLE_ADV_DIRECTION_SUPPORTED,
)

BleAdvFan = bleadvcontroller_ns.class_('BleAdvFan', fan.Fan, BleAdvEntity)

CONFIG_SCHEMA = cv.All(
    fan.FAN_SCHEMA.extend(
        {
            cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(BleAdvFan),
            cv.Optional(CONF_BLE_ADV_SPEED_COUNT, default=6): cv.one_of(0,3,6),
            cv.Optional(CONF_BLE_ADV_DIRECTION_SUPPORTED, default=True): cv.boolean,
        }
    ).extend(ENTITY_BASE_CONFIG_SCHEMA),
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_OUTPUT_ID])
    await entity_base_code_gen(var, config)
    await fan.register_fan(var, config)
    cg.add(var.set_speed_count(config[CONF_BLE_ADV_SPEED_COUNT]))
    cg.add(var.set_direction_supported(config[CONF_BLE_ADV_DIRECTION_SUPPORTED]))
