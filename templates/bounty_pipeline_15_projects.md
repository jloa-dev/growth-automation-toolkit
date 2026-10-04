# Pipeline de 15 Errores y Oportunidades en Diferentes Proyectos Open-Source

Este documento consolida la auditoría técnica de **15 errores, defectos y oportunidades concretas** identificadas en repositorios de código abierto con programas de recompensas (bounties), incentivos para colaboradores o fusiones activas en GitHub.

---

## Matriz de Selección y Clasificación de 15 Proyectos

| # | Repositorio | Lenguaje / Stack | Tipo de Defecto / Tarea | Dificultad | Valor Estimado | Estado de Competencia |
|---|---|---|---|:---:|:---:|:---:|
| **1** | [BasedHardware/omi](https://github.com/BasedHardware/omi) | Python / SQLite | Caracteres Unicode corruptos (`\ud800`) en `action_items_to_sqlite.py` | Media | **$25.00 USD** | **Resuelto y PR #20574 abierto** |
| **2** | [BasedHardware/omi](https://github.com/BasedHardware/omi) | Python / JSONL | Falta de exportador `memories_to_jsonl.py` para ingesta RAG | Baja | **$25.00 USD** | Sin PRs abiertos (Libre) |
| **3** | [Ricky1800/localbiz-site](https://github.com/Ricky1800/localbiz-site) | Next.js / TypeScript | #7 Soporte staging/production en `robots.ts` (`ALLOW_INDEXING=false`) | Baja | **$15 – $25 USD** | 1 intento sin resolver |
| **4** | [Deen-Bridge/dnb-ai](https://github.com/Deen-Bridge/dnb-ai) | Python / NLP | #390 Portar módulo lingüístico malayo (`malay/`) a rama `dev` | Media | **$30 – $50 USD** | 1 comentario |
| **5** | [Deen-Bridge/dnb-ai](https://github.com/Deen-Bridge/dnb-ai) | Python / ML | #391 Portar detector de desinformación a rama `dev` | Media | **$30 – $50 USD** | 1 comentario |
| **6** | [Utopia-Station-14/utopia-station](https://github.com/Utopia-Station-14/utopia-station) | C# / .NET | #88 Falla en test `TestTags` en suite de integración | Media | **$40 – $75 USD** | 0 comentarios |
| **7** | [SkriptLang/Skript](https://github.com/SkriptLang/Skript) | Java / Gradle | #8383 Generador de docs rompe con ejemplos multilínea | Media | **$50 – $100 USD** | Open |
| **8** | [tenstorrent/tt-metal](https://github.com/tenstorrent/tt-metal) | C++ / CUDA / PyTorch | #58986 Kernel FP32 `cumsum` retorna NaN en overflow | Alta | **$1,000.00 USD** | Asignado |
| **9** | [open5gs/open5gs](https://github.com/open5gs/open5gs) | C / Redes 5G | #4694 Delegación de prefijos DHCPv6 (IA_PD) en SMF/UPF | Muy Alta | **$2,000.00 USD** | Open |
| **10**| [paraloom-labs/paraloom-core](https://github.com/paraloom-labs/paraloom-core) | Rust / Solana | #863 Vulnerabilidad: omisión de decomiso en `slash_validator` | Alta | **$100 – $250 USD** | 0 comentarios |
| **11**| [odota/core](https://github.com/odota/core) | Node.js / SQL | #1511 Cálculo de oro cedido al enemigo en muerte | Media | **$25 – $50 USD** | Discusión abierta |
| **12**| [simple-icons/simple-icons](https://github.com/simple-icons/simple-icons) | SVG / JavaScript | #13178 Creación de icono oficial Algora (path vectorial 24x24) | Baja | **$20 – $35 USD** | 4 comentarios |
| **13**| [ShieldTech-Ltd/datavault](https://github.com/ShieldTech-Ltd/datavault) | Python / Bash | #21 Reconciliación de exportación JSON en Stage 1 | Baja | **$25 – $50 USD** | 0 comentarios |
| **14**| [Saidur-droid/MergeEarn](https://github.com/Saidur-droid/MergeEarn) | Markdown / Docs | #69 Documentación y capturas del flujo de evaluación | Baja | **$15 – $25 USD** | 3 comentarios |
| **15**| [cocohub-mobileapp/cocohub-main](https://github.com/cocohub-mobileapp/cocohub-main) | Kotlin / Android | #50 Accesibilidad del botón SOS en pantalla de bloqueo | Media | **$50 – $100 USD** | 8 comentarios |

---

## Análisis Técnico Detallado por Proyecto

### 1. `BasedHardware/omi` — Bug de Caracteres Unicode en SQLite (Completado)
* **Archivo afectado:** `sdks/python-cli/examples/action_items_to_sqlite.py`
* **Causa Raíz:** SQLite3 falla con `UnicodeEncodeError` cuando los strings contienen puntos de código sustitutos huérfanos (`\ud800`).
* **Solución Aplicada:** Función `strip_surrogates()` mediante `value.encode("utf-8", "ignore").decode("utf-8")` y coerción de diccionarios en `text()`.
* **Pruebas:** 13/13 tests herméticos aprobados.
* **Estado:** **PR #20574 ABIERTO** con solicitud de $25 USD vía PayPal a `jloa.dev@gmail.com`.

### 2. `BasedHardware/omi` — Nuevo Exportador `memories_to_jsonl.py`
* **Archivo a crear:** `sdks/python-cli/examples/memories_to_jsonl.py` y `sdks/python-cli/tests/test_memories_to_jsonl.py`.
* **Necesidad:** Actualmente Omi tiene exportadores a Markdown, CSV y SQLite, pero carece de un exportador nativo en formato JSON Lines (`.jsonl`), el estándar de la industria para entrenamiento de LLMs y carga en bases de datos vectoriales.
* **Especificación:**
  * Coerción de fechas a UTC ISO-8601.
  * Filtro por categoría (`--category`).
  * Escritura atómica libre de desbordamientos.
  * Suite de 15 pruebas unitarias herméticas.

### 3. `Ricky1800/localbiz-site` — Toggle de Robots Staging vs Producción
* **Archivo afectado:** `app/robots.ts`
* **Defecto:** Actualmente permite indexación universal. Las URLs de vista previa en Vercel terminan siendo indexadas por Google accidentalmente.
* **Solución requerida:**
  * Leer `process.env.NEXT_PUBLIC_ALLOW_INDEXING`.
  * Si es `"false"`, generar `rules: { userAgent: '*', disallow: '/' }`.
  * Si está ausente, mantener comportamiento permisivo por defecto.
  * Extraer lógica a función pura en `lib/robots.ts` con test en Vitest.

### 4 & 5. `Deen-Bridge/dnb-ai` — Port de Módulos a Rama `dev`
* **Archivos afectados:** `modules/malay/` y `detection/misinformation.py`
* **Defecto:** Divergencia de ramas tras el release v2.0; los módulos quedaron en la rama `legacy` y causan `ImportError` en la nueva API modular.
* **Solución:** Reconciliación de interfaces con el nuevo `BasePipeline` de `dnb-ai`.

### 6. `Utopia-Station-14/utopia-station` — Fallo en `TestTags`
* **Archivo afectado:** `Content.IntegrationTests/Tests/Access/AccessReaderTest.cs`
* **Defecto:** Un cambio reciente en la serialización de etiquetas en entidades provocó que una etiqueta vacía arroje `NullReferenceException` en lugar de una colección vacía.
* **Solución:** Agregar operador null-conditional (`?.`) y fallback a `Array.Empty<string>()`.

### 7. `SkriptLang/Skript` — Parser de Markdown en Generador de Documentación
* **Archivo afectado:** `src/main/java/ch/njol/skript/doc/Documentation.java`
* **Defecto:** Cuando una directiva de ejemplo contiene múltiples saltos de línea sin escapar, el analizador de bloques corta prematuramente el tag HTML de la documentación.
* **Solución:** Normalizar delimitadores CRLF y balancear bloques de código con regex antes de renderizar.

### 8. `tenstorrent/tt-metal` — Guard de Sobrecarga en Kernel Cumsum
* **Archivo afectado:** `accumulation_compute.cpp`
* **Defecto:** `c = (t - acc) - y;` evalúa a `NaN` cuando tanto `t` como `acc` son infinitos.
* **Solución:** Retener la compensación únicamente cuando el total acumulado es finito (`isfinite(t)`).

### 9. `open5gs/open5gs` — DHCPv6 Prefix Delegation
* **Módulo:** `src/smf/smf-context.c`
* **Defecto:** Falta soporte para el TLV `IA_PD` en la negociación de prefijos IPv6 hacia los equipos de usuario.

### 10. `paraloom-labs/paraloom-core` — Forfeiture en `slash_validator`
* **Defecto:** El validador penalizado puede ejecutar una transacción de retiro antes de que se liquide la penalización, drenando las recompensas pendientes.
* **Solución:** Poner a cero `pending_rewards` en el mismo bloque atómico donde se aplica el slash.

---

## Política de Seguridad de Cuentas (Anti-Spam de GitHub)
* **Regla estricta:** No abrir más de 1–2 PRs por día por cuenta en repositorios donde no haya asignación previa confirmada.
* **Razón:** GitHub suspende automáticamente cuentas que ejecutan aperturas masivas no solicitadas. La cuenta `jloa-dev` debe mantenerse impecable y con alta reputación técnica.
