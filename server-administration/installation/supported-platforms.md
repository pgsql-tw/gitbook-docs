<a id="SUPPORTED-PLATFORMS"></a>

## 17.6. 受支援的平台 [#](#SUPPORTED-PLATFORMS)

一個平台（也就是 CPU 架構與作業系統的組合）如果程式碼中含有能在該平台上運作的支援措施，且最近曾驗證能在該平台上建置並通過回歸測試，就會被 PostgreSQL 開發社群視為受支援的平台。目前，平台相容性的大部分測試都是由
[PostgreSQL Build Farm](https://buildfarm.postgresql.org/) 的測試機器自動完成。
如果你有興趣在 Build Farm 中尚未出現的平台上使用 PostgreSQL，但該程式碼可以在該平台上運作或可以修改使其運作，強烈建議你架設一台 Build Farm 成員機器，以確保能持續獲得相容性保證。

一般而言，PostgreSQL 可預期能在以下 CPU 架構上運作：x86、PowerPC、S/390、SPARC、ARM、MIPS
以及 RISC-V，包含 big-endian、little-endian、32 位元與 64 位元等各種變體（視適用情況而定）。

PostgreSQL 可預期能在以下作業系統的目前版本上運作：Linux、Windows、
FreeBSD、OpenBSD、NetBSD、DragonFlyBSD、macOS、Solaris 以及 illumos。
其他類 Unix 系統也可能可以運作，但目前並未受到測試。在大多數情況下，
特定作業系統所支援的所有 CPU 架構都能運作。請參閱下方的
[第 17.7 節](installation-platform-notes.md)，
看看是否有針對你所使用作業系統的特定資訊，
尤其是在使用較舊系統的情況下。

如果你在依據近期 Build Farm 結果判斷應屬受支援的平台上遇到安裝問題，
請回報至 `<pgsql-bugs@lists.postgresql.org>`。如果你有興趣將 PostgreSQL 移植到新平台，
`<pgsql-hackers@lists.postgresql.org>` 是討論此事的適當場所。

PostgreSQL 或 POSTGRES 的歷史版本也曾在包含 Alpha、Itanium、M32R、M68K、
M88K、NS32K、PA-RISC、SuperH 以及 VAX 等 CPU 架構，
以及包含 4.3BSD、AIX、BEOS、
BSD/OS、DG/UX、Dynix、HP-UX、IRIX、NeXTSTEP、QNX、SCO、SINIX、Sprite、SunOS、
Tru64 UNIX 以及 ULTRIX 等作業系統上運作過。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/supported-platforms.html)（原文版本：18.6；核對日期：2026-09-26）
