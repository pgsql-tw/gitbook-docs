# 18. 以原始碼在 Windows 上安裝

It is recommended that most users download the binary distribution for Windows, available as a graphical installer package from the PostgreSQL website at [https://www.postgresql.org/download/](https://www.postgresql.org/download/). Building from source is only intended for people developing PostgreSQL or extensions.

There are several different ways of building PostgreSQL on Windows. The simplest way to build with Microsoft tools is to install Visual Studio 2022 and use the included compiler. It is also possible to build with the full Microsoft Visual C++ 2013 to 2022. In some cases that requires the installation of the Windows SDK in addition to the compiler.

It is also possible to build PostgreSQL using the GNU compiler tools provided by MinGW, or using Cygwin for older versions of Windows.

使用 MinGW 或 Cygwin 的話，請以標準方式建置系統，參閱[第 17 章](../installation-from-source-code/)[第 17.7.4 節](../installation-from-source-code/platform-specific-notes.md#17.7.4.-mingw-native-windows)和[第 17.7.2 節](../installation-from-source-code/platform-specific-notes.md#17.7.2.-cygwin)的特定說明。 要在這些環境中產生原生 64 位元的編輯執行檔，請使用 MinGW-w64 的工具。 這些工具還可用於在其他主機（例如 Linux 和 macOS）上交叉編譯 32 位元和 64 位元 Windows 標的。 但不建議將 Cygwin 用於運作正式線上伺服器，它應該只用於在無法建置的舊版本 Windows 上。 官方預編譯安裝套件是使用 Visual Studio 編譯的。

Native builds of psql don't support command line editing. The Cygwin build does support command line editing, so it should be used where psql is needed for interactive use on Windows.
