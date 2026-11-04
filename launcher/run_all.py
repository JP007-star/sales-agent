#!/usr/bin/env python
"""
Launch both Streamlit apps with a single command.
Sales Agent on port 8501, JP Finds Deals on port 8502.
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path


def run_app(name: str, directory: str, port: int):
    """Run a Streamlit app in a subprocess."""
    app_path = Path(directory) / "app.py"
    if not app_path.exists():
        print(f"[ERROR] {name}: app.py not found at {app_path}")
        return None

    cmd = [
        sys.executable, "-m", "streamlit", "run", str(app_path),
        "--server.port", str(port),
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ]

    print(f"[START] Starting {name} on port {port}...")
    print(f"   Command: {' '.join(cmd)}")

    # Run in the project directory
    proc = subprocess.Popen(
        cmd,
        cwd=directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding='utf-8',
        errors='replace'
    )
    return proc


def monitor_process(proc, name: str):
    """Monitor and print output from a process."""
    if proc and proc.stdout:
        for line in proc.stdout:
            print(f"[{name}] {line.rstrip()}")


def main():
    print("=" * 60)
    print("JP Sales Agent Suite - Dual App Launcher")
    print("=" * 60)

    # Get the parent directory (project root)
    base_dir = Path(__file__).parent.parent

    apps = [
        ("Sales Pipeline", base_dir / "sales-pipeline", 8501),
        ("Affiliate Studio", base_dir / "affiliate-studio", 8502),
    ]

    processes = []

    try:
        # Start both apps
        for name, directory, port in apps:
            proc = run_app(name, str(directory), port)
            if proc:
                processes.append((name, proc))
            time.sleep(2)  # Stagger startup

        if not processes:
            print("[ERROR] No apps started successfully")
            return 1

        print("\n" + "=" * 60)
        print("[SUCCESS] Both apps running!")
        print("=" * 60)
        print("Sales Agent:     http://localhost:8501")
        print("JP Finds Deals:  http://localhost:8502")
        print("=" * 60)
        print("Press Ctrl+C to stop both apps\n")

        # Monitor output from both processes
        import threading

        def monitor(name, proc):
            if proc and proc.stdout:
                for line in proc.stdout:
                    print(f"[{name}] {line.rstrip()}")

        threads = []
        for name, proc in processes:
            t = threading.Thread(target=monitor, args=(name, proc), daemon=True)
            t.start()
            threads.append(t)

        # Wait for interrupt
        while True:
            time.sleep(1)
            # Check if any process died
            for name, proc in processes:
                if proc.poll() is not None:
                    print(f"\n[WARNING] {name} stopped unexpectedly (exit code: {proc.returncode})")
                    return 1

    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Shutting down...")
    finally:
        # Terminate all processes
        for name, proc in processes:
            if proc and proc.poll() is None:
                print(f"   Stopping {name}...")
                try:
                    proc.terminate()
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()

        print("[SUCCESS] All apps stopped")

    return 0


if __name__ == "__main__":
    sys.exit(main())