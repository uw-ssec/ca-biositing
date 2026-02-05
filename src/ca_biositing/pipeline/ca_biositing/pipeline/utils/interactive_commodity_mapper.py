#!/usr/bin/env python3
"""
Enhanced USDA Commodity Mapper - Interactive Fuzzy Matching

This script implements the workflow:
1. Import ALL USDA commodities for California from NASS API
2. Populate all commodities into usda_commodity table (with URI)
3. Get your project's resources + primary_ag_products
4. Auto-match clear matches (high similarity)
5. Present 1-5 fuzzy match candidates for user to select
6. Track all resources in mapping table (including unmatched for progress)

Usage:
    # Step 1: Fetch and cache all CA USDA commodities (run once)
    python enhanced_commodity_mapper.py --fetch-ca-commodities

    # Step 2: Populate all commodities into database (run after fetching)
    python enhanced_commodity_mapper.py --populate-commodities

    # Step 3: Auto-match clear matches (>90% similarity)
    python enhanced_commodity_mapper.py --auto-match

    # Step 4: Interactive review of fuzzy matches (50-90% similarity)
    python enhanced_commodity_mapper.py --review

    # Step 5: Save approved mappings to database (includes progress tracking)
    python enhanced_commodity_mapper.py --save

    # Complete workflow (all steps)
    python enhanced_commodity_mapper.py --full-workflow

    # Management interface (view, edit, delete mappings)
    python enhanced_commodity_mapper.py --manage

Reference:
    USDA Commodity Codes: https://www.nass.usda.gov/Data_and_Statistics/County_Data_Files/Frequently_Asked_Questions/commcodes.php
"""

import sys
import os
import json
import requests
import re
from pathlib import Path
from difflib import SequenceMatcher
from typing import List, Tuple, Dict, Optional
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd

# Setup Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src' / 'ca_biositing' / 'pipeline'))
sys.path.insert(0, str(project_root / 'src' / 'ca_biositing' / 'datamodels'))

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlmodel import Session

load_dotenv()

# Cache files
CACHE_DIR = Path(__file__).parent / '.cache'
CACHE_DIR.mkdir(exist_ok=True)
CA_COMMODITIES_CACHE = CACHE_DIR / 'ca_usda_commodities.json'
PENDING_MATCHES_FILE = CACHE_DIR / 'pending_matches.json'
APPROVED_MATCHES_FILE = CACHE_DIR / 'approved_matches.json'


# ============================================================================
# STEP 1: Fetch all CA commodities from NASS API
# ============================================================================

def fetch_ca_commodities() -> List[Dict]:
    """
    Fetch all unique USDA commodities available for California.
    Uses web scraping from official USDA commodity codes page (fastest method).

    Returns:
        List of {code, name, description} dicts
    """
    print("\n" + "=" * 80)
    print("STEP 1: Fetching All USDA Commodities (Web Scraping)")
    print("=" * 80)

    print("Scraping USDA commodity codes from official website...")

    try:
        # Scrape the official USDA commodity codes page
        commodities = scrape_usda_commodity_codes()

        if commodities:
            print(f"✓ Found {len(commodities)} commodities from official USDA website")

            # Save to cache
            with open(CA_COMMODITIES_CACHE, 'w') as f:
                json.dump(commodities, f, indent=2)
            print(f"✓ Cached to {CA_COMMODITIES_CACHE}")

            return commodities
        else:
            print("⚠ Web scraping failed, trying API method...")
            return fetch_ca_commodities_api()

    except Exception as e:
        print(f"⚠ Web scraping failed ({e}), trying API method...")
        return fetch_ca_commodities_api()


def scrape_usda_commodity_codes() -> List[Dict]:
    """
    Scrape commodity codes from official USDA website.
    https://www.nass.usda.gov/Data_and_Statistics/County_Data_Files/Frequently_Asked_Questions/commcodes.php
    """
    url = "https://www.nass.usda.gov/Data_and_Statistics/County_Data_Files/Frequently_Asked_Questions/commcodes.php"

    print(f"  → Fetching {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the commodity codes table (there's only one table on this page)
    table = soup.find('table')

    if not table:
        raise Exception("No table found on the page")

    rows = table.find_all('tr')
    print(f"  → Found table with {len(rows)} rows")

    if len(rows) < 2:
        raise Exception("Table has no data rows")

    # Check headers - looking for cmdty and cmdty_desc columns
    header_row = rows[0]
    headers = [cell.get_text().strip().lower() for cell in header_row.find_all(['th', 'td'])]
    print(f"  → Headers: {headers}")

    # Find column indices
    code_col = None
    desc_col = None

    for i, header in enumerate(headers):
        if header == 'cmdty' or 'code' in header:
            code_col = i
        elif header == 'cmdty_desc' or ('commodity' in header and 'desc' in header):
            desc_col = i

    print(f"  → Code column: {code_col}, Description column: {desc_col}")

    if code_col is None or desc_col is None:
        raise Exception(f"Could not find required columns. Headers: {headers}")

    # Extract commodities
    commodities = []

    for row_num, row in enumerate(rows[1:], 1):  # Skip header
        cells = row.find_all(['td', 'th'])

        if len(cells) <= max(code_col, desc_col):
            continue

        code = cells[code_col].get_text().strip()
        name = cells[desc_col].get_text().strip()

        # Clean and validate the data
        if code and name and len(code) >= 4:  # USDA codes are typically 6-8 digits
            commodities.append({
                'code': code,
                'name': name.upper(),
                'description': name,
                'source': 'NASS_WEB',
                'scraped_at': datetime.now().isoformat()
            })

    print(f"  → Extracted {len(commodities)} valid commodities")

    if len(commodities) < 50:  # Sanity check - should have hundreds
        raise Exception(f"Too few commodities extracted ({len(commodities)}), something went wrong")

    return commodities


def fetch_ca_commodities_api() -> List[Dict]:
    """
    Fallback: Fetch commodities using NASS API with lightweight parameter query only.
    """
    print("  → Using NASS API parameter query (lightweight method)...")

    api_key = os.getenv('USDA_NASS_API_KEY')
    if not api_key:
        print("ERROR: USDA_NASS_API_KEY not found in .env file")
        return []

    try:
        # Use ONLY the parameter endpoint (no data queries to avoid 413 errors)
        url = "https://quickstats.nass.usda.gov/api/get_param_values/"
        params = {
            'key': api_key,
            'param': 'commodity_desc',
        }

        print("  → Getting all commodity names from parameter endpoint...")
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()

        commodity_names = response.json().get('commodity_desc', [])
        print(f"  → Found {len(commodity_names)} commodity names")

        # Convert to our format (without codes, since we'd need heavy data queries)
        commodities = []
        for i, name in enumerate(commodity_names, 1):
            commodities.append({
                'code': f"API_{i:06d}",  # Temporary placeholder codes
                'name': name,
                'description': name,
                'source': 'NASS_API_PARAMS',
                'fetched_at': datetime.now().isoformat()
            })

        return commodities

    except Exception as e:
        print(f"  → API parameter query also failed: {e}")
        return []


def fetch_ca_commodities_fallback() -> List[Dict]:
    """
    Last resort: Simple manual commodity list for basic functionality.
    """
    print("  → Using minimal fallback commodity list...")

    # Basic commodity list that covers most common agricultural products
    basic_commodities = [
        {'code': '10199999', 'name': 'WHEAT', 'description': 'Wheat'},
        {'code': '11199199', 'name': 'CORN', 'description': 'Corn for grain'},
        {'code': '12199199', 'name': 'RICE', 'description': 'Rice'},
        {'code': '16199199', 'name': 'SORGHUM', 'description': 'Sorghum for grain'},
        {'code': '21199999', 'name': 'BEANS', 'description': 'Beans, dry edible'},
        {'code': '22199999', 'name': 'PEAS', 'description': 'Peas, dry'},
        {'code': '24199999', 'name': 'LENTILS', 'description': 'Lentils'},
        {'code': '26199999', 'name': 'ALMONDS', 'description': 'Almonds'},
        {'code': '27199999', 'name': 'WALNUTS', 'description': 'Walnuts'},
        {'code': '31199999', 'name': 'STRAWBERRIES', 'description': 'Strawberries'},
        {'code': '35199999', 'name': 'GRAPES', 'description': 'Grapes'},
        {'code': '37899999', 'name': 'TOMATOES', 'description': 'Tomatoes'},
        {'code': '41299999', 'name': 'LETTUCE', 'description': 'Lettuce'},
        {'code': '43199999', 'name': 'SPINACH', 'description': 'Spinach'},
        {'code': '45199999', 'name': 'CARROTS', 'description': 'Carrots'},
        {'code': '51199999', 'name': 'HAY', 'description': 'Hay, alfalfa'},
    ]

    for commodity in basic_commodities:
        commodity['source'] = 'FALLBACK'
        commodity['fallback_at'] = datetime.now().isoformat()

    print(f"  → Loaded {len(basic_commodities)} basic commodities")
    return basic_commodities


def load_ca_commodities() -> List[Dict]:
    """Load CA commodities from cache or fetch if not cached"""
    if CA_COMMODITIES_CACHE.exists():
        with open(CA_COMMODITIES_CACHE) as f:
            import json
            commodities = json.load(f)
        print(f"Loaded {len(commodities)} commodities from cache")
        return commodities
    else:
        print("Cache not found. Fetching from NASS API...")
        return fetch_ca_commodities()


def populate_usda_commodities_to_database():
    """
    Load all scraped USDA commodities into the usda_commodity table.
    This ensures we have a complete reference list in the database.
    """
    print("\n" + "=" * 80)
    print("POPULATING ALL USDA COMMODITIES TO DATABASE")
    print("=" * 80)

    commodities = load_ca_commodities()

    if not commodities:
        print("No commodities to populate. Run --fetch-ca-commodities first.")
        return

    db_url = os.getenv('DATABASE_URL')
    engine = create_engine(db_url)

    # The URL we scraped from
    source_uri = "https://www.nass.usda.gov/Data_and_Statistics/County_Data_Files/Frequently_Asked_Questions/commcodes.php"

    inserted_count = 0
    existing_count = 0

    with engine.connect() as conn:
        for commodity in commodities:
            # TODO: Switch to ON CONFLICT after adding UNIQUE constraint on usda_code
            # This requires: ALTER TABLE usda_commodity ADD CONSTRAINT usda_commodity_code_unique UNIQUE (usda_code);
            #
            # Option 1: INSERT IGNORE (skip duplicates)
            # conn.execute(text("""
            #     INSERT INTO usda_commodity (name, usda_code, usda_source, description, uri)
            #     VALUES (:name, :code, :source, :description, :uri)
            #     ON CONFLICT (usda_code) DO NOTHING
            # """), {...})
            #
            # Option 2: UPSERT (update if exists, insert if new)
            # conn.execute(text("""
            #     INSERT INTO usda_commodity (name, usda_code, usda_source, description, uri)
            #     VALUES (:name, :code, :source, :description, :uri)
            #     ON CONFLICT (usda_code)
            #     DO UPDATE SET
            #         name = EXCLUDED.name,
            #         description = EXCLUDED.description,
            #         uri = EXCLUDED.uri,
            #         usda_source = EXCLUDED.usda_source
            # """), {...})

            # Current approach: Check-then-insert (works without constraints)
            # Check if commodity already exists
            check_existing = conn.execute(text(
                "SELECT id FROM usda_commodity WHERE usda_code = :code"
            ), {'code': commodity['code']})

            if check_existing.scalar():
                existing_count += 1
                continue

            # Insert new commodity
            conn.execute(text(
                """
                INSERT INTO usda_commodity (name, usda_code, usda_source, description, uri)
                VALUES (:name, :code, :source, :description, :uri)
                """
            ), {
                'name': commodity['name'],
                'code': commodity['code'],
                'source': commodity.get('source', 'NASS_WEB'),
                'description': commodity.get('description', commodity['name']),
                'uri': source_uri
            })
            inserted_count += 1

            if inserted_count % 100 == 0:
                print(f"  → Inserted {inserted_count} commodities...")

        conn.commit()

    print(f"\n✓ Inserted {inserted_count} new commodities")
    print(f"→ {existing_count} commodities already existed")
    print(f"✓ Total commodities in database: {inserted_count + existing_count}")


# ============================================================================
# STEP 2: Get project resources and primary_ag_products
# ============================================================================

def get_project_resources() -> List[Dict]:
    """
    Get all resources and primary_ag_products from your database.

    Returns:
        List of {id, name, type, table} dicts
    """
    print("\n" + "=" * 80)
    print("STEP 2: Loading Project Resources")
    print("=" * 80)

    db_url = os.getenv('DATABASE_URL')
    engine = create_engine(db_url)

    resources = []

    with engine.connect() as conn:
        # Get primary_ag_products
        try:
            result = conn.execute(text(
                'SELECT id, name FROM primary_ag_product WHERE name IS NOT NULL ORDER BY name'
            ))
            for row in result:
                resources.append({
                    'id': row[0],
                    'name': row[1],
                    'type': 'primary_ag_product',
                    'table': 'primary_ag_product'
                })
        except Exception as e:
            print(f"Warning: Could not load primary_ag_products: {e}")

        # Get resources (if table exists)
        try:
            result = conn.execute(text(
                'SELECT id, name FROM resource WHERE name IS NOT NULL ORDER BY name LIMIT 200'
            ))
            for row in result:
                resources.append({
                    'id': row[0],
                    'name': row[1],
                    'type': 'resource',
                    'table': 'resource'
                })
        except Exception as e:
            print(f"Note: Resource table not queried: {e}")

    print(f"OK Loaded {len(resources)} project resources/crops")
    return resources


# ============================================================================
# STEP 3: Fuzzy matching logic
# ============================================================================

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate normalized string similarity (0-1)"""
    return SequenceMatcher(None, text1.lower().strip(), text2.lower().strip()).ratio()


def lookup_manual_commodity_code(commodity_code: str) -> Optional[Dict]:
    """
    Lookup a USDA commodity by code in the database.
    Returns commodity dict if found, None if not found.
    """
    from ca_biositing.datamodels.database import get_session_local
    from ca_biositing.datamodels.schemas.generated.ca_biositing import UsdaCommodity

    try:
        session = get_session_local()()  # Get actual session instance

        # Look up commodity by code
        commodity = session.query(UsdaCommodity).filter(
            UsdaCommodity.usda_code == commodity_code
        ).first()

        if commodity:
            return {
                'code': commodity.usda_code,
                'name': commodity.name,
                'description': commodity.name,  # Using name as description
                'source': 'manual_lookup'
            }
        else:
            return None

    except Exception as e:
        print(f"Database error during manual lookup: {e}")
        return None
    finally:
        session.close()


def find_best_matches(resource_name: str, usda_commodities: List[Dict], top_n: int = 8) -> List[Dict]:
    """
    Find top N best matching USDA commodities for a resource name.
    Uses improved matching logic that considers partial word matches.

    Returns:
        List of {code, name, description, score} sorted by score descending
    """
    matches = []

    # Clean resource name for better matching
    resource_clean = resource_name.lower().strip()
    resource_words = set(resource_clean.replace('-', ' ').replace('_', ' ').split())

    for commodity in usda_commodities:
        commodity_name = commodity['name']
        commodity_desc = commodity.get('description', commodity_name)

        # Calculate multiple similarity scores

        # 1. Full string similarity (original method)
        full_name_score = calculate_similarity(resource_name, commodity_name)
        full_desc_score = calculate_similarity(resource_name, commodity_desc)

        # 2. Word-based similarity (new method for better partial matches)
        commodity_words = set(commodity_name.lower().replace('-', ' ').replace('_', ' ').split())
        desc_words = set(commodity_desc.lower().replace('-', ' ').replace('_', ' ').split())

        # Calculate word overlap scores
        if resource_words and commodity_words:
            word_overlap_name = len(resource_words & commodity_words) / len(resource_words | commodity_words)
        else:
            word_overlap_name = 0

        if resource_words and desc_words:
            word_overlap_desc = len(resource_words & desc_words) / len(resource_words | desc_words)
        else:
            word_overlap_desc = 0

        # 3. Key word match (exact word matches get bonus)
        key_words = resource_words - {'for', 'and', 'the', 'of', 'all', '-', 'processing'}  # Remove common words
        commodity_key_words = commodity_words - {'for', 'and', 'the', 'of', 'all', '-'}

        if key_words and commodity_key_words:
            key_word_match = len(key_words & commodity_key_words) / len(key_words)
        else:
            key_word_match = 0

        # Calculate final score as weighted combination
        scores = [
            full_name_score * 0.4,      # Original method
            full_desc_score * 0.2,      # Description match
            word_overlap_name * 0.3,    # Word overlap (important for partial matches)
            key_word_match * 0.1        # Exact key word match bonus
        ]

        final_score = sum(scores)

        # Special boost: If any resource word (>3 chars) appears in commodity name, ensure it's considered
        # This handles cases like "almond shells" → "ALMONDS"
        resource_key_words = [w for w in resource_words if len(w) > 3 and w not in {'hulls', 'shells', 'straw', 'processing', 'waste'}]
        commodity_name_lower = commodity_name.lower()

        for word in resource_key_words:
            # Check if resource word is contained in commodity name (handles plural, etc.)
            if word in commodity_name_lower or any(word in cw for cw in commodity_words):
                final_score = max(final_score, 0.75)  # Ensure it gets into top candidates
                break

        matches.append({
            'code': commodity['code'],
            'name': commodity['name'],
            'description': commodity.get('description', commodity['name']),
            'score': final_score,
            'source': commodity.get('source', 'NASS'),
            'debug_scores': {
                'full_name': full_name_score,
                'word_overlap': word_overlap_name,
                'key_word_match': key_word_match
            }
        })

    # Sort by score descending
    matches.sort(key=lambda x: x['score'], reverse=True)

    return matches[:top_n]


# ============================================================================
# STEP 4: Auto-match high-confidence matches
# ============================================================================

def auto_match_clear_matches(resources: List[Dict], usda_commodities: List[Dict], threshold: float = 0.90):
    """
    Automatically match resources with USDA commodities when similarity > threshold.
    """
    print("\n" + "=" * 80)
    print(f"STEP 3: Auto-Matching Clear Matches (>{threshold:.0%} similarity)")
    print("=" * 80)

    auto_matches = []
    pending_review = []

    for resource in resources:
        matches = find_best_matches(resource['name'], usda_commodities, top_n=8)

        if not matches:
            continue

        best_match = matches[0]

        if best_match['score'] >= threshold:
            # Clear match - auto-approve as DIRECT_MATCH
            auto_matches.append({
                'resource': resource,
                'usda_commodity': best_match,
                'status': 'auto_matched',
                'match_tier': 'DIRECT_MATCH',  # Auto-matches are considered direct
                'matched_at': datetime.now().isoformat()
            })
            print(f"OK AUTO: {resource['name']} -> {best_match['name']} ({best_match['score']:.1%})")
        else:
            # ALL other resources go to manual review (no threshold filter)
            pending_review.append({
                'resource': resource,
                'candidates': matches[:8],  # Top 8 candidates
                'status': 'pending_review'
            })
            print(f"? REVIEW: {resource['name']} (best: {best_match['name']} @ {best_match['score']:.1%})")

    print(f"\nOK Auto-matched: {len(auto_matches)}")
    print(f"? Pending manual review: {len(pending_review)}")
    print(f"Total resources: {len(resources)}")

    # Save auto-matches to approved file
    save_approved_matches(auto_matches)

    # Save pending for interactive review
    save_pending_matches(pending_review)

    return auto_matches, pending_review


# ============================================================================
# STEP 5: Interactive review of fuzzy matches
# ============================================================================

def interactive_review():
    """
    Present fuzzy match candidates (1-5) for user to select best match.
    """
    print("\n" + "=" * 80)
    print("STEP 4: Interactive Review of Fuzzy Matches")
    print("=" * 80)

    pending = load_pending_matches()

    if not pending:
        print("No pending matches to review. Run --auto-match first.")
        return

    approved = load_approved_matches()

    print(f"\nYou have {len(pending)} resources with fuzzy matches to review.")
    if approved:
        print(f"Already completed: {len(approved)} matches")
    print()
    print("For each resource, select the best USDA commodity match:")
    print("  - Enter 1-8 to select a candidate")
    print("  - Enter 'n' to skip (no good match)")
    print("  - Enter 'm' for manual commodity code entry")
    print("  - Enter 'u' to undo last match (if any)")
    print("  - Enter 'q' to quit and save progress")
    print("\nMatch Types:")
    print("  - DIRECT_MATCH: Resource/crop exactly matches the USDA commodity")
    print("  - CROP_FALLBACK: Resource not represented, using parent crop")
    print("  - AGGREGATE_PARENT: Resource is component of broader commodity category\n")

    for i, item in enumerate(pending, 1):
        resource = item['resource']
        candidates = item['candidates']

        print(f"\n[{i}/{len(pending)}] Resource: '{resource['name']}' ({resource['type']})")
        print("-" * 80)

        for j, candidate in enumerate(candidates, 1):
            print(f"  [{j}] {candidate['name']} (code: {candidate['code']}) - {candidate['score']:.1%} match")

        print("\n  [n] No suitable match - mark as NO_MATCH")
        print("  [m] Manual entry - enter commodity code directly")
        undo_available = len(approved) > 0
        if undo_available:
            print(f"  [u] Undo last match ({approved[-1]['resource']['name']} → {approved[-1]['usda_commodity']['name']})")
        print()

        while True:
            prompt = "Your selection (1-8, n, m"
            if undo_available:
                prompt += ", u"
            prompt += ", or q): "
            choice = input(f"\n{prompt}").strip().lower()

            if choice == 'q':
                print("\nSaving progress and exiting...")
                save_pending_matches(pending[i:])  # Save remaining items
                save_approved_matches(approved)
                return

            if choice == 'n':
                print(f"  → Skipping '{resource['name']}' (no match)")
                break

            if choice == 'm':
                print("\nManual commodity code entry:")
                while True:
                    manual_code = input("Enter USDA commodity code (8 digits, or 'q' to cancel): ").strip().lower()

                    if manual_code == 'q':
                        print("  → Cancelled manual entry")
                        break  # Exit manual entry, go back to main menu

                    if len(manual_code) == 8 and manual_code.isdigit():
                        # Look up the commodity in the database
                        manual_commodity = lookup_manual_commodity_code(manual_code)

                        if manual_commodity:
                            print(f"\nFound: {manual_commodity['name']} (code: {manual_commodity['code']})")

                            # Ask for match tier
                            print("\nWhat type of match is this?")
                            print("  [d] DIRECT_MATCH - exact same commodity")
                            print("  [c] CROP_FALLBACK - parent crop (resource not directly represented)")
                            print("  [r] RELATED_GROUP - resource is component of broader commodity")

                            while True:
                                tier_choice = input("\nMatch tier (d/c/r): ").strip().lower()

                                if tier_choice == 'd':
                                    match_tier = 'DIRECT_MATCH'
                                    break
                                elif tier_choice == 'c':
                                    match_tier = 'CROP_FALLBACK'
                                    break
                                elif tier_choice == 'r':
                                    match_tier = 'RELATED_GROUP'
                                    break
                                else:
                                    print("  Invalid choice. Enter 'd', 'c', or 'r'.")

                            approved.append({
                                'resource': resource,
                                'usda_commodity': manual_commodity,
                                'match_tier': match_tier,
                                'similarity': 1.0  # Manual matches get 100% similarity
                            })
                            print(f"  ✓ Matched '{resource['name']}' to '{manual_commodity['name']}' (MANUAL_{match_tier})")
                            break  # Exit manual entry loop
                        else:
                            print(f"\nError: Commodity code '{manual_code}' not found in database.")
                            print("Please add this commodity to the usda_commodity table first using:")
                            print(f"  pixi run -e default python enhanced_commodity_mapper.py --populate-commodities")
                            print("Or verify the correct code from USDA NASS website.\n")
                            continue  # Ask for code again
                    else:
                        print("Invalid format. Please enter exactly 8 digits.")
                        continue
                break  # Exit main choice loop after successful manual entry

            if choice == 'u':
                if approved:
                    last_match = approved.pop()  # Remove last match
                    # Put the resource back at the beginning of pending for re-review
                    pending.insert(i, {
                        'resource': last_match['resource'],
                        'candidates': find_best_matches(last_match['resource']['name'], load_usda_commodities())
                    })
                    print(f"\n  ↶ Undid match: '{last_match['resource']['name']}' → '{last_match['usda_commodity']['name']}'")
                    print(f"    Resource moved back to pending review.")
                    continue  # Stay on current resource, but now we have one more pending
                else:
                    print("\n  No matches to undo.")
                    continue

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(candidates):
                    selected = candidates[idx]

                    # Ask for match tier
                    print(f"\nSelected: {selected['name']} (code: {selected['code']})")
                    print("\nWhat type of match is this?")
                    print("  [d] DIRECT_MATCH - exact same commodity")
                    print("  [c] CROP_FALLBACK - parent crop (resource not directly represented)")
                    print("  [r] RELATED_GROUP - resource is component of broader commodity")

                    while True:
                        tier_choice = input("\nMatch tier (d/c/r): ").strip().lower()

                        if tier_choice == 'd':
                            match_tier = 'DIRECT_MATCH'
                            break
                        elif tier_choice == 'c':
                            match_tier = 'CROP_FALLBACK'
                            break
                        elif tier_choice == 'r':
                            match_tier = 'RELATED_GROUP'
                            break
                        else:
                            print("  Invalid choice. Enter 'd', 'c', or 'r'.")

                    approved.append({
                        'resource': resource,
                        'usda_commodity': selected,
                        'status': 'user_approved',
                        'match_tier': match_tier,
                        'matched_at': datetime.now().isoformat()
                    })
                    print(f"  ✓ Matched: {resource['name']} → {selected['name']} ({match_tier})")
                    break
                else:
                    print("  Invalid choice. Try again.")
            except ValueError:
                print("  Invalid input. Enter a number (1-8), 'n', or 'q'.")

    print(f"\n✓ Review complete! {len(approved)} total resource mappings created.")

    # Clear pending (all reviewed)
    save_pending_matches([])
    save_approved_matches(approved)


# ============================================================================
# STEP 6: Save approved mappings to database
# ============================================================================

def save_mappings_to_database():
    """
    Insert approved mappings into resource_usda_commodity_map table.
    """
    print("\n" + "=" * 80)
    print("STEP 5: Saving Approved Mappings to Database")
    print("=" * 80)

    approved = load_approved_matches()

    if not approved:
        print("No approved matches to save. Run --review first.")
        return

    db_url = os.getenv('DATABASE_URL')
    engine = create_engine(db_url)

    print(f"\nSaving {len(approved)} mappings to database...")

    saved_count = 0
    skipped_count = 0
    updated_count = 0

    with engine.connect() as conn:
        for item in approved:
            resource = item['resource']
            commodity = item.get('usda_commodity')  # May be None for NO_MATCH
            match_tier = item.get('match_tier', 'USER_APPROVED')  # Get specified tier

            # Handle NO_MATCH case
            if not commodity:
                # Determine which column to use
                if resource['type'] == 'primary_ag_product':
                    field_name = 'primary_ag_product_id'
                else:
                    field_name = 'resource_id'

                # Insert NO_MATCH record
                conn.execute(text(f"""
                    INSERT INTO resource_usda_commodity_map
                    ({field_name}, usda_commodity_id, match_tier, note, created_at, updated_at)
                    VALUES (:resource_id, NULL, 'NO_MATCH', :note, NOW(), NOW())
                """), {
                    'resource_id': resource['id'],
                    'note': f"Reviewed and marked as NO_MATCH - no suitable USDA commodity found - {datetime.now().isoformat()}"
                })
                saved_count += 1
                print(f"  ✓ Saved: {resource['name']} → NO_MATCH")
                conn.commit()
                continue

            # Handle commodity matches (existing logic)

            # First, ensure USDA commodity exists in usda_commodity table
            check_commodity = conn.execute(text(
                "SELECT id FROM usda_commodity WHERE usda_code = :code"
            ), {'code': commodity['code']})

            commodity_id = check_commodity.scalar()

            if not commodity_id:
                # Insert USDA commodity with parent tracking support
                # TODO: Add created_at and updated_at columns to usda_commodity table schema
                # This would require an Alembic migration to add these timestamp columns
                # for better data auditing and tracking when commodities are added/modified
                source_uri = "https://www.nass.usda.gov/Data_and_Statistics/County_Data_Files/Frequently_Asked_Questions/commcodes.php"
                result = conn.execute(text(
                    """
                    INSERT INTO usda_commodity (name, usda_code, usda_source, description, uri)
                    VALUES (:name, :code, :source, :description, :uri)
                    RETURNING id
                    """
                ), {
                    'name': commodity['name'],
                    'code': commodity['code'],
                    'source': commodity.get('source', 'NASS_WEB'),
                    'description': commodity.get('description', commodity['name']),
                    'uri': source_uri
                })
                commodity_id = result.scalar()
                print(f"  + Created USDA commodity: {commodity['name']} (code: {commodity['code']})")

            # Determine which column to use (primary_ag_product_id or resource_id)
            if resource['type'] == 'primary_ag_product':
                field_name = 'primary_ag_product_id'
            else:
                field_name = 'resource_id'

            # Check if mapping already exists
            existing_mapping = conn.execute(text(f"""
                SELECT id, match_tier, note FROM resource_usda_commodity_map
                WHERE {field_name} = :resource_id
            """), {'resource_id': resource['id']})

            existing = existing_mapping.fetchone()

            # Get the match tier from the item - use modern structure
            match_tier = item.get('match_tier', 'USER_APPROVED')  # Default to USER_APPROVED if no tier specified
            similarity = item.get('similarity', commodity.get('score', 0))
            note = f"Matched by enhanced_commodity_mapper.py - user_approved - {match_tier} - similarity: {similarity:.2%} - {datetime.now().isoformat()}"

            if existing:
                # Update existing mapping
                conn.execute(text(f"""
                    UPDATE resource_usda_commodity_map
                    SET usda_commodity_id = :commodity_id,
                        match_tier = :match_tier,
                        note = :note,
                        updated_at = NOW()
                    WHERE id = :mapping_id
                """), {
                    'commodity_id': commodity_id,
                    'match_tier': match_tier,
                    'note': note,
                    'mapping_id': existing[0]
                })
                updated_count += 1
                print(f"  ↻ Updated: {resource['name']} → {commodity['name']} ({match_tier})")
            else:
                # Create new mapping
                conn.execute(text(f"""
                    INSERT INTO resource_usda_commodity_map
                    ({field_name}, usda_commodity_id, match_tier, note, created_at, updated_at)
                    VALUES (:resource_id, :commodity_id, :match_tier, :note, NOW(), NOW())
                """), {
                    'resource_id': resource['id'],
                    'commodity_id': commodity_id,
                    'match_tier': match_tier,
                    'note': note
                })
                saved_count += 1
                print(f"  ✓ Saved: {resource['name']} → {commodity['name']} ({match_tier})")

            conn.commit()

    print(f"\n✓ Saved {saved_count} new mappings")
    print(f"↻ Updated {updated_count} existing mappings")
    print(f"⚠ Skipped {skipped_count} unchanged mappings")

    # Clear the approved matches since they've been saved
    save_approved_matches([])
    print(f"✓ Cleared approved matches cache")


def save_unmatched_resources_to_database():
    """
    Save all resources to the mapping table, even if they don't have matches yet.
    This helps track mapping progress by showing which resources still need attention.
    """
    print("\n" + "=" * 80)
    print("TRACKING UNMAPPED RESOURCES FOR PROGRESS")
    print("=" * 80)

    resources = get_project_resources()

    if not resources:
        print("No resources found to track.")
        return

    db_url = os.getenv('DATABASE_URL')
    engine = create_engine(db_url)

    unmapped_count = 0
    already_mapped_count = 0

    with engine.connect() as conn:
        for resource in resources:
            # Determine which column to check
            if resource['type'] == 'primary_ag_product':
                field_name = 'primary_ag_product_id'
            else:
                field_name = 'resource_id'

            # Check if resource is already in mapping table
            existing_check = conn.execute(text(f"""
                SELECT id FROM resource_usda_commodity_map
                WHERE {field_name} = :resource_id
            """), {'resource_id': resource['id']})

            if existing_check.scalar():
                already_mapped_count += 1
                continue

            # Insert unmapped resource placeholder
            conn.execute(text(f"""
                INSERT INTO resource_usda_commodity_map
                ({field_name}, usda_commodity_id, match_tier, note, created_at, updated_at)
                VALUES (:resource_id, NULL, 'UNMAPPED', :note, NOW(), NOW())
            """), {
                'resource_id': resource['id'],
                'note': f"Resource tracked for mapping progress - unmapped as of {datetime.now().isoformat()}"
            })
            unmapped_count += 1
            print(f"  → Tracked unmapped: {resource['name']} ({resource['type']})")

        conn.commit()

    print(f"\n→ Tracked {unmapped_count} unmapped resources for progress monitoring")
    print(f"→ {already_mapped_count} resources already had mappings")
    print(f"✓ Total resources now tracked in mapping table")
    print(f"\nTip: Use --manage to view all resources and their mapping status!")


def manage_commodity_mappings():
    """
    Interactive tool to view and edit existing commodity mappings.
    """
    print("\n" + "=" * 80)
    print("COMMODITY MAPPING MANAGEMENT")
    print("=" * 80)

    db_url = os.getenv('DATABASE_URL')
    engine = create_engine(db_url)

    while True:
        print("\nOptions:")
        print("  [1] View all mappings")
        print("  [2] Edit a specific mapping")
        print("  [3] Delete a mapping")
        print("  [4] Search for unmapped resources")
        print("  [q] Quit")

        choice = input("\nSelect option: ").strip().lower()

        if choice == 'q':
            break
        elif choice == '1':
            view_all_mappings(engine)
        elif choice == '2':
            edit_mapping(engine)
        elif choice == '3':
            delete_mapping(engine)
        elif choice == '4':
            find_unmapped_resources(engine)
        else:
            print("Invalid choice. Try again.")


def view_all_mappings(engine):
    """View all current commodity mappings"""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                m.id,
                COALESCE(r.name, 'No Resource') as resource_name,
                COALESCE(pap.name, 'No Crop') as crop_name,
                COALESCE(uc.name, 'No Commodity') as usda_commodity,
                uc.usda_code,
                m.match_tier,
                m.note,
                m.updated_at
            FROM resource_usda_commodity_map m
                LEFT JOIN resource r ON m.resource_id = r.id
                LEFT JOIN primary_ag_product pap ON m.primary_ag_product_id = pap.id
                LEFT JOIN usda_commodity uc ON m.usda_commodity_id = uc.id
            ORDER BY r.name, pap.name
        """))

        mappings = result.fetchall()

        if not mappings:
            print("No mappings found.")
            return

        print(f"\nFound {len(mappings)} mappings:")
        print("-" * 120)
        print(f"{'ID':<4} {'Resource':<25} {'Crop':<20} {'USDA Commodity':<30} {'Code':<10} {'Tier':<15}")
        print("-" * 120)

        for mapping in mappings:
            print(f"{mapping[0]:<4} {mapping[1][:24]:<25} {mapping[2][:19]:<20} {mapping[3][:29]:<30} {mapping[4]:<10} {mapping[5]:<15}")


def edit_mapping(engine):
    """Edit a specific mapping"""
    mapping_id = input("Enter mapping ID to edit: ").strip()

    if not mapping_id.isdigit():
        print("Invalid ID")
        return

    # Load current mapping
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                m.id,
                m.resource_id,
                m.primary_ag_product_id,
                COALESCE(r.name, pap.name) as resource_name,
                uc.name as current_commodity,
                uc.usda_code,
                m.match_tier
            FROM resource_usda_commodity_map m
                LEFT JOIN resource r ON m.resource_id = r.id
                LEFT JOIN primary_ag_product pap ON m.primary_ag_product_id = pap.id
                LEFT JOIN usda_commodity uc ON m.usda_commodity_id = uc.id
            WHERE m.id = :mapping_id
        """), {'mapping_id': mapping_id})

        mapping = result.fetchone()

        if not mapping:
            print("Mapping not found")
            return

        print(f"\nCurrent mapping:")
        print(f"  Resource: {mapping[3]}")
        print(f"  USDA Commodity: {mapping[4]} (code: {mapping[5]})")
        print(f"  Match Tier: {mapping[6]}")

        # Get new commodity code
        new_code = input(f"\nEnter new USDA commodity code (or press Enter to cancel): ").strip()

        if not new_code:
            return

        # Check if commodity exists
        commodity_result = conn.execute(text("""
            SELECT id, name FROM usda_commodity WHERE usda_code = :code
        """), {'code': new_code})

        commodity = commodity_result.fetchone()

        if not commodity:
            print(f"USDA commodity code {new_code} not found")
            return

        # Update mapping
        conn.execute(text("""
            UPDATE resource_usda_commodity_map
            SET usda_commodity_id = :commodity_id,
                match_tier = 'USER_EDITED',
                note = :note,
                updated_at = NOW()
            WHERE id = :mapping_id
        """), {
            'commodity_id': commodity[0],
            'mapping_id': mapping_id,
            'note': f"Manually edited to {commodity[1]} ({new_code}) on {datetime.now().isoformat()}"
        })

        conn.commit()
        print(f"✓ Updated mapping: {mapping[3]} → {commodity[1]} ({new_code})")


def find_unmapped_resources(engine):
    """Find resources that don't have commodity mappings"""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, name, 'resource' as type FROM resource r
            WHERE r.id NOT IN (SELECT resource_id FROM resource_usda_commodity_map WHERE resource_id IS NOT NULL)
            UNION
            SELECT id, name, 'primary_ag_product' as type FROM primary_ag_product pap
            WHERE pap.id NOT IN (SELECT primary_ag_product_id FROM resource_usda_commodity_map WHERE primary_ag_product_id IS NOT NULL)
            ORDER BY name
        """))

        unmapped = result.fetchall()

        print(f"\nFound {len(unmapped)} unmapped resources:")
        for resource in unmapped:
            print(f"  {resource[1]} ({resource[2]})")

def delete_mapping(engine):
    """Delete a specific mapping"""
    mapping_id = input("Enter mapping ID to delete: ").strip()

    if not mapping_id.isdigit():
        print("Invalid ID")
        return

    # Show current mapping before deletion
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                m.id,
                COALESCE(r.name, pap.name) as resource_name,
                uc.name as commodity_name,
                uc.usda_code
            FROM resource_usda_commodity_map m
                LEFT JOIN resource r ON m.resource_id = r.id
                LEFT JOIN primary_ag_product pap ON m.primary_ag_product_id = pap.id
                LEFT JOIN usda_commodity uc ON m.usda_commodity_id = uc.id
            WHERE m.id = :mapping_id
        """), {'mapping_id': mapping_id})

        mapping = result.fetchone()

        if not mapping:
            print("Mapping not found")
            return

        print(f"\nMapping to delete:")
        print(f"  Resource: {mapping[1]}")
        print(f"  USDA Commodity: {mapping[2]} (code: {mapping[3]})")

        confirm = input(f"\nAre you sure you want to delete this mapping? (y/N): ").strip().lower()

        if confirm == 'y':
            conn.execute(text("DELETE FROM resource_usda_commodity_map WHERE id = :mapping_id"),
                        {'mapping_id': mapping_id})
            conn.commit()
            print(f"✓ Deleted mapping")
        else:
            print("Cancelled")


def find_unmapped_resources(engine):
    """Find resources that don't have commodity mappings"""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, name, 'resource' as type FROM resource r
            WHERE r.id NOT IN (SELECT resource_id FROM resource_usda_commodity_map WHERE resource_id IS NOT NULL)
            UNION
            SELECT id, name, 'primary_ag_product' as type FROM primary_ag_product pap
            WHERE pap.id NOT IN (SELECT primary_ag_product_id FROM resource_usda_commodity_map WHERE primary_ag_product_id IS NOT NULL)
            ORDER BY name
        """))

        unmapped = result.fetchall()

        print(f"\nFound {len(unmapped)} unmapped resources:")
        for resource in unmapped:
            print(f"  {resource[1]} ({resource[2]})")

        if unmapped:
            print(f"\nTo map these resources, run:")
            print(f"  python enhanced_commodity_mapper.py --auto-match --review --save")


# ============================================================================
# File I/O helpers
# ============================================================================

def load_pending_matches() -> List[Dict]:
    """Load pending matches from file"""
    if PENDING_MATCHES_FILE.exists():
        with open(PENDING_MATCHES_FILE) as f:
            return json.load(f)
    return []


def save_pending_matches(pending: List[Dict]):
    """Save pending matches to file"""
    with open(PENDING_MATCHES_FILE, 'w') as f:
        json.dump(pending, f, indent=2)


def load_approved_matches() -> List[Dict]:
    """Load approved matches from file"""
    if APPROVED_MATCHES_FILE.exists():
        with open(APPROVED_MATCHES_FILE) as f:
            return json.load(f)
    return []


def save_approved_matches(approved: List[Dict]):
    """Save approved matches to file"""
    with open(APPROVED_MATCHES_FILE, 'w') as f:
        json.dump(approved, f, indent=2)


# ============================================================================
# Main CLI
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Enhanced USDA Commodity Mapper with Interactive Fuzzy Matching"
    )
    parser.add_argument('--fetch-ca-commodities', action='store_true',
                       help='Fetch all CA USDA commodities from NASS API')
    parser.add_argument('--auto-match', action='store_true',
                       help='Auto-match clear matches (>90%% similarity)')
    parser.add_argument('--review', action='store_true',
                       help='Interactively review fuzzy matches')
    parser.add_argument('--save', action='store_true',
                       help='Save approved mappings to database')
    parser.add_argument('--full-workflow', action='store_true',
                       help='Run complete workflow (fetch → auto-match → review → save)')
    parser.add_argument('--manage', action='store_true',
                       help='Interactive mapping management (view, edit, delete mappings)')
    parser.add_argument('--populate-commodities', action='store_true',
                        help='Populate all scraped commodities into database')

    args = parser.parse_args()

    if args.fetch_ca_commodities or args.full_workflow:
        commodities = fetch_ca_commodities()
        print(f"\n✓ Fetched and cached {len(commodities)} commodities.")
        if not args.full_workflow:
            print("\n💡 Next step: Run --populate-commodities to load them into the database")

    if args.populate_commodities or args.full_workflow:
        populate_usda_commodities_to_database()

    if args.auto_match or args.full_workflow:
        commodities = load_ca_commodities()
        resources = get_project_resources()
        auto_match_clear_matches(resources, commodities)

    if args.review or args.full_workflow:
        interactive_review()

    if args.save or args.full_workflow:
        save_mappings_to_database()

    if args.manage:
        manage_commodity_mappings()

    if not any(vars(args).values()):
        parser.print_help()


if __name__ == "__main__":
    main()
