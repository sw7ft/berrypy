# BerryPy Installation Guide

Complete installation instructions for BerryPy on BlackBerry BB10/QNX devices.

---

## 🎯 Choose Your Installation Method

### Method 1: BerryCore Port (Recommended) ⭐

**Best for:** Users with BerryCore installed  
**Advantages:** Easy installation, automatic updates, clean management

### Method 2: Standalone Installation (Legacy)

**Best for:** Users without BerryCore  
**Advantages:** No dependencies, direct installation

---

## 📦 Method 1: BerryCore Port Installation

### Prerequisites
- BlackBerry BB10/QNX device
- [BerryCore v0.7+](https://github.com/sw7ft/BerryCore) installed
- Terminal access (Term49 or SSH)

### Step 1: Install Python (if not already installed)
```bash
qpkg install python
```

Verify Python installation:
```bash
python3 --version
# Should show: Python 3.11.x or later
```

### Step 2: Install BerryPy
```bash
qpkg install berrypy
```

### Step 3: Start BerryPy
```bash
berrypy start
```

Expected output:
```
Starting BerryPy...
✓ BerryPy started successfully!

  Access at: http://127.0.0.1:8001
  View logs: berrypy logs
  Stop with: berrypy stop
```

### Step 4: Access the Interface
1. Open your BlackBerry browser
2. Navigate to: `http://127.0.0.1:8001`
3. Bookmark or add to home screen for quick access

### Step 5: Auto-Start (Optional)
To start BerryPy automatically on boot:

```bash
nano ~/.profile
```

Add this line at the end:
```bash
# BerryPy Auto-Start
berrypy start >/dev/null 2>&1 &
```

Save and exit (Ctrl+O, Enter, Ctrl+X).

---

## 🔧 Method 2: Standalone Installation

### Prerequisites
- BlackBerry BB10/QNX device
- Terminal access (Term49 or SSH)
- Internet connection

### Step 1: Download Installation Script
```bash
curl -O https://berrystore.sw7ft.com/setup.sh
chmod +x setup.sh
```

### Step 2: Run Installation
```bash
./setup.sh
```

The script will:
1. Download and install Python 3.11
2. Install pip and required packages
3. Download and install BerryPy
4. Configure auto-start
5. Set up PATH and environment

### Step 3: Verify Installation
```bash
# Check if taskapp directory exists
ls ~/apps/taskapp/

# Verify Python is accessible
which python3
python3 --version
```

### Step 4: Access the Interface
BerryPy starts automatically. Open your browser to:
```
http://127.0.0.1:8001
```

### Step 5: Manual Start (if needed)
```bash
cd ~/apps/taskapp
python3 taskapp.py &
```

---

## 🔄 Upgrading

### BerryCore Port
```bash
qpkg update berrypy
```

### Standalone
```bash
# Stop the old version
pkill -f taskapp.py

# Re-run installation script
./setup.sh
```

---

## 🗑️ Uninstallation

### BerryCore Port
```bash
# Stop BerryPy
berrypy stop

# Uninstall
qpkg remove berrypy
```

### Standalone
```bash
# Stop BerryPy
pkill -f taskapp.py

# Remove files
rm -rf ~/apps/taskapp/

# Clean up .profile
nano ~/.profile
# Remove the lines between:
# # <<< TaskApp Start >>>
# # <<< End TaskApp Start >>>
```

---

## 📱 Post-Installation

### First Run Checklist

1. ✅ **Access the interface:**
   - Open browser to `http://127.0.0.1:8001`
   - You should see the BerryPy purple interface

2. ✅ **Test app management:**
   - Navigate to "Available Apps" tab
   - Try installing a sample app
   - Check "Manage Apps" to see it running

3. ✅ **Bookmark the page:**
   - In BlackBerry browser, tap menu
   - Select "Add to Home Screen"
   - Name it "BerryPy"

4. ✅ **Configure auto-start:**
   - Go to Device Settings (☰ menu)
   - Select "Auto-Start Config"
   - Enable auto-start for desired apps

### Recommended Apps to Install

After installing BerryPy, try these apps:
- **copyclip** - Clipboard manager
- **Webshell** - Web-based terminal
- **Term49-Settings** - Terminal configuration

---

## 🔐 Security Notes

- BerryPy listens on `127.0.0.1` (localhost only)
- Not accessible from network by default
- All app data stored locally on device
- No external authentication required

To make BerryPy accessible from network:
1. Edit `taskapp.py`
2. Change `("", PORT)` to `("0.0.0.0", PORT)`
3. **Warning:** Only do this on trusted networks

---

## 🌐 Network Configuration

### Accessing from Computer (via USB/WiFi)

If your BlackBerry is connected via USB or on same WiFi:

1. Find your BlackBerry's IP address:
```bash
ifconfig | grep "inet addr"
```

2. Edit BerryPy to allow network access:
```bash
nano ~/apps/taskapp/taskapp.py
```

Find this line:
```python
with socketserver.TCPServer(("", PORT), TaskManagerHandler) as httpd:
```

Change to:
```python
with socketserver.TCPServer(("0.0.0.0", PORT), TaskManagerHandler) as httpd:
```

3. Restart BerryPy:
```bash
berrypy restart
```

4. Access from computer:
```
http://[BlackBerry-IP]:8001
```

---

## 🐛 Troubleshooting Installation

### Issue: Python installation fails

**Solution:**
```bash
# Clean up any partial installation
rm -rf ~/apps/ ~/usr/

# Restart phone
reboot

# Try again
./setup.sh
```

### Issue: pip installation fails

**Solution:**
```bash
# Try manual pip installation
python3 -m ensurepip --upgrade

# Install Flask manually
python3 -m pip install flask
```

### Issue: Port 8001 already in use

**Solution:**
```bash
# Find what's using the port
netstat -an | grep 8001

# Kill the process
pkill -f taskapp.py

# Start again
berrypy start
```

### Issue: BerryPy starts but can't access

**Solution:**
```bash
# Check if it's actually running
berrypy status

# Check logs for errors
berrypy logs

# Try restarting
berrypy restart
```

### Issue: "command not found: berrypy"

**Solution (BerryCore users):**
```bash
# Source BerryCore environment
source /accounts/1000/shared/misc/berrycore/env.sh

# Add to .profile if not already there
echo 'source /accounts/1000/shared/misc/berrycore/env.sh' >> ~/.profile
```

### Issue: Apps won't install/start

**Solution:**
```bash
# Check app paths
ls ~/apps/

# Verify Python is in PATH
which python3

# Check BerryPy logs
berrypy logs
```

---

## 📞 Getting Help

### Before Asking for Help

1. Check the logs:
```bash
berrypy logs
```

2. Verify system requirements:
```bash
python3 --version  # Should be 3.11+
which python3      # Should show a path
```

3. Try restarting:
```bash
berrypy restart
```

### Support Channels

- **GitHub Issues:** https://github.com/sw7ft/BerryCore/issues
- **BerryCore Discussion:** https://github.com/sw7ft/BerryCore/discussions
- **BerryPy Store:** https://berrystore.sw7ft.com

---

## ✅ Installation Complete!

You should now have:
- ✅ BerryPy running on your BlackBerry
- ✅ Access to the web interface at http://127.0.0.1:8001
- ✅ Ability to install and manage apps
- ✅ Auto-start configured (optional)

**Next Steps:**
1. Browse available apps in the "Available Apps" tab
2. Install your first app
3. Configure auto-start for essential apps
4. Add BerryPy to your home screen

---

**Made with 💜 for BlackBerry users everywhere**


