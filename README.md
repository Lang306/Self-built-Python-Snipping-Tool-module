# Self-built Python Snipping Tool Module
Welcome contributions from experts, and also welcome all users to use it.

## ✅ User Instructions:

### 1. **Install Python**
- Visit the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Recommended: Install the latest stable version (e.g., Python 3.10 or 3.11)
- During installation, **check "Add to PATH"**

> 🧪 Check if installation was successful:
```powershell
python --version
pip --version
```

---

### 2. **Install Required Libraries**

Run the following command in the terminal to install all necessary libraries:

```powershell
pip install pyinstaller pyqt5 pillow keyboard pystray
```

---

### 3. **Prepare Project File Structure**

Place both files in the same directory, for example:

```
screenshot_tool/
├── jt_module.py
└── main.py
```

Make sure there are no typos, filename mismatches, or indentation issues.

---

### 4. **Package into EXE with PyInstaller**

In the terminal, navigate to the folder and execute the packaging command:

```powershell
cd path\to\screenshot_tool
pyinstaller --noconfirm --onefile --windowed main.py
```

This will generate a standalone `.exe` file.

---

### 5. **Get the Final EXE File**

After packaging is complete, several folders will appear in the project directory. The `.exe` file is located at:

```
dist/main.exe
```

Users can double-click to run this file directly.

---

## 📦 Summary Table

| Step | Description |
|------|-------------|
| 1    | Install Python and configure environment variables |
| 2    | Use pip to install dependencies (PyInstaller, PyQt5, etc.) |
| 3    | Prepare `jt_module.py` and `main.py` files |
| 4    | Run PyInstaller command to generate `.exe` |
| 5    | Locate and run `dist/main.exe` |

---

### 📝 You can do like this:

> Put these two files into a new folder, then open the Command Prompt and run the following commands sequentially:
>
> ```powershell
> pip install pyinstaller pyqt5 pillow keyboard pystray
> pyinstaller --noconfirm --onefile --windowed main.py
> ```
>
> Then go to the `dist` folder to find `main.exe`, double-click and you're good to go!
