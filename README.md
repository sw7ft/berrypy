# 🫐 BerryPy

> **Modern web-based application manager for BlackBerry BB10/QNX devices**

[![Version](https://img.shields.io/badge/version-2.0-purple)](https://github.com/sw7ft/BerryPy)
[![Platform](https://img.shields.io/badge/platform-BB10%2FQNX-black)](https://github.com/sw7ft/BerryPy)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)

---

## 📱 What is BerryPy?

BerryPy transforms your BlackBerry BB10 into a powerful app platform. Install, manage, and monitor Python applications directly from your browser.

### ✨ Key Features

- **🎨 Beautiful UI** - Purple-themed interface optimized for BB10 browsers
- **📦 App Store** - Browse and install apps from berrystore.sw7ft.com
- **⚡ Process Manager** - Start, stop, and monitor running applications
- **🔄 Auto-Start** - Configure apps to launch automatically on boot
- **💜 Custom Icons** - Visual app identification with 48x48px icons
- **📰 News Feed** - Stay updated with the latest app releases
- **🤖 Android Support** - Manage APK installations

### 🌐 Access

Once running, access BerryPy at: **http://127.0.0.1:8001**

---

## 🚀 Quick Start

### For Users

```bash
# Install Python
qpkg install python3

# Install BerryPy
qpkg install berrypy

# Start BerryPy
berrypy start

# Open browser to http://127.0.0.1:8001
```

📖 **Full installation guide:** [docs/INSTALL.md](docs/INSTALL.md)

---

### For Developers

```bash
# Clone repository
git clone https://github.com/sw7ft/BerryPy.git
cd BerryPy

# Build package
./build-port.sh

# Output: web-berrypy-2.0.zip (80KB)
```

📖 **Developer guide:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🎯 How It Works

```
┌─────────────────────────────────────┐
│  BlackBerry Browser                 │
│  http://127.0.0.1:8001             │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│  BerryPy Flask Server               │
│  • Manage apps                      │
│  • Process control                  │
│  • Download/Install                 │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│  BerryStore (berrystore.sw7ft.com)  │
│  • Web apps  → ~/apps/              │
│  • CLI tools → ~/usr/local/bin/     │
│  • APK files → Downloads            │
└─────────────────────────────────────┘
```

---

## 🛠️ Development

### Project Structure

```
BerryPy/
├── taskapp/                  # 📦 Application source
│   ├── taskapp.py           #    Main Flask server
│   ├── taskmgr.html         #    Web interface
│   ├── about.html           #    About page
│   ├── android.html         #    Android APK manager
│   ├── auto-config.html     #    Auto-start configuration
│   ├── news.json            #    News feed data
│   ├── news_manager.py      #    News system
│   └── app-icons/           #    48x48 PNG icons
│
├── port/                    # 🎯 Official BerryCore Port
│   ├── web-berrypy-2.0.zip  #    Ready-to-install package
│   └── README.md            #    Port documentation
│
├── build-port.sh            # 🔨 Package builder script
├── taskapp.zip              # 📦 Original source archive
│
├── docs/                    # 📖 Documentation
│   ├── QUICK-START.md       #    5-minute setup guide
│   ├── INSTALL.md           #    Detailed installation
│   ├── ARCHITECTURE.md      #    System design
│   ├── CHANGELOG.md         #    Version history
│   ├── QNX-COMPATIBILITY.md #    BB10/QNX specifics
│   ├── ICON_UPDATES.md      #    Icon system guide
│   └── overview.md          #    Detailed overview
│
├── CONTRIBUTING.md          # 🤝 Contribution guidelines
├── LICENSE                  # 📜 MIT License
└── README.md               # 📄 This file
```

### Building

```bash
# Build BerryCore package
./build-port.sh

# Output: web-berrypy-2.0.zip (80KB)
# Automatically copied to port/ directory
```

**Package contents:**
```
web-berrypy-2.0.zip
├── bin/berrypy              # Launcher script
├── share/berrypy/           # Application files
│   ├── taskapp.py
│   ├── taskmgr.html
│   ├── app-icons/
│   └── ...
└── doc/                     # Documentation
```

📦 **Official package:** [port/web-berrypy-2.0.zip](port/web-berrypy-2.0.zip)

### Testing

**⚠️ CRITICAL:** Always test on actual BB10/QNX device before submitting PRs.

```bash
# Deploy to BB10 device
scp web-berrypy-2.0.zip bb10:/tmp/

# SSH to device and install
ssh bb10
cd $NATIVE_TOOLS
unzip -o /tmp/web-berrypy-2.0.zip

# Test
berrypy start
# Open browser to http://127.0.0.1:8001
```

---

## 🤝 Contributing

We welcome contributions from the BlackBerry community! 

### Get Started

1. **Fork** the repository
2. **Clone** your fork
3. **Create** a feature branch
4. **Make** your changes
5. **Test** on BB10 device
6. **Submit** a pull request

📖 **Full guide:** [CONTRIBUTING.md](CONTRIBUTING.md)

### Important BB10/QNX Rules

When developing for BB10/QNX, always follow these critical rules:

| Rule | ❌ Wrong | ✅ Correct |
|------|----------|-----------|
| **Shebang** | `#!/bin/bash` | `#!/bin/sh` |
| **Process Check** | `ps -p $PID` | `pidin -p $PID` |
| **Shell Syntax** | `[[ ]]` | `[ ]` |
| **String Compare** | `==` | `=` |

**Why?** BB10/QNX doesn't have bash or GNU utilities. Using Linux-specific commands will fail!

📖 **Details:** [docs/QNX-COMPATIBILITY.md](docs/QNX-COMPATIBILITY.md)

---

## 📚 Documentation

| Guide | Description |
|-------|-------------|
| [Quick Start](docs/QUICK-START.md) | Get BerryPy running in 5 minutes |
| [Installation](docs/INSTALL.md) | Detailed installation instructions |
| [Architecture](docs/ARCHITECTURE.md) | How BerryPy works internally |
| [QNX Compatibility](docs/QNX-COMPATIBILITY.md) | BB10/QNX development guide |
| [Changelog](docs/CHANGELOG.md) | Version history and updates |
| [Icon System](docs/ICON_UPDATES.md) | Adding custom app icons |

---

## 🎨 Supported Apps

BerryPy comes with pre-configured icons for popular apps:

- **🤖 AI-Chat** - AI-powered chat assistant
- **🐙 BB10Git** - GitHub repository manager  
- **📋 copyclip** - Clipboard sync tool
- **💬 RocketChat** - Team communication
- **✈️ Telegram** - Messaging client
- **⚙️ Term49-Settings** - Terminal configuration
- **🖥️ Webshell** - Web-based terminal
- **📺 YouTube** - Video player

All icons are 48x48px PNG format, optimized for BB10 displays.

**Want to add an icon?** See [docs/ICON_UPDATES.md](docs/ICON_UPDATES.md)

---

## 🔧 Commands

BerryPy includes a convenient command-line interface:

```bash
berrypy start      # Start the BerryPy server
berrypy stop       # Stop the server gracefully
berrypy restart    # Restart the server
berrypy status     # Check if running
berrypy logs       # View recent log entries
berrypy url        # Display access URL
berrypy help       # Show help information
```

---

## 🐛 Troubleshooting

### Common Issues

**BerryPy won't start:**
```bash
# Check if Python is installed
which python3
python3 --version

# Check logs
berrypy logs

# Try manual start
cd $NATIVE_TOOLS/share/berrypy
python3 taskapp.py
```

**Can't access web interface:**
```bash
# Verify BerryPy is running
berrypy status

# Check if port 8001 is in use
pidin | grep 8001

# Restart BerryPy
berrypy restart
```

**Apps won't install:**
```bash
# Check network connectivity
ping berrystore.sw7ft.com

# Verify disk space
df -h

# Check logs for errors
berrypy logs
```

📖 **More troubleshooting:** [docs/INSTALL.md](docs/INSTALL.md)

---

## ⚙️ Requirements

- **Device:** BlackBerry BB10 (any model with QNX)
- **BerryCore:** Package manager (required)
- **Python:** 3.11 or higher (install via `qpkg install python3`)
- **Storage:** ~80KB for BerryPy (apps vary)
- **Network:** Internet connection for app downloads

**For Development:**
- SSH access to device
- Git for version control

---

## 🗺️ Roadmap

Future features under consideration:

- [ ] **App Updates** - Check for and install app updates
- [ ] **Ratings/Reviews** - Community app feedback
- [ ] **Search & Filters** - Find apps faster
- [ ] **Dark Theme** - Alternative color scheme
- [ ] **Backup/Restore** - Save app configurations
- [ ] **Multi-language** - Internationalization support

**Want to contribute?** Pick a feature and submit a PR!

---

## 📜 License

BerryPy is open source software licensed under the [MIT License](LICENSE).

```
Copyright (c) 2025 SW7FT

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🔗 Links

- **📦 Repository:** [github.com/sw7ft/BerryPy](https://github.com/sw7ft/BerryPy)
- **🎯 BerryCore:** [github.com/sw7ft/BerryCore](https://github.com/sw7ft/BerryCore)
- **🏪 App Store:** [berrystore.sw7ft.com](https://berrystore.sw7ft.com)
- **🐛 Issues:** [github.com/sw7ft/BerryPy/issues](https://github.com/sw7ft/BerryPy/issues)
- **💬 Discussions:** [github.com/sw7ft/BerryPy/discussions](https://github.com/sw7ft/BerryPy/discussions)

---

## 🙏 Acknowledgments

Special thanks to:

- The **BlackBerry community** for keeping BB10 alive
- **Contributors** who help improve BerryPy
- **App developers** on BerryStore
- Everyone keeping QNX development active

---

## 📸 Screenshots

*Coming soon! Add screenshots of your BerryPy interface to showcase features.*

---

<div align="center">

**Made with 💜 for BlackBerry enthusiasts everywhere**

*Keep your BB10 alive with BerryPy*

[⭐ Star this repo](https://github.com/sw7ft/BerryPy) • [🐛 Report Bug](https://github.com/sw7ft/BerryPy/issues) • [💡 Request Feature](https://github.com/sw7ft/BerryPy/issues)

</div>
