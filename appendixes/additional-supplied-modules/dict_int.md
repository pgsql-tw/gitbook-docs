<a id="DICT-INT"></a>

# F.13. dict_int

[F.13.1. 設定](#id-1.11.7.22.5)

[F.13.2. 使用方式](#id-1.11.7.22.6)

<a id="id-1.11.7.22.2"></a>

`dict_int` 是全文檢索附加字典樣板的範例。此範例字典的目的在於控制整數（有正負號及無正負號）的索引，使這些數字能建立索引，同時避免唯一詞彙數量過度增加；唯一詞彙數量會大幅影響搜尋效能。

此模組被視為「受信任」，也就是說，對目前資料庫具有 `CREATE` 權限的非超級使用者可以安裝它。

<a id="id-1.11.7.22.5"></a>

## F.13.1. 設定

此字典接受三個選項：

* `maxlen` 參數指定整數詞彙允許的最大位數。預設值為 6。
* `rejectlong` 參數指定是否應截斷或忽略超長整數。若 `rejectlong` 為 `false`（預設值），字典傳回整數的前 `maxlen` 位數。若 `rejectlong` 為 `true`，字典會將超長整數視為停用詞，因此不會為它建立索引。請注意，這也表示無法搜尋該整數。
* `absval` 參數指定是否應從整數詞彙移除前導「`+`」或「`-`」符號。預設值為 `false`。為 `true` 時，會先移除符號再套用 `maxlen`。

<a id="id-1.11.7.22.6"></a>

## F.13.2. 使用方式

安裝 `dict_int` 擴充功能會以預設參數建立文字搜尋樣板 `intdict_template`，以及以該樣板為基礎的字典 `intdict`。您可以變更參數，例如：

```

mydb# ALTER TEXT SEARCH DICTIONARY intdict (MAXLEN = 4, REJECTLONG = true);
ALTER TEXT SEARCH DICTIONARY
```

或者根據此樣板建立新的字典。

若要測試字典，您可以嘗試：

```

mydb# select ts_lexize('intdict', '12345678');
 ts_lexize
-----------
 {123456}
```

但實際使用時，會如[第 12 章](../../the-sql-language/12.-quan-wen-jian-suo/README.md)所述，將它加入文字搜尋設定。如下所示：

```

ALTER TEXT SEARCH CONFIGURATION english
    ALTER MAPPING FOR int, uint WITH intdict;
```

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/dict-int.html)
