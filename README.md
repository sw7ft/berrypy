# 🫐 BerryPy - BlackBerry App Platform

> **Web-based application manager for BlackBerry BB10/QNX devices**

[![Version](https://img.shields.io/badge/version-2.0-purple)](https://github.com/sw7ft/BerryPy)
[![Platform](https://img.shields.io/badge/platform-BB10%2FQNX-black)](https://github.com/sw7ft/BerryPy)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## 📱 What is BerryPy?

BerryPy is a web-based application manager for BlackBerry BB10/QNX devices. Install, manage, and monitor Python web applications - all from your BlackBerry browser.

**Features:**
- 🎨 Modern purple-themed UI optimized for BB10
- 📦 Install apps from berrystore.sw7ft.com
- 🔄 Start/stop/monitor running applications
- ⚙️ Configure auto-start on boot
- 💜 Custom app icons

**Access:** http://127.0.0.1:8001

---

## 🚀 Quick Start

### For Users

```bash
# With BerryCore
qpkg install python berrypy
berrypy start

# Standalone
curl -O https://berrystore.sw7ft.com/setup.sh
chmod +x setup.sh
./setup.sh
```

Open browser to: `http://127.0.0.1:8001`

📖 **Full installation guide:** [docs/INSTALL.md](docs/INSTALL.md)

### For Developers

```bash
# Clone and build
git clone https://github.com/sw7ft/BerryPy.git
cd BerryPy
./build-port.sh

# Output: web-berrypy-2.0.zip
```

📖 **Contributing guide:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🎯 How It Works

```
BerryPy (web interface @ :8001)
    ↓
Downloads apps from berrystore.sw7ft.com
    ↓
Installs to:
  - Web apps: ~/apps/
  - CLI apps: ~/usr/local/bin/
    ↓
Manages via web interface
```

---

## 🛠️ Development

### Building

```bash
./build-port.sh
```

Creates `web-berrypy-2.0.zip` (80KB) ready for deployment.

### Testing

**⚠️ CRITICAL:** Always test on actual BB10/QNX device.

```bash
# On BB10 device:
cd $NATIVE_TOOLS
unzip -o /path/to/web-berrypy-2.0.zip
berrypy start
# Open browser to http://127.0.0.1:8001
```

### Project Structure

```
BerryPy/
├── taskapp/              # Source files
│   ├── taskapp.py       # Python server
│   ├── taskmgr.html     # Web interface
│   └── app-icons/       # App icons (48x48 PNG)
├── build-port.sh        # Port builder
└── docs/                # Documentation
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Important for BB10/QNX

- ✅ Use `#!/bin/sh` (not `#!/bin/bash`)
- ✅ Use `pidin -p` (not `ps -p`) for process detection
- ✅ Test on actual BB10 device

See [docs/QNX-COMPATIBILITY.md](docs/QNX-COMPATIBILITY.md) for details.

---

## 📚 Documentation

- **[Quick Start](docs/QUICK-START.md)** - 5-minute setup
- **[Installation](docs/INSTALL.md)** - Detailed installation
- **[Architecture](docs/ARCHITECTURE.md)** - How it works
- **[QNX Compatibility](docs/QNX-COMPATIBILITY.md)** - BB10/QNX specifics
- **[Changelog](docs/CHANGELOG.md)** - Version history

---

## 🎨 Supported Apps

BerryPy includes icons for:
- AI-Chat, BB10Git, copyclip
- RocketChat, Telegram, Term49-Settings
- Webshell, YouTube

All icons are 48x48px PNG optimized for BB10.

---

## 🔧 Commands

```bash
berrypy start      # Start server
berrypy stop       # Stop server
berrypy restart    # Restart server
berrypy status     # Check status
berrypy logs       # View logs
berrypy help       # Show help
```

---

## 🐛 Troubleshooting

```bash
# Check logs
berrypy logs

# Verify Python
which python3

# Check BerryCore environment
echo $NATIVE_TOOLS

# Test manually
cd $NATIVE_TOOLS/share/berrypy
python3 taskapp.py
```

See [docs/INSTALL.md](docs/INSTALL.md) for more troubleshooting.

---

## 📦 Installation Methods

### BerryCore (Recommended)

```bash
qpkg install python berrypy
```

### Standalone

```bash
curl -O https://berrystore.sw7ft.com/setup.sh
./setup.sh
```

---

## ⚙️ Requirements

- BlackBerry BB10/QNX device
- Python 3.11+
- ~80KB storage

---

## 📜 License

MIT License - see [LICENSE](LICENSE)

---

## 🔗 Links

- **GitHub:** https://github.com/sw7ft/BerryPy
- **BerryCore:** https://github.com/sw7ft/BerryCore
- **Store:** https://berrystore.sw7ft.com
- **Issues:** https://github.com/sw7ft/BerryPy/issues

---

## 🙏 Acknowledgments

Thanks to the BlackBerry community and all contributors!

---

**Made with 💜 for BlackBerry users everywhere**
