import socket
import platform
import subprocess
import errno
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Server, Config

ERROR_CODES = {
    0: "OK",

    # Connection refused
    111: "Connection refused",      # Linux
    10061: "Connection refused",    # Windows

    # Timeout
    110: "Timeout",                 # Linux
    10060: "Timeout",               # Windows

    # Non-blocking / no immediate response
    10035: "No response",

    # Host / Network unreachable
    113: "Host unreachable",
    101: "Network unreachable",

    # Others
    10051: "Network is unreachable",     # Windows
    10053: "Software caused connection abort",  # Windows
    10054: "Connection reset by peer",   # Windows/Linux
    10050: "Network down",               # Windows
}


# Ping a host using the system command
def ping_host(ip):
    # Windows -n, linux -c
    if platform.system().lower() == "windows":
        cmd = ['ping', '-n', '1', ip]
    else:
        cmd = ['ping', '-c', '1', ip]
    
    try:
        # Run the command with no output
        out = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if out == 0:
            return True
        else:
            return False
    except:
        return False


# Check the connection on a given port, if returns true then the service is open, otherwise is closed
""" # Old version
    def check_service(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    
    try:
        result = s.connect_ex((ip, int(port))) # TCP connectino
        s.close()
        return result
    except socket.error:
        return -1 """


def check_service(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    try:
        s.connect((ip, int(port)))
        s.close()
        return 0 
    except socket.timeout:
        return 10060
    except ConnectionRefusedError:
        return 10061
    except OSError as e:
        err = getattr(e, 'winerror', None) or getattr(e, 'errno', None)

        if err in ERROR_CODES:
            return err
        else:
            return 10035


def logout_view(request):
    logout(request)
    return redirect('/admin/login/')


@login_required(login_url='/admin/login/')
def dashboard(request):
    refresh_rate = Config.objects.first()
    if refresh_rate:
        refresh_rate = refresh_rate.refresh_seconds
    else:
        refresh_rate = 60 # Default if no config found

    servers = Server.objects.all()
    
    dashboard_data = []
    
    count_online = 0
    count_total = 0
    
    for s in servers:
        count_total = count_total + 1
        
        # Check Ping
        is_up = ping_host(s.ip_address)
        if is_up:
            count_online = count_online + 1
            
        # Check Services
        services_data = []
        my_services = s.services.all() # Get services from the db
        
        for service in my_services:
            code = check_service(s.ip_address, service.port)

            if code == 0:
                is_open = True
            else:
                is_open = False
            
            description = ERROR_CODES.get(code, "Unknown error")
            error_msg = f"{description} ({code})"

            services_data.append({
                'name': service.name,
                'port': service.port,
                'open': is_open,
                'error': error_msg
            })
            
        # Add to list
        dashboard_data.append({
            'name': s.name,
            'ip': s.ip_address,
            'owner': s.owner,
            'is_up': is_up,
            'services': services_data
        })

    context = {
        'servers': dashboard_data,
        'refresh_time': refresh_rate,
        'total': count_total,
        'online': count_online,
        'offline': count_total - count_online
    }
    
    return render(request, 'dashboard.html', context)