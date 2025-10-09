from python_sandbox.sandbox import PythonSandbox

# Create sandbox with network access enabled
sandbox = PythonSandbox(allow_net=True)

code = """
import pyodide.http
import asyncio

# Define async function for each request
async def fetch_url(url):
    response = await pyodide.http.pyfetch(url)
    data = await response.json()
    return data

# URLs to fetch in parallel
urls = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/todos/2",
    "https://jsonplaceholder.typicode.com/todos/3",
    "https://jsonplaceholder.typicode.com/todos/4",
    "https://jsonplaceholder.typicode.com/todos/5"
]

# Make all requests in parallel using asyncio.gather
print("Making 5 parallel requests...")
results = await asyncio.gather(*[fetch_url(url) for url in urls])

# Process results
print(f"\\nReceived {len(results)} responses:\\n")
for i, result in enumerate(results, 1):
    print(f"{i}. {result['title']}")
"""

print("Executing parallel HTTP requests...")

result = sandbox.execute(code)

if result.success:
    print(result.output)
else:
    print(f"Error: {result.error}")

