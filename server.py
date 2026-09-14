#!/usr/bin/env python3
"""
Servidor local para el Radar de Inversión 2026.
- Sirve dashboard.html (con pestañas de análisis + mercado en vivo).
- Expone /api/quotes?symbols=A,B,C  -> proxy a Yahoo Finance (chart v8, sin API key).

Uso:
    python3 server.py [puerto]     # default 8765
    luego abre http://127.0.0.1:8765

Solo usa librería estándar de Python 3.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=ytd&interval=1d"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}


def fetch_symbol(symbol):
    """Devuelve un dict con los datos de un símbolo, o None si falla."""
    url = YAHOO.format(symbol=urllib.parse.quote(symbol))
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        res = (data.get("chart") or {}).get("result")
        if not res:
            return None
        meta = res[0].get("meta", {})
        closes = (res[0].get("indicators", {}).get("quote", [{}])[0].get("close") or [])
        closes = [c for c in closes if c is not None]

        price = meta.get("regularMarketPrice")
        hi52 = meta.get("fiftyTwoWeekHigh")
        lo52 = meta.get("fiftyTwoWeekLow")
        ytd = None
        if len(closes) >= 2 and closes[0]:
            ytd = round((closes[-1] / closes[0] - 1) * 100, 2)
        dist_high = None
        pos_in_range = None
        if price and hi52 and lo52 and hi52 > lo52:
            dist_high = round((price / hi52 - 1) * 100, 2)
            pos_in_range = round((price - lo52) / (hi52 - lo52) * 100, 1)
            pos_in_range = max(0.0, min(100.0, pos_in_range))

        return {
            "symbol": symbol,
            "name": meta.get("longName") or meta.get("shortName") or symbol,
            "price": price,
            "currency": meta.get("currency"),
            "dayChangePct": meta.get("regularMarketChangePercent"),
            "dayHigh": meta.get("regularMarketDayHigh"),
            "dayLow": meta.get("regularMarketDayLow"),
            "high52w": hi52,
            "low52w": lo52,
            "ytdPct": ytd,
            "distFromHigh52w": dist_high,
            "posIn52wRange": pos_in_range,
            "volume": meta.get("regularMarketVolume"),
            "exchange": meta.get("fullExchangeName") or meta.get("exchangeName"),
            "asOf": meta.get("regularMarketTime"),
        }
    except Exception as e:  # noqa: BLE001
        return {"symbol": symbol, "error": str(e)}


def get_quotes(symbols):
    """Consulta varios símbolos en paralelo."""
    results = {}
    with ThreadPoolExecutor(max_workers=12) as pool:
        futs = {pool.submit(fetch_symbol, s): s for s in symbols}
        for fut in as_completed(futs):
            sym = futs[fut]
            try:
                results[sym] = fut.result()
            except Exception as e:  # noqa: BLE001
                results[sym] = {"symbol": sym, "error": str(e)}
    # mantener orden de petición
    return [results[s] for s in symbols]


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False)
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", f"{ctype}; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/quotes":
            qs = urllib.parse.parse_qs(parsed.query)
            raw = qs.get("symbols", [""])[0]
            symbols = [s for s in raw.split(",") if s]
            if not symbols:
                self._send(400, {"error": "falta parámetro symbols"})
                return
            self._send(200, {"asOf": int(time.time()), "quotes": get_quotes(symbols)})
            return

        if path == "/api/health":
            self._send(200, {"ok": True, "time": int(time.time())})
            return

        # servir archivos estáticos del directorio
        if path in ("/", "/dashboard.html", "/index.html"):
            target = os.path.join(BASE_DIR, "dashboard.html")
        else:
            target = os.path.join(BASE_DIR, urllib.parse.unquote(path).lstrip("/"))
        if not os.path.isfile(target):
            self._send(404, {"error": "not found"}, "application/json")
            return
        ext = os.path.splitext(target)[1].lower()
        ctype = {"html": "text/html", "css": "text/css", "js": "application/javascript",
                 "json": "application/json"}.get(ext.lstrip("."), "application/octet-stream")
        with open(target, "rb") as f:
            self._send(200, f.read(), ctype)

    def log_message(self, fmt, *args):
        pass  # silencio


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Radar 2026 corriendo en http://127.0.0.1:{port}  (Ctrl+C para detener)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nDetenido.")


if __name__ == "__main__":
    main()
