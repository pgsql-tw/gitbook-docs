<a id="ECPG-SQL-GET-DESCRIPTOR"></a>

## GET DESCRIPTOR

GET DESCRIPTOR — 從 SQL 描述區取得資訊

## 語法

```

GET DESCRIPTOR descriptor_name :cvariable = descriptor_header_item
GET DESCRIPTOR descriptor_name VALUE column_number :cvariable = descriptor_item [, ... ]
```

<a id="id-1.7.5.20.11.3"></a>

## 說明

`GET DESCRIPTOR` 會從 SQL 描述區擷取查詢結果集的相關資訊，並將其存入主機變數。在使用此命令將資訊傳送到主機語言變數之前，描述區通常會先以 `FETCH` 或 `SELECT` 填入資料。

此命令有兩種形式：第一種形式擷取描述區的「標頭」項目，這類項目適用於整個結果集，例如欄位數（原文此處寫作 row count，但下方參數說明指出，目前唯一支援的標頭項目 COUNT 取得的是結果集的欄位數，而不是資料列數）。第二種形式需要以欄位編號作為額外參數，擷取特定欄位的相關資訊，例如欄位名稱與實際的欄位值。

<a id="id-1.7.5.20.11.4"></a>

## 參數

<a id="ECPG-SQL-GET-DESCRIPTOR-DESCRIPTOR-NAME"></a>

*`descriptor_name`* [#](#ECPG-SQL-GET-DESCRIPTOR-DESCRIPTOR-NAME)
:   描述區名稱。
<a id="ECPG-SQL-GET-DESCRIPTOR-DESCRIPTOR-HEADER-ITEM"></a>

*`descriptor_header_item`* [#](#ECPG-SQL-GET-DESCRIPTOR-DESCRIPTOR-HEADER-ITEM)
:   識別要擷取哪一個標頭資訊項目的標記（token）。目前只支援 `COUNT`，用於取得結果集中的欄位數。
<a id="ECPG-SQL-GET-DESCRIPTOR-COLUMN-NUMBER"></a>

*`column_number`* [#](#ECPG-SQL-GET-DESCRIPTOR-COLUMN-NUMBER)
:   要擷取其相關資訊的欄位編號。編號從 1 開始。
<a id="ECPG-SQL-GET-DESCRIPTOR-DESCRIPTOR-ITEM"></a>

*`descriptor_item`* [#](#ECPG-SQL-GET-DESCRIPTOR-DESCRIPTOR-ITEM)
:   識別要擷取欄位的哪一項資訊的標記。支援的項目清單請參閱[第 34.7.1 節](ecpg-descriptors.md#ECPG-NAMED-DESCRIPTORS)。
<a id="ECPG-SQL-GET-DESCRIPTOR-CVARIABLE"></a>

*`cvariable`* [#](#ECPG-SQL-GET-DESCRIPTOR-CVARIABLE)
:   用來接收從描述區擷取之資料的主機變數。

<a id="id-1.7.5.20.11.5"></a>

## 範例

擷取結果集欄位數的範例：

```

EXEC SQL GET DESCRIPTOR d :d_count = COUNT;
```

擷取第一個欄位資料長度的範例：

```

EXEC SQL GET DESCRIPTOR d VALUE 1 :d_returned_octet_length = RETURNED_OCTET_LENGTH;
```

以字串形式擷取第二個欄位資料本體的範例：

```

EXEC SQL GET DESCRIPTOR d VALUE 2 :d_data = DATA;
```

以下是完整流程的範例：執行 `SELECT current_database();`，並顯示欄位數、欄位資料長度與欄位資料：

```

int
main(void)
{
EXEC SQL BEGIN DECLARE SECTION;
    int  d_count;
    char d_data[1024];
    int  d_returned_octet_length;
EXEC SQL END DECLARE SECTION;

    EXEC SQL CONNECT TO testdb AS con1 USER testuser;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL ALLOCATE DESCRIPTOR d;

    /* Declare, open a cursor, and assign a descriptor to the cursor  */
    EXEC SQL DECLARE cur CURSOR FOR SELECT current_database();
    EXEC SQL OPEN cur;
    EXEC SQL FETCH NEXT FROM cur INTO SQL DESCRIPTOR d;

    /* Get a number of total columns */
    EXEC SQL GET DESCRIPTOR d :d_count = COUNT;
    printf("d_count                 = %d\n", d_count);

    /* Get length of a returned column */
    EXEC SQL GET DESCRIPTOR d VALUE 1 :d_returned_octet_length = RETURNED_OCTET_LENGTH;
    printf("d_returned_octet_length = %d\n", d_returned_octet_length);

    /* Fetch the returned column as a string */
    EXEC SQL GET DESCRIPTOR d VALUE 1 :d_data = DATA;
    printf("d_data                  = %s\n", d_data);

    /* Closing */
    EXEC SQL CLOSE cur;
    EXEC SQL COMMIT;

    EXEC SQL DEALLOCATE DESCRIPTOR d;
    EXEC SQL DISCONNECT ALL;

    return 0;
}
```

執行此範例後，結果會如下所示：

```

d_count                 = 1
d_returned_octet_length = 6
d_data                  = testdb
```

<a id="id-1.7.5.20.11.6"></a>

## 相容性

SQL 標準規定了 `GET DESCRIPTOR`。

<a id="id-1.7.5.20.11.7"></a>

## 另請參閱

[ALLOCATE DESCRIPTOR](ecpg-sql-allocate-descriptor.md), [SET DESCRIPTOR](ecpg-sql-set-descriptor.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-get-descriptor.html)（原文版本：18.6；核對日期：2026-10-18）
