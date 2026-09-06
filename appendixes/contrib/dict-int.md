## F.12. `dict_int` — 整數全文檢索字典範例 [#](#DICT-INT)

[F.12.1. 設定](dict-int.md#DICT-INT-CONFIG)

[F.12.2. 使用方式](dict-int.md#DICT-INT-USAGE)

<a id="id-1.11.7.22.2"></a>

`dict_int` 是全文檢索附加字典範本的範例。此範例字典的目的在於控制整數（帶正負號或不帶正負號）的索引方式，讓這類數字可被索引，同時避免不重複詞彙數量過度增加，因而嚴重影響搜尋效能。

此模組被視為「受信任」，也就是說，具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

<a id="DICT-INT-CONFIG"></a>

### F.12.1. 設定 [#](#DICT-INT-CONFIG)

此字典接受三個選項：

* `maxlen` 參數指定整數詞彙允許的最大位數。預設值為 6。
* `rejectlong` 參數指定是否應截斷或忽略超過長度的整數。若 `rejectlong` 為 `false`（預設值），字典會傳回整數的前 `maxlen` 位數；若 `rejectlong` 為 `true`，字典會將超過長度的整數視為停用詞，因此不會為其建立索引。請注意，這也表示無法搜尋這類整數。
* `absval` 參數指定是否應從整數詞彙移除開頭的「`+`」或「`-`」符號。預設值為 `false`。值為 `true` 時，會在套用 `maxlen` 前移除符號。

<a id="DICT-INT-USAGE"></a>

### F.12.2. 使用方式 [#](#DICT-INT-USAGE)

安裝 `dict_int` 擴充功能會以預設參數建立全文檢索範本 `intdict_template` 與基於該範本的字典 `intdict`。你可以變更這些參數，例如：

```

mydb# ALTER TEXT SEARCH DICTIONARY intdict (MAXLEN = 4, REJECTLONG = true);
ALTER TEXT SEARCH DICTIONARY
```

也可以基於該範本建立新的字典。

若要測試此字典，可以嘗試：

```

mydb# select ts_lexize('intdict', '12345678');
 ts_lexize
-----------
 {123456}
```

但實際使用時，會如[第 12 章](../../the-sql-language/textsearch/README.md)所述，將它納入全文檢索設定。範例如下：

```

ALTER TEXT SEARCH CONFIGURATION english
    ALTER MAPPING FOR int, uint WITH intdict;
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/dict-int.html)（原文版本：18.6；核對日期：2026-09-06）
