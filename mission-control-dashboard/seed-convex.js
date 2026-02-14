// Manual seed script for Convex Mission Control
// Run with: node seed-convex.js

const CONVEX_URL = "https://fast-duck-920.convex.cloud";
const DEPLOY_KEY = "dev:fast-duck-920|eyJ2MiI6ImMwNGVkMzQ5NGE4NzRkNWRhNDM4MDQ4NDc4OWQ4MWY0In0=";

async function seedConvex() {
  const now = Date.now();

  // Create agents
  const agents = await fetch(`${CONVEX_URL}/api/agents`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Convex ${DEPLOY_KEY}`
    },
    body: JSON.stringify({
      args: {},
      // We'll need to use the mutation endpoint format
    })
  });

  console.log("Seeding complete!");
}

seedConvex().catch(console.error);
