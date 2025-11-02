# 🎯 BerryPy + BerryCore Integration Summary

**TL;DR:** BerryPy is now a BerryCore port that manages apps from berrystore.sw7ft.com

---

## 🔑 Key Concepts

### 1. BerryPy = BerryCore Port

**What it means:**
- BerryPy itself installs via `qpkg install berrypy`
- Goes to: `$NATIVE_TOOLS/share/berrypy/`
- Launcher: `berrypy` command

### 2. BerryPy Manages Apps from BerryStore

**What it means:**
- BerryPy has a web interface at http://127.0.0.1:8001
- Downloads apps from http://berrystore.sw7ft.com
- Apps install to: `~/apps/` (web) and `~/usr/local/bin/` (CLI)

### 3. Two Separate Package Systems

```
┌─────────────────────────┐
│   BerryCore (qpkg)      │  → System packages
│   - Python              │     Location: $NATIVE_TOOLS/
│   - BerryPy itself      │     Command: qpkg
│   - nano, htop, etc.    │
└─────────────────────────┘

┌─────────────────────────┐
│   BerryPy Store         │  → User applications
│   - AI-Chat             │     Location: ~/apps/
│   - BB10Git             │     Command: Web interface
│   - copyclip, etc.      │
└─────────────────────────┘
```

---

## 📊 Complete Architecture

```
[BerryCore Repository]
       │
       ↓ qpkg install berrypy
       │
[BerryPy Port Package]
       │
       ↓ Extracts to $NATIVE_TOOLS/
       │
[BerryPy Application]
       │
       ↓ User runs: berrypy start
       │
[Web Interface: http://127.0.0.1:8001]
       │
       ↓ User clicks "Install" on an app
       │
[Downloads from berrystore.sw7ft.com]
       │
       ↓ Downloads APP.zip
       │
[Extracts to ~/apps/APP/]
       │
       ↓ User clicks "Start"
       │
[Runs: python3 ~/apps/APP/app.py]
       │
       ↓ App running on port XXXX
       │
[User clicks "Launch"]
       │
       ↓ Opens in browser
       │
[App Interface Running]
```

---

## 🛠️ Setup Requirements

### System PATH Configuration

Your `.profile` needs BOTH paths:

```bash
# 1. BerryCore environment (provides qpkg, berrypy command)
BERRYCORE_ENV="/accounts/1000/shared/misc/berrycore/env.sh"
if [ -e $BERRYCORE_ENV ];then
    . $BERRYCORE_ENV
fi

# 2. BerryPy-managed apps path (provides CLI apps installed via BerryPy)
export PATH="$HOME/usr/local/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/usr/local/lib:$LD_LIBRARY_PATH"
```

### Why Both?

- **Line 1-4:** Makes `berrypy` command available (BerryCore port)
- **Line 6-7:** Makes BerryPy-installed CLI apps available (BerryStore apps)

---

## 📦 Installation Flow

### Step 1: Install BerryCore (if not already)
```bash
curl -O https://raw.githubusercontent.com/sw7ft/berrycore/main/install.sh
chmod +x install.sh
./install.sh
```

### Step 2: Add BerryPy App Paths
```bash
echo 'export PATH="$HOME/usr/local/bin:$PATH"' >> ~/.profile
echo 'export LD_LIBRARY_PATH="$HOME/usr/local/lib:$LD_LIBRARY_PATH"' >> ~/.profile
source ~/.profile
```

### Step 3: Install Python (BerryCore Port)
```bash
qpkg install python
```

### Step 4: Install BerryPy (BerryCore Port)
```bash
qpkg install berrypy
```

### Step 5: Start BerryPy
```bash
berrypy start
```

### Step 6: Use Web Interface
```
Open browser → http://127.0.0.1:8001
Install apps from BerryStore
```

---

## 🎯 What Changed from Old Setup

### Old Way (old-setup.sh)
```bash
# Downloaded and installed everything manually
curl -O https://berrystore.sw7ft.com/python/...
curl -O https://berrystore.sw7ft.com/apps/taskapp.zip
./install.sh
# Modified .profile with hard-coded paths
# Installed to ~/apps/taskapp/
# Ran directly: python3 ~/apps/taskapp/taskapp.py &
```

### New Way (BerryCore Integration)
```bash
# Install system packages
qpkg install python
qpkg install berrypy

# Start with clean command
berrypy start

# Everything just works™
```

### Benefits of New Way
- ✅ Cleaner installation (one command)
- ✅ Standard locations following BerryCore conventions
- ✅ Easy updates (`qpkg update berrypy`)
- ✅ Clean removal (`qpkg remove berrypy`)
- ✅ Better process management
- ✅ Proper logging
- ✅ No hard-coded paths

---

## 🔄 Data Flow Examples

### Example 1: Installing BerryPy

```
User: qpkg install berrypy
  ↓
BerryCore: Downloads web-berrypy-2.0.zip
  ↓
BerryCore: Extracts to $NATIVE_TOOLS/
  ├─ bin/berrypy          (launcher command)
  ├─ share/berrypy/       (application files)
  └─ doc/                 (documentation)
  ↓
User: berrypy start
  ↓
BerryPy: Starts web server on port 8001
  ↓
User: Opens http://127.0.0.1:8001
  ↓
SUCCESS: BerryPy interface loaded
```

### Example 2: Installing an App via BerryPy

```
User: Clicks "AI-Chat" in Available Apps
  ↓
User: Clicks "Install"
  ↓
BerryPy: Fetches http://berrystore.sw7ft.com/apps/AI-Chat.zip
  ↓
BerryPy: Downloads 22KB file
  ↓
BerryPy: Extracts to ~/apps/AI-Chat/
  ├─ app.py
  ├─ templates/
  └─ static/
  ↓
User: Goes to "Manage Apps" tab
  ↓
User: Clicks "Start" on AI-Chat
  ↓
BerryPy: Runs python3 ~/apps/AI-Chat/app.py
  ↓
BerryPy: Detects port 8002 (from app.py)
  ↓
User: Clicks "Launch"
  ↓
Browser: Opens http://127.0.0.1:8002
  ↓
SUCCESS: AI-Chat running
```

---

## 📁 File Locations Reference

```
BlackBerry Device File System
│
├── /accounts/1000/shared/misc/              # BerryCore Root
│   │
│   ├── berrycore/
│   │   └── env.sh                          # BerryCore environment
│   │
│   ├── bin/                                 # BerryCore binaries
│   │   ├── qpkg                            # Package manager
│   │   ├── python3                         # Python (BerryCore port)
│   │   └── berrypy                         # BerryPy launcher (port)
│   │
│   └── share/
│       └── berrypy/                        # BerryPy application
│           ├── taskapp.py                  # Main server
│           ├── taskmgr.html                # Web interface
│           ├── app-icons/                  # Icons
│           ├── berrypy.log                 # Logs
│           └── berrypy.pid                 # Process ID
│
└── /accounts/1000/appdata/.../data/         # User Space
    │
    ├── apps/                                # BerryPy web apps
    │   ├── AI-Chat/
    │   │   ├── app.py
    │   │   └── templates/
    │   │
    │   ├── BB10Git/
    │   │   ├── app.py
    │   │   └── templates/
    │   │
    │   └── copyclip/
    │       ├── app.py
    │       └── static/
    │
    └── usr/local/
        ├── bin/                            # BerryPy CLI apps
        │   ├── htop
        │   ├── nano
        │   └── custom-script
        │
        └── lib/                            # BerryPy libraries
            ├── libfoo.so
            └── python3.11/
```

---

## 🌐 Network Endpoints

### BerryCore Repository
```
https://raw.githubusercontent.com/sw7ft/berrycore/main/
├── install.sh
├── ports/
│   ├── INDEX
│   └── web-berrypy-2.0.zip
```

### BerryPy Store
```
http://berrystore.sw7ft.com/
├── apps/                    # Web applications
│   ├── catalog.json
│   ├── AI-Chat.zip
│   ├── BB10Git.zip
│   └── app-icons/
│
├── bins/                    # CLI utilities
│   ├── catalog.json
│   └── *.zip
│
└── apks/                    # Android APKs
    └── *.apk
```

---

## 🔧 Commands Cheat Sheet

### BerryCore Commands
```bash
qpkg install python      # Install Python
qpkg install berrypy     # Install BerryPy
qpkg update berrypy      # Update BerryPy
qpkg remove berrypy      # Remove BerryPy
qpkg list               # List installed ports
```

### BerryPy Commands
```bash
berrypy start           # Start BerryPy server
berrypy stop            # Stop BerryPy server
berrypy restart         # Restart server
berrypy status          # Check if running
berrypy logs            # View logs
berrypy url             # Show URL
berrypy help            # Show help
```

### BerryPy App Management
```
Via web interface at http://127.0.0.1:8001
- Browse "Available Apps" tab
- Click app → Click "Install"
- Go to "Manage Apps" tab
- Click "Start" → Click "Launch"
```

---

## 📝 Complete Example Session

```bash
# === SETUP (One Time) ===

# 1. Install BerryCore (if not already)
curl -O https://raw.githubusercontent.com/sw7ft/berrycore/main/install.sh
chmod +x install.sh
./install.sh

# 2. Add BerryPy app paths to .profile
echo 'export PATH="$HOME/usr/local/bin:$PATH"' >> ~/.profile
echo 'export LD_LIBRARY_PATH="$HOME/usr/local/lib:$LD_LIBRARY_PATH"' >> ~/.profile
source ~/.profile

# 3. Install Python and BerryPy
qpkg install python
qpkg install berrypy

# === DAILY USE ===

# Start BerryPy
berrypy start

# Check status
berrypy status
# Output: Status: Running (PID: 12345)
#         URL: http://127.0.0.1:8001

# Open browser to http://127.0.0.1:8001

# Install apps via web interface
# (Click "Available Apps" → Select app → "Install")

# View logs if needed
berrypy logs

# Stop when done
berrypy stop
```

---

## ✅ Verification Checklist

After installation, verify everything works:

```bash
# 1. BerryCore is installed
which qpkg
# Should show: /accounts/1000/shared/misc/bin/qpkg

# 2. Python is available
which python3
python3 --version
# Should show: Python 3.11.x

# 3. BerryPy is installed
which berrypy
# Should show: /accounts/1000/shared/misc/bin/berrypy

# 4. Paths are configured
echo $PATH | grep berrycore
echo $PATH | grep usr/local/bin
# Both should show results

# 5. BerryPy starts
berrypy start
berrypy status
# Should show: Running

# 6. Web interface works
# Open browser to http://127.0.0.1:8001
# Should see purple BerryPy interface
```

---

## 🎓 Key Takeaways

1. **BerryPy is TWO things:**
   - A BerryCore port (the app manager itself)
   - A web-based store client (manages other apps)

2. **Two package systems coexist:**
   - BerryCore (`qpkg`) for system packages
   - BerryStore (web interface) for user apps

3. **Paths matter:**
   - `$NATIVE_TOOLS/bin` for BerryCore commands
   - `~/usr/local/bin` for BerryPy-managed CLI apps

4. **Apps come from different sources:**
   - BerryCore ports from GitHub
   - BerryStore apps from berrystore.sw7ft.com

5. **Both systems work together:**
   - BerryPy uses Python from BerryCore
   - BerryPy apps use Python from BerryCore
   - Clean separation, no conflicts

---

## 📚 Documentation Index

- **[README.md](README.md)** - Main documentation
- **[QUICK-START.md](QUICK-START.md)** - 5-minute setup guide
- **[INSTALL.md](INSTALL.md)** - Detailed installation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[BERRYCORE-INTEGRATION.md](BERRYCORE-INTEGRATION.md)** - Integration details
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[PORTING-GUIDE.md](PORTING-GUIDE.md)** - Creating ports

---

**Made with 💜 for BlackBerry users everywhere**


