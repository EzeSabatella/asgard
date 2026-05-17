# CURRENT_CONTEXT — Asgard

_Última actualización: 2026-05-17_

> Este archivo es el punto de entrada para cualquier LLM que trabaje en este proyecto.
> Leer este archivo + CLAUDE.md es suficiente para tener contexto completo.

---

## Qué estamos construyendo

**Asgard** es el chassis de identidad digital persistente de Hugmun IA. Observa las conversaciones del usuario con cualquier LLM, extrae eventos significativos, construye un perfil acumulativo y lo devuelve como contexto enriquecido. El activo es el conocimiento acumulado — no el modelo.

La metáfora: Pepe el Grillo. Siempre presente, sin agenda propia, que acompaña, cuida y ayuda a crecer.

Más detalle: [SUPERAGENT.md](SUPERAGENT.md)

---

## Estado actual

**Fase 0 completada.** El MVP está funcional con 22/22 tests pasando.

El paso inmediato es infraestructura de deploy: Git + GitHub + primer push + clone en servidor.

Ver estado detallado: [STATUS.md](STATUS.md)

---

## Stack técnico

- **Lenguaje:** Python 3.11+
- **Framework:** FastAPI + Pydantic v2
- **Storage:** SQLite (aiosqlite) + ChromaDB + Neo4j
- **Embeddings:** OpenAI (interfaz abstracta, switcheable a Ollama)
- **Config:** `chassis.config.yaml`
- **Infra:** Docker Compose
- **Servidor local:** `antigravity` — 192.168.1.43 / Tailscale 100.76.101.123

---

## Decisiones ya tomadas

Las decisiones arquitectónicas vigentes están en [CLAUDE.md](CLAUDE.md) — sección "Decisiones arquitectónicas vigentes". No se re-discuten sin escalado a Ezequiel.

El log completo está en [docs/20260503-1800_DECISION_decisions-log-sesion-01.md](docs/20260503-1800_DECISION_decisions-log-sesion-01.md).

---

## Estructura del repo

```
chassis/          ← código fuente del MVP
  models/         ← BaseProfile, PersonalProfile, EnterpriseProfile
  observers/      ← ConversationObserver, TechnicalObserver
  stores/         ← BaseStore, RawStore (SQLite)
  embeddings/     ← interfaz abstracta + proveedor OpenAI
  classifier/     ← clasificador heurístico
  api/            ← FastAPI REST + MCP skeleton
  config.py       ← carga de chassis.config.yaml
docs/             ← toda la documentación del proyecto (briefs, auditorías, decisiones)
.agents/skills/   ← skills de Gemini
.claude/skills/   ← skills de Claude
```

---

## Roles de IA en este proyecto

| Modelo | Rol |
|---|---|
| **Claude** | Arquitecto / Auditor / Lead Developer |
| **Gemini** | Ejecutor (implementa según briefs de Claude) |
| **Ezequiel** | Owner / Product |

Workflow detallado: [CLAUDE.md](CLAUDE.md) — sección "Workflow estándar".

---

## Próxima tarea concreta

1. Instalar Git en la laptop
2. Crear repo privado `asgard` en GitHub (cuenta: eze.datascientist@gmail.com)
3. `git config --global user.name "Ezequiel Sabatella"`
4. `git config --global user.email "eze.datascientist@gmail.com"`
5. `git init` + `git add .` + primer commit + `git remote add origin <url>` + `git push`

---

## Qué NO hacer todavía

- No implementar Fase 1 antes de tener el deploy funcionando
- No abrir observadores emocionales, consolidador LLM ni Neo4j alimentado
- No modificar interfaces abstractas existentes sin autorización de Ezequiel

---

## Documentación relevante

| Archivo | Contenido |
|---|---|
| [SUPERAGENT.md](SUPERAGENT.md) | Visión completa, arquitectura, fases |
| [CLAUDE.md](CLAUDE.md) | Manual de operación, roles, decisiones vigentes |
| [STATUS.md](STATUS.md) | Estado actual detallado |
| [TASKS.md](TASKS.md) | Backlog operativo |
| [docs/INDEX.md](docs/INDEX.md) | Índice de toda la documentación |
