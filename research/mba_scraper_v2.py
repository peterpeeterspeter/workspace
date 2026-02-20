#!/usr/bin/env python3
"""
Enhanced MBA Program Scraper
Uses multiple sources and strategies to collect comprehensive MBA data
"""

import subprocess
import json
import csv
import re
from datetime import datetime
import time

# Expanded list of MBA programs with multiple URL attempts
MBA_PROGRAMS = [
    # Top Online MBA Programs
    {
        'school': 'University of North Carolina',
        'program': 'MBA@UNC',
        'urls': ['https://onlinemba.unc.edu', 'https://mba.unc.edu/online'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'Indiana University Bloomington',
        'program': 'Kelley Direct Online MBA',
        'urls': ['https://kelley.iu.edu/programs/online-mba', 'https://kd.iu.edu'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'Carnegie Mellon University',
        'program': 'Online Hybrid MBA',
        'urls': ['https://www.tepper.cmu.edu/online-mba', 'https://www.tepper.cmu.edu/programs/online-hybrid-mba'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'University of Southern California',
        'program': 'Online MBA',
        'urls': ['https://www.marshall.usc.edu/programs/online-mba', 'https://www.marshall.usc.edu/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'University of Florida',
        'program': 'Online MBA',
        'urls': ['https://warrington.ufl.edu/online-mba', 'https://warrington.ufl.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'Arizona State University',
        'program': 'Online MBA',
        'urls': ['https://wpcarey.asu.edu/online-mba', 'https://wpcarey.asu.edu/degrees/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'University of Texas at Dallas',
        'program': 'Online MBA',
        'urls': ['https://jindal.utdallas.edu/online-mba', 'https://jindal.utdallas.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'University of Massachusetts Amherst',
        'program': 'Online MBA',
        'urls': ['https://www.isenberg.umass.edu/online-mba', 'https://www.isenberg.umass.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'University of Arizona',
        'program': 'Online MBA',
        'urls': ['https://eller.arizona.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'University of Wisconsin',
        'program': 'Online MBA',
        'urls': ['https://business.wisc.edu/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    # Affordable Options
    {
        'school': 'Liberty University',
        'program': 'Online MBA',
        'urls': ['https://www.liberty.edu/online-mba', 'https://www.liberty.edu/business/online-mba'],
        'accreditation': 'ACBSP',
        'tier': 'Affordable'
    },
    {
        'school': 'Southern New Hampshire University',
        'program': 'Online MBA',
        'urls': ['https://www.snhu.edu/online-mba', 'https://www.snhu.edu/degrees/online/mba'],
        'accreditation': 'ACBSP',
        'tier': 'Affordable'
    },
    {
        'school': 'Western Governors University',
        'program': 'MBA',
        'urls': ['https://www.wgu.edu/mba'],
        'accreditation': 'ACBSP',
        'tier': 'Affordable'
    },
    {
        'school': 'University of the People',
        'program': 'MBA',
        'urls': ['https://www.uopeople.edu/programs/mba'],
        'accreditation': 'DEAC',
        'tier': 'Affordable'
    },
    {
        'school': 'Purdue University Global',
        'program': 'Online MBA',
        'urls': ['https://www.purdueglobal.edu/business-school/mba'],
        'accreditation': 'ACBSP',
        'tier': 'Affordable'
    },
    # Mid-Tier Programs
    {
        'school': 'Ball State University',
        'program': 'Online MBA',
        'urls': ['https://www.bsu.edu/business/online/mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of Nebraska-Lincoln',
        'program': 'Online MBA',
        'urls': ['https://business.unl.edu/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'Oklahoma State University',
        'program': 'Online MBA',
        'urls': ['https://business.okstate.edu/online/mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of South Dakota',
        'program': 'Online MBA',
        'urls': ['https://www.usd.edu/business/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Affordable'
    },
    {
        'school': 'Mississippi State University',
        'program': 'Online MBA',
        'urls': ['https://www.business.msstate.edu/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Affordable'
    },
    # International Programs (UK)
    {
        'school': 'University of London',
        'program': 'Online MBA',
        'urls': ['https://london.ac.uk/mba'],
        'accreditation': 'AMBA',
        'tier': 'International'
    },
    {
        'school': 'University of Manchester',
        'program': 'Online MBA',
        'urls': ['https://www.mbs.ac.uk/mba/online-mba'],
        'accreditation': 'AMBA,AACSB,EQUIS',
        'tier': 'International'
    },
    {
        'school': 'Warwick Business School',
        'program': 'Online MBA',
        'urls': ['https://www.wbs.ac.uk/mba/online'],
        'accreditation': 'AMBA,AACSB,EQUIS',
        'tier': 'International'
    },
    {
        'school': 'Imperial College London',
        'program': 'Global Online MBA',
        'urls': ['https://www.imperial.ac.uk/business-school/programmes/mba/global-online-mba'],
        'accreditation': 'AMBA,AACSB,EQUIS',
        'tier': 'International'
    },
    {
        'school': 'University of Edinburgh',
        'program': 'Online MBA',
        'urls': ['https://www.business-school.ed.ac.uk/mba/online'],
        'accreditation': 'AACSB,AMBA,EQUIS',
        'tier': 'International'
    },
    # Canadian Programs
    {
        'school': 'University of Toronto',
        'program': 'Online MBA',
        'urls': ['https://www.rotman.utoronto.ca/Degrees/OnlineMBA'],
        'accreditation': 'AACSB',
        'tier': 'International'
    },
    {
        'school': 'York University',
        'program': 'Online MBA',
        'urls': ['https://schulich.yorku.ca/programs/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'International'
    },
    {
        'school': 'Queen\'s University',
        'program': 'Online MBA',
        'urls': ['https://smith.queensu.ca/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'International'
    },
    {
        'school': 'University of British Columbia',
        'program': 'Online MBA',
        'urls': ['https://www.sauder.ubc.ca/programs/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'International'
    },
    # Tech-Focused Programs
    {
        'school': 'MIT Sloan',
        'program': 'Online MBA',
        'urls': ['https://mitsloan.mit.edu/mba'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'University of Washington',
        'program': 'Online MBA',
        'urls': ['https://www.foster.washington.edu/degrees/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'Georgia Tech',
        'program': 'Online MBA',
        'urls': ['https://www.scheller.gatech.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'Carnegie Mellon',
        'program': 'MBA Online',
        'urls': ['https://www.tepper.cmu.edu'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    # Healthcare MBA Programs
    {
        'school': 'Johns Hopkins University',
        'program': 'Online MBA',
        'urls': ['https://carey.jhu.edu/programs/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'University of Utah',
        'program': 'Online MBA',
        'urls': ['https://eccles.utah.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of Colorado',
        'program': 'Online MBA',
        'urls': ['https://www.colorado.edu/business/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    # Executive Programs
    {
        'school': 'Northwestern University',
        'program': 'Online MBA',
        'urls': ['https://www.kellogg.northwestern.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'University of Michigan',
        'program': 'Online MBA',
        'urls': ['https://michiganross.umich.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'Duke University',
        'program': 'Online MBA',
        'urls': ['https://www.fuqua.duke.edu/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'Vanderbilt University',
        'program': 'Online MBA',
        'urls': ['https://www.vanderbilt.edu/owen/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'University of Virginia',
        'program': 'Online MBA',
        'urls': ['https://www.darden.virginia.edu/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    # More Tier 1 Programs
    {
        'school': 'Ohio State University',
        'program': 'Online MBA',
        'urls': ['https://www.fisher.osu.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'Penn State University',
        'program': 'Online MBA',
        'urls': ['https://worldcampus.psu.edu/degrees/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'University of Maryland',
        'program': 'Online MBA',
        'urls': ['https://www.rhsmith.umd.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'Boston University',
        'program': 'Online MBA',
        'urls': ['https://www.bu.edu/questrom/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'Northeastern University',
        'program': 'Online MBA',
        'urls': ['https://www.northeastern.edu/business/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    # More Affordable Options
    {
        'school': 'Fayetteville State University',
        'program': 'Online MBA',
        'urls': ['https://www.uncfsu.edu/business/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Affordable'
    },
    {
        'school': 'Georgia Southwestern State University',
        'program': 'Online MBA',
        'urls': ['https://www.gsw.edu/business/mba-online'],
        'accreditation': 'AACSB',
        'tier': 'Affordable'
    },
    {
        'school': 'Fort Hays State University',
        'program': 'Online MBA',
        'urls': ['https://www.fhsu.edu/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'Affordable'
    },
    {
        'school': 'Southeast Missouri State University',
        'program': 'Online MBA',
        'urls': ['https://www.semo.edu/business/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Affordable'
    },
    {
        'school': 'Arkansas State University',
        'program': 'Online MBA',
        'urls': ['https://www.astate.edu/college-of-business/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Affordable'
    },
    # European Programs
    {
        'school': 'IE Business School (Spain)',
        'program': 'Online MBA',
        'urls': ['https://www.ie.edu/business-school/mba/online'],
        'accreditation': 'AACSB,AMBA,EQUIS',
        'tier': 'International'
    },
    {
        'school': 'IESE Business School (Spain)',
        'program': 'Online MBA',
        'urls': ['https://www.iese.edu/mba/online'],
        'accreditation': 'AACSB,AMBA,EQUIS',
        'tier': 'International'
    },
    {
        'school': 'ESADE (Spain)',
        'program': 'Online MBA',
        'urls': ['https://www.esade.edu/mba-online'],
        'accreditation': 'AACSB,AMBA,EQUIS',
        'tier': 'International'
    },
    {
        'school': 'HEC Paris',
        'program': 'Online MBA',
        'urls': ['https://www.hec.edu/en/programs/mba/online'],
        'accreditation': 'AACSB,AMBA,EQUIS',
        'tier': 'International'
    },
    {
        'school': 'Rotterdam School of Management',
        'program': 'Online MBA',
        'urls': ['https://www.rsm.nl/mba/online'],
        'accreditation': 'AACSB,AMBA,EQUIS',
        'tier': 'International'
    },
    # Australian Programs
    {
        'school': 'University of Queensland',
        'program': 'Online MBA',
        'urls': ['https://business.uq.edu.au/programs/online-mba'],
        'accreditation': 'AACSB,EQUIS',
        'tier': 'International'
    },
    {
        'school': 'Monash University',
        'program': 'Online MBA',
        'urls': ['https://www.monash.edu/business/mba/online'],
        'accreditation': 'AACSB,EQUIS',
        'tier': 'International'
    },
    {
        'school': 'UNSW Sydney',
        'program': 'Online MBA',
        'urls': ['https://www.unswbusiness.unsw.edu.au/mba-online'],
        'accreditation': 'AACSB,EQUIS',
        'tier': 'International'
    },
    # More Top Tier US Programs
    {
        'school': 'University of California Berkeley',
        'program': 'Online MBA',
        'urls': ['https://www.haas.berkeley.edu/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'Columbia University',
        'program': 'Online MBA',
        'urls': ['https://www8.gsb.columbia.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'New York University',
        'program': 'Online MBA',
        'urls': ['https://www.stern.nyu.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    # Specialized Programs
    {
        'school': 'Babson College',
        'program': 'Online MBA',
        'urls': ['https://www.babson.edu/academics/graduate/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'Bentley University',
        'program': 'Online MBA',
        'urls': ['https://www.bentley.edu/graduate/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'Pepperdine University',
        'program': 'Online MBA',
        'urls': ['https://bschool.pepperdine.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'Brigham Young University',
        'program': 'Online MBA',
        'urls': ['https://marriottschool.byu.edu/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'Texas A&M University',
        'program': 'Online MBA',
        'urls': ['https://mays.tamu.edu/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'University of Georgia',
        'program': 'Online MBA',
        'urls': ['https://www.terry.uga.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'University of Illinois',
        'program': 'Online MBA',
        'urls': ['https://www.mba.illinois.edu/online'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'University of Minnesota',
        'program': 'Online MBA',
        'urls': ['https://carlsonschool.umn.edu/degrees/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'University of Iowa',
        'program': 'Online MBA',
        'urls': ['https://www.tippie.uiowa.edu/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'Iowa State University',
        'program': 'Online MBA',
        'urls': ['https://www.business.iastate.edu/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of Kansas',
        'program': 'Online MBA',
        'urls': ['https://www.kuscholarship.org/mba-online'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of Kentucky',
        'program': 'Online MBA',
        'urls': ['https://www.gatton.uky.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of Tennessee',
        'program': 'Online MBA',
        'urls': ['https://mba.utk.edu/online'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of Alabama',
        'program': 'Online MBA',
        'urls': ['https://www.culverhouse.ua.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'Auburn University',
        'program': 'Online MBA',
        'urls': ['https://business.auburn.edu/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'Clemson University',
        'program': 'Online MBA',
        'urls': ['https://www.clemson.edu/business/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'Louisiana State University',
        'program': 'Online MBA',
        'urls': ['https://www.lsu.edu/business/mba/online.php'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of South Carolina',
        'program': 'Online MBA',
        'urls': ['https://www.moore.sc.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'Virginia Tech',
        'program': 'Online MBA',
        'urls': ['https://www.pamplin.vt.edu/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'North Carolina State University',
        'program': 'Online MBA',
        'urls': ['https://www.poole.ncsu.edu/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of Cincinnati',
        'program': 'Online MBA',
        'urls': ['https://business.uc.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of Pittsburgh',
        'program': 'Online MBA',
        'urls': ['https://www.katz.pitt.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'Rutgers University',
        'program': 'Online MBA',
        'urls': ['https://www.business.rutgers.edu/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'Temple University',
        'program': 'Online MBA',
        'urls': ['https://www.fox.temple.edu/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of Connecticut',
        'program': 'Online MBA',
        'urls': ['https://www.business.uconn.edu/mba-online'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'George Washington University',
        'program': 'Online MBA',
        'urls': ['https://business.gwu.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'Georgetown University',
        'program': 'Online MBA',
        'urls': ['https://msb.georgetown.edu/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'American University',
        'program': 'Online MBA',
        'urls': ['https://www.american.edu/kogod/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'Howard University',
        'program': 'Online MBA',
        'urls': ['https://www.bschool.howard.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'Florida State University',
        'program': 'Online MBA',
        'urls': ['https://business.fsu.edu/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of Central Florida',
        'program': 'Online MBA',
        'urls': ['https://www.ucf.edu/business/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of Houston',
        'program': 'Online MBA',
        'urls': ['https://www.bauer.uh.edu/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 2'
    },
    {
        'school': 'University of Texas at Austin',
        'program': 'Online MBA',
        'urls': ['https://www.mccombs.utexas.edu/mba/online'],
        'accreditation': 'AACSB',
        'tier': 'Top Tier'
    },
    {
        'school': 'Texas Christian University',
        'program': 'Online MBA',
        'urls': ['https://www.neely.tcu.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'Southern Methodist University',
        'program': 'Online MBA',
        'urls': ['https://www.cox.smu.edu/programs/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Tier 1'
    },
    {
        'school': 'Brigham Young University Hawaii',
        'program': 'Online MBA',
        'urls': ['https://byuh.edu/business/online-mba'],
        'accreditation': 'AACSB',
        'tier': 'Affordable'
    }
]

def fetch_with_web_fetch(url):
    """Use Python requests to get page content directly"""
    import urllib3
    import requests
    from bs4 import BeautifulSoup
    
    # Disable SSL warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract meaningful text content
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        return None
    except Exception as e:
        print(f"  Error fetching: {e}")
        return None

def extract_data_from_content(content, school, program, url, accreditation, tier):
    """Extract MBA data from page content"""
    import re
    
    data = {
        'school_name': school,
        'program_name': program,
        'tuition_total': '',
        'tuition_per_credit': '',
        'in_state_tuition': '',
        'out_of_state_tuition': '',
        'format': '',
        'duration': '',
        'total_credits': '',
        'gmat_requirement': '',
        'gre_accepted': '',
        'acceptance_rate': '',
        'class_size': '',
        'avg_salary': '',
        'employment_rate': '',
        'accreditation': accreditation,
        'specializations': '',
        'start_dates': '',
        'application_deadlines': '',
        'program_url': url,
        'source_url': url,
        'date_scraped': datetime.now().isoformat(),
        'confidence_score': 0,
        'tier': tier
    }
    
    if not content:
        return data
    
    content_lower = content.lower()
    
    # Extract tuition
    tuition_patterns = [
        r'tuition[^$]*\$[\d,]+',
        r'cost[^$]*\$[\d,]+',
        r'price[^$]*\$[\d,]+',
        r'\$[\d,]+.*per credit',
        r'\$[\d,]+.*total',
        r'\$[\d,]+.*program'
    ]
    
    for pattern in tuition_patterns:
        matches = re.findall(pattern, content_lower)
        if matches:
            if 'per credit' in matches[0]:
                data['tuition_per_credit'] = re.search(r'\$[\d,]+', matches[0]).group(0)
            elif 'total' in matches[0] or 'program' in matches[0]:
                data['tuition_total'] = re.search(r'\$[\d,]+', matches[0]).group(0)
            break
    
    # Extract duration
    duration_patterns = [
        r'(\d+)\s*months?',
        r'(\d+)\s*years?',
        r'(\d+)\s*semesters?'
    ]
    
    for pattern in duration_patterns:
        matches = re.findall(pattern, content_lower)
        if matches:
            if 'month' in pattern:
                data['duration'] = f"{matches[0]} months"
            elif 'year' in pattern:
                data['duration'] = f"{matches[0]} years"
            break
    
    # Extract credits
    credit_patterns = [
        r'(\d+)\s*credits?',
        r'(\d+)\s*credit\s*hours?',
        r'(\d+)\s*semester\s*hours?'
    ]
    
    for pattern in credit_patterns:
        matches = re.findall(pattern, content_lower)
        if matches:
            data['total_credits'] = matches[0]
            break
    
    # GMAT info
    if re.search(r'gmat.*required', content_lower):
        data['gmat_requirement'] = 'Required'
    elif re.search(r'gmat.*optional', content_lower):
        data['gmat_requirement'] = 'Optional'
    elif re.search(r'gmat.*waived', content_lower):
        data['gmat_requirement'] = 'Waived'
    
    # GRE acceptance
    if re.search(r'gre.*accept', content_lower):
        data['gre_accepted'] = 'Yes'
    else:
        data['gre_accepted'] = 'No'
    
    # Format
    if 'online' in content_lower:
        data['format'] = 'Online'
    if 'hybrid' in content_lower:
        if data['format']:
            data['format'] += '/Hybrid'
        else:
            data['format'] = 'Hybrid'
    
    # Acceptance rate
    acceptance_match = re.search(r'acceptance rate[^%]*\d+%', content_lower)
    if acceptance_match:
        data['acceptance_rate'] = acceptance_match.group(0)
    
    # Class size
    class_match = re.search(r'class size[^:]*:\s*(\d+)', content_lower)
    if class_match:
        data['class_size'] = class_match.group(1)
    
    # Employment rate
    employment_match = re.search(r'employment[^%]*\d+%', content_lower)
    if employment_match:
        data['employment_rate'] = employment_match.group(0)
    
    # Calculate confidence
    fields_filled = sum(1 for k, v in data.items() if v and v != '' and k not in ['source_url', 'date_scraped', 'program_url', 'tier'])
    total_fields = len(data) - 4
    data['confidence_score'] = round((fields_filled / total_fields) * 100, 2)
    
    return data

def main():
    """Main scraping function"""
    print("=" * 80)
    print("ENHANCED MBA PROGRAM SCRAPER v2")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Total programs to scrape: {len(MBA_PROGRAMS)}")
    print()
    
    all_programs = []
    successful = 0
    failed = 0
    
    for i, program_info in enumerate(MBA_PROGRAMS, 1):
        school = program_info['school']
        program = program_info['program']
        urls = program_info['urls']
        accreditation = program_info['accreditation']
        tier = program_info['tier']
        
        print(f"[{i}/{len(MBA_PROGRAMS)}] {school} - {program}")
        
        content_fetched = False
        working_url = None
        
        # Try each URL
        for url in urls:
            print(f"  Trying: {url}")
            content = fetch_with_web_fetch(url)
            
            if content and len(content) > 100:
                content_fetched = True
                working_url = url
                print(f"  ✓ Content fetched ({len(content)} chars)")
                break
        
        if content_fetched:
            data = extract_data_from_content(content, school, program, working_url, accreditation, tier)
            all_programs.append(data)
            successful += 1
            print(f"  ✓ Extracted data (confidence: {data['confidence_score']}%)")
        else:
            failed += 1
            print(f"  ✗ Failed to fetch content")
            # Still add minimal entry
            all_programs.append({
                'school_name': school,
                'program_name': program,
                'program_url': urls[0],
                'accreditation': accreditation,
                'tier': tier,
                'confidence_score': 0,
                'date_scraped': datetime.now().isoformat()
            })
        
        print()
        
        # Rate limiting
        if i < len(MBA_PROGRAMS):
            time.sleep(3)
    
    # Save to CSV
    output_file = '/root/.openclaw/workspace/research/onlinembaprograms-comprehensive.csv'
    
    fieldnames = [
        'school_name', 'program_name', 'tuition_total', 'tuition_per_credit',
        'in_state_tuition', 'out_of_state_tuition', 'format', 'duration',
        'total_credits', 'gmat_requirement', 'gre_accepted', 'acceptance_rate',
        'class_size', 'avg_salary', 'employment_rate', 'accreditation',
        'specializations', 'start_dates', 'application_deadlines',
        'program_url', 'source_url', 'date_scraped', 'confidence_score', 'tier'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_programs)
    
    print("=" * 80)
    print(f"✓ SAVED {len(all_programs)} programs to {output_file}")
    print("=" * 80)
    print()
    print("SUMMARY:")
    print(f"  Total programs: {len(all_programs)}")
    print(f"  Successful scrapes: {successful}")
    print(f"  Failed scrapes: {failed}")
    print(f"  Average confidence: {sum(p.get('confidence_score', 0) for p in all_programs)/len(all_programs):.1f}%")
    print(f"  Programs with 50%+ confidence: {sum(1 for p in all_programs if p.get('confidence_score', 0) >= 50)}")
    print()
    print("BREAKDOWN BY TIER:")
    tiers = {}
    for p in all_programs:
        t = p.get('tier', 'Unknown')
        tiers[t] = tiers.get(t, 0) + 1
    
    for tier, count in sorted(tiers.items()):
        print(f"  {tier}: {count}")
    
    return len(all_programs)

if __name__ == '__main__':
    main()
