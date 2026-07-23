class ToolAdapter:

    def adapt(self, tools):
        adapted_tools = []

        for tool in tools:

            parameters = tool["parameters"]

            # Handle tools with no parameters
            if isinstance(parameters, list):
                properties = {}
                required = []
            else:
                properties = parameters
                required = list(parameters.keys())

            adapted_tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required
                    }
                }
            })

        return adapted_tools