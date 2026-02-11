# 🔧 NSIS TAR Installer Workflow

This project builds a secure NSIS-based installer (`package.exe`) that:

- Bundles additional files from `extra/`
- Verifies the SHA256 signature of an external `.tar` archive
- Extracts the `.tar` content to the install directory
- Cleans up all temporary traces after verification or failure

---

## ⚙️ How It Works

### 🧱 Batch Scripts

- **`build_package.bat`**
  - Removes previous `out/` folder (if any)
  - Calls:
    - `create_tar.bat` → builds `.tar` + `.sig` into `out/source`
    - `create_package.bat` → builds installer
    - `copy_sources.bat` → moves `.tar` and `.sig` to `out/bin`

- **`create_tar.bat`**
  - Uses Windows `tar` to create `payload.tar` from the `payload/` folder
  - Hashes the tar using `certutil` and stores result in `payload.sig` (single 64-char line)

- **`create_package.bat`**
  - Runs `makensis.exe` with `installer.nsi`

- **`copy_sources.bat`**
  - Moves `.tar` and `.sig` from `out/source/` to `out/bin/` for deployment

---

### ✅ Requirements

- **Windows 10/11+** for `tar.exe` and `certutil`)
- **NSIS** [Download](https://sourceforge.net/projects/nsisbi/)
- installed at:  `C:\Program Files\NSIS`
- add path to .exe into PATH

---

### 🧪 Verification Flow

1. `certutil` generates a fresh hash from the `.tar`
2. That hash is compared against the embedded `.sig`
3. If they differ, installation is immediately aborted
4. If they match, `.tar` is extracted using native `tar`

---

### 📁 Folder Structure

```text
project_root/
├── build_package.bat       # Orchestrates full build process
├── create_tar.bat          # Creates payload.tar + payload.sig in out/source
├── create_package.bat      # Builds package.exe via NSIS from nsis/installer.nsi
├── copy_sources.bat        # Copies payload.tar + payload.sig to out/bin
│
├── nsis/
│   └── installer.nsi       # NSIS script: verifies, installs, allows dir selection
│
├── payload/                # Source files to be tarred into payload.tar
├── extra/                  # Extra files to be embedded into installer
│
└── out/
    ├── source/             # Intermediate step (outputs from create_tar.bat)
    │   ├── payload.tar     # Generated tarball from payload/
    │   └── payload.sig     # SHA256 signature of the .tar
    │
    └── bin/                # Final deployment output
        ├── package.exe     # NSIS-built installer
        ├── payload.tar     # Copied from source (external reference)
        └── payload.sig     # Copied from source (external reference)
```
