# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

import asyncio
from harami import *
from punit import *


class ObservableTests:

    @fact
    def basicVerification(self) -> None:
        o:Observable[int] = Observable()
        #
        class X:
            s1_last:int = None
            s2_last:int = None
            def s1(self, v:int):
                self.s1_last = v
            def s2(self, v:int):
                self.s2_last = v
        x:X = X()
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
        o:Observable[int] = Observable[int]()
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
        o:Observable[int] = Observable()
        #
        class X:
            callCount:int
            def __init__(self):
                self.callCount = 0
            def s1(self, v:int):
                self.callCount += 1
        x:X = X()
        o.attach(x.s1)
        o.attach(x.s1)
        o.attach(x.s1)
        #
        assert o() is None
        assert 0 == x.callCount
        o(1)
        assert 1 == o()
        assert 1 == x.callCount
        o.detach(x.s1)
        o(2)
        assert 2 == o()
        assert 1 == x.callCount

    @fact
    async def supportAsyncObservers(self) -> None:
        o:Observable[int] = Observable()
        #
        class X:
            callCount:int
            def __init__(self):
                self.callCount = 0
            async def s1(self, v:int):
                self.callCount += 1
        x:X = X()
        o.attach(x.s1)
        o.attach(x.s1)
        o.attach(x.s1)
        #
        assert o() is None
        assert 0 == x.callCount
        o(1)
        await asyncio.sleep(0.1) # arbitrary wait to yield to async observers
        assert 1 == o()
        assert 1 == x.callCount
        o.detach(x.s1)
        o(2)
        assert 2 == o()
        assert 1 == x.callCount

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
            syncCallCount:int
            syncEventArgs:FakeEventArgs
            asyncCallCount:int
            asyncEventArgs:FakeEventArgs
            def __init__(self):
                self.syncCallCount = 0
                self.syncEventArgs = None
                self.asyncCallCount = 0
                self.asyncEventArgs = None
            def s1(self, args:FakeEventArgs) -> None:
                self.syncCallCount += 1
                self.syncEventArgs = args
            async def s2(self, args:FakeEventArgs) -> None:
                self.asyncCallCount += 1
                self.asyncEventArgs = args
        #
        x:X = X()
        o1:Observable[FakeEventArgs] = Observable[FakeEventArgs]()
        o1.attach(x.s1)
        o2:Observable[FakeEventArgs] = Observable[FakeEventArgs]()
        o2.attach(x.s2)
        #
        source = FakeEventProvider()
        source.sync_event.addHandler(o1)
        source.async_event.addHandler(o2)
        #
        source.sync_event(FakeEventTypeEnum.ONE, 'Hello, World!'.encode())
        await source.async_event(FakeEventTypeEnum.TWO, 'Hello, World!'.encode())
        await asyncio.sleep(0.1)
        #
        assert x.syncCallCount == 1
        assert x.syncEventArgs is not None
        assert x.syncEventArgs.type == FakeEventTypeEnum.ONE
        assert x.syncEventArgs.data.decode() == 'Hello, World!'
        assert x.asyncCallCount == 1
        assert x.asyncEventArgs is not None
        assert x.asyncEventArgs.type == FakeEventTypeEnum.TWO
        assert x.asyncEventArgs.data.decode() == 'Hello, World!'
