# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

import asyncio
from enum import IntEnum
from harami import *
from punit import *


class FakeEventTypeEnum(IntEnum):
    """A fake enum used in the fake `EventArgs` subclass."""
    ONE = 1,
    TWO = 2


class FakeEventArgs(EventArgs):
    """A fake `EventArgs` subclass used for testing."""

    @property
    def type(self) -> FakeEventTypeEnum:
        return self.args[0]

    @property
    def data(self) -> bytes:
        return self.args[1]
    

class FakeEventProvider:
    """A fake concrete class that exposes events."""

    def __init__(self):
        self.sync_was_executed = False
        self.async_was_executed = False

    @event(FakeEventArgs)
    def sync_event(self, the_type:FakeEventTypeEnum, the_data:bytes) -> str:
        """A synchronous Event Source."""
        self.sync_was_executed = True
        return the_data.decode()

    @event(FakeEventArgs)
    async def async_event(self, the_type:FakeEventTypeEnum, the_data:bytes) -> str:
        """An asynchronous Event Source."""
        self.async_was_executed = True
        return the_data.decode()
    
sync_event_type_received:FakeEventTypeEnum = None
sync_event_data_received:bytes = None
sync_handler1_was_executed = False
sync_handler2_was_executed = False

@fact
async def sync_events_signal_handlers() -> None:
    # arrange
    def handler1(sender:object, e:FakeEventArgs):
        global sync_handler1_was_executed
        global sync_event_type_received
        assert sender is not None
        assert e is not None
        sync_handler1_was_executed = True
        sync_event_type_received = e.type
    # NOTE: even though Event Source is non-async, async handlers are permitted (requires an active event loop in the call context.)
    async def handler2(sender:object, e:FakeEventArgs):
        global sync_handler2_was_executed
        global sync_event_data_received
        assert sender is not None
        assert e is not None
        sync_handler2_was_executed = True
        sync_event_data_received = e.data
    target = FakeEventProvider()
    target.sync_event.addHandler(handler1)
    target.sync_event.addHandler(handler2)
    expectedData = "Hello, World!".encode()
    # act
    result = target.sync_event(FakeEventTypeEnum.ONE, expectedData)
    # NOTE: calling `sleep` gives async event handlers an opportunity to execute
    while len(asyncio.all_tasks()) > 1:
        await asyncio.sleep(0)
    # assert
    assert result == "Hello, World!"
    assert sync_handler1_was_executed
    assert sync_handler2_was_executed
    assert sync_event_type_received == FakeEventTypeEnum.ONE
    assert sync_event_data_received.decode() == expectedData.decode()
    assert target.sync_was_executed

async_event_type_received:FakeEventTypeEnum = None
async_event_data_received:bytes = None
async_handler1_was_executed = False
async_handler2_was_executed = False

@fact
async def async_events_signal_handlers() -> None:
    # arrange
    async def handler1(sender:object, e:FakeEventArgs):
        global async_handler1_was_executed
        global async_event_type_received
        assert sender is not None
        assert e is not None
        async_handler1_was_executed = True
        async_event_type_received = e.type
    # NOTE: even though Event Source is async, it is permitted to use sync handlers
    def handler2(sender:object, e:FakeEventArgs):
        global async_handler2_was_executed
        global async_event_data_received
        assert sender is not None
        assert e is not None
        async_handler2_was_executed = True
        async_event_data_received = e.data
    target = FakeEventProvider()
    target.async_event.addHandler(handler1)
    target.async_event.addHandler(handler2)
    expectedData = "Hello, World!".encode()
    # act
    result = await target.async_event(FakeEventTypeEnum.TWO, expectedData)
    # NOTE: calling `sleep` gives async event handlers an opportunity to execute
    while len(asyncio.all_tasks()) > 1:
        await asyncio.sleep(0)
    # assert
    assert result == "Hello, World!"
    assert async_handler1_was_executed
    assert async_handler2_was_executed
    assert async_event_type_received == FakeEventTypeEnum.TWO
    assert async_event_data_received.decode() == expectedData.decode()
    assert target.async_was_executed


class FakeEventConsumer:
    """A fake concrete class that handles events exposed by another class."""

    def __init__(self):
        self.target = FakeEventProvider()
        self.handler1_was_executed = False
        self.sender1 = None
        self.e1 = None
        self.handler2_was_executed = False
        self.sender2 = None
        self.e2 = None

    def handler1(self, sender:object, e:FakeEventArgs) -> None:
        self.handler1_was_executed = True
        self.sender1 = sender
        self.e1 = e

    async def handler2(self, sender:object, e:FakeEventArgs) -> None:
        self.handler2_was_executed = True
        self.sender2 = sender
        self.e2 = e

    @fact
    def class_can_event_sync(self) -> None:
        self.target.sync_event.addHandler(self.handler1)
        result = self.target.sync_event(FakeEventTypeEnum.ONE, 'Hello, World!'.encode())
        assert result == 'Hello, World!'
        assert self.handler1_was_executed
        assert self.e1 is not None
        assert self.e1.type == FakeEventTypeEnum.ONE
        assert self.e1.data.decode() == 'Hello, World!'
        # verify that `sender` is the class the event was defined on, and not the class calling the Event Source.
        assert id(self.sender1) == id(self.target)

    @fact
    async def class_can_event_async(self) -> None:
        self.target.async_event.addHandler(self.handler2)
        result = await self.target.async_event(FakeEventTypeEnum.TWO, 'Hello, World!'.encode())
        # NOTE: calling `sleep` gives async event handlers an opportunity to execute
        while len(asyncio.all_tasks()) > 1:
            await asyncio.sleep(0)
        assert result == 'Hello, World!'
        assert self.handler2_was_executed
        assert self.e2 is not None
        assert self.e2.type == FakeEventTypeEnum.TWO
        assert self.e2.data.decode() == 'Hello, World!'
        # verify that `sender` is the class the event was defined on, and not the class calling the Event Source.
        assert id(self.sender2) == id(self.target)
