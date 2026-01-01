# Claude Code Instructions - Edinburgh Finds

This file contains **Claude Code-specific** instructions for autonomous development workflows.

**For universal codebase information:** See [`agents.md`](agents.md) for architecture, patterns, and development commands that apply to all AI assistants.

---

## Claude Code Tool Usage

### Live Internet Research (WebSearch)

**Mandatory usage per [agents.md](agents.md) research protocol:**

```typescript
// Before providing code for version-specific APIs
WebSearch: "Prisma 7.1.0 PrismaPg adapter setup PostgreSQL 2025"
WebSearch: "Next.js 16.0.7 server components security advisory 2025"
WebSearch: "Instructor 1.13.0 Anthropic Claude API best practices 2025"
```

**After searching, cite sources:**
- Include documentation links in code comments
- Reference official docs in explanations
- Note version discrepancies found

### File Navigation for Version Checking

Before making framework-specific changes:

```typescript
// Check exact versions currently in use
Read: "edinburgh_finds_web/package.json"
Read: "edinburgh_finds_backend/requirements.txt"

// Then search for those exact versions
WebSearch: "[framework] [exact version from file] [feature] official docs 2025"
```

### Schema Synchronization Workflow

This is the most critical cross-repo workflow. Use tools in this sequence:

```typescript
// 1. Read current backend schema
Read: "edinburgh_finds_backend/database/models.py"

// 2. Search for current best practices
WebSearch: "SQLModel [version] PostgreSQL schema migration 2025"

// 3. Make changes
Edit: "edinburgh_finds_backend/database/models.py"
// Add new field to Venue model

// 4. Apply to database (use Bash)
Bash: "cd edinburgh_finds_backend && python scripts/create_tables.py"

// 5. Read current Prisma schema
Read: "edinburgh_finds_web/prisma/schema.prisma"

// 6. Introspect database to update Prisma
Bash: "cd edinburgh_finds_web && npx prisma db pull"

// 7. Verify the change
Read: "edinburgh_finds_web/prisma/schema.prisma"
// Confirm new field appears

// 8. Regenerate TypeScript types
Bash: "cd edinburgh_finds_web && npx prisma generate"

// 9. Verify no breaking changes
Bash: "cd edinburgh_finds_web && npm run build"
```

### Autonomous Task Planning

For multi-step tasks, use TodoWrite to track progress:

```typescript
// Example: Adding a new category
TodoWrite: [
  { content: "Add 'climbing' to CANONICAL_CATEGORIES", status: "in_progress", activeForm: "Adding climbing to canonical categories" },
  { content: "Add synonyms for climbing", status: "pending", activeForm: "Adding climbing synonyms" },
  { content: "Update frontend categories.ts config", status: "pending", activeForm: "Updating frontend category config" },
  { content: "Add climbing category image", status: "pending", activeForm: "Adding category image" },
  { content: "Verify category displays correctly", status: "pending", activeForm: "Verifying category display" }
]

// Mark completed as you progress
TodoWrite: [
  { content: "Add 'climbing' to CANONICAL_CATEGORIES", status: "completed", activeForm: "Adding climbing to canonical categories" },
  { content: "Add synonyms for climbing", status: "in_progress", activeForm: "Adding climbing synonyms" },
  // ... rest
]
```

### Multi-File Code Changes

When a task requires changes across multiple files:

```typescript
// 1. Read all affected files first
Read: "edinburgh_finds_backend/database/models.py"
Read: "edinburgh_finds_backend/core/entity_registry.py"
Read: "edinburgh_finds_web/app/config/categories.ts"

// 2. Search for current patterns
WebSearch: "entity type pattern polyglot monorepo 2025"

// 3. Make coordinated changes
Edit: "edinburgh_finds_backend/database/models.py"
// Add Retailer model

Edit: "edinburgh_finds_backend/core/entity_registry.py"
// Register retailer type

Edit: "edinburgh_finds_web/app/config/categories.ts"
// Add retailer config

// 4. Verify changes compile
Bash: "cd edinburgh_finds_backend && python -m py_compile database/models.py"
Bash: "cd edinburgh_finds_web && npm run build"
```

### Error Handling & Debugging

When encountering errors:

```typescript
// 1. Read error output carefully
Bash: "cd edinburgh_finds_web && npm run dev"
// Error appears in output

// 2. Search for the specific error
WebSearch: "[exact error message] [framework] [version] 2025"

// 3. Read relevant files
Read: "[file mentioned in error]"

// 4. Check git diff to see what changed
Bash: "git diff [file]"

// 5. Apply fix based on research
Edit: "[file]"

// 6. Verify fix works
Bash: "[command that triggered error]"
```

---

## Autonomous Workflows

### Adding a New Venue (End-to-End)

```typescript
// 1. Research current extraction patterns
Read: "edinburgh_finds_backend/services/extraction_pipeline.py"
Read: "edinburgh_finds_backend/main.py"

// 2. Run extraction
Bash: 'cd edinburgh_finds_backend && python main.py --entity-name "The Climbing Academy" --entity-type venue'

// 3. Verify output files created
Bash: "ls -la data/venues/the_climbing_academy/processed/"

// 4. Check extraction result
Read: "data/venues/the_climbing_academy/processed/[latest_file].json"

// 5. Verify in database via Prisma Studio
Bash: "cd edinburgh_finds_web && npx prisma studio"
// Opens GUI at http://localhost:5555

// 6. Check frontend display
Bash: "cd edinburgh_finds_web && npm run dev"
// Visit category page
```

### Adding a New Entity Type (Retailer Example)

**TodoWrite Plan:**
```typescript
[
  { content: "Create Retailer SQLModel in database/models.py", status: "pending", activeForm: "Creating Retailer model" },
  { content: "Create retailer extraction schema", status: "pending", activeForm: "Creating extraction schema" },
  { content: "Register in entity_registry.py", status: "pending", activeForm: "Registering entity type" },
  { content: "Update main.py CLI choices", status: "pending", activeForm: "Updating CLI" },
  { content: "Apply database schema changes", status: "pending", activeForm: "Applying schema" },
  { content: "Sync Prisma schema", status: "pending", activeForm: "Syncing Prisma" },
  { content: "Add frontend category config", status: "pending", activeForm: "Adding category config" },
  { content: "Create RetailerCard component", status: "pending", activeForm: "Creating card component" },
  { content: "Update category page switch statement", status: "pending", activeForm: "Updating category page" },
  { content: "Test end-to-end", status: "pending", activeForm: "Testing" }
]
```

**Execution:**

```typescript
// 1. Research current entity patterns
Read: "edinburgh_finds_backend/database/models.py"
WebSearch: "SQLModel one-to-one relationship PostgreSQL 2025"

// 2. Create Retailer model
Edit: "edinburgh_finds_backend/database/models.py"
// Add Retailer class after Venue

// 3. Create schema
Write: "edinburgh_finds_backend/schemas/retailer_extraction_schema.py"
```python
from database.models import Listing, Retailer
from utils.model_conversion import to_pydantic_model

RetailerSchema = to_pydantic_model([Listing, Retailer])
```

// 4. Register entity type
Edit: "edinburgh_finds_backend/core/entity_registry.py"
// Add retailer case to get_entity_config

// 5. Update CLI
Edit: "edinburgh_finds_backend/main.py"
// Add "retailer" to --entity-type choices

// 6-10. Continue through remaining todos...
TodoWrite: [/* mark each completed as you go */]
```

### Debugging LLM Extraction Issues

```typescript
// 1. Read the processed output
Read: "data/venues/venue_slug/processed/[latest].json"

// 2. Check confidence scores
Bash: "cat data/venues/venue_slug/processed/*.json | jq '.listing.field_confidence'"

// 3. Read raw input that was sent to LLM
Read: "data/venues/venue_slug/raw/[latest].txt"

// 4. Read extraction prompt builder
Read: "edinburgh_finds_backend/utils/prompt_builder.py"

// 5. Search for LLM best practices
WebSearch: "Instructor Claude API structured extraction field confidence 2025"

// 6. Modify prompt if needed
Edit: "edinburgh_finds_backend/utils/prompt_builder.py"

// 7. Re-run extraction
Bash: 'cd edinburgh_finds_backend && python main.py --entity-name "Venue Name" --entity-type venue'

// 8. Compare outputs
Read: "data/venues/venue_slug/processed/[new_latest].json"
```

---

## Code Modification Patterns

### Always Read Before Edit

**❌ Never do this:**
```typescript
Edit: "some/file.py"  // Without reading first
```

**✅ Always do this:**
```typescript
Read: "some/file.py"
// Understand current code
Edit: "some/file.py"
// Make informed changes
```

### Preserve Existing Patterns

When adding new code, match the existing style:

```typescript
// 1. Read similar existing code
Read: "edinburgh_finds_backend/database/models.py"
// See how Venue model is structured

// 2. Match the pattern for new entity
Edit: "edinburgh_finds_backend/database/models.py"
// Use same Field() patterns, same comment style, same ordering
```

### Use Edit for Small Changes, Write for New Files

```typescript
// Modifying existing file - use Edit
Edit: "file.py"
old_string: "old code"
new_string: "new code"

// Creating new file - use Write
Write: "new_file.py"
content: "complete file contents"
```

---

## Error Recovery Patterns

### Build Failures

```typescript
// 1. Capture full error output
Bash: "cd edinburgh_finds_web && npm run build 2>&1 | tee build_error.log"

// 2. Read error log
Read: "build_error.log"

// 3. Search for specific error
WebSearch: "[exact error code/message] Next.js 16.0.7 2025"

// 4. Read problematic file
Read: "[file mentioned in error]"

// 5. Apply fix
Edit: "[file]"

// 6. Clean and rebuild
Bash: "cd edinburgh_finds_web && rm -rf .next && npm run build"
```

### Schema Drift Detection

```typescript
// 1. Check if Prisma schema matches database
Bash: "cd edinburgh_finds_web && npx prisma db pull --force"

// 2. Check for differences
Bash: "cd edinburgh_finds_web && git diff prisma/schema.prisma"

// 3. If differences exist, regenerate
Bash: "cd edinburgh_finds_web && npx prisma generate"

// 4. Rebuild frontend
Bash: "cd edinburgh_finds_web && npm run build"
```

### Python Import Errors

```typescript
// 1. Check if venv is activated (error will show system Python)
Bash: "which python"  // Should show venv path

// 2. Check if package is installed
Bash: "pip show [package-name]"

// 3. Install if missing
Bash: "pip install [package-name]"

// 4. Verify version matches requirements.txt
Read: "edinburgh_finds_backend/requirements.txt"
```

---

## Best Practices for Claude Code

### 1. Sequential Tool Calls for Dependencies

**❌ Don't call tools with missing dependencies in parallel:**
```typescript
// This fails if file doesn't exist yet
Read: "new_file.py"
Edit: "new_file.py"  // Can't edit what wasn't read
```

**✅ Call sequentially when order matters:**
```typescript
Write: "new_file.py"
Read: "new_file.py"   // Now it exists
Edit: "new_file.py"   // Now we can edit
```

### 2. Verify Before Proceeding

After major changes, verify:

```typescript
// After schema changes
Bash: "cd edinburgh_finds_backend && python scripts/create_tables.py"
Bash: "cd edinburgh_finds_web && npx prisma db pull && npx prisma generate"
Bash: "cd edinburgh_finds_web && npm run build"  // Verify no TypeScript errors

// After adding dependencies
Bash: "pip install -r requirements.txt"
Bash: "npm install"
```

### 3. Use TodoWrite for User Visibility

Users appreciate seeing progress on complex tasks:

```typescript
// At start of task
TodoWrite: [
  { content: "Research current implementation", status: "in_progress", activeForm: "Researching" },
  { content: "Make code changes", status: "pending", activeForm: "Making changes" },
  { content: "Run tests", status: "pending", activeForm: "Running tests" },
  { content: "Verify in browser", status: "pending", activeForm: "Verifying" }
]

// Update as you work
TodoWrite: [
  { content: "Research current implementation", status: "completed", activeForm: "Researching" },
  { content: "Make code changes", status: "in_progress", activeForm: "Making changes" },
  // ...
]
```

### 4. Search Before Suggesting Outdated Patterns

**❌ Don't assume patterns from training data:**
```typescript
// Suggesting Tailwind config in tailwind.config.js
// (Wrong for v4 - config is now in CSS)
```

**✅ Search for current version's patterns:**
```typescript
Read: "edinburgh_finds_web/package.json"
// See Tailwind v4
WebSearch: "Tailwind CSS 4 configuration setup 2025"
// Learn about CSS-based config
```

### 5. Explain Trade-offs

When multiple approaches exist, explain why you chose one:

```markdown
I'm using Server Components instead of Client Components because:
1. No client JavaScript needed (better performance)
2. Direct database access (no API route)
3. Built-in Next.js 16 caching

Trade-off: Can't use useState/useEffect
```

---

## Integration with VSCode

### File References

Use clickable file paths in responses:

```markdown
I updated the confidence threshold in [services/upsert_entity.py:12](edinburgh_finds_backend/services/upsert_entity.py#L12)
```

### Line-Specific References

```markdown
The issue is in [database/models.py:45-52](edinburgh_finds_backend/database/models.py#L45-L52)
```

### Folder Navigation

```markdown
Check the extraction artifacts in [data/venues/](data/venues/)
```

---

## Handling Ambiguity

### Use AskUserQuestion for Unclear Requirements

**When to ask:**
- Multiple valid implementation approaches
- Uncertain about desired behavior
- Potential breaking changes to existing functionality

**Example:**
```typescript
AskUserQuestion: {
  questions: [
    {
      question: "Should the new 'climbing_walls' field be required or optional?",
      header: "Field Type",
      multiSelect: false,
      options: [
        {
          label: "Required (always present)",
          description: "LLM extraction will fail if not found in source data"
        },
        {
          label: "Optional (nullable)",
          description: "LLM can leave blank if data not available"
        }
      ]
    }
  ]
}
```

---

## Common Pitfalls to Avoid

### ❌ Don't Assume File Locations

```typescript
// Wrong - guessing path
Edit: "backend/database/models.py"

// Right - use actual structure
Read: "edinburgh_finds_backend/database/models.py"
```

### ❌ Don't Skip the Read Step

```typescript
// Wrong
Edit: "file.py"  // Without reading

// Right
Read: "file.py"
Edit: "file.py"
```

### ❌ Don't Ignore Search Results

```typescript
// Wrong
WebSearch: "Prisma 7 breaking changes 2025"
// Get results showing adapter requirement
// Ignore and use old pattern anyway

// Right
WebSearch: "Prisma 7 breaking changes 2025"
// Read results
// Apply new adapter pattern
```

### ❌ Don't Forget Schema Sync

```typescript
// Wrong
Edit: "edinburgh_finds_backend/database/models.py"
// Add field
// Forget to sync Prisma
// Frontend breaks because TypeScript types are outdated

// Right
Edit: "edinburgh_finds_backend/database/models.py"
Bash: "cd edinburgh_finds_backend && python scripts/create_tables.py"
Bash: "cd edinburgh_finds_web && npx prisma db pull && npx prisma generate"
```

---

## Summary

**Key Principles for Claude Code:**
1. **Research first** (WebSearch for version-specific patterns)
2. **Read before editing** (understand existing code)
3. **Follow existing patterns** (match the codebase style)
4. **Sync schemas religiously** (backend → database → Prisma)
5. **Track progress** (TodoWrite for complex tasks)
6. **Verify changes** (build/test after modifications)
7. **Cite sources** (link to official docs)

For architecture and universal patterns, refer back to [`agents.md`](agents.md).
