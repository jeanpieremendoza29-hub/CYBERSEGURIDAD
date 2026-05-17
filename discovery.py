# Grupo 3: Descubrimiento de Hosts (3 estudiantes)
import datetime
import ipaddress
import subprocess
from scapy.all import IP, TCP, sr1

def ping_sweep(target_range: str, timeout: int = 10) -> dict:
    """
    Estudiante 1: Implementa un ping sweep utilizando el comando ping para identificar hosts activos en una red.

    Args:
        target_range (str): El rango de red en formato CIDR
        timeout (int): Timeout en ms para cada ping (default: 10 ms).
    
    Returns:
        Dict: Resultados de la auditoría, cumpliendo con el esquema definido en docs/schema_resultados.json.
    """
    resultado = {
        "modulo": "Discovery",
        "grupo": 3,
        "estudiante": "E1",
        "target": target_range,
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "success",
        "data": {"hosts_activos": []},
        "error_message": None
    }
    #Verificar si el formato del rango es correcto
    try:
        red = ipaddress.ip_network(target_range, strict=False)
        for host in red.hosts():
            direccion = str(host)
            comando = ["ping", "-n", "1", "-w", str(timeout), direccion]
            respuesta = subprocess.run(comando, capture_output=True, text=True)
            if respuesta.returncode == 0:
                print(f"[+] Host encontrado en: {direccion}\n")
                resultado["data"]["hosts_activos"].append(direccion)
        # Si no se encontró ningún host activo, puedes dejar la lista vacía
    except Exception as e:
        resultado["status"] = "error"
        resultado["error_message"] = str(e)
    return resultado

def procesar_cidr(rango_cidr: str) -> dict:
      """
    Realiza un escaneo de descubrimiento mediante TCP SYN a un puerto común (80).

    Args:
        target_range (str): El rango de red a escanear en notación CIDR.

    Returns:
        dict: Resultados del escaneo siguiendo el esquema JSON definido.
    """
    resultado = {
        'modulo': 'Discovery',
        'grupo': 3,
        'estudiante': 'E2',
        'target': target_range,
        'timestamp': datetime.datetime.now().isoformat(),
        'status': 'success', # Corregido: se usa 'status' en lugar de 'exito'
        'data': {'hosts_activos': []}, # Corregido: se usa 'data' en lugar de 'datos'
        'error_message': None
    }

    try:
        # Se convierte el rango CIDR a una red [cite: 172, 173]
        red = ipaddress.ip_network(target_range, strict=False)
        hosts_activos = []

        # Iteramos sobre los hosts de la red [cite: 174]
        for host in red.hosts():
            # Lógica de escaneo TCP SYN con Scapy [cite: 175]
            paquete = scapy.IP(dst=str(host))/scapy.TCP(dport=80, flags="S")
            respuesta = scapy.sr1(paquete, timeout=1, verbose=0)

            if respuesta and respuesta.haslayer(scapy.TCP):
                if respuesta.getlayer(scapy.TCP).flags == 0x12: # 0x12 es SYN-ACK
                    hosts_activos.append(str(host))
                    # Enviamos RST para cerrar la conexión amablemente
                    scapy.send(scapy.IP(dst=str(host))/scapy.TCP(dport=80, flags="R"), verbose=0)

        resultado['data']['hosts_activos'] = hosts_activos

    except Exception as e:
        # Manejo de errores actualizando el status y guardando el mensaje [cite: 177, 178, 179, 180]
        resultado['status'] = 'error'
        resultado['error_message'] = str(e)

    return resultado

def ping_tcp_ack(target_range: str) -> dict:
    """
    Estudiante 3: Realiza un descubrimiento de hosts que responden con un paquete RST (TCP ACK Scan).
    Es necesario tener permisos de administrador.

    Args:
        target_range (str): El rango de red en formato CIDR (ej. '192.168.1.0/24').

    Returns:
        Dict[str, Any]: Resultados de la auditoría, cumpliendo con el esquema definido en docs/schema_resultados.json.
    """
    resultado = {
        "modulo": "Discovery",
        "grupo": 3,
        "estudiante": "E3",
        "target": target_range,
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "success",
        "data": {"hosts_activos": []},
        "error_message": None
    }
    try:
        red = ipaddress.ip_network(target_range, strict=False)
        for host in red.hosts():
            pkt = IP(dst=str(host))/TCP(dport=80, flags="A")
            resp = sr1(pkt, timeout=1, verbose=0)
            if resp and resp.haslayer(TCP) and resp.getlayer(TCP).flags == 0x4:  # RST
                print(f"[+] Host activo (RST recibido): {host}")
                resultado["data"]["hosts_activos"].append(str(host))
    except Exception as e:
        resultado["status"] = "error"
        resultado["error_message"] = str(e)
    return resultado