import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import display
from esphome.const import (
    CONF_ID,
    CONF_LAMBDA,
    CONF_PAGES,
    CONF_CONTRAST,
)

DEPENDENCIES = []

CONF_LATCH_PIN = 'latch_pin'
CONF_CLOCK_PIN = 'clock_pin'
CONF_DATA_PIN = 'data_pin'

frekvenspanel_ns = cg.esphome_ns.namespace("frekvenspanel")
Panel = frekvenspanel_ns.class_(
    "Panel", cg.PollingComponent, display.DisplayBuffer
)


CONFIG_SCHEMA = cv.All(
    display.FULL_DISPLAY_SCHEMA.extend(
        {
            cv.GenerateID(): cv.declare_id(Panel),
            cv.Required(CONF_LATCH_PIN): cv.int_,
            cv.Required(CONF_CLOCK_PIN): cv.int_,
            cv.Required(CONF_DATA_PIN): cv.int_,
            cv.Optional(CONF_CONTRAST, default=0x7F): cv.int_,
        }
    )
    .extend(cv.polling_component_schema("200ms")),
    cv.has_at_most_one_key(CONF_PAGES, CONF_LAMBDA),
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])

    if cv.Version.parse(ESPHOME_VERSION) < cv.Version.parse("2023.12.0"):
        await cg.register_component(var, config)
    await display.register_display(var, config)

    cg.add(var.set_pins(
        config[CONF_LATCH_PIN],
        config[CONF_CLOCK_PIN],
        config[CONF_DATA_PIN],
    ))

    if CONF_LAMBDA in config:
        lambda_ = await cg.process_lambda(
            config[CONF_LAMBDA], [(display.DisplayRef, "it")], return_type=cg.void
        )
        cg.add(var.set_writer(lambda_))
