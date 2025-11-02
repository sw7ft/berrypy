# BerryPy Architecture

Understanding how BerryPy fits into the BerryCore ecosystem.

---

## 🏗️ System Architecture

BerryPy operates as a **bridge between two package systems**:

### 1. BerryCore Port System (BerryPy Installation)

**What:** BerryPy itself is installed as a BerryCore port  
**How:** `qpkg install berrypy`  
**Where:** `$NATIVE_TOOLS/share/berrypy/`

```bash
$NATIVE_TOOLS/
├── bin/
│   └── berrypy                    # Launcher command
└── share/
    └── berrypy/
        ├── taskapp.py             # Main application
        ├── taskmgr.html           # Web interface
        └── app-icons/             # Icons
```

### 2. BerryPy Store System (App Management)

**What:** BerryPy manages OTHER apps from berrystore.sw7ft.com  
**How:** Via web interface at http://127.0.0.1:8001  
**Where:** Apps install to `~/apps/` and `~/usr/local/bin/`

```bash
~/
├── apps/                          # Web apps managed by BerryPy
│   ├── AI-Chat/
│   ├── BB10Git/
│   ├── copyclip/
│   └── Telegram/
└── usr/local/bin/                 # CLI apps managed by BerryPy
    ├── htop
    ├── nano
    └── ...
```

---

## 🌐 Remote Store Structure

### BerryPy Store (berrystore.sw7ft.com)

**Base URLs:**
```python
CLI_APPS_URL = 'http://berrystore.sw7ft.com/bins/'
WEB_APPS_URL = 'http://berrystore.sw7ft.com/apps/'
APKS_URL = 'http://berrystore.sw7ft.com/apks/'
```

**Directory Structure:**
```
berrystore.sw7ft.com/
├── apps/                          # Web applications
│   ├── catalog.json               # Web app metadata
│   ├── AI-Chat.zip
│   ├── BB10Git.zip
│   ├── copyclip.zip
│   ├── Telegram.zip
│   └── app-icons/                 # Shared icons
│       ├── aichat.png
│       ├── github.png
│       └── ...
├── bins/                          # CLI utilities
│   ├── catalog.json               # CLI app metadata
│   ├── htop.zip
│   ├── nano.zip
│   └── ...
└── apks/                          # Android APKs
    ├── termux.apk
    └── ...
```

### Catalog System

Each category has a `catalog.json` file:

```json
{
  "apps": {
    "AI-Chat": {
      "name": "AI Chat Assistant",
      "description": "AI-powered chat assistant",
      "category": "Productivity",
      "version": "1.0",
      "author": "SW7FT",
      "icon": "aichat.png",
      "requirements": ["flask", "requests"]
    },
    "BB10Git": {
      "name": "BB10 Git Manager",
      "description": "GitHub repository manager",
      "category": "Development",
      "version": "2.1",
      "author": "SW7FT",
      "icon": "github.png",
      "requirements": ["flask", "requests", "beautifulsoup4"]
    }
  }
}
```

---

## 📦 Two Package Systems Compared

| Aspect | BerryCore Ports | BerryPy Store |
|--------|-----------------|---------------|
| **Purpose** | System packages | User applications |
| **Manager** | `qpkg` command | BerryPy web interface |
| **Source** | BerryCore repository | berrystore.sw7ft.com |
| **Install To** | `$NATIVE_TOOLS/` | `~/apps/` & `~/usr/local/bin/` |
| **Examples** | Python, nano, git | AI-Chat, BB10Git, copyclip |
| **Updates** | `qpkg update` | Via BerryPy interface |
| **Metadata** | ports/INDEX | catalog.json |

---

## 🔄 Data Flow

### Installing BerryPy (One-Time)

```
User runs:
  qpkg install berrypy
         ↓
BerryCore downloads:
  web-berrypy-2.0.zip from ports/
         ↓
Extracts to:
  $NATIVE_TOOLS/share/berrypy/
         ↓
User runs:
  berrypy start
         ↓
Web interface available:
  http://127.0.0.1:8001
```

### Installing Apps via BerryPy (Ongoing)

```
User clicks "Install" on AI-Chat
         ↓
BerryPy fetches:
  http://berrystore.sw7ft.com/apps/AI-Chat.zip
         ↓
Downloads & extracts to:
  ~/apps/AI-Chat/
         ↓
User clicks "Start"
         ↓
BerryPy runs:
  python3 ~/apps/AI-Chat/app.py
         ↓
App available at detected port
```

---

## 🛣️ PATH Configuration

For everything to work seamlessly, your PATH needs both systems:

### Required in .profile

```bash
# BerryCore Environment (provides $NATIVE_TOOLS/bin)
BERRYCORE_ENV="/accounts/1000/shared/misc/berrycore/env.sh"
if [ -e $BERRYCORE_ENV ];then
    . $BERRYCORE_ENV
fi

# BerryPy Managed Apps (provides ~/usr/local/bin)
export PATH="$HOME/usr/local/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/usr/local/lib:$LD_LIBRARY_PATH"
```

### Why Both Are Needed

1. **BerryCore PATH** (`$NATIVE_TOOLS/bin`)
   - Makes `berrypy` command available
   - Provides BerryCore-managed utilities

2. **BerryPy PATH** (`~/usr/local/bin`)
   - Makes BerryPy-installed CLI apps available
   - Independent from BerryCore

---

## 🔍 Example: Full Workflow

### 1. System Setup (One Time)

```bash
# Install BerryCore
curl -O https://raw.githubusercontent.com/sw7ft/berrycore/main/install.sh
chmod +x install.sh
./install.sh

# Add BerryPy managed apps PATH
echo 'export PATH="$HOME/usr/local/bin:$PATH"' >> ~/.profile
echo 'export LD_LIBRARY_PATH="$HOME/usr/local/lib:$LD_LIBRARY_PATH"' >> ~/.profile
source ~/.profile
```

### 2. Install Python via BerryCore

```bash
qpkg install python
which python3  # Should show: $NATIVE_TOOLS/bin/python3
```

### 3. Install BerryPy via BerryCore

```bash
qpkg install berrypy
which berrypy  # Should show: $NATIVE_TOOLS/bin/berrypy
```

### 4. Start BerryPy

```bash
berrypy start
# Access at http://127.0.0.1:8001
```

### 5. Install Apps via BerryPy Interface

```
Open browser → http://127.0.0.1:8001
  ↓
Go to "Available Apps" tab
  ↓
Click "AI-Chat" → Click "Install"
  ↓
App installs to: ~/apps/AI-Chat/
  ↓
Go to "Manage Apps" tab
  ↓
Click "Start" on AI-Chat
  ↓
App runs on port 8002 (example)
  ↓
Click "Launch" to open app
```

---

## 🔧 Integration Points

### 1. BerryPy Uses BerryCore Python

BerryPy's launcher script uses the system Python:

```bash
#!/bin/bash
# Uses python3 from PATH (BerryCore installation)
python3 $NATIVE_TOOLS/share/berrypy/taskapp.py
```

### 2. BerryPy-Managed Apps Use BerryCore Python

When BerryPy starts a web app:

```python
# In taskapp.py
process = subprocess.Popen(['python3', app_path], ...)
# Uses python3 from PATH (BerryCore installation)
```

### 3. Python Dependencies

Apps require Python packages:

```bash
# BerryCore Python includes pip
python3 -m pip install flask requests beautifulsoup4

# Apps installed by BerryPy can use these packages
```

---

## 🎯 Key Concepts

### Separation of Concerns

1. **BerryCore** manages:
   - System-level packages (Python, nano, etc.)
   - Location: `$NATIVE_TOOLS/`
   - Updates: `qpkg update`

2. **BerryPy** manages:
   - User applications (web apps, CLI tools)
   - Location: `~/apps/`, `~/usr/local/bin/`
   - Updates: Via web interface

### Why This Design?

✅ **Clean Separation**
- System packages don't mix with user apps
- BerryCore updates don't affect user apps
- User can reinstall apps without affecting system

✅ **Flexibility**
- BerryPy can work without BerryCore (legacy mode)
- BerryCore can exist without BerryPy
- Users can choose their preferred method

✅ **Compatibility**
- Existing BerryPy apps continue to work
- No migration needed for installed apps
- Old install locations preserved

---

## 🔒 Security Considerations

### BerryPy Access Control

- BerryPy listens on `127.0.0.1` (localhost only)
- Not accessible from network by default
- All downloads over HTTP (consider HTTPS upgrade)

### App Installation

- Apps downloaded as ZIP files
- Extracted to user's home directory
- No sudo/root required
- Apps run as user, not system

### Recommendations

1. **Only install trusted apps** from berrystore.sw7ft.com
2. **Review app code** before first run (it's Python!)
3. **Use network isolation** if running untrusted apps
4. **Keep Python updated** via `qpkg update python`

---

## 📊 Storage Locations Summary

```
BlackBerry Device
├── /accounts/1000/shared/misc/           # BerryCore
│   ├── berrycore/
│   │   └── env.sh
│   ├── bin/
│   │   ├── python3                       # BerryCore port
│   │   ├── berrypy                       # BerryCore port
│   │   └── qpkg                          # BerryCore manager
│   └── share/
│       └── berrypy/                      # BerryPy application
│           ├── taskapp.py
│           └── taskmgr.html
│
├── /accounts/1000/appdata/.../data/      # User space
│   ├── apps/                             # BerryPy web apps
│   │   ├── AI-Chat/
│   │   ├── BB10Git/
│   │   └── copyclip/
│   └── usr/local/
│       ├── bin/                          # BerryPy CLI apps
│       │   ├── htop
│       │   └── nano
│       └── lib/                          # BerryPy libraries
│           └── libfoo.so
│
└── /accounts/1000/appdata/.../data/.profile  # Environment
    ├── Sources BerryCore env.sh
    └── Adds ~/usr/local/bin to PATH
```

---

## 🚀 Future Architecture

### Potential Enhancements

1. **Unified Package System**
   - Single command for both systems
   - Example: `berrypy install AI-Chat` uses BerryPy store
   - Example: `berrypy install python` delegates to qpkg

2. **Local Port Mirror**
   - Cache berrystore.sw7ft.com locally
   - Faster installations
   - Offline mode

3. **Dependency Resolution**
   - BerryPy apps declare BerryCore dependencies
   - Auto-install via qpkg before app install
   - Example: `"requires": ["qpkg:python", "qpkg:openssl"]`

4. **Unified Updates**
   - Single command to update all packages
   - Both BerryCore and BerryPy apps
   - Update notifications in web interface

---

## ❓ FAQ

### Q: Should I use BerryCore ports or BerryPy store?

**A:** Use BerryCore for system packages (Python, libraries, system tools). Use BerryPy for applications (web apps, user utilities).

### Q: Can apps from BerryPy store become BerryCore ports?

**A:** Yes! Popular apps can be promoted to BerryCore ports. Follow the [PORTING-GUIDE.md](PORTING-GUIDE.md).

### Q: What if berrystore.sw7ft.com is down?

**A:** Already installed apps continue to work. New installations will fail until store is back online. Consider setting up a local mirror.

### Q: Can I create my own BerryPy store?

**A:** Yes! Edit `taskapp.py` and change:
```python
WEB_APPS_URL = 'http://your-server.com/apps/'
CLI_APPS_DIR = 'http://your-server.com/bins/'
```

### Q: Do BerryPy apps auto-update?

**A:** Not currently. You must manually reinstall to update. This is planned for v2.1.

---

**Made with 💜 for BlackBerry users everywhere**


