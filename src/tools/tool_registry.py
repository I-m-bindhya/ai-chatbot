class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, tools):
        for tool in tools:
            self.tools[tool["name"]] = tool

    def get_tools(self):
        return list(self.tools.values())
    
    def execute(self, tool_name, arguments):
        tool = self.tools[tool_name]
        function = tool["function"]
        return function(**arguments)
    
    