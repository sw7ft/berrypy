#!/bin/bash
# BerryPy Port Builder for BerryCore
# Creates a proper BerryCore port package from taskapp

set -e

VERSION="2.0"
PORT_NAME="berrypy"
CATEGORY="web"
PACKAGE_NAME="${CATEGORY}-${PORT_NAME}-${VERSION}.zip"

echo "==================================="
echo "BerryPy Port Builder for BerryCore"
echo "Version: $VERSION"
echo "==================================="
echo ""

# Clean up any previous builds
echo "Cleaning previous builds..."
rm -rf port-build/
rm -f ${PACKAGE_NAME}

# Create port structure
echo "Creating port structure..."
mkdir -p port-build/bin
mkdir -p port-build/share/berrypy
mkdir -p port-build/doc

# Extract taskapp.zip to get files
echo "Extracting taskapp.zip..."
unzip -q taskapp.zip -d temp-extract/

# Copy main script to bin with wrapper
echo "Creating launcher script..."
cat > port-build/bin/berrypy << 'EOF'
#!/bin/sh
# BerryPy Launcher for BerryCore
# CRITICAL: Must use /bin/sh (not /bin/bash) for BB10/QNX compatibility
# Starts the BerryPy app manager on port 8001

BERRYPY_DIR="${NATIVE_TOOLS}/share/berrypy"
BERRYPY_LOG="${BERRYPY_DIR}/berrypy.log"
BERRYPY_PID="${BERRYPY_DIR}/berrypy.pid"

# Ensure BerryPy-managed app paths are available
# BerryPy installs web apps to ~/apps/ and CLI apps to ~/usr/local/bin/
export PATH="$HOME/usr/local/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/usr/local/lib:$LD_LIBRARY_PATH"

usage() {
    cat << HELP
BerryPy - BlackBerry App Platform Manager

Usage: berrypy [command]

Commands:
    start       Start BerryPy server (default)
    stop        Stop BerryPy server
    restart     Restart BerryPy server
    status      Check if BerryPy is running
    logs        Show recent logs
    url         Show the access URL

Examples:
    berrypy start          # Start the server
    berrypy                # Same as start
    berrypy status         # Check if running

Once started, access BerryPy at: http://127.0.0.1:8001

HELP
}

start_berrypy() {
    if [ -f "$BERRYPY_PID" ]; then
        PID=$(cat "$BERRYPY_PID")
        # CRITICAL: Use pidin (QNX) instead of ps for BB10 compatibility
        if pidin -p "$PID" > /dev/null 2>&1; then
            echo "BerryPy is already running (PID: $PID)"
            echo "Access at: http://127.0.0.1:8001"
            return 0
        else
            # Stale PID file
            rm -f "$BERRYPY_PID"
        fi
    fi
    
    echo "Starting BerryPy..."
    cd "$BERRYPY_DIR"
    nohup python3 taskapp.py >> "$BERRYPY_LOG" 2>&1 &
    echo $! > "$BERRYPY_PID"
    
    # Wait a moment and verify it started
    sleep 2
    # CRITICAL: Use pidin for QNX process detection
    if pidin -p $(cat "$BERRYPY_PID") > /dev/null 2>&1; then
        echo "✓ BerryPy started successfully!"
        echo ""
        echo "  Access at: http://127.0.0.1:8001"
        echo "  View logs: berrypy logs"
        echo "  Stop with: berrypy stop"
        echo ""
    else
        echo "✗ Failed to start BerryPy. Check logs:"
        echo "  berrypy logs"
        rm -f "$BERRYPY_PID"
        exit 1
    fi
}

stop_berrypy() {
    if [ ! -f "$BERRYPY_PID" ]; then
        echo "BerryPy is not running (no PID file)"
        return 0
    fi
    
    PID=$(cat "$BERRYPY_PID")
    # CRITICAL: Use pidin for QNX process detection
    if ! pidin -p "$PID" > /dev/null 2>&1; then
        echo "BerryPy is not running (stale PID file)"
        rm -f "$BERRYPY_PID"
        return 0
    fi
    
    echo "Stopping BerryPy (PID: $PID)..."
    kill "$PID" 2>/dev/null || true
    
    # Wait for process to stop (max 5 seconds)
    for i in 1 2 3 4 5; do
        # CRITICAL: Use pidin for QNX process detection
        if ! pidin -p "$PID" > /dev/null 2>&1; then
            echo "✓ BerryPy stopped successfully"
            rm -f "$BERRYPY_PID"
            return 0
        fi
        sleep 1
    done
    
    # Force kill if still running
    echo "Force stopping BerryPy..."
    kill -9 "$PID" 2>/dev/null || true
    rm -f "$BERRYPY_PID"
    echo "✓ BerryPy stopped"
}

status_berrypy() {
    if [ ! -f "$BERRYPY_PID" ]; then
        echo "Status: Not running"
        return 1
    fi
    
    PID=$(cat "$BERRYPY_PID")
    # CRITICAL: Use pidin for QNX process detection
    if pidin -p "$PID" > /dev/null 2>&1; then
        echo "Status: Running (PID: $PID)"
        echo "URL: http://127.0.0.1:8001"
        echo "Logs: $BERRYPY_LOG"
        return 0
    else
        echo "Status: Not running (stale PID file)"
        rm -f "$BERRYPY_PID"
        return 1
    fi
}

show_logs() {
    if [ ! -f "$BERRYPY_LOG" ]; then
        echo "No logs found at $BERRYPY_LOG"
        return 1
    fi
    
    echo "=== BerryPy Logs (last 50 lines) ==="
    tail -50 "$BERRYPY_LOG"
}

# Main command handling
case "${1:-start}" in
    start)
        start_berrypy
        ;;
    stop)
        stop_berrypy
        ;;
    restart)
        stop_berrypy
        sleep 1
        start_berrypy
        ;;
    status)
        status_berrypy
        ;;
    logs)
        show_logs
        ;;
    url)
        echo "http://127.0.0.1:8001"
        ;;
    -h|--help|help)
        usage
        ;;
    *)
        echo "Unknown command: $1"
        echo "Run 'berrypy help' for usage"
        exit 1
        ;;
esac
EOF

chmod +x port-build/bin/berrypy

# Copy application files to share directory
echo "Copying application files..."
if [ -d "temp-extract/taskapp" ]; then
    # Handle nested directory
    cp -r temp-extract/taskapp/* port-build/share/berrypy/
else
    cp -r temp-extract/* port-build/share/berrypy/
fi

# Remove development artifacts (CRITICAL for clean package)
echo "Removing development artifacts..."
rm -f port-build/share/berrypy/taskapp.log
rm -f port-build/share/berrypy/taskmgr.html.*
rm -f port-build/share/berrypy/oldmgr.html
rm -rf port-build/share/berrypy/__MACOSX
rm -f port-build/share/berrypy/.DS_Store
find port-build/share/berrypy -name ".DS_Store" -delete

# Create documentation
echo "Creating documentation..."
cat > port-build/doc/README.md << 'DOCEOF'
# BerryPy - BlackBerry App Platform Manager

**Version:** 2.0  
**Category:** Web Application Manager  
**Author:** SW7FT

## Overview

BerryPy is a full-featured application manager designed specifically for BlackBerry 
devices running BB10/QNX systems. Manage, install, and monitor all your Python web 
applications from one beautiful, unified interface.

## Installation

```bash
# Install BerryPy (requires Python port)
qpkg install berrypy

# Start BerryPy
berrypy start

# Access the web interface
# Open browser to: http://127.0.0.1:8001
```

## Usage

### Starting BerryPy
```bash
berrypy start     # Start the server
berrypy           # Same as start
```

### Stopping BerryPy
```bash
berrypy stop      # Stop the server
```

### Other Commands
```bash
berrypy restart   # Restart the server
berrypy status    # Check if running
berrypy logs      # View recent logs
berrypy url       # Show access URL
```

## Features

- **App Management** - Start, stop, and monitor running applications
- **App Installation** - Install web apps from the BerryPy store
- **Auto-Start Config** - Configure apps to launch on boot
- **Beautiful UI** - Dark purple theme optimized for BlackBerry
- **Process Detection** - Automatic detection of running apps
- **Port Management** - Smart port detection and display

## Requirements

- Python 3.11+ (install via: `qpkg install python`)
- Flask (will be installed automatically)

## Auto-Start on Boot (Optional)

To start BerryPy automatically when your device boots:

1. Edit your `~/.profile`:
```bash
nano ~/.profile
```

2. Add this line at the end:
```bash
berrypy start >/dev/null 2>&1 &
```

3. Save and exit (Ctrl+O, Enter, Ctrl+X)

## Accessing BerryPy

After starting BerryPy, open your BlackBerry browser and navigate to:
```
http://127.0.0.1:8001
```

You can also add this to your home screen for quick access!

## Troubleshooting

### BerryPy won't start
```bash
# Check logs
berrypy logs

# Try stopping and restarting
berrypy stop
berrypy start
```

### Port 8001 already in use
```bash
# Check what's using the port
netstat -an | grep 8001

# Stop the conflicting process
berrypy stop
```

### Python not found
```bash
# Install Python port
qpkg install python

# Verify installation
which python3
python3 --version
```

## Files and Directories

- **Binary:** `$NATIVE_TOOLS/bin/berrypy`
- **Application:** `$NATIVE_TOOLS/share/berrypy/`
- **Logs:** `$NATIVE_TOOLS/share/berrypy/berrypy.log`
- **PID File:** `$NATIVE_TOOLS/share/berrypy/berrypy.pid`

## Support

For issues, updates, or feature requests:
- Visit: https://berrystore.sw7ft.com
- GitHub: https://github.com/sw7ft/BerryPy

## License

Developed by SW7FT for the BlackBerry community.

---

**Made with 💜 for BlackBerry users everywhere**
DOCEOF

# Copy overview and icon updates docs
if [ -f "overview.md" ]; then
    cp overview.md port-build/doc/
fi

if [ -f "ICON_UPDATES.md" ]; then
    cp ICON_UPDATES.md port-build/doc/
fi

# Clean up extraction directory
rm -rf temp-extract/

# Create the port package
echo "Creating port package: $PACKAGE_NAME"
cd port-build
zip -r ../${PACKAGE_NAME} . -q
cd ..

# Verify package structure
echo ""
echo "Verifying package structure..."
unzip -l ${PACKAGE_NAME} | head -20

# Clean up build directory
rm -rf port-build/

# Copy to port/ directory
echo ""
echo "Copying package to port/ directory..."
mkdir -p port/
cp ${PACKAGE_NAME} port/
echo "✓ Package copied to: port/${PACKAGE_NAME}"

# Calculate package size
PACKAGE_SIZE=$(du -h ${PACKAGE_NAME} | cut -f1)

echo ""
echo "==================================="
echo "✓ Port package created successfully!"
echo "==================================="
echo ""
echo "Package: ${PACKAGE_NAME}"
echo "Size: ${PACKAGE_SIZE}"
echo "Location: port/${PACKAGE_NAME}"
echo ""
echo "Next steps:"
echo "1. Add to BerryCore ports directory"
echo "2. Update INDEX with:"
echo "   berrypy|web|${VERSION}|${PACKAGE_SIZE}|BlackBerry App Platform - Full-featured application manager"
echo ""
echo "Installation (after adding to ports):"
echo "   qpkg install berrypy"
echo ""
echo "Usage:"
echo "   berrypy start"
echo "   # Open browser to http://127.0.0.1:8001"
echo ""

