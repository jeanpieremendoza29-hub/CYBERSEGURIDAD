# Módulo a desarrollar por el Grupo 1 (Fase I: Captura de Anuncios)
import socket
import re
import logging
import datetime

class BannerGrabber:
    def __init__(self, ip_address, timeout=3):
        self.ip_address = ip_address
        self.timeout = timeout
        # Expresión regular para limpiar caracteres no imprimibles (útil para limpiar el banner)
        self.clean_regex = re.compile(r'[^a-zA-Z0-9\s\.\-\/\:]')

    def grab_port(self, port):
        """
        Intenta conectarse a un puerto TCP y obtener el anuncio de servicio (banner).
        Retorna un diccionario estandarizado para facilitar la generación de reportes.
        """
        banner_data = {
            'port': port,
            'status': 'closed',
            'banner': None
        }
        
        try:
            # TODO: Inicializar el socket TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((self.ip_address, port))
                
                if result == 0:
                    banner_data['status'] = 'open'
                    
                    # TODO: Algunos servicios (como HTTP en el puerto 80) necesitan una petición 
                    # para responder. Implementar un condicional para enviar un "HEAD / HTTP/1.0"
                    if port == 80:
                        s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                        
                    # Leer respuesta y decodificar
                    raw_banner = s.recv(1024)
                    if raw_banner:
                        decoded = raw_banner.decode('utf-8', errors='ignore').strip()
                        banner_data['banner'] = self.clean_regex.sub('', decoded)
                        
        except Exception as e:
            logging.debug(f"Error escaneando {self.ip_address}:{port} - {e}")
            
        return banner_data

if __name__ == "__main__":
    # Área de pruebas independiente para el Grupo 1
    target = "127.0.0.1"
    grabber = BannerGrabber(target)
    print(f"Iniciando captura de anuncios en {target}...")
    for p in [21, 22, 80]:
        print(grabber.grab_port(p))