# 🫐 BerryPy BlackBerry App Platform

**Version:** 2.0  
**Category:** System  
**Author:** SW7FT  
**Last Updated:** October 30, 2025

## Overview

BerryPy is a full-featured application manager designed specifically for BlackBerry devices running BB10/QNX systems. Manage, install, and monitor all your Python web applications from one beautiful, unified interface.

## Key Features

### 📱 Modern BlackBerry-Optimized UI
- **Dark Purple Theme**: Beautiful gradient interface with custom berry icon branding
- **Smooth Transitions**: Optimized section switching for seamless navigation
- **Responsive Design**: Perfect layout for BlackBerry Passport (1440x1440) and all BB10 devices
- **Browser Compatible**: Fully tested and optimized for BlackBerry WebKit browser

### 🎯 App Management
- **Three Main Sections**:
  - **Manage Apps**: Control running applications, view status, and access app URLs
  - **Installed Apps**: Browse locally installed applications with detailed info
  - **Available Apps**: Discover and install new apps from the BerryPy store

### 🖼️ Custom App Icons
BerryPy now features beautiful custom icons for apps:
- **AI-Chat** (aichat.png) - Purple AI assistant icon
- **BB10Git** (github.png) - Git repository manager icon
- **copyclip** (copyclip.png) - Clipboard utility icon
- **RocketChat** (rocketchat.png) - Chat application icon
- **Telegram** (telegram.png) - Messaging app icon
- **Term49-Settings** (term49-settings.png) - Terminal configuration icon
- **Webshell** (webshell.png) - Web terminal icon
- **YouTube** (youtube.png) - Video player icon

All app icons are 48x48px PNG files optimized for BlackBerry displays.

### 📋 Centralized Catalog System
- **catalog.json**: Single source of truth for all app metadata
- **Rich Metadata**: Name, description, category, version, author, and icons
- **Dependency Display**: Python requirements shown with pip install commands
- **Easy Maintenance**: Update one file to refresh all app information

### 🏠 Home Screen Icon Support
All web apps now support "Add to Home Screen" with custom icons:
- Full URL icon paths for BlackBerry browser compatibility
- Theme colors optimized for each app
- Web app manifest support for standalone mode

### ⚙️ Device Settings
Access comprehensive device configuration:
- **Auto-Start Configuration**: Set apps to launch automatically on boot
- **Port Management**: View and configure application ports
- **System Information**: Monitor device status and resources

### 🔧 Developer Features
- **Process Detection**: Automatic detection of running apps using `pidin`
- **Smart Port Discovery**: Detects ports from both `PORT = XXXX` and `app.run(port=XXXX)` patterns
- **Caching System**: Performance-optimized with intelligent cache management
- **Lazy Loading**: Fast app browsing with on-demand content loading

## Installation

1. Download `taskapp.zip` from the BerryPy store
2. Install using the app manager or manually extract to your apps directory
3. Run: `python3 taskapp.py`
4. Access the interface at: `http://127.0.0.1:49000`
5. Bookmark or add to home screen for quick access

## Requirements

- **Python 3.6+** (BB10/QNX Python 3.11+ recommended)
- **Flask** (for web interface)
- **BlackBerry BB10/QNX device** or compatible system
- **Working internet connection** (for app store features)

## File Structure

```
taskapp/
├── taskapp.py              # Main application server
├── taskmgr.html           # Primary UI interface
├── auto-config.html       # Device configuration page
├── app-icons/             # Custom app icons directory
│   ├── aichat.png
│   ├── github.png
│   ├── copyclip.png
│   ├── rocketchat.png
│   ├── telegram.png
│   ├── term49-settings.png
│   ├── webshell.png
│   ├── youtube.png
│   └── README.txt
└── news.json              # News and updates feed
```

## Recent Updates (v2.0)

### Visual Enhancements
- ✅ Purple berry icon (🫐) added to header
- ✅ "BerryPy" branding with bold typography
- ✅ Dark purple theme (#9b59b6) throughout interface
- ✅ Header background changed to #111 for better contrast
- ✅ App cards now use #111 background with #222 borders
- ✅ Hamburger menu icon (☰) replaces phone icon
- ✅ Device Settings (⚙️) menu with gear icon

### Functionality Improvements
- ✅ Removed "Start" and "Delete" buttons from Installed Apps tab
- ✅ Enhanced port detection for BB10Git and other apps
- ✅ Implemented catalog.json system for app metadata
- ✅ Added Python dependency requirements display
- ✅ Custom app icons with fallback to first letter
- ✅ Home screen icon support for all web apps
- ✅ Streamlined menu (removed Ports, About, News links)
- ✅ Smoother section transitions (removed bounce effect)

### Bug Fixes
- ✅ Fixed icon overwriting issue (removed setAllAppIcons timer)
- ✅ Fixed BB10Git startup (improved port detection)
- ✅ Fixed icon display with full URL paths
- ✅ Corrected BlackBerry spelling throughout

## Navigation

**Main Sections:**
1. **Manage Apps** - Control and monitor running applications
2. **Installed Apps** - View installed applications with details
3. **Available Apps** - Browse and install new applications

**Menu (☰ Device Settings):**
- Auto-Start Config - Configure automatic app startup
- Task Manager - Return to main interface

## Color Palette

- **Primary Purple**: #9b59b6 (berry purple)
- **Dark Background**: #111 (header/cards)
- **Border**: #222 (app card borders)
- **Hover**: #444 (interactive elements)
- **Text**: #e0e0e0 (primary text)
- **Gradient**: Linear gradients from #9b59b6 to #b37cc7

## Browser Compatibility

Fully tested and optimized for:
- ✅ BlackBerry 10 Browser (WebKit-based)
- ✅ BlackBerry Passport (1440x1440)
- ✅ BlackBerry Classic
- ✅ BlackBerry Z30
- ✅ All BB10 devices

## Performance

- **Fast Loading**: Lazy loading and caching for instant response
- **Efficient**: Minimal resource usage (~10-20MB RAM)
- **Responsive**: Debounced search with real-time filtering
- **Reliable**: Automatic error handling and recovery

## Support

For issues, updates, or feature requests:
- Visit the BerryPy store at berrystore.sw7ft.com
- Check the news feed for updates
- Report issues through the Device Settings menu

## License

Developed by SW7FT for the BlackBerry community.

---

**Made with 💜 for BlackBerry users everywhere**

