from python_sandbox.sandbox import PythonSandbox

# Test code that tries to access different APIs
test_code = """
import pyodide.http

urls = [
    ("GitHub", "https://api.github.com/zen"),
    ("JSONPlaceholder", "https://jsonplaceholder.typicode.com/todos/1"),
    ("HTTPBin", "https://httpbin.org/get")
]

for name, url in urls:
    try:
        response = await pyodide.http.pyfetch(url)
        print(f"✓ {name}: {response.status}")
    except Exception as e:
        print(f"✗ {name}: {str(e)[:80]}")
"""

print("=== Example 1: Allow all networks (default) ===")
sandbox1 = PythonSandbox(allow_net=True)
result1 = sandbox1.execute(test_code)
print(result1.output)

print("\n=== Example 2: Deny all networks ===")
sandbox2 = PythonSandbox(allow_net=False)
result2 = sandbox2.execute(test_code)
print(result2.output)

print("\n=== Example 3: Whitelist only specific domains ===")
sandbox3 = PythonSandbox(allow_net=["api.github.com", "jsonplaceholder.typicode.com"])
result3 = sandbox3.execute(test_code)
print(result3.output)

print("\n=== Example 4: Whitelist with actual usage ===")
sandbox4 = PythonSandbox(allow_net=["api.github.com"])
code4 = """
import pyodide.http

# This should work
response = await pyodide.http.pyfetch("https://api.github.com/zen")
print(f"GitHub Zen: {await response.string()}")
"""
result4 = sandbox4.execute(code4)
print(result4.output)

