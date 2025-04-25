`harami` is a lightweight "Event" and "Observable" library for Python.

This README is only a high-level introduction to **harami**. For more detailed documentation, please view the official docs at [https://harami.readthedocs.io](https://harami.readthedocs.io).

## Installation

**harami** can be installed from pypi through the usual means:

```bash
pip install harami
```

## Usage

Let's try a "learn by example" approach. The following code is a Widget Factory implementation. The Widget Factory raises an event on Widget Creation, it also emits the Widgets it creates through an Observable. The MyApp class creates an instance of the Widget Factory, adds an event handler, and also adds an observer, then requests the factory create a Widget.

```python
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
```

When executed the program outputs the following:

```plaintext
Widget Created: color is red
Widget Emitted: color is red
```

## Notables..

Things not obvious given the example above:

* Events and Observables can be declared at a module scope (classes are not required.)
* The names you use for events, observables, handlers, and observers are not relevant, name things as you please.
* The scoping (public vs. private) of members and functions is not important, scope as you please.
* Event Handlers can be async, whether or not the Event Source is async.
* Event Sources can be async, whether or not event handlers are async.
* Event Handlers receive an EventArgs, which you can optionally subclass as seen in the example.
* All `*args` and `*kwargs` passed to an Event Source are forwarded via an `args` attribute of type `tuple` and a `kwargs` attribute of type `dict`, both accessible on `EventArgs` and any `EventArgs` subclass. You can use these in the raw for downstream method invocations or wrap them behind properties as seen in the example above.
* Observers can be async, even though observables do not expose an async/coro signature.
* Observables provide a value-assignment syntax, ex: `myObserver.state = 'foo'` if that is preferred, this also simplifies using an observable to back properties.
* Events offer `addHandler()` and `removeHandler()`, observables offer `attach()` and `detach()`, each as respective alternatives to the `+=` and `-=` shorthand syntax seen in the example.
* Last, but not least, Observables and be used as Event Handlers, and Event Sources can be used as Observers.

This library is meant to be lightweight and not have dependencies on other libraries, as such it has an intentionally narrow focus.

## Contact

You can reach me on [Discord](https://discordapp.com/users/307684202080501761) or [open an Issue on Github](https://github.com/wilson0x4d/harami/issues/new/choose).
