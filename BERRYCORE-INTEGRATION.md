# BerryPy Integration with BerryCore

This document explains how BerryPy integrates with the BerryCore package management system.

## Overview

BerryPy is now available as a native BerryCore port, making installation and management seamless with the `qpkg` package manager.

---

## Building the Port

### Prerequisites
- BerryCore v0.7 or later installed
- `taskapp.zip` file in the current directory

### Build Command
```bash
chmod +x build-port.sh
./build-port.sh
```

This creates: `web-berrypy-2.0.zip`

---

## Port Structure

```
web-berrypy-2.0.zip
├── bin/
│   └── berrypy              # Main launcher script
├── share/
│   └── berrypy/
│       ├── taskapp.py       # Main Python application
│       ├── taskmgr.html     # Web interface
│       ├── auto-config.html # Configuration page
│       ├── app-icons/       # Application icons
│       ├── news.json        # News feed
│       └── ...              # Other app files
└── doc/
    ├── README.md            # Installation & usage guide
    ├── overview.md          # Detailed overview
    └── ICON_UPDATES.md      # Icon system documentation
```

---

## Installation in BerryCore

### Option 1: Add to BerryCore Repository

1. **Copy port package:**
   ```bash
   cp web-berrypy-2.0.zip /path/to/BerryCore/ports/
   ```

2. **Update INDEX:**
   ```bash
   cd /path/to/BerryCore/ports/
   echo "berrypy|web|2.0|150K|BlackBerry App Platform - Full-featured application manager" >> INDEX
   ```

3. **Install via qpkg:**
   ```bash
   qpkg install berrypy
   ```

### Option 2: Local Installation (Testing)

```bash
# Install directly from local file
cd $NATIVE_TOOLS
unzip -o /path/to/web-berrypy-2.0.zip

# Test the installation
berrypy start
```

---

## Usage

### Starting BerryPy
```bash
berrypy start
```

The web interface will be available at: `http://127.0.0.1:8001`

### Stopping BerryPy
```bash
berrypy stop
```

### Check Status
```bash
berrypy status
```

### View Logs
```bash
berrypy logs
```

### Other Commands
```bash
berrypy restart   # Restart the server
berrypy url       # Show access URL
berrypy help      # Show help
```

---

## Auto-Start Configuration

### Method 1: Using .profile (Recommended for BerryCore)

Add to your `~/.profile`:
```bash
# BerryPy Auto-Start
if command -v berrypy >/dev/null 2>&1; then
    berrypy start >/dev/null 2>&1 &
fi
```

### Method 2: Using BerryCore Environment

Create a startup script in BerryCore:
```bash
cat > $NATIVE_TOOLS/../startup.d/berrypy.sh << 'EOF'
#!/bin/bash
# Auto-start BerryPy
if command -v berrypy >/dev/null 2>&1; then
    berrypy start >/dev/null 2>&1 &
fi
EOF

chmod +x $NATIVE_TOOLS/../startup.d/berrypy.sh
```

### Method 3: Manual .profile Edit

Edit `~/.profile`:
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

## Dependencies

BerryPy requires:
- **Python 3.11+** - Install via: `qpkg install python`
- **Flask** - Auto-installed via pip when Python is available

### Installing Python (if not already installed)
```bash
qpkg install python
```

---

## Integration Benefits

### Compared to Old Setup Script

| Feature | Old Setup | BerryCore Port |
|---------|-----------|----------------|
| Installation | Manual curl + unzip | `qpkg install berrypy` |
| Updates | Manual re-download | `qpkg update berrypy` |
| Removal | Manual rm -rf | `qpkg remove berrypy` |
| Dependencies | Manual pip install | Automatic via qpkg |
| Path Setup | Manual .profile edit | Automatic via BerryCore |
| Location | `~/apps/taskapp/` | `$NATIVE_TOOLS/share/berrypy/` |
| Launcher | Direct python call | Clean `berrypy` command |

### Advantages

✅ **Cleaner Installation** - One command to install  
✅ **Better Management** - Standard qpkg commands  
✅ **Automatic Updates** - Update via package system  
✅ **Dependency Tracking** - Python requirement handled  
✅ **Standard Paths** - Follows BerryCore conventions  
✅ **Clean Launcher** - Simple `berrypy` command  
✅ **Log Management** - Centralized logging  
✅ **PID Tracking** - Proper process management  

---

## File Locations

After installation via BerryCore:

```bash
# Assuming NATIVE_TOOLS=/accounts/1000/shared/misc

# Launcher script
/accounts/1000/shared/misc/bin/berrypy

# Application files
/accounts/1000/shared/misc/share/berrypy/
├── taskapp.py
├── taskmgr.html
├── app-icons/
└── ...

# Documentation
/accounts/1000/shared/misc/doc/README.md

# Runtime files
/accounts/1000/shared/misc/share/berrypy/berrypy.log    # Logs
/accounts/1000/shared/misc/share/berrypy/berrypy.pid    # PID file
```

---

## Troubleshooting

### BerryPy command not found

```bash
# Verify BerryCore environment is loaded
echo $NATIVE_TOOLS

# Source BerryCore environment if needed
source /accounts/1000/shared/misc/berrycore/env.sh

# Check if berrypy is installed
ls $NATIVE_TOOLS/bin/berrypy
```

### Python not found

```bash
# Install Python via qpkg
qpkg install python

# Verify Python is available
which python3
python3 --version
```

### Port 8001 already in use

```bash
# Check what's using the port
netstat -an | grep 8001

# Find the process
pidin | grep python

# Stop BerryPy cleanly
berrypy stop
```

### Flask not installed

```bash
# Install Flask via pip
python3 -m pip install flask

# Or let BerryPy install it on first run
berrypy start
```

---

## Migration from Old Setup

If you previously installed BerryPy using the old `old-setup.sh`:

### 1. Stop the old installation
```bash
# Find the old process
ps aux | grep taskapp.py

# Kill it
kill <PID>
```

### 2. Remove old installation
```bash
# Remove old files
rm -rf ~/apps/taskapp/

# Clean up .profile (remove old auto-start lines)
nano ~/.profile
# Remove the lines between:
# # <<< TaskApp Start >>>
# # <<< End TaskApp Start >>>
```

### 3. Install BerryCore port
```bash
qpkg install berrypy
```

### 4. Start new version
```bash
berrypy start
```

### 5. Add auto-start (optional)
```bash
echo 'berrypy start >/dev/null 2>&1 &' >> ~/.profile
```

---

## Testing the Port

### Verification Checklist

1. ✅ **Package structure is correct:**
   ```bash
   unzip -l web-berrypy-2.0.zip
   ```

2. ✅ **Installation works:**
   ```bash
   qpkg install berrypy
   ```

3. ✅ **Launcher is executable:**
   ```bash
   which berrypy
   berrypy help
   ```

4. ✅ **Server starts:**
   ```bash
   berrypy start
   berrypy status
   ```

5. ✅ **Web interface accessible:**
   ```bash
   # Open in browser: http://127.0.0.1:8001
   ```

6. ✅ **Logs are created:**
   ```bash
   berrypy logs
   ```

7. ✅ **Server stops cleanly:**
   ```bash
   berrypy stop
   ```

---

## Contributing

To contribute improvements to the BerryPy port:

1. Fork the BerryCore repository
2. Make changes to the port
3. Test thoroughly on BB10 device
4. Submit pull request with:
   - Updated port package
   - Updated INDEX entry
   - Description of changes
   - Testing notes

---

## Support

- **BerryPy Store:** https://berrystore.sw7ft.com
- **BerryCore GitHub:** https://github.com/sw7ft/BerryCore
- **BerryCore Issues:** https://github.com/sw7ft/BerryCore/issues

---

## Version History

### v2.0 (Current)
- Converted to BerryCore port
- Added `berrypy` launcher command
- Integrated with qpkg system
- Improved logging and process management
- Updated documentation

### v1.0
- Original standalone installation
- Used old-setup.sh for installation
- Installed to ~/apps/taskapp/

---

**Made with 💜 for BlackBerry + BerryCore users everywhere**


