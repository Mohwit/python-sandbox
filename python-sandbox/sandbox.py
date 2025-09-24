# simple python wrapper for core.ts sandbox
import subprocess
import json
import os
from dataclasses import dataclass
from typing import Any

@dataclass
class CodeExecutionResult:
    output: str
    error: str
    success: bool

class PythonSandbox:
    def __init__(self, allow_net: bool = True, allow_read: bool = True, allow_env: bool = False):
        self.allow_net = allow_net
        self.allow_read = allow_read
        self.allow_env = allow_env
        self.core_script = os.path.join(os.path.dirname(__file__), "core.ts")
        if not os.path.exists(self.core_script):
            raise FileNotFoundError("core.ts not found")

    def execute(self, code: str) -> CodeExecutionResult:
        try:
            # build node command with TypeScript support
            cmd = ["npx", "tsx", self.core_script, code]
            
            # prepare environment variables based on permissions
            env = os.environ.copy()
            
            # set permission flags as environment variables for potential use
            ## dummy values for now
            env["SANDBOX_ALLOW_NET"] = str(self.allow_net).lower()
            env["SANDBOX_ALLOW_READ"] = str(self.allow_read).lower()
            env["SANDBOX_ALLOW_ENV"] = str(self.allow_env).lower()
            
            # run node with tsx for TypeScript support
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                env=env
            )
            
            if process.returncode != 0:
                return CodeExecutionResult(
                    output="",
                    error=process.stderr,
                    success=False
                )
            
            # parse the JSON output from core.ts
            try:
                result_data = json.loads(process.stdout.strip())
                return CodeExecutionResult(
                    output=result_data.get("output", ""),
                    error=result_data.get("error", ""),
                    success=result_data.get("success", False)
                )
            except json.JSONDecodeError:
                return CodeExecutionResult(
                    output=process.stdout,
                    error="",
                    success=True
                )
                
        except subprocess.TimeoutExpired:
            return CodeExecutionResult(
                output="",
                error="execution timed out",
                success=False
            )
        except Exception as e:
            return CodeExecutionResult(
                output="",
                error=str(e),
                success=False
            )

# usage example
if __name__ == "__main__":
    # create sandbox 
    sandbox = PythonSandbox()
    
    # create sandbox with all permissions enabled
    sandbox_full = PythonSandbox(allow_net=True, allow_read=True, allow_env=True)
    
    # execute python code with default sandbox
    result = sandbox.execute("import os; print(os.getcwd())")
    print(f"Output: {result}")
