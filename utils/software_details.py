import subprocess
import json
import os
import datetime
import shutil
import platform
try:
    import psutil
except ImportError:
    psutil = None
    print("Warning: psutil library not found. Some system hardware details (RAM, CPU) will be unavailable.")
    print("Install it with: pip install psutil")

def get_appx_packages():
    """Get System apps using powerShell"""
    result = subprocess.run([
        "powershell", "-Command","Get-AppxPackage -AllUsers | Select Name, InstallLocation | ConvertTo-Json"
    ], capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except Exception:
        return []
    
def get_win32_apps():
    powershell_script = r"""
    $keys = @(
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"
    )

    $apps = foreach ($key in $keys) {
        Get-ItemProperty $key -ErrorAction SilentlyContinue | 
        Where-Object { $_.DisplayName } | 
        Select-Object DisplayName, InstallLocation
    }
    $uniqueApps = $apps | Sort-Object DisplayName -Unique 
    $uniqueApps | ConvertTo-Json

   # $apps | ConvertTo-Json
    """

    result = subprocess.run(
        ["powershell", "-Command", powershell_script],
        capture_output=True,
        text=True
    )
    if result.returncode !=0:
        print(f"PowerShell script for get_win32_apps returned an error. Stderr: {result.stderr}")
        return[]
    
    app_list=[]
    try:
        if result.stdout and result.stdout.strip():
            parsed_output = json.loads(result.stdout)
            if parsed_output is None:
                app_list=[]
            elif isinstance(parsed_output,dict):
                app_list=[parsed_output]
            elif isinstance(parsed_output,list):
                app_list=parsed_output
            else:
                print(f"Warning: Unexpected data type from PowerShell JSON in get_win32_apps: {type(parsed_output)}. Output: {result.stdout[:200]}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from get_win32_apps: {e}. PowerShell stdout: '{result.stdout[:200]}...'")
    except Exception as e:
        print(f"An unexpected error occurred in get_win32_apps: {e}" )
    return app_list
    
def get_folder_size(path):
    """Recursively calculate folder size in bytes"""
    total_size =0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
            except Exception:
                pass
    return total_size

def get_last_updated_date(path):
    """Get the last modified timestamp of the install folder"""
    try:
        timestamp = os.path.getmtime(path)
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    except Exception:
        return "Unknown"

def scan_apps_and_storage():
    """Scanning and classifying apps with their storage details"""
    system_apps = get_appx_packages()
    downloaded_apps = get_win32_apps()
    #updatable_apps = get_apps_with_updates()
    
    system_apps = system_apps if system_apps is not None else []
    downloaded_apps = downloaded_apps if downloaded_apps is not None else []
    
    system_total = 0
    downloaded_total =0
    system_list =[]
    downloaded_list =[]
    
    # system app
    for app in system_apps:
        path = app.get("InstallLocation")
        name = app.get("Name")
        if path and os.path.exists(path):
            size = get_folder_size(path)
            last_updated = get_last_updated_date(path)
            system_total += size
            system_list.append({"App": name, "Size(MB)": f"{size/1e6: .2f}", "Last Updated":last_updated})
            
    # downloaded apps
    for app in downloaded_apps:
        path = app.get("InstallLocation")
        name = app.get("DisplayName")
        if name and path and os.path.exists(path):
            size = get_folder_size(path)
            downloaded_total +=size
            last_updated=get_last_updated_date(path)
            #update_status = "✅" if name and name.lower() in updatable_apps else "❌"
            downloaded_list.append({"App": name, "Size(MB)": f"{size/1e6: .2f}","Last Updated":last_updated})
        else:
            downloaded_list.append({"App":name, "Size(MB)":"N/A","Last Updated":"N/A"})
            
    return system_list, downloaded_list, system_total, downloaded_total
    
def get_hardware_details():
    details={}
    
    details['os_version'] = f"{platform.system()}{platform.release()}(Version:{platform.version()})"
    details['os_architecture'] = platform.machine()  
    try:
        usage_c = shutil.disk_usage("C:\\")
        details['disk_c_total_gb'] = usage_c.total/(1024**3)
        details['disk_c_used_gb']=usage_c.used/(1024**3)
        details['disk_c_free_gb'] = usage_c.free(1024**3)
    except Exception as e:
        print(f"Could not get disk usage for C:: {e}")
        details['disk_c_total_gb'] = 'N/A'
        details['disk_c_used_gb'] = 'N/A'
        details['disk_c_free_gb'] = 'N/A'
    all_disks_info=[]
    total_system_storage_bytes=0
    processed_devices=set()
    if psutil: # psutil provides a more convenient way to list partitions
        try:
            partitions = psutil.disk_partitions(all=False)
            for p in partitions:
                if 'cdrom' in p.opts or p.fstype=='' or 'loop' in p.device.lower() or not p.mountpoint or not os.path.exists(p.mountpoint): 
                    # Check if mountpoint is accessible
                    continue
                try:
                    usage = shutil.disk_usage(p.mountpoint)
                    current_disk_total_gb: usage.total / (1024**3)
                    current_disk_used_gb: usage.used / (1024**3)
                    current_disk_free_gb: usage.free / (1024**3)
                    all_disks_info.append({
                        "mountpoint": p.mountpoint,
                        "device":p.device,
                        "fstype": p.fstype,
                        "total_gb":current_disk_total_gb,
                        "used_gb":current_disk_used_gb,
                        "free_gb":current_disk_free_gb,
                    })
                    if p.device not in processed_devices:
                        total_system_storage_bytes +=usage.total
                        processed_devices.add(p.device)
                    
                    if p.mountpoint.upper() == 'C:\\':
                        details['disk_c_total_gb'] = current_disk_total_gb
                        details['disk_c_used_gb'] = current_disk_used_gb
                        details['disk_c_free_gb'] = current_disk_free_gb
                        
                    
                except OSError as e: # Skip drives that cause errors (e.g. optical drives with no media)
                        pass
                except Exception as e_inner:
                    pass
        except Exception as e:
            print(f"Could not get all disk partitions info: {e}")
    elif 'disk_c_total_gb' in details and details['disk_c_total_gb'] is not None:
        try:
            usage_c_for_total = shutil.disk_usage("C:\\")
        except:
            pass
    details['all_disks'] = all_disks_info
    details['total_system_storage_gb'] = total_system_storage_bytes/(1024**3) if total_system_storage_bytes>0 else None
    
    if 'disk_c_total_gb' not in details or details['disk_c_total_gb'] is None:
        c_drive_info_from_all_disks = next((d for d in all_disks_info if  d['mountpoint'].upper() == 'C:\\'),None)
        if c_drive_info_from_all_disks:
            details['disk_c_total_gb'] = c_drive_info_from_all_disks('total_gb')
            details['disk_c_used_gb'] = c_drive_info_from_all_disks('used_gb')
            details['disk_c_free_gb'] = c_drive_info_from_all_disks('free_gb')
        else:
            if 'disk_c_total_gb' not in details:
                details['disk_c_total_gb'] = None
            if 'disk_c_used_gb' not in details: details['disk_c_used_gb'] = None
            if 'disk_c_free_gb' not in details: details['disk_c_free_gb'] = None


    # RAM Information (using psutil)
    if psutil:
        try:
            svmem = psutil.virtual_memory()
            details['ram_total_gb'] = svmem.total / (1024**3)
            details['ram_available_gb'] = svmem.available / (1024**3)
            details['ram_used_gb'] = svmem.used / (1024**3)
            details['ram_percent_used'] = svmem.percent
        except Exception as e:
            print(f"Could not get RAM info using psutil: {e}")
            details['ram_total_gb'] = 'N/A'
            details['ram_available_gb'] = 'N/A'
    else:
        details['ram_total_gb'] = 'N/A (psutil not found)'
        details['ram_available_gb'] = 'N/A (psutil not found)'

    # CPU Information (using psutil for more detail)
    details['cpu_model'] = platform.processor() # Basic CPU info
    if psutil:
        try:
            details['cpu_physical_cores'] = psutil.cpu_count(logical=False)
            details['cpu_logical_cores'] = psutil.cpu_count(logical=True)
            details['cpu_current_freq_mhz'] = psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A'
            details['cpu_max_freq_mhz'] = psutil.cpu_freq().max if psutil.cpu_freq() else 'N/A'
            details['cpu_usage_percent'] = psutil.cpu_percent(interval=0.1) # Small interval for quick check
        except Exception as e:
            print(f"Could not get detailed CPU info using psutil: {e}")
            # Keep basic platform.processor() if detailed fails

    return details
