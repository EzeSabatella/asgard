# SUPERAGENTE Database Schemas

This document defines the proposed schemas for the various storage layers used in the project.

## 1. Raw Stores (SQLite + SQLCipher)

We maintain separate stores for technical and emotional events to ensure physical separation of data.

### Technical Raw Store (`raw_technical.db`)

```sql
CREATE TABLE technical_events (
    id TEXT PRIMARY KEY,
    ts DATETIME DEFAULT CURRENT_TIMESTAMP,
    type TEXT CHECK(type IN ('DECISION', 'PREFERENCE', 'INSIGHT', 'PROJECT_UPDATE', 'BLOCKER', 'MILESTONE')),
    project TEXT,
    content TEXT,
    rationale TEXT,
    source TEXT DEFAULT 'conversation',
    consolidated BOOLEAN DEFAULT 0,
    tags TEXT, -- JSON string or comma-separated
    metadata TEXT -- JSON string
);

CREATE INDEX idx_tech_ts ON technical_events(ts);
CREATE INDEX idx_tech_project ON technical_events(project);
CREATE INDEX idx_tech_consolidated ON technical_events(consolidated);
```

### Emotional Raw Store (`raw_emotional.db`)

```sql
CREATE TABLE emotional_events (
    id TEXT PRIMARY KEY,
    ts DATETIME DEFAULT CURRENT_TIMESTAMP,
    type TEXT CHECK(type IN ('EMOTIONAL_SIGNAL', 'RELATIONAL_PATTERN', 'SUPPORT_OUTCOME', 'HUMOR_SIGNAL', 'BOND_REINFORCEMENT')),
    signal TEXT,
    trigger TEXT,
    intensity REAL,
    context TEXT,
    source TEXT DEFAULT 'conversation',
    consolidated BOOLEAN DEFAULT 0,
    metadata TEXT -- JSON string
);

CREATE INDEX idx_emot_ts ON emotional_events(ts);
CREATE INDEX idx_emot_consolidated ON emotional_events(consolidated);
```

### Co-activation Patterns Store (`patterns.db`)

```sql
CREATE TABLE co_activations (
    id TEXT PRIMARY KEY,
    ts_start DATETIME,
    ts_end DATETIME,
    observer_pair TEXT, -- e.g., "Technical|Humor"
    count INTEGER DEFAULT 1,
    last_detected DATETIME
);
```

## 2. Knowledge Graph (Neo4j)

The knowledge graph captures relationships between concepts, projects, and decisions across different contexts.

### Node Labels
- `User`
- `Project`
- `Concept`
- `Decision`
- `Technology` (Stack)
- `Insight`

### Relationships
- `(User)-[:WORKS_ON]->(Project)`
- `(Project)-[:USES]->(Technology)`
- `(Decision)-[:AFFECTS]->(Project)`
- `(Concept)-[:IS_ISOMORPHIC_TO]->(Concept)`
- `(Insight)-[:RELATES_TO]->(Concept)`

### Initial Schema Setup (Cypher)

```cypher
// Constraints
CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE;
CREATE CONSTRAINT project_name IF NOT EXISTS FOR (p:Project) REQUIRE p.name IS UNIQUE;
CREATE CONSTRAINT concept_name IF NOT EXISTS FOR (c:Concept) REQUIRE c.name IS UNIQUE;

// Initial User
MERGE (u:User {id: 'lexa', name: 'Ezequiel Sabatella'});
```

## 3. Inferred Store (ChromaDB)

ChromaDB is used for vector search of "memories".

### Collection: `user_memories`
- **ID**: Event ID or Memory ID
- **Document**: The text content of the memory
- **Metadata**:
    - `type`: `technical` | `emotional` | `insight`
    - `project`: Project name
    - `ts`: Timestamp
    - `relevance`: Score
