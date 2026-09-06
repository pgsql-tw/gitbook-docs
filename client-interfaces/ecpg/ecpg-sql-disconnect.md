## DISCONNECT

DISCONNECT — 結束資料庫連線

## 語法

```

DISCONNECT connection_name
DISCONNECT [ CURRENT ]
DISCONNECT ALL
```

<a id="id-1.7.5.20.9.3"></a>

## 說明

`DISCONNECT` 關閉資料庫的一個連線（或所有連線）。

<a id="id-1.7.5.20.9.4"></a>

## 參數

<a id="ECPG-SQL-DISCONNECT-CONNECTION-NAME"></a>

*`connection_name`* [#](#ECPG-SQL-DISCONNECT-CONNECTION-NAME)
:   由 `CONNECT` 命令建立的資料庫連線名稱。
<a id="ECPG-SQL-DISCONNECT-CURRENT"></a>

`CURRENT` [#](#ECPG-SQL-DISCONNECT-CURRENT)
:   關閉「目前」連線；它是最近開啟的連線，或由 `SET CONNECTION` 命令設定的連線。若未向 `DISCONNECT` 命令提供引數，這也是預設值。
<a id="ECPG-SQL-DISCONNECT-ALL"></a>

`ALL` [#](#ECPG-SQL-DISCONNECT-ALL)
:   關閉所有已開啟的連線。

<a id="id-1.7.5.20.9.5"></a>

## 範例

```

int
main(void)
{
    EXEC SQL CONNECT TO testdb AS con1 USER testuser;
    EXEC SQL CONNECT TO testdb AS con2 USER testuser;
    EXEC SQL CONNECT TO testdb AS con3 USER testuser;

    EXEC SQL DISCONNECT CURRENT;  /* close con3          */
    EXEC SQL DISCONNECT ALL;      /* close con2 and con1 */

    return 0;
}
```

<a id="id-1.7.5.20.9.6"></a>

## 相容性

SQL 標準規定了 `DISCONNECT`。

<a id="id-1.7.5.20.9.7"></a>

## 另請參閱

[CONNECT](ecpg-sql-connect.md), [SET CONNECTION](ecpg-sql-set-connection.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-sql-disconnect.html)（英文原文，待翻譯）
