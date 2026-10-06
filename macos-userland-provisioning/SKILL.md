---
source: self-generated
author: Hermes Agent
license: MIT
name: macos-userland-provisioning
description: "Install macOS apps and CLI tools without sudo/Homebrew."
version: 1.0.0
metadata:
  hermes:
    tags: [macos, install, cli-tools, checksum, provenance, no-sudo]
  prerequisites:
    commands: [curl, python3]
---

# macOS 免管理员权限安装工具链

适用：账号在 admin 组但**拿不到密码**（agent 不能代输密码）、机器上**没有 Homebrew**，却要装 .app 或 CLI 工具。

## When to Use

- 要在 macOS 上装桌面应用或 CLI 工具，但没有 sudo 密码、也没有 Homebrew。
- 安装流程里混着「需要管理员密码」和「不需要」的步骤，要把可自动化的部分全做完。
- 需要证明一个下载的二进制可信（官方校验文件 + provenance 比对）。

## 0. 先分类，不要因为缺密码就整体放弃

| 必须人工（管理员密码 / GUI） | 可全自动（用户级） |
|---|---|
| 桌面应用首启装特权助手（如 Docker Desktop 的 `DockerHelper.app`） | 下载、挂载 .dmg、`ditto` 拷贝 `.app` 到 `/Applications` |
| 系统扩展 / 网络权限授权（如 Tailscale） | 静态二进制放进 `~/.local/bin` |
| 开启「远程登录」、改系统设置 | `uv tool install` 装 Python 工具 |
| 写 `/usr/local/bin`（root:wheel，不可写） | 用户级 `launchd` agent、CLI 插件软链、socket |

做法：把任务切成「能自动的」和「需人工的」，自动的部分全跑完，只把最后一步交给用户，并在报告里显式列出**仍需用户手动**的清单。

## 1. 落点与 PATH

- 二进制统一放 `~/.local/bin`；用幂等写法加进 `~/.zshrc`（不要重复追加）：
  `case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) export PATH="$HOME/.local/bin:$PATH" ;; esac`
- `ls -ld /Applications` 为 `drwxrwxr-x root:admin` 时，admin 用户**免 sudo** 可往里拷 `.app`。
- agent 的 terminal 是非登录 shell：**拿不到 `~/.zshrc` 里的 PATH 与代理变量**，用绝对路径调用，别依赖 `command -v`。

## 2. 装 .app（.dmg，无 sudo）

```bash
curl -L --proxy http://127.0.0.1:7897 -o X.dmg "<URL>"   # 直连不通时走代理
hdiutil attach -nobrowse -readonly X.dmg                  # 记下挂载点
[ -e /Applications/X.app ] && echo "已存在，停止" || ditto "<挂载点>/X.app" /Applications/X.app
hdiutil detach "<挂载点>"
hdiutil info | grep -c "<卷名>"                            # 应为 0（无挂载残留）
```

装完必须自己验（**安装者的「成功」是自报**）：

```bash
defaults read /Applications/X.app/Contents/Info.plist CFBundleShortVersionString
codesign --verify --deep --strict --verbose=1 /Applications/X.app   # valid on disk + satisfies its Designated Requirement
spctl --assess --type execute -vv /Applications/X.app               # accepted / source=Notarized Developer ID
```

## 3. 装单文件 CLI（GitHub Releases）

流程：API 查 latest release → 挑 `darwin-arm64` 资产 → 下载包 **+ 官方校验文件** → 比对 → `install -m 755` 到 `~/.local/bin` → 打版本号。

**provenance 三连（缺一不可）**：
1. 官方校验文件里的行 == 下载包 sha256
2. 解压出的二进制 sha256 == 已安装文件 sha256
3. 能把版本号打出来

上游确实没有校验文件时：记录实际 sha256，并在报告里明确写「上游无校验文件」——不要假装校验过。
直接跑 `scripts/verify_download_provenance.sh --archive <包> --checksums <校验文件> [--extracted <解压文件> --installed <已装文件>]`。

## 4. Python 工具用 uv（不要动系统 python）

```bash
~/.local/bin/uv tool install <name>                       # shim 默认落在 ~/.local/bin
uv tool dir --bin                                          # shim 不在 ~/.local/bin 时先查再建软链
uv tool install --force pgcli --with "psycopg[binary]"     # 缺后端库时用 --with 补（pgcli 这类要 libpq/psycopg）
HTTPS_PROXY=http://127.0.0.1:7897 HTTP_PROXY=http://127.0.0.1:7897 UV_HTTP_TIMEOUT=120 uv tool install <name>
```

系统 python 可能是很旧的版本（如 3.9），不要把包装到宿主 python 环境。

## 5. 代理

- 直连 `github.com` / `docker.com` / registry 常不通：curl 用 `--proxy`，Python 生态用 `HTTPS_PROXY`/`HTTP_PROXY` 前缀。
- **Docker Desktop 有内建代理**：容器拉镜像不需要手工配代理（宿主机直连 registry 不通也不影响）。

## 6. 验证纪律

- 装完至少做一次**真实调用**，不只看版本号：能连库就真连一次、能加解密就真跑一轮加解密、能 lint 就在真实文件上跑一次。
- 判断命令成败要看**它自己的退出码**：管道（`cmd | grep ...`）之后的 `$?` 是管道最后一个命令的退出码，不是被检查命令的。用 `cmd; echo $?`，或把输出先存变量再判断。

## 7. 会浪费时间的环境陷阱

- **没有 `timeout` 命令**（coreutils 未装）：别写 `timeout 580 cmd`，靠调用工具自身的 timeout 参数。
- **随 app 打包的 CLI 会换代**：如 `ChatGPT.app/Contents/Resources/codex-cli/bin/codex`，app 更新后版本与路径都会变。建稳定软链 `~/.local/bin/<tool>` 指向 bundle 内的 wrapper，每次会话先探一次版本。
- **用户级 launchd 只在有人登录后才跑**：未开 FileVault/自动登录时，重启后用户服务不会自动起——「重启后自动恢复」这类承诺要写清前提。
- **改 Docker Desktop 资源设置会重置它的 VM 数据**（镜像、卷、容器一起清空）：改前先 `pg_dump`/备份。

## 8. 顺手写脚本时的 shell 陷阱（都踩过）

- `$var` 后**紧跟中文字符**时，bash 在 C locale 下会把多字节当变量名的一部分 → `unbound variable`。**一律写 `${var}`**。
- 双引号字符串里的**反引号会被当命令替换执行**（`echo "跑 \`diskutil\` 看看"` 会真的去跑）。去掉反引号，或改用单引号。
- 检查类脚本若 `source` 了带 `set -e` 的公共脚本，要在其后 `set +e`，否则「预期失败」的命令会中断整个脚本。
- 比对 `psql -Xt` 的标量输出前先 `tr -d '[:space:]'`（行首有空格导致比较永远不等）。
- 别用 python `multiprocessing` 直接 spawn 起负载做压测：子进程会重新 import 主模块，缺 `if __name__ == "__main__":` 时会把整个脚本再跑 N 遍。用 `subprocess.Popen(["sh","-c","while :; do :; done"])` 起负载、自己 `terminate()`。

## 9. 交付

- 把每一步的「命令 / 退出码 / 关键输出 / 校验结论」写进一个 report 文件，便于事后复查（尤其校验结论）。
- 报告末尾固定附：① 仍需用户手动的清单 ② 未能验证的项（如手机端渲染、需要 GUI 的授权步骤）。
