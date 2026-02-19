# FUTURE ENHANCEMENT TODO

## Full USDA API Commodity Mapping

**Context:** We currently map our 17 internal commodities to USDA API names.
However, the USDA API has 465 total commodities that could be valuable for a
more comprehensive agricultural data tool.

**Goal:** Create a complete mapping system for all 465 USDA NASS QuickStats API
commodities to support:

- Backend tools that aren't limited to our internal resource list
- Broader agricultural analysis beyond our current 17 crops
- Future expansion of commodity coverage

**Approach:**

1. **Extract all 465 API commodities** - Use the existing `get_param_values`
   endpoint
2. **Categorize commodities** - Group by type (crops, livestock, byproducts,
   etc.)
3. **Create comprehensive mapping structure** - Map to standardized names,
   categories, and hierarchies
4. **Store in stable format** - Database table or configuration file for easy
   access

**Files to create:**

- `comprehensive_commodity_mapping.py` - Full 465 commodity mapping (use
  `template_comprehensive_commodity_mapping.py` as starting point)
- `commodity_categories.py` - Classification system for commodity types
- `expand_commodity_coverage.py` - Tool to add new commodities to our system

**Existing references:**

- `template_comprehensive_commodity_mapping.py` - Template with original
  17-commodity logic
- `reviewed_api_mappings.py` - Validated mappings for current 17 commodities
- `review_api_mappings.py` pattern - Interactive validation approach

**Benefits:**

- Support for comprehensive agricultural data analysis
- Easy expansion of ETL coverage to new commodities
- Foundation for agricultural data API that covers more than our current crops

**Implementation priority:** Medium - valuable for future expansion but not
blocking current work

**Estimated effort:** 1-2 days to build comprehensive mapping system

---

_Added: 2026-02-05 - Full API commodity mapping for future expansion_
