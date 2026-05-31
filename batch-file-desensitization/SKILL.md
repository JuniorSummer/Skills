---
name: batch-file-desensitization
description: Batch rename files to remove sensitive info — company names, person names, dates, document numbers. Typical for Chinese corporate document desensitization.
source: self-generated
tags: [files, rename, desensitization, chinese, batch]
---

## When to Use
User wants to rename files in bulk to remove company names, personal names, dates, or other identifiable information. Common for Chinese corporate documents with patterns like "浙江公司", "中国电信", person names followed by titles (总经理/书记/领导), year patterns (2026年/2026年度), document numbers (〔2026〕49号, 第9期).

## Approach: Multi-Pass Desensitization

### Pass 1: Remove Company Names
```
patterns: 浙江公司, 中国电信, 集团公司, 中电信浙, 北京公司, 前端公司, etc.
```

### Pass 2: Remove Person Names
Match pattern: `[\u4e00-\u9fa5]{2,4}(?=总经理|书记|领导|部长|主任)`
Known names to strip: 李云庄, 习近平, 习近平总书记

### Pass 3: Remove Years (with suffix handling)
```python
# Remove "2026年" AND "2026年度" (important: include 年度)
re.sub(r'20[0-9]{2}年度?', '', name)
```
PITFALL: Removing "2026年度" leaves orphan "度". Must clean up:
```python
name = re.sub(r'度$', '', name)  # trailing 度
name = re.sub(r'^度', '', name)  # leading 度
```

### Pass 4: Remove Document Numbers
```python
re.sub(r'第[0-9]+期', '', name)   # 第9期
re.sub(r'〔[0-9]+〕', '', name)   # 〔2026〕
re.sub(r'[0-9]+号', '', name)     # 49号, 78号
re.sub(r'附件[0-9]+[：:]', '', name)  # 附件1：
```

### Pass 5: Clean Punctuation & Whitespace
```python
re.sub(r'[\(\)（）]', '', name)    # brackets
re.sub(r'[""""]', '', name)       # Chinese quotes
re.sub(r'\+', '', name)           # plus signs
re.sub(r'\s+', ' ', name)         # collapse spaces
```

## Edge Cases

### Empty Filenames After Cleaning
If content becomes empty after desensitization (e.g., "中国电信〔2026〕49号" → nothing), assign a generic name like "文件".

### Chinese Quotes in Filenames
Filenames with `"..."` (中文引号) cause Python string escaping issues. Use `os.listdir('.')` to find the actual filename, then rename programmatically — don't hardcode the filename string.

### Residue Words
Watch for partial words left after removal:
- "度" from "年度" after year removal
- "级" from "公司级" after company removal
- "信息" from "公司信息" after company removal
- "信息" from "公司信息" after company removal

## Sequential Numbering Format
Prefix with `001_`, `002_`, etc. using `f"{i+1:03d}_{cleaned_name}"`.

## Verification
After renaming, scan all new filenames for leftover sensitive patterns to confirm complete desensitization.
