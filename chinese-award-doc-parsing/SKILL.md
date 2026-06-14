---
name: chinese-award-doc-parsing
description: Parse Chinese corporate award/recognition notification documents (.doc/.docx) to extract person names, awards, and units. Common in state-owned enterprises and telecom companies.
source: self-generated
tags: [documents, chinese, awards, parsing, corporate]
---

## When to Use
User has a folder of Chinese award notification documents (表彰通知) and wants to extract who won what awards. Common formats include "关于表彰XXX的通知" files.

## Prerequisites
```bash
pip install python-docx --break-system-packages
apt install -y catdoc
```

## Key Learnings

### File Format Handling
- **.docx files**: Use python-docx (`docx.Document`)
- **.doc files**: Use `catdoc` (NOT antiword - antiword fails on WPS Office generated .doc files)
- Check with `file` command if uncertain about format

### Document Structure Patterns
Chinese award documents typically follow this structure:
1. Title: "关于表彰XXX的通知"
2. Background/context paragraphs
3. Award categories (一、二、三...)
4. Team/unit awards
5. Individual awards with "分公司：姓名 姓名" format
6. Appendices with detailed lists

### Extraction Patterns

#### Pattern 1: Direct "分公司：姓名" format
```
温州分公司：董  姣  缪蓓蓓  林伟凡  华  盈  叶圣权
嘉兴分公司：吴晓倩  汪晓叶  赵  珉
省公司：张颖
```

#### Pattern 2: Inline mentions
```
通报表彰杭州分公司徐亚男等48人
```

#### Pattern 3: Parenthetical notes
```
舟山分公司：吴  玮（省公司下沉）
```

### Name Extraction Code
```python
import re

def extract_names_from_line(line):
    names = []
    if '：' in line or ':' in line:
        parts = re.split(r'[：:]', line, 1)
        if len(parts) == 2:
            unit_part = parts[0].strip()
            name_part = parts[1].strip()
            
            # Extract Chinese names (2-4 chars)
            name_pattern = r'[\u4e00-\u9fa5]{2,4}'
            found_names = re.findall(name_pattern, name_part)
            
            # Filter non-person words
            exclude_words = ['分公司', '公司', '团队', '优秀', '个人', '奖', 
                           '荣誉', '表彰', '推荐', '合作伙伴', '单位', '等', '人']
            for name in found_names:
                if name not in exclude_words and len(name) >= 2:
                    names.append((unit_part, name))
    return names
```

### Provincial Company (省公司) Filtering
To find provincial company employees:
```python
if '省公司' in unit_part:
    # This is a provincial company employee
```

Also check for:
- "省公司下沉" (provincial employee stationed at subsidiary)
- "省10000中心" (provincial call center)

## Step-by-Step Workflow

### Step 1: Install Dependencies
```bash
pip install python-docx --break-system-packages
apt install -y catdoc
```

### Step 2: Read All Files
```python
import os, subprocess, docx

def read_file(file_path):
    if file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return '\n'.join(para.text for para in doc.paragraphs if para.text.strip())
    else:  # .doc
        result = subprocess.run(['catdoc', file_path], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else ""
```

### Step 3: Extract Awards
Parse each file for:
1. Competition/竞赛名称 (from filename)
2. Award type/奖项 (from section headers)
3. Person names with units

### Step 4: Filter and Summarize
- Group by person name
- Filter for specific unit (e.g., 省公司)
- Summarize awards and honors

## Pitfalls

### antiword Failures
antiword may fail on WPS Office .doc files with "not a Word Document" error. Always use catdoc as fallback.

### False Positives
Common false positives in name extraction:
- "案例主创" (case creator)
- "鼓励条线" (encouragement line)
- "创新应用" (innovation application)
- "专项奖" (special award)

Solution: Add more exclude words or validate name length/structure.

### Encoding Issues
Some .doc files may have encoding issues. catdoc handles most cases but may show garbled text for some characters.

### Multiple Awards Per Person
One person may appear in multiple competitions. Use (name, competition) as unique key for deduplication.

## Output Format
```python
# Summary structure
{
    "name": "张颖",
    "award": "岗位创新能手奖，C2级荣誉",
    "competition": "集团云网双提升系列竞赛",
    "unit": "省公司",
    "reward": "5000元"
}
```

## Verification
After extraction, verify:
1. No duplicate names in same competition
2. All "省公司" entries are actual person names (not job titles)
3. Award types match document structure (C2/C3/D3荣誉)
