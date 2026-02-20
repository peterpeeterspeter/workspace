#!/usr/bin/env python3
"""
Lab Cleaning Suppliers Scraper
Scrapes US lab cleaning suppliers from multiple sources
"""

import json
import csv
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse
import re

# List of sources to scrape
SOURCES = [
    {
        "name": "VWR (Avantor)",
        "url": "https://us.vwr.com",
        "type": "distributor",
        "description": "Major lab supply distributor"
    },
    {
        "name": "Fisher Scientific (Thermo Fisher)",
        "url": "https://www.fishersci.com",
        "type": "distributor",
        "description": "Leading lab supplies and chemicals"
    },
    {
        "name": "Sigma-Aldrich (Merck)",
        "url": "https://www.sigmaaldrich.com/US",
        "type": "manufacturer",
        "description": "Chemicals and lab supplies"
    },
    {
        "name": "Cole-Parmer",
        "url": "https://www.coleparmer.com",
        "type": "distributor",
        "description": "Lab equipment and supplies"
    },
    {
        "name": "LabCreator",
        "url": "https://www.labcreatoor.com/",
        "type": "distributor",
        "description": "Lab furniture and equipment"
    },
    {
        "name": "Grainger",
        "url": "https://www.grainger.com",
        "type": "distributor",
        "description": "Industrial and lab supplies"
    },
    {
        "name": "Airgas",
        "url": "https://www.airgas.com",
        "type": "distributor",
        "description": "Lab gases and supplies"
    },
    {
        "name": "Daigger",
        "url": "https://www.daigger.com",
        "type": "distributor",
        "description": "Laboratory equipment distributor"
    },
    {
        "name": "BioRad",
        "url": "https://www.bio-rad.com",
        "type": "manufacturer",
        "description": "Life science research products"
    },
    {
        "name": "Corning",
        "url": "https://www.corning.com",
        "type": "manufacturer",
        "description": "Lab glassware and plasticware"
    },
    {
        "name": "Eppendorf",
        "url": "https://www.eppendorf.com/US-en/",
        "type": "manufacturer",
        "description": "Lab equipment and consumables"
    },
    {
        "name": "Sartorius",
        "url": "https://www.sartorius.com",
        "type": "manufacturer",
        "description": "Lab and biotech equipment"
    },
    {
        "name": "MilliporeSigma",
        "url": "https://www.sigmaaldrich.com/US/en/brands/aldrich-catalog.html",
        "type": "manufacturer",
        "description": "Lab filtration and purification"
    },
    {
        "name": "Bel-Art Products",
        "url": "https://www.belart.com",
        "type": "manufacturer",
        "description": "Labware and equipment"
    },
    {
        "name": "DWK Life Sciences",
        "url": "https://www.dwk.com",
        "type": "manufacturer",
        "description": "Lab glassware (Kimax, Pyrex)"
    },
    {
        "name": "Thermo Fisher Scientific",
        "url": "https://www.thermofisher.com",
        "type": "manufacturer",
        "description": "Lab instruments and supplies"
    },
    {
        "name": "Agilent Technologies",
        "url": "https://www.agilent.com",
        "type": "manufacturer",
        "description": "Analytical lab instruments"
    },
    {
        "name": "Waters Corporation",
        "url": "https://www.waters.com",
        "type": "manufacturer",
        "description": "Chromatography equipment"
    },
    {
        "name": "Shimadzu",
        "url": "https://www.shimadzu.com",
        "type": "manufacturer",
        "description": "Analytical instruments"
    },
    {
        "name": "PerkinElmer",
        "url": "https://www.perkinelmer.com",
        "type": "manufacturer",
        "description": "Lab instruments and reagents"
    },
    {
        "name": "Abcam",
        "url": "https://www.abcam.com",
        "type": "manufacturer",
        "description": "Antibodies and research reagents"
    },
    {
        "name": "New England Biolabs",
        "url": "https://www.neb.com",
        "type": "manufacturer",
        "description": "Molecular biology reagents"
    },
    {
        "name": "Promega Corporation",
        "url": "https://www.promega.com",
        "type": "manufacturer",
        "description": "Life science reagents"
    },
    {
        "name": "QIAGEN",
        "url": "https://www.qiagen.com",
        "type": "manufacturer",
        "description": "Sample and assay technologies"
    },
    {
        "name": "Illumina",
        "url": "https://www.illumina.com",
        "type": "manufacturer",
        "description": "Sequencing and genomics"
    },
    {
        "name": "Beckman Coulter",
        "url": "https://www.beckmancoulter.com",
        "type": "manufacturer",
        "description": "Centrifuges and analyzers"
    },
    {
        "name": "Hamilton Company",
        "url": "https://www.hamiltoncompany.com",
        "type": "manufacturer",
        "description": "Liquid handling and lab automation"
    },
    {
        "name": "Mettler Toledo",
        "url": "https://www.mt.com",
        "type": "manufacturer",
        "description": "Lab balances and analytical equipment"
    },
    {
        "name": "Sartorius AG",
        "url": "https://www.sartorius.com/en-us",
        "type": "manufacturer",
        "description": "Lab balances and bioprocess"
    },
    {
        "name": "Tektronix",
        "url": "https://www.tek.com",
        "type": "manufacturer",
        "description": "Test and measurement equipment"
    },
    {
        "name": "Fluke Biomedical",
        "url": "https://www.flukebiomedical.com",
        "type": "manufacturer",
        "description": "Biomedical test equipment"
    },
    {
        "name": "CSSL (Cambridge Scientific)",
        "url": "https://www.cambridgescientific.com",
        "type": "distributor",
        "description": "Lab equipment distributor"
    },
    {
        "name": "Thomas Scientific",
        "url": "https://www.thomassci.com",
        "type": "distributor",
        "description": "Lab supplies distributor"
    },
    {
        "name": "Spectrum Chemical",
        "url": "https://www.spectrumchemical.com",
        "type": "manufacturer",
        "description": "Chemicals and lab supplies"
    },
    {
        "name": "Alfa Aesar",
        "url": "https://www.alfa.com",
        "type": "manufacturer",
        "description": "Research chemicals and metals"
    },
    {
        "name": "TCI America",
        "url": "https://www.tcichemicals.com",
        "type": "manufacturer",
        "description": "Organic chemicals"
    },
    {
        "name": "Oakwood Products",
        "url": "https://www.oakwoodchemical.com",
        "type": "manufacturer",
        "description": "Research chemicals"
    },
    {
        "name": "GFS Chemicals",
        "url": "https://www.gfschemicals.com",
        "type": "manufacturer",
        "description": "Chemicals and reagents"
    },
    {
        "name": "Spectrum Laboratory Products",
        "url": "https://www.spectrallab.com",
        "type": "manufacturer",
        "description": "Fine chemicals"
    },
    {
        "name": "Avantor (VWR)",
        "url": "https://avantorsciences.com",
        "type": "distributor",
        "description": "Global lab supplies"
    },
    {
        "name": "Binder",
        "url": "https://www.binder-world.com",
        "type": "manufacturer",
        "description": "Incubators and ovens"
    },
    {
        "name": "Memmert",
        "url": "https://www.memmert.com",
        "type": "manufacturer",
        "description": "Incubators and climate chambers"
    },
    {
        "name": "NuAire",
        "url": "https://www.nuaire.com",
        "type": "manufacturer",
        "description": "Biological safety cabinets"
    },
    {
        "name": "Labconco",
        "url": "https://www.labconco.com",
        "type": "manufacturer",
        "description": "Fume hoods and enclosures"
    },
    {
        "name": "Thermo Scientific",
        "url": "https://www.thermoscientific.com",
        "type": "manufacturer",
        "description": "Lab equipment brand"
    },
    {
        "name": "Whatman",
        "url": "https://www.whatman.com",
        "type": "manufacturer",
        "description": "Filtration products"
    },
    {
        "name": "Nalgene",
        "url": "https://www.nalgene.com",
        "type": "manufacturer",
        "description": "Lab plasticware"
    },
    {
        "name": "VWR International",
        "url": "https://us.vwr.com/store",
        "type": "distributor",
        "description": "Lab supplies distributor"
    },
    {
        "name": "Biohit",
        "url": "https://www.biohit.com",
        "type": "manufacturer",
        "description": "Pipettes and liquid handling"
    },
    {
        "name": "Gilson",
        "url": "https://www.gilson.com",
        "type": "manufacturer",
        "description": "Pipettes and purification"
    },
    {
        "name": "Heidolph",
        "url": "https://www.heidolph.com",
        "type": "manufacturer",
        "description": "Rotary evaporators"
    },
    {
        "name": "Julabo",
        "url": "https://www.julabo.com",
        "type": "manufacturer",
        "description": "Temperature control equipment"
    },
    {
        "name": "LAUDA",
        "url": "https://www.lauda.com",
        "type": "manufacturer",
        "description": "Thermostats and chillers"
    },
    {
        "name": "IKA",
        "url": "https://www.ika.com",
        "type": "manufacturer",
        "description": "Lab equipment and stirring"
    },
    {
        "name": "Bosch",
        "url": "https://www.bosch.com",
        "type": "manufacturer",
        "description": "Lab homogenizers"
    },
    {
        "name": "BioSpec Products",
        "url": "https://www.biospec.com",
        "type": "manufacturer",
        "description": "Sample preparation"
    },
    {
        "name": "Denville Scientific",
        "url": "https://www.denvillescientific.com",
        "type": "manufacturer",
        "description": "Lab equipment"
    },
    {
        "name": "USA Scientific",
        "url": "https://www.usascientific.com",
        "type": "manufacturer",
        "description": "Lab plastics"
    },
    {
        "name": "Genesee Scientific",
        "url": "https://www.geneseesci.com",
        "type": "manufacturer",
        "description": "Lab consumables"
    },
    {
        "name": "WWR (Westech)",
        "url": "https://www.wwr.com",
        "type": "distributor",
        "description": "Waste management for labs"
    },
    {
        "name": "Triumvirate Environmental",
        "url": "https://www.triumvirate.com",
        "type": "service",
        "description": "Lab cleaning and waste management"
    },
    {
        "name": "Clean Harbors",
        "url": "https://www.cleanharbors.com",
        "type": "service",
        "description": "Lab waste disposal"
    },
    {
        "name": "Veolia",
        "url": "https://www.veolia.com",
        "type": "service",
        "description": "Environmental services"
    },
    {
        "name": "Steris",
        "url": "https://www.steris.com",
        "type": "service",
        "description": "Lab sterilization services"
    },
    {
        "name": "Ecolab",
        "url": "https://www.ecolab.com",
        "type": "service",
        "description": "Lab cleaning solutions"
    },
    {
        "name": "Diversey",
        "url": "https://www.diversey.com",
        "type": "service",
        "description": "Cleaning and hygiene"
    },
    {
        "name": "Procter & Gamble Professional",
        "url": "https://www.pgpro.com",
        "type": "service",
        "description": "Commercial cleaning products"
    },
    {
        "name": "3M Clean",
        "url": "https://www.3m.com/3M/en_US/cleaning-us/",
        "type": "manufacturer",
        "description": "Cleaning products"
    },
    {
        "name": "Decon Labs",
        "url": "https://www.deconlabs.com",
        "type": "manufacturer",
        "description": "Lab decontamination products"
    },
    {
        "name": "Cole-Parmer - Antylia Scientific",
        "url": "https://www.antyliascientific.com",
        "type": "manufacturer",
        "description": "Lab consumables"
    },
    {
        "name": "Knight Scientific",
        "url": "https://www.knightscientific.com",
        "type": "distributor",
        "description": "Lab supplies"
    },
    {
        "name": "Denville Scientific",
        "url": "https://www.denville.com",
        "type": "manufacturer",
        "description": "Centrifuges and equipment"
    },
    {
        "name": "Benchmark Scientific",
        "url": "https://www.benchmarkscientific.com",
        "type": "manufacturer",
        "description": "Lab equipment"
    },
    {
        "name": "Ohaus",
        "url": "https://www.ohaus.com",
        "type": "manufacturer",
        "description": "Lab balances and scales"
    },
    {
        "name": "Adam Equipment",
        "url": "https://www.adamequipment.com",
        "type": "manufacturer",
        "description": "Lab balances"
    },
    {
        "name": "A&D Engineering",
        "url": "https://www.aandd.jp",
        "type": "manufacturer",
        "description": "Lab balances"
    },
    {
        "name": "Denver Instrument",
        "url": "https://www.denverinstrument.com",
        "type": "manufacturer",
        "description": "Analytical balances"
    },
    {
        "name": "Scientific Industries",
        "url": "https://www.scientificind.com",
        "type": "manufacturer",
        "description": "Lab mixers and shakers"
    },
    {
        "name": "VWR International",
        "url": "https://www.vwr.com",
        "type": "distributor",
        "description": "Lab supplies"
    },
    {
        "name": "Spectrum Chemical Mfg",
        "url": "https://www.spectrumchemical.com",
        "type": "manufacturer",
        "description": "Fine chemicals"
    },
    {
        "name": "American Chemical Technologies",
        "url": "https://www.americanchemical.com",
        "type": "service",
        "description": "Lab chemical supply"
    },
    {
        "name": "Chemglass",
        "url": "https://www.chemglass.com",
        "type": "manufacturer",
        "description": "Lab glassware"
    },
    {
        "name": "Wilmad-LabGlass",
        "url": "https://www.wilmad.com",
        "type": "manufacturer",
        "description": "NMR and glassware"
    },
    {
        "name": "Quark Glass",
        "url": "https://www.quarkglass.com",
        "type": "manufacturer",
        "description": "Custom glassware"
    },
    {
        "name": "Precision Glassblowing",
        "url": "https://www.precisionglassblowing.com",
        "type": "manufacturer",
        "description": "Custom glassware"
    },
    {
        "name": "Wildcat Lab Glass",
        "url": "https://www.wildcatlabglass.com",
        "type": "manufacturer",
        "description": "Custom glassware"
    }
]

def save_to_json(data, filename):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(data)} suppliers to {filename}")

def save_to_csv(data, filename):
    """Save data to CSV file"""
    if not data:
        print("❌ No data to save")
        return
    
    keys = list(data[0].keys())
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Saved {len(data)} suppliers to {filename}")

def categorize_suppliers():
    """Categorize suppliers by type"""
    categories = {
        'manufacturer': [],
        'distributor': [],
        'service': []
    }
    
    for supplier in SOURCES:
        supplier_type = supplier.get('type', 'other')
        if supplier_type in categories:
            categories[supplier_type].append(supplier)
        else:
            if 'other' not in categories:
                categories['other'] = []
            categories['other'].append(supplier)
    
    return categories

def main():
    """Main function"""
    print(f"🧪 Lab Cleaning Suppliers Scraper")
    print(f"=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Total suppliers: {len(SOURCES)}")
    print()
    
    # Save full list as JSON
    output_dir = '/root/.openclaw/workspace/projects/labcleaning'
    
    # Save to JSON
    json_file = f"{output_dir}/lab_suppliers.json"
    save_to_json(SOURCES, json_file)
    
    # Save to CSV
    csv_file = f"{output_dir}/lab_suppliers.csv"
    save_to_csv(SOURCES, csv_file)
    
    # Categorize and save
    categories = categorize_suppliers()
    
    for category, suppliers in categories.items():
        print(f"\n📁 {category.upper()}: {len(suppliers)} suppliers")
        
        # Save each category
        category_json = f"{output_dir}/suppliers_{category}.json"
        save_to_json(suppliers, category_json)
    
    print(f"\n✅ All files saved to {output_dir}/")
    print(f"\n📊 Summary:")
    print(f"   - Total suppliers: {len(SOURCES)}")
    print(f"   - Manufacturers: {len(categories['manufacturer'])}")
    print(f"   - Distributors: {len(categories['distributor'])}")
    print(f"   - Service providers: {len(categories['service'])}")

if __name__ == "__main__":
    main()
