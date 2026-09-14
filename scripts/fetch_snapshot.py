#!/usr/bin/env python3
"""
Snapshot semanal de mercado.

Consulta Yahoo Finance (chart API v8, sin key) para los 26 instrumentos del radar,
anexa una fila por instrumento a datos/historial_semanal.csv (formato largo, para
seguir la evolución en el tiempo) y escribe datos/snapshot_latest.json con la foto
actual. Imprime un resumen compacto a stdout.

Uso:
    python3 scripts/fetch_snapshot.py
"""
import csv
import datetime
import json
import os
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "datos")
HISTORY_CSV = os.path.join(DATA_DIR, "historial_semanal.csv")
SNAPSHOT_JSON = os.path.join(DATA_DIR, "snapshot_latest.json")

YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=ytd&interval=1d"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

# (símbolo, nombre) — debe coincidir con INSTRUMENTS de dashboard.html
SYMBOLS = [
    ("SNDK", "SanDisk"),
    ("DELL", "Dell Technologies"),
    ("MU", "Micron"),
    ("INTC", "Intel"),
    ("MRVL", "Marvell"),
    ("AMD", "AMD"),
    ("WDC", "Western Digital"),
    ("ARM", "Arm Holdings"),
    ("STX", "Seagate"),
    ("CORT", "Corcept Therapeutics"),
    ("SOXX", "iShares Semiconductor"),
    ("SMH", "VanEck Semiconductor"),
    ("PSI", "Invesco Semiconductors"),
    ("AIS", "AI Supercycle ETF"),
    ("XLE", "Energy Select SPDR"),
    ("VDE", "Vanguard Energy"),
    ("USO", "United States Oil Fund"),
    ("EWY", "iShares MSCI Corea"),
    ("EWT", "iShares MSCI Taiwán"),
    ("DBC", "Invesco DB Commodity"),
    ("XBI", "SPDR Biotech"),
    ("DECO", "Galaxy Digital Assets"),
    ("CHILE.SN", "Banco de Chile"),
    ("LTM.SN", "Latam Airlines"),
    ("BSANTANDER.SN", "Santander Chile"),
    ("^IPSA", "IPSA (índice)"),
]


def fetch(symbol):
    url = YAHOO.format(symbol=urllib.parse.quote(symbol))
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        res = (data.get("chart") or {}).get("result")
        if not res:
            return {"symbol": symbol, "error": "sin resultado"}
        meta = res[0].get("meta", {})
        closes = (res[0].get("indicators", {}).get("quote", [{}])[0].get("close") or [])
        closes = [c for c in closes if c is not None]

        price = meta.get("regularMarketPrice")
        hi52, lo52 = meta.get("fiftyTwoWeekHigh"), meta.get("fiftyTwoWeekLow")
        ytd = None
        if len(closes) >= 2 and closes[0]:
            ytd = round((closes[-1] / closes[0] - 1) * 100, 2)
        dist_high = None
        if price and hi52 and hi52 > 0:
            dist_high = round((price / hi52 - 1) * 100, 2)

        return {
            "symbol": symbol,
            "name": meta.get("longName") or meta.get("shortName") or symbol,
            "price": price,
            "currency": meta.get("currency"),
            "ytdPct": ytd,
            "dayChangePct": meta.get("regularMarketChangePercent"),
            "distFromHigh52w": dist_high,
        }
    except Exception as e:  # noqa: BLE001
        return {"symbol": symbol, "error": str(e)}


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    today = datetime.date.today().isoformat()

    with ThreadPoolExecutor(max_workers=12) as pool:
        futs = {pool.submit(fetch, s): s for s, _ in SYMBOLS}
        results = {}
        for fut in as_completed(futs):
            sym = futs[fut]
            try:
                results[sym] = fut.result()
            except Exception as e:  # noqa: BLE001
                results[sym] = {"symbol": sym, "error": str(e)}

    rows = []
    snapshot = {"fecha": today, "instrumentos": {}}
    for sym, nombre in SYMBOLS:
        q = results.get(sym, {})
        rows.append({
            "fecha": today,
            "symbol": sym,
            "nombre": nombre,
            "precio": q.get("price"),
            "moneda": q.get("currency", ""),
            "ytd_pct": q.get("ytdPct"),
            "cambio_dia_pct": q.get("dayChangePct"),
            "dist_max52_pct": q.get("distFromHigh52w"),
        })
        snapshot["instrumentos"][sym] = {
            "nombre": nombre,
            "precio": q.get("price"),
            "moneda": q.get("currency"),
            "ytd_pct": q.get("ytdPct"),
            "cambio_dia_pct": q.get("dayChangePct"),
            "dist_max52_pct": q.get("distFromHigh52w"),
            "error": q.get("error"),
        }

    # anexar al histórico (crear cabecera si no existe)
    new_file = not os.path.exists(HISTORY_CSV)
    fieldnames = ["fecha", "symbol", "nombre", "precio", "moneda",
                  "ytd_pct", "cambio_dia_pct", "dist_max52_pct"]
    with open(HISTORY_CSV, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if new_file:
            w.writeheader()
        w.writerows(rows)

    with open(SNAPSHOT_JSON, "w") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    # resumen a stdout (se inyecta como contexto al agente del cron)
    ok = [r for r in rows if r["precio"] is not None]
    err = [r for r in rows if r["precio"] is None]
    print(f"Snapshot {today}: {len(ok)}/{len(rows)} instrumentos con datos, {len(err)} sin datos.")
    print(f"Histórico acumulado: {HISTORY_CSV}")
    print(f"Snapshot actual: {SNAPSHOT_JSON}")
    for r in sorted(ok, key=lambda x: -(x["ytd_pct"] or -999))[:8]:
        print(f"  {r['symbol']:<15} precio={r['precio']}  ytd={r['ytd_pct']}%  día={r['cambio_dia_pct']}%  dist52={r['dist_max52_pct']}%")
    if err:
        print("Sin datos:", ", ".join(r["symbol"] for r in err))


if __name__ == "__main__":
    main()
