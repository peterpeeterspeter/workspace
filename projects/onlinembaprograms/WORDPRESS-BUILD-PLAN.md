# onlinembaprograms.com - WordPress Build Plan

**Project:** Affiliate website for online MBA programs
**Timeline:** 2-3 weeks to launch
**Tech Stack:** WordPress 6.x + GeneratePress + Custom Post Types
**Goal:** 200+ pages, automated content production, affiliate revenue

---

## Phase 1: Server & WordPress Setup (Days 1-2)

### 1.1 Server Setup

**Hosting Requirements:**
- PHP 8.0 or higher
- MySQL 5.7 or higher / MariaDB 10.2 or higher
- SSL certificate (Let's Encrypt)
- 10GB+ storage
- 2GB+ RAM recommended

**Recommended Hosting:**
- Cloudways (managed, fast, easy)
- SiteGround (good support, affordable)
- WP Engine (premium, managed)

**Tasks:**
- [ ] Purchase domain (onlinembaprograms.com)
- [ ] Set up hosting account
- [ ] Point DNS to hosting
- [ ] Install SSL certificate
- [ ] Verify site accessible via HTTPS

### 1.2 WordPress Installation

**Installation Steps:**
```bash
# Via hosting panel or WP-CLI
wp core install --url=https://onlinembaprograms.com \
  --title="OnlineMBAPrograms.com" \
  --admin_user=[your-admin] \
  --admin_password=[strong-password] \
  --admin_email=[your-email]
```

**WordPress Configuration:**
- [ ] Install WordPress 6.x (latest)
- [ ] Set permalink structure: `/post-name/`
- [ ] Set timezone: America/New_York (or your preference)
- [ ] Set site title and tagline
- [ ] Disable user registration
- [ ] Set comment policy (disable for affiliate site)

**Basic Settings:**
- [ ] Settings → General: Configure site details
- [ ] Settings → Reading: "Latest posts" (homepage)
- [ ] Settings → Discussion: Disable comments
- [ ] Settings → Media: Organize uploads (month/year)
- [ ] Settings → Permalinks: Post name

---

## Phase 2: Theme Setup (Days 2-3)

### 2.1 Theme Selection

**Theme: GeneratePress Premium**

**Why GeneratePress:**
- Fastest loading theme
- Clean code
- Modular design
- Affiliate-friendly
- Active development (500K+ installs)
- Excellent support

**Purchase & Install:**
- [ ] Purchase GeneratePress Premium ($59/year)
- [ ] Download theme ZIP file
- [ ] Upload to WordPress: Appearance → Themes → Add New → Upload
- [ ] Activate GeneratePress

### 2.2 Theme Configuration

**GeneratePress Settings:**
```
Appearance → Customize → GeneratePress Options

General:
- Site Layout: Wide (1400px max)
- Right Sidebar: Enabled (for affiliate widgets)
- Footer Widgets: 4 columns

Header:
- Site Identity: Logo upload
- Header Layout: Logo left, navigation right
- Navigation Location: Primary (below header)

Navigation:
- Primary Navigation: Enable
- Mobile Navigation: Enable (slide-out)
- Navigation Search: Enable

Blog:
- Blog Layout: Grid (3 columns)
- Excerpt Length: 55 words
- Featured Images: Enable
```

**Color Scheme:**
```
Appearance → Customize → Colors

Global Colors:
- Background: #ffffff (white)
- Text: #222222 (dark gray)
- Link: #0066cc (blue)
- Link Hover: #004499 (darker blue)

Header Colors:
- Background: #1a2332 (navy)
- Text: #ffffff (white)

Footer Colors:
- Background: #1a2332 (navy)
- Text: #cccccc (light gray)
```

### 2.3 Custom CSS

**Create Custom CSS File:**
```css
/* File: wp-content/themes/generatepress_child/style.css */

/* === Affiliate Buttons === */
.affiliate-cta {
    display: inline-block;
    background: #f59e0b; /* Gold/amber */
    color: #ffffff;
    padding: 12px 24px;
    border-radius: 6px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
}

.affiliate-cta:hover {
    background: #d97706;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* === Program Cards === */
.program-card {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 24px;
    background: #ffffff;
    transition: all 0.3s ease;
}

.program-card:hover {
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    transform: translateY(-4px);
}

/* === Star Ratings === */
.star-rating {
    color: #fbbf24;
    font-size: 1.2rem;
}

/* === Comparison Tables === */
.comparison-table {
    width: 100%;
    border-collapse: collapse;
}

.comparison-table th,
.comparison-table td {
    padding: 16px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}

.comparison-table th {
    background: #f9fafb;
    font-weight: 600;
}

/* === Quick Stats Box === */
.quick-stats {
    background: #f3f4f6;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}

.quick-stats-item {
    display: inline-block;
    margin-right: 24px;
}

/* === Mobile Optimization === */
@media (max-width: 768px) {
    .program-card {
        padding: 16px;
    }
    
    .quick-stats-item {
        display: block;
        margin: 8px 0;
    }
}
```

**Install Child Theme:**
- [ ] Create folder: `wp-content/themes/generatepress_child/`
- [ ] Create `style.css` with above CSS
- [ ] Create `functions.php` for theme customizations
- [ ] Activate child theme

---

## Phase 3: Plugin Installation (Days 3-4)

### 3.1 Essential Plugins

**Install These Plugins:**

1. **Pinch-to-Post** (Automation)
   - Already configured in workspace
   - Install via script or manual upload
   - Configure for onlinembaprograms site

2. **ThirstyAffiliates** (Link Management)
   - Download: https://wordpress.org/plugins/thirstyaffiliates/
   - Install and activate
   - Configure affiliate link cloaking
   - Set up link categories

3. **TablePress** (Comparison Tables)
   - Download: https://wordpress.org/plugins/tablepress/
   - Install and activate
   - Configure default table styling

4. **RankMath SEO** (SEO + Schema)
   - Download: https://wordpress.org/plugins/seo-by-rank-math/
   - Install and activate
   - Run setup wizard
   - Configure schema markup

5. **WP Rocket** (Caching/Performance)
   - Purchase: $59/year
   - Install and activate
   - Configure caching settings
   - Enable minification, lazy loading

6. **Shortcodes Ultimate** (Dynamic Content)
   - Download: https://wordpress.org/plugins/shortcodes-ultimate/
   - Install and activate

7. **Contact Form 7** (Forms)
   - Download: https://wordpress.org/plugins/contact-form-7/
   - Install and activate
   - Create contact form

8. **UpdraftPlus** (Backups)
   - Download: https://wordpress.org/plugins/updraftplus/
   - Install and activate
   - Schedule daily backups

**Installation:**
```bash
# Via WP-CLI
wp plugin install thirstyaffiliates tablepress \
  seo-by-rank-math shortcodes-ultimate \
  contact-form-7 updraftplus --activate

# Or via WordPress admin:
# Plugins → Add New → Search → Install → Activate
```

### 3.2 Plugin Configuration

**ThirstyAffiliates Setup:**
```
Affiliates → ThirstyAffiliates → Settings

General:
- Link Prefix: /recommend/
- NoFollow: Enable (for SEO)
- New Window: Enable (opens in new tab)
- Cloaking: Enable
- Auto-linking: Enable (for keywords)

Categories:
- University Programs
- Test Prep
- Learning Platforms
```

**RankMath Setup:**
```
RankMath → Dashboard → Setup Wizard

Step 1: Site Type = Affiliate Site
Step 2: Business Info = Your details
Step 3: Search Console = Connect (later)
Step 4: Schema = Enable Article schema
Step 5: Analytics = Connect Google Analytics (later)
Step 6: Webmaster = Verify site (later)
```

**WP Rocket Setup:**
```
Settings → WP Rocket

Cache:
- Enable mobile cache
- Enable gzip compression
- Minify CSS, JS
- Lazy load images
- Defer JS

File Optimization:
- Minify HTML, CSS, JS
- Combine files
- Remove query strings

Database:
- Clean database weekly
- Revisions limit: 10
```

---

## Phase 4: Custom Post Types (Days 4-5)

### 4.1 Create Custom Post Types

**Post Types Needed:**
- `mba_programs` (Program listings)
- `mba_reviews` (Detailed reviews)
- `mba_comparisons` (Comparison pages)

**Installation:**
```php
/* File: wp-content/themes/generatepress_child/functions.php */

// Register MBA Programs Post Type
function register_mba_programs_post_type() {
    $labels = array(
        'name' => 'MBA Programs',
        'singular_name' => 'MBA Program',
        'add_new' => 'Add New',
        'add_new_item' => 'Add New Program',
        'edit_item' => 'Edit Program',
        'new_item' => 'New Program',
        'view_item' => 'View Program',
        'search_items' => 'Search Programs',
        'not_found' => 'No programs found',
        'not_found_in_trash' => 'No programs in trash'
    );

    $args = array(
        'labels' => $labels,
        'public' => true,
        'has_archive' => true,
        'menu_icon' => 'dashicons-welcome-learn-more',
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt'),
        'rewrite' => array('slug' => 'programs'),
        'show_in_rest' => true,
        'capability_type' => 'post'
    );

    register_post_type('mba_programs', $args);
}
add_action('init', 'register_mba_programs_post_type');

// Register MBA Reviews Post Type
function register_mba_reviews_post_type() {
    $labels = array(
        'name' => 'MBA Reviews',
        'singular_name' => 'MBA Review',
        'add_new' => 'Add New Review',
        'add_new_item' => 'Add New Review',
        'edit_item' => 'Edit Review',
        'new_item' => 'New Review',
        'view_item' => 'View Review',
        'search_items' => 'Search Reviews',
        'not_found' => 'No reviews found',
        'not_found_in_trash' => 'No reviews in trash'
    );

    $args = array(
        'labels' => $labels,
        'public' => true,
        'has_archive' => true,
        'menu_icon' => 'dashicons-star-filled',
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt'),
        'rewrite' => array('slug' => 'reviews'),
        'show_in_rest' => true,
        'capability_type' => 'post'
    );

    register_post_type('mba_reviews', $args);
}
add_action('init', 'register_mba_reviews_post_type');
```

**Via Plugin Option:**
- Install "Custom Post Type UI" plugin
- Create post types via admin interface
- No coding required

### 4.2 Create Custom Fields

**Using Meta Box or ACF:**

**For MBA Programs:**
```
Fields:
- tuition_total (Text: Total tuition)
- tuition_per_credit (Text: Per credit cost)
- duration_months (Number: Program length)
- total_credits (Number: Credits required)
- gmat_required (Select: Yes/No/Waived)
- gre_accepted (Select: Yes/No)
- accreditation (Text: AACSB, etc.)
- us_news_ranking (Number: US News rank)
- fortune_ranking (Number: Fortune rank)
- program_url (URL: Official website)
- affiliate_link (URL: Affiliate link)
- format (Select: Online/Hybrid/Executive)
- specializations (Text: List of specializations)
- application_deadline (Date: Deadline)
- class_size (Number: Students per cohort)
- avg_salary (Number: Post-grad salary)
- employment_rate (Number: Employment %)
```

**For MBA Reviews:**
```
Fields:
- reviewed_program (Relationship: Link to MBA Program)
- rating_score (Number: 1-10)
- pros (Wysiwyg: Pros list)
- cons (Wysiwyg: Cons list)
- verdict (Wysiwyg: Final verdict)
- affiliate_disclosure (Text: Disclosure text)
```

**Installation:**
```bash
# Option 1: Meta Box (Free)
wp plugin install meta-box --activate

# Option 2: Advanced Custom Fields (Pro)
wp plugin install advanced-custom-fields --activate
```

**Field Configuration:**
- Use plugin UI to create field groups
- Assign to post types
- Configure display options

---

## Phase 5: Page Templates (Days 5-7)

### 5.1 Page Templates Structure

**Templates to Create:**
```
wp-content/themes/generatepress_child/
├── page-homepage.php
├── page-programs-hub.php
├── single-mba_programs.php
├── single-mba_reviews.php
├── taxonomy-program_type.php
├── archive-mba_programs.php
└── template-comparison.php
```

### 5.2 Homepage Template

**File: page-homepage.php**
```php
<?php
/**
 * Template Name: Homepage
 */

get_header();
?>

<div class="homepage-hero">
    <h1>Find Your Perfect Online MBA Program</h1>
    <p>Compare 95+ accredited programs from top universities</p>
    <a href="/programs/" class="affiliate-cta">Browse Programs</a>
</div>

<div class="featured-programs">
    <h2>Top 3 Online MBA Programs</h2>
    <?php
    $args = array(
        'post_type' => 'mba_programs',
        'posts_per_page' => 3,
        'meta_key' => 'us_news_ranking',
        'orderby' => 'meta_value_num',
        'order' => 'ASC'
    );
    $programs = new WP_Query($args);
    
    if ($programs->have_posts()) :
        while ($programs->have_posts()) : $programs->the_post();
            get_template_part('template-parts/program-card');
        endwhile;
    endif;
    wp_reset_postdata();
    ?>
</div>

<div class="quick-stats">
    <div class="quick-stats-item">
        <strong>95+</strong> Programs
    </div>
    <div class="quick-stats-item">
        <strong>$15K</strong> Avg Tuition
    </div>
    <div class="quick-stats-item">
        <strong>91%</strong> No GMAT
    </div>
</div>

<?php get_footer(); ?>
```

### 5.3 Program Hub Template

**File: page-programs-hub.php**
```php
<?php
/**
 * Template Name: Programs Hub
 */

get_header();
?>

<div class="programs-header">
    <h1>All Online MBA Programs</h1>
    <p>Compare programs by tuition, format, and ranking</p>
</div>

<div class="programs-filter">
    <!-- Filter options can be added here -->
</div>

<div class="programs-grid">
    <?php
    $args = array(
        'post_type' => 'mba_programs',
        'posts_per_page' => -1,
        'orderby' => 'title',
        'order' => 'ASC'
    );
    $programs = new WP_Query($args);
    
    if ($programs->have_posts()) :
        while ($programs->have_posts()) : $programs->the_post();
            get_template_part('template-parts/program-card');
        endwhile;
    endif;
    wp_reset_postdata();
    ?>
</div>

<?php get_footer(); ?>
```

### 5.4 Single Program Template

**File: single-mba_programs.php**
```php
<?php
get_header();

while (have_posts()) : the_post();
    
    $tuition = get_post_meta(get_the_ID(), 'tuition_total', true);
    $duration = get_post_meta(get_the_ID(), 'duration_months', true);
    $ranking = get_post_meta(get_the_ID(), 'us_news_ranking', true);
    $affiliate_link = get_post_meta(get_the_ID(), 'affiliate_link', true);
?>

<div class="program-header">
    <h1><?php the_title(); ?></h1>
    <div class="program-meta">
        <?php if ($ranking) : ?>
            <span class="ranking-badge">Ranking #<?php echo esc_html($ranking); ?></span>
        <?php endif; ?>
    </div>
</div>

<div class="program-quick-stats">
    <div class="stat">
        <strong>Tuition:</strong> $<?php echo esc_html($tuition); ?>
    </div>
    <div class="stat">
        <strong>Duration:</strong> <?php echo esc_html($duration); ?> months
    </div>
</div>

<div class="program-content">
    <?php the_content(); ?>
</div>

<div class="program-cta">
    <a href="<?php echo esc_url($affiliate_link); ?>" class="affiliate-cta" target="_blank" rel="nofollow">
        Visit School Site
    </a>
</div>

<?php endwhile; ?>

<?php get_footer(); ?>
```

### 5.5 Program Card Template Part

**File: template-parts/program-card.php**
```php
<?php
$tuition = get_post_meta(get_the_ID(), 'tuition_total', true);
$ranking = get_post_meta(get_the_ID(), 'us_news_ranking', true);
$affiliate_link = get_post_meta(get_the_ID(), 'affiliate_link', true);
?>

<div class="program-card">
    <?php if (has_post_thumbnail()) : ?>
        <div class="program-thumbnail">
            <?php the_post_thumbnail('medium'); ?>
        </div>
    <?php endif; ?>
    
    <h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
    
    <?php if ($ranking) : ?>
        <div class="ranking-badge">Ranking #<?php echo esc_html($ranking); ?></div>
    <?php endif; ?>
    
    <div class="program-tuition">
        <strong>Tuition:</strong> $<?php echo esc_html($tuition); ?>
    </div>
    
    <a href="<?php echo esc_url($affiliate_link); ?>" class="affiliate-cta" target="_blank" rel="nofollow">
        Learn More
    </a>
</div>
```

---

## Phase 6: Content Integration (Days 7-10)

### 6.1 Import MBA Programs Data

**Data Source:**
`/root/.openclaw/workspace/research/onlinembaprograms-comprehensive.csv`

**Import Process:**
1. Convert CSV to WordPress import format
2. Use WP All Import plugin or custom script
3. Map CSV columns to custom fields
4. Import 14 ready programs first (test)
5. Import remaining 81 programs (later)

**Import Script:**
```bash
# Via pinch-to-post
cd /root/.openclaw/workspace/scripts
./pinch-to-post.sh import onlinembaprograms programs.csv

# Or use WP All Import plugin
# Tools → Import → Upload CSV → Map Fields → Import
```

**Field Mapping:**
```
CSV Column → WordPress Field
school_name → Post Title
program_name → Meta Field: program_name
tuition_total → Meta Field: tuition_total
us_news_ranking → Meta Field: us_news_ranking
format → Meta Field: format
accreditation → Meta Field: accreditation
program_url → Meta Field: program_url
```

### 6.2 Create Initial Pages

**First 10 Pages:**
1. Homepage (template: homepage)
2. Programs Hub (template: programs-hub)
3. No-GMAT Programs Hub (category page)
4. Affordable Programs Hub (category page)
5. Requirements Guide (informational)
6. Comparison: Online vs Traditional
7. Accelerated Programs Guide
8. Tuition Guide
9. Salary Guide
10. ROI Calculator

**Page Creation:**
- [ ] Create pages in WordPress
- [ ] Assign appropriate templates
- [ ] Add content (from content calendar)
- [ ] Insert affiliate links
- [ ] Optimize for SEO (RankMath)
- [ ] Add schema markup

---

## Phase 7: Automation Integration (Days 10-12)

### 7.1 Configure Pinch-to-Post

**Setup Pinch-to-Post for onlinembaprograms:**
```bash
cd /root/.openclaw/workspace/scripts

# Test connection
./pinch-to-post.sh test onlinembaprograms

# Configure site
./pinch-to-post.sh config onlinembaprograms
```

**Configuration:**
- Site URL: https://onlinembaprograms.com
- WordPress credentials (admin + password)
- API access (XML-RPC or REST API)
- Post defaults (draft/publish, categories, tags)

### 7.2 Test Automated Publishing

**Test with 1 Article:**
```bash
# Run automated pipeline
/root/.openclaw/workspace/scripts/onlinembaprograms-automated-content-pipeline.sh

# Verify article created
# Check quality score (should be 70+)
# Test publishing via pinch-to-post
```

**Test Checklist:**
- [ ] Pipeline runs without errors
- [ ] NeuronWriter query created successfully
- [ ] SEO brief fetched
- [ ] Article generated (1,500 words)
- [ ] Content score ≥ 70
- [ ] Article published to WordPress
- [ ] Affiliate links working
- [ ] Schema markup added

### 7.3 Schedule Automated Runs

**Cron Job Already Configured:**
```
Mon/Wed/Fri at 09:00 CET
Runs: onlinembaprograms-automated-content-pipeline.sh
Output: 15 articles/month
```

**Verify Cron:**
```bash
crontab -l | grep onlinembaprograms
```

---

## Phase 8: Affiliate Integration (Days 12-14)

### 8.1 Join Affiliate Programs

**Immediate Actions:**
1. **Coursera** (Impact network)
   - Sign up: https://impact.com/
   - Join Coursera program
   - Get affiliate links

2. **edX** (direct)
   - Sign up: https://www.edx.org/affiliate
   - Get approved
   - Get affiliate links

3. **Amazon Associates**
   - Sign up: https://affiliate-program.amazon.com/
   - Get approval
   - Create affiliate links

### 8.2 Configure ThirstyAffiliates

**Add Affiliate Links:**
```
Affiliates → ThirstyAffiliates → Add New

Link Details:
- Name: Indiana Kelley Direct Online MBA
- URL: [Affiliate link]
- Slug: indiana-kelley-online-mba
- Category: University Programs
- NoFollow: Yes
- New Window: Yes

Cloaked URL: https://onlinembaprograms.com/recommend/indiana-kelley-online-mba
```

**Create Link Categories:**
- University Programs
- Test Prep
- Learning Platforms
- Books & Resources

### 8.3 Insert Affiliate Links in Content

**Automatic Linking:**
```
Affiliates → ThirstyAffiliates → Autolinker

Keywords to Link:
- "Visit School Site" → [Affiliate link]
- "Learn More" → [Affiliate link]
- "Request Information" → [Affiliate link]
- "Apply Now" → [Affiliate link]
```

**Manual Linking in Templates:**
```php
<a href="<?php echo esc_url($affiliate_link); ?>" class="affiliate-cta" target="_blank" rel="nofollow">
    Visit School Site
</a>
```

---

## Phase 9: SEO & Schema (Days 14-15)

### 9.1 Configure RankMath SEO

**Global Settings:**
```
RankMath → Titles & Meta

Homepage:
- Title Template: %site_title% - Find Your Perfect Online MBA Program
- Meta Description: Compare 95+ online MBA programs from top universities. Filter by tuition, format, and ranking. Find the perfect program for your goals.

Single Programs:
- Title Template: %program_name% at %university% - Tuition, Ranking & Review
- Meta Description: Detailed review of %program_name% at %university%. Tuition: $%tuition%, Duration: %duration% months, Ranking: #%ranking.

Single Reviews:
- Title Template: %university% %program_name% Review [Year] - Pros, Cons & Verdict
- Meta Description: Honest review of %university% %program_name%. Learn about curriculum, cost, ROI, and whether it's worth it.
```

### 9.2 Schema Markup

**Enable Schema Types:**
```
RankMath → Schema → Schema Generator

Article Schema:
- Enable for posts and custom post types
- Include headline, image, date, author

Review Schema:
- Enable for mba_reviews
- Include item reviewed, rating, author

Organization Schema:
- Enable site-wide
- Add logo, name, URL

Product Schema:
- Enable for mba_programs (optional)
- Include offers, aggregate rating
```

**Schema Configuration:**
```php
/* Add to functions.php */

add_filter('rank_math/snippet/rich_snippet_article', function($data) {
    // Customize article schema
    return $data;
});

add_filter('rank_math/snippet/rich_snippet_review', function($data) {
    // Customize review schema
    return $data;
});
```

### 9.3 XML Sitemap

**Generate Sitemap:**
```
RankMath → Sitemap Settings

Enable:
- Custom post types (mba_programs, mba_reviews)
- Taxonomies
- Image sitemap

Submit to Google:
- Copy sitemap URL: https://onlinembaprograms.com/sitemap_index.xml
- Add to Google Search Console
```

---

## Phase 10: Testing & QA (Days 15-16)

### 10.1 Functional Testing

**Test Checklist:**

**Homepage:**
- [ ] Hero section displays correctly
- [ ] Featured programs show (3 cards)
- [ ] Quick stats display
- [ ] CTAs working
- [ ] Mobile responsive

**Program Pages:**
- [ ] All 14 programs display
- [ ] Custom fields show (tuition, duration, etc.)
- [ ] Affiliate links work
- [ ] Internal links working
- [ ] Schema markup present

**Review Pages:**
- [ ] Star ratings display
- [ ] Pros/Cons show
- [ ] Verdict displays
- [ ] Affiliate disclosure visible
- [ ] Mobile responsive

**Search & Filter:**
- [ ] Search working
- [ ] Filters working (by category)
- [ ] Sorting works (tuition, ranking)

### 10.2 Performance Testing

**Google PageSpeed Insights:**
```
Test URLs:
- Homepage
- Program hub
- Single program
- Single review
- Comparison page

Target Scores:
- Mobile: 90+
- Desktop: 95+
- Load time: <2 seconds
```

**GTmetrix:**
```
Target:
- Grade: A
- Load time: <2s
- Total size: <500KB
- Requests: <50
```

### 10.3 SEO Testing

**RankMath Tests:**
```
RankMath → SEO Analysis

Test 5-10 pages:
- Homepage
- Top 3 program pages
- Top 3 review pages
- 1 comparison page

Check:
- Title tags optimized
- Meta descriptions present
- Keywords in H1
- Internal links
- External links
- Image alt tags
- Schema markup
```

**Google Search Console:**
```
Add site: https://onlinembaprograms.com
Verify ownership
Submit sitemap
Check for crawl errors
Test robots.txt
```

### 10.4 Affiliate Link Testing

**ThirstyAffiliates Tests:**
```
Test each affiliate link:
- Clicks through correctly
- Opens in new window
- Tracking working
- NoFollow present
- Cloaked URL works

Test categories:
- University programs (10 links)
- Test prep (5 links)
- Learning platforms (5 links)
```

**Click-Through Verification:**
- Test each affiliate program
- Verify link formatting
- Check tracking parameters
- Test on mobile

---

## Phase 11: Pre-Launch (Days 16-17)

### 11.1 Legal Pages

**Create Required Pages:**

**Privacy Policy:**
```
Page: Privacy Policy
Content: GDPR compliance, data collection, cookies
Template: Use legal template or generator
```

**Terms of Service:**
```
Page: Terms of Service
Content: Site usage, disclaimer, liability
Template: Use legal template
```

**Affiliate Disclosure:**
```
Page: Affiliate Disclosure (or in footer)
Content: FTC disclosure compliance
Example: "We earn commissions from qualifying purchases. This doesn't affect our recommendations."
```

**Contact Page:**
```
Page: Contact
Content: Contact form, email, social links
Form: Use Contact Form 7
```

### 11.2 Footer & Navigation

**Footer Setup:**
```
Footer Widget 1: About
Footer Widget 2: Quick Links
Footer Widget 3: Legal (Privacy, Terms, Disclosure)
Footer Widget 4: Social Media

Footer Copyright:
- Copyright notice
- Year (dynamic)
- Site name
```

**Navigation Menu:**
```
Primary Menu:
- Home
- Programs (dropdown by category)
- Reviews
- Compare
- About
- Contact

Secondary Menu (Footer):
- Privacy Policy
- Terms of Service
- Affiliate Disclosure
- Contact
```

### 11.3 Security Checklist

**Security Measures:**
- [ ] SSL certificate active (HTTPS)
- [ ] WordPress updated (latest version)
- [ ] All plugins updated
- [ ] Strong passwords (admin, FTP, database)
- [ ] Limit login attempts (install Wordfence or similar)
- [ ] Disable file editing in WordPress
- [ ] Disable XML-RPC if not needed
- [ ] Change default database prefix
- [ ] Install security plugin (Wordfence or iThemes Security)

**Security Plugin Installation:**
```bash
wp plugin install wordfence --activate
```

### 11.4 Backup Setup

**UpdraftPlus Configuration:**
```
Settings → UpdraftPlus Backups

Schedule:
- Manual backup before launch
- Automated daily backups after launch
- Retention: Keep 30 days of backups

Backup Locations:
- Local server
- Remote storage (Google Drive, Dropbox, etc.)

Backup Files:
- Database
- Themes
- Plugins
- Uploads
```

**Test Backup:**
```
UpdraftPlus → Backup Now
Verify backup created
Test restore process
```

---

## Phase 12: Launch (Day 18)

### 12.1 Pre-Launch Checklist

**Final Checks:**
- [ ] All 14 programs imported
- [ ] All 10 initial pages created
- [ ] Affiliate links tested and working
- [ ] SEO optimized (titles, meta descriptions, schema)
- [ ] Performance optimized (cache, minification)
- [ ] Security configured
- [ ] Backups scheduled
- [ ] Legal pages created
- [ ] Analytics installed (Google Analytics)
- [ ] Search Console connected
- [ ] Sitemap submitted
- [ ] Robots.txt configured
- [ ] SSL active
- [ ] Mobile responsive test passed
- [ ] Cross-browser test (Chrome, Firefox, Safari, Edge)
- [ ] Affiliate disclosure visible
- [ ] All forms working (contact)
- [ ] Email notifications configured

### 12.2 Launch Day Tasks

**Morning:**
1. **Final Backup**
   ```
   UpdraftPlus → Backup Now
   Download backup to local computer
   ```

2. **Go Live**
   - Change DNS if using staging
   - Verify site accessible via HTTPS
   - Test all pages
   - Test all forms
   - Test affiliate links

3. **Submit to Search Engines**
   ```
   Google Search Console:
   - Add property
   - Verify ownership
   - Submit sitemap
   - Request indexing for homepage

   Bing Webmaster Tools:
   - Add site
   - Verify
   - Submit sitemap
   ```

**Afternoon:**
4. **Monitor**
   - Check Google Analytics (real-time visitors)
   - Check Search Console (crawl stats)
   - Check server load
   - Check for errors

5. **Initial Promotion**
   - Share on social media (Twitter, LinkedIn)
   - Post in relevant communities (Reddit, forums)
   - Build initial backlinks (5-10)

6. **Start Content Automation**
   - Verify automated pipeline runs
   - Monitor first automated article
   - Check quality scores
   - Ensure publishing works

---

## Phase 13: Post-Launch (Weeks 2-4)

### 13.1 Week 1 Monitoring

**Daily Tasks:**
- [ ] Check analytics (visitors, traffic sources)
- [ ] Check Search Console (crawl errors, indexing)
- [ ] Check affiliate clicks (ThirstyAffiliates reports)
- [ ] Monitor automated content pipeline
- [ ] Respond to comments/contact form submissions
- [ ] Check for broken links
- [ ] Monitor server performance

**Weekly Tasks:**
- [ ] Review traffic growth
- [ ] Review affiliate earnings
- [ ] Check keyword rankings (RankMath reports)
- [ ] Update internal links
- [ ] Optimize underperforming pages
- [ ] Plan content for next week

### 13.2 Week 2 Optimization

**Content Optimization:**
- [ ] Add internal links (10-20 per page)
- [ ] Optimize images (compress, lazy load)
- [ ] Improve page load time
- [ ] A/B test CTAs
- [ ] Add schema markup missing pages

**SEO Optimization:**
- [ ] Build backlinks (10-20)
- [ ] Guest posts on relevant sites
- [ ] Submit to directories (MBA, education)
- [ ] Social bookmarking
- [ ] Forum participation (value-add, not spam)

### 13.3 Week 3-4 Scaling

**Content Production:**
- Continue automated pipeline (3 articles/week)
- Monitor quality scores
- Review and optimize low-scoring articles
- Expand to TIER 2 keywords

**Affiliate Optimization:**
- Test different CTAs
- Optimize link placement
- Test affiliate programs (drop low performers)
- Add new affiliate programs

**Technical Optimization:**
- Continue performance monitoring
- Test mobile experience
- Optimize for Core Web Vitals
- Fix any issues

---

## Phase 14: Month 1 Review (End of Month 1)

### 14.1 Analytics Review

**Traffic Metrics:**
```
Google Analytics → Reports

Check:
- Total visitors
- Traffic sources (organic, direct, referral, social)
- Top pages
- Bounce rate
- Time on site
- Pages per session
- Mobile vs desktop
```

**SEO Metrics:**
```
Google Search Console → Performance

Check:
- Total clicks
- Total impressions
- CTR (click-through rate)
- Average position
- Top keywords
- Top pages
```

**Revenue Metrics:**
```
ThirstyAffiliates → Reports

Check:
- Total clicks
- Top performing programs
- Revenue per program
- Conversion rate
- EPC (earnings per click)
```

### 14.2 Content Review

**Published Content:**
- Total articles published (target: 15)
- Average content score (target: 70+)
- Top performing articles
- Underperforming articles

**Optimization Needed:**
- Articles with low scores (revise)
- Articles with low traffic (optimize)
- Articles with low conversions (improve CTAs)

### 14.3 Technical Review

**Performance:**
- Load time (target: <2s)
- PageSpeed scores (target: 90+)
- Server uptime (target: 99.9%)
- Error logs (check for issues)

**Security:**
- Security scan (Wordfence)
- Plugin updates
- WordPress updates
- Backup completion

---

## Phase 15: Ongoing Maintenance (Monthly)

### 15.1 Monthly Tasks

**Content:**
- [ ] Review published articles
- [ ] Update outdated information
- [ ] Optimize low-performing pages
- [ ] Plan new content (based on data)
- [ ] Review content calendar

**SEO:**
- [ ] Check keyword rankings
- [ ] Build backlinks (10-20 per month)
- [ ] Update internal link structure
- [ ] Optimize for new keywords
- [ ] Review competitor strategies

**Technical:**
- [ ] Update WordPress core
- [ ] Update all plugins
- [ ] Run security scans
- [ ] Test backups
- [ ] Monitor server performance
- [ ] Check SSL certificate

**Revenue:**
- [ ] Review affiliate earnings
- [ ] Test new affiliate programs
- [ ] Optimize CTAs
- [ ] A/B test offers
- [ ] Review conversion funnels

### 15.2 Quarterly Tasks

**Content Audit:**
- [ ] Review all content
- [ ] Update outdated statistics
- [ ] Improve thin content
- [ ] Delete/redirect low-value pages
- [ ] Consolidate similar content

**SEO Deep Dive:**
- [ ] Full keyword research update
- [ ] Competitor analysis
- [ ] Technical SEO audit
- [ ] Backlink analysis
- [ ] Content gap analysis

**Revenue Optimization:**
- [ ] Test new affiliate programs
- [ ] Optimize top performers
- [ ] Drop low performers
- [ ] A/B test new placements
- [ ] Review commission rates

---

## Success Metrics

### Month 1 Targets
- **Pages Published:** 15 articles
- **Organic Traffic:** 200-400 visitors/day
- **Keywords in Top 100:** 20+
- **Affiliate Clicks:** 50-100
- **Revenue:** $300-$600

### Month 3 Targets
- **Pages Published:** 45 articles
- **Organic Traffic:** 800-1,500 visitors/day
- **Keywords in Top 50:** 15+
- **Affiliate Clicks:** 300-500
- **Revenue:** $1,500-$3,500

### Month 6 Targets
- **Pages Published:** 90 articles
- **Organic Traffic:** 2,000-3,500 visitors/day
- **Keywords in Top 20:** 20+
- **Affiliate Clicks:** 1,000-2,000
- **Revenue:** $5,000-$12,000

### Month 12 Targets
- **Pages Published:** 180+ articles
- **Organic Traffic:** 4,000-6,000 visitors/day
- **Keywords in Top 10:** 30+
- **Affiliate Clicks:** 3,000-5,000
- **Revenue:** $15,000-$30,000/month

---

## Timeline Summary

**Week 1:** Server, WordPress, Theme Setup (Days 1-7)
**Week 2:** Plugins, Custom Post Types, Templates (Days 8-14)
**Week 3:** Content Import, Automation, Affiliates (Days 15-21)
**Week 4:** Testing, QA, Launch (Days 22-28)

**Total:** 3-4 weeks to launch

---

## Cost Summary

### One-Time Costs:
- **Domain:** ~$10-15/year
- **GeneratePress Premium:** $59/year
- **WP Rocket:** $59/year
- **Total Setup:** ~$130/year

### Ongoing Costs:
- **Hosting:** $10-50/month
- **Affiliates:** FREE
- **Total Monthly:** ~$10-50

### First Year Total:
- **Setup:** $130
- **Hosting:** $120-600
- **Grand Total:** $250-730 Year 1

### Revenue Potential:
- **Conservative:** $40,000 Year 1
- **Aggressive:** $80,000 Year 1

**ROI:** 5,500% - 32,000% (conservative to aggressive)

---

## Next Steps

1. **Review this plan** - Make sure you're happy with everything
2. **Choose hosting** - Pick a provider and sign up
3. **Purchase domain** - Register onlinembaprograms.com
4. **Purchase theme** - Buy GeneratePress Premium
5. **Start building** - Follow the plan phase by phase
6. **Launch** - Go live and start earning

---

**Status:** Plan complete, ready to execute
**Timeline:** 3-4 weeks to launch
**Budget:** $250-730 Year 1
**Revenue Potential:** $40,000-$80,000 Year 1

---

*WordPress Build Plan Created: 2026-02-17*
*Project: onlinembaprograms.com*
*Type: Affiliate Site*
*Tech Stack: WordPress + GeneratePress + Custom Post Types*
