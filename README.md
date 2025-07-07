# Self-built-Python-Snipping-Tool-module
Self-built Python Snipping Tool module.
Welcome the big guy to correct, but also welcome the majority of users to use



## ✅ 用户需要完成的步骤如下：

### 1. **安装 Python**
- 前往官网：[https://www.python.org/downloads/](https://www.python.org/downloads/)
- 推荐安装最新稳定版（如 Python 3.10 或 3.11）
- 安装时**勾选 “Add to PATH”**

> 🧪 检查是否安装成功：
```powershell
python --version
pip --version
```

---

### 2. **安装依赖库**

在命令行中运行以下命令安装程序所需的所有库：

```powershell
pip install pyinstaller pyqt5 pillow keyboard pystray
```

---

### 3. **准备项目文件结构**

将两个文件放在同一个目录下，例如：

```
screenshot_tool/
├── jt_module.py
└── main.py
```

确保没有拼写错误、文件名不一致或缩进问题。

---

### 4. **使用 PyInstaller 打包成 EXE**

在命令行中进入该文件夹，执行打包命令：

```powershell
cd path\to\screenshot_tool
pyinstaller --noconfirm --onefile --windowed main.py
```

这会生成一个独立的 `.exe` 文件。

---

### 5. **获取最终的 EXE 文件**

打包完成后，在项目目录下会出现几个文件夹，`.exe` 文件位于：

```
dist/main.exe
```

用户可以直接双击运行这个文件。

---

## 📦 总结表格

| 步骤 | 内容 |
|------|------|
| 1    | 安装 Python 并配置环境变量 |
| 2    | 使用 pip 安装依赖库（PyInstaller、PyQt5 等） |
| 3    | 准备好 `jt_module.py` 和 `main.py` 文件 |
| 4    | 运行 PyInstaller 打包命令生成 `.exe` |
| 5    | 获取并运行 `dist/main.exe` 文件 |

---

### 📝 可以这样：

> 把这两个文件放到一个新文件夹里，然后打开命令提示符，依次运行下面这些命令：
>
> ```powershell
> pip install pyinstaller pyqt5 pillow keyboard pystray
> pyinstaller --noconfirm --onefile --windowed main.py
> ```
>
> 然后去 `dist` 文件夹里找 `main.exe`，双击就能用了！

---
