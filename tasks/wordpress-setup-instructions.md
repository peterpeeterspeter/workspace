# WordPress Configuration for Content Cleanup

To run the cleanup script, add these credentials to your `.env` file:

---

## crashgamegambling.com
```
WORDPRESS_CRASHGAMEGAMBLING_URL=https://crashgamegambling.com/wp-json
WORDPRESS_CRASHGAMEGAMBLING_USER=your_username
WORDPRESS_CRASHGAMEGAMBLING_APP_PASSWORD=your_application_password
```

## cryptocrashgambling.com
```
WORDPRESS_CRYPTOCRASH_URL=https://cryptocrashgambling.com/wp-json
WORDPRESS_CRYPTOCRASH_USER=your_username
WORDPRESS_CRYPTOCRASH_APP_PASSWORD=your_application_password
```

## freecrashgames.com
```
WORDPRESS_FREECRASH_URL=https://freecrashgames.com/wp-json
WORDPRESS_FREECRASH_USER=your_username
WORDPRESS_FREECRASH_APP_PASSWORD=your_application_password
```

## crashcasino.io
```
WORDPRESS_CRASHCASINO_URL=https://crashcasino.io/wp-json
WORDPRESS_CRASHCASINO_USER=your_username
WORDPRESS_CRASHCASINO_APP_PASSWORD=your_application_password
```

---

## How to Generate WordPress Application Passwords

1. Log into WordPress admin
2. Go to: Users → Profile → Application Passwords
3. Enter a name (e.g., "OpenClaw Cleanup Script")
4. Click "Add New Application Password"
5. Copy the generated password (format: `xxxx xxxx xxxx xxxx xxxx xxxx`)
6. Paste into `.env` file

---

## Usage

**Dry run (safe, no deletions):**
```bash
python3 cleanup_wordpress.py --site crashgamegambling.com
```

**Execute deletions:**
```bash
python3 cleanup_wordpress.py --site crashgamegambling.com --execute
```

**Audit all sites (dry run):**
```bash
for site in crashgamegambling.com cryptocrashgambling.com freecrashgames.com; do
    python3 cleanup_wordpress.py --site $site
done
```

---

*Created: 2026-02-02*
