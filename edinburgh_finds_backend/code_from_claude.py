# ====================================================================
# GENERIC ENTITY EXTRACTION PROMPTS
# Entity-agnostic system for extracting structured data from URLs
# ====================================================================

from typing import Dict, Any, Type, Optional, List
from pydantic import BaseModel
import json

# ====================================================================
# SYSTEM PROMPT - FULLY GENERIC
# ====================================================================
SYSTEM_PROMPT = """You are an expert data extraction specialist with deep knowledge across all domains, industries, and entity types.

Your mission is to extract complete, accurate, and comprehensive data from provided URLs with maximum data discovery and completeness.

CORE EXTRACTION PRINCIPLES:

1. EXHAUSTIVE ANALYSIS
   - Analyze ALL content: main content, sidebars, headers, footers, metadata, navigation menus
   - Examine embedded elements: maps, booking widgets, contact forms, social media feeds, galleries
   - Check technical elements: meta tags, structured data (JSON-LD, microdata), OpenGraph tags
   - Review visual content: extract information from images, infographics, diagrams

2. SCHEMA ADHERENCE
   - Extract ALL attributes defined in the provided JSON schema
   - Respect data types: strings, numbers, booleans, arrays, objects, enums
   - Properly structure nested objects and arrays
   - Follow any enum constraints exactly as specified

3. INTELLIGENT INFERENCE
   - Use domain knowledge and contextual clues to infer missing data
   - Cross-reference multiple mentions to validate information
   - Apply logical reasoning based on entity type and industry standards
   - Make educated inferences when data is implied but not explicit

4. COMPREHENSIVE DISCOVERY (other_attributes)
   - Beyond schema fields, identify ALL additional relevant attributes
   - Capture metadata, specifications, relationships, identifiers, social links
   - Include domain-specific properties unique to the entity type
   - Extract technical details, certifications, awards, statistics
   - Never duplicate data already captured in defined schema fields

5. MULTI-SOURCE VALIDATION
   - Cross-reference information when multiple data points exist
   - Prioritize official, authoritative sources
   - Resolve conflicts by choosing most recent or most detailed information
   - Note when information appears contradictory (in other_attributes if relevant)

6. DATA QUALITY STANDARDS
   - Accuracy: Verify all extracted data against source content
   - Completeness: Aim for 100% population of applicable fields
   - Consistency: Use standardized formats (dates, phone numbers, addresses)
   - Relevance: Only include factual, verifiable information
   - Structure: Maintain proper hierarchy in nested objects

OUTPUT REQUIREMENTS:
- Return ONLY valid JSON matching the provided schema
- Use null for fields that are genuinely unavailable after exhaustive search
- Convert values to appropriate data types as specified in schema
- Populate other_attributes array with ALL discoverable additional data
- Use clear, descriptive keys in snake_case for other_attributes (e.g., "social_media_instagram", "year_established")
- Convert all other_attributes values to strings for consistency"""

# ====================================================================
# USER PROMPT GENERATOR - ENTITY AGNOSTIC
# ====================================================================
def create_extraction_prompt(
    url: str,
    entity_name: str,
    entity_type: str,
    schema_hints: Optional[Dict[str, str]] = None
) -> str:
    """
    Generate a comprehensive, entity-agnostic extraction prompt.
    
    Args:
        url: The URL to extract data from
        entity_name: Name of the entity being extracted
        entity_type: Type of entity (e.g., "venue", "event", "organization")
        schema_hints: Optional dict of field categories to emphasize (e.g., {"location": "address and geographic data"})
    
    Returns:
        Formatted user prompt optimized for maximum data extraction
    """
    
    # Build schema-specific hints if provided
    hints_section = ""
    if schema_hints:
        hints_section = "\n**SCHEMA-SPECIFIC GUIDANCE:**\n"
        for category, description in schema_hints.items():
            hints_section += f"- {category}: {description}\n"
    
    return f"""EXTRACTION TASK: Analyze and extract comprehensive data for the specified entity from the provided URL.

**ENTITY DETAILS:**
- Entity Name: {entity_name}
- Entity Type: {entity_type}
- Source URL: {url}

**OBJECTIVE:** Extract maximum data completeness while maintaining accuracy. This is a progressive data collection task where every piece of information matters.

**EXTRACTION PHASES:**

═══════════════════════════════════════════════════════════
PHASE 1: SCHEMA-DEFINED FIELD EXTRACTION
═══════════════════════════════════════════════════════════

Extract ALL fields defined in the provided JSON schema:

1. IDENTIFICATION & CLASSIFICATION
   - entity_name: Official or primary name of the entity
   - entity_type: Confirm as "{entity_type}"
   - primary_category: Main classification/category
   - additional_categories: All other relevant categories or classifications

2. LOCATION & GEOGRAPHIC DATA (if applicable)
   - Complete address components (street, city, postcode, country)
   - Geographic coordinates (latitude, longitude)
   - Location identifiers or references
   - Regional or administrative divisions

3. CONTACT & COMMUNICATION (if applicable)
   - Phone numbers (all formats, mobile, landline, international)
   - Email addresses (check contact forms, mailto links, footers)
   - Website URLs (canonical, alternate language versions)
   - Social media profiles and handles
   - Communication preferences or hours

4. TEMPORAL DATA (if applicable)
   - Operating hours or schedules
   - Opening/closing times
   - Seasonal variations
   - Special hours or exceptions
   - Time zone information

5. QUANTITATIVE DATA (if applicable)
   - Counts, capacities, inventory numbers
   - Ratings, scores, or metrics
   - Sizes, dimensions, or measurements
   - Statistical information
   - Financial data (prices, fees, ranges)

6. STRUCTURED RELATIONSHIPS (if applicable)
   - Nested objects for complex data structures
   - Arrays for multiple items or lists
   - Hierarchical relationships
   - Associated entities or references
{hints_section}

**EXTRACTION STRATEGIES:**
- Read entire page content from top to bottom
- Check navigation menus for additional pages or sections
- Examine footer content (often contains contact/location data)
- Look for "About", "Contact", "Location", "FAQ" sections
- Extract from embedded maps, booking systems, or widgets
- Check meta tags and structured data markup
- Analyze image captions, alt text, and infographics
- Review any downloadable documents or linked resources

═══════════════════════════════════════════════════════════
PHASE 2: ADDITIONAL ATTRIBUTE DISCOVERY
═══════════════════════════════════════════════════════════

Populate the "other_attributes" array with ALL discoverable information not captured in schema fields.

**DISCOVERY CATEGORIES:**

IDENTITY & METADATA
- Established/founded date, year, or history
- Legal names, DBA names, trading names
- Registration numbers, identifiers, codes
- Ownership, parent company, affiliates
- Brand information, logos, trademarks

DIGITAL PRESENCE
- Social media: Instagram, Facebook, Twitter, LinkedIn, TikTok, YouTube handles/URLs
- Review platform profiles: Google, Yelp, TripAdvisor, Trustpilot
- App store links: iOS, Android applications
- Online booking/reservation systems
- E-commerce or online store links

FEATURES & ATTRIBUTES
- Amenities, facilities, services offered
- Special features or unique characteristics
- Accessibility information
- Certifications, accreditations, memberships
- Awards, recognitions, achievements

OPERATIONAL DETAILS
- Capacity, size, scale information
- Equipment, inventory, resources
- Staff information (team size, key personnel)
- Languages spoken or supported
- Payment methods accepted

POLICY & REQUIREMENTS
- Rules, regulations, policies
- Age restrictions or requirements
- Dress codes, equipment needs
- Booking or reservation policies
- Cancellation terms

CUSTOMER INFORMATION
- Review scores from any platform
- Number of reviews or ratings
- Testimonials or quotes
- Customer demographics served
- Membership or loyalty programs

PRICING & FINANCIAL
- Price ranges or indicators
- Membership fees or subscription costs
- Booking fees, service charges
- Discounts, promotions, offers
- Accepted payment methods

TECHNICAL & SPECIFICATIONS
- Technical specifications
- Model numbers, versions
- Dimensions, measurements
- Materials, construction details
- Compatibility or requirements

CONTEXTUAL & ENVIRONMENTAL
- Surrounding area or neighborhood info
- Nearby landmarks or transport
- Parking availability and details
- Climate or weather considerations
- Safety or security features

**other_attributes FORMAT:**
- Key: Use clear, descriptive snake_case names (e.g., "instagram_handle", "founded_year", "wheelchair_accessible")
- Value: Convert ALL values to strings (numbers, booleans, dates all as strings)
- Uniqueness: Each key should appear only once
- Relevance: Only include factual, verifiable information
- No Duplication: Never repeat data from schema-defined fields

═══════════════════════════════════════════════════════════
PHASE 3: VALIDATION & QUALITY CHECK
═══════════════════════════════════════════════════════════

Before finalizing output:
1. Verify all numeric values are logical and within expected ranges
2. Ensure date formats are consistent
3. Confirm contact details are properly formatted
4. Check that enum values match exactly (if applicable)
5. Validate that nested objects are complete and properly structured
6. Ensure no data duplication between schema fields and other_attributes
7. Confirm all array items are relevant and non-duplicate

═══════════════════════════════════════════════════════════
OUTPUT REQUIREMENTS
═══════════════════════════════════════════════════════════

- Return ONLY valid JSON matching the provided schema
- Populate every applicable field with accurate data
- Use null ONLY when data is genuinely unavailable after exhaustive search
- Maximize the other_attributes array with all discoverable data
- Maintain proper data types as specified in schema
- Ensure all nested structures are correctly formatted

**PRIORITY:** This data will be progressively merged across multiple sources. Extract every piece of valuable information to maximize the completeness of the final aggregated dataset."""

# ====================================================================
# IMPROVED DATA EXTRACTION MODULE
# ====================================================================

import os
from typing import Optional, List, Dict, Any, Type
from pydantic import BaseModel

class DataExtractor:
    """
    Generic entity data extraction system with progressive augmentation.
    Works with any Pydantic model that inherits from BaseListing.
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "sonar"):
        """
        Initialize the data extractor.
        
        Args:
            api_key: Perplexity API key (defaults to PERPLEXITY_API_KEY env var)
            model_name: Model to use for extraction
        """
        from perplexity import Perplexity
        
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY environment variable not set.")
        
        self.client = Perplexity(api_key=self.api_key)
        self.model_name = model_name
        self.system_prompt = SYSTEM_PROMPT
    
    def discover_urls(
        self,
        entity_name: str,
        entity_type: str,
        max_results: int = 10
    ) -> List[str]:
        """
        Discover relevant URLs for an entity.
        
        Args:
            entity_name: Name of the entity
            entity_type: Type of entity
            max_results: Maximum number of URLs to return
            
        Returns:
            List of discovered URLs
        """
        query = f'Find official website and information pages for "{entity_name}" ({entity_type})'
        
        try:
            results = self.client.search.create(
                query=query,
                max_results=max_results
            ).results
            urls = [r.url for r in results if r.url]
            print(f"🔍 Discovered {len(urls)} URLs for {entity_name}")
            return urls
        except Exception as e:
            print(f"⚠️  URL discovery failed: {e}")
            return []
    
    def extract_from_url(
        self,
        url: str,
        entity_name: str,
        entity_type: str,
        model_class: Type[BaseModel],
        schema_hints: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Extract data from a single URL.
        
        Args:
            url: URL to extract from
            entity_name: Name of the entity
            entity_type: Type of entity
            model_class: Pydantic model class to validate against
            schema_hints: Optional hints about schema structure
            
        Returns:
            Extracted data as dict, or None if extraction failed
        """
        try:
            user_prompt = create_extraction_prompt(
                url=url,
                entity_name=entity_name,
                entity_type=entity_type,
                schema_hints=schema_hints
            )
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "schema": model_class.model_json_schema(),
                        "name": f"{entity_type}_extraction"
                    }
                },
                temperature=0.0,
            )
            
            raw_json = response.choices[0].message.content
            validated_data = model_class.model_validate_json(raw_json)
            print(f"  ✓ Extracted data from {url[:50]}...")
            
            return validated_data.model_dump()
            
        except Exception as e:
            print(f"  ✗ Failed to extract from {url[:50]}...: {e}")
            return None
    
    def deep_merge(
        self,
        master: Dict[str, Any],
        new: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Recursively merge new data into master data.
        Improved with better handling of other_attributes deduplication.
        
        Args:
            master: Master data dictionary
            new: New data to merge in
            
        Returns:
            Merged dictionary
        """
        for key, value in (new or {}).items():
            if value is None:
                continue
            
            # Special handling for other_attributes to prevent duplicates
            if key == "other_attributes" and isinstance(value, list):
                master_attrs = master.get(key, [])
                if not isinstance(master_attrs, list):
                    master_attrs = []
                
                # Create a set of existing keys
                existing_keys = {attr.get("key", "").lower() for attr in master_attrs if isinstance(attr, dict)}
                
                # Add new attributes only if key doesn't exist
                for attr in value:
                    if isinstance(attr, dict) and attr.get("key"):
                        attr_key = attr["key"].lower()
                        if attr_key not in existing_keys and attr.get("value") is not None:
                            master_attrs.append(attr)
                            existing_keys.add(attr_key)
                
                if master_attrs:
                    master[key] = master_attrs
                continue
            
            if isinstance(value, dict):
                if value:
                    master_value = master.get(key)
                    if not isinstance(master_value, dict):
                        master_value = {}
                    merged = self.deep_merge(master_value, value)
                    if merged:
                        master[key] = merged
            
            elif isinstance(value, list):
                if value:
                    master_list = master.get(key, [])
                    if not isinstance(master_list, list):
                        master_list = []
                    
                    # Normalize strings for categories
                    if key in ["additional_categories", "categories"]:
                        seen = {s.lower() for s in master_list if isinstance(s, str)}
                        for item in value:
                            if isinstance(item, str) and item.lower() not in seen:
                                master_list.append(item)
                                seen.add(item.lower())
                    else:
                        # Generic list merging with string comparison
                        seen = {str(item) for item in master_list}
                        for item in value:
                            if item is not None and str(item) not in seen:
                                master_list.append(item)
                                seen.add(str(item))
                    
                    if master_list:
                        master[key] = master_list
            
            else:
                # Only overwrite if key doesn't exist or master value is None
                if key not in master or master[key] is None:
                    master[key] = value
        
        return master
    
    def progressive_augmentation(
        self,
        urls: List[str],
        entity_name: str,
        entity_type: str,
        model_class: Type[BaseModel],
        schema_hints: Optional[Dict[str, str]] = None
    ) -> Optional[BaseModel]:
        """
        Progressively augment data by extracting from multiple URLs.
        
        Args:
            urls: List of URLs to extract from
            entity_name: Name of the entity
            entity_type: Type of entity
            model_class: Pydantic model class
            schema_hints: Optional schema hints
            
        Returns:
            Validated model instance with merged data, or None if all extractions failed
        """
        print(f"\n📊 Starting progressive augmentation across {len(urls)} URLs...")
        
        # Initialize master data
        master_data = model_class.model_construct(
            entity_name=entity_name,
            entity_type=entity_type
        ).model_dump()
        
        successful_extractions = 0
        
        for idx, url in enumerate(urls, 1):
            print(f"\n[{idx}/{len(urls)}] Processing: {url}")
            
            new_data = self.extract_from_url(
                url=url,
                entity_name=entity_name,
                entity_type=entity_type,
                model_class=model_class,
                schema_hints=schema_hints
            )
            
            if new_data:
                master_data = self.deep_merge(master_data, new_data)
                successful_extractions += 1
        
        if successful_extractions == 0:
            print(f"\n❌ No successful extractions from {len(urls)} URLs")
            return None
        
        print(f"\n✅ Successfully merged data from {successful_extractions}/{len(urls)} URLs")
        
        # Validate final merged data
        try:
            return model_class.model_validate(master_data)
        except Exception as e:
            print(f"⚠️  Final validation failed: {e}")
            return None
    
    def extract_entity(
        self,
        entity_name: str,
        entity_type: str,
        model_class: Type[BaseModel],
        max_urls: int = 10,
        schema_hints: Optional[Dict[str, str]] = None,
        custom_urls: Optional[List[str]] = None
    ) -> Optional[BaseModel]:
        """
        Complete entity extraction workflow.
        
        Args:
            entity_name: Name of the entity to extract
            entity_type: Type of entity
            model_class: Pydantic model class to use
            max_urls: Maximum URLs to discover (ignored if custom_urls provided)
            schema_hints: Optional hints about schema structure
            custom_urls: Optional list of specific URLs to use instead of discovery
            
        Returns:
            Validated model instance with complete data, or None if extraction failed
        """
        # Use custom URLs or discover them
        urls = custom_urls if custom_urls else self.discover_urls(
            entity_name=entity_name,
            entity_type=entity_type,
            max_results=max_urls
        )
        
        if not urls:
            print(f"❌ No URLs found for {entity_name}")
            return None
        
        # Perform progressive augmentation
        return self.progressive_augmentation(
            urls=urls,
            entity_name=entity_name,
            entity_type=entity_type,
            model_class=model_class,
            schema_hints=schema_hints
        )

# ====================================================================
# USAGE EXAMPLE - WORKS WITH ANY MODEL
# ====================================================================

if __name__ == "__main__":
    import uuid
    from listings_data_model import Venue  # Or any other Pydantic model
    
    # Initialize extractor
    extractor = DataExtractor(model_name="sonar")
    
    # Define schema hints (optional - helps guide extraction)
    venue_hints = {
        "location": "Complete address and geographic coordinates",
        "contact": "All communication methods including phone, email, website",
        "hours": "Operating hours and schedule information",
        "court_inventory": "Sport-specific facility counts (tennis, squash, padel, pickleball courts)"
    }
    
    # Extract entity data
    result = extractor.extract_entity(
        entity_name="David Lloyd Club Edinburgh Shawfair",
        entity_type="venue",
        model_class=Venue,
        max_urls=10,
        schema_hints=venue_hints
    )
    
    if result:
        result.listing_id = str(uuid.uuid4())
        
        print("\n" + "="*60)
        print("✅ FINAL EXTRACTION OUTPUT")
        print("="*60)
        print(f"Entity: {result.entity_name}")
        print(f"Type: {result.entity_type}")
        print(f"ID: {result.listing_id}")
        
        # Print summary statistics
        data_dict = result.model_dump(exclude_none=True)
        print(f"\nPopulated fields: {len(data_dict)}")
        
        if result.other_attributes:
            print(f"Additional attributes discovered: {len(result.other_attributes)}")
            print("\nSample additional attributes:")
            for attr in result.other_attributes[:10]:
                print(f"  • {attr.key}: {attr.value}")
        
        # Save to file
        output_file = f"{entity_type}_{result.listing_id}.json"
        with open(output_file, 'w') as f:
            json.dump(data_dict, f, indent=2)
        print(f"\n💾 Saved to: {output_file}")
    else:
        print("\n❌ Extraction pipeline failed")