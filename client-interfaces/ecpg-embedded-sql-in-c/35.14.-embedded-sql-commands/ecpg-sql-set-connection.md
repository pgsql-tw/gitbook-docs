<a id="ECPG-SQL-SET-CONNECTION"></a>

# SET CONNECTION

SET CONNECTION — 選取資料庫連線

## 語法

```

SET CONNECTION [ TO | = ] connection_name
```

<a id="id-1.7.5.20.15.3"></a>

## 說明

`SET CONNECTION` 設定「目前」資料庫連線；除非另有指定，所有命令都使用此連線。

<a id="id-1.7.5.20.15.4"></a>

## 參數

<em class="replaceable"><code>connection&#95;name</code></em>

由 `CONNECT` 命令建立的資料庫連線名稱。

`CURRENT`

將連線設為目前連線（因此不會發生任何變化）。

<a id="id-1.7.5.20.15.5"></a>

## 範例

```

EXEC SQL SET CONNECTION TO con2;
EXEC SQL SET CONNECTION = con1;
```

<a id="id-1.7.5.20.15.6"></a>

## 相容性

SQL 標準規定了 `SET CONNECTION`。

<a id="id-1.7.5.20.15.7"></a>

## 另請參閱

[CONNECT](ecpg-sql-connect.md), [DISCONNECT](ecpg-sql-disconnect.md)

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/ecpg-sql-set-connection.html)
