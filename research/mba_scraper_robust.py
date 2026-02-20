#!/usr/bin/env python3
"""
Robust MBA Scraper with Checkpointing
Saves progress incrementally and can resume if interrupted
"""

import csv
import json
import os
import time
from datetime import datetime
import requests
import urllib3
from bs4 import BeautifulSoup
import re

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

OUTPUT_FILE = '/root/.openclaw/workspace/research/onlinembaprograms-comprehensive.csv'
CHECKPOINT_FILE = '/root/.openclaw/workspace/research/.scraper_checkpoint.json'

# Comprehensive program list
PROGRAMS = [
    # Top Tier Programs
    {'school': 'University of North Carolina', 'program': 'MBA@UNC', 'urls': ['https://onlinemba.unc.edu'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'Indiana University Bloomington', 'program': 'Kelley Direct Online MBA', 'urls': ['https://kd.iu.edu'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'University of Southern California', 'program': 'Online MBA', 'urls': ['https://www.marshall.usc.edu/programs/online-mba'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'Carnegie Mellon University', 'program': 'Online Hybrid MBA', 'urls': ['https://www.tepper.cmu.edu'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'University of Texas at Dallas', 'program': 'Online MBA', 'urls': ['https://jindal.utdallas.edu/programs/online-mba'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'University of Massachusetts Amherst', 'program': 'Online MBA', 'urls': ['https://www.isenberg.umass.edu/programs/online-mba'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'University of Arizona', 'program': 'Online MBA', 'urls': ['https://eller.arizona.edu/programs/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'University of Wisconsin', 'program': 'Online MBA', 'urls': ['https://business.wisc.edu/mba/online'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'University of Florida', 'program': 'Online MBA', 'urls': ['https://warrington.ufl.edu/online-mba'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'Arizona State University', 'program': 'Online MBA', 'urls': ['https://wpcarey.asu.edu/online-mba'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    
    # Tier 1 Programs
    {'school': 'University of Michigan', 'program': 'Online MBA', 'urls': ['https://michiganross.umich.edu/programs/online-mba'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'Northwestern University', 'program': 'Online MBA', 'urls': ['https://www.kellogg.northwestern.edu/programs/online-mba'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'Duke University', 'program': 'Online MBA', 'urls': ['https://www.fuqua.duke.edu/online-mba'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'University of Virginia', 'program': 'Online MBA', 'urls': ['https://www.darden.virginia.edu/online-mba'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'University of Texas at Austin', 'program': 'Online MBA', 'urls': ['https://www.mccombs.utexas.edu/mba/online'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'Georgetown University', 'program': 'Online MBA', 'urls': ['https://msb.georgetown.edu/mba/online'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'Vanderbilt University', 'program': 'Online MBA', 'urls': ['https://www.vanderbilt.edu/owen/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'Ohio State University', 'program': 'Online MBA', 'urls': ['https://www.fisher.osu.edu/programs/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'Penn State University', 'program': 'Online MBA', 'urls': ['https://worldcampus.psu.edu/degrees/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'University of Maryland', 'program': 'Online MBA', 'urls': ['https://www.rhsmith.umd.edu/programs/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'Boston University', 'program': 'Online MBA', 'urls': ['https://www.bu.edu/questrom/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'Northeastern University', 'program': 'Online MBA', 'urls': ['https://www.northeastern.edu/business/programs/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'George Washington University', 'program': 'Online MBA', 'urls': ['https://business.gwu.edu/programs/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'Texas A&M University', 'program': 'Online MBA', 'urls': ['https://mays.tamu.edu/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'University of Georgia', 'program': 'Online MBA', 'urls': ['https://www.terry.uga.edu/programs/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'University of Illinois', 'program': 'Online MBA', 'urls': ['https://www.mba.illinois.edu/online'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'Georgia Tech', 'program': 'Online MBA', 'urls': ['https://www.scheller.gatech.edu/programs/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'University of Washington', 'program': 'Online MBA', 'urls': ['https://www.foster.washington.edu/degrees/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'Brigham Young University', 'program': 'Online MBA', 'urls': ['https://marriottschool.byu.edu/mba/online'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'Texas Christian University', 'program': 'Online MBA', 'urls': ['https://www.neely.tcu.edu/programs/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    
    # Tier 2 Programs
    {'school': 'Ball State University', 'program': 'Online MBA', 'urls': ['https://www.bsu.edu/business/online/mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of Nebraska-Lincoln', 'program': 'Online MBA', 'urls': ['https://business.unl.edu/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'Oklahoma State University', 'program': 'Online MBA', 'urls': ['https://business.okstate.edu/online/mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of South Dakota', 'program': 'Online MBA', 'urls': ['https://www.usd.edu/business/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of Kansas', 'program': 'Online MBA', 'urls': ['https://www.kuscholarship.org/mba-online'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of Kentucky', 'program': 'Online MBA', 'urls': ['https://www.gatton.uky.edu/programs/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of Tennessee', 'program': 'Online MBA', 'urls': ['https://mba.utk.edu/online'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of Alabama', 'program': 'Online MBA', 'urls': ['https://www.culverhouse.ua.edu/programs/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'Auburn University', 'program': 'Online MBA', 'urls': ['https://business.auburn.edu/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'Clemson University', 'program': 'Online MBA', 'urls': ['https://www.clemson.edu/business/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'Louisiana State University', 'program': 'Online MBA', 'urls': ['https://www.lsu.edu/business/mba/online.php'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of South Carolina', 'program': 'Online MBA', 'urls': ['https://www.moore.sc.edu/programs/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'Virginia Tech', 'program': 'Online MBA', 'urls': ['https://www.pamplin.vt.edu/mba/online'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'North Carolina State University', 'program': 'Online MBA', 'urls': ['https://www.poole.ncsu.edu/mba/online'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of Cincinnati', 'program': 'Online MBA', 'urls': ['https://business.uc.edu/programs/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of Pittsburgh', 'program': 'Online MBA', 'urls': ['https://www.katz.pitt.edu/programs/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'Rutgers University', 'program': 'Online MBA', 'urls': ['https://www.business.rutgers.edu/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'Temple University', 'program': 'Online MBA', 'urls': ['https://www.fox.temple.edu/mba/online'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of Connecticut', 'program': 'Online MBA', 'urls': ['https://www.business.uconn.edu/mba-online'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'Florida State University', 'program': 'Online MBA', 'urls': ['https://business.fsu.edu/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of Central Florida', 'program': 'Online MBA', 'urls': ['https://www.ucf.edu/business/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of Houston', 'program': 'Online MBA', 'urls': ['https://www.bauer.uh.edu/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of Iowa', 'program': 'Online MBA', 'urls': ['https://www.tippie.uiowa.edu/mba/online'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'Iowa State University', 'program': 'Online MBA', 'urls': ['https://www.business.iastate.edu/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of Minnesota', 'program': 'Online MBA', 'urls': ['https://carlsonschool.umn.edu/degrees/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'University of Colorado', 'program': 'Online MBA', 'urls': ['https://www.colorado.edu/business/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'University of Utah', 'program': 'Online MBA', 'urls': ['https://eccles.utah.edu/programs/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'Mississippi State University', 'program': 'Online MBA', 'urls': ['https://www.business.msstate.edu/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    
    # Affordable Options
    {'school': 'Liberty University', 'program': 'Online MBA', 'urls': ['https://www.liberty.edu/online-mba'], 'tier': 'Affordable', 'accreditation': 'ACBSP'},
    {'school': 'Southern New Hampshire University', 'program': 'Online MBA', 'urls': ['https://www.snhu.edu/online-mba'], 'tier': 'Affordable', 'accreditation': 'ACBSP'},
    {'school': 'Western Governors University', 'program': 'MBA', 'urls': ['https://www.wgu.edu/mba'], 'tier': 'Affordable', 'accreditation': 'ACBSP'},
    {'school': 'Purdue University Global', 'program': 'Online MBA', 'urls': ['https://www.purdueglobal.edu/business-school/mba'], 'tier': 'Affordable', 'accreditation': 'ACBSP'},
    {'school': 'University of the People', 'program': 'MBA', 'urls': ['https://www.uopeople.edu/programs/mba'], 'tier': 'Affordable', 'accreditation': 'DEAC'},
    {'school': 'Fayetteville State University', 'program': 'Online MBA', 'urls': ['https://www.uncfsu.edu/business/online-mba'], 'tier': 'Affordable', 'accreditation': 'AACSB'},
    {'school': 'Georgia Southwestern State University', 'program': 'Online MBA', 'urls': ['https://www.gsw.edu/business/mba-online'], 'tier': 'Affordable', 'accreditation': 'AACSB'},
    {'school': 'Fort Hays State University', 'program': 'Online MBA', 'urls': ['https://www.fhsu.edu/mba/online'], 'tier': 'Affordable', 'accreditation': 'AACSB'},
    {'school': 'Southeast Missouri State University', 'program': 'Online MBA', 'urls': ['https://www.semo.edu/business/online-mba'], 'tier': 'Affordable', 'accreditation': 'AACSB'},
    {'school': 'Arkansas State University', 'program': 'Online MBA', 'urls': ['https://www.astate.edu/college-of-business/online-mba'], 'tier': 'Affordable', 'accreditation': 'AACSB'},
    
    # International (UK/Europe)
    {'school': 'University of London', 'program': 'Online MBA', 'urls': ['https://london.ac.uk/mba'], 'tier': 'International', 'accreditation': 'AMBA'},
    {'school': 'University of Manchester', 'program': 'Online MBA', 'urls': ['https://www.mbs.ac.uk/mba/online-mba'], 'tier': 'International', 'accreditation': 'AMBA,AACSB,EQUIS'},
    {'school': 'Warwick Business School', 'program': 'Online MBA', 'urls': ['https://www.wbs.ac.uk/mba/online'], 'tier': 'International', 'accreditation': 'AMBA,AACSB,EQUIS'},
    {'school': 'Imperial College London', 'program': 'Global Online MBA', 'urls': ['https://www.imperial.ac.uk/business-school/programmes/mba/global-online-mba'], 'tier': 'International', 'accreditation': 'AMBA,AACSB,EQUIS'},
    {'school': 'University of Edinburgh', 'program': 'Online MBA', 'urls': ['https://www.business-school.ed.ac.uk/mba/online'], 'tier': 'International', 'accreditation': 'AACSB,AMBA,EQUIS'},
    {'school': 'IE Business School (Spain)', 'program': 'Online MBA', 'urls': ['https://www.ie.edu/business-school/mba/online'], 'tier': 'International', 'accreditation': 'AACSB,AMBA,EQUIS'},
    {'school': 'IESE Business School (Spain)', 'program': 'Online MBA', 'urls': ['https://www.iese.edu/mba/online'], 'tier': 'International', 'accreditation': 'AACSB,AMBA,EQUIS'},
    {'school': 'ESADE (Spain)', 'program': 'Online MBA', 'urls': ['https://www.esade.edu/mba-online'], 'tier': 'International', 'accreditation': 'AACSB,AMBA,EQUIS'},
    {'school': 'HEC Paris', 'program': 'Online MBA', 'urls': ['https://www.hec.fr/en/programs/mba/online'], 'tier': 'International', 'accreditation': 'AACSB,AMBA,EQUIS'},
    {'school': 'Rotterdam School of Management', 'program': 'Online MBA', 'urls': ['https://www.rsm.nl/mba/online'], 'tier': 'International', 'accreditation': 'AACSB,AMBA,EQUIS'},
    
    # Canadian
    {'school': 'University of Toronto', 'program': 'Online MBA', 'urls': ['https://www.rotman.utoronto.ca/Degrees/OnlineMBA'], 'tier': 'International', 'accreditation': 'AACSB'},
    {'school': 'York University', 'program': 'Online MBA', 'urls': ['https://schulich.yorku.ca/programs/mba/online'], 'tier': 'International', 'accreditation': 'AACSB'},
    {'school': 'Queen\'s University', 'program': 'Online MBA', 'urls': ['https://smith.queensu.ca/mba/online'], 'tier': 'International', 'accreditation': 'AACSB'},
    {'school': 'University of British Columbia', 'program': 'Online MBA', 'urls': ['https://www.sauder.ubc.ca/programs/mba/online'], 'tier': 'International', 'accreditation': 'AACSB'},
    
    # Australian
    {'school': 'University of Queensland', 'program': 'Online MBA', 'urls': ['https://business.uq.edu.au/programs/online-mba'], 'tier': 'International', 'accreditation': 'AACSB,EQUIS'},
    {'school': 'Monash University', 'program': 'Online MBA', 'urls': ['https://www.monash.edu/business/mba/online'], 'tier': 'International', 'accreditation': 'AACSB,EQUIS'},
    {'school': 'UNSW Sydney', 'program': 'Online MBA', 'urls': ['https://www.unswbusiness.unsw.edu.au/mba-online'], 'tier': 'International', 'accreditation': 'AACSB,EQUIS'},
    
    # Specialized/Other
    {'school': 'Babson College', 'program': 'Online MBA', 'urls': ['https://www.babson.edu/academics/graduate/mba/online'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'Bentley University', 'program': 'Online MBA', 'urls': ['https://www.bentley.edu/graduate/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'Pepperdine University', 'program': 'Online MBA', 'urls': ['https://bschool.pepperdine.edu/programs/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'American University', 'program': 'Online MBA', 'urls': ['https://www.american.edu/kogod/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
    {'school': 'Howard University', 'program': 'Online MBA', 'urls': ['https://www.bschool.howard.edu/programs/online-mba'], 'tier': 'Tier 2', 'accreditation': 'AACSB'},
    {'school': 'Johns Hopkins University', 'program': 'Online MBA', 'urls': ['https://carey.jhu.edu/programs/mba/online'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'MIT Sloan', 'program': 'Online MBA', 'urls': ['https://mitsloan.mit.edu/mba'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'Columbia University', 'program': 'Online MBA', 'urls': ['https://www8.gsb.columbia.edu/programs/online-mba'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'New York University', 'program': 'Online MBA', 'urls': ['https://www.stern.nyu.edu/programs/online-mba'], 'tier': 'Top Tier', 'accreditation': 'AACSB'},
    {'school': 'Southern Methodist University', 'program': 'Online MBA', 'urls': ['https://www.cox.smu.edu/programs/online-mba'], 'tier': 'Tier 1', 'accreditation': 'AACSB'},
]

def load_checkpoint():
    """Load checkpoint if exists"""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    return {'completed': [], 'last_index': 0}

def save_checkpoint(completed, last_index):
    """Save checkpoint"""
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump({'completed': completed, 'last_index': last_index}, f)

def fetch_url(url):
    """Fetch a URL with proper error handling"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=20, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            return ' '.join(chunk for chunk in chunks if chunk)
    except Exception as e:
        pass
    return None

def extract_mba_data(content, school, program, url, tier, accreditation):
    """Extract MBA data from content"""
    data = {
        'school_name': school,
        'program_name': program,
        'tuition_total': '',
        'tuition_per_credit': '',
        'format': '',
        'duration': '',
        'total_credits': '',
        'gmat_requirement': '',
        'gre_accepted': '',
        'accreditation': accreditation,
        'tier': tier,
        'program_url': url,
        'source_url': url,
        'date_scraped': datetime.now().isoformat(),
        'confidence_score': 0
    }
    
    if not content:
        return data
    
    content_lower = content.lower()
    
    # Duration
    dur_match = re.search(r'(\d+)\s*(months?|years?|semesters?)', content_lower)
    if dur_match:
        data['duration'] = f"{dur_match.group(1)} {dur_match.group(2)}"
    
    # Credits
    cred_match = re.search(r'(\d+)\s*(credits?|credit hours?|semester hours?)', content_lower)
    if cred_match:
        data['total_credits'] = cred_match.group(1)
    
    # Tuition
    tuition_patterns = [
        (r'\$[\d,]+\s*(?:to\s*-)?\s*\$[\d,]+.*total', 'tuition_total'),
        (r'\$[\d,]+.*per credit', 'tuition_per_credit'),
        (r'tuition[^$]*\$[\d,]+', 'tuition_total'),
    ]
    
    for pattern, field in tuition_patterns:
        match = re.search(pattern, content_lower)
        if match:
            amount = re.search(r'\$[\d,]+', match.group(0))
            if amount:
                data[field] = amount.group(0)
                break
    
    # GMAT
    if re.search(r'gmat.*required|required.*gmat', content_lower):
        data['gmat_requirement'] = 'Required'
    elif re.search(r'gmat.*optional|optional.*gmat', content_lower):
        data['gmat_requirement'] = 'Optional'
    elif re.search(r'gmat.*waived|waived.*gmat|no gmat', content_lower):
        data['gmat_requirement'] = 'Waived'
    
    # GRE
    data['gre_accepted'] = 'Yes' if re.search(r'gre.*accept|accept.*gre', content_lower) else 'No'
    
    # Format
    data['format'] = 'Online' if 'online' in content_lower else ''
    
    # Calculate confidence
    filled = sum(1 for v in data.values() if v and v != '' and v not in ['source_url', 'date_scraped', 'program_url', 'tier'])
    total = len(data) - 4
    data['confidence_score'] = round((filled / total) * 100, 0)
    
    return data

def append_to_csv(data):
    """Append a row to CSV"""
    file_exists = os.path.exists(OUTPUT_FILE)
    
    fieldnames = [
        'school_name', 'program_name', 'tuition_total', 'tuition_per_credit',
        'format', 'duration', 'total_credits', 'gmat_requirement', 'gre_accepted',
        'accreditation', 'tier', 'program_url', 'source_url', 'date_scraped', 'confidence_score'
    ]
    
    with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def main():
    print("=" * 80)
    print("ROBUST MBA SCRAPER WITH CHECKPOINTING")
    print("=" * 80)
    print(f"Total programs: {len(PROGRAMS)}")
    print()
    
    # Load checkpoint
    checkpoint = load_checkpoint()
    start_index = checkpoint['last_index']
    completed = set(checkpoint['completed'])
    
    print(f"Resuming from index {start_index}")
    print(f"Already completed: {len(completed)}")
    print()
    
    successful = 0
    failed = 0
    
    for i in range(start_index, len(PROGRAMS)):
        prog = PROGRAMS[i]
        school = prog['school']
        program = prog['program']
        urls = prog['urls']
        tier = prog['tier']
        accreditation = prog['accreditation']
        
        # Skip if already completed
        if f"{school}-{program}" in completed:
            continue
        
        print(f"[{i+1}/{len(PROGRAMS)}] {school} - {program}")
        
        content = None
        working_url = urls[0]
        
        for url in urls:
            content = fetch_url(url)
            if content:
                working_url = url
                break
        
        if content:
            data = extract_mba_data(content, school, program, working_url, tier, accreditation)
            append_to_csv(data)
            completed.add(f"{school}-{program}")
            successful += 1
            print(f"  ✓ Success ({data['confidence_score']}%)")
        else:
            # Still add entry even if failed
            data = {
                'school_name': school,
                'program_name': program,
                'accreditation': accreditation,
                'tier': tier,
                'program_url': urls[0],
                'source_url': urls[0],
                'date_scraped': datetime.now().isoformat(),
                'confidence_score': 0,
                **{k: '' for k in ['tuition_total', 'tuition_per_credit', 'format', 'duration', 
                                   'total_credits', 'gmat_requirement', 'gre_accepted']}
            }
            append_to_csv(data)
            completed.add(f"{school}-{program}")
            failed += 1
            print(f"  ✗ Failed (added with 0% confidence)")
        
        # Save checkpoint every 5 programs
        if (i + 1) % 5 == 0:
            save_checkpoint(list(completed), i + 1)
            print(f"  Checkpoint saved")
        
        print()
        time.sleep(2)  # Rate limiting
    
    # Final checkpoint
    save_checkpoint(list(completed), len(PROGRAMS))
    
    print("=" * 80)
    print(f"✓ COMPLETED: {len(PROGRAMS)} programs processed")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Output: {OUTPUT_FILE}")
    print("=" * 80)

if __name__ == '__main__':
    main()
