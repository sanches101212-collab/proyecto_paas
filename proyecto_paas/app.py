# app.py (versión 2): Práctica 3. Estado de salud y registros en formato JSON
import json
import logging
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8000"))
NOMBRE = os.environ.get("APP_NOMBRE", "Mi app en la nube")
ENTORNO = os.environ.get("ENTORNO", "desarrollo")
INICIO = time.time()

# Los registros salen por la salida estándar; la plataforma los recolecta
logging.basicConfig(level=logging.INFO, format="%(message)s")

def log(evento, **datos):
    registro = {"ts": round(time.time(), 3), "evento": evento, **datos}
    logging.info(json.dumps(registro, ensure_ascii=False))

class Handler(BaseHTTPRequestHandler):
    def responder(self, codigo, cuerpo, tipo="application/json"):
        datos = cuerpo.encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", f"{tipo}; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_GET(self):
         t0 = time.perf_counter()
         if self.path == "/":
             self.responder(200, f"<h1>{NOMBRE}</h1><p>Entorno: {ENTORNO}</p>", "text/html")
         elif self.path == "/health":
             estado = {"estado": "ok", "uptime_s": round(time.time() - INICIO, 1)}
             self.responder(200, json.dumps(estado))
         else:
             self.responder(404, json.dumps({"error": "no encontrado"}))
         log("peticion", ruta=self.path, ms=round((time.perf_counter() - t0) * 1000, 2))
    def log_message(self, *args):
        pass # silenciamos el log por defecto; usamos el nuestro



if __name__ == "__main__":
    log("inicio", puerto=PORT, entorno=ENTORNO)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()