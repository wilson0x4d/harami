# SPDX-FileCopyrightText: © 2025 Shaun Wilson
# SPDX-License-Identifier: MIT

import asyncio
from harami import Observable
from punit import fact


class ObservableTests:

    @fact
    def basicVerification(self) -> None:
        o: Observable[int] = Observable()


        class X:
            s1_last: int | None = None
            s2_last: int | None = None

            def s1(self, v: int):
                self.s1_last = v

            def s2(self, v: int):
                self.s2_last = v
        x: X = X()
        o.attach(x.s1)
        o.attach(x.s2)
        #
        assert o() is None
        assert x.s1_last is None
        assert x.s2_last is None
        o(1)
        assert 1 == o()
        assert 1 == x.s1_last
        assert 1 == x.s2_last
        o(2)
        assert o() == 2
        assert x.s1_last == 2
        assert x.s2_last == 2
        o.detach(x.s1)
        o(None)
        assert o() is None
        assert 2 == x.s1_last
        assert x.s2_last is None

    @fact
    def canAssignStateViaPropertyOrCall(self) -> None:
        o: Observable[int] = Observable[int]()
        #
        assert o.state is None
        assert o() is None
        o(1)
        assert 1 == o.state
        assert 1 == o()
        o.state = 2
        assert 2 == o.state
        assert 2 == o()
        o.state = None
        assert o() is None
        assert o.state is None
        assert type(o) is Observable

    @fact
    def attachingSameObserverMultipleTimesOnlyAttachesOnce(self) -> None:
        o: Observable[int] = Observable()
        #

        class X:
            call_count: int

            def __init__(self):
                self.call_count = 0

            def s1(self, v: int):
                self.call_count += 1
        x: X = X()
        o.attach(x.s1)
        o.attach(x.s1)
        o.attach(x.s1)
        #
        assert o() is None
        assert 0 == x.call_count
        o(1)
        assert 1 == o()
        assert 1 == x.call_count
        o.detach(x.s1)
        o(2)
        assert 2 == o()
        assert 1 == x.call_count

    @fact
    async def supportAsyncObservers(self) -> None:
        o: Observable[int] = Observable()
        #

        class X:
            call_count: int

            def __init__(self):
                self.call_count = 0

            async def s1(self, v: int):
                self.call_count += 1
        x: X = X()
        o.attach(x.s1)
        o.attach(x.s1)
        o.attach(x.s1)
        #
        assert o() is None
        assert 0 == x.call_count
        o(1)
        await asyncio.sleep(0.1)  # arbitrary wait to yield to async observers
        assert 1 == o()
        assert 1 == x.call_count
        o.detach(x.s1)
        o(2)
        assert 2 == o()
        assert 1 == x.call_count

    @fact
    async def observablesCanConsumeEvents(self) -> None:
        """
        Confirms that Observable[T] can be used as a handler for `@event` methods.

        ---
        There is special logic inside the Event implementation which allows EventHandlers
        to forward EventArgs over to Observable[T] implementations, creating a convenient
        mechanism for event consumers.
        """
        from .EventTests import FakeEventProvider, FakeEventArgs, FakeEventTypeEnum
        #

        class X:
            sync_call_count: int
            sync_event_args: FakeEventArgs
            async_call_count: int
            async_event_args: FakeEventArgs

            def __init__(self):
                self.sync_call_count = 0
                self.sync_event_args = None
                self.async_call_count = 0
                self.async_event_args = None

            def s1(self, args: FakeEventArgs) -> None:
                self.sync_call_count += 1
                self.sync_event_args = args

            async def s2(self, args: FakeEventArgs) -> None:
                self.async_call_count += 1
                self.async_event_args = args
        #
        x: X = X()
        o1: Observable[FakeEventArgs] = Observable[FakeEventArgs]()
        o1.attach(x.s1)
        o2: Observable[FakeEventArgs] = Observable[FakeEventArgs]()
        o2.attach(x.s2)
        #
        source = FakeEventProvider()
        source.sync_event.add_handler(o1)
        source.async_event.add_handler(o2)
        #
        source.sync_event(FakeEventTypeEnum.ONE, 'Hello, World!'.encode())
        await source.async_event(FakeEventTypeEnum.TWO, 'Hello, World!'.encode())
        await asyncio.sleep(0.1)
        #
        assert x.sync_call_count == 1
        assert x.sync_event_args is not None
        assert x.sync_event_args.type == FakeEventTypeEnum.ONE
        assert x.sync_event_args.data.decode() == 'Hello, World!'
        assert x.async_call_count == 1
        assert x.async_event_args is not None
        assert x.async_event_args.type == FakeEventTypeEnum.TWO
        assert x.async_event_args.data.decode() == 'Hello, World!'
