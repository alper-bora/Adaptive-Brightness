import os
import shutil
import subprocess
import sys
import time

def get_startup_folder():
    return os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

def kill_existing_process():
    print("Checking for existing running process...")
    # Force kills the existing executable if it is currently running
    subprocess.run(["taskkill", "/F", "/IM", "adaptive_brightness.exe"], 
                   stdout=subprocess.DEVNULL, 
                   stderr=subprocess.DEVNULL)
    # Give the OS a moment to fully release file locks
    time.sleep(1)

def main():
    print("Adaptive Brightness Deployer")
    print("----------------------------")
    ans = input("Do you want to build and deploy the up-to-date script to your startup folder? (y/n): ")
    
    if ans.lower().strip() not in ['y', 'yes']:
        print("Deployment cancelled.")
        return

    # We must stop the currently running app before we can build/overwrite its file,
    # because sometimes pyinstaller or the dist folder might have locks, 
    # but strictly speaking, it's safest to kill it at the very beginning.
    kill_existing_process()

    print("\nBuilding executable with PyInstaller (this may take a minute)...")
    
    # Run pyinstaller with --noconsole (no command prompt on launch) and --onefile (single .exe file)
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--noconsole",
            "--onefile",
            "--clean",
            "adaptive_brightness.pyw"
        ])
    except subprocess.CalledProcessError:
        print("\nError: PyInstaller build failed.")
        print("Make sure you have it installed by running: pip install pyinstaller")
        return

    exe_path = os.path.join(os.getcwd(), "dist", "adaptive_brightness.exe")
    
    if not os.path.exists(exe_path):
        print(f"\nError: The built executable was not found at {exe_path}")
        return

    startup_folder = get_startup_folder()
    dest_path = os.path.join(startup_folder, "adaptive_brightness.exe")
    
    print(f"\nCopying new executable to Startup folder...")
    try:
        shutil.copy2(exe_path, dest_path)
        print("Copy successful!")
    except Exception as e:
        print(f"Error copying file: {e}")
        return
        
    print("Starting the new version...")
    try:
        os.startfile(dest_path)
        print("All done! Adaptive Brightness is now updated and running in the background.")
    except Exception as e:
        print(f"Error starting the executable: {e}")

if __name__ == "__main__":
    main()
