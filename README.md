# Radar de Inversión Corto Plazo · 2026

Dashboard web autocontenido para visualizar el rendimiento de acciones y ETFs durante 2026,
comparar escenarios especulativos de corto plazo (3-6 meses) y consultar cotizaciones en vivo
vía Yahoo Finance. Pensado para operar con capital bajo (USD 500-2.000) mediante fracciones de
acciones en [Racional](https://racional.cl).

> ⚠️ **Este proyecto es material informativo/educativo. No es asesoría financiera ni
> recomendación de compra.** Las proyecciones son especulativas y el rendimiento pasado no
> garantiza resultados futuros.

---

## Características

- **Pestaña "Análisis"**: rankings de los mayores ganadores YTD (acciones y ETFs de EE.UU.),
  contexto del IPSA chileno, tres carteras modelo (conservadora / moderada / agresiva) y
  escenarios especulativos Bear/Base/Bull.
- **Pestaña "Mercado en vivo"**: cotizaciones en tiempo real de 35 instrumentos (precio, cambio
  del día, retorno YTD calculado, distancia desde el máximo de 52 semanas y posición en el
  rango de 52 semanas), con auto-refresco cada 60 s.
- **Página aparte "Portafolios agresivos"** (`portafolios.html`): un manifiesto del mercado
  (por qué está donde está) y 4 portafolios de máximo riesgo con rangos Bear/Base/Bull.
- **Sin API keys ni dependencias de terceros** en el backend: solo Python estándar.

---

## Stack tecnológico

| Capa | Tecnología | Rol |
|---|---|---|
| Frontend | HTML5 + CSS (Tailwind CSS vía CDN) | UI, tema oscuro, responsive |
| Gráficos | Chart.js 4 (vía CDN) | Barras, doughnuts, escenarios |
| Backend | Python 3 (stdlib: `http.server`, `urllib`) | Servidor estático + proxy de datos |
| Datos en vivo | Yahoo Finance chart API v8 | Cotizaciones (sin clave) |

No hay `package.json`, bundler ni build step. El backend no requiere `pip install`.

---

## Estructura del proyecto

```
inversion-2026/
├── dashboard.html          # SPA con las dos pestañas (autocontenida)
├── portafolios.html        # Portafolios agresivos + manifiesto del mercado
├── server.py               # Servidor HTTP + proxy a Yahoo Finance
├── README.md
├── .gitignore
├── datos/
│   ├── top_acciones_eeuu_2026.csv
│   ├── top_etfs_2026.csv
│   └── ipsa_chile_2026.md
├── 01_resumen_ejecutivo.md
├── 02_acciones_eeuu.md
├── 03_etfs.md
├── 04_chile_ipsa.md
├── 05_estrategia_3a6meses.md
├── 06_riesgos_disclaimer.md
└── 07_procesadores_cadena.md
```

- `dashboard.html` es el frontend completo: lógica de pestañas, gráficos y `fetch` a `/api/quotes`.
- `server.py` sirve los estáticos y reenvía las consultas de cotizaciones a Yahoo.
- `*.md` y `datos/` son la investigación de respaldo (notas y rankings crudos en CSV).

---

## Requisitos

- Python **3.8+** (sin paquetes externos).
- Navegador moderno con acceso a internet (para los CDN de Tailwind/Chart.js y para que el
  servidor consulte Yahoo).

---

## Instalación

```bash
git clone <url-del-repo>
cd inversion-2026
# no hay dependencias que instalar
```

## Uso

```bash
python3 server.py            # puerto por defecto: 8765
# o con puerto personalizado:
python3 server.py 8080
```

Abre **http://127.0.0.1:8765** en el navegador.

> Importante: usa la URL servida por `server.py`, **no** abras `dashboard.html` directamente con
> `file://`. La pestaña "Mercado en vivo" necesita el proxy porque Yahoo Finance no envía
> cabeceras CORS (ver Arquitectura).

Para detener: `Ctrl+C`.

---

## Arquitectura

### Por qué existe el proxy

Yahoo Finance expone cotizaciones en `query1.finance.yahoo.com/v8/finance/chart/{symbol}`,
pero **no devuelve `Access-Control-Allow-Origin`**, por lo que un `fetch()` directo desde el
navegador es bloqueado por la política de mismo origen (CORS). La API v7 (`/v7/finance/quote`)
requiere cookie + crumb y devuelve `401` sin autenticación.

`server.py` resuelve ambos problemas actuando de proxy: el navegador llama a un endpoint local
(mismo origen, sin CORS) y el servidor consulta Yahoo del lado servidor, donde CORS no aplica.

```
[Navegador] --GET /api/quotes?symbols=...--> [server.py :8765] --GET Yahoo v8--> [Yahoo]
              <--JSON limpio--                      <--JSON crudo--
```

### Endpoint de datos

`GET /api/quotes?symbols=SNDK,MU,SOXX`

- Consulta Yahoo en paralelo (`ThreadPoolExecutor`, 12 workers) con
  `range=ytd&interval=1d`.
- Calcula en el servidor: retorno YTD (primer vs último cierre del año) y distancia respecto
  al máximo de 52 semanas.
- Respuesta:

```json
{
  "asOf": 1789408193,
  "quotes": [
    {
      "symbol": "SNDK",
      "name": "SanDisk Corporation",
      "price": 1575.51,
      "currency": "USD",
      "dayChangePct": -3.54,
      "dayHigh": 1577.77,
      "dayLow": 1505.0,
      "high52w": 2354.39,
      "low52w": 85.12,
      "ytdPct": 472.41,
      "distFromHigh52w": -33.08,
      "posIn52wRange": 65.6,
      "volume": 1234567,
      "exchange": "NasdaqGS",
      "asOf": 1789407970
    }
  ]
}
```

### Otros endpoints

| Endpoint | Descripción |
|---|---|
| `GET /api/health` | `{"ok": true, "time": <epoch>}` — liveness |
| `GET /dashboard.html` | Frontend (también en `/`) |
| `GET /api/quotes` | Cotizaciones (requiere `symbols`) |

---

## Símbolos soportados

El listado está definido en el array `INSTRUMENTS` dentro de `dashboard.html`.

- **Acciones EE.UU.**: `SNDK, DELL, MU, INTC, MRVL, AMD, WDC, ARM, STX, CORT`
- **Cadena de procesadores**: `TSM, ASML, KLAC, AMAT, LRCX, SNPS, CDNS, NVDA, QCOM`
- **ETFs**: `SOXX, SMH, PSI, AIS, XLE, VDE, USO, EWY, EWT, DBC, XBI, DECO`
- **Chile (CLP, sufijo `.SN`)**: `CHILE.SN, LTM.SN, BSANTANDER.SN`
- **Índice**: `^IPSA` (debe ir URL-encoded como `%5EIPSA`)

Para agregar un instrumento, añade una entrada a `INSTRUMENTS` con su `s` (símbolo), `cat`
(`acción` | `ETF` | `chile`) y los escenarios `bear` / `base` / `bull`. No hay que tocar
`server.py`; el proxy consulta cualquier símbolo válido de Yahoo.

---

## Configuración

- **Puerto**: primer argumento de `server.py` (`python3 server.py 8080`).
- **Intervalo de refresco**: `setTimeout(loadLive, 60000)` al final de `loadLive()` en
  `dashboard.html` (por defecto 60 s).
- **Escenarios especulativos**: valores `bear`/`base`/`bull` en `INSTRUMENTS`.

---

## Limitaciones conocidas

- Yahoo puede entregar precios con ~15 min de retraso según la bolsa; no es una fuente de
  tick-by-tick.
- El índice `^IPSA` no expone historial diario por el endpoint v8, por lo que su YTD aparece
  como `—` (sí muestra precio, cambio del día y rango de 52 semanas).
- Sin caché ni rate-limiting: si abres muchas pestañas o recargas agresivamente, Yahoo podría
  empezar a devolver errores transitorios. El cliente muestra "sin datos" por símbolo en ese caso.
- El proxy escucha solo en `127.0.0.1` (no expuesto a la red).

---

## Descargo de responsabilidad

Este proyecto no constituye asesoría financiera. Los datos de retorno YTD varían por fuente y
fecha de corte. Las proyecciones Bear/Base/Bull son rangos heurísticos especulativos, no
pronósticos ni un modelo cuantitativo. Consulta siempre el precio vigente en tu bróker antes de
operar y no inviertas dinero que no puedas permitirte perder.

---

## Fuentes de datos

- Rankings y retornos: ChartRow, YCharts, StockTitan, csimarket
- Noticias/análisis de semiconductores: CNBC, Investopedia, Yahoo Finance
- ETFs: ETF.com, ETFdb, myinvestacademy
- Mercado chileno: La Tercera, Diario Financiero, Rankia, Bloomberg Línea, LarrainVial
- Cotizaciones en vivo: Yahoo Finance (chart API v8)

La lista con enlaces también está dentro de la pestaña "Análisis" del dashboard.

---

## Licencia

MIT. Úsalo, modifícalo y compártelo libremente, sin garantías.
