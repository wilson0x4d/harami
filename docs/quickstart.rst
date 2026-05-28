Quick Start
============
.. _quickstart:


Installation
------------

You can install the library from `PyPI <https://pypi.org/project/harami/>`_ using typical methods, such as ``pip``:

.. code:: bash

   python3 -m pip install harami

Usage
----------------------

Let's try a "learn by example" approach. The following code is a Widget Factory implementation. The Widget Factory raises an event on Widget Creation, it also emits the Widgets it creates through an Observable. The MyApp class creates an instance of the Widget Factory, adds an event handler, adds an observer, and finally requests the factory create a Widget.

.. code:: python

    from harami import *

    class Widget:
        color:str
        def __init__(self, color: str = None) -> None:
            self.color = color

    class WidgetEventArgs(EventArgs):
        @property
        def widget(self) -> Widget:
            return self.args[0]

    class WidgetFactory:
        def __init__(self) -> None:
            self.widget_emitter = Observable[Widget]()

        @event(WidgetEventArgs)
        def on_widget_created(self, widget: Widget) -> None:
            # this is an "Event Source", it does not require an
            # implementation, but one can be provided if it
            # makes sense for your application
            pass

        def create_widget(color: str) -> None:
            widget = Widget(color)
            self.on_widget_created(widget)
            self.widget_emitter(widget)

    class MyApp:
        def __init__(self) -> None:
            self.__widget_factory = WidgetFactory()
            self.__widget_factory.on_widget_created += self.__on_widget_created_handler
            self.__widget_factory.widget_emitter += self.__widget_observer

        def __on_widget_created_handler(sender:object, e: WidgetEventArgs) -> None:
            print(f'Widget Created: color is {e.widget.color}')

        def __widget_observer(widget: Widget) -> None:
            print(f'Widget Emitted: color is {e.widget.color}')

        def run(self) -> None:
            self.__widget_factory.create_widget('red')

    MyApp().run()

When executed the program outputs the following:

.. code:: plaintext
    
    Widget Created: color is red
    Widget Emitted: color is red
