Observables
===========

An **Observable** notifies **Observers** of state changes. An **Observer** is attached to an **Observable** to be notified that state has changed. ``harami`` implements the Observable-Observer pattern using a single class ``Observable[T]``, and **Observers** are simple ``Callable[[T],None]`` (ie. functions or methods, or objects with conforming ``__call__`` implementations.)

Initialization
--------------

.. py:currentmodule:: harami

.. py:class:: Observable()
    :canonical: harami.observables.Observable

    ``Observable`` init does not accept any parameters.

Properties
----------

.. py:attribute:: Observable.state

    The most-recent state of the Observable.

    :type: Any


Methods
-------

.. py:method:: Observable.attach(observer)

    Attach an Observer.

    :param Observer observer: A callable that accepts a single parameter (the state being observed.)


.. tip:: Attempting to attach an Observer more than once to a single Observable results in only a single attachment. Conversely, an Observer can be attached to multiples Observables.


.. py:method:: Observable.detach(observer)

    Detach an Observer.

    :param Observer observer: An observer that was previously attached to the Observable, to be detached.


.. py:method:: notify(state)

    Notifies attached Observers of a state change.

    :param T state: The state change observed.


.. rubric:: Example:

.. code:: python

    from harami import Observable

    observer = lambda state: print(f'Observing {state}')
    subject:Observable[str] = Observable()
    subject.attach(observer)
    subject.notify('foo')
    subject.detach(observer)
    subject.notify('bar')

    # Outputs: "Observing foo" (but not "Observing bar")


.. rubric:: Example (alternative syntax):

.. code:: python

    from harami import Observable

    observer = lambda state: print(f'Observing {state}')
    subject:Observable[str] = Observable()
    subject += observer
    subject('foo')
    subject.state = 'bar'
    subject -= observer
    subject.notify('baz')

    # Outputs: "Observing foo" and "Observing bar", but not "Observing baz"


