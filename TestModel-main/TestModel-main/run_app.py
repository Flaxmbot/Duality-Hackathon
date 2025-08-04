import os
import subprocess
import time
import socket
import platform
import psutil

# CONFIG
BACKEND_PORT = 8000
BACKEND_DIR = os.getcwd()  # adjust if needed
FRONTEND_DIR = os.path.join(os.getcwd(), "frontend")  # adjust if needed

def free_port(port):
    system = platform.system().lower()

    # Cross-platform way to find and kill processes on a port
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            conns = proc.connections()
            for conn in conns:
                if conn.status == 'LISTEN' and conn.laddr.port == port:
                    pid = proc.pid
                    print(f"[INFO] Killing process on port {port} (PID {pid})")
                    proc.kill()
        except Exception:
            continue

def start_backend():
    print("[INFO] Starting FastAPI backend server...")
    free_port(BACKEND_PORT)
    backend_process = subprocess.Popen(
        ["uvicorn", "main:app", "--reload", "--port", str(BACKEND_PORT)],
        cwd=BACKEND_DIR
    )
    return backend_process

def start_frontend():
    print("[INFO] Starting Next.js frontend server...")
    is_windows = platform.system().lower() == 'windows'
    npm_command = "npm.cmd" if is_windows else "npm"
    
    frontend_process = subprocess.Popen(
        [npm_command, "run", "dev"],
        cwd=FRONTEND_DIR
    )
    return frontend_process

def main():
    print("== Duality Dev Launcher ==")
    backend = start_backend()
    time.sleep(5)  # Give backend time to start
    frontend = start_frontend()

    print("\n[INFO] Servers running.\n")
    print(f"  ➤ Backend: http://localhost:{BACKEND_PORT}")
    print("  ➤ Frontend: http://localhost:3000")
    print("\n[INFO] Press CTRL+C to stop both servers.")

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\n[INFO] Stopping servers...")
        backend.terminate()
        frontend.terminate()

if __name__ == "__main__":
    main()
