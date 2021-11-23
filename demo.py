"""Demo"""
import asyncio
import logging

from pyweatherflowudp.client import EVENT_DEVICE_DISCOVERED, WeatherFlowListener
from pyweatherflowudp.const import EVENT_RAIN_START, EVENT_RAPID_WIND, EVENT_STRIKE
from pyweatherflowudp.device import (
    EVENT_LOAD_COMPLETE,
    EVENT_OBSERVATION,
    EVENT_STATUS_UPDATE,
    AirSensorType,
    SkySensorType,
    WeatherFlowDevice,
)
from pyweatherflowudp.event import Event

logging.basicConfig(level=logging.INFO)


async def main():
    """Main entry point."""

    def device_discovered(device: WeatherFlowDevice):
        """Handle a discovered device."""
        logging.info("Found device: %s", device)

        def device_event(event: Event):
            """Handle an event."""
            logging.info("%s from %s", event, device)

        event_lambda = lambda event: device_event(event)
        device.on(EVENT_LOAD_COMPLETE, event_lambda)
        device.on(EVENT_OBSERVATION, event_lambda)
        device.on(EVENT_STATUS_UPDATE, event_lambda)
        if isinstance(device, AirSensorType):
            device.on(EVENT_STRIKE, event_lambda)
        if isinstance(device, SkySensorType):
            device.on(EVENT_RAIN_START, event_lambda)
            device.on(EVENT_RAPID_WIND, event_lambda)

    async with WeatherFlowListener() as client:
        client.on(EVENT_DEVICE_DISCOVERED, lambda device: device_discovered(device))
        await asyncio.sleep(60)
        await client.stop_listening()


if __name__ == "__main__":
    asyncio.run(main())
