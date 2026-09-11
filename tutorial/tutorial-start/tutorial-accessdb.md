<a id="TUTORIAL-ACCESSDB"></a>

## 1.4. 存取資料庫 [#](#TUTORIAL-ACCESSDB)

<a id="id-1.4.3.5.2"></a>

建立資料庫之後，你可以透過下列方式存取它：

* 執行 PostgreSQL 的互動式終端程式 *psql*，讓你以互動方式輸入、編輯並執行 SQL 指令。
* 使用現有的圖形化前端工具，例如 pgAdmin，或支援 ODBC 或 JDBC 的辦公室套裝軟體，來建立與操作資料庫。本教學不會介紹這些方式。
* 使用現有的多種程式語言繫結之一，撰寫自訂的應用程式。這些方式會在[第四部分](../../client-interfaces/README.md)進一步說明。

你大概會想啟動 `psql` 來試試本教學中的範例。要對 `mydb` 資料庫啟動它，請輸入下列指令：

```

$ psql mydb
```

如果沒有提供資料庫名稱，預設會使用你的使用者帳號名稱。你在上一節使用 `createdb` 時已經見過這個規則。

在 `psql` 中，你會看到下列歡迎訊息：

```

psql (18.6)
Type "help" for help.

mydb=>
```

<a id="id-1.4.3.5.4.3"></a>
最後一行也可能是：

```

mydb=#
```

這表示你是資料庫超級使用者；如果 PostgreSQL 執行個體是你自行安裝的，情況多半如此。身為超級使用者，你不受存取控制的限制。就本教學而言，這一點並不重要。

如果你啟動 `psql` 時遇到問題，請回到上一節。`createdb` 與 `psql` 的診斷方式相似，如果前者可以運作，後者應該也可以。

`psql` 印出的最後一行是提示字元，表示 `psql` 正在等待你的輸入，你可以在 `psql` 維護的工作區中輸入 SQL 查詢。請試試下列指令：
<a id="id-1.4.3.5.6.5"></a>

```

mydb=> SELECT version();
                                         version
-------------------------------------------------------------------​-----------------------
 PostgreSQL 18.6 on x86_64-pc-linux-gnu, compiled by gcc (Debian 4.9.2-10) 4.9.2, 64-bit
(1 row)

mydb=> SELECT current_date;
    date
------------
 2016-01-07
(1 row)

mydb=> SELECT 2 + 2;
 ?column?
----------
        4
(1 row)
```

`psql` 程式有一些不屬於 SQL 指令的內部指令，它們以反斜線字元「`\`」開頭。舉例來說，你可以輸入下列指令，取得各種 PostgreSQL SQL 指令語法的說明：

```

mydb=> \h
```

要離開 `psql`，請輸入：

```

mydb=> \q
```

`psql` 就會結束，並讓你回到命令列 shell。（要查看更多內部指令，請在 `psql` 提示字元下輸入 `\?`。）`psql` 的完整功能記載於 [psql](../../reference/reference-client/app-psql.md)。本教學不會明確使用這些功能，但你可以在需要時自行運用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/tutorial-accessdb.html)（原文版本：18.6；核對日期：2026-09-11）
