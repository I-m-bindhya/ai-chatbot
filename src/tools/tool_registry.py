from src.util.exception import ToolExecutionError


class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, tools):
        for tool in tools:
            self.tools[tool["name"]] = tool

    def get_tools(self):
        return list(self.tools.values())

    def get_selected_tools(
        self,
        tool_names
    ):
        return [
            self.tools[name]["schema"]
            for name in tool_names
            if name in self.tools
        ]
    
    def execute(self, tool_name, arguments):
        try:
            tool = self.tools[tool_name]
            function = tool["function"]
            return function(**arguments)
        except Exception as ex:
            raise ToolExecutionError(
                f"{tool_name}: {ex}"
            )
    
    