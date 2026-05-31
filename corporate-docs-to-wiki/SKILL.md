---
name: corporate-docs-to-wiki
description: Extract content from mixed corporate documents (PDF/DOCX/XLSX/PPTX) and generate a structured policy wiki for quick understanding of company policies, strategies, and trends.
source: self-generated
tags: [documents, wiki, policy, extraction, chinese, corporate]
---

## When to Use
User has a folder of corporate documents (PDFs, DOCX, XLSX, PPTX) and wants to understand the company's policies, strategies, and trends. Common for onboarding, compliance review, or strategic analysis.

## Step 1: Install Dependencies
```bash
pip install pymupdf pymupdf4llm python-docx openpyxl python-pptx --break-system-packages
```

## Step 2: Extract Content by File Type

### PDFs (pymupdf)
```python
import pymupdf
doc = pymupdf.open(pdf_file)
text = ""
for page in doc:
    text += page.get_text()
```
PITFALL: Some scanned PDFs return empty text. Check with:
```python
doc = pymupdf.open('file.pdf')
for i in [0, 5, 10]:
    if doc[i].get_text().strip():
        break  # text-based PDF
else:
    # scanned PDF, needs marker-pdf or vision_analyze
```

### DOCX (python-docx)
```python
from docx import Document
doc = Document(docx_file)
text = "\n".join(para.text for para in doc.paragraphs)
```

### XLSX (openpyxl)
```python
import openpyxl
wb = openpyxl.load_workbook(xlsx_file, data_only=True)
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    for row in sheet.iter_rows(values_only=True):
        # process row
```
NOTE: `data_only=True` reads computed values, not formulas.

### PPTX (python-pptx)
```python
from pptx import Presentation
prs = Presentation(pptx_file)
for i, slide in enumerate(prs.slides):
    for shape in slide.shapes:
        if hasattr(shape, "text"):
            # process text
```

## Step 3: Batch Extract All Files
```python
import os, json

contents = {}
for f in os.listdir('.'):
    if f.endswith('.pdf'):
        # extract PDF
    elif f.endswith('.docx'):
        # extract DOCX
    elif f.endswith('.xlsx'):
        # extract XLSX
    elif f.endswith('.pptx'):
        # extract PPTX

with open('contents.json', 'w', encoding='utf-8') as f:
    json.dump(contents, f, ensure_ascii=False, indent=2)
```

## Step 4: Analyze and Structure Wiki

### Common Chinese Corporate Policy Categories
1. **战略与工作主线** - Strategy, goals, work priorities
2. **AI+行动** - AI initiatives, products, applications
3. **市场经营** - Market operations, customer management
4. **政企业务** - Enterprise business, ICT, products
5. **人力资源与考核** - HR, performance evaluation
6. **党建与团建** - Party building, youth work
7. **安全与合规** - Security, compliance, regulations
8. **技术与基础设施** - Technology, infrastructure

### Wiki Structure Template
```markdown
# 公司政策Wiki

## 一、公司战略与工作主线
### 核心战略
### 年度主题
### 关键理念

## 二、AI+行动
### 战略定位
### 重点方向
### 产品体系

## 三、市场经营
### 经营体系
### 重点任务
### 考核指标

...

## 附录：文件索引
| 序号 | 文件主题 |
```

### Key Information to Extract
- **战略关键词**：云改数转智惠、3+2、453、4+1、一图清
- **考核指标**：收入目标、增长率、渗透率
- **时间节点**：启动时间、完成时限
- **责任部门**：牵头部门、配合部门
- **产品名称**：AI+产品、平台名称
- **术语定义**：专业术语、缩写解释

## Step 5: Save and Deliver
- Save wiki as markdown file
- Include file index appendix for traceability
- Note: Wiki is for learning/reference, official documents take precedence

## Pitfalls

### Scanned PDFs
pymupdf cannot extract text from scanned PDFs. Use marker-pdf (needs ~5GB) or vision_analyze as fallback.

### Large Document Sets
For 20+ documents, use `delegate_task` to parallelize extraction by file type.

### Chinese Encoding
Always use `encoding='utf-8'` when reading/writing JSON files with Chinese content.

### Formula Cells in XLSX
`data_only=True` returns None for formula cells if the file was never opened in Excel. Use `data_only=False` and evaluate formulas manually if needed.
