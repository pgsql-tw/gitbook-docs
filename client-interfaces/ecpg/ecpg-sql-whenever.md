## WHENEVER

WHENEVER — 指定 SQL 陳述式引發特定類別條件時要採取的動作

## 語法

```

WHENEVER { NOT FOUND | SQLERROR | SQLWARNING } action
```

<a id="id-1.7.5.20.19.3"></a>

## 說明

定義 SQL 執行結果出現特殊情況（找不到資料列、SQL 警告或錯誤）時要呼叫的行為。

<a id="id-1.7.5.20.19.4"></a>

## 參數

參數說明請參閱[第 34.8.1 節](ecpg-errors.md#ECPG-WHENEVER)。

<a id="id-1.7.5.20.19.5"></a>

## 範例

```

EXEC SQL WHENEVER NOT FOUND CONTINUE;
EXEC SQL WHENEVER NOT FOUND DO BREAK;
EXEC SQL WHENEVER NOT FOUND DO CONTINUE;
EXEC SQL WHENEVER SQLWARNING SQLPRINT;
EXEC SQL WHENEVER SQLWARNING DO warn();
EXEC SQL WHENEVER SQLERROR sqlprint;
EXEC SQL WHENEVER SQLERROR CALL print2();
EXEC SQL WHENEVER SQLERROR DO handle_error("select");
EXEC SQL WHENEVER SQLERROR DO sqlnotice(NULL, NONO);
EXEC SQL WHENEVER SQLERROR DO sqlprint();
EXEC SQL WHENEVER SQLERROR GOTO error_label;
EXEC SQL WHENEVER SQLERROR STOP;
```

典型用途是使用 `WHENEVER NOT FOUND BREAK` 處理走訪結果集的迴圈：

```

int
main(void)
{
    EXEC SQL CONNECT TO testdb AS con1;
    EXEC SQL SELECT pg_catalog.set_config('search_path', '', false); EXEC SQL COMMIT;
    EXEC SQL ALLOCATE DESCRIPTOR d;
    EXEC SQL DECLARE cur CURSOR FOR SELECT current_database(), 'hoge', 256;
    EXEC SQL OPEN cur;

    /* when end of result set reached, break out of while loop */
    EXEC SQL WHENEVER NOT FOUND DO BREAK;

    while (1)
    {
        EXEC SQL FETCH NEXT FROM cur INTO SQL DESCRIPTOR d;
        ...
    }

    EXEC SQL CLOSE cur;
    EXEC SQL COMMIT;

    EXEC SQL DEALLOCATE DESCRIPTOR d;
    EXEC SQL DISCONNECT ALL;

    return 0;
}
```

<a id="id-1.7.5.20.19.6"></a>

## 相容性

SQL 標準規定了 `WHENEVER`，但多數動作都是 PostgreSQL 擴充功能。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-whenever.html)（英文原文，待翻譯）
