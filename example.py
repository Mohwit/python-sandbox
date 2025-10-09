from python_sandbox.sandbox import PythonSandbox

# Example 1: Default sandbox (all network access)
# sandbox = PythonSandbox()
# result = sandbox.execute("print('Hello, World!')")
# print(f"Output: {result}")

# print()

# Example 2: Sandbox with all permissions enabled
sandbox_full = PythonSandbox(allow_net=True, allow_read=True, allow_env=True)

# Example 3: Sandbox with whitelisted domains only
sandbox_whitelist = PythonSandbox(allow_net=["api.github.com", "jsonplaceholder.typicode.com"])
code = """
import pyodide.http
response = await pyodide.http.pyfetch("https://api.github.com/zen")
print(await response.string())
"""
result = sandbox_whitelist.execute(code)
print(f"Whitelisted request: {result.output.strip()}")

# Example 4: Sandbox with no network access
sandbox_no_net = PythonSandbox(allow_net=False)
result_no_net = sandbox_no_net.execute(code)
print(f"No network: {result_no_net}")