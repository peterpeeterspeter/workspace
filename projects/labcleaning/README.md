# Lab Cleaning Suppliers Database

Scraped database of US laboratory cleaning suppliers and service providers for **labcleaning.com**.

## Files Generated

### 1. **lab_suppliers.json** (86 companies)
Complete list of lab supply manufacturers, distributors, and service providers.

**Columns:**
- `name` - Company name
- `url` - Company website
- `type` - Category (manufacturer/distributor/service)
- `description` - Brief description

### 2. **suppliers_manufacturer.json** (64 companies)
Lab equipment and chemical manufacturers.

### 3. **suppliers_distributor.json** (14 companies)
Lab supply distributors (VWR, Fisher Scientific, etc.)

### 4. **suppliers_service.json** (8 companies)
Lab service and cleaning companies.

### 5. **lab_cleaning_services.json** (70 companies)
**Most relevant for labcleaning.com** - Specialized lab cleaning and decontamination services.

**Categories:**
- `cleaning_service` - Lab cleaning and decontamination
- `sterilization` - Lab sterilization services (STERIS, etc.)
- `cleaning_products` - Lab cleaning chemicals (Ecolab, 3M, etc.)
- `waste_management` - Lab waste disposal
- `lab_decommissioning` - Lab closure and decontamination
- `lab_services` - Equipment maintenance and calibration
- `equipment_manufacturer` - Safety equipment (fume hoods, biosafety cabinets)
- `software` - LIMS and management software
- `marketplace` - Lab service marketplaces

## Usage

### Load Data in Python

```python
import json

# Load lab cleaning services (most relevant)
with open('lab_cleaning_services.json', 'r') as f:
    services = json.load(f)

# Filter by type
cleaning_companies = [s for s in services if s['type'] == 'cleaning_service']
sterilization = [s for s in services if s['type'] == 'sterilization']
waste_management = [s for s in services if s['type'] == 'waste_management']

# Search by service
lab_decontamination = [s for s in services if any('decontamination' in svc.lower() for svc in s.get('services', []))]
```

### Import to WordPress

```bash
# Convert CSV to WordPress import format
python3 csv_to_wordpress.py lab_cleaning_services.csv

# Or use WP-CLI
wp post import lab_cleaning_services.csv --user=yourusername
```

### Import to Database

```sql
-- Create table
CREATE TABLE lab_suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    url VARCHAR(255),
    type VARCHAR(50),
    description TEXT,
    emails JSON,
    phones JSON,
    services JSON,
    scraped_at DATETIME
);

-- Import from CSV
LOAD DATA LOCAL INFILE 'lab_cleaning_services.csv'
INTO TABLE lab_suppliers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

## Data Fields

Each company includes:

- **Basic Info:**
  - `name` - Company name
  - `url` - Website URL
  - `type` - Company category
  - `description` - Description of services

- **Contact Info:**
  - `emails` - List of email addresses found
  - `phones` - List of phone numbers found
  - `title` - Page title from website
  - `meta_description` - Meta description from website

- **Service Details:**
  - `services` - List of services offered
  - `scraped_at` - Timestamp of data collection

## Top Lab Cleaning Services

### Lab Decontamination & Cleaning
1. **Triumvirate Environmental** - Laboratory cleaning, decontamination, waste management
2. **Clean Harbors** - Lab decontamination and hazardous waste
3. **Noxilico** - Lab decontamination and decommissioning

### Sterilization
1. **STERIS** - Lab sterilization and infection prevention
2. **3M Health Care** - Disinfectants and sanitization

### Cleaning Products
1. **Ecolab** - Cleaning and sanitizing solutions
2. **Diversey** - Cleaning and hygiene solutions
3. **CloroxPro** - Professional disinfection

### Waste Management
1. **Stericycle** - Medical and lab waste disposal
2. **Clean Harbors** - Hazardous waste services
3. **Waste Management** - Comprehensive waste services

## Next Steps for labcleaning.com

### 1. Create Supplier Listings
- Import data as custom post type
- Add contact forms for each supplier
- Include reviews and ratings

### 2. Build Directories
- By state (CA, NY, TX, etc.)
- By service type (decontamination, sterilization, waste)
- By facility type (research lab, medical lab, industrial)

### 3. Monetization
- Claimed listings (suppliers pay to claim)
- Featured placements
- Lead generation (contact forms)
- Affiliate links for products

### 4. SEO
- "Lab cleaning services [state]"
- "Laboratory decontamination companies"
- "Lab waste disposal near me"
- "Biosafety cabinet certification [city]"

### 5. Content Marketing
- "How to choose a lab cleaning service"
- "Lab decontamination checklist"
- "Guide to lab waste disposal regulations"
- "Biosafety cabinet certification requirements"

## Data Quality

- **Emails:** Scraped from website content (may include general info emails)
- **Phones:** Extracted from web pages (may include multiple departments)
- **Services:** Based on company descriptions and service pages

**Recommendation:** Verify contact information before outreach. Consider:
- Calling to verify current services
- Checking for location-specific offices
- Verifying email addresses for the right department

## Scraping Details

- **Date:** 2026-02-19
- **Method:** Firecrawl + custom Python scraper
- **Sources:** Company websites and business directories
- **Rate limiting:** 2 second delays between requests

## Updates

To update the data:

```bash
# Run the scraper again
python3 scrape_lab_cleaning_services.py

# Merge with existing data
python3 merge_suppliers.py lab_cleaning_services.json lab_cleaning_services_new.json

# Re-export to CSV
python3 json_to_csv.py lab_cleaning_services_merged.json
```

## License

This data is scraped from public websites. Use for outreach and directory purposes only. Comply with all applicable laws and website terms of service.

## Contact

For questions about this data or scraping methodology, contact your development team.
