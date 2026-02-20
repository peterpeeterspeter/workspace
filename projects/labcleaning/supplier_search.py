#!/usr/bin/env python3
"""
Simple search and filter interface for lab cleaning suppliers
"""

import json
from pathlib import Path

DATA_DIR = Path("/root/.openclaw/workspace/projects/labcleaning")

# Load data
with open(DATA_DIR / "lab_cleaning_services_enriched.json", 'r') as f:
    suppliers = json.load(f)

class SupplierSearch:
    def __init__(self, suppliers):
        self.suppliers = suppliers
    
    def search(self, query):
        """Search suppliers by name, description, or services"""
        query = query.lower()
        results = []
        
        for supplier in self.suppliers:
            # Search in name
            if query in supplier.get('name', '').lower():
                results.append(supplier)
                continue
            
            # Search in description
            if query in supplier.get('description', '').lower():
                results.append(supplier)
                continue
            
            # Search in services
            services = supplier.get('services', [])
            if any(query in service.lower() for service in services):
                results.append(supplier)
                continue
            
            # Search in emails
            emails = supplier.get('emails', [])
            if any(query in email.lower() for email in emails):
                results.append(supplier)
        
        return results
    
    def filter_by_state(self, state):
        """Filter suppliers by state"""
        return [s for s in self.suppliers if s.get('state', '').lower() == state.lower()]
    
    def filter_by_type(self, supplier_type):
        """Filter suppliers by type"""
        return [s for s in self.suppliers if s.get('type', '').lower() == supplier_type.lower()]
    
    def filter_by_service(self, service_keyword):
        """Filter suppliers that offer a specific service"""
        results = []
        for supplier in self.suppliers:
            services = supplier.get('services', [])
            if any(service_keyword.lower() in service.lower() for service in services):
                results.append(supplier)
        return results
    
    def has_email(self):
        """Get suppliers with email addresses"""
        return [s for s in self.suppliers if s.get('emails')]
    
    def has_address(self):
        """Get suppliers with physical addresses"""
        return [s for s in self.suppliers if s.get('address')]
    
    def has_phone(self):
        """Get suppliers with phone numbers"""
        return [s for s in self.suppliers if s.get('phones')]
    
    def get_public_companies(self):
        """Get publicly traded companies"""
        return [s for s in self.suppliers if s.get('ticker')]
    
    def get_by_revenue_tier(self, min_revenue):
        """Get companies by minimum revenue"""
        results = []
        for supplier in self.suppliers:
            revenue = supplier.get('revenue', '')
            if not revenue:
                continue
            
            # Parse revenue
            if 'B+' in revenue:
                amount = float(revenue.replace('$', '').replace('B+', '').replace('+', '')) * 1000000000
            elif 'M+' in revenue:
                amount = float(revenue.replace('$', '').replace('M+', '').replace('+', '')) * 1000000
            else:
                continue
            
            if amount >= min_revenue:
                results.append(supplier)
        
        return sorted(results, key=lambda x: x.get('revenue', ''), reverse=True)

# Example usage
if __name__ == '__main__':
    search = SupplierSearch(suppliers)
    
    print("🔍 Search Examples:\n")
    
    # Example 1: Search for decontamination services
    print("1. Companies offering 'decontamination':")
    results = search.filter_by_service('decontamination')
    for r in results[:5]:
        print(f"   - {r['name']}")
    print(f"   Total: {len(results)}\n")
    
    # Example 2: Filter by state
    print("2. Companies in Massachusetts:")
    results = search.filter_by_state('MA')
    for r in results:
        print(f"   - {r['name']} ({r.get('city', 'N/A')})")
    print(f"   Total: {len(results)}\n")
    
    # Example 3: Public companies
    print("3. Publicly traded companies:")
    results = search.get_public_companies()
    for r in results:
        print(f"   - {r['name']} ({r.get('ticker', 'N/A')}) - {r.get('revenue', 'N/A')}")
    print(f"   Total: {len(results)}\n")
    
    # Example 4: Companies with emails
    print("4. Companies with email addresses:")
    results = search.has_email()
    for r in results[:10]:
        emails = r.get('emails', [])
        print(f"   - {r['name']}: {emails[0] if emails else 'N/A'}")
    print(f"   Total: {len(results)}\n")
    
    # Example 5: Large companies (> $1B revenue)
    print("5. Companies with $1B+ revenue:")
    results = search.get_by_revenue_tier(1000000000)
    for r in results:
        print(f"   - {r['name']}: {r.get('revenue', 'N/A')}")
    print(f"   Total: {len(results)}\n")
    
    # Example 6: General search
    print("6. Search for 'sterilization':")
    results = search.search('sterilization')
    for r in results[:5]:
        print(f"   - {r['name']}")
    print(f"   Total: {len(results)}\n")
