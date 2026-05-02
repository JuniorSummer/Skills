---
name: video-to-wiki-pipeline
description: "Batch-analyze multiple videos and generate an interlinked LLM Wiki. End-to-end pipeline: download → extract frames → parallel vision analysis → wiki pages with cross-references."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [video-analysis, wiki, parallel, batch-processing, vision]
    category: research
  related_skills: [bilibili-video-analysis, llm-wiki]
---

# Video-to-Wiki Pipeline

Batch-analyze multiple videos (e.g., tutorial series) and generate a structured, interlinked LLM Wiki. Designed for cases where a single video analysis is insufficient — multi-video knowledge compilation.

## When This Skill Activates

- User provides 2+ video URLs and wants a knowledge base/wiki
- User wants to analyze a video series comprehensively
- User wants cross-referenced teaching content from multiple sources

## Workflow

### 1. Setup Directory Structure

```bash
mkdir -p ~/project/{jungle,common}/frames_N  # organize by domain
```

### 2. Get Video Metadata (parallel)

Use `execute_code` to fetch metadata for all videos in one pass:
```python
for bv in bv_list:
    meta = terminal(f'curl -s ... "https://api.bilibili.com/x/web-interface/view?bvid={bv}"')
```

Save metadata to JSON for later reference.

### 3. Download Videos (parallel)

Use `delegate_task` with 3 concurrent subagents to download videos in parallel.
Each subagent: get stream URL → curl download → verify file size.
**Always re-fetch AID/CID from the view API** — don't trust pre-calculated values.

### 4. Extract Frames (parallel terminal calls)

Extract at 1fps for full coverage:
```bash
ffmpeg -y -i video.mp4 -vf "fps=1" -q:v 2 frames/frame_%04d.jpg
```

Can run 4 terminal calls in parallel (one per video).

### 5. Parallel Frame Analysis (critical step)

**Batch size: ≤80 frames per subagent** (150 caused 600s timeouts).

Pattern for each video:
```python
# 1440 frames / 80 = 18 batches, 3 concurrent = 6 rounds
delegate_task(tasks=[
    {"goal": "Analyze frames 1-80, save to batch_01.md", "toolsets": ["vision", "file"]},
    {"goal": "Analyze frames 81-160, save to batch_02.md", "toolsets": ["vision", "file"]},
    {"goal": "Analyze frames 161-240, save to batch_03.md", "toolsets": ["vision", "file"]},
])
# Repeat for next round...
```

Each subagent:
- Reads frames from the specified path
- Uses vision_analyze on each frame (or sampled frames for long videos)
- Focuses on: text overlays, teaching points, UI elements
- Saves structured summary to a batch .md file

**For videos >20 minutes**: Sample every 3-5 frames to reduce batch count.
**For videos <10 minutes**: Analyze every frame.

### 6. Synthesize into Wiki

After all batches complete, use `execute_code` to:

1. Read all batch summary files
2. Identify distinct concepts, entities, and themes across all videos
3. Create wiki pages using the llm-wiki skill's conventions:
   - YAML frontmatter (title, created, type, tags, sources, confidence)
   - Cross-references with `[[wikilinks]]` (minimum 2 per page)
   - Entity pages for videos, UP主s, series
   - Concept pages for teaching topics
4. Update index.md and log.md

### 7. Update SCHEMA.md

Add domain-specific tags to the wiki schema before creating pages.

## Pitfalls

- **Batch size >80 causes timeouts**: vision_analyze takes ~4-7s per frame. 80 frames ≈ 370-510s. 150 frames ≈ 700-1050s (exceeds 600s default timeout).
- **AID/CID changes**: Bilibili AID/CID values can differ between API calls. Always re-fetch in each subagent.
- **Frame numbering**: ffmpeg outputs frame_0001.jpg (4-digit padding). Ensure subagents use correct format.
- **Duplicate analysis**: If a subagent times out, check if it saved partial results before re-running. Use different output filenames for retries.
- **Memory limits**: Large batch files (>50KB) can cause issues. Keep batch summaries focused.
- **Wiki page sprawl**: Don't create a page for every minor topic. Follow the llm-wiki skill's Page Thresholds (2+ source mentions or central to one source).

## Example: 5-Video Tutorial Series

```
Input: 5 Bilibili URLs (~100 minutes total)
Frames: ~6000 at 1fps
Batches: ~75 at 80 frames each
Rounds: ~25 rounds of 3 parallel subagents
Time: ~60-90 minutes for full analysis
Output: ~24 wiki pages (18 concepts + 6 entities)
```

## Related Skills

- [[bilibili-video-analysis]] — Single video download and analysis
- [[llm-wiki]] — Wiki structure, conventions, and maintenance
