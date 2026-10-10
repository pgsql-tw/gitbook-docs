<a id="INSTALLATION"></a>

## 第 17 章 從原始碼安裝

**目錄**

[17.1. 需求](install-requirements.md)

[17.2. 取得原始碼](install-getsource.md)

[17.3. 以 Autoconf 與 Make 建置與安裝](install-make.md)
:   [17.3.1. 精簡版](install-make.md#INSTALL-SHORT-MAKE)

    [17.3.2. 安裝程序](install-make.md#INSTALL-PROCEDURE-MAKE)

    [17.3.3. `configure` 選項](install-make.md#CONFIGURE-OPTIONS)

    [17.3.4. `configure` 環境變數](install-make.md#CONFIGURE-ENVVARS)

[17.4. 使用 Meson 建置與安裝](install-meson.md)
:   [17.4.1. 簡短版本](install-meson.md#INSTALL-SHORT-MESON)

    [17.4.2. 安裝程序](install-meson.md#INSTALL-PROCEDURE-MESON)

    [17.4.3. `meson setup` 選項](install-meson.md#MESON-OPTIONS)

    [17.4.4. `meson` 建置目標](install-meson.md#TARGETS-MESON)

[17.5. 安裝後設定](install-post.md)
:   [17.5.1. 共用函式庫](install-post.md#INSTALL-POST-SHLIBS)

    [17.5.2. 環境變數](install-post.md#INSTALL-POST-ENV-VARS)

[17.6. 受支援的平台](supported-platforms.md)

[17.7. 特定平台注意事項](installation-platform-notes.md)
:   [17.7.1. Cygwin](installation-platform-notes.md#INSTALLATION-NOTES-CYGWIN)

    [17.7.2. macOS](installation-platform-notes.md#INSTALLATION-NOTES-MACOS)

    [17.7.3. MinGW](installation-platform-notes.md#INSTALLATION-NOTES-MINGW)

    [17.7.4. Solaris](installation-platform-notes.md#INSTALLATION-NOTES-SOLARIS)

    [17.7.5. Visual Studio](installation-platform-notes.md#INSTALLATION-NOTES-VISUAL-STUDIO)

<a id="id-1.6.4.2"></a>

本章說明如何使用原始碼發行版安裝
PostgreSQL。如果你要安裝的是預先封裝好的發行版，
例如 RPM 或 Debian 套件，請略過本章，
改為參閱[第 16 章](../install-binaries/README.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/installation.html)（原文版本：18.6；核對日期：2026-10-10）
