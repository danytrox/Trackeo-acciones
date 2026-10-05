# 07 — Análisis de la cadena de procesadores (Intel, AMD y proveedores)

Actualizado 2026-09-28 con cotizaciones reales (Yahoo Finance v8).

El superciclo de IA está reconfigurando toda la cadena de semiconductores. Ya no basta con
mirar solo a Intel o AMD: la inversión en procesadores se juega en los eslabones que hacen
posible los chips (fundición, equipos, diseño, software EDA). Este análisis cubre las 5 capas,
con un criterio propio de scoring y predicciones a 3-6 meses.

---

## La cadena de procesadores: 5 capas

```
[DISEÑO]          INTC, AMD, ARM, NVDA, MRVL, QCOM
   ↓  envían el diseño a...
[FUNDICIÓN]       TSM (TSMC), GFS (GlobalFoundries), Intel Foundry
   ↓  que usan equipos de...
[EQUIPOS]         ASML (litografía EUV), AMAT (deposición), LRCX (etch),
                  KLAC (inspección/metrología)
   ↓  y software de...
[EDA/SOFTWARE]    SNPS (Synopsys), CDNS (Cadence)
   ↓  y todo se integra con...
[MEMORIA]         MU, WDC, HBM de SK Hynix, Samsung
```

---

## Dato clave: los diseñadores ya corrieron, los "servicios" se quedaron atrás

Este es el hallazgo central del análisis. Mira los retornos reales al 28-sep-2026:

| Capa | Nombre | Precio | YTD 2026 | Dist. máx 52s |
|---|---|---|---|---|
| Diseño | INTC (Intel) | USD 116,03 | **+194,6%** | -18,5% |
| Diseño | MRVL (Marvell) | USD 251,90 | **+181,8%** | -23,6% |
| Diseño | AMD | USD 607,87 | **+172,0%** | -4,9% ⚠️ |
| Diseño | ARM | USD 283,33 | +147,0% | -37,4% |
| Diseño | NVDA | USD 228,86 | +21,2% | -3,3% ⚠️ |
| Diseño | QCOM | USD 187,48 | +8,4% | -27,9% |
| Equipos | AMAT | USD 486,76 | +81,0% | -34,2% |
| Equipos | LRCX | USD 314,47 | +69,9% | -28,3% |
| Equipos | ASML | USD 1.771,41 | +52,2% | -11,4% |
| Equipos | KLAC | USD 189,17 | +48,4% | **-38,5%** |
| Fundición | TSM | USD 452,88 | +41,7% | -5,5% |
| EDA | CDNS | USD 326,70 | +5,3% | -21,6% |
| EDA | SNPS | USD 417,61 | **-13,1%** | -22,6% |

Lectura: los **diseñadores de chips** (INTC +195%, AMD +172%, MRVL +182%) explotaron en 2026
impulsados por la narrativa de IA. Los **proveedores** (equipos, fundición, EDA) subieron mucho
menos (+41% a +81%) o directamente cayeron (SNPS -13%). Eso significa:

1. Si la tesis de procesadores es correcta, el dinero aún no ha llegado del todo a los
   eslabones "picos y palas" — ahí hay upside rezagado.
2. AMD está a solo -4,9% de su máximo de 52 semanas tras +172%: es la entrada más cara de la
   lista. NVDA lo mismo (-3,3%).
3. Varios proveedores ya corrigieron fuerte (KLAC -38%, AMAT -34%, LRCX -28%): compras menos
   extendidas, con la misma exposición al boom.

---

## Criterio propio de scoring (0-100)

Cuatro dimensiones. A diferencia del análisis típico que mira solo momentum, acá la posición
estructural vale más (35 pts) porque en un rally extendido el "foso" es lo que sobrevive a una
corrección. "Valuación" usa la distancia real al máximo de 52 semanas como proxy de cuánto ya
corrigió cada nombre.

### Dimensión A: Posición estratégica (35 pts)

| Nivel | Puntaje | Ejemplos |
|---|---|---|
| Monopolio absoluto (una sola fuente) | 32-35 | ASML (EUV), TSMC (sub-5nm + CoWoS) |
| Liderazgo con barreras muy altas | 26-31 | KLAC (56% metrología), AMAT/LRCX (triopolio), SNPS/CDNS (duopolio EDA) |
| Diferenciado con competencia real | 18-25 | ARM, NVDA, AMD |
| Expuesto a competencia/ciclo | 10-17 | INTC (foundry no probado, CapEx bajando), MRVL, QCOM |

### Dimensión B: Momentum fundamental (25 pts)

| Señal | Puntaje |
|---|---|
| YTD >100% con revisiones al alza | 20-25 |
| YTD 40-100% | 15-19 |
| YTD 5-40% | 10-14 |
| YTD <5% o negativo | 5-9 |

### Dimensión C: Valuación / margen de seguridad (20 pts)

Distancia real al máximo de 52 semanas (dato en vivo).

| Distancia | Puntaje |
|---|---|
| >30% abajo (corrigió fuerte) | 18-20 |
| 20-30% abajo | 15-17 |
| 10-20% abajo | 11-14 |
| 5-10% abajo | 8-10 |
| <5% abajo (pegado al máximo) | 3-7 |

### Dimensión D: Catalizador de corto plazo (20 pts)

| Tipo | Puntaje |
|---|---|
| Guidance/resultados que confirmen superciclo | 16-20 |
| Contratos/producto nuevo | 11-15 |
| Catalizador difuso (rota con el sector) | 5-10 |

---

## Scoring (recalibrado con datos reales al 28-sep-2026)

| Ticker | Empresa  | Capa    | Posición | Momentum | Valuación | Cataliz. | TOTAL | Señal |
|--------|----------|---------|:---:|:---:|:---:|:---:|:---:|-------|
| ASML | ASML | Equipos | 35 | 17 | 13 | 18 | **83** | COMPRAR |
| KLAC | KLA | Equipos | 30 | 15 | 19 | 14 | **78** | COMPRAR |
| AMAT | Applied Materials | Equipos | 28 | 16 | 18 | 14 | **76** | COMPRAR |
| TSM | TSMC | Fundición | 33 | 14 | 10 | 18 | **75** | COMPRAR |
| LRCX | Lam Research | Equipos | 28 | 16 | 17 | 14 | **75** | COMPRAR |
| ARM | Arm Holdings | Diseño | 22 | 18 | 18 | 14 | **72** | ESPECULATIVO |
| CDNS | Cadence | EDA | 28 | 10 | 17 | 12 | **67** | MANTENER |
| MRVL | Marvell | Diseño | 16 | 19 | 17 | 14 | **66** | ESPECULATIVO |
| INTC | Intel | Diseño | 15 | 20 | 15 | 16 | **66** | ESPECULATIVO |
| SNPS | Synopsys | EDA | 28 | 7 | 17 | 12 | **64** | MANTENER |
| AMD | AMD | Diseño | 20 | 20 | 5 | 16 | **61** | ESPECULATIVO |
| QCOM | Qualcomm | Diseño | 16 | 10 | 17 | 12 | **55** | ESPERAR |
| NVDA | Nvidia | Diseño | 20 | 11 | 5 | 15 | **51** | CORREGIR |

Leyenda: COMPRAR (75+), MANTENER (64-74), ESPECULATIVO (55-63), CORREGIR/ESPERAR (<55).

Nota NVDA: no es mala empresa — es que su valuación ya descuenta años de crecimiento perfecto
y está a -3,3% del máximo. En 3-6 meses el riesgo/beneficio está inclinado a la baja si el
ritmo de CapEx de data centers se modera (Deloitte ya advierte ese riesgo para 2027-2028).

---

## Predicciones a 3-6 meses (heurísticas, escenarios)

### Equipos + fundición (ASML, KLAC, AMAT, LRCX, TSM) — la apuesta de mayor convicción

Cada dólar de los ~USD 200B de CapEx 2026 de TSMC, Samsung, Micron y SK Hynix pasa por estas
máquinas. Ya corrigieron entre -11% y -38% desde máximos, así que el punto de entrada es más
limpio que el de los diseñadores.

| Ticker | Bear | Base | Bull | Catalizador |
|--------|:---:|:---:|:---:|------|
| ASML | -8% | +15% | +30% | Guidance TSMC 2026; High-NA EUV a Intel/Samsung |
| KLAC | -8% | +18% | +30% | Cada nodo nuevo (2nm, 1.4nm) exige MÁS inspección, no menos |
| AMAT | -8% | +14% | +25% | Beneficiario directo de todo CapEx de fundición |
| LRCX | -8% | +14% | +25% | HBM stacking + ciclo de recuperación de NAND |
| TSM | -5% | +15% | +30% | CoWoS a 130k wafers/mes; alza de precios en 2nm/3nm |

### Diseño (INTC, AMD, ARM, MRVL) — consolidación probable tras el rally

Ya subieron +147% a +195%. El escenario base es digestión (sideways o leve baja) mientras el
mercado procesa las ganancias. El upside viene de ejecución, no de narrativa.

| Ticker | Bear | Base | Bull | Catalizador |
|--------|:---:|:---:|:---:|------|
| INTC | -25% | 0% | +30% | 18A con yields viables; contrato foundry grande |
| AMD | -20% | 0% | +20% | MI400 supera expectativas; gana share en data center |
| ARM | -20% | +5% | +25% | AGI CPU con Meta escala (ya -37% del máximo, base más limpia) |
| MRVL | -20% | +5% | +20% | Custom ASIC para hyperscalers |

### EDA (SNPS, CDNS) — los rezagados, candidatos a mean-reversion

SNPS cayó -13% YTD y CDNS apenas +5% pese al duopolio de diseño. Si el ciclo de semis sigue,
la brecha con el resto debería cerrarse; si se enfría, su recurrencia los defiende mejor.

| Ticker | Bear | Base | Bull |
|--------|:---:|:---:|:---:|
| SNPS | -10% | +12% | +25% |
| CDNS | -8% | +10% | +20% |

---

## Conclusión para el portafolio (3-6 meses, USD 500-2.000)

Si solo pudiera elegir 4 posiciones de la cadena de procesadores HOY (28-sep-2026):

1. **ASML (núcleo, ~25%)** — Monopolio absoluto de EUV. Backlog ~€38,8B. Todo chip 2nm pasa
   por ASML. La apuesta más simple y duradera. Ya corrigió -11% desde máximos.

2. **KLAC (~25%)** — El más interesante de los equipos: -38,5% desde el máximo (la corrección
   más profunda de la lista) con un foso casi monopolio (56% de inspección). Margen bruto ~60%.
   Cada nodo nuevo exige más metrología. Riesgo/recompensa superior.

3. **TSM (~25%)** — Si la IA crece, TSMC gana; si se enfría, TSMC sigue ganando (fabrica TODO:
   CPUs, GPUs, celulares, autos). +41,7% YTD y a solo -5,5% del máximo es lo más "caliente" de
   mis cuatro, pero su posición es tan dominante que lo mantengo como núcleo.

4. **AMAT o LRCX (~25%, elegir una)** — Exposición amplia al gasto de fábricas (deposición y
   etch son dos de los tres procesos críticos). -28% a -34% desde máximos = entrada menos
   extendida que los diseñadores.

Por qué NO los diseñadores como núcleo AHORA: INTC +195% y AMD +172% ya descontaron una
enorme parte de la tesis, y AMD está a -4,9% del máximo (perseguirla acá es la forma más
rápida de perder en una corrección). Si quieres exposición a diseño, ARM es la menos mala
(-37% del máximo, tesis AGI CPU intacta), pero como satélite pequeño, no como núcleo.

Regla de oro de este análisis: **compra el foso, no el hype**. Los que hacen POSIBLES los
procesadores (ASML, KLAC, AMAT, LRCX, TSMC) ganan sin importar si gana Intel o AMD o Nvidia —
porque le venden a todos. Esa es la forma menos arriesgada de jugar el boom de procesadores.

---

## Fuentes y método

- Cotizaciones: Yahoo Finance chart API v8 (snapshot real del 28-sep-2026, vía scripts/fetch_snapshot.py).
- Scoring: modelo propio de 4 dimensiones (posición 35 / momentum 25 / valuación 20 /
  catalizador 20). Valuación y momentum usan datos reales (distancia al máximo 52s y YTD).
- Predicciones: escenarios bear/base/bull heurísticos derivados del scoring, catalizadores
  identificables y la posición actual en el ciclo (rally masivo de diseñadores 2026, proveedores
  rezagados y/o ya corregidos).
- Datos de industria: Deloitte 2026 Semiconductor Outlook, SEMI CapEx Q2 2025, chokepoints.ai,
  SC-IQ CapEx estimates, Korean Tech Texas analysis.

**Esto no es asesoría financiera.** Los puntajes y predicciones son un marco de análisis, no
una recomendación de compra. El sector es volátil (SOX corrigió -20% en semanas). Opera con
fracciones y no arriesgues más del 20% del capital en nombres individuales.
