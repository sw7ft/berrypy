# 🫐 BerryPy - BlackBerry App Platform

**Full-featured application manager for BlackBerry BB10/QNX devices**

[![Version](https://img.shields.io/badge/version-2.0-purple)](https://github.com/sw7ft/BerryPy)
[![Platform](https://img.shields.io/badge/platform-BB10%2FQNX-black)](https://github.com/sw7ft/BerryPy)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## 📱 Overview

BerryPy is a sophisticated, full-featured application manager specifically designed for BlackBerry devices running BB10/QNX systems. It provides a beautiful web-based interface to manage, install, and monitor all your Python web applications from one unified platform.

### Key Features

✨ **Modern UI** - Dark purple theme optimized for BlackBerry displays  
📦 **App Management** - Install, start, stop, and monitor applications  
🔄 **Auto-Start Config** - Configure apps to launch on boot  
🎨 **Custom Icons** - Beautiful 48x48px icons for all apps  
⚡ **Smart Detection** - Automatic port and process detection  
🔍 **Search & Filter** - Find apps quickly with real-time search  
📊 **Process Tracking** - Monitor running apps with PID management  
🌐 **App Store** - Browse and install from BerryPy store  

---

## 🚀 Installation

### Option 1: BerryCore Port (Recommended)

If you have [BerryCore](https://github.com/sw7ft/BerryCore) installed:

```bash
# Install BerryPy
qpkg install berrypy

# Start BerryPy
berrypy start

# Open browser to: http://127.0.0.1:8001
```

**Requirements:**
- BerryCore v0.7 or later
- Python 3.11+ (install via: `qpkg install python`)

### Option 2: Standalone Installation (Legacy)

```bash
# Download and run setup script
curl -O https://berrystore.sw7ft.com/setup.sh
chmod +x setup.sh
./setup.sh
```

---

## 📖 Usage

### Starting BerryPy

```bash
# Using BerryCore
berrypy start

# Direct Python (legacy)
cd ~/apps/taskapp
python3 taskapp.py &
```

### Accessing the Interface

Open your BlackBerry browser and navigate to:
```
http://127.0.0.1:8001
```

💡 **Tip:** Add this to your home screen for quick access!

### Managing BerryPy

```bash
berrypy status    # Check if running
berrypy stop      # Stop the server
berrypy restart   # Restart the server
berrypy logs      # View recent logs
berrypy help      # Show help
```

---

## 🎯 Features in Detail

### 1. Manage Apps Section
- View all installed web applications
- Start/Stop apps with toggle buttons
- Launch apps in new browser tabs
- Real-time status indicators
- Port information display

### 2. Installed Apps Section
- List all installed apps (CLI + Web)
- Multi-select with checkboxes
- Bulk delete functionality
- Category filtering (All/Web/CLI)

### 3. Available Apps Section
- Browse apps from BerryPy store
- Click for detailed descriptions
- Install with one click
- Search functionality
- Custom icons with fallbacks

### 4. Device Settings
- Auto-start configuration
- Android APK downloads
- System information

---

## 🏗️ Building the Port

### Prerequisites
- BerryCore v0.7 or later
- `taskapp.zip` file

### Build Command
```bash
chmod +x build-port.sh
./build-port.sh
```

This creates: `web-berrypy-2.0.zip`

### Port Structure
```
web-berrypy-2.0.zip
├── bin/
│   └── berrypy              # Launcher script
├── share/
│   └── berrypy/
│       ├── taskapp.py       # Main application
│       ├── taskmgr.html     # Web interface
│       ├── app-icons/       # App icons (8 PNG files)
│       └── ...              # Other files
└── doc/
    ├── README.md            # Documentation
    ├── overview.md          # Detailed overview
    └── ICON_UPDATES.md      # Icon documentation
```

---

## 📦 Port Package Details

### INDEX Entry
```
berrypy|web|2.0|112K|BlackBerry App Platform - Full-featured application manager
```

### Installation in BerryCore
```bash
# Copy to BerryCore ports directory
cp web-berrypy-2.0.zip /path/to/BerryCore/ports/

# Update INDEX
echo "berrypy|web|2.0|112K|BlackBerry App Platform - Full-featured application manager" >> /path/to/BerryCore/ports/INDEX

# Install
qpkg install berrypy
```

---

## 🔧 Configuration

### Auto-Start on Boot

Add to your `~/.profile`:
```bash
# BerryPy Auto-Start
if command -v berrypy >/dev/null 2>&1; then
    berrypy start >/dev/null 2>&1 &
fi
```

### Custom Port

Edit `taskapp.py` and change:
```python
PORT = 8001  # Change to your preferred port
```

---

## 🎨 Supported Apps

BerryPy comes with custom icons for:
- **AI-Chat** - AI assistant with purple theme
- **BB10Git** - GitHub repository manager
- **copyclip** - Clipboard utility
- **RocketChat** - Chat application
- **Telegram** - Messaging app
- **Term49-Settings** - Terminal configuration
- **Webshell** - Web-based terminal
- **YouTube** - Video player

All icons are 48x48px PNG optimized for BlackBerry displays.

---

## 🔍 Technical Details

### Architecture
- **Backend:** Python 3.11+ with Flask
- **Frontend:** Vanilla JavaScript (ES5-compatible)
- **UI Framework:** Custom CSS with dark purple theme
- **Process Detection:** QNX `pidin` command
- **Port Detection:** Smart regex + netstat scanning

### Performance
- **RAM Usage:** ~10-20MB
- **Startup Time:** ~2 seconds
- **Cache Duration:** 5 minutes (network requests)
- **Request Timeout:** 10 seconds

### Browser Compatibility
- ✅ BlackBerry 10 Browser (WebKit-based)
- ✅ BlackBerry Passport (1440x1440)
- ✅ All BB10 devices

---

## 📁 File Structure

```
BerryPy/
├── taskapp.zip              # Original application package
├── build-port.sh            # BerryCore port builder
├── web-berrypy-2.0.zip      # Built port package
├── INDEX-entry.txt          # INDEX entry for BerryCore
├── BERRYCORE-INTEGRATION.md # Integration guide
├── overview.md              # Detailed documentation
├── ICON_UPDATES.md          # Icon system documentation
├── PORTING-GUIDE.md         # BerryCore porting guide
└── old-setup.sh             # Legacy installation script
```

---

## 🆚 BerryCore vs Legacy Installation

| Feature | Legacy Setup | BerryCore Port |
|---------|--------------|----------------|
| **Installation** | Manual curl + bash | `qpkg install berrypy` |
| **Updates** | Re-download entire setup | `qpkg update berrypy` |
| **Removal** | Manual rm -rf | `qpkg remove berrypy` |
| **Dependencies** | Manual pip install | Automatic via qpkg |
| **Path Setup** | Manual .profile edit | Automatic via BerryCore |
| **Location** | `~/apps/taskapp/` | `$NATIVE_TOOLS/share/berrypy/` |
| **Launcher** | `python3 taskapp.py` | `berrypy start` |
| **Management** | Manual process control | Built-in commands |

---

## 🛠️ Development

### Project Structure
```python
taskapp/
├── taskapp.py              # Main Flask server (1,736 lines)
├── taskmgr.html            # Main UI (2,500 lines)
├── auto-config.html        # Configuration page
├── app-icons/              # Custom app icons
│   ├── aichat.png
│   ├── github.png
│   ├── copyclip.png
│   ├── rocketchat.png
│   ├── telegram.png
│   ├── term49-settings.png
│   ├── webshell.png
│   └── youtube.png
├── news.json               # News feed
└── about.html              # About page
```

### Key Components

**Python Backend (`taskapp.py`):**
- HTTP server on port 8001
- Process management (start/stop apps)
- App installation from remote store
- Auto-start configuration
- Caching system (5-min cache)
- Smart port detection

**HTML/JavaScript Frontend:**
- ES5-compatible JavaScript
- Dark purple theme (#9b59b6)
- Responsive design
- Modal dialogs
- Real-time search
- Category filtering

---

## 🐛 Troubleshooting

### BerryPy won't start
```bash
# Check logs
berrypy logs

# Verify Python is installed
which python3
python3 --version

# Try stopping and restarting
berrypy stop
berrypy start
```

### Port 8001 already in use
```bash
# Check what's using the port
netstat -an | grep 8001

# Find the process
pidin | grep python

# Stop BerryPy
berrypy stop
```

### Command not found: berrypy
```bash
# Verify BerryCore environment is loaded
echo $NATIVE_TOOLS

# Source BerryCore environment
source /accounts/1000/shared/misc/berrycore/env.sh

# Check PATH
echo $PATH | grep berrycore
```

### Flask not installed
```bash
# Install Flask manually
python3 -m pip install flask

# Or reinstall BerryPy
qpkg remove berrypy
qpkg install berrypy
```

---

## 📚 Documentation

- **[BERRYCORE-INTEGRATION.md](BERRYCORE-INTEGRATION.md)** - Complete BerryCore integration guide
- **[overview.md](overview.md)** - Detailed feature overview
- **[ICON_UPDATES.md](ICON_UPDATES.md)** - Icon system documentation
- **[PORTING-GUIDE.md](PORTING-GUIDE.md)** - BerryCore porting guide

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Test thoroughly on BB10 device
4. Submit a pull request

### Areas for Contribution
- [ ] Additional app icons
- [ ] New app integrations
- [ ] UI/UX improvements
- [ ] Performance optimizations
- [ ] Documentation updates

---

## 📜 License

Developed by SW7FT for the BlackBerry community.

---

## 🔗 Links

- **BerryPy Store:** https://berrystore.sw7ft.com
- **BerryCore:** https://github.com/sw7ft/BerryCore
- **Support:** https://github.com/sw7ft/BerryCore/issues

---

## 🙏 Acknowledgments

- BlackBerry community for testing and feedback
- BerryCore developers for the excellent package system
- All contributors and users

---

## 📊 Version History

### v2.0 (Current) - November 2025
- ✅ Converted to BerryCore port
- ✅ Added `berrypy` launcher command
- ✅ Integrated with qpkg system
- ✅ Improved logging and process management
- ✅ Updated documentation
- ✅ Purple berry branding
- ✅ Custom app icons (8 apps)
- ✅ Enhanced port detection

### v1.0 - July 2024
- Initial release
- Standalone installation via old-setup.sh
- Basic app management features
- Web interface

---

**Made with 💜 for BlackBerry users everywhere**



# berrypy
