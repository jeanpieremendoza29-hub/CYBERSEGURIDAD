# Historial de Errores de la Suite de Auditoría

Este documento almacena fallos comunes y soluciones de la ejecución de la suite.

## Fallo de ejecución en OSINT (E3) contra Google (Rate Limit)

**El Problema:**
Durante la ejecución de búsquedas pasivas con Google Dorks (ej. búsqueda de archivos expuestos), el script arroja resultados vacíos y muestra la nota: "Búsqueda completada o interrumpida por rate-limit de Google". Esto sucede porque los servidores de Google detectan ráfagas de peticiones automatizadas (Scraping) y bloquean temporalmente la IP retornando un código HTTP 429 (Too Many Requests).

**La Solución:**
Para mitigar este bloqueo y evitar que el script falle, se deben implementar las siguientes técnicas:
1. **Retardos (Delays):** Usar `time.sleep(2)` o superior entre cada petición iterativa.
2. **User-Agents:** Enviar cabeceras HTTP (`headers={'User-Agent': '...'}`) válidas y, de ser posible, rotarlas para simular tráfico legítimo de navegadores reales.
3. **Manejo de Excepciones:** Capturar explícitamente el código de error 429 (Too Many Requests) para finalizar la recolección elegantemente sin quebrar la ejecución global del orquestador.