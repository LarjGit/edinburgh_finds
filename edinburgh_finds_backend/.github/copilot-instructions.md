# Edinburgh Finds Backend - AI Coding Guidelines

## Architecture Overview
This is a data extraction pipeline for Edinburgh venues/retailers using AI-powered web scraping and structured data extraction. The system processes raw text through LLM extraction into PostgreSQL storage.

**Core Data Flow:**
1. **Data Gathering**: AI models (Claude, Perplexity) collect venue/retailer information using confidence-graded prompts
2. **Raw Storage**: Text saved to `data/[entity_type]/[entity_slug]/gather/` with timestamps
3. **Extraction**: `extraction_pipeline.py` uses Instructor + LLM to convert raw text → structured Pydantic models
4. **Persistence**: Data upserted to SQLModel tables with confidence tracking
5. **Output**: JSON snapshots in `processed/`, raw text in `raw/` for reproducibility

## Key Components
- **`services/extraction_pipeline.py`**: Main pipeline orchestrating LLM extraction, DB upsert, and file output
- **`database/models.py`**: SQLModel definitions (Listing + entity-specific tables like Venue)
- **`schemas/venue_extraction_schema.py`**: Dynamic Pydantic schema generation from SQLModel
- **`services/instructor_client.py`**: LLM client supporting Claude (LaoZhang), Gemini, Anthropic
- **`services/upsert_entity.py`**: Confidence-aware database upserts with change tracking
- **`core/entity_registry.py`**: Entity type configuration (venue, retailer, club)

## Project Patterns

### Entity Organization
- **Directory Structure**: `data/[entity_type]s/[entity_slug]/[raw|processed|gather|extract]/`
- **Slug Generation**: `entity_name.lower().replace(" ", "_").replace("/", "_").replace("'", "")`
- **Entity Types**: Currently "venue", "retailer", "club" - extensible via `entity_registry.py`

### Data Quality & Confidence
- **Confidence Grading**: GRADE A (1.0), B (0.8), C (0.5), X (null) for data sources
- **Field Confidence**: Every extracted field tracks confidence score in `field_confidence` dict
- **Update Rules**: Only replace existing data if new confidence ≥ 0.7
- **Source Provenance**: `source_info` merges LLM sources with system timestamps

### LLM Integration
- **Instructor Library**: Enforces Pydantic schemas on LLM responses
- **Prompt Structure**: System prompt + raw text input → structured JSON output
- **Model Selection**: Configurable via `LLM_PROVIDER` and `LLM_MODEL` in settings
- **Max Tokens**: Always set `max_tokens=30000` for complex venue schemas

### Database Design
- **Dual Purpose Models**: SQLModel classes serve as both DB tables and Pydantic validators
- **Field Exclusion**: Use `exclude=True` for DB-only fields (listing_id, slug, timestamps)
- **Relationships**: Listing ↔ Venue via foreign key on `listing_id`
- **JSON Fields**: `opening_hours`, `other_attributes`, `field_confidence` as JSON columns

## Development Workflows

### Running Extraction
```bash
python main.py --entity-name "David Lloyd Club Edinburgh Shawfair" --entity-type venue --file data/venues/david_lloyd_club_edinburgh_shawfair/gather/file.txt
```

### Database Setup
```bash
python scripts/create_tables.py  # Creates tables from SQLModel definitions
```

### Adding New Entity Types
1. Create entity-specific model in `database/models.py`
2. Add to `core/entity_registry.py` with schema/table/field mappings
3. Create extraction schema in `schemas/`
4. Update `main.py` choices if needed

### Data Gathering Prompts
- Located in `data/prompts/` with entity-specific versions
- Use confidence grading (A/B/C/X) for source quality
- Include all discoverable attributes: facilities, contact info, coordinates, hours

## Code Style Notes
- **Imports**: Standard library → third-party → local modules
- **Error Handling**: Use specific exceptions, avoid bare `except:`
- **Type Hints**: Full typing with `Optional`, `List`, `Dict` for clarity
- **Docstrings**: Describe purpose, parameters, return values
- **Naming**: `snake_case` for variables/functions, `PascalCase` for classes
- **Path Handling**: Use `pathlib.Path`, absolute paths for reliability

## Common Gotchas
- **Schema Fields**: Only include fields present in both Listing and entity models
- **Foreign Keys**: Venue `listing_id` must match existing Listing record
- **Confidence Updates**: Always check `field_confidence` before overwriting data
- **URL Validation**: Must start with `http://` or `https://`, otherwise `null`
- **Phone Normalization**: Use `phonenumbers` library for E164 format
- **Coordinate Precision**: Round lat/lon to 5 decimal places

## Testing Approach
- **Integration Tests**: Test full pipeline with sample data
- **Schema Validation**: Ensure Pydantic models accept/reject correctly
- **DB Operations**: Verify upserts handle confidence and relationships properly
- **File Outputs**: Check JSON structure and raw text snapshots</content>
<parameter name="filePath">c:\Projects\edinburgh_finds\edinburgh_finds_backend\.github\copilot-instructions.md