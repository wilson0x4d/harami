Events
======

An **Event** is a change in system state. ``harami`` implements Events as a combination of an ``@event`` decorator applied to an **Event Source**. An **Event Source** is a function or method that the generator of an event will use to raise an event. For example, a network analyzer might raise an event to signal a change in network availability. An **Event Handler** receives the args passed to an **Event Source**, and is typically implemented as a function or method that receives ``sender`` (the object that raised the event) and ``EventArgs`` (the args used to raise the event.)

Decorators
----------

.. py:currentmodule:: harami

.. py:decorator:: event
    :canonical: harami.events.event

    Decorates a function or method as an **Event Source**.

.. rubric:: Example (functions):

.. code:: python

    from harami import event

    @event
    def onStateChanged(state:Any):
        pass
    onStateChanged += lambda s,e: print(f'New State: {e.args}')
    onStateChanged('Hello, World!')
    # outputs to console
    # New State: ['Hello, World!']

.. rubric:: Example (methods):

.. code:: python

    from harami import event

    class Foo:
        @event
        def onStateChanged(self, state:Any):
            pass

    class Bar:
        def __init__(self, foo:Foo) -> None:
            self.__foo = foo
            self.__foo.onStateChanged += self.__myEventHandler
        def __myEventHandler(self:object, e:EventArgs) -> None:
            print(f'New State: {e:args})

    foo = Foo()
    bar = Bar(foo)
    foo.onStateChanged('Hello, World!')
    # outputs to console
    # New State: ['Hello, World!']
