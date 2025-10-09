from python_sandbox.sandbox import PythonSandbox

# Create sandbox with network access enabled
sandbox = PythonSandbox(allow_net=True)

# Simple HTTP GET request example
code = """
import pyodide.http
import json

# Make a request to a public API
response = await pyodide.http.pyfetch("https://api.github.com/zen")
text = await response.string()

print(f"Status Code: {response.status}")
print(f"Response Text: {text}")
"""

print("Making HTTP request...")

result = sandbox.execute(code)

if result.success:
    print(result.output)
else:
    print(f"Error: {result.error}")

