---
source: self-generated
name: cn-price-data-scraping
description: 爬取国内价格数据网站 - 国际油价(guojiyoujia.com)和台州造价网(tzzj.cn)
tags: [scraping, curl, china, price-data, construction]
---

# 国内价格数据网站爬取

## 1. 国际油价网 (gujiyoujia.com)

**特点**：免费公开API，无需登录

### 数据源
直接访问JSONP数据接口，无需渲染页面：
```
curl -s -L -A "Mozilla/5.0" "https://www.guojiyoujia.com/data/oil.js"
```

### 数据格式
返回JavaScript变量，格式：
```javascript
var hq_str_hf_GAS="1104.148,,1104.500,1105.250,1114.250,1097.250,14:16:59,1153.250,1111.000,0,3,5,2026-05-22,柴油,3514";
```

### 字段索引（逗号分隔）
- [0] 当前价格
- [4] 今日最高
- [5] 今日最低
- [6] 时间 (HH:MM:SS)
- [7] 昨日收盘
- [8] 今日开盘
- [12] 日期
- [13] 名称

### 可用数据代码
| 代码 | 名称 |
|------|------|
| hf_GAS | ICE国际柴油 |
| hf_CL | 纽约原油(WTI) |
| hf_OIL | 布伦特原油 |
| hf_DBI | ICE布伦特原油 |
| hf_EUA | 欧盟碳排放 |
| hf_NG | 天然气 |

### 计算公式
```
涨跌额 = 当前价 - 昨收
涨跌幅 = 涨跌额 / 昨收 * 100
```

---

## 2. 台州造价网 (tzzj.cn)

**特点**：需要登录，有验证码，数据API隐藏在JS中

### 登录流程
```bash
# 1. 获取cookie（访问商情价页面）
curl -s -L -c cookies.txt -A "Mozilla/5.0" "https://www.tzzj.cn/tzperiodical/vipBusController.do?toBusiness"

# 2. 获取验证码图片（GET请求，不是POST）
curl -s -L -b cookies.txt -c cookies.txt -A "Mozilla/5.0" "https://www.tzzj.cn/tzperiodical/sysuserController.do?generalCode" -o vcode.jpg

# 3. 识别验证码（用vision_analyze工具）
# 4. 提交登录（密码中的特殊字符需URL编码，如 # → %23）
curl -s -D login_headers.txt -b cookies.txt -c cookies.txt -A "Mozilla/5.0" -X POST \
  -d "userCellphone=手机号&userPassword=密码&randCode=验证码" \
  "https://www.tzzj.cn/tzperiodical/vipLoginController.do?doLogin"

# 5. 验证登录结果：
#    - 成功：返回 HTTP 302 重定向到 index 页面
#    - 失败：返回 HTTP 200，响应体中 <input type="hidden" id="msg" value="验证码错误"/>
#    - 确认登录：访问 index 页面，检查 curUserName 是否有值
curl -s -L -b cookies.txt -c cookies.txt -A "Mozilla/5.0" "https://www.tzzj.cn/tzperiodical/vipLoginController.do?index" | grep "curUserName"
```

### 数据API
```
POST /tzperiodical/vipBusController.do?getList
```

### 请求参数
| 参数 | 说明 | 示例 |
|------|------|------|
| smCategory | 分类ID | 见下表 |
| smBrand | 品牌筛选 | 留空=全部 |
| keyWord | 关键词 | URL编码两次 |
| year | 年份 | 2026 |
| month | 期号（两位数月份） | 04 |
| entName | 供应商名 | URL编码两次 |
| page | 页码 | 1 |
| limit | 每页条数 | 200（建议大值避免分页） |

### 分类ID (smCategory)
| 分类 | ID |
|------|------|
| 水泥 | `100af350-8f19-41bc-8c4c-b11c16d5187d.cc422c7a-30cd-4178-afca-1810ad313241` |
| 钢筋 | `e8d3b7a3-53a0-4e2a-af64-140f52e38d2d.a0114133-f17d-4bbc-8822-8ceb62874eb7` |
| 混凝土 | `2fbcd6a6-c3ac-4e9e-9b2c-4e2f6e3e970c.bab4aa1c-aa70-432b-8f7d-f7c0273b78fc` |

### 响应格式
```json
{
  "msg": "",
  "total": 57,
  "code": 0,
  "data": [
    {
      "sm_name": "洋房牌水泥",
      "sm_kinds": "42.5级散装",
      "sm_brand": "洋房",
      "sm_unit": "t",
      "mp_price": "435",
      "mp_remarks": "厂家报价(台州市区)",
      "md_entname": "浙江亚东经贸有限公司",
      "offerdate": "2026-4-01"
    }
  ]
}
```

### 登录判断要点
- 登录成功：HTTP 302 重定向，Location 指向 index 页面
- 验证码错误：HTTP 200，响应HTML中含 `value="验证码错误"` 的隐藏input
- 确认已登录：访问 index 页面后 `curUserName = '用户名'` 有值
- 未登录时：`curUserName = ''` 为空

### 备注字段过滤
`mp_remarks` 字段括号格式不统一，存在半角和全角两种：
- `厂家报价(台州市区)` - 半角括号
- `厂家报价（台州市区）` - 全角括号

筛选时用 `contains` 而非精确匹配：
```python
filtered = [item for item in data if '台州市区' in item.get('mp_remarks', '')]
```

### 注意事项
- 验证码识别不稳定，可能需要重试（成功率约70-80%）
- 数据按月发布，当月可能无数据，需查询上月
- 密码中的特殊字符需URL编码（如 `#` → `%23`）
- Cookie有效期有限，定时任务需每次重新登录

### 已配置定时任务

| 数据源 | 任务ID | 频率 | 时间 |
|--------|--------|------|------|
| ICE柴油 | `30eed0ad30f2` | 每天 | 09:00 |
| 台州水泥 | `9d3a9ce76b7c` | 每24小时 | ~15:56 |

### 全自动登录方案（已验证可行）

定时任务 prompt 中通过以下流程实现全自动：
1. 访问商情价页面获取 cookie（`/vipBusController.do?toBusiness`）
2. 获取验证码图片（GET `/sysuserController.do?generalCode`）保存到 /tmp/vcode.jpg
3. 用 `vision_analyze` 工具识别验证码文字
4. 提交登录（POST `/vipLoginController.do?doLogin`，参数：userCellphone、userPassword、randCode）
5. 检查响应头：302=成功，200=验证码错误需重试
6. 成功后调用数据API并格式化输出

**注意**：vision_analyze 必须在 prompt 中以自然语言指令调用，不能写在 script 中（工具调用只有AI能执行）。

---

## Pitfalls
1. **浏览器超时**：这两个网站用浏览器访问经常超时，优先用curl
- **验证码**：tzzj.cn验证码用AI识别准确率约70%，失败需重试。vision_analyze 常读出6个字符（实际可能5个），但登录仍可能成功，不必纠结精确匹配，直接尝试即可
3. **月份格式**：tzzj.cn月份需两位数（04不是4），参数名为 `month`
4. **URL编码**：中文关键词需编码两次（encodeURIComponent两次）
5. **括号格式**：mp_remarks字段半角/全角括号混用，过滤时用contains
6. **vision工具限制**：定时任务中vision_analyze需在prompt中调用，不能写在script里
7. **登录检测**：不要依赖 `-L` 跟随重定向来判断登录结果，用 `-D` 保存响应头检查状态码（302=成功，200=失败），失败时响应体含"验证码错误"
- **密码编码**：密码中 `#` 必须编码为 `%23`，其他特殊字符同理。也可用 `--data-urlencode` 让 curl 自动处理编码
