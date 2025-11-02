# QNX/BB10 Compatibility Guide

Critical information for developing BerryPy and other BB10/QNX applications.

---

## ⚠️ **Critical Differences from Linux**

### 1. Process Detection

#### ❌ **LINUX/MACOS (WRONG for BB10):**
```bash
ps -p $PID > /dev/null 2>&1
```

#### ✅ **QNX/BB10 (CORRECT):**
```bash
pidin -p $PID > /dev/null 2>&1
```

**Why:** QNX uses `pidin` (Process Information Display) instead of `ps`. Using `ps -p` will cause false negatives - it will report a process as not running when it actually is!

**All 5 locations in berrypy launcher:**
1. Check if already running (start function)
2. Verify startup success (start function)
3. Check before stopping (stop function)
4. Wait for shutdown loop (stop function)
5. Status check (status function)

---

### 2. Shell Shebang

#### ❌ **COMMON (WRONG for BB10):**
```bash
#!/bin/bash
```

#### ✅ **BB10 (CORRECT):**
```bash
#!/bin/sh
```

**Why:** BB10/QNX doesn't have bash installed at `/bin/bash`. Use POSIX-compliant `/bin/sh` instead.

**Impact:** Scripts with `#!/bin/bash` will fail with "No such file or directory" error.

---

### 3. POSIX Shell Compliance

When using `#!/bin/sh`, avoid bash-isms:

#### ❌ **Bash-specific (AVOID):**
```bash
[[ $var == "value" ]]           # Use [ ] instead
${var,,}                        # Lowercase not in POSIX
${var^^}                        # Uppercase not in POSIX
array=(1 2 3)                   # Arrays not in POSIX
function name() { }             # Use name() { } only
```

#### ✅ **POSIX-compliant (USE):**
```bash
[ "$var" = "value" ]            # Single bracket, single =
echo "$var" | tr 'A-Z' 'a-z'    # External command for case
space_separated="1 2 3"         # Use strings instead of arrays
name() { }                      # POSIX function syntax
```

---

### 4. QNX-Specific Commands

| Task | Linux | QNX/BB10 |
|------|-------|----------|
| **Process info** | `ps -p PID` | `pidin -p PID` |
| **All processes** | `ps aux` | `pidin ar` |
| **Process tree** | `pstree` | `pidin tree` |
| **Memory info** | `free` | `pidin info` |
| **Network** | `netstat -an` | `netstat -an` (same) |
| **Kill process** | `kill PID` | `slay PID` or `kill PID` |

---

### 5. File Paths

```bash
# BerryCore installation
$NATIVE_TOOLS=/accounts/1000/shared/misc

# User home (Terminal49)
~/  = /accounts/1000/appdata/com.update.Term49.*/data/

# Python location
which python3
# /accounts/1000/shared/misc/bin/python3
```

---

## 🔍 **Testing on Device**

### Essential Commands

```bash
# Check BerryCore environment
echo $NATIVE_TOOLS
# Should show: /accounts/1000/shared/misc

# Check PATH
echo $PATH
# Should include: /accounts/1000/shared/misc/bin

# Verify Python
which python3
python3 --version
# Should show: Python 3.11.x

# Check process
pidin ar | grep python3
# Shows all Python processes

# Check port
netstat -an | grep 8001
# Shows port 8001 usage

# Check berrypy
which berrypy
# Should show: /accounts/1000/shared/misc/bin/berrypy

# Test berrypy
berrypy status
berrypy logs
```

---

## 📝 **Development Workflow**

### 1. Develop on Desktop
```bash
# Write code on macOS/Linux
vim build-port.sh

# Test locally (will work differently!)
./build-port.sh
```

### 2. Test on Device
```bash
# Copy to BB10 device
scp web-berrypy-2.0.zip device:/tmp/

# SSH to device
ssh device

# Install and test
cd $NATIVE_TOOLS
unzip -o /tmp/web-berrypy-2.0.zip
berrypy start

# Check if actually running
pidin ar | grep python3
berrypy status
```

### 3. Common Issues

**Issue:** Script fails with "No such file or directory"  
**Cause:** Using `#!/bin/bash`  
**Fix:** Change to `#!/bin/sh`

**Issue:** `berrypy status` says "Not running" but web interface works  
**Cause:** Using `ps -p` instead of `pidin -p`  
**Fix:** Replace all `ps -p` with `pidin -p`

**Issue:** Python not found  
**Cause:** BerryCore environment not loaded  
**Fix:** 
```bash
source /accounts/1000/shared/misc/berrycore/env.sh
# Or add to ~/.profile
```

**Issue:** Port 8001 already in use  
**Cause:** Stale BerryPy process  
**Fix:**
```bash
pidin ar | grep python3
# Find PID and kill it
slay <PID>
# Or use kill
kill <PID>
```

---

## 🧪 **Testing Checklist**

Before releasing any BB10/QNX software:

- [ ] Uses `#!/bin/sh` shebang
- [ ] Uses `pidin -p` for process detection
- [ ] No bash-specific syntax
- [ ] Tested on actual BB10 device
- [ ] Process start/stop works correctly
- [ ] Logs are created properly
- [ ] Error handling works
- [ ] Network functionality works
- [ ] File paths are correct
- [ ] Dependencies are available

---

## 📚 **Resources**

### QNX Documentation
- Process Manager: `use pidin`
- Man pages on device: `use <command>`
- QNX Neutrino RTOS

### BerryCore
- GitHub: https://github.com/sw7ft/BerryCore
- Environment: Source `$NATIVE_TOOLS/../berrycore/env.sh`

### BlackBerry 10
- Platform: ARMv7
- OS: QNX 8.0 (Neutrino)
- Browser: WebKit-based

---

## 💡 **Quick Reference Card**

Print this and keep it handy:

```
╔════════════════════════════════════════════════════╗
║        QNX/BB10 Compatibility Quick Reference      ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║  Shebang:      #!/bin/sh  (NOT #!/bin/bash)       ║
║  Process:      pidin -p   (NOT ps -p)             ║
║  Comparison:   [ "$a" = "$b" ]  (NOT ==)          ║
║  Root:         $NATIVE_TOOLS                       ║
║  Python:       $NATIVE_TOOLS/bin/python3           ║
║  Kill:         slay PID   (or kill PID)           ║
║                                                    ║
║  Test Process: pidin -p $PID >/dev/null 2>&1      ║
║  List All:     pidin ar                           ║
║  Check Port:   netstat -an | grep PORT            ║
║                                                    ║
║  ALWAYS TEST ON ACTUAL BB10 DEVICE!               ║
║                                                    ║
╚════════════════════════════════════════════════════╝
```

---

**Made with 💜 for BB10 developers**

