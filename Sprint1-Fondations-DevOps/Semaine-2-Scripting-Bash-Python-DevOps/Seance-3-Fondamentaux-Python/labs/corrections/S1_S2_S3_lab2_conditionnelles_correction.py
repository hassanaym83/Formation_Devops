print("LAB 2 - Structures conditionnelles CORRECTION")
print("=" * 50)

cpu = 89.7
memory = 92.1
disk = 75.0
status = "running"

cpu_critical = 85
memory_critical = 90

print("CPU:", cpu, "% - Memory:", memory, "% - Disk:", disk, "%")

# CONDITIONS SIMPLES
if cpu >= cpu_critical:
    cpu_status = "CRITICAL"
elif cpu >= 70:
    cpu_status = "WARNING"
else:
    cpu_status = "OK"

if memory >= memory_critical:
    memory_status = "CRITICAL"
elif memory >= 80:
    memory_status = "WARNING"
else:
    memory_status = "OK"

print("CPU Status:", cpu_status)
print("Memory Status:", memory_status)

# OPERATEURS LOGIQUES
system_critical = cpu >= cpu_critical and memory >= memory_critical
has_warning = cpu >= 70 or memory >= 80 or disk >= 75

print("Systeme critique (AND):", system_critical)
print("Alerte active (OR):", has_warning)

# CONDITIONS IMBRIQUEES
if status == "running":
    if system_critical:
        alert_level = "URGENCE"
    elif has_warning:
        alert_level = "SURVEILLANCE"
    else:
        alert_level = "OK"
else:
    alert_level = "HORS_SERVICE"

print("Niveau alerte:", alert_level)

# CAS SPECIAUX
if cpu is not None and memory is not None:
    print("Metriques disponibles")

if cpu > 100:
    print("Valeur CPU aberrante")
else:
    print("Valeur CPU normale")

print("LAB 2 termine avec succes!")
