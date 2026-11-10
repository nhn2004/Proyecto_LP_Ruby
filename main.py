import os
from datetime import datetime
import lexer  # Importamos tu motor de reglas

def probar_lexer_consola():
    print("=== PRUEBA DE ANALIZADOR LÉXICO (MODO CONSOLA) ===")
    usuario = input("Ingresa tu usuario de GitHub: ").strip()
    ruta = input("Ingresa la ruta del archivo a analizar (ej. algoritmos/prueba1.rb): ").strip()
    
    if not os.path.exists(ruta):
        print(f"Error: No se encontró el archivo '{ruta}'")
        return

    # Leer archivo Ruby
    with open(ruta, 'r', encoding='utf-8') as archivo:
        codigo = archivo.read()

    # Usar la función puente de tu lexer
    tokens_encontrados, errores_encontrados = lexer.tokenizar(codigo)

    # Preparar el texto del Log
    fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    nombre_log = f"lexico-{usuario}-{fecha_hora}.txt"
    
    log_texto = f"Archivo de log: {nombre_log}\n"
    log_texto += f"Estudiante: {usuario}\n"
    log_texto += f"Fecha de ejecución: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n"
    log_texto += f"Archivo analizado: {ruta}\n\n"
    
    log_texto += "*********** TOKENS VÁLIDOS *********** \n"
    if tokens_encontrados:
        for tok in tokens_encontrados:
            log_texto += f"[{tok.lineno}] {tok.type}: {tok.value}\n"
    else:
        log_texto += "No se encontraron tokens válidos.\n"
        
    log_texto += "\n*********** ERRORES ***********\n"
    if errores_encontrados:
        for err in errores_encontrados:
            log_texto += f"{err}\n"
    else:
        log_texto += "No se encontraron errores léxicos.\n"

    # 1. Imprimir en consola
    print("\n" + log_texto)

    # 2. Guardar físicamente en la carpeta logs/
    os.makedirs("logs", exist_ok=True)
    ruta_log = os.path.join("logs", nombre_log)
    
    with open(ruta_log, 'w', encoding='utf-8') as archivo_log:
        archivo_log.write(log_texto)
        
    print(f"\n[✓] Análisis exitoso. Log guardado en: {ruta_log}")

if __name__ == '__main__':
    probar_lexer_consola()