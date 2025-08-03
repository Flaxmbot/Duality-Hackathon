import os
import subprocess
import time
import socket

# CONFIG
BACKEND_PORT = 8000
BACKEND_DIR = os.path.join(os.getcwd(), "")  # adjust if needed
FRONTEND_DIR = os.path.join(os.getcwd(), "frontend")  # adjust if needed

def free_port(port):
    try:
        result = subprocess.check_output(f'netstat -ano | findstr :{port}', shell=True).decode()
        lines = result.strip().split("\n")
        for line in lines:
            if "LISTENING" in line or "ESTABLISHED" in line:
                pid = int(line.strip().split()[-1])
                print(f"[INFO] Killing process on port {port} (PID {pid})")
                os.system(f"taskkill /PID {pid} /F >nul 2>&1")
    except Exception as e:
        print(f"[INFO] Port {port} seems free or could not be freed: {e}")

def start_backend():
    print("[INFO] Starting FastAPI backend server...")
    free_port(BACKEND_PORT)
    backend_process = subprocess.Popen(
        ["uvicorn", "main:app", "--reload", "--port", str(BACKEND_PORT)],
        cwd=BACKEND_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    return backend_process

def start_frontend():
    print("[INFO] Starting Next.js frontend server...")
    frontend_process = subprocess.Popen(
        ["npm.cmd", "run", "dev"],
        cwd=FRONTEND_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    return frontend_process

def main():
    print("== Duality Dev Launcher ==")
    backend = start_backend()
    time.sleep(3)  # Give backend time to start
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