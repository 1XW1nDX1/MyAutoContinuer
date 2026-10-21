
# MyAutoContinuer

A simple Python tool that automatically sends messages to ChatGPT at a scheduled time.

一个基于 Python 的轻量级 ChatGPT 定时消息发送工具，通过模拟 Windows 鼠标与键盘操作，在指定时间自动向 ChatGPT 发送预设消息。

## ✨ 功能特性

- **定时发送**：在指定时间自动发送消息。
- **窗口识别**：根据窗口标题查找 ChatGPT 浏览器窗口。
- **自动切换焦点**：尝试将 ChatGPT 窗口切换至前台。
- **中文输入支持**：使用剪贴板实现中文消息输入。
- **异常处理**：窗口不存在或无法激活时取消发送。
- **防止误操作**：发送前检查当前前台窗口，降低误输入到其他应用的风险。
- **轻量简单**：无需 ChatGPT API Key，直接通过图形界面完成操作。

## 📋 环境要求

- Windows 10 / 11
- Python 3.10 或更高版本（推荐）
- 已安装并登录 ChatGPT 的浏览器
- 可正常访问 ChatGPT 的网络环境

> 本项目依赖 Windows API，暂不支持 macOS 和 Linux。

## 📦 安装

### 1. 克隆仓库

```bash
git clone https://github.com/<your-username>/MyAutoContinuer.git
cd MyAutoContinuer
```

将 `<your-username>` 替换为实际的 GitHub 用户名。

### 2. 创建虚拟环境

```powershell
python -m venv .venv
```

在 PowerShell 中激活虚拟环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. 安装依赖

```powershell
pip install -r requirements.txt
```

主要依赖包括：

| 依赖            | 用途                      |
| --------------- | ------------------------- |
| `pyautogui`   | 模拟鼠标点击和键盘输入    |
| `pyperclip`   | 通过剪贴板输入中文        |
| `pygetwindow` | 查找和管理窗口            |
| `pywin32`     | 调用 Windows API 激活窗口 |

## 🚀 使用方法

### 1. 配置参数

打开 `scripts/main.py`，修改以下配置：

```python
TARGET_TIME = "23:50:00"
MESSAGE = "继续"
WINDOW_TITLE = "ChatGPT"
```

参数说明：

| 参数             | 说明                    | 默认值示例   |
| ---------------- | ----------------------- | ------------ |
| `TARGET_TIME`  | 计划发送时间，24 小时制 | `23:50:00` |
| `MESSAGE`      | 要发送的消息            | `继续`     |
| `WINDOW_TITLE` | 目标窗口标题关键字      | `ChatGPT`  |

如果当天指定时间已经过去，程序会等待至第二天的对应时间。

### 2. 打开 ChatGPT

在浏览器中访问 [ChatGPT](https://chatgpt.com/)，登录账号并打开希望发送消息的对话。

确保浏览器窗口标题包含配置的 `WINDOW_TITLE` 关键字。

### 3. 运行程序

在项目根目录执行：

```powershell
python scripts/main.py
```

程序会显示计划执行时间，例如：

```text
计划执行时间：2026-10-22 23:50:00
```

到达指定时间后，程序尝试激活 ChatGPT 窗口，点击输入框并发送消息。

## ⚙️ 工作原理

```text
启动程序
   │
   ▼
读取配置
   │
   ▼
等待指定时间
   │
   ▼
查找 ChatGPT 窗口
   │
   ├── 未找到 ──→ 取消发送
   │
   ▼
尝试激活窗口
   │
   ├── 激活失败 ──→ 取消发送
   │
   ▼
验证前台窗口
   │
   ├── 验证失败 ──→ 取消发送
   │
   ▼
点击消息输入框
   │
   ▼
粘贴预设消息
   │
   ▼
模拟 Enter 发送
   │
   ▼
结束程序
```

本项目通过 Windows API 与 GUI 自动化实现消息发送，不使用 ChatGPT API，也不直接操作浏览器内部的网页元素。

## ⚠️ 注意事项

**1. 电脑必须保持运行**

如果 Windows 进入睡眠状态，程序将无法按预定时间执行。仅关闭显示器通常不影响程序运行，但锁屏和屏幕保护程序可能导致 GUI 自动化失败。

**2. 依赖浏览器窗口位置**

当前版本通过窗口相对坐标定位输入框：

```python
x = window.left + window.width // 2
y = window.top + window.height - 120
```

不同浏览器、窗口大小、缩放比例或 ChatGPT 页面布局可能导致点击位置不准确。

**3. 不保证消息一定成功发送**

程序可以验证目标窗口是否获得焦点，但无法确认 ChatGPT 输入框是否正确聚焦，也无法确认消息是否已经被服务器接收。

**4. 避免执行期间操作鼠标和键盘**

自动发送过程会临时控制鼠标和键盘。请避免同时操作其他应用，以减少误操作风险。

**5. 仅发送一次**

当前版本属于单次定时任务，执行后程序自动退出，不支持定时循环发送。

## 📁 项目结构

```text
MyAutoContinuer/
├── scripts/
│   └── main.py          # 主程序
├── .gitignore           # Git 忽略规则
├── README.md            # 项目说明
└── requirements.txt     # Python 依赖
```

## 🛠️ 常见问题

### 找不到 ChatGPT 窗口

确认 ChatGPT 页面已经打开，并检查浏览器窗口标题是否包含 `ChatGPT`。必要时修改 `WINDOW_TITLE`。

### 出现 PyGetWindowException

Windows 可能限制后台应用抢占前台焦点。项目使用 Win32 API 尝试激活窗口，但仍可能受到操作系统限制。

### 程序运行了，但没有发送消息

检查目标窗口是否被正确激活、输入框坐标是否正确，以及 ChatGPT 页面是否加载完成。

### 到指定时间没有执行

检查电脑是否进入睡眠状态，以及系统时间是否正确。该程序需要在后台持续运行至指定时间。

## 🔮 后续计划

- [ ] 支持自定义发送间隔与循环发送
- [ ] 支持倒计时模式
- [ ] 支持通过配置文件管理参数
- [ ] 改进输入框识别方式
- [ ] 添加发送结果验证与失败重试
- [ ] 支持最小化到系统托盘
- [ ] 增加图形化配置界面

## 📄 许可证

目前尚未指定开源许可证。如需允许其他人使用、修改和分发本项目，可考虑添加 [MIT License](https://choosealicense.com/licenses/mit/)。

---

**Disclaimer / 免责声明**

This project is an independent experimental automation tool and is not affiliated with or endorsed by OpenAI.

本项目是独立开发的实验性自动化工具，与 OpenAI 无官方关联。请合理使用，并遵守相关平台的使用条款。
