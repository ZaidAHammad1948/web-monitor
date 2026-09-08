from flask import Flask, render_template, jsonify
import psutil
import time
from datetime import datetime
import socket

app = Flask(__name__)

def get_system_info():
    """Collect system performance metrics"""
    
    # CPU information
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    
    # Memory information
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # Disk information
    disk = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()
    
    # Network information
    net_io = psutil.net_io_counters()
    net_interfaces = psutil.net_if_addrs()
    
    # System uptime
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    current_time = datetime.now()
    uptime = str(current_time - boot_time).split('.')[0]
    
    # Process count
    process_count = len(psutil.pids())
    
    return {
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'hostname': socket.gethostname(),
        'cpu': {
            'percent': cpu_percent,
            'count': cpu_count,
            'freq_current': round(cpu_freq.current / 1000, 2) if cpu_freq else 0,
            'freq_max': round(cpu_freq.max / 1000, 2) if cpu_freq and cpu_freq.max else 0
        },
        'memory': {
            'total': round(memory.total / (1024**3), 2),
            'available': round(memory.available / (1024**3), 2),
            'used': round(memory.used / (1024**3), 2),
            'percent': memory.percent,
            'swap_total': round(swap.total / (1024**3), 2),
            'swap_used': round(swap.used / (1024**3), 2),
            'swap_percent': swap.percent
        },
        'disk': {
            'total': round(disk.total / (1024**3), 2),
            'used': round(disk.used / (1024**3), 2),
            'free': round(disk.free / (1024**3), 2),
            'percent': disk.percent,
            'read_bytes': round(disk_io.read_bytes / (1024**3), 2) if disk_io else 0,
            'write_bytes': round(disk_io.write_bytes / (1024**3), 2) if disk_io else 0
        },
        'network': {
            'bytes_sent': round(net_io.bytes_sent / (1024**3), 2),
            'bytes_recv': round(net_io.bytes_recv / (1024**3), 2),
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'interfaces': list(net_interfaces.keys())
        },
        'process_count': process_count,
        'uptime': uptime
    }

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/metrics')
def api_metrics():
    """API endpoint for system metrics"""
    return jsonify(get_system_info())

@app.route('/api/metrics/history')
def api_metrics_history():
    """Get historical metrics (last 60 seconds)"""
    # This is a simple example - in production you'd use a database
    history = []
    for i in range(1, 11):
        data = get_system_info()
        history.append({
            'timestamp': data['timestamp'],
            'cpu': data['cpu']['percent'],
            'memory': data['memory']['percent'],
            'disk': data['disk']['percent']
        })
        time.sleep(1)
    return jsonify(history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
