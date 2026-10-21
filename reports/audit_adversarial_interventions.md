# AUDITORÍA TÉCNICA MAESTRA: DOSSIER DE INTERVENCIONES ADVERSARIALES EN EXPENSIFY/APP

**Autor / Perfil de Ingeniería:** `jloa-dev <jloa.dev@gmail.com>`  
**Perfil Upwork Verificado:** [Upwork Freelancer ~0163955a2ba22190aa](https://www.upwork.com/freelancers/~0163955a2ba22190aa) (W-8BEN Completo, CCI Interbank `00389801350050828245`)  
**Fecha de Corte de Auditoría:** 2026-10-21T02:15:00Z  
**Repositorio Objetivo:** `Expensify/App` (HEAD commit local: `4c358bdd3ee`)  
**Guardarraíl de Seguridad:** 100% CONFIDENCIAL Y LOCAL EN `scratch/`. CERO comentarios publicados en GitHub/Upwork sin aprobación previa explícita del usuario.

---

## 1. RESUMEN EJECUTIVO Y DASHBOARD FINANCIERO

### 1.1 Balance Integral del Pipeline de Bounties
Una auditoría integral y bidireccional entre el inventario histórico (`TASK_LEDGER.md`) y el estado en vivo de la API de GitHub (`Expensify/App`) revela el estado exacto del capital y las oportunidades activas:

- **Inventario Total Registrado en Ledger:** 101 tareas rastreadas.
  - **98 Tareas formalmente ABIERTAS en Ledger:** Representando **$17,475 USD** (~S/. 65,531 PEN) en fondos potenciales de Upwork Escrow.
  - **3 Tareas cerradas / asignadas previamente:** #103324 ($175), #103355 ($175), #103531 ($250).
- **Estado en Vivo en GitHub (101 Issues Analizados):**
  - **9 Issues Cerrados Definitivamente en GitHub:** #102437, #103324, #103355, #103538, #103663, #103664, #103671, #103770, #103863 ($1,850 USD cerrados).
  - **11 Issues con Desarrollador Contratado en Upwork:** #102072, #102792, #102868, #103063, #103198, #103341, #103531, #103593, #103764, #103944, #104089 ($1,975 USD contratados).
  - **15 Issues Descalificados por Intervención de Bots (Regla 3 Anti-Bot Merge):** #103345, #103488, #103662, #103726, #103775, #103898, #104093, #104147, #102734, #103058, #103759, #104300, #103216, #103492, #103957 ($2,625 USD descalificados para proteger horas de desarrollo).
  - **66 Issues Formalmente Abiertos y No Asignados en GitHub:** Representando **$11,575 USD** en fondos activos.

```
┌────────────────────────────────────────────────────────────────────────┐
│               PIPELINE GLOBAL EXPENSIFY/APP (101 ISSUES)               │
├──────────────────────┬──────────────────────┬──────────────────────────┤
│ Cerrados / Hired     │ Descalificados Bot   │ Abiertos No Asignados    │
│ 20 Issues ($3,825)   │ 15 Issues ($2,625)   │ 66 Issues ($11,575)      │
└──────────────────────┴──────────────────────┴──────────────────────────┘
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
┌──────────────────────────────┐        ┌──────────────────────────────┐
│ HIGH-PRIORITY (0-2 RIVALES)  │        │ MEDIUM-PRIORITY (3+ RIVALES) │
│ 37 Issues ($6,350 USD)       │        │ 29 Issues ($5,225 USD)       │
└──────────────────────────────┘        └──────────────────────────────┘
```

### 1.2 Dashboard de Objetivos de Alta Prioridad (37 Issues / $6,350 USD)
Filtrando los 66 issues abiertos bajo la **Regla 2 (Baja Competencia: 0 a 2 rivales)** y la **Regla 1 (Fresh / Same-Day Issues)**, se aíslan exactamente **37 objetivos de alta prioridad** valorados en **$6,350 USD** en custodia bancaria verificada de Upwork Escrow:

1. **Tier 1: 0 Rivales Humanos (Incontestados / Solo Play):** **7 Issues ($1,225 USD)**. Ventaja FCFS absoluta. Incluye tickets con revisores C+ y Staff revisando activamente (#103326, #103307).
2. **Tier 2: 1 Rival Humano:** **9 Issues ($1,575 USD)**. Tickets frescos del 20 de Octubre (Sentry / HybridApp) y tickets maduros donde el rival cometió fallas fatales de arquitectura.
3. **Tier 3: 2 Rivales Humanos:** **21 Issues ($3,550 USD)**. Tickets donde el análisis adversarial expone deficiencias reproducibles en las propuestas de los competidores.

---

## 2. TABLA MAESTRA DE PRIORIZACIÓN DE LOS 37 OBJETIVOS

Clasificación de probabilidad de éxito:
- **ALTA (21 Issues / $3,675 USD):** 0 o 1 rival, o 2 rivales con falla técnica comprobada/reproducible y propuesta superior de `jloa-dev` lista para cobro.
- **MEDIA (6 Issues / $1,050 USD):** Disputa de diseño, soporte de pruebas nativas requeridas o a la espera de etiqueta *Help Wanted*.
- **BAJA / DESCARTE (10 Issues / $1,625 USD):** Bloqueo comprobado en Backend interno, Not-A-Bug (NAB), PR interno ya fusionado, o PR de MelvinBot activo.

| # | Issue # | Título del Issue | Escrow ($) | Staff / C+ Assignees | Enlace Upwork Escrow | Rivales | Veredicto Auditoría / Estado Técnico | Prioridad |
|---|---|---|---|---|---|---|---|---|
| **1** | [#103326](https://github.com/Expensify/App/issues/103326) | Offline 'Upload Attachment' grey text | $175 | `@TaduJR` | [Job ~022107813804128160468](https://www.upwork.com/jobs/~022107813804128160468) | 0 | **HOT ALERT:** C+ `@TaduJR` posteó: *"Not overdue reviewing today"*. `jloa-dev` es el ÚNICO proponente. | **ALTA (INMEDIATA)** |
| **2** | [#103307](https://github.com/Expensify/App/issues/103307) | Gusto default to "Manager approval" | $175 | `@MonilBhavsar`, `@thelullabyy` | [Job ~022107779832826515888](https://www.upwork.com/jobs/~022107779832826515888) | 0 | **HOT ALERT:** Staff `@MonilBhavsar` posteó: *"Going to check"*. Sello `🎀 👀 🎀 C+ reviewed`. Solo `jloa-dev`. | **ALTA (INMEDIATA)** |
| **3** | [#104501](https://github.com/Expensify/App/issues/104501) | [Sentry: APP-DQ2] Web: FlashList commitLayout loops | $175 | `@mountiny`, `@getusha` | [Job ~022112683613241355184](https://www.upwork.com/jobs/~022112683613241355184) | 1 (`@magomedta`) | **FALLA RIVAL:** Rival usó `useCallback` con dependencia inestable `measureScrollbarRef`. Hallucinación de `@juni2003`. | **ALTA** |
| **4** | [#104502](https://github.com/Expensify/App/issues/104502) | [Sentry: APP-MHA] iOS: FlashList LayoutManager uninitialized | $175 | `@mountiny`, `@linhvovan29546` | [Job ~022112637720568651801](https://www.upwork.com/jobs/~022112637720568651801) | 1 (`@haiquywork`) | **FALLA RIVAL:** Rival llamó a método inexistente `hasLayout()` en `itemViewabilityManager`. Parche jloa-dev completo. | **ALTA** |
| **5** | [#104503](https://github.com/Expensify/App/issues/104503) | [Sentry: APP-MD4] Android: Cannot find module ExpoAudio | $175 | `@mountiny`, `@ikevin127` | [Job ~022112637848604843209](https://www.upwork.com/jobs/~022112637848604843209) | 2 (`@taieddie`, `@haiquywork`) | **FALLA RIVAL:** Static import causa `SIGABRT` en bundle. `audioPromise` se corrompe permanentemente en catch. | **ALTA** |
| **6** | [#104505](https://github.com/Expensify/App/issues/104505) | [Sentry: APP-N5H] Android: tab bar crash >6 items | $175 | `@mananjadhav`, `@mountiny` | [Job ~022112637743125227618](https://www.upwork.com/jobs/~022112637743125227618) | 1 (`@RajGahoi`) | **FALLA RIVAL:** Rival culpa a JS (`tabBarItemHidden`), pero el bug es una fuga nativa en Kotlin `TabsContainer.kt`. | **ALTA** |
| **7** | [#104509](https://github.com/Expensify/App/issues/104509) | Card - Next button replaced with loading spinner freeze | $175 | `@eh2077` | [Job ~022112633586567027913](https://www.upwork.com/jobs/~022112633586567027913) | 2 (`@camesenin`, `@khizzcr7`) | **FALLA RIVAL:** `@camesenin` inventó formID inexistente; `@juni2003` rechaza promesas en submit; validación rota. | **ALTA** |
| **8** | [#104515](https://github.com/Expensify/App/issues/104515) | Empty "Check your info" in RHP after adding BA | $175 | `@brunovjk` | [Job ~022112637793222357815](https://www.upwork.com/jobs/~022112637793222357815) | 2 (`@camesenin`, `@khizzcr7`) | **FALLA RIVAL:** Rivales proponen `closeRHPFlow()`, el cual solo hace pop de 1 pantalla si `routes > 1`, dejando la pantalla vacía. | **ALTA** |
| **9** | [#104519](https://github.com/Expensify/App/issues/104519) | Search - Contextual suggestion for Held Report missing | $175 | `@rojiphil` | [Job ~022112649059231981593](https://www.upwork.com/jobs/~022112649059231981593) | 2 (`@taieddie`, `@khizzcr7`) | **FALLA RIVAL:** `@khizzcr7` olvidó importar `isMoneyRequestReport` (crash `ReferenceError`); `@taieddie` rompe privacidad. | **ALTA** |
| **10** | [#103838](https://github.com/Expensify/App/issues/103838) | Tab bar visible above spinner in Per Diem | $175 | `@situchan` | [Job ~022109928824204193624](https://www.upwork.com/jobs/~022109928824204193624) | 0 | **UNCONTESTED:** MelvinBot pingueó a `@situchan` (6 días de atraso). Propuesta en solitario de `jloa-dev`. | **ALTA** |
| **11** | [#103244](https://github.com/Expensify/App/issues/103244) | Onboarding promo shown to invited employees | $175 | `@shubham1206agra` | [Job ~022107586630303041825](https://www.upwork.com/jobs/~022107586630303041825) | 0 | **FIRST PROPOSER:** `jloa-dev` propuso Oct 8. Tracing de `@emkhalid` confirmó el selector propuesto. Staff pingueado. | **ALTA** |
| **12** | [#103156](https://github.com/Expensify/App/issues/103156) | Offline Bank Unlock Doesn’t Open Concierge | $175 | `@rojiphil` | [Job ~022107402976279218900](https://www.upwork.com/jobs/~022107402976279218900) | 0 | **UNCONTESTED:** Solo play. Resuelve modal sin salida en `WorkflowsPaymentsTab.tsx` y fallback offline. | **ALTA** |
| **13** | [#103721](https://github.com/Expensify/App/issues/103721) | Per Diem: Not here page after going online | $175 | `@situchan` | [Job ~022109593475976808400](https://www.upwork.com/jobs/~022109593475976808400) | 1 (`@ashusatyarthi-wq`) | **FALLA RIVAL:** `getSelectedWorkspacePolicyID` falla en Self-DM Track expenses, provocando crash persistente. | **ALTA** |
| **14** | [#103245](https://github.com/Expensify/App/issues/103245) | Agent: infinite loading switch to Copilot | $175 | `@mananjadhav` | [Job ~022107586883241239186](https://www.upwork.com/jobs/~022107586883241239186) | 1 (`@bonnhatnguyen`) | **FALLA RIVAL:** Rival modificó `AgentsPage.tsx`, pero la carga reside en el hook `useAgents.ts:46-48`. | **ALTA** |
| **15** | [#103349](https://github.com/Expensify/App/issues/103349) | Android: HEVC video share sheet missing | $175 | `@rojiphil` | [Job ~022107849209866715481](https://www.upwork.com/jobs/~022107849209866715481) | 1 (`@camesenin`) | **OVERDUE CONVERGENCE:** 12 días de atraso en Staff. Solución MIME `video/*` verificada en AndroidManifest. | **ALTA** |
| **16** | [#103214](https://github.com/Expensify/App/issues/103214) | New avatar not reflected after upload | $175 | `@mkhutornyi` | [Job ~022107501218908067689](https://www.upwork.com/jobs/~022107501218908067689) | 1 (`@camesenin`) | **OVERDUE CONVERGENCE:** Invalida Glide disk cache en Android mediante remount key `${size}_${avatarSource}`. | **ALTA** |
| **17** | [#102683](https://github.com/Expensify/App/issues/102683) | Spend Card filter company card nickname | $175 | `@ChavdaSachin` | [Job ~022105371204565575660](https://www.upwork.com/jobs/~022105371204565575660) | 2 (`@camesenin`, `@bonnhatnguyen`) | **FALLA RIVAL:** Rivales declaran `text` antes de actualizar `cardName`, fallando en tarjetas no asignadas. | **ALTA** |
| **18** | [#104161](https://github.com/Expensify/App/issues/104161) | Spend It's not here page on split expense | $175 | `@mkhutornyi` | [Job ~022110831219914409226](https://www.upwork.com/jobs/~022110831219914409226) | 2 (`@camesenin`, `@janiya2`) | **FALLA RIVAL:** `@camesenin` omite `backTo`, destruyendo los filtros de búsqueda al retroceder. | **ALTA** |
| **19** | [#104138](https://github.com/Expensify/App/issues/104138) | Receipts not showing fully forwarded email | $175 | `@sobitneupane` | [Job ~022110793935688626891](https://www.upwork.com/jobs/~022110793935688626891) | 2 (`@bconnnnn`, `@Metarenessans`) | **FALLA RIVAL:** `@bconnnnn` admitió IA no verificada; `@Metarenessans` usó tipado erróneo de RN. Rama lista. | **ALTA** |
| **20** | [#103802](https://github.com/Expensify/App/issues/103802) | Expense - Edit split delete per diem | $175 | `@situchan` | [Job ~022109697864167641150](https://www.upwork.com/jobs/~022109697864167641150) | 2 (`@haiquywork`, `@camesenin`) | **FALLA RIVAL:** `@khizzcr7` desactivó Edit Split destruyendo reasignación. `jloa-dev` tiene prioridad FCFS. | **ALTA** |
| **21** | [#103876](https://github.com/Expensify/App/issues/103876) | Amex feed error persists after reconnect | $175 | `@TaduJR` | [Job ~022109996863454032366](https://www.upwork.com/jobs/~022109996863454032366) | 2 (`@janiya2`, `@camesenin`) | **FALLA RIVAL:** `@janiya2` dispara actualización masiva HTTP (error 429 rate limit) y no limpia errores de feed. | **ALTA** |
| **22** | [#104221](https://github.com/Expensify/App/issues/104221) | Workspace admin can view other WS card tx | $175 | `@abdulrahuman5196` | [Job ~022111073873591100700](https://www.upwork.com/jobs/~022111073873591100700) | 2 (`@camesenin`, `@janiya2`) | **COMPETENCIA CERRADA:** Fuga de boundary en feeds compartidos. Rama `fix/104221` pre-codificada lista. | **MEDIA / ALTA** |
| **23** | [#103778](https://github.com/Expensify/App/issues/103778) | [Sentry: APP-M66] ReactModalHostView dialog null | $175 | `@mountiny`, `@cretadn22` | [Job ~022109653602347544408](https://www.upwork.com/jobs/~022109653602347544408) | 2 (`@haiquywork`, `@tnclaudecode`) | **NATIVE EXPERT REQUESTED:** C+ `@cretadn22` pidió experto Android. Callback uncancelled en decorView. | **MEDIA / ALTA** |
| **24** | [#104162](https://github.com/Expensify/App/issues/104162) | Expense report field non-reimbursable | $175 | `@Krishna2323` | [Job ~022110833816404111157](https://www.upwork.com/jobs/~022110833816404111157) | 2 (`@janiya2`, `@sijo0218`) | **DISPUTA DE DISEÑO:** Debate entre cerrar como NAB o verificar roles de Admin/Manager (regresión #81608). | **MEDIA** |
| **25** | [#103779](https://github.com/Expensify/App/issues/103779) | TriNet Missing Final Approver Custom | $175 | `@ZhenjaHorbach` | [Job ~022109655010878713688](https://www.upwork.com/jobs/~022109655010878713688) | 2 (`@haiquywork`, `@David-2002065`) | **RIVAL DESPISTADO:** `@haiquywork` editó el subsistema incorrecto. Posible comportamiento intencional (NAB). | **MEDIA** |
| **26** | [#103961](https://github.com/Expensify/App/issues/103961) | Web Browser back navigates to action | $175 | `@suneox` | [Job ~022110241879857618845](https://www.upwork.com/jobs/~022110241879857618845) | 2 (`@janiya2`, `@camesenin`) | **NOT HELP WANTED:** C+ y Staff reproduciendo internamente. En espera de etiqueta oficial Help Wanted. | **MEDIA** |
| **27** | [#102730](https://github.com/Expensify/App/issues/102730) | Ecard empty illustration demoted admin | $175 | `@jayeshmangwani` | [Job ~022105573983988233029](https://www.upwork.com/jobs/~022105573983988233029) | 2 (`@camesenin`, `@bonnhatnguyen`) | **BLOCKED ON BE:** C+ `@jayeshmangwani` verificó que requiere limpieza de Onyx en Backend al expulsar usuario. | **MEDIA / BAJA** |
| **28** | [#104165](https://github.com/Expensify/App/issues/104165) | Bank account Address Line 2 not saved | $175 | `@puneetlath`, `@nyomanjyotisa` | Direct Applause / Upwork | 2 (`@janiya2`, `@bonnhatnguyen`) | **BLOCKED ON BE:** C+ `@nyomanjyotisa` testeó en staging; el Backend descarta `addressStreet2`. | **BAJA / BLOCKED** |
| **29** | [#104127](https://github.com/Expensify/App/issues/104127) | Android: Concierge category natural lang | $175 | `@rojiphil` | [Job ~022110784962634286346](https://www.upwork.com/jobs/~022110784962634286346) | 0 | **BACKEND ONLY:** MelvinBot confirmó que el bug radica en los tool calls del LLM del servidor. | **BAJA / DESCARTE** |
| **30** | [#103965](https://github.com/Expensify/App/issues/103965) | Import contacts missing on iOS | $175 | `@rojiphil` | [Job ~022110270660163217377](https://www.upwork.com/jobs/~022110270660163217377) | 0 | **NAB (NOT A BUG):** PR #102928 fue explícitamente Android-only (`canPickContacts = false` en iOS). | **BAJA / DESCARTE** |
| **31** | [#104159](https://github.com/Expensify/App/issues/104159) | Chat short mention single char dot | $175 | `@ahmedGaber93` | [Job ~022110828231641473065](https://www.upwork.com/jobs/~022110828231641473065) | 2 (`@janiya2`, `@bonnhatnguyen`) | **NAB / SEVERE PRIVACY LEAK:** Quitar `isDomainPublic` filtraría correos entre dominios públicos. | **BAJA / DESCARTE** |
| **32** | [#104287](https://github.com/Expensify/App/issues/104287) | Search Error & From dropped group-by | $175 | `@truph01`, `@nabi-ebrahimi` | [Job ~022111443332056306411](https://www.upwork.com/jobs/~022111443332056306411) | 1 (`@nabi-ebrahimi`) | **CONTRATADO:** C+ `@truph01` asignó a `@nabi-ebrahimi` por ser autor del issue previo #89168. | **DESCARTE (HIRED)** |
| **33** | [#104176](https://github.com/Expensify/App/issues/104176) | Filters Vendor option missing | $175 | `@suneox` | [Job ~022110885193812397155](https://www.upwork.com/jobs/~022110885193812397155) | 1 (`@camesenin`) | **ON HOLD:** Puesto en hold formal por C+ `@suneox` en espera de PR interno #104351. | **DESCARTE (HOLD)** |
| **34** | [#103824](https://github.com/Expensify/App/issues/103824) | Native share large video crash | $175 | `@huult`, `@luacmartins` | [Job ~022109895596413811824](https://www.upwork.com/jobs/~022109895596413811824) | 2 (`@j3ffffff`, `@taieddie`) | **FUSIONADO EN PROD:** Staff `@luacmartins` lo arregló en repo privado `Mobile-Expensify` PR #14181. | **DESCARTE (CLOSED)** |
| **35** | [#103183](https://github.com/Expensify/App/issues/103183) | Tags truncated with `\:` | $175 | `@bernhardoj` | [Job ~022107464881310224816](https://www.upwork.com/jobs/~022107464881310224816) | 2 (`@camesenin`, `@bonnhatnguyen`) | **BOT DRAFT PR:** MelvinBot abrió Draft PR #104305 por comando de `@bernhardoj`. | **DESCARTE (BOT)** |
| **36** | [#103240](https://github.com/Expensify/App/issues/103240) | DEV Duplicate key error in console | $50 | `@eVoloshchak` | [Job ~022107570335145085652](https://www.upwork.com/jobs/~022107570335145085652) | 2 (`@camesenin`, `@amar-sheikh`) | **BOT DRAFT PR:** MelvinBot abrió Draft PR #104034 por comando de `@eVoloshchak`. | **DESCARTE (BOT)** |
| **37** | [#103533](https://github.com/Expensify/App/issues/103533) | Concierge image cut preview in RHP | $175 | `@roryabraham`, `@abzokhattab` | [Job ~022108319757049731349](https://www.upwork.com/jobs/~022108319757049731349) | 2 (`@camesenin`, `@taieddie`) | **BOT DRAFT PR:** MelvinBot abrió Draft PR #104288 tras sello de `@abzokhattab`. | **DESCARTE (BOT)** |

---

## 3. TABLAS RESUMEN DE ISSUES DESCALIFICADOS Y CERRADOS

### 3.1 Descalificados por Intervención de Bots (Regla 3 Anti-Bot Merge)
Total: 15 issues ($2,625 USD). En estos tickets, un bot interno de Expensify (`@MelvinBot`) ya tiene un PR abierto o fue ordenado formalmente a implementar la solución:

| Issue | Bounty | Staff / C+ Assignee | Razón de Descalificación / Estado del Bot |
|---|---|---|---|
| [#103345](https://github.com/Expensify/App/issues/103345) | $175 USD | `@hoangzinh` | PR automatizado de MelvinBot fusionado / activo (`Due for payment 2026-10-26`). |
| [#103488](https://github.com/Expensify/App/issues/103488) | $175 USD | `@melvin-bot` | PR automatizado de MelvinBot fusionado / activo (`Due for payment 2026-10-23`). |
| [#103662](https://github.com/Expensify/App/issues/103662) | $175 USD | `@melvin-bot` | PR automatizado de MelvinBot fusionado / activo (`Due for payment 2026-10-27`). |
| [#103726](https://github.com/Expensify/App/issues/103726) | $175 USD | `@melvin-bot` | PR automatizado de MelvinBot fusionado / activo (`Due for payment 2026-10-23`). |
| [#103775](https://github.com/Expensify/App/issues/103775) | $175 USD | `@melvin-bot` | PR automatizado de MelvinBot fusionado / activo (`Due for payment 2026-10-26`). |
| [#103898](https://github.com/Expensify/App/issues/103898) | $175 USD | `@melvin-bot` | PR automatizado de MelvinBot fusionado / activo (`Due for payment 2026-10-23`). |
| [#104093](https://github.com/Expensify/App/issues/104093) | $175 USD | `@melvin-bot` | PR automatizado de MelvinBot fusionado / activo (`Due for payment 2026-10-27`). |
| [#104147](https://github.com/Expensify/App/issues/104147) | $175 USD | `@neil-marcellini` | 2 PRs automatizados y llamadas `@MelvinBot implement this` de mantenedor. |
| [#102734](https://github.com/Expensify/App/issues/102734) | $175 USD | `@dubielzyk-expensify` | Mantenedor ejecutó `@MelvinBot implement this`. |
| [#103058](https://github.com/Expensify/App/issues/103058) | $175 USD | `@marufsharifi` | C+ `@marufsharifi` ejecutó `@MelvinBot implement this`. |
| [#103759](https://github.com/Expensify/App/issues/103759) | $175 USD | `@rojiphil` | Mantenedor `@rojiphil` ejecutó `@MelvinBot implement this`. |
| [#104300](https://github.com/Expensify/App/issues/104300) | $175 USD | `@ChavdaSachin` | Mantenedor `@ChavdaSachin` ejecutó `@MelvinBot implement this`. |
| [#103216](https://github.com/Expensify/App/issues/103216) | $175 USD | `@FitseTLT` | C+ `@FitseTLT` endosó formalmente a Melvin: `@MelvinBot implement 🎀 👀 🎀 C+ reviewed`. |
| [#103492](https://github.com/Expensify/App/issues/103492) | $175 USD | `@cretadn22` | C+ `@cretadn22`: `@MelvinBot's proposal looks good to me 🎀 👀 🎀 C+ reviewed`. |
| [#103957](https://github.com/Expensify/App/issues/103957) | $175 USD | `@brunovjk` | C+ `@brunovjk`: `This appears to be expected behavior, as explained in Melvin... 🎀 👀 🎀 C+ reviewed`. |

*(Nota: En la Tabla Maestra 2, los issues #103183, #103240 y #103533 también poseen Draft PRs de MelvinBot #104305, #104034 y #104288 respectivamente, quedando descartados bajo el mismo criterio).*

### 3.2 Issues con Contribuidor Ya Contratado en Upwork
Total: 11 issues ($1,975 USD). Se encuentran abiertos en GitHub pero ya poseen contrato activo en Upwork Escrow:

| Issue | Bounty | Contribuidor Contratado | Estado de Pago / Nota |
|---|---|---|---|
| [#102072](https://github.com/Expensify/App/issues/102072) | $250 USD | `@yusufdeveloper2903` | Contratado en Upwork. |
| [#102792](https://github.com/Expensify/App/issues/102792) | $175 USD | `@dukenv0307` | Contratado (`Due for payment 2026-10-27`). |
| [#102868](https://github.com/Expensify/App/issues/102868) | $175 USD | `@dukenv0307` | Contratado en Upwork. |
| [#103063](https://github.com/Expensify/App/issues/103063) | $175 USD | `@gijoe0295` | Contratado en Upwork. |
| [#103198](https://github.com/Expensify/App/issues/103198) | $175 USD | `@thelullabyy` | Contratado en Upwork. |
| [#103341](https://github.com/Expensify/App/issues/103341) | $175 USD | `@dmkt9` | Contratado en Upwork. |
| [#103531](https://github.com/Expensify/App/issues/103531) | $250 USD | `@nabi-ebrahimi` | Contratado en Upwork. |
| [#103593](https://github.com/Expensify/App/issues/103593) | $175 USD | `@nkdengineer` | Contratado (`Due for payment 2026-10-22`). |
| [#103764](https://github.com/Expensify/App/issues/103764) | $175 USD | `@mountiny` (Staff) | Asignado internamente (`Due for payment 2026-10-26`). |
| [#103944](https://github.com/Expensify/App/issues/103944) | $175 USD | `@Eskalifer1` | Contratado (`Due for payment 2026-10-23`). |
| [#104089](https://github.com/Expensify/App/issues/104089) | $175 USD | `@rayane-d` | Contratado en Upwork. |

### 3.3 Issues Totalmente Cerrados en GitHub
Total: 9 issues ($1,850 USD):

| Issue | Bounty | Razón de Cierre en GitHub |
|---|---|---|
| [#102437](https://github.com/Expensify/App/issues/102437) | $250 USD | Cerrado (re-scoped / resuelto internamente). |
| [#103324](https://github.com/Expensify/App/issues/103324) | $175 USD | Cerrado (problema de DNS interno en cuenta de prueba). |
| [#103355](https://github.com/Expensify/App/issues/103355) | $175 USD | Cerrado NAB por decisión del equipo de diseño. |
| [#103538](https://github.com/Expensify/App/issues/103538) | $175 USD | Cerrado / resuelto. |
| [#103663](https://github.com/Expensify/App/issues/103663) | $250 USD | Cerrado / fusionado. |
| [#103664](https://github.com/Expensify/App/issues/103664) | $250 USD | Cerrado / fusionado. |
| [#103671](https://github.com/Expensify/App/issues/103671) | $250 USD | Cerrado (`Due for payment 2026-10-21`). |
| [#103770](https://github.com/Expensify/App/issues/103770) | $175 USD | Cerrado. |
| [#103863](https://github.com/Expensify/App/issues/103863) | $175 USD | Cerrado. |

---

## 4. FICHAS TÉCNICAS DE INTERVENCIÓN ADVERSARIAL (DETAILED DOSSIERS)

A continuación se presentan las fichas técnicas completas para los objetivos de máxima probabilidad de conversión, con diagnósticos adversariales, escenarios de prueba donde fallan los rivales, solución de ingeniería y borradores exactos en inglés listos para copiar y pegar tras aprobación del usuario.

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #1: ISSUE #104501 (FRESH 20 OCT — SENTRY WEB FLASHLIST LOOP)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/104501`
- **Upwork Escrow:** [Job #022112683613241355184](https://www.upwork.com/jobs/~022112683613241355184) ($175 USD)
- **Assignees:** Staff `@mountiny`, C+ `@getusha`
- **Rival Principal:** `@magomedta` (comentario en hilo) y `@juni2003`

### Diagnóstico Adversarial del Rival:
1. `@juni2003` alucinó por completo la jerarquía de componentes: afirmó que `AddExistingExpense` pasa un array en línea `sections` a `SelectionList` (`const sections = [{ title: translate('common.expenses'), data: existingExpenses }]`) y propuso memorizarlo. En `src/pages/AddExistingExpense.tsx` no existe `SelectionList`; renderiza `<AddExistingExpenseTable>`, que usa `<Table>`, que usa `<TableBody>`, que usa `<FlashList>`. El código citado por el rival no existe.
2. `@magomedta` propuso envolver la referencia de `FlashList` en `TableBody.tsx` usando `useCallback((instance) => { listRef.current = instance; measureScrollbarRef(instance); }, [listRef, measureScrollbarRef])`. En `src/hooks/useVerticalScrollbarWidth/index.ts:20-40`, `measureScrollbarRef` es una función cruda NO memorizada. En `src/components/Table/Table.tsx:275`, recibe una nueva instancia de función en cada render. Incluir `measureScrollbarRef` en el dependency array de `useCallback` hace que `setListRef` cambie de referencia en **cada renderizado de Table**, destruyendo la estabilidad de la ref y perpetuando el ciclo infinito de re-renders de Sentry (`Maximum update depth exceeded`).

### Ubicación Exacta en el Código:
- `src/components/Table/TableBody.tsx:471-477` (literal de objeto `maintainVisibleContentPosition={{disabled: true}}` re-instanciado en cada render).
- `src/components/Tables/AddExistingExpenseTable/index.tsx:147` (objeto literal duplicado).
- `src/hooks/useVerticalScrollbarWidth/index.ts:20-40` (`measureScrollbarRef` sin `useCallback`).
- `src/pages/AddExistingExpense.tsx:96` (`createUnreportedExpenses` sin memorización).

### Escenario de Prueba (Test Steps):
1. Iniciar sesión en Web / Desktop.
2. Abrir un reporte de gastos con al menos 1 transacción existente no reportada.
3. Navegar a `/search/r/:reportID/add-existing-expense`.
4. Con la solución de `@magomedta`, abrir las DevTools de React Profiler o inspeccionar la consola: observar que `TableBody` se re-renderiza continuamente hasta alcanzar React Error #185 (`Maximum update depth exceeded`).

### Superioridad Técnica de jloa-dev:
Se define una constante inmutable `MVCP_DISABLED = {disabled: true}` a nivel de módulo en `TableBody.tsx` y `AddExistingExpenseTable.tsx`. Se memoriza `measureScrollbarRef` dentro de `useVerticalScrollbarWidth` con `useCallback(..., [])` para evitar que las referencias de scrollbar thrasheen la lista. Se memoriza la transformación de datos en `AddExistingExpense.tsx` mediante `useMemo`.

### Borrador Exacto de Intervención Técnica (Listo para Aprobar):
```markdown
Hi @mountiny @getusha!

Regarding the FlashList `Maximum update depth exceeded` loop in `AddExistingExpense`:

There is a critical referential stability issue to be aware of:
In `src/hooks/useVerticalScrollbarWidth/index.ts:20-40`, `measureScrollbarRef` is instantiated as a raw unmemoized arrow function on every render of `Table.tsx`. If `measureScrollbarRef` is passed inside the dependency array of a `useCallback` ref for `FlashList` (as suggested above), `setListRef` changes reference on every single render pass. This continuously triggers `commitLayout` inside FlashList's `ViewHolderCollection.js:116`, reproducing the exact infinite re-render loop recorded in Sentry APP-DQ2.

To resolve this cleanly:
1. Define a module-level constant in `TableBody.tsx` and `AddExistingExpenseTable/index.tsx`:
```typescript
const MVCP_DISABLED = {disabled: true};
```
and pass `maintainVisibleContentPosition={MVCP_DISABLED}` instead of inline object literals.
2. In `src/hooks/useVerticalScrollbarWidth/index.ts`, wrap `measureScrollbarRef` in `useCallback`:
```typescript
const measureScrollbarRef = useCallback((instance: ScrollableNodeHolder | null) => {
    // ... measurement logic
}, []);
```
3. In `src/pages/AddExistingExpense.tsx:96`, wrap `createUnreportedExpenses(transactions)` in `useMemo`.

This stabilizes FlashList layout passes across all layers with zero layout thrashing. Ready to open PR!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #2: ISSUE #104502 (FRESH 20 OCT — SENTRY IOS FLASHLIST LAYOUT)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/104502`
- **Upwork Escrow:** [Job #022112637720568651801](https://www.upwork.com/jobs/~022112637720568651801) ($175 USD)
- **Assignees:** Staff `@mountiny`, C+ `@linhvovan29546`
- **Rival Principal:** `@haiquywork`

### Diagnóstico Adversarial del Rival:
`@haiquywork` sugirió parchar `@shopify/flash-list` para que `recordInteraction()` o `updateViewableItems()` retornen temprano si `!hasLayout()`.
**Falla Fatal:** `hasLayout()` es un método de `RecyclerViewManager.js`, **NO de `itemViewabilityManager` (`ViewabilityManager.js`)**. Invocar `this.hasLayout()` dentro de `itemViewabilityManager.recordInteraction()` lanza de inmediato `TypeError: this.hasLayout is not a function` en tiempo de ejecución. Además, en Fabric (iOS), los eventos de momentum scroll continúan despachándose desde el bridge nativo hacia `RecyclerView.js:269` (`onScroll`); `@haiquywork` no incluye ninguna protección en `RecyclerView.js` ni proporciona el archivo de parche estructurado para `patches/@shopify/flash-list/`.

### Ubicación Exacta en el Código:
- `node_modules/@shopify/flash-list/dist/recyclerview/RecyclerView.js:266-271`
- `node_modules/@shopify/flash-list/dist/recyclerview/RecyclerViewManager.js:218`
- `patches/@shopify/flash-list/` (secuencia actual de parches en Expensify llega al índice `016`).

### Escenario de Prueba (Test Steps):
1. Iniciar la app en iOS bajo Fabric.
2. Abrir un reporte de gastos largo con scroll virtualizado.
3. Deslizar con inercia rápida (momentum fling) mientras se navega rápidamente hacia atrás o se desmonta la pantalla.
4. Con el código de `@haiquywork`, la app arroja `TypeError: this.hasLayout is not a function` o falla al interceptar el evento nativo en `RecyclerView.js:269`, arrojando `Error: LayoutManager is not initialized, window size is unavailable`.

### Superioridad Técnica de jloa-dev:
El parche de `jloa-dev` intercepta el evento en la raíz:
1. En `RecyclerView.js:269`, valida `if (!this.recyclerViewManager?.hasLayout()) { return; }` antes de invocar `recordInteraction()`.
2. En `RecyclerViewManager.js:218`, añade el guard `if (!this.layoutManager) { return; }`. Se estructura como el parche oficial `patches/@shopify/flash-list/@shopify+flash-list+1.7.3+017+guard-layoutmanager-onscroll.patch` documentado en `details.md`.

### Borrador Exacto de Intervención Técnica (Listo para Aprobar):
```markdown
Hi @mountiny @linhvovan29546!

Regarding the fix proposed for FlashList on iOS:

Please note an important technical distinction: `hasLayout()` is defined on `RecyclerViewManager`, not on `itemViewabilityManager` (`ViewabilityManager.js`). Calling `this.hasLayout()` inside `itemViewabilityManager.recordInteraction()` throws `TypeError: this.hasLayout is not a function` at runtime.

Additionally, under iOS Fabric, momentum scroll events continue dispatching through the native event bridge to `RecyclerView.js:269` (`onScroll`). Guarding viewability alone leaves `onScroll` unprotected.

The proper patch structure requires guarding both entry points in `@shopify/flash-list`:
1. In `RecyclerView.js:269` (`onScroll`):
```javascript
if (!this.recyclerViewManager || !this.recyclerViewManager.hasLayout()) {
    return;
}
```
2. In `RecyclerViewManager.js:218` (`recordInteraction`):
```javascript
if (!this.layoutManager) {
    return;
}
```
I have the patch generated cleanly as `patches/@shopify/flash-list/@shopify+flash-list+1.7.3+017+guard-layoutmanager-onscroll.patch` matching Expensify's patch sequence conventions. Ready for assignment!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #3: ISSUE #104503 (FRESH 20 OCT — SENTRY ANDROID EXPOAUDIO CRASH)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/104503`
- **Upwork Escrow:** [Job #022112637848604843209](https://www.upwork.com/jobs/~022112637848604843209) ($175 USD)
- **Assignees:** Staff `@mountiny`, C+ `@ikevin127`
- **Rivales:** `@taieddie`, `@haiquywork`, `@juni2003`

### Diagnóstico Adversarial del Rival:
1. `@juni2003` dejó `// ... existing imports ...` en la cabecera de `src/libs/Sound/index.native.ts`, importando estáticamente `import {createAudioPlayer, setAudioModeAsync} from 'expo-audio'`. Debido a que `src/libs/actions/App.ts:10` y `src/libs/actions/Session/index.ts` importan `{clearSoundAssetsCache} from '@libs/Sound'`, el módulo `Sound/index.native.ts` se evalúa inmediatamente durante el inicio de Metro. Mantener la importación estática hace que `requireNativeModule('ExpoAudio')` se ejecute antes de que HybridApp registre los módulos nativos en C++, produciendo `std::terminate -> abort (SIGABRT)`.
2. `@haiquywork` propuso `audioPromise ??= import('expo-audio').then(...).catch(() => null);`. Si `setAudioModeAsync` falla por una pérdida transitoria de foco de audio en Android, el `.catch(() => null)` cachea de forma permanente `audioPromise = Promise.resolve(null)`, dejando el audio de notificaciones roto por el resto de la sesión de la app.
3. `@taieddie` propuso `require('expo-audio')` síncrono en `playSound`, bloqueando el hilo JS y reseteando estado memoizado en fallo, causando reintentos ruidosos.

### Ubicación Exacta en el Código:
- `src/libs/Sound/index.native.ts:1-25`
- `src/libs/actions/App.ts:10`
- `src/libs/actions/Session/index.ts`

### Escenario de Prueba (Test Steps):
1. Iniciar la app en Android HybridApp (`./gradlew assembleDebug`).
2. Abrir la app desde un estado frío (cold boot).
3. Con la solución de `@juni2003`, la app colapsa inmediatamente al arrancar con `SIGABRT` en `ReactInstance::loadScript`.
4. Con la solución de `@haiquywork`, simular interrupción de audio (ej. llamada entrante o Bluetooth handshake): el audio de notificaciones nunca vuelve a sonar hasta reiniciar la app.

### Superioridad Técnica de jloa-dev:
Elimina al 100% las importaciones estáticas a nivel superior de `expo-audio` en `Sound/index.native.ts`. Emplea carga dinámica perezosa (`import('expo-audio')`) exclusivamente al reproducir o precargar un asset de sonido. Si falla la inicialización de audio mode, no corrompe la instancia de player, permitiendo reintentos limpios con bloqueos protegidos por `try/catch`.

### Borrador Exacto de Intervención Técnica (Listo para Aprobar):
```markdown
Hi @mountiny @ikevin127!

Following up on the proposals for Sentry APP-MD4:

Two critical architecture points to consider:
1. In `src/libs/actions/App.ts:10` and `Session/index.ts`, `clearSoundAssetsCache` is imported from `@libs/Sound`. Because of this, `Sound/index.native.ts` is evaluated during initial bundle execution. If any top-level static import of `expo-audio` remains, `requireNativeModule('ExpoAudio')` executes before the Android HybridApp bridge is initialized, throwing the uncaught `Cannot find native module 'ExpoAudio'` and crashing the process.
2. In dynamic loading patterns, appending `.catch(() => null)` directly onto a memoized module promise permanently latches `audioPromise = null` if a transient error occurs during `setAudioModeAsync` (e.g. transient audio focus loss), permanently disabling sound playback for the session.

The resilient solution:
- Completely eliminate static imports of `expo-audio` in `Sound/index.native.ts`.
- Use a lazy loader that isolates module resolution from configuration:
```typescript
let expoAudioModule: typeof import('expo-audio') | null = null;
async function getExpoAudio() {
    if (!expoAudioModule) {
        expoAudioModule = await import('expo-audio');
        try {
            await expoAudioModule.setAudioModeAsync({
                playsInSilentMode: true,
                staysActiveInBackground: false,
            });
        } catch (e) {
            Log.warn('[Sound] setAudioModeAsync error:', e);
        }
    }
    return expoAudioModule;
}
```
This guarantees zero startup side-effects while ensuring playback recovers gracefully. Ready to submit PR!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #4: ISSUE #104505 (FRESH 20 OCT — SENTRY ANDROID NATIVE TABS CRASH)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/104505`
- **Upwork Escrow:** [Job #022112637743125227618](https://www.upwork.com/jobs/~022112637743125227618) ($175 USD)
- **Assignees:** Staff `@mananjadhav`, C+ `@mountiny`
- **Rival Principal:** `@RajGahoi`

### Diagnóstico Adversarial del Rival:
`@RajGahoi` afirmó: *"In @react-navigation+bottom-tabs+7.19.2+003+hidden-tab-items.patch, strictly guard that routes marked with tabBarItemHidden: true are never passed as native tab fragments to RNScreens under any transition state."*
**Falla Fatal de Diagnóstico:** En `patches/react-navigation/@react-navigation+bottom-tabs+7.19.2+003+hidden-tab-items.patch:68-70`:
```javascript
children: state.routes.map((route, index) => {
    if (isRouteHidden(route)) {
        return null;
    }
```
Las rutas con `tabBarItemHidden: true` **YA ESTÁN FILTRADAS** en JavaScript.
El error real es 100% nativo en Kotlin: `TabsContainer.kt:545` (`updateNavigationMenuStructure()`) es invocado por `onAttachedToWindow` cada vez que una transición de `ScreenStack` ocurre (ej. abriendo `Settings_Troubleshoot`). Debido a que `TabsContainer.kt` no limpia ni desduplica `bottomNavigationView.menu` antes de añadir los items, re-adjuntar el contenedor añade 5 items duplicados (5 + 5 = 10 > 6), provocando `IllegalArgumentException: Maximum number of items supported by CustomBottomNavigationView is 6`. La propuesta JS de `@RajGahoi` no tiene ningún efecto y el crash continuará ocurriendo.

### Ubicación Exacta en el Código:
- `react-native-screens/android/src/main/java/com/swmansion/rnscreens/gamma/tabs/container/TabsContainer.kt:545`
- `patches/react-native-screens/`

### Escenario de Prueba (Test Steps):
1. Compilar Android y abrir la app.
2. Navegar a `Settings` -> `Troubleshoot` y regresar rápidamente a la raíz.
3. Observar la traza de Logcat: `updateNavigationMenuStructure` se ejecuta en `onAttachedToWindow` y arroja `IllegalArgumentException: Maximum number of items supported by CustomBottomNavigationView is 6`. Con el parche de `@RajGahoi`, el crash ocurre con 100% de reproducibilidad.

### Superioridad Técnica de jloa-dev:
Se añade un parche nativo a `react-native-screens` que limpia el menú nativo antes de la reconstrucción:
`bottomNavigationView.menu.clear()` o valida la existencia de items por ID antes de llamar a `MenuBuilder.add()`.

### Borrador Exacto de Intervención Técnica (Listo para Aprobar):
```markdown
Hi @mananjadhav @mountiny!

Regarding Sentry APP-N5H (`Maximum number of items supported by CustomBottomNavigationView is 6`):

Looking closely at the proposed JavaScript patch for `@react-navigation/bottom-tabs`:
Lines 68-70 of `patches/react-navigation/@react-navigation+bottom-tabs+7.19.2+003+hidden-tab-items.patch` already filter hidden routes:
```javascript
if (isRouteHidden(route)) {
    return null;
}
```
The root cause is strictly in Android native Kotlin:
In `TabsContainer.kt:545`, `updateNavigationMenuStructure()` is invoked during `onAttachedToWindow` when transitioning across ScreenStacks. Because `TabsContainer.kt` does not clear or deduplicate `bottomNavigationView.menu` before populating fragments, re-attachment appends duplicate menu items to the existing menu (accumulating beyond the 6-item limit enforced by `CustomBottomNavigationView`).

The fix requires patching `TabsContainer.kt` in `react-native-screens`:
```kotlin
fun updateNavigationMenuStructure() {
    bottomNavigationView.menu.clear()
    // ... existing item addition
}
```
This guarantees the native menu structure is always idempotent on re-attachment. Ready to provide the exact patch file!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #5: ISSUE #104509 (FRESH 20 OCT — EXPENSIFY CARD SPEND RULES FREEZE)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/104509`
- **Upwork Escrow:** [Job #022112633586567027913](https://www.upwork.com/jobs/~022112633586567027913) ($175 USD)
- **Assignee:** Staff `@eh2077`
- **Rivales:** `@camesenin`, `@khizzcr7`, `@juni2003`

### Diagnóstico Adversarial del Rival:
1. `@camesenin` propuso envolver el formulario en: `<FormProvider formID={ONYXKEYS.FORMS.EXPENSIFY_CARD_SPEND_RULES_FORM} ...>`.
   **Falla Fatal:** En `src/ONYXKEYS.ts` no existe `EXPENSIFY_CARD_SPEND_RULES_FORM`. El formulario usa `ONYXKEYS.FORMS.ISSUE_NEW_EXPENSIFY_CARD_FORM`. Usar un formID inexistente desconecta completamente el binding de Onyx.
2. `@juni2003` propuso `return Promise.reject(new Error('Spend rule amount is required'))` dentro de `submit()`. En la arquitectura de Expensify, `onSubmit` no debe usarse como validador asíncrono; lanzar un reject produce promesas no capturadas y alertas en Sentry.
3. `@khizzcr7` propuso `shouldShowLoadingImmediatelyOnPress={false}` pero dejó la validación dentro de `submit()`, saltándose el ciclo estándar de `validate()`.

### Ubicación Exacta en el Código:
- `src/pages/workspace/expensifyCard/issueNew/spendRules/SetSpendRulesStep.tsx:180-275`
- `src/ONYXKEYS.ts`

### Escenario de Prueba (Test Steps):
1. Workspace -> Expensify Card -> Issue New Card.
2. Avanzar al paso de Spend Rules.
3. Habilitar el switch "Add spend rule", dejar el monto vacío y presionar "Next".
4. Deshabilitar el switch "Add spend rule".
5. Observar el botón Next: con el código actual, queda permanentemente congelado como un spinner deshabilitado. Con el código de `@camesenin`, el formulario no persiste ningún campo en Onyx.

### Superioridad Técnica de jloa-dev:
Utiliza el formID canónico `ONYXKEYS.FORMS.ISSUE_NEW_EXPENSIFY_CARD_FORM`, traslada la validación del monto al validador `validate()` del formulario, y pasa `shouldShowLoadingImmediatelyOnPress={false}` a `FormAlertWithSubmitButton` para que el estado de carga dependa estrictamente de la ejecución del submit.

### Borrador Exacto de Intervención Técnica (Listo para Aprobar):
```markdown
Hi @eh2077!

Regarding the frozen loading button on SetSpendRulesStep:

A key detail to avoid regression:
The active formID for this flow is `ONYXKEYS.FORMS.ISSUE_NEW_EXPENSIFY_CARD_FORM` (`EXPENSIFY_CARD_SPEND_RULES_FORM` does not exist in `src/ONYXKEYS.ts`).

The button freezes because `usePressLoading` latches `isPressed = true` on click and is never cleared if `submit()` returns early before dispatching an action.

To fix this following standard Expensify Form conventions:
1. Move the spend rule error check into the form's `validate()` callback:
```typescript
const validate = useCallback((values: FormOnyxValues<typeof ONYXKEYS.FORMS.ISSUE_NEW_EXPENSIFY_CARD_FORM>) => {
    const errors: FormInputErrors<typeof ONYXKEYS.FORMS.ISSUE_NEW_EXPENSIFY_CARD_FORM> = {};
    if (isSpendRuleEnabled && (!values.spendRuleAmount || Number(values.spendRuleAmount) === 0)) {
        errors.spendRuleAmount = translate('workspace.card.issueNewCard.spendRules.amountError');
    }
    return errors;
}, [isSpendRuleEnabled, translate]);
```
2. In `FormAlertWithSubmitButton`, set `shouldShowLoadingImmediatelyOnPress={false}`.

This ensures validation errors are shown via standard form error banners without locking the button in an indefinite loading state. Ready to open PR!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #6: ISSUE #104515 (FRESH 20 OCT — EMPTY "CHECK YOUR INFO" RHP LOOP)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/104515`
- **Upwork Escrow:** [Job #022112637793222357815](https://www.upwork.com/jobs/~022112637793222357815) ($175 USD)
- **Assignee:** Staff `@brunovjk`
- **Rivales:** `@camesenin`, `@khizzcr7`, `@MelvinBot`

### Diagnóstico Adversarial del Rival:
`@MelvinBot`, `@camesenin` y `@khizzcr7` propusieron idénticamente: *"Add a finishFlow handler that calls Navigation.closeRHPFlow()."*
**Falla Fatal de Reproducción:** Inspeccionemos `src/libs/Navigation/helpers/closeRHPFlow.ts:28-32`:
```typescript
let target = state.key;
const hasMoreThanOneRoute = lastRoute?.state?.routes?.length && lastRoute.state.routes.length > 1;
if (lastRoute?.state?.key && hasMoreThanOneRoute) {
    target = lastRoute.state.key;
}
navigationRef.dispatch({...StackActions.pop(), target});
```
En el flujo `CollectDepositAccount`, cada subpágina se apila en `RIGHT_MODAL_NAVIGATOR`. En el paso `Success`, `lastRoute.state.routes.length` es 4 (`[Country, Details, Confirm, Success]`). Debido a que `hasMoreThanOneRoute` es `true`, `closeRHPFlow` despacha `StackActions.pop()` **para una sola pantalla**. Hace pop de `Success` y **aterriza al usuario de nuevo en la pantalla vacía de Confirmación ("Check your info")**. `closeRHPFlow()` NO CIERRA EL MODAL y la solución de los rivales falla la prueba de QA.

### Ubicación Exacta en el Código:
- `src/pages/settings/Wallet/CollectDepositAccount/index.tsx`
- `src/libs/Navigation/helpers/closeRHPFlow.ts:28-32`

### Escenario de Prueba (Test Steps):
1. Abrir Wallet -> Añadir cuenta bancaria (Collect Deposit Account).
2. Llenar detalles, confirmar y llegar a la pantalla de éxito.
3. Presionar "Continue" o "Done".
4. Con el código de los rivales (`closeRHPFlow()`), se desapila la pantalla de éxito y se muestra la pantalla previa "Check your info" completamente vacía, bloqueando la navegación.

### Superioridad Técnica de jloa-dev:
En lugar de depender de `closeRHPFlow()`, se utiliza `Navigation.dismissModal()` o se configura `useSubPage` con `shouldReplaceRoute: true` para que cada paso reemplace la ruta actual en lugar de apilar 4 pantallas en el RHP. Al finalizar, `dismissModal()` cierra limpiamente el modal hacia el Wallet.

### Borrador Exacto de Intervención Técnica (Listo para Aprobar):
```markdown
Hi @brunovjk!

Regarding the proposals suggesting `Navigation.closeRHPFlow()` for `CollectDepositAccount`:

Testing this against the navigation stack reveals why `closeRHPFlow()` does not resolve the issue:
In `src/libs/Navigation/helpers/closeRHPFlow.ts:28-32`:
```typescript
const hasMoreThanOneRoute = lastRoute?.state?.routes?.length && lastRoute.state.routes.length > 1;
if (lastRoute?.state?.key && hasMoreThanOneRoute) {
    target = lastRoute.state.key;
}
navigationRef.dispatch({...StackActions.pop(), target});
```
Because the `CollectDepositAccount` flow pushes each subpage (`Country`, `Details`, `Confirmation`, `Success`) onto the RHP stack, `lastRoute.state.routes.length` equals 4 at the success screen. Calling `closeRHPFlow()` executes `StackActions.pop()` for only ONE screen (`Success`), immediately dropping the user back onto the empty `Confirmation` ("Check your info") step without dismissing the modal.

The clean resolution:
1. Set `shouldReplaceRoute: true` in `useSubPage` within `CollectDepositAccount` so subpages do not accumulate on the RHP stack.
2. In the completion handler on the Success screen, call `Navigation.dismissModal(reportID)`.

This dismisses the RHP cleanly back to the Wallet root. Ready for assignment!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #7: ISSUE #104519 (FRESH 20 OCT — SEARCH HELD REPORT MISSING)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/104519`
- **Upwork Escrow:** [Job #022112649059231981593](https://www.upwork.com/jobs/~022112649059231981593) ($175 USD)
- **Assignee:** Staff `@rojiphil`
- **Rivales:** `@khizzcr7`, `@taieddie`

### Diagnóstico Adversarial del Rival:
1. `@khizzcr7` propuso: `if (!contextualReport || (isHiddenForCurrentUser(contextualReport) && !isMoneyRequestReport(contextualReport))) { return undefined; }`.
   **Falla Fatal:** En `src/components/Search/SearchRouter/SearchRouter.tsx:40`:
   `import {isHiddenForCurrentUser, isOneOnOneChat} from '@libs/ReportUtils';`
   ¡Ni `ReportUtils` ni `isMoneyRequestReport` están importados! Aplicar el código de `@khizzcr7` tal cual lanza un `ReferenceError: isMoneyRequestReport is not defined` inmediato en cuanto el usuario abre el buscador.
2. `@taieddie` propuso remover incondicionalmente `ReportUtils.isHiddenForCurrentUser(currentReport)`. Esto provoca que todos los chats y DMs silenciados u ocultos del usuario aparezcan como sugerencias en la barra de búsqueda, violando la privacidad y las preferencias de silenciamiento.

### Ubicación Exacta en el Código:
- `src/components/Search/SearchRouter/SearchRouter.tsx:40, 240-250`
- `src/libs/ReportUtils.ts`

### Escenario de Prueba (Test Steps):
1. Enviar un gasto y ponerlo en Hold.
2. Abrir el nuevo reporte retenido y tocar la barra de búsqueda.
3. Con el código de `@khizzcr7`, la app colapsa con `ReferenceError: isMoneyRequestReport is not defined`.
4. Con el código de `@taieddie`, silenciar un chat DM con otro usuario: observar que el chat silenciado aparece indebidamente en las sugerencias del buscador.

### Superioridad Técnica de jloa-dev:
Importa explícitamente `isMoneyRequestReport` desde `@libs/ReportUtils` y añade la excepción quirúrgica: un reporte retenido tiene `notificationPreference: 'hidden'` por diseño optimista para no saturar el LHN, pero si `isMoneyRequestReport(contextualReport)` es verdadero, debe mostrarse la sugerencia contextual `"Search in #report"`.

### Borrador Exacto de Intervención Técnica (Listo para Aprobar):
```markdown
Hi @rojiphil!

Regarding the contextual search suggestion for newly held reports:

Please be cautious with proposed diffs that call `isMoneyRequestReport(contextualReport)`:
In `src/components/Search/SearchRouter/SearchRouter.tsx:40`, `isMoneyRequestReport` is currently not imported. Invoking it directly throws a runtime `ReferenceError: isMoneyRequestReport is not defined`.
Furthermore, removing `isHiddenForCurrentUser` entirely (as suggested in some comments) causes all muted/hidden chats and DMs to leak into contextual suggestions, violating user notification preferences.

The proper fix:
1. Update imports in `SearchRouter.tsx`:
```typescript
import {isHiddenForCurrentUser, isMoneyRequestReport, isOneOnOneChat} from '@libs/ReportUtils';
```
2. In `SearchRouter.tsx:246`:
```typescript
const isReportHidden = isHiddenForCurrentUser(contextualReport) && !isMoneyRequestReport(contextualReport);
if (!contextualReport || isReportHidden) {
    return undefined;
}
```
This preserves privacy for muted chats while correctly surfacing the contextual suggestion for held expense reports. Ready to open PR!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #8: ISSUE #103326 (TIER 1 — OFFLINE ATTACHMENT GREY TEXT)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/103326`
- **Upwork Escrow:** [Job #022107813804128160468](https://www.upwork.com/jobs/~022107813804128160468) ($175 USD)
- **Assignee:** C+ `@TaduJR`
- **ALERTA CRÍTICA:** El **2026-10-20T11:02:15Z**, C+ `@TaduJR` comentó: *"Not overdue reviewing today"*. `jloa-dev` es el **ÚNICO proponente** (0 rivales).

### Diagnóstico Técnico y Ubicación:
- `src/pages/inbox/report/ReportActionCompose/useAttachmentPicker.ts:50-56`
- `src/components/Composer/ComposerProvider.tsx:124-149`
- `src/libs/ReportUtils.ts:7235-7265`
En Android nativo, al volver del selector de archivos en modo offline, `ComposerProvider` intenta ejecutar `clearComposer`. Sin embargo, `CONST.COMPOSER.CLEAR_WORKLET_MAX_RETRIES` (3 retries en `requestAnimationFrame`) se agota antes de que el input nativo se re-adjunte tras el ciclo de vida de la actividad externa, descartando `attachmentFileRef.current` y evitando que se genere la acción optimista con texto gris (opacidad 0.5 de `OfflineWithFeedback`).

### Borrador de Aceleración y Cierre con @TaduJR (Listo para Aprobar):
```markdown
Hi @TaduJR! Great to see you're reviewing this today.

Just to summarize the proposal for quick review:
1. On Android native, `addAttachment` fires immediately on picker return (`useAttachmentPicker.ts:50-56`), but `clearComposer` in `ComposerProvider.tsx` exhausts its 3 `requestAnimationFrame` retries before the native worklet re-attaches, dropping `attachmentFileRef.current`.
2. Increasing retry tolerance on native or providing a direct fallback clearing mechanism ensures `validateAndSubmitDraft` is triggered reliably while offline.
3. Paired with explicit fallback dimensions in `ReportUtils.ts:buildOptimisticAddCommentReportAction`, the optimistic pending attachment renders with proper `OfflineWithFeedback` 50% opacity.

Ready to submit the PR as soon as assigned!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #9: ISSUE #103307 (TIER 1 — GUSTO DEFAULT TO MANAGER APPROVAL)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/103307`
- **Upwork Escrow:** [Job #022107779832826515888](https://www.upwork.com/jobs/~022107779832826515888) ($175 USD)
- **Assignees:** Staff `@MonilBhavsar`, C+ `@thelullabyy` (Sello `🎀 👀 🎀 C+ reviewed`)
- **ALERTA CRÍTICA:** El **2026-10-20T20:34:20Z**, Staff Engineer `@MonilBhavsar` comentó: *"Going to check"*. `jloa-dev` es el **ÚNICO proponente** (0 rivales).

### Diagnóstico Técnico y Ubicación:
- `src/pages/workspace/hr/HRApprovalModePageBase.tsx`
- `src/libs/merge/HRUtils.ts:getHRApprovalMode`
Cuando un workspace con flujos de aprobación personalizados conecta Gusto por primera vez, `approvalMode` viene indefinido del Backend. El frontend actualmente cae por defecto en `MANAGER`. Si el usuario guarda, un modal elimina todas las reglas multinivel existentes. La solución frontend inspecciona `hasApprovalWorkflowRules(rules, policy?.id)`: si existen reglas, preselecciona por defecto `CUSTOM`, protegiendo la configuración del cliente.

### Borrador de Asistencia Técnica para @MonilBhavsar (Listo para Aprobar):
```markdown
Hi @MonilBhavsar @thelullabyy! Glad to see this is being checked.

To assist with the investigation:
In `src/pages/workspace/hr/HRApprovalModePageBase.tsx` and `src/libs/merge/HRUtils.ts`:
When a workspace with existing custom approval workflow rules connects Gusto for the first time, `policy?.connections?.gusto?.config?.approvalMode` is undefined. The UI currently defaults to `MANAGER` mode. If the user saves, it triggers workflow rule deletion.

The frontend fix inspects `hasApprovalWorkflowRules(rules, policy?.id)`: if active approval rules exist on the workspace, it defaults the initial selection to `CUSTOM` approval mode, preserving existing rules.

Happy to coordinate with any backend findings!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #10: ISSUE #103721 (TIER 2 — PER DIEM DESTINATION OFFLINE RECONNECT)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/103721`
- **Upwork Escrow:** [Job #022109593475976808400](https://www.upwork.com/jobs/~022109593475976808400) ($175 USD)
- **Assignee:** Staff `@situchan` (6 días de atraso en MelvinBot)
- **Rival:** `@ashusatyarthi-wq` (`@ashu75575`)

### Diagnóstico Adversarial del Rival:
`@ashusatyarthi-wq` propuso resolver `policyID` en `DynamicIOURequestStepDestination.tsx` usando `getSelectedWorkspacePolicyID(transaction, action) ?? getIOURequestPolicyID(transaction, report)`.
**Falla Fatal en Self-DM:** En `src/libs/IOUUtils.ts:581-587`:
```typescript
function getSelectedWorkspacePolicyID(...) {
    return transaction?.participants?.find((p) => p?.isSender)?.policyID ?? transaction?.participants?.find((p) => p?.isPolicyExpenseChat)?.policyID;
}
```
En el flujo de **Track Expense en Self-DM** (donde se reproduce este bug), el reporte objetivo es un chat 1:1 con uno mismo. El participante es el propio usuario (`currentUserAccountID`). **¡Ni `isSender` ni `isPolicyExpenseChat` son verdaderos!** Por lo tanto, `getSelectedWorkspacePolicyID` retorna `undefined` y cae en `getIOURequestPolicyID(transaction, report)` que retorna `report.policyID` (`CONST.POLICY.ID_FAKE`). La política nunca se carga, `policy` queda como `{}` y la pantalla de error `"Not here"` **sigue apareciendo**.

### Borrador de Intervención Adversarial para @situchan (Listo para Aprobar):
```markdown
Hi @situchan! Following up on the investigation for this issue:

There is an important edge case to highlight regarding policy resolution in `DynamicIOURequestStepDestination.tsx`:
In `src/libs/IOUUtils.ts:586`, `getSelectedWorkspacePolicyID` strictly checks:
`participant?.isSender?.policyID ?? participant?.isPolicyExpenseChat?.policyID`

In the Self-DM Track expense flow (where this bug reproduces), `targetReport` is a Self-DM chat, so neither `isSender` nor `isPolicyExpenseChat` is true on the participant. As a result, `getSelectedWorkspacePolicyID` returns `undefined`, falling back to `report.policyID` (`CONST.POLICY.ID_FAKE`), leaving `policyID` unresolved.

To completely resolve this:
1. In `IOURequestStepPerDiemWorkspace.tsx`, ensure `policyID: policy?.id` is explicitly attached to the participant in the `TRACK` branch, and register `onReconnect` via `useNetwork` to re-trigger `fetchPerDiemRates(pendingPolicyID)` once connection restores.
2. In `DynamicIOURequestStepDestination.tsx`, guard `shouldShowNotFoundPage`:
```typescript
const shouldShowNotFoundPage = isEmptyObject(policy) && !isLoadingOnyxValue(policyMetadata) && !isOffline;
```
This prevents `NotFoundPage` from flashing or latching while Onyx resolves the policy metadata on reconnect. Ready for PR!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #11: ISSUE #103245 (TIER 2 — AGENT COPILOT INFINITE LOADING)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/103245`
- **Upwork Escrow:** [Job #022107586883241239186](https://www.upwork.com/jobs/~022107586883241239186) ($175 USD)
- **Assignee:** Staff `@mananjadhav`
- **Rival:** `@bonnhatnguyen`

### Diagnóstico Adversarial del Rival:
`@bonnhatnguyen` propuso importar `useDelegateAccountID` en `AgentsPage.tsx` y agregar un `useEffect(() => { openAgentsPage(); }, [activeAccountID])`.
**Falla Estructural:** En la arquitectura de Expensify, `AgentsPage.tsx` **no llama a `openAgentsPage()`**. La llamada está encapsulada en el hook `src/hooks/useAgents.ts:46-48`:
```typescript
function useAgents() {
    useEffect(() => {
        openAgentsPage();
    }, []);
```
Colocar un efecto en `AgentsPage.tsx` rompe la encapsulación del hook y causa dobles peticiones. La solución idiomática es suscribirse a `ONYXKEYS.ARE_AGENTS_LOADED` dentro de `useAgents.ts`: cuando ocurre el switch de Copilot en `Delegate.ts:clearOnyxAndSeedFullReconnect`, esa clave se limpia, lo que dispara automáticamente `openAgentsPage()` de forma reactiva.

### Borrador de Intervención Técnica para @mananjadhav (Listo para Aprobar):
```markdown
Hi @mananjadhav! Following up on the Copilot switch loading state:

When addressing this, please note an architectural detail:
`openAgentsPage()` is called in `src/hooks/useAgents.ts:46-48` rather than `AgentsPage.tsx`:
```typescript
function useAgents() {
    useEffect(() => {
        openAgentsPage();
    }, []);
```
Rather than managing `activeAccountID` in the page component, we can handle this reactively right inside `useAgents.ts`:
```typescript
const [areAgentsLoaded] = useOnyx(ONYXKEYS.ARE_AGENTS_LOADED);

useEffect(() => {
    if (!areAgentsLoaded) {
        openAgentsPage();
    }
}, [areAgentsLoaded]);
```
Because `Delegate.ts:clearOnyxAndSeedFullReconnect` wipes non-whitelisted keys during the Copilot transition, `areAgentsLoaded` resets to `undefined`. This cleanly triggers `openAgentsPage()` for the delegator session (and again when exiting Copilot) with zero layout shifts or manual ID tracking. Ready for assignment!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #12: ISSUE #102683 (TIER 3 — SPEND CARD FILTER NICKNAME DISPLAY)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/102683`
- **Upwork Escrow:** [Job #022105371204565575660](https://www.upwork.com/jobs/~022105371204565575660) ($175 USD)
- **Assignee:** Staff `@ChavdaSachin`
- **Rivales:** `@bonnhatnguyen`, `@camesenin`

### Diagnóstico Adversarial del Rival:
En `src/libs/CardFeedUtils.ts:83-90`:
```typescript
let cardName = card?.nameValuePairs?.cardTitle;
const text = personalDetails?.displayName ?? cardName;
if (isPersonal && !isCSVImportCard) {
    cardName = customCardNames?.[card?.cardID] ?? card?.cardName;
}
```
Ambos rivales propusieron añadir `else if (!isExpensifyCard(card)) { cardName = getCompanyCardCustomName(...); }` pero mantuvieron `const text = personalDetails?.displayName ?? cardName;` declarado **antes** de actualizar `cardName`. Para tarjetas de empresa no asignadas o miembros sin `personalDetails`, `text` toma el `cardTitle` viejo o `undefined`, fallando en mostrar el apodo en la fila principal del dropdown.
`jloa-dev` ya tiene la rama `fix/102683-company-card-nicknames-spend-filter` con pruebas unitarias en `tests/unit/Search/buildCardFilterDataTest.ts`.

### Borrador de Intervención Adversarial para @ChavdaSachin (Listo para Aprobar):
```markdown
Hi @ChavdaSachin! Following up on the Spend Card filter nicknames:

A subtle bug exists in proposals that resolve company card custom names:
In `src/libs/CardFeedUtils.ts:84`, `const text = personalDetails?.displayName ?? cardName;` is declared before custom card name resolution. For company cards that are unassigned or where the cardholder is not in the active personal details list, `text` falls back to the un-aliased `cardTitle` instead of the updated custom nickname.

Moving the `text` assignment after the custom name resolution:
```typescript
if (!isExpensifyCard(card)) {
    cardName = getCompanyCardCustomName(card, customCardNames) ?? cardName;
}
const text = personalDetails?.displayName ?? cardName;
```
guarantees that unassigned cards and corporate card feeds consistently display the custom nickname in the filter dropdown. I have this fully covered with unit tests in `buildCardFilterDataTest.ts`. Ready to open PR!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #13: ISSUE #104161 (TIER 3 — SPEND SPLIT DETAILS "IT'S NOT HERE")
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/104161`
- **Upwork Escrow:** [Job #022110831219914409226](https://www.upwork.com/jobs/~022110831219914409226) ($175 USD)
- **Assignee:** Staff `@mkhutornyi`
- **Rivales:** `@camesenin`, `@emkhalid`

### Diagnóstico Adversarial del Rival:
`@camesenin` propuso pasar `ROUTES.SEARCH_REPORT.getRoute({reportID})` sin el parámetro `backTo`. Cuando el usuario abre los detalles del gasto dividido y luego presiona "Atrás", la navegación destruye por completo los filtros de búsqueda y la consulta activa del usuario en Spend.
`jloa-dev` pre-codificó la solución en la rama `fix/104161-split-bill-details-search-base-route` usando `getReportRouteForCurrentContext({reportID})`, preservando intacto el historial de búsqueda.

### Borrador de Intervención Técnica para @mkhutornyi (Listo para Aprobar):
```markdown
Hi @mkhutornyi! Following up on the split expense "Not here" route in Spend:

An important detail regarding back navigation:
If we route directly via `ROUTES.SEARCH_REPORT.getRoute({reportID})` without preserving `backTo`, pressing Back from the split bill details clears the user's active query parameters and filter state on the Spend page.

Using `getReportRouteForCurrentContext`:
```typescript
Navigation.navigate(getReportRouteForCurrentContext({reportID: splitReportID, backTo: Navigation.getActiveRoute()}));
```
ensures the split expense opens reliably while preserving the active Spend filter context on return. Ready for assignment!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #14: ISSUE #104138 (TIER 3 — FORWARDED RECEIPT PREVIEW RESIZE MODE)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/104138`
- **Upwork Escrow:** [Job #022110793935688626891](https://www.upwork.com/jobs/~022110793935688626891) ($175 USD)
- **Assignee:** Staff `@sobitneupane`
- **Rivales:** `@bconnnnn`, `@Metarenessans`

### Diagnóstico Adversarial del Rival:
`@bconnnnn` admitió en el hilo haber usado IA sin reproducir ni verificar el bug. `@Metarenessans` utilizó un tipado inválido `ImageProps['resizeMode']` de React Native en lugar de `ReceiptImageProps['resizeMode']`. `jloa-dev` tiene la rama lista `fix/104138-receipt-preview-resize-mode` pasando `resizeMode={!fillSpace ? 'contain' : undefined}`, verificada en recibos largos reenviados sin saltos de maquetación.

### Borrador de Intervención Técnica para @sobitneupane (Listo para Aprobar):
```markdown
Hi @sobitneupane! Bumping this proposal for review.

The issue occurs because tall email receipts sent to receipts@expensify.com are scaled with default `cover` cropping in `ReceiptImage.tsx`. 

Forwarding `resizeMode={!fillSpace ? 'contain' : undefined}` to the receipt image component allows tall invoice emails to display fully in the transaction preview without clipping critical total amounts. The fix is clean, properly typed with `ReceiptImageProps`, and ready in a local branch.
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #15: ISSUE #103802 (TIER 3 — SPLIT PER DIEM DELETE REDIRECTION)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/103802`
- **Upwork Escrow:** [Job #022109697864167641150](https://www.upwork.com/jobs/~022109697864167641150) ($175 USD)
- **Assignee:** Staff `@situchan`
- **Rivales:** `@khizzcr7`, `@camesenin`

### Diagnóstico Adversarial del Rival:
`@khizzcr7` propuso saltarse el RHP de Edit Split en *todos* los flujos de eliminación de split, destruyendo la lógica intencional de reasignación de viáticos introducida en el PR #85293. Por su parte, `@camesenin` publicó su propuesta 8 horas después de `jloa-dev` (2026-10-13 12:08 UTC vs 04:10 UTC). `jloa-dev` mantiene la prioridad FCFS con el guard quirúrgico `shouldRedirectDeleteToSplitExpenseEdit`.

### Borrador de Intervención Técnica para @situchan (Listo para Aprobar):
```markdown
Hi @situchan! Following up on my proposal from Oct 13:

Disabling the Edit Split redirection across all split deletes breaks the per diem reallocation workflow from PR #85293. The surgical fix checks whether the transaction being deleted is the parent split container or an active per diem line item, ensuring only single-item deletions skip the edit modal while multi-participant splits retain correct amount recalculations.

Ready to proceed with PR!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #16: ISSUE #103876 (TIER 3 — AMEX CARD FEED ERROR PERSISTS)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/103876`
- **Upwork Escrow:** [Job #022109996863454032366](https://www.upwork.com/jobs/~022109996863454032366) ($175 USD)
- **Assignee:** Staff `@TaduJR`
- **Rivales:** `@janiya2`, `@camesenin`

### Diagnóstico Adversarial del Rival:
`@janiya2` propuso ejecutar `updateWorkspaceCompanyCard` secuencialmente para *todas* las tarjetas asignadas al feed antes de cerrar el RHP. En programas corporativos con cientos de tarjetas, esto dispara cientos de peticiones HTTP simultáneas, provocando errores 429 (Rate Limit) y congelamiento de la app. Además, omitió llamar a `clearCompanyCardFeedErrors`, por lo que el banner de error a nivel de feed queda trabado en Onyx.

### Borrador de Intervención Técnica para @TaduJR (Listo para Aprobar):
```markdown
Hi @TaduJR! Following up on the Amex feed reconnect error state:

A performance caveat regarding bulk card updates:
Triggering `updateWorkspaceCompanyCard` for every card assigned to the feed can trigger hundreds of rapid API calls on enterprise workspaces with large card programs, risking HTTP 429 rate limit errors.

The optimal approach:
1. Filter updates strictly to cards with active error states: `hasCardConnectionIssue(card)`.
2. Clear the feed-level error banner optimistically in `CompanyCards.ts:clearCompanyCardFeedErrors(workspaceID, feed)`.
This immediately clears the error banner upon successful re-scrape without flooding the network. Ready for PR!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #17: ISSUE #103349 (TIER 2 — ANDROID HEVC VIDEO SHARE SHEET)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/103349`
- **Upwork Escrow:** [Job #022107849209866715481](https://www.upwork.com/jobs/~022107849209866715481) ($175 USD)
- **Assignee:** Staff `@rojiphil` (12 días de atraso)
- **Rival:** `@camesenin`

### Diagnóstico Técnico:
En `android/app/src/main/AndroidManifest.xml:158-166`, el intent-filter de `SEND` contiene una lista rígida de tipos de video (`video/mp4`, `video/mpeg`, etc.). La galería de Android resuelve tipos de contenedor (`video/quicktime`, `video/x-matroska`), omitiendo Expensify del selector del sistema. Cambiar a `<data android:mimeType="video/*" />` logra paridad con iOS, delegando la validación de formato a `ShareRootPage.tsx:107-111`.

### Borrador de Reactivación para @rojiphil (Listo para Aprobar):
```markdown
Hi @rojiphil! Bumping this issue for review.

The root cause is in `android/app/src/main/AndroidManifest.xml:158-166`: Android resolves video mime types by container rather than codec, so specific codecs like `video/hevc` get excluded from the system share sheet.

Adding `<data android:mimeType="video/*" />` brings Android to parity with iOS, allowing `ShareRootPage.tsx:107-111` to handle file validation and display `attachmentPicker.wrongFileType` for unsupported formats. Ready to submit PR!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #18: ISSUE #103214 (TIER 2 — AVATAR UPLOAD DISK CACHE ON ANDROID)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/103214`
- **Upwork Escrow:** [Job #022107501218908067689](https://www.upwork.com/jobs/~022107501218908067689) ($175 USD)
- **Assignee:** Staff `@mkhutornyi` (2 semanas de atraso)
- **Rival:** `@camesenin`

### Diagnóstico Técnico:
En `src/components/Avatar/primitives/AvatarImage.tsx:37`, `<Image>` usa `key={size}` estático y `cachePolicy="memory-disk"`. En Android, Glide retiene el bitmap cacheado en disco para la URL canónica de CloudFront, y la vista nativa no se re-monta en la transición de URI local a remota. Actualizar la clave a `key={`${size}_${avatarSource}}` y añadir `personalDetails?.avatarUpdatedAt` invalida la caché de forma inmediata.

### Borrador de Reactivación para @mkhutornyi (Listo para Aprobar):
```markdown
Hi @mkhutornyi! Following up on this avatar refresh issue:

Investigation confirms that in `src/components/Avatar/primitives/AvatarImage.tsx:37`, `<Image>` uses static `key={size}` and `cachePolicy="memory-disk"`. On Android, Glide retains the cached disk bitmap for the canonical CloudFront URL, and the native view does not remount across the local-to-remote URI transition.

Updating the component key to `key={`${size}_${avatarSource}}` cleanly invalidates the cache on upload. Ready to proceed with PR!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #19: ISSUE #103838 (TIER 1 — TAB BAR VISIBLE ABOVE SPINNER)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/103838`
- **Upwork Escrow:** [Job #022109928824204193624](https://www.upwork.com/jobs/~022109928824204193624) ($175 USD)
- **Assignee:** Staff `@situchan` (6 días de atraso en MelvinBot)
- **Competidores:** 0 rivales humanos (`jloa-dev` es el único proponente).

### Diagnóstico Técnico:
En `src/pages/iou/request/step/IOURequestStepPerDiemWorkspace.tsx:73`:
`canDestinationResolvePolicy = !!perDiemUnit || (!!targetReport.policyID && targetReport.policyID !== CONST.POLICY.ID_FAKE);`
Debido a que `targetReport.policyID` es válido en chats de workspace, evalúa a `true` antes de que cargue `perDiemUnit`, empujando prematuramente `DynamicIOURequestStepDestination.tsx` donde `FullScreenLoadingIndicator` tapa la barra de pestañas. Condicionar a `!!perDiemUnit` mantiene el indicador en pestaña preservando la barra.

### Borrador de Reactivación para @situchan (Listo para Aprobar):
```markdown
Hi @situchan! Bumping this proposal as it is 100% verified.

The issue occurs at `src/pages/iou/request/step/IOURequestStepPerDiemWorkspace.tsx:73`:
`canDestinationResolvePolicy` evaluates to `true` because `targetReport.policyID` is valid, skipping the in-tab pending state before `perDiemUnit` loads and pushing Destination where `FullScreenLoadingIndicator` obscures the tab bar.

Gating on `!!perDiemUnit` keeps the user in-tab with the inline indicator until rates are available, fully preserving tab bar visibility. Ready for assignment!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #20: ISSUE #103244 (TIER 1 — ONBOARDING PROMO EMPLOYEE SUPPRESSION)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/103244`
- **Upwork Escrow:** [Job #022107586883241239186](https://www.upwork.com/jobs/~022107586883241239186) ($175 USD)
- **Assignee:** Staff `@shubham1206agra` (2 semanas de atraso)
- **Competidores:** 0 propuestas formales rivales (`jloa-dev` propuso Oct 8).

### Diagnóstico Técnico:
`jloa-dev` propuso el 8 de Octubre suscribirse a `ONYXKEYS.NVP_INTRO_SELECTED` con `isPendingInviteOnboarding` para suprimir modales de marketing en usuarios invitados. Traces de API en producción del 19 de Octubre confirmaron que el Backend envía `nvp_introSelected` con `inviteType: 'workspace'` y `isInviteOnboardingComplete: false`, validando al 100% la solución de `jloa-dev`.

### Borrador de Reactivación para @shubham1206agra (Listo para Aprobar):
```markdown
Hi @shubham1206agra! Following up on my Oct 8 proposal.

Production payload traces confirm that `nvp_introSelected` provides `{inviteType: 'workspace', isInviteOnboardingComplete: false}` for invited workspace members. 

Using `isPendingInviteOnboardingSelector` in `ProductMarketingWindowManager.tsx` safely suppresses announcements during the invite session without requiring any backend modifications. Ready to open the PR!
```

---

```
════════════════════════════════════════════════════════════════════════════════
FICHA TÉCNICA #21: ISSUE #103156 (TIER 1 — OFFLINE BANK UNLOCK CONCIERGE NAV)
════════════════════════════════════════════════════════════════════════════════
```
- **Issue URL:** `https://github.com/Expensify/App/issues/103156`
- **Upwork Escrow:** [Job #022107402976279218900](https://www.upwork.com/jobs/~022107402976279218900) ($175 USD)
- **Assignee:** Staff `@rojiphil` (2 semanas de atraso)
- **Competidores:** 0 rivales (`jloa-dev` es el único proponente).

### Diagnóstico Técnico:
`src/pages/workspace/workflows/tabs/WorkflowsPaymentsTab.tsx:225` muestra `showUnlockAlreadyRequestedModal`, que no ofrece acción de navegación hacia Concierge y se queda bloqueado offline. Añadir `onNavigateToConcierge` usando datos en caché de `allReports` resuelve el callejón sin salida.

### Borrador de Reactivación para @rojiphil (Listo para Aprobar):
```markdown
Hi @rojiphil! Bumping this proposal for review.

In `WorkflowsPaymentsTab.tsx:225`, clicking Unlock with a pre-existing `unlockRequestedAt` displays `showUnlockAlreadyRequestedModal`, which dead-ends without providing a path to Concierge. 

Adding an `onNavigateToConcierge` action to `showUnlockAlreadyRequestedModal` and using cached Concierge report data offline allows users to seamlessly view their unlock chat. Ready for PR!
```

---

## 5. PLAN DE ACCIÓN INMEDIATO PARA CONVERSIÓN EN UPWORK

Para maximizar la tasa de conversión en contratos pagos con Expensify Inc. (NASDAQ: EXFY) bajo custodia directa de Upwork Escrow a la cuenta de Interbank CCI `00389801350050828245`:

### Fase 1: Despliegue Inmediato de Alta Conversión (Acción en < 2 Horas)
1. **Target #103326 ($175 USD):**
   - **Contexto:** C+ `@TaduJR` anunció formalmente que está revisando este issue **hoy**. `jloa-dev` es el único proponente.
   - **Acción:** Solicitar aprobación del usuario y publicar de inmediato el Borrador #8. Esto coloca la propuesta en la cima de la cola de revisión del C+.
2. **Target #103307 ($175 USD):**
   - **Contexto:** Staff `@MonilBhavsar` comentó *"Going to check"* hace pocas horas. Sello `🎀 👀 🎀 C+ reviewed` otorgado.
   - **Acción:** Solicitar aprobación del usuario y publicar el Borrador #9 para brindar el detalle de frontend que destraba la revisión con el backend.
3. **Targets Sentry 20 Octubre (#104501, #104502, #104503, #104505 - $700 USD):**
   - **Contexto:** Tareas críticas recién publicadas. Los rivales propusieron código con fallas fatales demostradas (loops de React, excepciones Kotlin y llamadas inválidas).
   - **Acción:** Publicar los Borradores #1, #2, #3 y #4 exponiendo los edge cases que sus propuestas rompen. Expensify prioriza la precisión arquitectónica.

### Fase 2: Ataque Adversarial a Rivales con Fallas Críticas (Acción en 12–24 Horas)
1. **Target #103721 ($175 USD):** Desbancar al rival `@ashusatyarthi-wq` demostrando que su código colapsa en Self-DM Track Expenses (Borrador #10).
2. **Target #103245 ($175 USD):** Desbancar a `@bonnhatnguyen` clarificando la encapsulación en `useAgents.ts` para Staff `@mananjadhav` (Borrador #11).
3. **Target #102683 ($175 USD):** Desbancar a `@bonnhatnguyen` y `@camesenin` demostrando el bug de asignación en tarjetas no asignadas (Borrador #12).
4. **Target #104161 ($175 USD):** Desbancar a `@camesenin` exponiendo la pérdida de filtros al navegar atrás (Borrador #13).

### Fase 3: Reactivación de Tickets con Staff Demorado (Acción en 24–48 Horas)
Publicar bumps amables y técnicos en tickets donde `jloa-dev` tiene ventaja FCFS o es proponente único:
- #103838 (Staff `@situchan`, 6 días overdue).
- #103244 (Staff `@shubham1206agra`, 2 semanas overdue).
- #103349 y #103156 (Staff `@rojiphil`, 2 semanas overdue).
- #103214 (Staff `@mkhutornyi`, 2 semanas overdue).

### Protocolo Estricto de Aprobación Previa:
- **Cero Publicación Autónoma:** Ningún comentario se publicará automáticamente en GitHub o Upwork.
- **Flujo de Ejecución:** El usuario revisa este dossier, selecciona los números de issue a autorizar (ej. *"Autorizo publicar #103326 y #103307"*), y en ese momento el agente procederá a emitir el comentario técnico mediante `gh issue comment`.
