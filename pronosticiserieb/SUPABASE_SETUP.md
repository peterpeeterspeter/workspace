# 📘 Supabase Setup - Click-by-Click Guide

## Step 1: Create Account (2 minutes)

### Option A: Use GitHub (Fastest)
1. Go to: https://supabase.com
2. Click "Start your project" button
3. Click "Continue with GitHub"
4. Authorize GitHub access
5. **Skip to Step 2** ✅

### Option B: Use Email (if no GitHub)
1. Go to: https://supabase.com
2. Click "Start your project" button
3. Click "Sign up" (bottom of dialog)
4. Enter email + password
5. Check email for verification link
6. Click verification link
7. Log in

---

## Step 2: Create Organization (1 minute)

After logging in:

1. **If this is your first time:**
   - Enter organization name: `PeterPeeters` (or your preference)
   - Click "Create organization"

2. **If you already have an organization:**
   - You'll see it listed
   - Click on it or skip to Step 3

---

## Step 3: Create Project (2 minutes)

1. Click **"New Project"** button
   - Usually top-right or in organization view

2. Fill in the form:
   ```
   Name: pronosticiserieb
   Database Password: [Generate one or use your own]
   Region: EU West (Frankfurt) ← Important for Italy
   Pricing Plan: Free (recommended for launch)
   ```

3. Click **"Create new project"**

4. **Wait 2-3 minutes** for provisioning
   - You'll see a progress bar
   - It will say "Preparing your project..."

---

## Step 4: Get Your Credentials (1 minute)

Once project is ready:

### Find API Keys
1. You should be on the project dashboard
2. Look for **"Project API Keys"** or click **Settings** (left sidebar) → **API**
3. You'll see three important keys:

**Copy these somewhere safe:**

```
Project URL: https://xxxxx.supabase.co
anon public: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
service_role: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

⚠️ **IMPORTANT:**
- **Project URL** - Needed for frontend
- **anon public key** - Needed for frontend (safe to share)
- **service_role key** - Needed for backend/sync (NEVER share, admin access)

---

## Step 5: Launch SQL Editor (30 seconds)

1. In left sidebar, click **"SQL Editor"**
2. You'll see a query editor (like a code editor)
3. Leave this open - I'll need you to paste the schema here

---

## ✅ Done! Send Carlottta These Three Things:

```
1. Project URL: https://xxxxx.supabase.co
2. Anon Key: eyJhbGci... (the "public" one)
3. Service Role Key: eyJhbGci... (the "service_role" one)
```

Just paste them here in Telegram like:
```
Supabase URL: https://abc123.supabase.co
Anon: eyJhbGci...
Service: eyJhbGci...
```

---

## 🎯 What Happens Next

Once I have the credentials:
1. ✅ I'll deploy the database schema
2. ✅ Set up the connection
3. ✅ Test everything works
4. ✅ We're ready for Day 2 deployment!

---

## 📸 Screenshots Reference

**What you should see:**

### Login Page
- [ ] "Start your project" button visible
- [ ] GitHub login option OR email/password form

### Project Creation
- [ ] Name field
- [ ] Password field (with generate option)
- [ ] Region dropdown (select EU West)
- [ ] Pricing plan selector (Free/Pro)

### Dashboard (After Creation)
- [ ] Left sidebar with: Table Editor, SQL Editor, etc.
- [ ] Project info card
- [ ] API keys section

### API Keys Page
- [ ] Project URL field
- [ ] Two keys listed: anon public, service_role
- [ ] Copy buttons next to each

---

## ⚠️ Common Issues

**Issue:** "Stuck on creating project"
- **Solution:** Wait 2-3 minutes, it's normal

**Issue:** "Region selection"
- **Solution:** Choose EU West for fastest connection to Italy

**Issue:** "Which key do I use?"
- **Solution:** Send all three (URL, anon, service_role) - I'll sort them

**Issue:** "Can't find API keys"
- **Solution:** Settings → API (left sidebar)

---

## 🔐 Security Note

**Safe to share with Carlottta:**
- ✅ Project URL
- ✅ Anon public key (limited access)

**Keep private (never share):**
- ❌ Service role key (admin access)
- ❌ Database password

*Note: I need service role key for the sync script, but I'll store it securely in environment variables, not in any code.*

---

*Ready when you are! Click away and send me those keys.* 🚀
