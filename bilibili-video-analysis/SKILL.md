---
name: bilibili-video-analysis
description: Download and analyze Bilibili videos — extract metadata, comments, download video via API, extract frames with ffmpeg, and analyze with vision AI. Use when a user shares a Bilibili video URL and wants content analysis, game review, or visual breakdown.
version: 1.0.0
metadata:
  hermes:
    tags: [bilibili, video, analysis, gaming, ffmpeg, vision]
  prerequisites:
    commands: [ffmpeg, curl]
    packages: [ffmpeg]
  examples:
    - Analyze a Honor of Kings gameplay video
    - Extract and describe key frames from any Bilibili video
    - Summarize video content from frame-by-frame visual analysis
---

# Bilibili Video Analysis

Download and visually analyze Bilibili videos. B站's website blocks direct HTTP/yt-dlp access (412 Precondition Failed), but their **API endpoints work** with proper headers.

## Workflow

### 1. Extract BV ID from URL

```
URL: https://www.bilibili.com/video/BV1vj9bBrEhZ/?...
BV ID: BV1vj9bBrEhZ
```

### 2. Get Video Metadata (always works)

```bash
curl -s -m 20 \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -H "Referer: https://www.bilibili.com/" \
  "https://api.bilibili.com/x/web-interface/view?bvid=BV_ID"
```

Key fields from response `data`:
- `title` — video title
- `desc` — description
- `duration` — seconds
- `owner.name` — UP主 name
- `stat.view/like/coin/favorite` — engagement stats
- `aid` — numeric video ID (needed for next steps)
- `cid` — numeric part ID (needed for video stream)
- `pages[0].cid` — fallback cid if single-part video

### 3. Get Comments (optional, for context)

```bash
AID=<numeric aid from step 2>
curl -s -m 20 \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -H "Referer: https://www.bilibili.com/" \
  "https://api.bilibili.com/x/v2/reply?type=1&oid=${AID}&sort=2&pn=1&ps=20"
```

Parse `data.replies[].content.message` for top comments.

### 4. Get Video Stream URL

```bash
AID=<aid>
CID=<cid>
curl -s -m 20 \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -H "Referer: https://www.bilibili.com/video/BV_ID/" \
  "https://api.bilibili.com/x/player/playurl?avid=${AID}&cid=${CID}&qn=32&fnval=1&fourk=0"
```

- `qn=32` = 480p (smaller download, enough for frame analysis)
- `qn=64` = 720p, `qn=80` = 1080p
- Response: `data.durl[0].url` — the actual video stream URL

### 5. Download Video

```bash
curl -s -L -o /tmp/bili_video.mp4 \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -H "Referer: https://www.bilibili.com/" \
  "${VIDEO_URL}"
```

**Critical:** Must include Referer header or download fails.

### 6. Extract Frames with ffmpeg

```bash
# One frame every N seconds (adjust based on video length)
# For a 5-min video: every 15s = ~20 frames
# For a 10-min video: every 30s = ~20 frames
mkdir -p /tmp/bili_frames
ffmpeg -y -i /tmp/bili_video.mp4 -vf "fps=1/15" -q:v 2 /tmp/bili_frames/frame_%03d.jpg
```

Target: ~15-25 frames for good coverage without overwhelming vision analysis.

### 7. Analyze Frames with vision_analyze

Batch analyze key frames (not all — pick representative ones):
- First 2-3 frames: opening/early game
- Middle frames: key moments
- Last 2-3 frames: ending/result

Ask specific questions per frame based on context (e.g., "describe score, gold difference, hero positions, team fights").

## Full-Frame Parallel Analysis (when user wants ALL frames analyzed)

When the user requests dense extraction (e.g. 1fps) and full analysis of every frame, the
sequential approach is too slow. Use **parallel delegate_task batching**:

### Extraction
```bash
# 1fps for dense coverage (e.g. 549 frames for a 9-min video)
mkdir -p /tmp/bili_frames
ffmpeg -y -i /tmp/bili_video.mp4 -vf "fps=1" -q:v 2 /tmp/bili_frames/frame_%04d.jpg
```

### Parallel Batch Analysis
Split frames into batches of ~55 frames each. Run 3 batches concurrently (default max_concurrent_children).
For 549 frames: 10 batches, ~4 rounds of 3+3+3+1.

```python
# Example batch ranges for 549 frames, 10 batches:
# Batch 1:  frame_0001 - frame_0055
# Batch 2:  frame_0056 - frame_0110
# ...
# Batch 10: frame_0496 - frame_0549
```

Each subagent gets:
- `toolsets: ["vision", "file"]`
- Instructions to use `vision_analyze` on every frame in its range
- Instructions to save summary to `/tmp/bili_batch_NN.md`
- Focus prompt: what to look for (text overlays, UI elements, game state, etc.)

Parent reads all batch files with `execute_code`, then synthesizes.

### Timing Benchmarks (from real session)
- 55 frames per subagent: ~5-6 minutes (vision_analyze per frame ~3-5s)
- 3 concurrent subagents: ~6 minutes per round
- 10 batches total: ~10-12 minutes (vs 30+ minutes sequential)

### Pitfalls
- Each subagent has no context from other batches — make the focus prompt self-contained
- vision_analyze character limits can truncate long descriptions — instruct subagents to save files immediately
- Use 4-digit frame numbering (`frame_%04d.jpg`) to avoid lexicographic sorting issues

### Multi-Video Batch Workflow

When analyzing multiple videos (e.g. 4 videos totaling 88 minutes):

1. **Get metadata** for all videos first (parallel API calls via execute_code)
2. **Download** all videos in parallel via delegate_task (3 concurrent)
3. **Extract frames** for all videos in parallel via terminal (4 concurrent ffmpeg calls)
4. **Analyze frames** in 80-frame batches via delegate_task (3 concurrent)
   - Process one video at a time, round-robin through batches
   - Each batch takes ~5-8 minutes with 80 frames
   - A 24-min video (1440 frames) = 18 batches = 6 rounds ≈ 30-40 min
   - A 34-min video (2048 frames) = 26 batches = 9 rounds ≈ 45-60 min
5. **Synthesize** by reading all batch summary files, then create wiki/report

Total wall-clock time for 4 videos (~5300 frames): ~60-90 minutes with 3 concurrent subagents.

## Pitfalls

- **B站 412 error**: Direct website access and yt-dlp both fail. Always use the API approach.
- **Danmaku (弹幕)**: The `dm/list.so` endpoint returns binary protobuf, not XML. Skip it or use a protobuf parser.
- **Video URL expiry**: Stream URLs have tokens that expire. Download immediately after fetching.
- **Referer header**: Required for both API calls and video download. Without it, requests fail silently or return errors.
- **Frame count**: Too many frames = expensive vision calls. 15-25 frames is the sweet spot. Calculate: `duration_seconds / target_frames = interval`.
- **Batch size for parallel analysis**: When processing many frames with delegate_task, keep batch size ≤80 frames per subagent. 150 frames/batch caused 600s timeouts. 80 frames takes ~370-510s (safe margin).
- **AID/CID reliability**: Don't trust pre-fetched AID/CID values — always re-fetch from the view API in each subagent, as values can change or be incorrect. Have subagents call the view API themselves.
- **Full-video analysis**: For complete frame-by-frame analysis (1fps), use delegate_task with 3 concurrent subagents, each handling 80-frame batches. A 24-minute video (~1440 frames) = ~18 batches = ~6 rounds of 3 parallel subagents ≈ 30-40 minutes total.
- **Vision analysis cost**: Each frame costs a vision API call. For long videos, consider sampling only key timestamps.

## Example: Complete Pipeline (execute_code)

```python
from hermes_tools import terminal
import json, re

BV = "BV1vj9bBrEhZ"

# Step 1: Get metadata
meta_raw = terminal(f'''curl -s -m 20 \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://www.bilibili.com/" \
  "https://api.bilibili.com/x/web-interface/view?bvid={BV}"''')
meta = json.loads(meta_raw['output'])
d = meta['data']
aid, cid = d['aid'], d['cid']
print(f"Title: {d['title']}")
print(f"Duration: {d['duration']}s")

# Step 2: Get video URL
stream_raw = terminal(f'''curl -s -m 20 \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://www.bilibili.com/video/{BV}/" \
  "https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn=32&fnval=1&fourk=0"''')
stream = json.loads(stream_raw['output'])
video_url = stream['data']['durl'][0]['url']

# Step 3: Download
terminal(f'''curl -s -L -o /tmp/bili_video.mp4 \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://www.bilibili.com/" \
  "{video_url}"''')

# Step 4: Extract frames
interval = max(10, d['duration'] // 20)
terminal(f"mkdir -p /tmp/bili_frames && ffmpeg -y -i /tmp/bili_video.mp4 -vf 'fps=1/{interval}' -q:v 2 /tmp/bili_frames/frame_%03d.jpg")
```

Then use `vision_analyze` on selected frames.
