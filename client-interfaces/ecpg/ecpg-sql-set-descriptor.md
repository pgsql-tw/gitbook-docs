## SET DESCRIPTOR

SET DESCRIPTOR — 在 SQL 描述區設定資訊

## 語法

```

SET DESCRIPTOR descriptor_name descriptor_header_item = value
SET DESCRIPTOR descriptor_name VALUE number descriptor_item = value [, ...]
```

<a id="id-1.7.5.20.16.3"></a>

## 說明

`SET DESCRIPTOR` 使用值填入 SQL 描述區。描述區通常隨後用於在執行備妥查詢時繫結參數。

此命令有兩種形式：第一種套用至與特定資料值無關的描述區「標頭」；第二種則為以編號識別的特定資料值指派值。

<a id="id-1.7.5.20.16.4"></a>

## 參數

<a id="ECPG-SQL-SET-DESCRIPTOR-DESCRIPTOR-NAME"></a>

*`descriptor_name`* [#](#ECPG-SQL-SET-DESCRIPTOR-DESCRIPTOR-NAME)
:   描述區名稱。
<a id="ECPG-SQL-SET-DESCRIPTOR-DESCRIPTOR-HEADER-ITEM"></a>

*`descriptor_header_item`* [#](#ECPG-SQL-SET-DESCRIPTOR-DESCRIPTOR-HEADER-ITEM)
:   用來識別要設定哪個標頭資訊項目的符記。目前只支援用於設定描述區項目數量的 `COUNT`。
<a id="ECPG-SQL-SET-DESCRIPTOR-NUMBER"></a>

*`number`* [#](#ECPG-SQL-SET-DESCRIPTOR-NUMBER)
:   要設定的描述區項目編號。計數從 1 開始。
<a id="ECPG-SQL-SET-DESCRIPTOR-DESCRIPTOR-ITEM"></a>

*`descriptor_item`* [#](#ECPG-SQL-SET-DESCRIPTOR-DESCRIPTOR-ITEM)
:   用來識別要在描述區中設定哪個資訊項目的符記。支援項目清單請參閱[第 34.7.1 節](ecpg-descriptors.md#ECPG-NAMED-DESCRIPTORS)。
<a id="ECPG-SQL-SET-DESCRIPTOR-VALUE"></a>

*`value`* [#](#ECPG-SQL-SET-DESCRIPTOR-VALUE)
:   要儲存至描述區項目的值。可以是 SQL 常數或主機變數。

<a id="id-1.7.5.20.16.5"></a>

## 範例

```

EXEC SQL SET DESCRIPTOR indesc COUNT = 1;
EXEC SQL SET DESCRIPTOR indesc VALUE 1 DATA = 2;
EXEC SQL SET DESCRIPTOR indesc VALUE 1 DATA = :val1;
EXEC SQL SET DESCRIPTOR indesc VALUE 2 INDICATOR = :val1, DATA = 'some string';
EXEC SQL SET DESCRIPTOR indesc VALUE 2 INDICATOR = :val2null, DATA = :val2;
```

<a id="id-1.7.5.20.16.6"></a>

## 相容性

SQL 標準規定了 `SET DESCRIPTOR`。

<a id="id-1.7.5.20.16.7"></a>

## 另請參閱

[ALLOCATE DESCRIPTOR](ecpg-sql-allocate-descriptor.md), [GET DESCRIPTOR](ecpg-sql-get-descriptor.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-set-descriptor.html)（英文原文，待翻譯）
