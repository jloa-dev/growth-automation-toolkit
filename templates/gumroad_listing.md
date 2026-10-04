# Ficha de Producto Digital: LeadPulse CLI (Gumroad / Ko-fi)

**Título del Producto:** LeadPulse CLI — Fast B2B Lead Harvester & Contact Enrichment Engine  
**Precio de Venta:** $25.00 USD  
**Objetivo de Ventas:** 4 compras = $100.00 USD netos  
**Formato de Entrega:** Código fuente Python completo (.zip + repositorio privado en GitHub) + Guía de inicio rápido en Markdown  

---

## Portada / Subtítulo
> Extract verified business emails, phone numbers, LinkedIn profiles, and company metadata at lightning speed. Zero bloated dependencies. Ready for CRM exports.

---

## Descripción del Producto (Markdown para Gumroad/Ko-fi)

Stop paying $99/month for slow SaaS scrapers with credit limits.

**LeadPulse CLI** is a lightweight, developer-friendly Python tool designed for growth engineers, agencies, and outbound sales teams who need clean B2B contact lists fast.

### ⚡ Key Features:
- **Comprehensive Contact Extraction:** Automatically extracts verified emails, phone numbers, LinkedIn company pages, Twitter/X profiles, and page metadata.
- **Smart Validation & Filtering:** Eliminates image files, media artifacts, and temporary disposable email domains (`mailinator`, `tempmail`, etc.).
- **Automated Lead Scoring (0-100):** Ranks leads into Tier-1, Tier-2, and Tier-3 based on contact completeness.
- **CRM-Ready Exports:** Generates clean CSV files formatted for instant import into Apollo, HubSpot, Outreach, or Google Sheets.
- **Executive Markdown Reports:** Creates beautiful client-ready summary tables showing conversion percentages and top verified domains.
- **Batch Processing:** Pass a `.txt` file with 500+ domains and let LeadPulse process them in parallel.
- **100% Standalone Python 3:** Clean, modular code you can customize, embed in your own SaaS, or run in headless Docker environments.

### 📦 What You Get in the Package:
1. `src/leadpulse/` — Full modular Python source code (extractor, enricher, exporter, CLI).
2. `tests/` — Automated test suite with 100% test coverage.
3. `documentation.md` — 5-minute setup guide with sample commands.
4. `sample_leads/` — Example output files (CSV, JSON, and Executive Report).

### 🚀 Quick Start Example:
```bash
# Scan a single domain
python -m src.leadpulse.cli scan stripe.com

# Batch scan a target list
python -m src.leadpulse.cli batch domains.txt --output leads_dataset/
```

**Instant Download:** Unlimited personal and commercial use license.
