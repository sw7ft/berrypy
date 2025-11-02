# BerryPy Changelog

All notable changes to this project will be documented in this file.

---

## [2.0.0] - 2025-11-02

### 🎉 Major Release: BerryCore Integration

This release transforms BerryPy into a native BerryCore port, making installation and management seamless with the `qpkg` package manager.

### Added

#### BerryCore Port System
- ✅ **New `build-port.sh` script** - Automated port package builder
- ✅ **Proper port structure** - Follows BerryCore standards (bin/, share/, doc/)
- ✅ **INDEX entry** - Ready for BerryCore repository integration
- ✅ **`berrypy` launcher command** - Clean command-line interface

#### Launcher Features
- `berrypy start` - Start the BerryPy server
- `berrypy stop` - Stop the server gracefully
- `berrypy restart` - Restart the server
- `berrypy status` - Check if running
- `berrypy logs` - View recent logs
- `berrypy url` - Show access URL
- `berrypy help` - Display help information

#### Documentation
- ✅ **BERRYCORE-INTEGRATION.md** - Comprehensive integration guide
- ✅ **README.md** - Complete project documentation
- ✅ **INSTALL.md** - Detailed installation instructions
- ✅ **CHANGELOG.md** - This file

### Changed

#### Installation Method
- **Old:** Manual installation via `old-setup.sh` to `~/apps/taskapp/`
- **New:** Clean qpkg installation to `$NATIVE_TOOLS/share/berrypy/`

#### Management
- **Old:** Direct `python3 taskapp.py` execution
- **New:** Managed via `berrypy` command with proper PID tracking

#### Environment
- **Old:** Manual `.profile` modification with hard-coded paths
- **New:** Automatic via BerryCore environment system

### Improved

#### Process Management
- ✅ PID file tracking (`berrypy.pid`)
- ✅ Graceful shutdown with timeout
- ✅ Force kill if process doesn't stop
- ✅ Stale PID file cleanup

#### Logging
- ✅ Centralized log file (`berrypy.log`)
- ✅ Log viewing via `berrypy logs` command
- ✅ Log rotation (handled by system)

#### Paths
- ✅ Standard BerryCore directory structure
- ✅ Uses `$NATIVE_TOOLS` environment variable
- ✅ No hard-coded paths in scripts

### Migration

Users upgrading from v1.0 should:

1. Stop the old installation:
   ```bash
   pkill -f taskapp.py
   ```

2. Remove old files:
   ```bash
   rm -rf ~/apps/taskapp/
   ```

3. Clean up `.profile` (remove old auto-start lines)

4. Install new version:
   ```bash
   qpkg install berrypy
   berrypy start
   ```

### Port Package Details

- **Package Name:** `web-berrypy-2.0.zip`
- **Category:** `web`
- **Size:** 112K (compressed)
- **Files:** 29 files total
  - 1 launcher script (`bin/berrypy`)
  - 3 documentation files
  - 25 application files (including 8 icons)

### INDEX Entry

```
berrypy|web|2.0|112K|BlackBerry App Platform - Full-featured application manager
```

---

## [1.0.0] - 2024-07-09

### Initial Release

#### Features
- Web-based application manager
- App installation from BerryPy store
- Start/stop app management
- Auto-start configuration
- Purple berry theme
- Custom app icons (8 apps)
- Process detection via pidin
- Port detection
- Search and filtering

#### Installation
- Standalone installation via `old-setup.sh`
- Installs to `~/apps/taskapp/`
- Modifies `.profile` for auto-start
- Manual Python and pip installation

#### Technical Details
- Python 3.11+ backend with Flask
- ES5-compatible JavaScript frontend
- Dark purple theme (#9b59b6)
- Optimized for BlackBerry Passport (1440x1440)
- Port 8001 (default)

---

## Version Comparison

| Feature | v1.0 (Legacy) | v2.0 (BerryCore) |
|---------|---------------|------------------|
| **Installation** | `./old-setup.sh` | `qpkg install berrypy` |
| **Location** | `~/apps/taskapp/` | `$NATIVE_TOOLS/share/berrypy/` |
| **Launcher** | `python3 taskapp.py` | `berrypy start` |
| **Updates** | Manual re-install | `qpkg update berrypy` |
| **Removal** | `rm -rf ~/apps/taskapp/` | `qpkg remove berrypy` |
| **Management** | Manual process control | Built-in commands |
| **Logging** | `taskapp.log` in app dir | Centralized logging |
| **Auto-start** | Hard-coded .profile edit | Optional .profile line |
| **Dependencies** | Manual pip install | Automatic via qpkg |

---

## Future Roadmap

### Planned for v2.1
- [ ] Enhanced app catalog with ratings
- [ ] App update notifications
- [ ] Backup and restore configuration
- [ ] Multi-language support
- [ ] Dark/light theme toggle

### Planned for v2.2
- [ ] Remote device management
- [ ] App statistics and analytics
- [ ] Custom app repositories
- [ ] Plugin system
- [ ] API for third-party integration

### Planned for v3.0
- [ ] Complete UI redesign
- [ ] React/Vue frontend (compiled to ES5)
- [ ] WebSocket support for real-time updates
- [ ] Database backend for better performance
- [ ] Multi-user support

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## Links

- **GitHub:** https://github.com/sw7ft/BerryPy
- **BerryCore:** https://github.com/sw7ft/BerryCore
- **Store:** https://berrystore.sw7ft.com

---

**Made with 💜 for BlackBerry users everywhere**


