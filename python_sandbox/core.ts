// Import Pyodide module from node_modules
import { loadPyodide } from "../node_modules/pyodide/pyodide.mjs";

// Extend ImportMeta to include Deno's main property
declare global {
  interface ImportMeta {
    main: boolean;
  }
  
  const Deno: {
    args: string[];
  };
}

// Interface defining the structure of Python execution results
export interface PythonResult {
   output: string;   
   error: string;   
   success: boolean;
 }

 // pythin sandbox class
export class PythonSandbox {
   private pyodide: any = null;        // Pyodide instance
   private initialized = false;        // Initialization state flag

   // initialize the pyodide environment (lazy loading)
   // only loads pyodide once, subsequent calls are no-ops
   async init(): Promise<void> {
     // skip initialization if already done
     if (this.initialized) return;
     
     try {
       // load pyodide webassembly environment with proper indexURL
       // This tells Pyodide where to find its WASM and other files
       this.pyodide = await loadPyodide({
         indexURL: "./node_modules/pyodide/"
       });
       this.initialized = true;
     } catch (error) {
       throw new Error(`Failed to load Pyodide: ${error}`);
     }
   }

   // execute python code in the sandbox environment
   // captures stdout, stderr and handles errors gracefully
   // 
   // @param pythonCode - The Python code string to execute
   // @returns Promise<PythonResult> - Execution results with output, errors, and success status
   async execute(pythonCode: string): Promise<PythonResult> {
     try {
       // ensure pyodide is initialized before execution
       await this.init();
       
       // variables to store captured output
       let stdout = "";
       let stderr = "";
       
       // set up output capture by redirecting Python's sys.stdout and sys.stderr
       // This allows us to capture print() statements and error output
       this.setupOutputCapture();
       
       // execute the user's Python code asynchronously
       const result = await this.pyodide.runPythonAsync(pythonCode);
       
       // retrieve captured output from our StringIO buffers
       stdout = this.pyodide.runPython("__stdout_buffer.getvalue()");
       stderr = this.pyodide.runPython("__stderr_buffer.getvalue()");
       
       // clean up: restore original stdout/stderr
       this.restoreOriginalStreams();
       
       // return successful execution result
       return {
         output: stdout || '',
         error: stderr || '',
         success: true,
       };
       
     } catch (error) {
       // handle execution errors gracefully
       return this.handleExecutionError(error);
     }
   }

   /**
    * set up Python stdout/stderr capture using StringIO buffers
    * This is a helper method to keep the main execute method clean
    */
   private setupOutputCapture(): void {
     this.pyodide.runPython(`
       import sys
       from io import StringIO
       
       # Create string buffers to capture output
       __stdout_buffer = StringIO()
       __stderr_buffer = StringIO()
       
       # Save original streams for later restoration
       __original_stdout = sys.stdout
       __original_stderr = sys.stderr
       
       # Redirect Python output to our buffers
       sys.stdout = __stdout_buffer
       sys.stderr = __stderr_buffer
     `);
   }

   // restore Python's original stdout/stderr streams
   private restoreOriginalStreams(): void {
     this.pyodide.runPython(`
       sys.stdout = __original_stdout
       sys.stderr = __original_stderr
     `);
   }

   // handle execution errors and attempt to capture any stderr output
   // @param error - The caught error object
   // @returns PythonResult with error information
   private handleExecutionError(error: any): PythonResult {
     let stderr = "";
     
     try {
       // Try to capture any stderr that might have been written before the error
       stderr = this.pyodide.runPython("__stderr_buffer.getvalue()");
       this.restoreOriginalStreams();
     } catch {
       // If we can't capture stderr, use the JavaScript error message
       stderr = (error as Error).message;
     }
     
     return {
       output: '',
       error: stderr,
       success: false,
     };
   }
 }

// demo function showing how to use the PythonSandbox
async function main(): Promise<void> {
  // create a new Python sandbox instance
  const sandbox = new PythonSandbox();
  
  // check if we have command line argument (from Python wrapper)
  let pythonCode = "print('Hello, World!')"; // default code
  
  // get Python code from command line argument
  if (Deno.args.length > 0) {
    pythonCode = Deno.args[0];
  }
  
  // execute Python code and get the result
  const result = await sandbox.execute(pythonCode);
  
  // display the execution result as JSON for Python wrapper
  console.log(JSON.stringify(result));
}

// run the demo if this file is executed directly
if (import.meta.main) {
  main();
}