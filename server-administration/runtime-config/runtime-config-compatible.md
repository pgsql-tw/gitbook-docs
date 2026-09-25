<a id="RUNTIME-CONFIG-COMPATIBLE"></a>

## 19.13. 版本與平台相容性 [#](#RUNTIME-CONFIG-COMPATIBLE)

[19.13.1. 舊版 PostgreSQL](runtime-config-compatible.md#RUNTIME-CONFIG-COMPATIBLE-VERSION)

[19.13.2. 平台與用戶端相容性](runtime-config-compatible.md#RUNTIME-CONFIG-COMPATIBLE-CLIENTS)

<a id="RUNTIME-CONFIG-COMPATIBLE-VERSION"></a>

### 19.13.1. 舊版 PostgreSQL [#](#RUNTIME-CONFIG-COMPATIBLE-VERSION)

<a id="GUC-ARRAY-NULLS"></a>

`array_nulls` (`boolean`) <a id="id-1.6.6.16.2.2.1.1.3"></a> [#](#GUC-ARRAY-NULLS)
:   這控制陣列輸入剖析器是否將未加引號的
    `NULL` 視為指定一個空值陣列元素。
    預設情況下此設定為 `on`，允許輸入含有空值的陣列值。
    然而，8.2 之前的 PostgreSQL 版本不支援陣列中的空值，
    因此會將 `NULL` 視為指定一個字串值為「NULL」的一般陣列元素。
    為了與需要舊行為的應用程式向後相容，可將此變數
    設為 `off`。

    請注意，即使此變數為 `off`，仍然可以建立含有空值的陣列值。
<a id="GUC-BACKSLASH-QUOTE"></a>

`backslash_quote` (`enum`) <a id="id-1.6.6.16.2.2.2.1.3"></a> <a id="id-1.6.6.16.2.2.2.1.4"></a> [#](#GUC-BACKSLASH-QUOTE)
:   這控制字串常值中是否可以用
    `\'` 表示引號。符合 SQL 標準、較建議的做法
    是將引號重複兩次（`''`）表示，但
    PostgreSQL 歷來也接受
    `\'` 的寫法。不過，使用 `\'` 會造成安全性風險，
    因為在某些用戶端字元集編碼中，存在最後一個位元組在數值上與
    ASCII `\` 相同的多位元組字元。如果用戶端程式碼未正確處理逸出，
    就可能發生 SQL 注入攻擊。可以讓伺服器拒絕引號看起來以反斜線逸出的查詢，
    以防止此風險。
    `backslash_quote` 允許的值有
    `on`（永遠允許 `\'`）、
    `off`（永遠拒絕），以及
    `safe_encoding`（僅在用戶端編碼不允許 ASCII
    `\` 出現在多位元組字元內時才允許）。
    `safe_encoding` 是預設設定。

    請注意，在符合標準的字串常值中，`\` 無論如何都僅代表
    `\` 本身。此參數只影響不符合標準字串常值的處理方式，
    包括逸出字串語法（`E'...'`）。
<a id="GUC-ESCAPE-STRING-WARNING"></a>

`escape_string_warning` (`boolean`) <a id="id-1.6.6.16.2.2.3.1.3"></a> <a id="id-1.6.6.16.2.2.3.1.4"></a> [#](#GUC-ESCAPE-STRING-WARNING)
:   當此設定為開啟時，如果一般字串常值（`'...'`
    語法）中出現反斜線（`\`），且
    `standard_conforming_strings` 為關閉，則會發出警告。
    預設值為 `on`。

    希望使用反斜線作為逸出字元的應用程式應改用逸出字串語法
    （`E'...'`），因為依照 SQL 標準，
    一般字串現在預設會將反斜線視為一般字元。
    可以啟用此變數，以協助找出需要修改的程式碼。
<a id="GUC-LO-COMPAT-PRIVILEGES"></a>

`lo_compat_privileges` (`boolean`) <a id="id-1.6.6.16.2.2.4.1.3"></a> [#](#GUC-LO-COMPAT-PRIVILEGES)
:   在 9.0 之前的 PostgreSQL 版本中，大型物件（large object）
    沒有存取權限，因此所有使用者永遠都可以讀取與寫入。
    將此變數設為 `on` 會停用新的權限檢查，
    以與舊版相容。預設值為 `off`。
    只有超級使用者以及具備相應 `SET`
    權限的使用者可以變更此設定。

    設定此變數並不會停用所有與大型物件相關的安全性檢查——
    僅停用那些在 PostgreSQL 9.0 中預設行為有所變更的檢查。
<a id="GUC-QUOTE-ALL-IDENTIFIERS"></a>

`quote_all_identifiers` (`boolean`) <a id="id-1.6.6.16.2.2.5.1.3"></a> [#](#GUC-QUOTE-ALL-IDENTIFIERS)
:   當資料庫產生 SQL 時，強制為所有識別字加上引號，
    即使它們（目前）並非關鍵字。這將影響
    `EXPLAIN` 的輸出，以及
    `pg_get_viewdef` 等函式的結果。另請參閱
    [pg_dump](../../reference/reference-client/app-pgdump.md) 與 [pg_dumpall](../../reference/reference-client/app-pg-dumpall.md) 的
    `--quote-all-identifiers` 選項。
<a id="GUC-STANDARD-CONFORMING-STRINGS"></a>

`standard_conforming_strings` (`boolean`) <a id="id-1.6.6.16.2.2.6.1.3"></a> <a id="id-1.6.6.16.2.2.6.1.4"></a> [#](#GUC-STANDARD-CONFORMING-STRINGS)
:   這控制一般字串常值（`'...'`）是否依照
    SQL 標準所述，將反斜線視為一般字元處理。
    自 PostgreSQL 9.1 起，預設值為
    `on`（先前版本預設為 `off`）。
    應用程式可以檢查此
    參數，以判斷字串常值將如何處理。
    此參數的存在也可視為支援逸出字串語法
    （`E'...'`）的指標。
    如果應用程式希望將反斜線視為逸出字元，
    則應使用逸出字串語法（[4.1.2.2 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS-ESCAPE)）。
<a id="GUC-SYNCHRONIZE-SEQSCANS"></a>

`synchronize_seqscans` (`boolean`) <a id="id-1.6.6.16.2.2.7.1.3"></a> [#](#GUC-SYNCHRONIZE-SEQSCANS)
:   這允許大型資料表的循序掃描（sequential scan）彼此同步，
    使並行的掃描大約在同一時間讀取同一個區塊，
    藉此共享 I/O 工作負載。啟用此功能後，
    某次掃描可能會從資料表中間開始，掃描到資料表結尾後會繞回開頭
    繼續，以涵蓋所有資料列，藉此與已在進行中的掃描活動同步。
    對於沒有 `ORDER BY` 子句的查詢，這可能導致
    傳回的資料列順序出現不可預期的變化。將此參數設為
    `off` 可確保恢復 8.3 之前的行為，即循序掃描
    永遠從資料表開頭開始。預設值
    為 `on`。

<a id="RUNTIME-CONFIG-COMPATIBLE-CLIENTS"></a>

### 19.13.2. 平台與用戶端相容性 [#](#RUNTIME-CONFIG-COMPATIBLE-CLIENTS)

<a id="GUC-TRANSFORM-NULL-EQUALS"></a>

`transform_null_equals` (`boolean`) <a id="id-1.6.6.16.3.2.1.1.3"></a> <a id="id-1.6.6.16.3.2.1.1.4"></a> [#](#GUC-TRANSFORM-NULL-EQUALS)
:   當此設定為開啟時，形式為 `expr =
    NULL`（或 `NULL =
    expr`）的運算式會被視為
    `expr IS NULL` 處理，也就是說，若
    *`expr`* 的求值結果為空值，則傳回真，
    否則傳回假。符合 SQL 規範、正確的
    `expr = NULL` 行為應該永遠
    傳回空值（未知）。因此此參數預設為
    `off`。

    不過，Microsoft
    Access 中的篩選表單所產生的查詢，看起來會使用
    `expr = NULL` 來測試
    空值，因此如果你使用該介面存取資料庫，
    可能會想要開啟此選項。由於形式為
    `expr = NULL` 的運算式（依照
    SQL 標準的解讀）永遠傳回空值，因此它們並不是
    很有用，在一般應用程式中也不常出現，所以
    此選項在實務上幾乎無害。但新使用者
    經常對涉及空值的運算式語意感到困惑，
    因此此選項預設為關閉。

    請注意，此選項只影響 `= NULL` 這種精確形式，
    不影響其他比較運算子，也不影響在計算上
    等效於某個涉及等號運算子之運算式的其他運算式
    （例如 `IN`）。
    因此，此選項並非解決不良程式撰寫方式的通用方法。

    相關資訊請參閱[9.2 節](../../the-sql-language/functions/functions-comparison.md)。
<a id="GUC-ALLOW-ALTER-SYSTEM"></a>

`allow_alter_system` (`boolean`) <a id="id-1.6.6.16.3.2.2.1.3"></a> [#](#GUC-ALLOW-ALTER-SYSTEM)
:   當 `allow_alter_system` 設為
    `off` 時，若執行 `ALTER
    SYSTEM` 命令，會傳回錯誤。此參數只能在
    `postgresql.conf` 檔案中或伺服器命令
    列上設定。預設值為 `on`。

    請注意，不應將此設定視為安全性功能。它
    只會停用 `ALTER SYSTEM` 命令，並不會
    阻止超級使用者透過其他 SQL 命令變更組態設定。
    超級使用者有許多方式可以在作業系統層級執行 shell 命令，
    因此無論此設定值為何，都能
    修改 `postgresql.auto.conf`。

    關閉此設定，是為了因應某些外部工具負責管理
    PostgreSQL 組態設定的環境而設計的。
    在這類環境中，善意的超級使用者可能會
    *誤用* `ALTER SYSTEM`
    來變更組態設定，而不是使用該外部工具。
    這可能導致非預期的行為，例如當外部工具日後
    更新組態設定時，會覆寫此變更。
    將此參數設為 `off` 可以
    協助避免此類錯誤。

    此參數僅控制 `ALTER SYSTEM` 的使用。
    即使 `allow_alter_system` 設為
    `off`，儲存在 `postgresql.auto.conf`
    中的設定仍會生效。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/runtime-config-compatible.html)（原文版本：18.6；核對日期：2026-09-25）
