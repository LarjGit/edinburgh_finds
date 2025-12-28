# Edinburgh Finds - Monorepo AI Guidelines

## Overview
A curated directory of niche activities and things to do in Edinburgh.

## Repository Structure
edinburgh_finds/
├── edinburgh_finds_backend/ ← Python data extraction → Postgres
├── edinburgh_finds_web/ ← Next.js 16 frontend
├── .gitignore, README.md
└── .github/copilot-instructions.md ← This file

## Backend (`edinburgh_finds_backend/`)

**Core workflow**: AI web scraping → LLM extraction → Postgres storage
data/[entity_type]s/[slug]/[gather|raw|processed]/ → extraction_pipeline.py → database/models.py

**Key patterns:**
Run extraction
python main.py --entity-name "David Lloyd Club Edinburgh Shawfair" --entity-type venue

Database setup
python scripts/create_tables.py

- **Entity types**: venue, retailer, club (add via `core/entity_registry.py`)
- **Data quality**: Confidence grading A/B/C/X, field_confidence JSON
- **LLM**: Instructor + Claude/Gemini, `max_tokens=30000`
- **DB**: SQLModel (Listing ↔ Venue 1:1), JSON fields for hours/confidence
- **Key files**: `services/extraction_pipeline.py`, `database/models.py`, `schemas/venue_extraction_schema.py`

## Frontend (`edinburgh_finds_web/`)

**Category-driven Next.js 16 app**:
Home → /category/[slug] → /listing/[slug]

**Key patterns:**
// Data access
import { prisma } from '@/lib/prisma'
const listings = await prisma.listings.findMany({
where: { canonical_categories: { has: slug } },
include: { venues: true }
})

// Category rendering
const config = categories[categorySlug]
const summary = listing.venues?.[config.venue.summaryField]

- **Server-first**: `'use client'` only for interactivity
- **Categories**: `app/config/categories.ts` drives UI/data
- **Prisma**: Generated client in `app/generated/prisma/`
- **UI**: shadcn/ui, Tailwind v4, `cn()` utility
- **Key files**: `app/config/categories.ts`, `lib/prisma.ts`, `components/ui/`

## Cross-Repo Workflows

**Full data refresh**:
cd edinburgh_finds_backend
python scripts/create_tables.py
python main.py --entity-name "..." --entity-type venue # Repeat for new venues
cd ../edinburgh_finds_web
npx prisma generate
npm run dev

**Adding new category**:
1. Backend: Extract venue → `data/venues/[slug]/`
2. Web: Add to `app/config/categories.ts`, image to `public/images/categories/`, set `isLive: true`

**Schema changes**:
backend/database/models.py → python scripts/create_tables.py
web/prisma/schema.prisma → npx prisma generate

## Common Patterns Across Repos

**Entity lifecycle**:
Raw text (gather/) → LLM extraction (Pydantic) → Postgres (Listing+Venue) → Next.js server components

**Confidence tracking**:
- Backend: `field_confidence` JSON, update if new ≥ 0.7
- Frontend: Show confidence-aware fields via category config

**Slug consistency**:
- Backend: `entity_name.lower().replace(" ", "_")`
- Frontend: URLs use `listing.slug`