#!/usr/bin/env node
/**
 * Photostudio.io TikTok Slideshow Generator
 * Creates 9:16 TikTok slideshows from before/after images
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');

const execPromise = util.promisify(exec);

async function generateSlideshow(projectName, hook, options = {}) {
  const {
    duration = 30,        // Total video duration in seconds
    fps = 30,             // Frames per second
    resolution = '1080x1920',  // 9:16 aspect ratio
    outputDir = path.join(process.cwd(), 'output'),
    music = 'none'
  } = options;

  const inputDir = path.join(process.cwd(), 'slideshows', 'input', projectName);
  const outputFile = path.join(process.cwd(), 'slideshows', 'output', `${projectName}.mp4`);

  // Check if input directory exists
  if (!fs.existsSync(inputDir)) {
    console.error(`❌ ERROR: Input directory not found: ${inputDir}`);
    console.error(`   Create it and add your images:`);
    console.error(`   mkdir -p ${inputDir}`);
    console.error(`   # Add: before.jpg, after-1.jpg, after-2.jpg, etc.`);
    process.exit(1);
  }

  // Find images
  const images = [];
  const beforeImage = path.join(inputDir, 'before.jpg');
  const afterImages = [];

  // Get before image
  if (fs.existsSync(beforeImage)) {
    images.push(beforeImage);
  } else {
    console.error('❌ ERROR: before.jpg not found in input directory');
    process.exit(1);
  }

  // Get after images
  for (let i = 1; i <= 10; i++) {
    const afterImage = path.join(inputDir, `after-${i}.jpg`);
    if (fs.existsSync(afterImage)) {
      images.push(afterImage);
    }
  }

  if (images.length < 2) {
    console.error('❌ ERROR: Need at least 1 before image and 1 after image');
    process.exit(1);
  }

  console.log(`\n📸 Found ${images.length} images:`);
  console.log(`   ✓ before.jpg`);
  for (let i = 1; i < images.length; i++) {
    console.log(`   ✓ after-${i}.jpg`);
  }

  // Calculate duration per image
  const durationPerImage = Math.floor(duration / images.length);
  const lastImageDuration = duration - (durationPerImage * (images.length - 1));

  console.log(`\n🎬 Creating slideshow:`);
  console.log(`   Total duration: ${duration}s`);
  console.log(`   Per image: ${durationPerImage}s (last: ${lastImageDuration}s)`);
  console.log(`   Resolution: ${resolution}`);
  console.log(`   FPS: ${fps}`);

  // Create output directory
  fs.mkdirSync(outputDir, { recursive: true });

  // Build ffmpeg command
  let ffmpegCmd = 'ffmpeg -y ';

  // Add input files with durations
  images.forEach((img, idx) => {
    const imgDuration = idx === images.length - 1 ? lastImageDuration : durationPerImage;
    ffmpegCmd += `-loop 1 -t ${imgDuration} -i "${img}" `;
  });

  // Add filter complex for scaling and overlays
  let filterParts = images.map((_, idx) => {
    return `[${idx}:v]scale=${resolution}:force_original_aspect_ratio=decrease,pad=${resolution}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=${fps}[v${idx}];`;
  }).join('');

  const concatParts = images.map((_, idx) => `[v${idx}]`).join('');
  filterParts += `${concatParts}concat=n=${images.length}:v=1:a=0[outv]`;

  ffmpegCmd += `-filter_complex "${filterParts}" -map "[outv]" "${outputFile}"`;

  console.log(`\n⚙️  Executing ffmpeg...`);

  try {
    const { stdout, stderr } = await execPromise(ffmpegCmd);
    console.log(`\n✅ Slideshow created successfully!`);
    console.log(`   📁 Output: ${outputFile}`);
    console.log(`   📊 File size: ${(fs.statSync(outputFile).size / 1024 / 1024).toFixed(2)} MB`);

    // Generate caption
    console.log(`\n📝 Suggested Caption:`);
    console.log(`   ${hook}`);
    console.log(`   `);
    console.log(`   One photo → Ghost mannequin + flatlay + on-model + video in seconds.`);
    console.log(`   `);
    console.log(`   Link in bio ↗️`);
    console.log(`   `);
    console.log(`   #fashion #ecommerce #ai #productphotography #smallbusiness`);

    console.log(`\n🎵 Music Recommendation:`);
    console.log(`   Open TikTok → Check For You page → Find trending upbeat track`);
    console.log(`   Look for "↑ rising" badge → Use in your video`);

    return outputFile;
  } catch (error) {
    console.error(`\n❌ ERROR: Failed to create slideshow`);
    console.error(error.message);
    if (error.stderr) {
      console.error(`FFmpeg output: ${error.stderr}`);
    }
    process.exit(1);
  }
}

// Parse command line arguments
const args = process.argv.slice(2);
function getArg(name) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 ? args[idx + 1] : null;
}

const project = getArg('project');
const hook = getArg('hook') || 'AI creates your entire product catalog in seconds.';
const duration = parseInt(getArg('duration') || '30');
const music = getArg('music') || 'none';

if (!project) {
  console.error('Usage: node generate-photostudio-slideshow.js --project <project-name> [--hook "text"] [--duration 30] [--music style]');
  console.error('');
  console.error('Example:');
  console.error('  node generate-photostudio-slideshow.js --project first-project \\');
  console.error('    --hook "We replaced our photographer with AI. Here\'s what happened." \\');
  console.error('    --duration 30');
  process.exit(1);
}

// Run
generateSlideshow(project, hook, { duration, music });
