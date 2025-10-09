from python_sandbox.sandbox import PythonSandbox

print("=== Python Sandbox Network Security Examples ===\n")

# Use case 1: Restrict to only trusted APIs
print("1. Restrict to trusted APIs only:")
trusted_sandbox = PythonSandbox(
    allow_net=["api.github.com", "jsonplaceholder.typicode.com"]
)

safe_code = """
import pyodide.http

# This will work - whitelisted domain
response = await pyodide.http.pyfetch("https://api.github.com/zen")
print(f"✓ Allowed: {await response.string()}")

# This will fail - not whitelisted
try:
    response = await pyodide.http.pyfetch("https://evil-site.com/data")
    print("✗ This shouldn't happen!")
except Exception as e:
    print(f"✓ Blocked: evil-site.com (as expected)")
"""

result = trusted_sandbox.execute(safe_code)
print(result.output)

# Use case 2: Data processing with no network
print("\n2. Data processing without any network access:")
offline_sandbox = PythonSandbox(allow_net=False)

data_processing = """
import json

data = [1, 2, 3, 4, 5]
result = sum(x**2 for x in data)
print(f"Processing result: {result}")
print("✓ Computation completed without network access")
"""

result = offline_sandbox.execute(data_processing)
print(result.output)

# Use case 3: Single API endpoint restriction
print("\n3. Restrict to single specific API:")
github_only = PythonSandbox(allow_net=["api.github.com"])

github_code = """
import pyodide.http
import json

response = await pyodide.http.pyfetch("https://api.github.com/users/github")
data = await response.json()
print(f"✓ GitHub user: {data['login']}")
print(f"✓ Followers: {data['followers']}")
"""

result = github_only.execute(github_code)
print(result.output)

print("\n=== Summary ===")
print("✓ allow_net=True          → Allow all domains")
print("✓ allow_net=False         → Block all network access")
print("✓ allow_net=['domain']    → Whitelist specific domains")

