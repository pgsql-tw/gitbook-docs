<a id="FUNCTIONS-TRIGGER"></a>

## 9.29. 觸發程序函式 [#](#FUNCTIONS-TRIGGER)

雖然觸發程序的許多用途都涉及使用者撰寫的觸發程序函式，但 PostgreSQL 也提供了一些內建的觸發程序函式，可以直接用在使用者定義的觸發程序中。這些函式彙整於[表 9.110](functions-trigger.md#BUILTIN-TRIGGERS-TABLE)。（另外還有其他實作外鍵限制條件與延遲索引限制條件的內建觸發程序函式。由於使用者不需要直接使用它們，因此這裡不加以說明。）

關於建立觸發程序的更多資訊，請參閱 [CREATE TRIGGER](../../reference/sql-commands/sql-createtrigger.md)。

<a id="BUILTIN-TRIGGERS-TABLE"></a>

**表 9.110. 內建觸發程序函式**

<table border="1" class="table" summary="Built-In Trigger Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        使用範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.35.4.2.2.1.1.1.1"></a>
<code class="function">suppress_redundant_updates_trigger</code> ( )
        → <code class="returnvalue">trigger</code>
</p>
<p>
        抑制不做任何事的更新操作。詳情請見下文。
       </p>
<p>
<code class="literal">CREATE TRIGGER ... suppress_redundant_updates_trigger()</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.35.4.2.2.2.1.1.1"></a>
<code class="function">tsvector_update_trigger</code> ( )
        → <code class="returnvalue">trigger</code>
</p>
<p>
        從相關聯的純文字文件欄位自動更新 <code class="type">tsvector</code> 欄位。要使用的文字搜尋組態，以名稱的形式作為觸發程序引數指定。詳情請參閱<a class="xref" href="../textsearch/textsearch-features.md#TEXTSEARCH-UPDATE-TRIGGERS">第 12.4.3 節</a>。
       </p>
<p>
<code class="literal">CREATE TRIGGER ... tsvector_update_trigger(tsvcol, 'pg_catalog.swedish', title, body)</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.35.4.2.2.3.1.1.1"></a>
<code class="function">tsvector_update_trigger_column</code> ( )
        → <code class="returnvalue">trigger</code>
</p>
<p>
        從相關聯的純文字文件欄位自動更新 <code class="type">tsvector</code> 欄位。要使用的文字搜尋組態，取自該資料表的一個 <code class="type">regconfig</code> 欄位。詳情請參閱<a class="xref" href="../textsearch/textsearch-features.md#TEXTSEARCH-UPDATE-TRIGGERS">第 12.4.3 節</a>。
       </p>
<p>
<code class="literal">CREATE TRIGGER ... tsvector_update_trigger_column(tsvcol, tsconfigcol, title, body)</code>
</p></td></tr></tbody></table>

<br>

`suppress_redundant_updates_trigger` 函式在作為資料列層級的 `BEFORE UPDATE` 觸發程序套用時，會阻止任何實際上沒有改變資料列中資料的更新發生。這會覆寫一般的行為；一般的行為是無論資料是否改變，都一律進行實體的資料列更新。（這種一般行為讓更新執行得更快，因為不需要進行任何檢查，而且在某些情況下也很有用。）

理想情況下，你應該避免執行實際上不會改變記錄中資料的更新。多餘的更新可能耗費相當多不必要的時間，特別是當有很多索引需要變更時；而且還會在失效資料列中占用空間，最終必須被清理。不過，在用戶端程式碼中偵測這類情況並不總是容易，甚至不一定可行，而撰寫偵測它們的運算式也很容易出錯。另一種做法是使用 `suppress_redundant_updates_trigger`，它會略過不改變資料的更新。不過，你應該謹慎使用它。這個觸發程序對每一筆記錄都會花費一點點但不可忽略的時間，因此如果受更新影響的記錄大多確實有改變，使用這個觸發程序反而會讓更新平均執行得更慢。

可以像這樣將 `suppress_redundant_updates_trigger` 函式加入資料表：

```

CREATE TRIGGER z_min_update
BEFORE UPDATE ON tablename
FOR EACH ROW EXECUTE FUNCTION suppress_redundant_updates_trigger();
```

在大多數情況下，你需要讓這個觸發程序在每一筆資料列上最後觸發，以免它覆寫可能想要變更該資料列的其他觸發程序。考量到觸發程序是依名稱順序觸發的，你應該選擇一個排在該資料表上任何其他觸發程序名稱之後的觸發程序名稱。（這就是範例中使用「z」前綴的原因。）

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-trigger.html)（原文版本：18.6；核對日期：2026-09-11）
