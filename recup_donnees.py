from datetime import datetime
def get_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("-------------------------------")
print("Date et heure :", get_datetime())
print("-------------------------------")

def get_hostname():
    try:
        with open("/proc/sys/kernel/hostname") as f:
            return f.read().strip()
    except Exception as e:
        return f"Erreur : {e}"

print("-------------------------------")
print("Nom d'hôte :", get_hostname())
print("-------------------------------")

def get_kernel_version():
    try:
        with open("/proc/version") as f:
            return f.read().strip()
    except Exception as e:
        return f"Erreur : {e}"

print("-------------------------------")
print("Version du noyau :", get_kernel_version())
print("-------------------------------")

def get_kernel_version():
    try:
        with open("/proc/version") as f:
            return f.read().strip()
    except Exception as e:
        return f"Erreur : {e}"

print("-------------------------------")
print("Version du noyau :", get_kernel_version())
print("-------------------------------")

def get_uptime():
    try:
        with open("/proc/uptime") as f:
            seconds = float(f.readline().split()[0])
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}min"
    except Exception as e:
        return f"Erreur : {e}"

print("-------------------------------")
print("Temps d'activité :", get_uptime())
print("-------------------------------")
def get_cpu_temperature():
    try:
        with open("/sys/class/thermal/cooling_device0/cur_state") as f:
            temp_milli = int(f.read().strip())
            temp_celsius = temp_milli / 1000.0
            return f"{temp_celsius:.1f} °C"
    except Exception as e:
        return f"Température non disponible : {e}"

print("Température du CPU :", get_cpu_temperature())
print("--------------------------------")
