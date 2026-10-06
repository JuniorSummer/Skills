---
name: macos-local-dev-stack
description: "Use when installing tools on a mac without admin rights."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [macOS, Docker-Desktop, Tooling, Verification, No-Admin]
    related_skills: [delegating-to-coding-agents, hermes-agent]
---

# macOS 本机工具与栈（无管理员权限路径）

用于「只有普通用户、没有 Homebrew、不能输管理员密码」的机器上装工具、起服务栈。
每条都要求结果**可验证**：版本、哈希、签名、真实调用，而不是安装器的话。
本机工具装完后接着做服务栈的阶段化落地（骨架 → 数据层 → 应用层 → 入口运维）时，
每一步都要有可重复运行的验收脚本。

## When to Use

- 在一台没有 Homebrew、且不能（或不想）输管理员密码的 mac 上装命令行工具、或起服务栈。
- 用户要求安装结果**可验证**（版本 / 哈希 / 签名 / 真实调用），或要求把工具跑在真实文件上。
- 需要在这台机上用 Docker Desktop 承载容器化服务，并要求交付可重复运行的验收脚本。

## 先确认约束，能省掉整轮返工

- `/usr/local/bin` 属于 `root:wheel` → 普通用户**不可写**。用户级落点是 `~/.local/bin`
  （必要时 `mkdir -p`），并确认它在 `~/.zshrc` 的 PATH 里。追加 PATH 用幂等写法，
  改完用 `diff` 证明「只增不改」：
  `case ":$PATH:" in *":$dir:"*) ;; *) export PATH="$dir:$PATH" ;; esac`
- `sudo` 需要密码 → 凡是需要管理员的步骤（Homebrew 安装、开启远程登录、Docker Desktop
  特权助手、Tailscale 登录与证书）都只能交给用户；列成简短编号清单，其余全部自动化。
- 直连境外站点常不通：`curl --proxy http://127.0.0.1:7897`；Python 生态工具用
  `HTTPS_PROXY=… HTTP_PROXY=… uv tool install …` 前缀并设 `UV_HTTP_TIMEOUT=120`。
- **但镜像拉取不要想当然配代理**：Docker Desktop 自带 `http.docker.internal:3128`，
  宿主直连 registry 不通也能拉。先 `docker pull hello-world` 实测再下结论。
- 容器出网要单独验：`docker run --rm <img> sh -c 'nslookup <host>'`。注意
  `wget https://registry-1.docker.io/v2/` 返回 **401 是正常连通**（未认证应答），
  别据此判定「出网失败」——判断标准是能否解析 DNS 并拿到 HTTP 状态行。

## 装三类东西

1. **Python 工具**（pgcli / ruff / pre-commit…）：`uv tool install <name>`，shim 落在
   `~/.local/bin`；不要用系统 python 装包。**shim 是软链**，真身在
   `~/.local/share/uv/tools/<name>/` —— `readlink -f ~/.local/bin/<tool>` 才是
   「到底装了哪个二进制」的答案，删或换版本要动那个目录而不是删软链。
   **pgcli 特例**：单独装 pgcli 会因缺驱动启动失败，必须
   `uv tool install --force pgcli --with "psycopg[binary]"`。
2. **单文件静态二进制**（shellcheck / hadolint / age / gitleaks / rclone）：GitHub
   Releases 取 `<os>-<arch>` 资产，解压后 `install -m 755` 到 `~/.local/bin`。
3. **需要 GUI 或特权助手的应用**（Docker Desktop 等）：下载、挂载、拷进 `/Applications`
   可以全自动（admin 组可写），**首次启动的协议与管理員密码必须用户来**。

## 下载必须验，并验到「装的就是这个文件」

- 有官方校验文件（`*checksums*.txt`、`SHA256SUMS`）→ 下载它逐字节比对。
- 没有 → 记录实际 sha256 并**明确写「上游无校验文件」**，不要含糊带过；GitHub API 的
  资产 `digest=sha256:…` 可作第二参照。
- **闭环**：解压出的二进制 sha256 == 已安装文件的 sha256。少了这一步，「校验通过」
  只说明压缩包没坏。
- 应用类再叠一层：`codesign --verify --deep --strict` + `spctl --assess --type execute -vv`
  （看 `Notarized Developer ID`）+ `Info.plist` 版本号。
- **功能验证优先于版本验证**：装完加密工具就做一次真加密/解密往返；装完数据库客户端
  就用真实账号连真实库跑一条 SELECT。版本号能打印不代表能用。

## 服务栈阶段的验收习惯

- 每层交付一个**可重复运行的验收脚本**（逐项 PASS/FAIL + 汇总 + 非零退出码），
  改动后回归一次；一次性手工检查等于没检查。
- 容器不要只测「起来了」：断言端口**只绑 `127.0.0.1` 且不出现 `0.0.0.0`**、健康检查为
  healthy、扩展/表结构到位，并用最小权限账号验权限边界（只读账号写不了、追加型表改删被拒）。
- 结论写进文件并提交；聊天里只给「装了什么 / 版本 / 怎么验的 / 还剩什么」，不要粘贴日志。

## 专题细节

- Docker Desktop 的用户级接线、改设置的正确入口、以及「改资源会重置 VM 数据」这个大坑：
  见 `references/docker-desktop-macos.md`。
- bash 脚本与静态检查的反复踩坑（变量名吃中文、`psql -Xt` 前导空格、检查器要 `set +e`、
  `$?` 读在管道后、shellcheck 的 severity 参数）：见 `references/shell-script-pitfalls.md`。
