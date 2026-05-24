---
source: self-generated
name: ocr-and-documents
description: Extract text from PDFs and scanned documents. Use web_extract for remote URLs, pymupdf for local text-based PDFs, marker-pdf for OCR/scanned docs. For DOCX use python-docx, for PPTX see the powerpoint skill.
version: 2.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR]
    related_skills: [powerpoint]
---

# PDF & Document Extraction

For DOCX: use `python-docx` (parses actual document structure, far better than OCR).
For PPTX: see the `powerpoint` skill (uses `python-pptx` with full slide/notes support).
This skill covers **PDFs and scanned documents**.

## Step 1: Remote URL Available?

If the document has a URL, **always try `web_extract` first**:

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.

Only use local extraction when: the file is local, web_extract fails, or you need batch processing.

## Step 2: Choose Local Extractor

| Feature | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|-----------------|---------------------|
| **Text-based PDF** | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ✅ (90+ languages) |
| **Tables** | ✅ (basic) | ✅ (high accuracy) |
| **Equations / LaTeX** | ❌ | ✅ |
| **Code blocks** | ❌ | ✅ |
| **Forms** | ❌ | ✅ |
| **Headers/footers removal** | ❌ | ✅ |
| **Reading order detection** | ❌ | ✅ |
| **Images extraction** | ✅ (embedded) | ✅ (with context) |
| **Images → text (OCR)** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown output** | ✅ (via pymupdf4llm) | ✅ (native, higher quality) |
| **Install size** | ~25MB | ~3-5GB (PyTorch + models) |
| **Speed** | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) |

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout analysis.

If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for PyTorch and models. Your system has [X]GB free. Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf which works for text-based PDFs but not scanned documents or equations."

---

## pymupdf (lightweight)

```bash
pip install pymupdf pymupdf4llm
```

**Via helper script**:
```bash
python scripts/extract_pymupdf.py document.pdf              # Plain text
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # Tables
python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline**:
```bash
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

---

## marker-pdf (high-quality OCR)

```bash
# Check disk space first
python scripts/extract_marker.py --check

pip install marker-pdf
```

**Via helper script**:
```bash
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # JSON with metadata
python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI** (installed with marker-pdf):
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

---

## Arxiv Papers

```
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## Split, Merge & Search

pymupdf handles these natively — use `execute_code` or inline Python:

```python
# Split: extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
# Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
# Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.

---

## Detecting Scanned PDFs (IMPORTANT — do this first!)

Always check if a PDF has extractable text before choosing an extractor. Scanned PDFs return empty strings with pymupdf — don't waste time trying multiple pages:

```python
import pymupdf
doc = pymupdf.open('document.pdf')
# Check 3-5 scattered pages
for i in [0, 5, 10, min(20, doc.page_count-1)]:
    text = doc[i].get_text().strip()
    if text:
        print(f"Page {i}: {len(text)} chars — text-based PDF, use pymupdf")
        break
else:
    print("All pages empty — scanned PDF, needs OCR (marker-pdf)")
```

If all checked pages are empty → scanned PDF → go directly to marker-pdf. Don't try pymupdf4llm.

## marker-pdf First Run — Expect Long Download

**First run downloads ~2.7GB+ of models** (multiple safetensors files). Actual timing from real sessions:
- 1.35GB main model: ~12 min at ~2MB/s
- 1.34GB second model: can be much slower (~350kB/s = ~1 hour)
- Additional smaller models: text_recognition, layout detection, etc.

**Total first-run time: 15-60+ minutes** depending on connection speed.

**User management:** Always warn the user before starting marker-pdf for the first time:
> "需要下载OCR模型（约2.7GB），预计需要X分钟。是否继续？"

Consider running as background process with `notify_on_complete=true` so the user can do other work.

**After first run:** Models are cached at `~/.cache/huggingface/` and `~/.cache/datalab/models/`. Subsequent runs are fast (~1-14s/page on CPU).

## marker-pdf Memory Requirements & OOM Pitfall

**marker-pdf needs 4GB+ free RAM.** It loads PyTorch + multiple models simultaneously. Systems with ≤4GB total RAM will get OOM-killed (exit code 137).

**Symptoms of OOM:**
- Process exits with code 137 (SIGKILL)
- `dmesg | grep -i oom` shows "Out of memory: Kill process"
- Process runs for a while then silently dies

**Check before running:**
```bash
free -h  # Need 4GB+ available (not just total)
```

## Fallback: pymupdf + vision_analyze for Low-Memory OCR

When marker-pdf OOMs or the system has <4GB RAM, use this alternative approach:

```python
import pymupdf

doc = pymupdf.open('scanned.pdf')
# Extract pages as images
for i in range(doc.page_count):
    page = doc[i]
    pix = page.get_pixmap(dpi=150)  # 150dpi = good balance of quality/speed
    pix.save(f'/tmp/page_{i:04d}.jpg')
```

Then use `vision_analyze` on the extracted images:
```
vision_analyze(image_url="/tmp/page_0001.jpg", question="识别这张图片中的所有文字")
```

**For large PDFs (50+ pages):** Use `delegate_task` with parallel batches:
- Split pages into batches of ~40-50 images each
- Run 3 concurrent subagents with `toolsets: ["vision", "file"]`
- Each subagent analyzes its batch and saves to a file
- Parent reads all batch files and synthesizes

**Trade-offs vs marker-pdf:**
- ✅ No extra RAM needed (pymupdf is lightweight)
- ✅ No model downloads
- ✅ Works on any system
- ❌ Slower for large documents (one vision API call per page)
- ❌ Less accurate for complex layouts, tables, equations
- ❌ More expensive (vision API calls)

**Best for:** Books, articles, simple layouts where you need key pages rather than full-document OCR.

## DOCX Extraction (no dependencies fallback)

When `python-docx` is unavailable (externally-managed Python environments, no venv), parse DOCX directly using zipfile + XML:

```python
import zipfile
import xml.etree.ElementTree as ET

def get_docx_text(docx_path):
    """Extract text from .docx without python-docx dependency."""
    with zipfile.ZipFile(docx_path, 'r') as z:
        xml_content = z.read('word/document.xml')
    
    tree = ET.fromstring(xml_content)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    paragraphs = []
    for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        texts = []
        for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
            if t.text:
                texts.append(t.text)
        if texts:
            paragraphs.append(''.join(texts))
    return paragraphs
```

**DOCX is a ZIP file** containing `word/document.xml` with all text content. This approach works on any Python installation with no pip installs needed.

## Notes

- `web_extract` is always first choice for URLs
- pymupdf is the safe default — instant, no models, works everywhere
- marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when needed
- Both helper scripts accept `--help` for full usage
- On root systems: `pip install pymupdf marker-pdf --break-system-packages`
- For Word docs: use `python-docx` first, fall back to zipfile+XML if unavailable
- For PowerPoint: see the `powerpoint` skill (uses python-pptx)
