# BerryPy Official Port Package

This directory contains the **official BerryCore port package** for BerryPy.

---

## 📦 Current Release

**Package:** `web-berrypy-2.0.zip`  
**Version:** 2.0  
**Size:** ~80KB  
**Category:** web  
**Platform:** BlackBerry BB10/QNX

---

## 🚀 Installation

### Quick Install

```bash
# Download package
curl -O https://raw.githubusercontent.com/sw7ft/BerryPy/main/port/web-berrypy-2.0.zip

# Extract to BerryCore directory
cd $NATIVE_TOOLS
unzip -o /path/to/web-berrypy-2.0.zip

# Verify installation
berrypy --help
```

### Via BerryCore (Recommended)

```bash
# Install from BerryCore repository
qpkg install berrypy

# Start BerryPy
berrypy start
```

---

## 📋 Package Contents

```
web-berrypy-2.0.zip
├── bin/
│   └── berrypy              # Launcher script
├── share/
│   └── berrypy/
│       ├── taskapp.py       # Python Flask server
│       ├── taskmgr.html     # Web interface
│       ├── about.html       # About page
│       ├── android.html     # Android APK manager
│       ├── auto-config.html # Auto-start configuration
│       ├── news.json        # News feed
│       ├── news_manager.py  # News system
│       └── app-icons/       # 48x48 PNG icons
└── doc/
    ├── README.md            # Main documentation
    ├── overview.md          # Detailed overview
    └── ICON_UPDATES.md      # Icon system guide
```

---

## ✅ Verification

After installation, verify the package:

```bash
# Check berrypy command exists
which berrypy
# Output: /accounts/1000/shared/misc/bin/berrypy

# Check version
berrypy help

# Check files are in place
ls $NATIVE_TOOLS/share/berrypy/

# Start BerryPy
berrypy start

# Check status
berrypy status
```

---

## 🔧 BerryCore INDEX Entry

For BerryCore repository maintainers, add this to `ports/INDEX`:

```
berrypy|web|2.0|80K|BlackBerry App Platform - Full-featured application manager
```

**Format:** `name|category|version|size|description`

---

## 🏗️ Building from Source

If you want to build the port yourself:

```bash
# Clone repository
git clone https://github.com/sw7ft/BerryPy.git
cd BerryPy

# Run build script
./build-port.sh

# Output will be in: web-berrypy-2.0.zip
```

See main [README.md](../README.md) for development details.

---

## 📝 Package Specifications

| Property | Value |
|----------|-------|
| **Name** | berrypy |
| **Category** | web |
| **Version** | 2.0 |
| **Size** | ~80KB |
| **Architecture** | All (Python) |
| **Dependencies** | python3 (3.11+) |
| **Port Type** | Binary + Scripts |
| **License** | MIT |

---

## 🎯 What Gets Installed

### Executables
- `$NATIVE_TOOLS/bin/berrypy` - Main launcher script

### Application Files
- `$NATIVE_TOOLS/share/berrypy/` - All application files

### Documentation
- `$NATIVE_TOOLS/doc/` - Documentation files (optional)

### Environment
The launcher automatically sets up:
- `PATH` includes `~/usr/local/bin` for BerryPy-managed CLI apps
- `LD_LIBRARY_PATH` includes `~/usr/local/lib` for libraries

---

## 🔄 Updating

To update to a new version:

```bash
# Via BerryCore (recommended)
qpkg update
qpkg upgrade berrypy

# Manual update
cd $NATIVE_TOOLS
unzip -o /path/to/web-berrypy-NEW-VERSION.zip

# Restart BerryPy
berrypy restart
```

---

## ⚠️ BB10/QNX Compatibility

This package is specifically built for BlackBerry BB10/QNX:

- ✅ Uses `#!/bin/sh` (not bash)
- ✅ Uses `pidin` for process management (not ps)
- ✅ POSIX-compliant shell scripts
- ✅ Tested on BB10 devices

Do **NOT** use generic Linux packages - they will fail on QNX!

---

## 🐛 Issues

If you encounter issues with the port package:

1. **Check logs:** `berrypy logs`
2. **Verify Python:** `which python3 && python3 --version`
3. **Check environment:** `echo $NATIVE_TOOLS`
4. **Report issue:** https://github.com/sw7ft/BerryPy/issues

---

## 📚 Documentation

- **Main README:** [../README.md](../README.md)
- **Installation Guide:** [../docs/INSTALL.md](../docs/INSTALL.md)
- **Contributing:** [../CONTRIBUTING.md](../CONTRIBUTING.md)
- **QNX Compatibility:** [../docs/QNX-COMPATIBILITY.md](../docs/QNX-COMPATIBILITY.md)

---

## 🔗 Links

- **Repository:** https://github.com/sw7ft/BerryPy
- **BerryCore:** https://github.com/sw7ft/BerryCore
- **Issues:** https://github.com/sw7ft/BerryPy/issues

---

**This is the official, tested, and supported port package for BerryPy on BlackBerry BB10/QNX devices.**

*Built with 💜 for the BlackBerry community*

