# simple python wrapper for core.ts sandbox
import subprocess
import json
import os
from dataclasses import dataclass
from typing import Union, List

@dataclass
class CodeExecutionResult:
    output: str
    error: str
    success: bool

class PythonSandbox:
    def __init__(self, allow_net: Union[bool, List[str]] = True, allow_read: bool = True, allow_env: bool = False):
        """
        Initialize Python sandbox with configurable permissions.
        
        Args:
            allow_net: Network access control. Can be:
                - True: Allow all network access
                - False: Deny all network access
                - List[str]: Allow only specific domains (e.g., ["api.github.com", "jsonplaceholder.typicode.com"])
            allow_read: Allow file system read access
            allow_env: Allow environment variable access
        """
        self.allow_net = allow_net
        self.allow_read = allow_read
        self.allow_env = allow_env
        self.core_script = os.path.join(os.path.dirname(__file__), "core.ts")
        if not os.path.exists(self.core_script):
            raise FileNotFoundError("core.ts not found")

    def execute(self, code: str) -> CodeExecutionResult:
        try:
            # build deno command with configurable permissions
            cmd = ["deno", "run"]
            
            # add permissions based on instance configuration
            if self.allow_net is True:
                cmd.append("--allow-net")
            elif isinstance(self.allow_net, list) and len(self.allow_net) > 0:
                # allow only specific domains
                domains = ",".join(self.allow_net)
                cmd.append(f"--allow-net={domains}")
            # if allow_net is False or empty list, don't add the flag
            
            if self.allow_read:
                cmd.append("--allow-read")
            if self.allow_env:
                cmd.append("--allow-env")
            
            # add script and code argument
            cmd.extend([self.core_script, code])
            
            # run deno with the configured permissions
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
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
    result = sandbox.execute("print('Hello, World!')")
    print(f"Output: {result}")
