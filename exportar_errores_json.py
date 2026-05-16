import json
import os

JSON_PATH = "/home/cero/MEGA/VS_CODE_WORKSPACE/CYBERSEGURIDAD/historial_auditoria.json"
MD_PATH = "/home/cero/MEGA/VS_CODE_WORKSPACE/CYBERSEGURIDAD/docs/auditoria.md"

def exportar_errores():
    if not os.path.exists(JSON_PATH):
        print(f"[!] Archivo JSON no encontrado: {JSON_PATH}")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        try:
            historial = json.load(f)
        except json.JSONDecodeError:
            print("[!] Error al leer el archivo JSON. Puede estar corrupto o vacío.")
            return

    # Filtramos solo los registros que fallaron o tienen un mensaje de error
    errores = [req for req in historial if req.get("error_message") or req.get("status") == "error"]

    if not errores:
        print("[*] ¡Todo en orden! No se encontraron fallos o errores en el historial para exportar.")
        return

    # Generamos el contenido Markdown estructurado para que knowledge_db.py lo entienda
    md_content = "# Historial de Errores de la Suite de Auditoría\n\nEste documento es auto-generado a partir de los fallos detectados en `historial_auditoria.json`.\n"

    for error in errores:
        modulo = error.get("modulo", "Módulo Desconocido")
        estudiante = error.get("estudiante", "Desconocido")
        target = error.get("target", "Desconocido")
        error_msg = error.get("error_message", "Fallo detectado sin mensaje específico.")
        data = error.get("data", {})

        # El título usando '##' para que funcione la separación en nuestro vector DB
        md_content += f"\n## Fallo de ejecución en {modulo} ({estudiante}) contra {target}\n\n"
        md_content += "**El Problema:**\n"
        md_content += f"El orquestador capturó el siguiente error:\n```text\n{error_msg}\n```\n\n"
        
        if data:
            md_content += "**Contexto y Variables (Data):**\n"
            md_content += f"```json\n{json.dumps(data, indent=4)}\n```\n\n"
            
        md_content += "**La Solución (Pendiente):**\n*(Agrega la solución aquí cuando el grupo lo resuelva para guardarlo en memoria)*\n"

    os.makedirs(os.path.dirname(MD_PATH), exist_ok=True)
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✅ Se han exportado {len(errores)} registro(s) de error a '{MD_PATH}'.")
    print("💡 Actualiza la base de datos de ChromaDB corriendo: python knowledge_db.py -c auditoria -u")

if __name__ == "__main__":
    exportar_errores()