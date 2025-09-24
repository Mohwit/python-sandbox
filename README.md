# Python Sandbox

A secure Python code execution environment using Pyodide and Deno. This sandbox allows you to execute Python code in a WebAssembly-based isolated environment without requiring a local Python installation.

## 🚀 Features

- **Secure Execution**: Python code runs in a WebAssembly sandbox via Pyodide
- **No Local Python Required**: Uses Pyodide for Python execution
- **Configurable Permissions**: Control Deno permissions for maximum security
- **Type-Safe Results**: Uses dataclasses for structured output
- **Error Handling**: Comprehensive error capture and timeout protection
- **Cross-Platform**: Works on any system that supports Deno

## 📋 Prerequisites

### Required Software

1. **Deno Runtime** (v1.37.0 or higher)

   - Download from: https://deno.com/
   - Or install via package manager:

     ```bash
     # macOS (Homebrew)
     brew install deno

     # Windows (Scoop)
     scoop install deno

     # Linux (curl)
     curl -fsSL https://deno.land/install.sh | sh
     ```

2. **Python** (3.7 or higher) - for the wrapper
   - Download from: https://python.org/
   - Or use system package manager

### System Requirements

- **Memory**: Minimum 512MB RAM (1GB+ recommended)
- **Network**: Internet connection required for Pyodide download
- **Disk Space**: ~100MB for Pyodide cache

## 🛠️ Installation

### 1. Clone or Download

```bash
git clone <your-repository-url>
cd python-sandbox
```

Or download the files:

- `core.ts` - Deno TypeScript sandbox core
- `sandbox.py` - Python wrapper class
- `deno.json` - Deno configuration

### 2. Verify Deno Installation

```bash
deno --version
```

Expected output:

```
deno 1.37.0 (release, x86_64-apple-darwin)
v8 11.8.172.13
typescript 5.2.2
```

### 3. Test Core Sandbox

```bash
deno task run
```

Expected output:

```json
{ "output": "Hello, World!\n", "error": "", "success": true }
```

### 4. Test Python Wrapper

```bash
python sandbox.py
```

Expected output:

```
Output: CodeExecutionResult(output='/home/pyodide\n', error='', success=True)
```

## 📖 Usage

### Basic Usage

```python
from sandbox import PythonSandbox

# Create sandbox instance
sandbox = PythonSandbox()

# Execute Python code
result = sandbox.execute("print('Hello, World!')")

print(f"Output: {result.output}")
print(f"Success: {result.success}")
print(f"Error: {result.error}")
```

### Security Configuration

```python
# Maximum security (default)
sandbox_secure = PythonSandbox(
    allow_net=True,   # Required for Pyodide
    allow_read=True,  # Required for Pyodide
    allow_env=False   # Disabled for security
)

# Full permissions
sandbox_full = PythonSandbox(
    allow_net=True,
    allow_read=True,
    allow_env=True
)

# Custom permissions
sandbox_custom = PythonSandbox(
    allow_net=True,
    allow_read=False,  # Disable file system access
    allow_env=False
)
```

### Code Examples

```python
# Mathematical calculations
result = sandbox.execute("result = 2 + 3 * 4; print(f'Result: {result}')")

# Working with data structures
code = """
data = [1, 2, 3, 4, 5]
squared = [x**2 for x in data]
print(f'Squared: {squared}')
"""
result = sandbox.execute(code)

# Error handling
result = sandbox.execute("print(undefined_variable)")
if not result.success:
    print(f"Error occurred: {result.error}")
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Python App    │───▶│  sandbox.py      │───▶│    core.ts      │
│                 │    │  (Wrapper)       │    │   (Deno)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                │                        ▼
                                │                ┌─────────────────┐
                                │                │    Pyodide      │
                                │                │  (WebAssembly)  │
                                │                └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │ CodeExecutionResult│    │  Python Code    │
                       │   - output         │    │   Execution     │
                       │   - error          │    │                 │
                       │   - success        │    └─────────────────┘
                       └──────────────────┘
```

## 🔧 Configuration

### Deno Permissions

| Permission   | Default | Description                             |
| ------------ | ------- | --------------------------------------- |
| `allow_net`  | `True`  | Network access (required for Pyodide)   |
| `allow_read` | `True`  | File system read (required for Pyodide) |
| `allow_env`  | `False` | Environment variables access            |

### Timeout Settings

Default execution timeout: **30 seconds**

To modify timeout, edit `sandbox.py`:

```python
process = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    timeout=60  # Change to desired timeout in seconds
)
```

## 🛡️ Security Considerations

### Sandboxing

- Python code runs in WebAssembly (Pyodide)
- No direct access to host file system
- Network access controlled by Deno permissions
- Process isolation via subprocess

### Limitations

- No access to native Python modules
- Limited file system operations
- Network requests subject to CORS
- CPU and memory usage not directly limited

### Best Practices

1. **Use minimal permissions** for production
2. **Set appropriate timeouts** to prevent hanging
3. **Validate input** before execution
4. **Monitor resource usage** in production environments
5. **Keep Deno and Pyodide updated**

## 🐛 Troubleshooting

### Common Issues

**Error: "core.ts not found"**

```bash
# Ensure core.ts is in the same directory as sandbox.py
ls -la core.ts sandbox.py
```

**Error: "deno: command not found"**

```bash
# Install Deno or add to PATH
export PATH="$HOME/.deno/bin:$PATH"
```

**Error: "Failed to load Pyodide"**

```bash
# Check internet connection and try again
# Pyodide downloads ~30MB on first run
```

**Execution timeout**

```python
# Increase timeout in sandbox.py
timeout=60  # seconds
```

### Debug Mode

Enable verbose output:

```bash
# Test core directly
deno run --allow-net --allow-read --allow-env core.ts "print('Debug test')"

# Check Deno permissions
deno run --allow-all core.ts "import os; print(os.getcwd())"
```

## 📝 API Reference

### PythonSandbox Class

```python
class PythonSandbox:
    def __init__(self, allow_net: bool = True, allow_read: bool = True, allow_env: bool = False)
    def execute(self, code: str) -> CodeExecutionResult
```

### CodeExecutionResult Dataclass

```python
@dataclass
class CodeExecutionResult:
    output: str    # Standard output from Python execution
    error: str     # Error messages or stderr content
    success: bool  # Whether execution completed successfully
```

## 📄 License

This project is open source. Please check the license file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with:
   - Python version
   - Deno version
   - Operating system
   - Error messages
   - Code that reproduces the issue
