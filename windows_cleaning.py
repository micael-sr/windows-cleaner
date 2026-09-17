import os
import subprocess
from rich import print


def clean_temp_files():
    subprocess.run('del /q /f /s "%TEMP%\\*"', shell=True)
    subprocess.run('del /q /f /s "C:\\Windows\\Temp\\*"', shell=True)


def clear_dns_cache():
    subprocess.run('ipconfig /flushdns', shell=True)


def clear_store_cache():
    subprocess.run('wsreset.exe', shell=True)


def clean_windows_update():
    subprocess.run('net stop wuauserv', shell=True)
    subprocess.run('net stop bits', shell=True)
    subprocess.run(
        'del /q /f /s "%windir%\\SoftwareDistribution\\Download\\*"',
        shell=True
    )
    subprocess.run('net start bits', shell=True)
    subprocess.run('net start wuauserv', shell=True)


def clean_windows_components():
    subprocess.run(
        'DISM /Online /Cleanup-Image /StartComponentCleanup',
        shell=True
    )
    subprocess.run('sfc /scannow', shell=True)


def check_system():
    pass


def full_cleanup():
    clean_temp_files()
    clear_dns_cache()
    clear_store_cache()
    clean_windows_update()
    clean_windows_components()


def menu():
    while True:
        print("""
========================================
          WINDOWS CLEANER
========================================

[1] Full Cleanup
[2] Clear Caches
[3] Temporary Files
[4] Windows Update
[5] Check/Repair Windows
[6] Disk Cleanup
[0] Exit
""")

        option = input("Choose an option: ")

        if option == "1":
            full_cleanup()

        elif option == "2":
            clear_dns_cache()
            clear_store_cache()

        elif option == "3":
            clean_temp_files()

        elif option == "4":
            clean_windows_update()

        elif option == "5":
            check_system()

        elif option == "6":
            pass

        elif option == "0":
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    menu()
