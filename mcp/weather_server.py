from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current weather for a city"""
    # This is a mock implementation
    return f"The weather in {city} is sunny and 25°C"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
