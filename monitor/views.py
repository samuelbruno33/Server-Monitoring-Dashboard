import socket
import subprocess
import platform
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Server
from django.contrib.auth import logout

# Ping function
def ping(ip):
    # Windows uses -n, Linux uses -c
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    cmd = ['ping', param, '1', ip]
    
    try:
        # Hide output
        return subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    except:
        return False

# Check if port is open
def check_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    result = s.connect_ex((ip, int(port)))
    s.close()
    return result == 0

@login_required(login_url='/admin/login/')
def dashboard(request):
    servers = Server.objects.all()
    data = []

    for s in servers:
        # Check if online
        online = ping(s.ip_address)
        
        # Check ports if listed
        p_status = []
        if s.ports_to_check:
            p_list = s.ports_to_check.split(',')
            for p in p_list:
                if p.strip().isdigit():
                    is_open = check_port(s.ip_address, p.strip())
                    p_status.append({'num': p, 'open': is_open})

        data.append({
            'name': s.name,
            'ip': s.ip_address,
            'owner': s.owner,
            'online': online,
            'ports': p_status,
        })

    return render(request, 'dashboard.html', {'servers': data})

def logout_view(request):
    logout(request)
    return redirect('/admin/login/')