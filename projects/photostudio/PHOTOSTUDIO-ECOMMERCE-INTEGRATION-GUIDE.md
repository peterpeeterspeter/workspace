# Photostudio.io E-commerce Integration Guide
*API, WooCommerce, Shopify - Best Practices & Implementation*

**Date:** 2026-02-21
**Based on:** AI Fashion Photography Market Research 2026

---

## 📊 Market Context

**Why Now?**
- AI fashion photography market: $1.51B (2024) → $6.12B (2029)
- CAGR: 32.5% explosive growth
- 76% of small businesses report 80%+ cost savings with AI tools
- ROI: 340% increase vs traditional photography

**Key Platforms:**
- **Shopify:** 28% market share (e-commerce leader)
- **WooCommerce:** 24% market share (WordPress ecosystem)
- **Custom API:** Enterprise clients (48% prefer direct integration)

**Competitor Analysis:**
- **WearView:** Best overall for fashion (full pipeline)
- **Botika:** Shopify-native, AI model shots
- **Claid.ai:** Background replacement, batch processing
- **SellerPic:** Fashion models + AI video generation

---

## 🎯 Integration Strategy: "The Photostudio Way"

### Unique Value Proposition

**What Makes Photostudio Different:**
1. **Ghost Mannequin Automation** - No physical mannequin needed
2. **Batch Upload** - Process 100+ products in one go
3. **Cost Control** - Structured JSON (CCJ) for unit economics
4. **E-commerce Quality** - Professional product photos, not generic AI

### Target Customers (Priority Order)

**1. Mid-Market Fashion Brands (€50K-500K revenue)**
- Pain: Expensive photography (€5-20K per shoot)
- Need: Fast turnaround, consistent quality
- Budget: €500-2K/month for imagery

**2. E-commerce Agencies (10-100 clients)**
- Pain: Can't scale photography for all clients
- Need: White-label solution, bulk processing
- Budget: €2-10K/month

**3. Marketplace Sellers (Amazon, Bol.com, Zalando)**
- Pain: Strict image requirements, 1000s of SKUs
- Need: Platform-specific formatting, fast updates
- Budget: €300-1K/month

---

## 🔌 Option 1: Shopify Integration (HIGH PRIORITY)

### Why First?
- 28% e-commerce market share
- Fashion brands prefer Shopify (62% of mid-market)
- API is mature and well-documented
- Built-in app store distribution

### Integration Architecture

```
┌─────────────────┐
│  Photostudio    │
│  Backend API    │
└────────┬────────┘
         │
         ├──────────────────────────────┐
         │                              │
    ┌────▼────┐                    ┌────▼────┐
    │ Shopify │                    │ Admin   │
    │ App     │                    │ Panel   │
    └────┬────┘                    └─────────┘
         │
    ┌────▼────────────────────────────┐
    │ Shopify Storefront              │
    │ - Products                       │
    │ - Collections                    │
    │ - Orders                         │
    └──────────────────────────────────┘
```

### Technical Implementation

**1. Shopify App (Recommended)**

```javascript
// shopify-app.js (Node.js/Express)
const Shopify = require('shopify-api-node');
const axios = require('axios');

class PhotostudioShopifyApp {
  constructor(shop, accessToken) {
    this.shopify = new Shopify({
      shopName: shop,
      accessToken: accessToken
    });
    this.photostudioAPI = 'https://api.photostudio.io/v1';
  }

  // Sync products from Shopify
  async syncProducts() {
    const products = await this.shopify.product.list({ limit: 250 });
    return products.map(p => ({
      id: p.id,
      title: p.title,
      images: p.images.map(i => i.src),
      variants: p.variants.map(v => ({
        sku: v.sku,
        inventory_quantity: v.inventory_quantity
      }))
    }));
  }

  // Submit batch to Photostudio
  async submitBatch(products) {
    const response = await axios.post(`${this.photostudioAPI}/batch`, {
      products: products,
      settings: {
        output_format: 'shopify',
        quality: 'high',
        background_removal: true,
        ghost_mannequin: true
      }
    });
    return response.data;
  }

  // Update Shopify with generated images
  async updateProductImages(productId, imageUrls) {
    for (const imageUrl of imageUrls) {
      await this.shopify.productImage.create(productId, {
        src: imageUrl,
        position: 1 // Replace main image
      });
    }
  }
}
```

**2. Shopify Webhook Handler**

```javascript
// webhooks.js
app.post('/webhooks/products/create', async (req, res) => {
  const product = req.body;

  // Auto-generate images for new products
  const result = await photostudio.generate({
    type: 'fashion',
    images: [product.images[0].src],
    style: 'ghost-mannequin'
  });

  // Update product with AI images
  await shopify.productImage.update(product.id, {
    src: result.images[0].url
  });

  res.status(200).send('OK');
});
```

**3. Shopify Admin Panel**

```liquid
<!-- admin-panel.liquid -->
<div id="photostudio-app">
  <h2>AI Product Photography</h2>

  <div class="batch-upload">
    <input type="file" multiple accept="image/*">
    <button>Generate Images</button>
  </div>

  <div class="settings">
    <label>
      <input type="checkbox" checked> Ghost Mannequin
    </label>
    <label>
      <input type="checkbox" checked> Background Removal
    </label>
    <label>
      <select>
        <option>Catalog (white background)</option>
        <option>Lifestyle (scene backgrounds)</option>
        <option>On-Model (AI models)</option>
      </select>
    </label>
  </div>

  <div class="progress">
    <span>Processing: 0/100</span>
    <div class="bar"></div>
  </div>
</div>
```

### Pricing Strategy

**Shopify App Pricing:**
- **Free Tier:** 10 images/month (lead generation)
- **Starter:** €49/month - 100 images
- **Pro:** €199/month - 500 images + priority queue
- **Enterprise:** Custom - Unlimited + white-label

**Value Proposition:**
- Traditional photography: €5-20 per image
- Photostudio: €0.49-€1.99 per image
- **Savings: 80-95%**

### Launch Checklist

**Phase 1: MVP (2 weeks)**
- [ ] Shopify App submission (review takes 3-5 days)
- [ ] Basic batch upload (10 products at once)
- [ ] Ghost mannequin + background removal
- [ ] Auto-update Shopify products
- [ ] Free tier for first 100 users

**Phase 2: Features (4 weeks)**
- [ ] On-Model generation (AI models)
- [ ] Lifestyle backgrounds
- [ ] Video generation (10-second clips)
- [ ] Batch optimization (1000+ products)
- [ ] White-label for agencies

**Phase 3: Scale (8 weeks)**
- [ ] API for custom integrations
- [ ] Zapier integration
- [ ] Multi-language support
- [ ] Enterprise SLA
- [ ] Affiliate program

---

## 🔌 Option 2: WooCommerce Integration (MEDIUM PRIORITY)

### Why Second?
- 24% e-commerce market share
- WordPress ecosystem (15M+ sites)
- Larger installs, but lower average revenue
- REST API is well-documented

### Integration Architecture

```
┌─────────────────┐
│  Photostudio    │
│  Backend API    │
└────────┬────────┘
         │
         ├──────────────────────────────┐
         │                              │
    ┌────▼──────────┐              ┌────▼────┐
    │ WordPress     │              │ Admin   │
    │ Plugin        │              │ Panel   │
    └────┬──────────┘              └─────────┘
         │
    ┌────▼────────────────────────────┐
    │ WooCommerce                    │
    │ - Products (WooCommerce API)    │
    │ - REST API endpoints            │
    │ - Action scheduler (cron jobs)  │
    └────────────────────────────────┘
```

### Technical Implementation

**1. WordPress Plugin Structure**

```php
<?php
/**
 * Plugin Name: Photostudio AI Photography
 * Description: Generate AI product images for WooCommerce
 * Version: 1.0.0
 * Author: Photostudio
 */

// Prevent direct access
if (!defined('ABSPATH')) {
  exit;
}

class Photostudio_WooCommerce {

  private $api_url = 'https://api.photostudio.io/v1';
  private $api_key;

  public function __construct() {
    $this->api_key = get_option('photostudio_api_key');

    // Add admin menu
    add_action('admin_menu', [$this, 'add_admin_menu']);

    // Add bulk action
    add_filter('bulk_actions-edit-product', [$this, 'register_bulk_action']);

    // Handle bulk action
    add_filter('handle_bulk_actions-edit-product', [$this, 'handle_bulk_action'], 10, 3);

    // Add product meta box
    add_action('add_meta_boxes', [$this, 'add_meta_box']);
  }

  public function add_admin_menu() {
    add_menu_page(
      'Photostudio',
      'Photostudio AI',
      'manage_options',
      'photostudio',
      [$this, 'admin_page'],
      'dashicons-format-image',
      30
    );
  }

  public function register_bulk_action($bulk_actions) {
    $bulk_actions['photostudio_generate'] = __('Generate AI Images', 'photostudio');
    return $bulk_actions;
  }

  public function handle_bulk_action($redirect_url, $action, $product_ids) {
    if ($action !== 'photostudio_generate') {
      return $redirect_url;
    }

    $batch_id = $this->submit_batch($product_ids);

    $redirect_url = add_query_arg([
      'photostudio_batch' => $batch_id,
      'generated' => count($product_ids)
    ], $redirect_url);

    return $redirect_url;
  }

  private function submit_batch($product_ids) {
    $products = [];

    foreach ($product_ids as $product_id) {
      $product = wc_get_product($product_id);
      $image_id = $product->get_image_id();
      $image_url = wp_get_attachment_image_url($image_id, 'full');

      $products[] = [
        'product_id' => $product_id,
        'sku' => $product->get_sku(),
        'image_url' => $image_url,
        'title' => $product->get_title()
      ];
    }

    $response = wp_remote_post($this->api_url . '/batch', [
      'headers' => [
        'Authorization' => 'Bearer ' . $this->api_key,
        'Content-Type' => 'application/json'
      ],
      'body' => json_encode([
        'products' => $products,
        'settings' => [
          'output_format' => 'woocommerce',
          'quality' => 'high',
          'ghost_mannequin' => true
        ]
      ]),
      'timeout' => 45
    ]);

    $body = json_decode(wp_remote_retrieve_body($response), true);
    return $body['batch_id'];
  }

  public function admin_page() {
    ?>
    <div class="wrap">
      <h1>Photostudio AI Photography</h1>

      <div class="card">
        <h2>Batch Generate Images</h2>
        <p>Select products from the <a href="<?php echo admin_url('edit.php?post_type=product'); ?>">Products page</a> and choose "Generate AI Images" from the bulk actions.</p>
      </div>

      <div class="card">
        <h2>Settings</h2>
        <label>API Key:</label>
        <input type="text" name="photostudio_api_key" value="<?php echo esc_attr($this->api_key); ?>">
        <button>Save</button>
      </div>

      <div class="card">
        <h2>Recent Batches</h2>
        <table class="wp-list-table widefat fixed striped">
          <thead>
            <tr>
              <th>Batch ID</th>
              <th>Date</th>
              <th>Products</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <?php foreach ($this->get_recent_batches() as $batch): ?>
            <tr>
              <td><?php echo $batch['batch_id']; ?></td>
              <td><?php echo $batch['created_at']; ?></td>
              <td><?php echo $batch['product_count']; ?></td>
              <td><?php echo $batch['status']; ?></td>
            </tr>
            <?php endforeach; ?>
          </tbody>
        </table>
      </div>
    </div>
    <?php
  }
}

// Initialize plugin
new Photostudio_WooCommerce();
```

**2. REST API Endpoint**

```php
// api.php
register_rest_route('photostudio/v1', '/batch', [
  'methods' => 'POST',
  'callback' => function($request) {
    $batch_id = $request->get_param('batch_id');

    // Fetch batch status from Photostudio API
    $response = wp_remote_get(
      'https://api.photostudio.io/v1/batch/' . $batch_id,
      ['headers' => ['Authorization' => 'Bearer ' . get_option('photostudio_api_key')]]
    );

    $body = json_decode(wp_remote_retrieve_body($response), true);

    // Update WooCommerce products
    foreach ($body['products'] as $product) {
      $wc_product = wc_get_product($product['product_id']);

      // Set main image
      $wc_product->set_image_id($this->upload_image($product['generated_image_url']));
      $wc_product->save();
    }

    return new WP_REST_Response(['success' => true], 200);
  },
  'permission_callback' => function() {
    return current_user_can('manage_options');
  }
]);
```

### Pricing Strategy

**WooCommerce Plugin Pricing:**
- **Free:** 50 images/month (WordPress.org repository)
- **Pro:** €79/year - 500 images
- **Agency:** €299/year - Unlimited + white-label

**Why Lower Than Shopify?**
- WooCommerce merchants spend less on average
- Larger install base = volume strategy
- WordPress.org repository = free marketing

### Launch Checklist

**Phase 1: MVP (1 week)**
- [ ] Submit to WordPress.org (review takes 3-7 days)
- [ ] Bulk action for products page
- [ ] Basic batch upload
- [ ] Ghost mannequin + background removal
- [ ] Settings page (API key)

**Phase 2: Features (3 weeks)**
- [ ] Webhook handler (auto-update products)
- [ ] On-Model generation
- [ ] Cron job integration
- [ ] Multi-site support
- [ ] Pro version upgrade

**Phase 3: Scale (6 weeks)**
- [ ] HPOS compatibility
- [ ] Block editor integration
- [ ] Custom product fields support
- [ ] Performance optimization
- [ ] Agency white-label program

---

## 🔌 Option 3: Direct API Integration (ENTERPRISE)

### Why For Enterprise?
- Large retailers (500+ SKUs)
- Custom platforms (Magento, Custom builds)
- White-label requirements
- Data control & security

### API Architecture

```
┌───────────────────────────────────────────┐
│  Photostudio API Gateway                   │
│  - Rate limiting (1000 req/min)            │
│  - Authentication (API keys + OAuth)       │
│  - Webhook support                         │
│  - Batch processing queue                  │
└────────┬──────────────────────────────────┘
         │
         ├──────────────────────────────────┐
         │                                  │
    ┌────▼──────────┐                ┌──────▼─────┐
    │ REST API      │                │ GraphQL    │
    │ /v1/batch     │                │ /v1/graphql │
    │ /v1/products  │                │             │
    │ /v1/webhooks  │                │             │
    └───────────────┘                └─────────────┘
```

### API Endpoints

**1. Authentication**

```http
POST /api/v1/auth/token
Authorization: Basic <base64(client_id:client_secret)>

Response:
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "eyJ..."
}
```

**2. Submit Batch**

```http
POST /api/v1/batch
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "batch_name": "Spring Collection 2026",
  "products": [
    {
      "external_id": "SKU-12345",
      "image_url": "https://cdn.shop.com/product.jpg",
      "settings": {
        "type": "ghost-mannequin",
        "background_color": "#FFFFFF",
        "output_format": "jpeg",
        "quality": "high",
        "dimensions": {
          "width": 1200,
          "height": 1500
        }
      }
    }
  ],
  "webhook_url": "https://api.shop.com/webhooks/photostudio",
  "priority": "normal"
}

Response:
{
  "batch_id": "batch_abc123",
  "status": "queued",
  "estimated_time": 180,
  "product_count": 1
}
```

**3. Check Batch Status**

```http
GET /api/v1/batch/{batch_id}
Authorization: Bearer <access_token>

Response:
{
  "batch_id": "batch_abc123",
  "status": "processing",
  "progress": {
    "completed": 45,
    "total": 100,
    "percentage": 45
  },
  "products": [
    {
      "external_id": "SKU-12345",
      "status": "completed",
      "generated_images": [
        {
          "url": "https://cdn.photostudio.io/generated/abc123.jpg",
          "type": "ghost-mannequin",
          "metadata": {
            "model_version": "v4.2",
            "processing_time": 3.2,
            "confidence": 0.98
          }
        }
      ]
    }
  ]
}
```

**4. Webhook Handler**

```javascript
// webhook-handler.js (Express.js)
app.post('/webhooks/photostudio', async (req, res) => {
  const { batch_id, status, products } = req.body;

  if (status === 'completed') {
    // Update your database with generated images
    for (const product of products) {
      await db.products.update(product.external_id, {
        images: product.generated_images.map(img => img.url),
        photostudio_batch_id: batch_id,
        photostudio_processed_at: new Date()
      });
    }

    // Trigger CDN cache refresh
    await cdn.purgeCache(products.map(p => p.external_id));
  }

  res.status(200).send('OK');
});
```

### API Rate Limits

| Plan | Requests/Minute | Burst | Monthly Quota |
|------|-----------------|-------|---------------|
| Starter | 10 | 20 | 1,000 |
| Pro | 100 | 200 | 50,000 |
| Enterprise | 1,000 | 2,000 | Unlimited |

### Pricing Strategy

**API Pricing:**
- **Starter:** €99/month - 1,000 images
- **Pro:** €499/month - 50,000 images
- **Enterprise:** Custom - Unlimited + SLA

**Unit Economics:**
- Cost per image: €0.01-€0.10
- Competitor cost: €0.50-€5.00
- **Margin: 90-95%**

### Launch Checklist

**Phase 1: Private Beta (2 weeks)**
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Authentication & rate limiting
- [ ] Batch processing queue
- [ ] Webhook infrastructure
- [ ] 3 beta customers

**Phase 2: Public Launch (4 weeks)**
- [ ] API dashboard (analytics, usage)
- [ ] SDK libraries (Python, Node.js, PHP)
- [ ] GraphQL endpoint
- [ ] Sandbox environment
- [ ] Developer portal

**Phase 3: Scale (8 weeks)**
- [ ] Enterprise SLA
- [ ] Dedicated support
- [ ] Custom model training
- [ ] White-label option
- [ ] API reseller program

---

## 🎯 Recommended Launch Order

### Month 1: Shopify App (MVP)
**Why:** Largest market share, easier distribution

**Deliverables:**
- Shopify App submission
- Basic batch upload (10 products)
- Ghost mannequin + background removal
- Free tier (10 images/month)
- Pricing: €49-199/month

**Success Metrics:**
- 100 installs in first month
- 20% conversion to paid
- 4.5+ star rating

### Month 2: WooCommerce Plugin
**Why:** WordPress.org repository = free marketing

**Deliverables:**
- WordPress.org submission
- Bulk action integration
- Basic batch upload
- Free tier (50 images/month)
- Pricing: €79-299/year

**Success Metrics:**
- 500 active installs
- 10% conversion to Pro
- 4.0+ star rating

### Month 3: Public API
**Why:** Enterprise customers, white-label revenue

**Deliverables:**
- Public API documentation
- Developer portal
- SDK libraries (Python, Node.js, PHP)
- Sandbox environment
- Pricing: €99-499/month

**Success Metrics:**
- 50 API keys issued
- 10 enterprise customers
- €10K MRR

---

## 📊 Revenue Projections

**Year 1 (Conservative):**
- Shopify App: 200 customers × €99/month = €19.8K/month
- WooCommerce: 500 customers × €79/year = €3.3K/month
- API: 20 customers × €499/month = €10K/month
- **Total: €33K/month = €396K/year**

**Year 2 (Moderate Growth):**
- Shopify: 1,000 × €149 = €149K/month
- WooCommerce: 2,500 × €99/year = €20.6K/month
- API: 100 × €999 = €99.9K/month
- **Total: €269K/month = €3.2M/year**

**Year 3 (Aggressive):**
- Shopify: 5,000 × €199 = €995K/month
- WooCommerce: 10,000 × €149/year = €124K/month
- API: 500 × €1,999 = €999.5K/month
- **Total: €2.1M/month = €25.2M/year**

---

## 🚀 Quick Start (This Week)

**Day 1-2: Shopify MVP**
- [ ] Create Shopify App scaffold
- [ ] Implement batch upload (10 products)
- [ ] Connect to Photostudio API
- [ ] Test ghost mannequin generation

**Day 3-4: Admin Panel**
- [ ] Build settings page
- [ ] Add progress indicator
- [ ] Implement webhook handler
- [ ] Auto-update products

**Day 5: Testing & Launch**
- [ ] Beta test with 5 stores
- [ ] Fix bugs
- [ ] Submit to Shopify App Store
- [ ] Create landing page

**Day 6-7: Documentation**
- [ ] User guide
- [ ] API documentation
- [ ] Video tutorials
- [ ] Email templates

---

## 🔑 Key Success Factors

**1. Speed = Competitive Advantage**
- "Professional product photos in 30 seconds"
- Batch processing (100+ products at once)
- Real-time progress updates
- Auto-publish to store

**2. Quality = Retention**
- E-commerce grade images (1200×1500px)
- Consistent lighting & colors
- Multiple angles (front, side, detail)
- Platform-specific formatting

**3. Cost Control = Profitability**
- Structured JSON (CCJ) for unit economics
- Track cost-per-image by customer
- Optimize GPU usage
- Cloud cost monitoring

**4. Distribution = Growth**
- Shopify App Store (built-in traffic)
- WordPress.org repository (SEO)
- API reseller program (partners)
- Content marketing (case studies)

---

## 🎬 Next Actions

**Today:**
1. Decide: Which integration first? (Shopify recommended)
2. Create Photostudio API specification
3. Set up development environment
4. Start Shopify App scaffold

**This Week:**
1. Build MVP (batch upload + ghost mannequin)
2. Test with 3 beta stores
3. Create landing page + pricing
4. Submit to Shopify App Store

**This Month:**
1. Launch Shopify App
2. Start WooCommerce plugin
3. Document API for public launch
4. Create case studies (first 10 customers)

**Questions? Let me know!**

---

*Generated by Midnight Surprise System*
*Date: 2026-02-21*
*Source: AI Fashion Photography Market Research 2026*
