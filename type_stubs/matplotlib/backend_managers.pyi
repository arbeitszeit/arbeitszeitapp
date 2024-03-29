from _typeshed import Incomplete
from matplotlib import backend_tools as backend_tools, cbook as cbook, widgets as widgets

class ToolEvent:
    name: Incomplete
    sender: Incomplete
    tool: Incomplete
    data: Incomplete
    def __init__(self, name, sender, tool, data: Incomplete | None = ...) -> None: ...

class ToolTriggerEvent(ToolEvent):
    canvasevent: Incomplete
    def __init__(self, name, sender, tool, canvasevent: Incomplete | None = ..., data: Incomplete | None = ...) -> None: ...

class ToolManagerMessageEvent:
    name: Incomplete
    sender: Incomplete
    message: Incomplete
    def __init__(self, name, sender, message) -> None: ...

class ToolManager:
    keypresslock: Incomplete
    messagelock: Incomplete
    def __init__(self, figure: Incomplete | None = ...) -> None: ...
    @property
    def canvas(self): ...
    @property
    def figure(self): ...
    def set_figure(self, figure, update_tools: bool = ...) -> None: ...
    def toolmanager_connect(self, s, func): ...
    def toolmanager_disconnect(self, cid): ...
    def message_event(self, message, sender: Incomplete | None = ...) -> None: ...
    @property
    def active_toggle(self): ...
    def get_tool_keymap(self, name): ...
    def update_keymap(self, name, key) -> None: ...
    def remove_tool(self, name) -> None: ...
    def add_tool(self, name, tool, *args, **kwargs): ...
    def trigger_tool(self, name, sender: Incomplete | None = ..., canvasevent: Incomplete | None = ..., data: Incomplete | None = ...) -> None: ...
    @property
    def tools(self): ...
    def get_tool(self, name, warn: bool = ...): ...
