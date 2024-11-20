import os
import subprocess
import psutil


def get_system_info():
    System_configuration = " System Configuration: \n"

    #  Get the system's hostname
    name = subprocess.check_output(['hostname']).decode('utf-8').strip()
    System_configuration = System_configuration + f"PC Name: {name}\n"
    
    # get cpu info
    cpu_info = subprocess.check_output("wmic cpu get name", shell=True).decode().strip().split('\n')[1].strip()
    System_configuration = System_configuration + f"CPU Info: {cpu_info}\n"
    
    #  get partion Information
    partitions = psutil.disk_partitions()
    for partition in  partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        System_configuration = System_configuration + f"Partition : {partition.mountpoint} | Total : {usage.total / (1024**3)} | Free : {usage.free / (1024**3)} | Used : {usage.used / (1024**3)}\n"
    

    
    
    
    print(System_configuration)
get_system_info()
