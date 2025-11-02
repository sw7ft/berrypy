# Contributing to BerryPy

Thank you for your interest in contributing to BerryPy!

---

## 🤝 How to Contribute

### Reporting Bugs

1. Check [Issues](https://github.com/sw7ft/BerryPy/issues) for duplicates
2. Create new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - BB10 device info
   - Logs from `berrypy logs`

### Suggesting Features

1. Check [Issues](https://github.com/sw7ft/BerryPy/issues) for similar requests
2. Create issue tagged `enhancement`
3. Describe the problem and proposed solution

### Pull Requests

1. Fork the repository
2. Create feature branch
3. Make your changes
4. **Test on actual BB10 device**
5. Submit pull request

---

## 🔧 Development Setup

### Prerequisites

- BlackBerry BB10/QNX device for testing
- Python 3.11+ on dev machine
- Git

### Building

```bash
./build-port.sh
```

Creates `web-berrypy-2.0.zip`

---

## ⚠️ BB10/QNX Critical Rules

### 1. Process Detection

❌ **WRONG:**
```bash
if ps -p "$PID" > /dev/null 2>&1; then
```

✅ **CORRECT:**
```bash
if pidin -p "$PID" > /dev/null 2>&1; then
```

**Why:** QNX uses `pidin` not `ps`. Using `ps` gives false negatives!

### 2. Shell Shebang

❌ **WRONG:**
```bash
#!/bin/bash
```

✅ **CORRECT:**
```bash
#!/bin/sh
```

**Why:** BB10 doesn't have bash at `/bin/bash`

### 3. POSIX Shell Only

Avoid bash-specific syntax:
- Use `[ ]` not `[[ ]]`
- Use `=` not `==` for strings
- No arrays
- No `${var,,}` lowercase

See [docs/QNX-COMPATIBILITY.md](docs/QNX-COMPATIBILITY.md) for details.

---

## 🧪 Testing Checklist

Before submitting PR:

- [ ] `./build-port.sh` succeeds
- [ ] Package is ~80KB
- [ ] Uses `#!/bin/sh` shebang
- [ ] Uses `pidin` for process detection
- [ ] Web interface loads on BB10
- [ ] Start/stop works
- [ ] No dev files in package
- [ ] **Tested on actual BB10 device**

---

## 📝 Code Guidelines

### Shell Scripts

- Must use `#!/bin/sh`
- Must use `pidin -p` not `ps -p`
- POSIX-compliant only
- Add comments for QNX-specific code

### Python

- Python 3.11+ compatible
- Follow PEP 8
- Handle errors gracefully

### JavaScript

- ES5-compatible (no arrow functions)
- Support BB10 WebKit browser
- Mobile-first responsive

---

## 📦 Packaging

### Before Building

Remove dev files:
```bash
rm -f taskapp/*.log
rm -f taskapp/*.bak
rm -f taskapp/taskmgr.html.*
rm -f taskapp/oldmgr.html
```

### Building

```bash
./build-port.sh
```

### Verifying

```bash
# Check size
ls -lh web-berrypy-2.0.zip

# Check for dev files
unzip -l web-berrypy-2.0.zip | grep -E "(\.log|\.bak|old)"
# Should return nothing

# Check shebang
unzip -p web-berrypy-2.0.zip bin/berrypy | head -1
# Should show: #!/bin/sh
```

---

## 🎯 Areas for Contribution

- [ ] Add update feature for installed apps
- [ ] Enhanced search and filtering
- [ ] App ratings/reviews
- [ ] Dark/light theme toggle
- [ ] Additional app icons
- [ ] Performance improvements
- [ ] Bug fixes
- [ ] Documentation improvements

---

## 💬 Communication

- **GitHub Issues:** Bug reports and features
- **GitHub Discussions:** General questions
- **Pull Requests:** Code contributions

---

## 📋 Commit Messages

Format:
```
<type>: <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
fix: Use pidin instead of ps for QNX process detection

BB10/QNX doesn't support ps -p. Changed all process detection
to use pidin -p which is QNX-native.

Fixes #123
```

---

## 🔍 Getting Help

- Read [docs/QNX-COMPATIBILITY.md](docs/QNX-COMPATIBILITY.md)
- Check existing issues
- Ask in GitHub Discussions

---

**Made with 💜 for BlackBerry developers**
