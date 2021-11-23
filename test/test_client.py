"""Test client listener behavior."""
import asyncio
import json
from typing import Any

from pyweatherflowudp.aioudp import RemoteEndpoint
from pyweatherflowudp.client import WeatherFlowListener


async def test_listen_and_stop(listener: WeatherFlowListener) -> None:
    """Test listen and stop."""
    async with listener:
        assert listener.is_listening
        await asyncio.sleep(0.1)

    assert not listener.is_listening


async def test_repetitive_listen_and_stop(listener: WeatherFlowListener) -> None:
    """Test repetitive listen and stop."""
    assert not listener.is_listening

    repeat = 2

    for _ in range(repeat):
        await listener.start_listening()
        assert listener.is_listening
    for _ in range(repeat):
        await listener.stop_listening()
        assert not listener.is_listening


async def test_process_message(
    listener: WeatherFlowListener,
    remote_endpoint: RemoteEndpoint,
    device_status: dict[str, Any],
) -> None:
    """Test processing a received message."""
    await listener.start_listening()
    await asyncio.sleep(0.1)
    remote_endpoint.send(bytes(json.dumps(device_status), "UTF-8"))
    await asyncio.sleep(0.1)
    await listener.stop_listening()
