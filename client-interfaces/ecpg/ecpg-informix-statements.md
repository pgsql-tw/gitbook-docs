<a id="ECPG-INFORMIX-STATEMENTS"></a>

## 34.15.2. 額外／缺少的嵌入式 SQL 陳述式 [#](#ecpg-informix-statements) <a href="#ecpg-informix-statements" id="ecpg-informix-statements"></a>

<a id="ECPG-INFORMIX-STATEMENTS-CLOSE-DATABASE"></a>

### `CLOSE DATABASE` [#](#ecpg-informix-statements-close-database) <a href="#ecpg-informix-statements-close-database" id="ecpg-informix-statements-close-database"></a>

此陳述式會關閉目前的連線。事實上，它是 ECPG 的 `DISCONNECT CURRENT` 的同義詞：

```

    $CLOSE DATABASE;                /* close the current connection */
    EXEC SQL CLOSE DATABASE;
```

<a id="ECPG-INFORMIX-STATEMENTS-FREE-CURSOR-NAME"></a>

### `FREE cursor_name` [#](#ecpg-informix-statements-free-cursor-name) <a href="#ecpg-informix-statements-free-cursor-name" id="ecpg-informix-statements-free-cursor-name"></a>

由於 ECPG 的運作方式與 Informix 的 ESQL/C 不同（也就是哪些步驟純屬語法轉換、哪些步驟仰賴底層的執行時期函式庫），ECPG 中沒有 `FREE cursor_name` 陳述式。這是因為在 ECPG 中，`DECLARE CURSOR` 並不會轉換成對執行時期函式庫、使用該游標名稱的函式呼叫。這表示 ECPG 執行時期函式庫中並不會在執行時期記錄 SQL 游標，只有 PostgreSQL 伺服器會記錄。

<a id="ECPG-INFORMIX-STATEMENTS-FREE-STATEMENT-NAME"></a>

### `FREE statement_name` [#](#ecpg-informix-statements-free-statement-name) <a href="#ecpg-informix-statements-free-statement-name" id="ecpg-informix-statements-free-statement-name"></a>

`FREE statement_name` 是 `DEALLOCATE PREPARE statement_name` 的同義詞。

[返回 34.15. Informix 相容模式](ecpg-informix-compat.md#ecpg-informix-compat)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/ecpg-informix-compat.html)（原文版本：18.6；核對日期：2026-10-22）
