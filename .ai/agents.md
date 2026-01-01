# AI Agent Instructions - Edinburgh Finds

**For AI Assistants:** This file contains universal instructions for working with the Edinburgh Finds codebase. It applies to all AI providers (Claude, GPT-4, Gemini, etc.).

**Claude Code users:** See [`.ai/claude.md`](.ai/claude.md) for Claude-specific tool usage and autonomous workflows.

---

## 🔍 MANDATORY: Live Internet Research Protocol

**Context**: This codebase uses rapidly-evolving web technologies where best practices, APIs, and security patches change frequently. Relying solely on training data will lead to outdated, insecure, or broken code.

### When You MUST Search the Internet Before Coding

1. **Version-Specific Syntax**
   - Package installation commands (flags and options change)
   - Configuration file formats (major version migrations)
   - Framework API calls (breaking changes between versions)
   - Import statements (package structure reorganization)

2. **Security-Critical Operations**
   - Authentication/authorization patterns
   - Database connection pooling
   - Environment variable handling
   - API key management
   - Input validation and sanitization

3. **Breaking Changes & Migrations**
   - Major version upgrades (e.g., Prisma 6 → 7, Next.js 15 → 16)
   - Deprecated APIs (removed in recent versions)
   - Migration guides (official upgrade paths)

4. **Dependencies Released After Your Training Cutoff**
   - Any package released after your knowledge cutoff date
   - Newly added dependencies in `package.json` or `requirements.txt`
   - Beta/RC versions of stable packages

### How to Verify Current Best Practices

**Search query pattern:**
```
[framework/library] [exact version] [specific feature] official documentation [current year]

Examples:
- "Prisma 7.1.0 PostgreSQL adapter setup official documentation 2025"
- "Next.js 16.0.7 server components caching 2025"
- "SQLModel 0.0.27 async PostgreSQL best practices 2025"
```

**Check sources in this order:**
1. **Official documentation** (e.g., nextjs.org/docs, prisma.io/docs, sqlmodel.tiangolo.com)
2. **Security advisories** (CVE databases, GitHub security tabs, framework changelogs)
3. **Migration guides** (official upgrade documentation for version changes)
4. **Local project files** (for project-specific patterns like confidence tracking)

### Red Flags That Require Immediate Research

- ⚠️ "I remember this API from my training..." → **STOP, search first**
- ⚠️ User's package version differs significantly from what you'd suggest → **Research the actual version**
- ⚠️ Security-related task (auth, database, secrets, file uploads) → **Search for current CVE and best practices**
- ⚠️ Major framework version (Next.js 15+, React 19+, Prisma 7+) → **APIs likely changed significantly**
- ⚠️ Configuration file syntax differs from your memory → **Verify with official docs**

### Checking Current Versions in This Project

**Frontend (JavaScript/TypeScript):**
```bash
# Check exact versions
cat edinburgh_finds_web/package.json
```

**Backend (Python):**
```bash
# Check pinned versions
cat edinburgh_finds_backend/requirements.txt
```

**Always verify syntax against the EXACT version listed in these files.**

---

## Repository Overview

**Edinburgh Finds** is a monorepo for a curated directory of niche activities and venues in Edinburgh, Scotland.

### Architecture Pattern: Database-Centric Integration

```
┌─────────────────────────┐
│ Backend (Python CLI)    │
│ - LLM data extraction   │
│ - SQLModel writes       │
└──────────┬──────────────┘
           │
           ▼
    ┌─────────────┐
    │ PostgreSQL  │ ← Shared database (single source of truth)
    └─────────────┘
           ▲
           │
┌──────────┴──────────────┐
│ Frontend (Next.js 16)   │
│ - Public web app        │
│ - Prisma reads          │
└─────────────────────────┘
```

**Critical Design Decision:** No REST API between backend and frontend.
- Backend: Writes using SQLModel/SQLAlchemy
- Frontend: Reads using Prisma ORM
- **Risk**: Schema drift - changes to Python models must be manually synced to Prisma schema

### Architecture Review & Future Direction

**⚠️ IMPORTANT:** This architecture has known limitations documented in [`.ai/context/architecture-review.md`](.ai/context/architecture-review.md).

**Current State vs. Planned Improvements:**

| Current Pattern (Avoid Perpetuating) | Planned Improvement | When Suggesting Changes |
|---------------------------------------|---------------------|-------------------------|
| Frontend queries database directly | Add API layer (FastAPI) | Prepare for future API: avoid tight coupling to Prisma queries |
| Load ALL listings (no pagination) | Cursor-based pagination | Always add `take` limits to new queries |
| No caching layer | Redis/CDN caching via API | Design data structures with cacheability in mind |
| Manual schema sync (Prisma db pull) | Automated CI/CD validation | Document schema changes clearly for automation |
| Sequential LLM processing | Queue-based batch processing | Design extraction functions to be stateless/parallelizable |
| Local file logging | Centralized structured logging | Use proper logging, avoid ad-hoc file writes |

**🎯 When Making Changes:**
- **Don't** add more direct database queries in frontend components
- **Do** prepare for API layer by keeping data fetching isolated
- **Don't** create unbounded queries (always paginate)
- **Do** add database indexes when adding new query patterns
- **Don't** hardcode configuration or secrets
- **Do** externalize configuration for future deployment flexibility

**Read the full architecture review before:**
- Adding new features that involve data fetching
- Suggesting performance optimizations
- Proposing scalability improvements
- Making security-related changes

---

## Technology Stack

### Frontend (`edinburgh_finds_web/`)

| Technology | Version | Purpose | Critical Notes |
|------------|---------|---------|----------------|
| Next.js | 16.0.7 | App Router framework | **Security**: Upgrade to 16.0.10+ ([CVE advisory](https://nextjs.org/blog/security-update-2025-12-11)) |
| React | 19.2.0 | UI library | **Security**: Upgrade to 19.2.3+ ([DoS vulnerability](https://react.dev/blog/2025/12/11/denial-of-service-and-source-code-exposure-in-react-server-components)) |
| Prisma | 7.1.0 | ORM | **Breaking**: Driver adapters mandatory in v7 |
| Tailwind CSS | 4.x | Styling | **Breaking**: Config moved from JS to CSS |
| TypeScript | 5.x | Type safety | Strict mode enabled |

### Backend (`edinburgh_finds_backend/`)

| Technology | Version | Purpose | Critical Notes |
|------------|---------|---------|----------------|
| Python | 3.11+ | Runtime | Async-capable |
| SQLModel | 0.0.27 | ORM | Dual Pydantic + SQLAlchemy |
| Instructor | 1.13.0 | LLM extraction | Structured outputs |
| Anthropic | 0.75.0 | Claude API | Primary LLM provider |
| Pydantic | 2.11.10 | Validation | **CRITICAL**: Must stay `<2.12` ([SQLModel incompatibility](https://github.com/fastapi/sqlmodel/issues/1623)) |
| PostgreSQL | - | Database | Shared with frontend |

### Supporting Services

- **google-genai** (1.23.0) - Gemini API support
- **openai** (2.8.1) - OpenAI API support
- **tavily-python** (0.7.12) - Web search API
- **phonenumbers** (9.0.18) - Phone validation/normalization

---

## Development Commands

### Backend Setup & Usage

```bash
# Activate virtual environment (adjust path as needed)
# Example: source venv/bin/activate or C:\path\to\venv\Scripts\activate

cd edinburgh_finds_backend

# Install dependencies (first time only)
pip install -r requirements.txt

# Initialize database tables
python scripts/create_tables.py

# Run extraction pipeline (primary workflow)
python main.py --entity-name "David Lloyd Edinburgh Shawfair" --entity-type venue

# With manual text file input
python main.py --entity-name "Venue Name" --entity-type venue --file data/venues/slug/raw/input.txt
```

### Frontend Setup & Usage

```bash
cd edinburgh_finds_web

# Install dependencies
npm install

# Generate Prisma client (REQUIRED after schema changes)
npx prisma generate

# Development server
npm run dev  # http://localhost:3000

# Production build
npm run build
npm run start

# Linting
npm run lint

# Database GUI (browse data)
npx prisma studio
```

### Critical Cross-Repo Workflow: Schema Synchronization

**⚠️ MOST IMPORTANT WORKFLOW** - Schema drift will break production.

```bash
# 1. Modify backend SQLModel definitions
# Edit: edinburgh_finds_backend/database/models.py

# 2. Apply backend schema changes to PostgreSQL
cd edinburgh_finds_backend
python scripts/create_tables.py

# 3. Introspect database to update Prisma schema
cd ../edinburgh_finds_web
npx prisma db pull  # Auto-updates prisma/schema.prisma

# 4. Regenerate TypeScript types
npx prisma generate  # Updates app/generated/prisma/

# 5. Verify no breaking changes in frontend code
npm run build
```

**Why this exists**: Backend SQLModel is the single source of truth. Prisma schema is derived from the live database, not manually written.

---

## Core Architecture Patterns

### Data Flow: Raw Text → Database → Web UI

```
Raw Text Input (Firecrawl/Tavily/Manual)
    ↓
extraction_pipeline.py (generates LLM prompt)
    ↓
Instructor + Claude API (extracts structured VenueSchema)
    ↓
upsert_entity.py (confidence-based merge)
    ↓
PostgreSQL (listings + venues tables)
    ↓
Prisma Client (type-safe queries)
    ↓
Next.js Server Components (SSR)
    ↓
User's Browser
```

### Confidence Tracking System

**Purpose**: Prevent low-quality re-scrapes from overwriting good data.

**Storage**: `field_confidence` JSONB column on all tables (0.0 to 1.0 scale)

**Update Logic** ([services/upsert_entity.py:32-60](edinburgh_finds_backend/services/upsert_entity.py)):
```python
CHANGE_MIN_CONF = 0.7  # Minimum confidence to overwrite existing value

if new_value == old_value:
    # Value unchanged - keep highest confidence
    field_confidence[field] = max(old_conf, new_conf)
elif new_conf >= CHANGE_MIN_CONF or new_conf > old_conf:
    # Value changed - update if confident enough
    setattr(obj, field, new_value)
    field_confidence[field] = new_conf
# Otherwise: reject update (too uncertain)
```

**Use Cases**:
- Multiple extractions from different sources
- Incremental data quality improvements
- Hallucination prevention

### Entity Type System

Supports multiple entity types (currently: `venue`; future: `retailer`, `club`, `coach`).

**Adding a new entity type requires changes to:**

**Backend:**
1. `database/models.py` - Add SQLModel table class
2. `schemas/[type]_extraction_schema.py` - Create Pydantic schema
3. `core/entity_registry.py` - Register type mapping
4. `main.py` - Add to CLI `--entity-type` choices

**Frontend:**
1. `app/config/categories.ts` - Add entity config to categories
2. `app/components/[Type]Card.tsx` - Create card component
3. `app/category/[slug]/page.tsx` - Add switch case for rendering

### Category Mapping: Raw → Canonical

**Flow**: LLM outputs free-form categories → `map_categories()` → normalized taxonomy

**Example**:
```python
# LLM output
categories = ["paddle tennis", "5-a-side football", "spa retreat"]

# After mapping (utils/category_mapping.py)
canonical_categories = ["padel", "football", "spa"]
```

**Adding new categories**:

1. Backend ([utils/category_mapping.py](edinburgh_finds_backend/utils/category_mapping.py)):
   ```python
   CANONICAL_CATEGORIES = {
       "padel", "tennis", "climbing",  # Add new canonical name
   }

   CATEGORY_SYNONYMS = {
       "bouldering": "climbing",  # Map synonyms
       "rock climbing": "climbing",
   }
   ```

2. Frontend ([app/config/categories.ts](edinburgh_finds_web/app/config/categories.ts)):
   ```typescript
   climbing: {  // Must match canonical name exactly
       name: "Climbing",
       image: "/images/categories/climbing.jpg",
       isLive: true,
       venue: {
           summaryField: 'climbing_summary',
           cardFields: [{ field: 'climbing_walls', suffix: 'walls' }]
       }
   }
   ```

3. Add category image: `public/images/categories/climbing.jpg`

### Dynamic Schema Generation

Backend combines multiple SQLModel classes into a single Pydantic schema for LLM extraction:

```python
# utils/model_conversion.py
def to_pydantic_model(sqlmodels: list[type[SQLModel]]) -> type:
    """Combine Listing + Venue, strip SQLAlchemy metadata."""
    fields = {}
    for cls in sqlmodels:
        for name, field in cls.model_fields.items():
            if not getattr(field, "exclude", False):  # Respect exclude=True
                fields[name] = (field.annotation, field.default)
    return create_model("VenueSchema", **fields)

# schemas/venue_extraction_schema.py
VenueSchema = to_pydantic_model([Listing, Venue])
```

**Benefits**:
- Single source of truth (database models)
- Auto-updates when models change
- Type safety for LLM validation
- Excludes internal fields (IDs, timestamps)

### File Organization for Extracted Data

```
data/
└── venues/                        # Entity type (plural)
    └── david_lloyd_shawfair/      # Slug (normalized entity_name)
        ├── raw/                   # Debug: raw text inputs (timestamped)
        ├── extract/               # Reserved for future use
        └── processed/             # Final JSON output (timestamped)
```

**Created automatically by** `extraction_pipeline.py:get_entity_dirs()`

**Purpose**:
- Reproducibility (re-run extractions on saved raw text)
- Debugging LLM hallucinations
- Audit trail for data quality

---

## Environment Variables

### Backend `.env`
```bash
# Database (must match frontend)
DATABASE_URL=postgresql://user:pass@host:5432/edinburgh_finds

# LLM Configuration
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4-5-20250929

# Data Sources (optional)
FIRECRAWL_API_KEY=fc-...
TAVILY_API_KEY=tvly-...
```

### Frontend `.env`
```bash
# Database (must match backend)
DATABASE_URL=postgresql://user:pass@host:5432/edinburgh_finds

# Public variables (exposed to browser)
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Security Notes**:
- Never commit `.env` files to git
- Use different databases for dev/staging/prod
- Rotate API keys regularly
- Use managed secrets in production (Vercel, AWS Secrets Manager, etc.)

---

## Critical Files Reference

### Backend Core Files

| File | Purpose | Key Patterns |
|------|---------|--------------|
| `services/extraction_pipeline.py` | Main extraction orchestration | LLM prompting, file management, upsert coordination |
| `services/upsert_entity.py` | Confidence-based persistence | Field-level conflict resolution (>= 0.7 threshold) |
| `database/models.py` | SQLModel table definitions | Dual Pydantic+SQLAlchemy models, `exclude=True` pattern |
| `core/entity_registry.py` | Entity type registration | Maps entity types to schemas/tables |
| `utils/category_mapping.py` | Category normalization | Raw LLM output → canonical taxonomy |
| `utils/model_conversion.py` | Dynamic Pydantic schema generation | Combines SQLModel classes, strips DB metadata |
| `config/settings.py` | Environment configuration | Pydantic Settings for .env loading |

### Frontend Core Files

| File | Purpose | Key Patterns |
|------|---------|--------------|
| `app/config/categories.ts` | Category definitions | Drives navigation, rendering, field mapping |
| `lib/prisma.ts` | Database client singleton | PrismaPg adapter, connection pooling |
| `app/category/[slug]/page.tsx` | Category listing page | Prisma queries with `canonical_categories` filter |
| `app/listing/[slug]/page.tsx` | Venue detail page | Joined queries with `include: { venues: true }` |
| `app/components/VenueCard.tsx` | Venue card component | Dynamic field rendering via category config |
| `prisma/schema.prisma` | Database schema (read-only) | Auto-generated via `prisma db pull` |

---

## Common Workflows

### Add a New Venue

```bash
# Extract data
cd edinburgh_finds_backend
python main.py --entity-name "The Climbing Academy" --entity-type venue

# Verify output
cat data/venues/the_climbing_academy/processed/*.json

# Check in database
cd ../edinburgh_finds_web
npx prisma studio

# View in frontend
npm run dev
# Visit: http://localhost:3000/category/climbing
```

### Extend Database Schema

**Example: Add `climbing_walls` field to Venue table**

```python
# 1. Update model: edinburgh_finds_backend/database/models.py
class Venue(SQLModel, table=True):
    # ... existing fields ...
    climbing_walls: Optional[int] = Field(
        None,
        description="Number of climbing walls available"
    )
```

```bash
# 2. Apply to database
cd edinburgh_finds_backend
python scripts/create_tables.py

# 3. Sync Prisma schema
cd ../edinburgh_finds_web
npx prisma db pull
npx prisma generate

# 4. Re-extract venues to populate new field
cd ../edinburgh_finds_backend
python main.py --entity-name "The Climbing Academy" --entity-type venue

# 5. Use in frontend
cd ../edinburgh_finds_web
npm run dev
```

### Debug LLM Extraction Issues

```bash
# 1. Check raw input
cat data/venues/venue_slug/raw/*.txt

# 2. View processed output
cat data/venues/venue_slug/processed/*.json

# 3. Check field confidence scores
cat data/venues/venue_slug/processed/*.json | jq '.listing.field_confidence'

# 4. Re-run with different LLM
# Edit: edinburgh_finds_backend/.env
LLM_PROVIDER=gemini  # or openai
LLM_MODEL=gemini-pro

python main.py --entity-name "Venue Name" --entity-type venue
```

---

## Framework-Specific Best Practices (Research Required)

**Before implementing any of these patterns, verify with live documentation for the exact versions in this project.**

### Next.js 16.x

- **Server Components**: Default in `app/` directory - only add `'use client'` for interactivity
- **Caching**: Use `export const revalidate = seconds` for time-based revalidation
- **Data Fetching**: Direct Prisma queries in Server Components (no API routes needed)
- **Security**: Check for security patches (16.0.7 has known vulnerabilities)

### React 19.2.x

- **Server Actions**: Use `'use server'` directive for form submissions
- **Suspense**: Wrap async components with `<Suspense>` boundaries
- **Security**: Verify version 19.2.3+ for DoS patch

### Prisma 7.x

- **Driver Adapters**: Now mandatory - use `PrismaPg` adapter
- **Connection Pooling**: `pg` driver has different timeout defaults than v6
- **Query Compiler**: TypeScript-based (no Rust binary)

### Tailwind CSS v4

- **Config Location**: CSS file, not `tailwind.config.js`
- **Theme Tokens**: Use `@theme` directive with CSS variables
- **Performance**: 5x faster builds, 100x faster incremental

### SQLModel + PostgreSQL

- **Async**: Use `asyncpg` + `psycopg2-binary` + `greenlet` for async operations
- **Dual-Purpose**: Models serve as both Pydantic and SQLAlchemy
- **Field Exclusions**: Use `exclude=True` for DB-only fields

### Instructor + Claude API

- **Latest API**: Use `instructor.from_anthropic()` wrapper
- **Token Limits**: Set `max_tokens=30000` for complex schemas
- **Validation**: Enable retries for hallucination mitigation

---

## PostgreSQL Connection Pooling (Serverless)

**Problem**: Serverless functions exhaust connection limits.

**Solutions**:
- **PgBouncer**: Transaction-mode pooling (10K concurrent connections)
- **Managed Services**: Neon (autoscaling), Supabase (built-in pooling), AWS RDS Proxy
- **Application-Level**: Initialize connection pool in global scope

**Research before implementing**: Connection pooling patterns change frequently. Search for "[provider] PostgreSQL connection pooling 2025" for current best practices.

---

## Security Checklist

Before deploying code changes, verify:

- [ ] API keys not hardcoded (use environment variables)
- [ ] Database credentials in `.env`, not committed to git
- [ ] User input validated/sanitized (especially in LLM prompts)
- [ ] Dependencies updated to patched versions (check CVE databases)
- [ ] SQL injection prevention (Prisma/SQLModel handle this, but verify)
- [ ] CORS configured correctly (if adding API routes)
- [ ] Rate limiting on public endpoints (if adding API)

---

## Sources & Further Reading

When researching, prioritize these official sources:

- **Next.js**: https://nextjs.org/docs
- **React**: https://react.dev
- **Prisma**: https://www.prisma.io/docs
- **Tailwind CSS**: https://tailwindcss.com
- **SQLModel**: https://sqlmodel.tiangolo.com
- **Instructor**: https://python.useinstructor.com
- **Anthropic**: https://docs.anthropic.com
- **PostgreSQL**: https://www.postgresql.org/docs

**Security Advisories**:
- GitHub Security Advisories: https://github.com/advisories
- CVE Database: https://cve.mitre.org
- Framework-specific changelogs (check "Security" tags)

---

**Last Updated**: December 2025 (technology stack versions listed above)
**Maintainer**: Verify current versions in `package.json` and `requirements.txt` before coding
