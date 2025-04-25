Quick Start
============
.. _quickstart:

.. contents::

Installation
------------

You can install the library from `PyPI <https://pypi.org/project/harami/>`_ using typical methods, such as ``pip``:

.. code:: bash

   python3 -m pip install harami

Usage
----------------------

Let's try a "learn by example" approach. The following code is a Widget Factory implementation. The Widget Factory raises an event on Widget Creation, it also emits the Widgets it creates through an Observable. The MyApp class creates an instance of the Widget Factory, adds an event handler, and also adds an observer, then requests the factory create a Widget.

.. code:: python

    from harami import *

    class Widget:
        color:str
        def __init__(self, color:str = None) -> None:
            self.color = color

    class WidgetEventArgs(EventArgs):
        @property
        def widget(self) -> Widget:
            return self.args[0]

    class WidgetFactory:
        def __init__(self) -> None:
            self.widgetEmitter = Observable[Widget]()

        @event
        def onWidgetCreated(self, widget:Widget) -> None:
            # this is an "Event Source", it does not require an
            # implementation, but one can be provided if it
            # makes sense for your application
            pass

        def createWidget(color:str) -> None:
            widget = Widget(color)
            self.onWidgetCreated(widget)
            self.widgetEmitter(widget)

    class MyApp:
        def __init__(self) -> None:
            self.__widgetFactory = WidgetFactory()
            self.__widgetFactory.onWidgetCreated += self.__onWidgetCreatedHandler
            self.__widgetFactory.widgetEmitter += self.__widgetObserver

        def __onWidgetCreatedHandler(sender:object, e:WidgetEventArgs) -> None:
            print(f'Widget Created: color is {e.widget.color}')

        def __widgetObserver(widget:Widget) -> None:
            print(f'Widget Emitted: color is {e.widget.color}')

        def run(self) -> None:
            self.__eventExample.createWidget('red')

    MyApp().run()

When executed the program outputs the following:

.. code:: plaintext
    
    Widget Created: color is red
    Widget Emitted: color is red
