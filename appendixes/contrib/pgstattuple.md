<a id="PGSTATTUPLE"></a>

## F.33. pgstattuple — 取得元組層級的統計資訊 [#](#pgstattuple) <a href="#pgstattuple" id="pgstattuple"></a>

[F.33.1. 函式](pgstattuple/pgstattuple-funcs.md#pgstattuple-funcs)

[F.33.2. 作者](pgstattuple.md#pgstattuple-authors)

<a id="id-1.11.7.43.2"></a>

`pgstattuple` 模組提供多種函式，用來取得元組（tuple）層級的統計資訊。

由於這些函式會傳回詳細的頁面層級資訊，預設會限制存取。預設情況下，只有
`pg_stat_scan_tables` 角色具有 `EXECUTE`
權限。超級使用者當然不受此限制。安裝擴充功能之後，使用者可以執行 `GRANT`
命令變更這些函式的權限，讓其他人也能執行它們。不過，改為將這些使用者加入
`pg_stat_scan_tables` 角色可能是較好的做法。

### F.33.1. 函式 [#](#pgstattuple-funcs) <a href="#pgstattuple-funcs" id="pgstattuple-funcs"></a>

完整內容請見 [F.33.1. 函式](pgstattuple/pgstattuple-funcs.md#pgstattuple-funcs)。

<a id="PGSTATTUPLE-AUTHORS"></a>

### F.33.2. 作者 [#](#pgstattuple-authors) <a href="#pgstattuple-authors" id="pgstattuple-authors"></a>

Tatsuo Ishii、Satoshi Nagayasu 與 Abhijit Menon-Sen

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgstattuple.html)（原文版本：18.6；核對日期：2026-10-23）
