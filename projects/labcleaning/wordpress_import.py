#!/usr/bin/env python3
"""
Convert lab suppliers data to WordPress import format
"""

import json
import csv

OUTPUT_DIR = "/root/.openclaw/workspace/projects/labcleaning"

def load_json(filename):
    """Load JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)

def create_wordpress_csv(suppliers, output_file):
    """Create WordPress-ready CSV file"""

    # WordPress custom post type structure
    fieldnames = [
        'post_title',          # Company name
        'post_content',        # Description
        'post_excerpt',        # Short description
        'post_status',         # publish/draft
        'post_type',          # supplier
        'meta_url',           # Website URL
        'meta_email',         # Email
        'meta_phone',         # Phone
        'meta_type',          # Company type
        'meta_services',      # Services (comma-separated)
        'meta_address',       # Address (if available)
        'categories'          # Comma-separated categories
    ]

    rows = []
    for supplier in suppliers:
        # Get services as string
        services = supplier.get('services', [])
        if isinstance(services, list):
            services_str = ', '.join(services)
        else:
            services_str = ''

        # Get first email
        emails = supplier.get('emails', [])
        email = emails[0] if emails else ''

        # Get first phone
        phones = supplier.get('phones', [])
        phone = phones[0] if phones else ''

        row = {
            'post_title': supplier.get('name', ''),
            'post_content': f"<p>{supplier.get('description', '')}</p>",
            'post_excerpt': supplier.get('description', '')[:150],
            'post_status': 'draft',  # Import as draft for review
            'post_type': 'lab_supplier',
            'meta_url': supplier.get('url', ''),
            'meta_email': email,
            'meta_phone': phone,
            'meta_type': supplier.get('type', ''),
            'meta_services': services_str,
            'meta_address': '',
            'categories': supplier.get('type', '')
        }
        rows.append(row)

    # Write CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ WordPress CSV created: {output_file}")
    print(f"   Total posts: {len(rows)}")

    return rows

def create_listing_pages(suppliers, output_file):
    """Create category listing pages"""

    # Group by type
    by_type = {}
    for supplier in suppliers:
        supplier_type = supplier.get('type', 'other')
        if supplier_type not in by_type:
            by_type[supplier_type] = []
        by_type[supplier_type].append(supplier)

    pages = []
    for supplier_type, type_suppliers in by_type.items():
        # Generate category page
        type_name = supplier_type.replace('_', ' ').title()

        # List suppliers
        supplier_list = '<ul class="supplier-list">'
        for supplier in type_suppliers:
            supplier_list += f'''
            <li>
                <strong><a href="{supplier.get('url', '')}">{supplier.get('name', '')}</a></strong><br>
                {supplier.get('description', '')}
            </li>'''
        supplier_list += '</ul>'

        content = f'''
<h1>{type_name} Lab Suppliers</h1>
<p>Directory of {type_name.lower()} suppliers serving laboratories in the United States.</p>
{supplier_list}
<p><strong>Total Suppliers:</strong> {len(type_suppliers)}</p>
'''

        page = {
            'post_title': f'{type_name} Lab Suppliers',
            'post_content': content,
            'post_excerpt': f'Directory of {len(type_suppliers)} {type_name.lower()} suppliers.',
            'post_status': 'draft',
            'post_type': 'page'
        }
        pages.append(page)

    # Save pages
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['post_title', 'post_content', 'post_excerpt', 'post_status', 'post_type']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(pages)

    print(f"✅ Category pages created: {output_file}")
    print(f"   Total pages: {len(pages)}")

    return pages

def main():
    """Main function"""
    print("📝 Creating WordPress Import Files")
    print("=" * 60)

    # Load lab cleaning services (most relevant for labcleaning.com)
    services = load_json(f"{OUTPUT_DIR}/lab_cleaning_services.json")
    print(f"📋 Loaded {len(services)} lab cleaning services")

    # Create WordPress CSV for suppliers
    supplier_csv = f"{OUTPUT_DIR}/wordpress_suppliers.csv"
    create_wordpress_csv(services, supplier_csv)

    # Create category pages
    pages_csv = f"{OUTPUT_DIR}/wordpress_pages.csv"
    create_listing_pages(services, pages_csv)

    # Also process general suppliers
    print("\n" + "=" * 60)
    suppliers = load_json(f"{OUTPUT_DIR}/lab_suppliers.json")
    print(f"📋 Loaded {len(suppliers)} general lab suppliers")

    general_csv = f"{OUTPUT_DIR}/wordpress_general_suppliers.csv"
    create_wordpress_csv(suppliers, general_csv)

    print("\n✅ All WordPress import files created!")
    print(f"\n📦 Files ready for import:")
    print(f"   - {supplier_csv}")
    print(f"   - {pages_csv}")
    print(f"   - {general_csv}")

    print(f"\n📖 Import instructions:")
    print(f"   1. Install WP All Import plugin")
    print(f"   2. Go to All Import → New Import")
    print(f"   3. Upload CSV file")
    print(f"   4. Map fields to custom post type")
    print(f"   5. Run import")

if __name__ == "__main__":
    main()
