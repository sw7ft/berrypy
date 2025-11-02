# BerryPy Quick Start Guide

Get up and running with BerryPy in 5 minutes.

---

## 📋 Prerequisites

- BlackBerry BB10/QNX device
- BerryCore v0.7+ installed
- Terminal access (Term49 or SSH)

---

## ⚡ 5-Minute Setup

### 1. Install Python
```bash
qpkg install python
```

### 2. Ensure BerryPy-Managed App Paths
```bash
# Add to .profile if not already there
echo 'export PATH="$HOME/usr/local/bin:$PATH"' >> ~/.profile
echo 'export LD_LIBRARY_PATH="$HOME/usr/local/lib:$LD_LIBRARY_PATH"' >> ~/.profile
source ~/.profile
```

### 3. Install BerryPy
```bash
qpkg install berrypy
```

### 4. Start BerryPy
```bash
berrypy start
```

### 5. Access Web Interface
Open BlackBerry browser to:
```
http://127.0.0.1:8001
```

**Done!** 🎉

---

## 🎯 Understanding the System

### Two Package Systems

**BerryCore Ports** (System Packages)
- Install: `qpkg install <package>`
- Location: `$NATIVE_TOOLS/`
- Examples: Python, nano, git

**BerryPy Store** (User Apps)
- Install: Via web interface at http://127.0.0.1:8001
- Location: `~/apps/` (web) and `~/usr/local/bin/` (CLI)
- Examples: AI-Chat, BB10Git, copyclip

### Download Sources

BerryPy downloads apps from:
- **Web apps:** http://berrystore.sw7ft.com/apps/
- **CLI apps:** http://berrystore.sw7ft.com/bins/
- **APKs:** http://berrystore.sw7ft.com/apks/

---

## 📱 First Steps After Install

### 1. Browse Available Apps
- Click "Available Apps" tab
- Browse web apps and CLI utilities
- Click any app for details

### 2. Install Your First App
Try installing **copyclip** (clipboard manager):
1. Find "copyclip" in Available Apps
2. Click to view details
3. Click "Install"
4. Wait for installation
5. Go to "Manage Apps" tab
6. Click "Start" on copyclip
7. Access via "Launch" button

### 3. Configure Auto-Start (Optional)
1. Click ☰ menu (top right)
2. Select "Device Config"
3. Choose "Auto-Start Apps" tab
4. Enable auto-start for desired apps

### 4. Add to Home Screen
In BlackBerry browser:
1. Tap menu button
2. Select "Add to Home Screen"
3. Name it "BerryPy"
4. Done! Quick access from home screen

---

## 🔧 Common Commands

```bash
# Start BerryPy
berrypy start

# Check status
berrypy status

# View logs
berrypy logs

# Stop BerryPy
berrypy stop

# Restart BerryPy
berrypy restart

# Show URL
berrypy url

# Get help
berrypy help
```

---

## 🌐 Web Interface Guide

### Main Sections

**1. Manage Apps**
- Shows all installed web apps
- Start/Stop apps
- Launch apps in browser
- View app ports

**2. Installed Apps**
- List all installed apps (web + CLI)
- Multi-select and delete
- Filter by type (All/Web/CLI)

**3. Available Apps**
- Browse apps from BerryPy store
- Search apps
- View descriptions
- One-click install

**4. Device Settings (☰ menu)**
- Auto-start configuration
- Android APK downloads
- System information

---

## 🔍 Where Things Are

### BerryPy Installation (BerryCore Port)
```
$NATIVE_TOOLS/
├── bin/berrypy                    # Command
└── share/berrypy/                 # Application files
    ├── taskapp.py
    ├── taskmgr.html
    └── app-icons/
```

### BerryPy-Managed Apps
```
~/
├── apps/                          # Web apps
│   ├── AI-Chat/
│   ├── BB10Git/
│   └── copyclip/
└── usr/local/bin/                 # CLI apps
    ├── htop
    └── nano
```

### Logs and Runtime
```
$NATIVE_TOOLS/share/berrypy/
├── berrypy.log                    # Application logs
└── berrypy.pid                    # Process ID
```

---

## 📊 Recommended Apps

### Productivity
- **copyclip** - Clipboard manager
- **AI-Chat** - AI assistant

### Development
- **BB10Git** - GitHub manager
- **Webshell** - Web terminal
- **Term49-Settings** - Terminal config

### Communication
- **Telegram** - Messaging
- **RocketChat** - Chat platform

### Media
- **YouTube** - Video player

---

## 🔄 Auto-Start Setup

To start BerryPy automatically on boot:

```bash
nano ~/.profile
```

Add at the end:
```bash
# BerryPy Auto-Start
berrypy start >/dev/null 2>&1 &
```

Save and exit (Ctrl+O, Enter, Ctrl+X).

---

## ⚠️ Troubleshooting

### BerryPy won't start
```bash
berrypy logs          # Check for errors
berrypy stop          # Stop any hanging process
berrypy start         # Try again
```

### Can't access web interface
```bash
berrypy status        # Verify it's running
berrypy url           # Get the URL
# Try: http://127.0.0.1:8001
```

### Apps won't install
```bash
# Check internet connection
ping berrystore.sw7ft.com

# Check Python
python3 --version

# Check paths
echo $PATH | grep berrycore
echo $PATH | grep usr/local/bin
```

### Command not found: berrypy
```bash
# Source BerryCore environment
source /accounts/1000/shared/misc/berrycore/env.sh

# Verify installation
ls $NATIVE_TOOLS/bin/berrypy
```

---

## 📚 Next Steps

- **[README.md](README.md)** - Full documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design
- **[BERRYCORE-INTEGRATION.md](BERRYCORE-INTEGRATION.md)** - Integration guide
- **[INSTALL.md](INSTALL.md)** - Detailed installation

---

## 💡 Pro Tips

1. **Bookmark the Interface**
   - Add http://127.0.0.1:8001 to home screen
   - Quick access from launcher

2. **Use Search**
   - Available Apps tab has search
   - Find apps quickly

3. **Check Logs**
   - `berrypy logs` shows what's happening
   - Useful for debugging

4. **Multiple Apps**
   - Each app runs on different port
   - Check port in Manage Apps tab

5. **Keep Updated**
   - `qpkg update` updates BerryPy itself
   - Reinstall apps via web interface for app updates

---

## 🤝 Need Help?

- **GitHub Issues:** https://github.com/sw7ft/BerryCore/issues
- **Store:** https://berrystore.sw7ft.com
- **Logs:** `berrypy logs`

---

**Made with 💜 for BlackBerry users everywhere**


