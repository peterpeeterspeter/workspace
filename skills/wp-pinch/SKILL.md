# OpenClaw Skill for WP Pinch

[WP Pinch](https://wp-pinch.com) turns your WordPress site into 88+ MCP tools you can use from OpenClaw. Publish posts, repurpose content with Molt, capture ideas with PinchDrop, manage WooCommerce orders, and run governance scans — all from chat.

[ClawHub](https://clawhub.ai/nickhamze/pinch-to-post) · [GitHub](https://github.com/RegionallyFamous/wp-pinch) · [Configuration](https://github.com/RegionallyFamous/wp-pinch/wiki/Configuration)

Install via ClawHub: `clawhub install nickhamze/pinch-to-post`

Or copy the SKILL.md into your OpenClaw workspace skills (e.g. `~/.openclaw/workspace/skills/wp-pinch/SKILL.md`).

---

## Quick Start

1. Install the WP Pinch plugin from [GitHub](https://github.com/RegionallyFamous/wp-pinch) or [wp-pinch.com](https://wp-pinch.com).
2. Set `WP_SITE_URL` in your OpenClaw environment (e.g. `https://mysite.com`).
3. Point your MCP server at `{WP_SITE_URL}/wp-json/wp-pinch/mcp` with an Application Password.
4. Start chatting — say "list my recent posts" or "create a draft about..."

For multiple sites, use different workspaces or env configs. See [Configuration](https://github.com/RegionallyFamous/wp-pinch/wiki/Configuration) for the full setup.

---

## When to use WP Pinch

- User asks to list, create, update, or delete posts → list-posts, get-post, create-post, update-post, delete-post
- User asks to find a post by ID or title → list-posts with search, then get-post
- User wants to capture an idea or link → PinchDrop: pinchdrop-generate (or Web Clipper / bookmarklet)
- User wants one post turned into many formats → Molt: wp-pinch/molt with a post_id
- User asks "what do I know about X?" → what-do-i-know with a query
- User wants stale posts surfaced → spaced-resurfacing (or daily Tide Report)
- User wants abandoned drafts completed in their voice → Ghost Writer: list-abandoned-drafts then ghostwrite

---

## Tool naming

All MCP tools are namespaced `wp-pinch/*` — e.g. wp-pinch/list_posts, wp-pinch/molt, wp-pinch/pinchdrop_generate.

---

## Quick reference

| Goal | Primary ability | Follow-up |
|------|-----------------|-----------|
| List posts (with filters) | list_posts | Use get_post with an ID for full content |
| Get one post | get_post | post_id required |
| Create/update/delete post | create_post, update_post, delete_post | |
| Capture idea → draft pack | pinchdrop_generate | Or use capture endpoint; then optionally create drafts |
| One post → many formats | wp-pinch/molt | post_id + optional output_types |
| "What do I know about X?" | what_do_i_know | query |
| Stale posts | spaced_resurfacing | days, optional category, tag, limit |
| Complete abandoned draft | list_abandoned_drafts then ghostwrite | post_id for ghostwrite |
| Content health report | content_health_report | Structure, readability, etc. |
| Suggest taxonomy terms | suggest_terms | post_id or content |
| Media | list_media, upload_media, delete_media | |
| Users / comments / settings | list_users, get_user, list_comments, moderate_comment, get_option, update_option | |

See Abilities Reference

---

## Errors

### Common Error Responses

- **`rate_limited`** — Back off and retry; respect Retry-After if present.
- **`validation_error`** or **`rest_invalid_param`** — Fix the request (missing param, length limit); don't retry unchanged.
- **`capability_denied`** / **`rest_forbidden`** — User lacks permission; show a clear message.
- **`post_not_found`** — Post ID invalid or deleted; suggest listing or searching.
- **`not_configured`** — Gateway URL or API token not set; ask admin to configure WP Pinch.

### Handling Rate Limits

When you get a 429 (rate limited), check for `Retry-After` header:

```json
{
  "code": "rate_limited",
  "message": "Too many requests. Please try again later.",
  "data": {
    "retry_after": 60
  }
}
```

Wait the specified number of seconds before retrying.

### Post Not Found

If a post ID doesn't exist:

```json
{
  "code": "post_not_found",
  "message": "The post with ID 123 does not exist or has been deleted."
}
```

Suggest actions:
- List recent posts to find valid IDs
- Search for the post by title
- Check if the post was deleted

### Not Configured

If the gateway isn't configured:

```json
{
  "code": "not_configured",
  "message": "WP Pinch is not configured. Please set the Gateway URL and API token."
}
```

User needs to:
1. Check OpenClaw gateway settings
2. Verify MCP connection
3. Confirm WP Pinch plugin is active

See [Error Codes](https://github.com/RegionallyFamous/wp-pinch/wiki/Error-Codes) for the full list.
