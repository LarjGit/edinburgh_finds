# Edinburgh Finds - AI Coding Guidelines

## Architecture Overview

This is a Next.js 16 application for discovering sports venues and activities in Edinburgh. The app follows a category-based browsing pattern:

- **Home page**: Hero section with category tiles
- **Category pages** (`/category/[slug]`): Lists venues for a specific activity (tennis, padel, etc.)
- **Listing pages** (`/listing/[slug]`): Detailed venue information

**Key architectural decisions:**
- Server components for data fetching, client components only when needed
- Prisma ORM with PostgreSQL database
- Generated Prisma client in `app/generated/prisma/` (not `node_modules`)
- Category configurations drive UI behavior and data display

## Data Model

**Core entities:**
- `listings`: Base entity with location, contact info, categories
- `venues`: Sports facility details extending listings

**Key patterns:**
- Categories stored as arrays in `canonical_categories` field
- Venue-specific data in separate `venues` table with 1:1 relationship
- Slugs used for URLs, generated from entity names

**Database access:**
```typescript
import { prisma } from '@/lib/prisma'

// Fetch venues for a category
const listings = await prisma.listings.findMany({
  where: { canonical_categories: { has: slug } },
  include: { venues: true }
})
```

## Component Patterns

**Category-driven components:**
- Categories configured in `app/config/categories.ts` with display settings
- `VenueCard` uses category config to show relevant fields (e.g., "5 courts" for tennis)
- Venue summary pulled from category-specific field (e.g., `tennis_summary`)

**UI Components:**
- shadcn/ui with "new-york" style, Radix UI primitives
- CSS variables for theming, oklch color space
- Dark mode support via CSS custom properties

**Styling conventions:**
- Tailwind CSS v4 with custom CSS variables
- `cn()` utility from `@/lib/utils` for conditional classes
- Component variants using `class-variance-authority`

## Development Workflow

**Database operations:**
- Schema changes: Edit `prisma/schema.prisma`, run `npx prisma generate`
- Migrations: `npx prisma migrate dev` (requires DATABASE_URL in .env)

**Adding categories:**
1. Add config to `app/config/categories.ts` with image path and field mappings
2. Add category image to `public/images/categories/`
3. Set `isLive: true` to make it browseable

**Component development:**
- Server components by default, add `'use client'` only for interactivity
- Import UI components from `@/components/ui/`
- Use path aliases: `@/*` maps to project root

## Key Files & Directories

- `app/config/categories.ts` - Category definitions and display configs
- `app/generated/prisma/` - Generated Prisma client (regenerate after schema changes)
- `lib/prisma.ts` - Prisma client singleton with PostgreSQL adapter
- `components/ui/` - shadcn/ui components
- `public/images/` - Static assets (branding, categories, venues)

## Common Patterns

**Venue data access:**
```typescript
// In server components
const listing = await prisma.listings.findUnique({
  where: { slug },
  include: { venues: true }
})

// Access venue-specific data
const tennisCourts = listing.venues?.tennis_total_courts
```

**Category-aware rendering:**
```typescript
// Use category config to drive UI
const config = categories[categorySlug]
const summary = listing.venues?.[config.venue.summaryField]
```

**Image handling:**
- Category images: `/images/categories/{slug}.jpg`
- Venue images: `/images/venues/{venue-slug}/` (if exist)
- Logo: `/images/branding/logo.png`</content>
<parameter name="filePath">c:\Projects\edinburgh_finds\edinburgh_finds_web\.github\copilot-instructions.md