---
name: gameplay-video-wiki-analysis
description: "Analyze gameplay videos (e.g. Honor of Kings, League of Legends) by combining frame-by-frame visual analysis with a domain-specific wiki knowledge base. Synthesize findings into actionable improvement advice and file as a wiki query page."
version: 1.0.0
metadata:
  hermes:
    tags: [gaming, video-analysis, wiki, honor-of-kings, gameplay-review]
    category: media
  related_skills: [bilibili-video-analysis, llm-wiki]
---

# Gameplay Video + Wiki Analysis Pipeline

Analyze gameplay videos by extracting frames, analyzing visual content with vision AI, cross-referencing findings with a domain wiki knowledge base, and filing the results as a structured wiki query page.

## When This Skill Activates

- User shares a gameplay video (Bilibili, YouTube, etc.) and asks for improvement analysis
- User wants to combine visual analysis with existing wiki/knowledge base content
- User asks "analyze my gameplay" with reference to training materials

## Prerequisites

- `bilibili-video-analysis` skill (for B站 videos)
- `llm-wiki` skill (for wiki knowledge base access)
- `ffmpeg` installed
- Vision AI access (`vision_analyze`)

## Workflow

### Step 1: Extract Video Metadata

For Bilibili videos, use the API approach (not yt-dlp):

```python
BV = "BV_ID_FROM_URL"
meta_raw = terminal(f'''curl -s -m 20 \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -H "Referer: https://www.bilibili.com/" \
  "https://api.bilibili.com/x/web-interface/view?bvid={BV}"''')
```

Save metadata to `/tmp/bili_meta.json` for later use.

### Step 2: Download Video

```python
# Get stream URL
stream_raw = terminal(f'''curl -s -m 20 \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://www.bilibili.com/video/{BV}/" \
  "https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn=32&fnval=1&fourk=0"''')

# Download (must include Referer header)
terminal(f'''curl -s -L -o /tmp/bili_video.mp4 \
  -H "User-Agent: Mozilla/5.0" \
  -H "Referer: https://www.bilibili.com/video/{BV}/" \
  "{video_url}"''')
```

### Step 3: Extract Frames at 1fps

```bash
mkdir -p /tmp/bili_frames
ffmpeg -y -i /tmp/bili_video.mp4 -vf 'fps=1' -q:v 2 /tmp/bili_frames/frame_%04d.jpg
```

For a 10-min video this produces ~600 frames. For 15-min, ~900 frames.

### Step 4: Gather Wiki Knowledge

Before analyzing frames, gather relevant wiki content:

1. Search wiki for domain-specific terms (e.g., "打野", "jungle", "gank")
2. Read relevant concept pages from `~/wiki/concepts/`
3. Read any previous analysis queries in `~/wiki/queries/` for format reference
4. Compile key concepts into a summary file for subagent context

### Step 5: Parallel Batch Analysis

Split frames into batches of ≤80 frames each. Use `delegate_task` with 3 concurrent subagents.

**Batch calculation:**
```python
batch_size = 80
batches = []
for i in range(0, total_frames, batch_size):
    batches.append({
        'batch_num': len(batches) + 1,
        'start_frame': i + 1,
        'end_frame': min(i + batch_size, total_frames),
        'frames': frames[i:i+batch_size]
    })
```

**Subagent distribution:** Round-robin batches across 3 subagents.

**Each subagent's prompt should include:**
- Assigned batch range and frame numbers
- Wiki knowledge concepts (self-contained, no cross-batch context needed)
- Specific analysis requirements (game phases, key events, problems, highlights)
- Output format (structured markdown)
- Save path: `/tmp/batch_analysis_N.md`

**Subagent config:**
```python
{
    'toolsets': ['vision', 'file'],
    'goal': analysis_prompt,  # Include wiki concepts inline
    'context': f"Frame files in /tmp/bili_frames/. Batch info: {json.dumps(batch_info)}"
}
```

### Step 6: Synthesize Results

After all subagents complete:

1. Read all batch analysis files (`/tmp/batch_analysis_*.md`)
2. Read video metadata for context
3. Generate comprehensive report with:
   - Match data overview
   - Phase-by-phase analysis (early/mid/late game)
   - Problem checklist with wiki references
   - Highlights
   - Prioritized improvement list with wiki cross-references

### Step 7: File as Wiki Query Page

Save to `~/wiki/queries/` with proper frontmatter:

```yaml
---
title: [英雄]对局分析-YYYYMMDD
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: query
tags: [打野, 赵云, 对局分析, 王者荣耀]
sources: [B站视频 BV_ID, wiki打野知识库]
---
```

Also update:
- `index.md` — add entry under "## 查询" section, bump total page count
- `log.md` — append action log entry

## Timing Benchmarks

| Step | Duration | Notes |
|------|----------|-------|
| Metadata + Download | ~60s | 58MB video |
| Frame extraction | ~13s | 817 frames at 1fps |
| Wiki knowledge gathering | ~18s | 17 concept pages |
| Parallel batch analysis | ~5 min | 3 subagents × 320/320/177 frames |
| Synthesis + filing | ~3s | Generate report + update wiki |
| **Total** | **~7 min** | For a 14-min video |

## Pitfalls

- **Multi-game videos:** Some B站 videos contain multiple game replays stitched together. The analysis will cover all visible gameplay, not just one match. Note this in the report.
- **AID/CID reliability:** Always re-fetch AID/CID from the view API in each subagent if needed. Pre-calculated values can be wrong.
- **Frame numbering:** Use 4-digit padding (`frame_%04d.jpg`) to avoid lexicographic sorting issues.
- **Wiki domain mismatch:** Check that the wiki actually contains relevant domain content before assuming it does. Search first.
- **Batch size:** Keep ≤80 frames per subagent. 150 frames caused 600s timeouts in testing.
- **Subagent context:** Each subagent is isolated — include all necessary wiki concepts in its prompt, don't assume it can read the wiki.
