<a id="FUNCTIONS-SEQUENCE"></a>

## 9.17. 序列操作函式 [#](#FUNCTIONS-SEQUENCE)

<a id="id-1.5.8.23.2"></a>

本節說明用於操作*序列物件*（sequence object）的函式；序列物件也稱為序列產生器，或簡稱序列。序列物件是以 [CREATE SEQUENCE](../../reference/sql-commands/sql-createsequence.md) 建立的特殊單列資料表。序列物件通常用來為資料表的資料列產生唯一識別碼。[表 9.55](functions-sequence.md#FUNCTIONS-SEQUENCE-TABLE) 所列的序列函式，提供了從序列物件取得連續序列值的簡單、多使用者安全的方法。

<a id="FUNCTIONS-SEQUENCE-TABLE"></a>

**表 9.55. 序列函式**

<table border="1" class="table" summary="Sequence Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.23.4.2.2.1.1.1.1"></a>
<code class="function">nextval</code> ( <code class="type">regclass</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        將序列物件推進到下一個值，並回傳該值。這是以原子方式完成的：即使多個工作階段同時執行 <code class="function">nextval</code>，每個工作階段也都會安全地取得不同的序列值。如果序列物件是以預設參數建立的，連續的 <code class="function">nextval</code> 呼叫會回傳從 1 開始的連續值。在 <a class="xref" href="../../reference/sql-commands/sql-createsequence.md"><span class="refentrytitle">CREATE SEQUENCE</span></a> 命令中使用適當的參數，可以得到其他行為。
      </p>
<p>
        這個函式需要序列上的 <code class="literal">USAGE</code> 或 <code class="literal">UPDATE</code> 權限。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.23.4.2.2.2.1.1.1"></a>
<code class="function">setval</code> ( <code class="type">regclass</code>, <code class="type">bigint</code> [<span class="optional">, <code class="type">boolean</code> </span>] )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        設定序列物件的目前值，並可選擇性地設定其 <code class="literal">is_called</code> 旗標。雙參數形式會將序列的 <code class="literal">last_value</code> 欄位設為指定的值，並將其 <code class="literal">is_called</code> 欄位設為 <code class="literal">true</code>，這表示下一次 <code class="function">nextval</code> 會先推進序列，再回傳值。<code class="function">currval</code> 所回報的值也會被設為指定的值。在三參數形式中，<code class="literal">is_called</code> 可以設為 <code class="literal">true</code> 或 <code class="literal">false</code>。<code class="literal">true</code> 的效果與雙參數形式相同。如果設為 <code class="literal">false</code>，下一次 <code class="function">nextval</code> 會正好回傳指定的值，而序列會從再下一次 <code class="function">nextval</code> 開始推進。此外，在這種情況下，<code class="function">currval</code> 所回報的值不會改變。例如，
</p><pre class="programlisting">
SELECT setval('myseq', 42);           <em class="lineannotation"><span class="lineannotation">Next <code class="function">nextval</code> will return 43</span></em>
SELECT setval('myseq', 42, true);     <em class="lineannotation"><span class="lineannotation">Same as above</span></em>
SELECT setval('myseq', 42, false);    <em class="lineannotation"><span class="lineannotation">Next <code class="function">nextval</code> will return 42</span></em>
</pre><p>
        <code class="function">setval</code> 回傳的結果就是它第二個引數的值。
       </p>
<p>
        這個函式需要序列上的 <code class="literal">UPDATE</code> 權限。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.23.4.2.2.3.1.1.1"></a>
<code class="function">currval</code> ( <code class="type">regclass</code> )
        → <code class="returnvalue">bigint</code>
</p>
<p>
        回傳目前工作階段中，<code class="function">nextval</code> 最近一次為這個序列取得的值。（如果在這個工作階段中從未為這個序列呼叫過 <code class="function">nextval</code>，就會回報錯誤。）由於回傳的是工作階段本機的值，無論其他工作階段在目前工作階段之後是否執行過 <code class="function">nextval</code>，它都會提供可預測的答案。
       </p>
<p>
        這個函式需要序列上的 <code class="literal">USAGE</code> 或 <code class="literal">SELECT</code> 權限。
       </p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.23.4.2.2.4.1.1.1"></a>
<code class="function">lastval</code> ()
        → <code class="returnvalue">bigint</code>
</p>
<p>
        回傳目前工作階段中 <code class="function">nextval</code> 最近一次回傳的值。這個函式與 <code class="function">currval</code> 相同，只是它不以序列名稱作為引數，而是參照目前工作階段中 <code class="function">nextval</code> 最近一次套用的那個序列。呼叫 <code class="function">lastval</code> 時，如果目前工作階段中還沒有呼叫過 <code class="function">nextval</code>，就會發生錯誤。
       </p>
<p>
        這個函式需要最後使用之序列上的 <code class="literal">USAGE</code> 或 <code class="literal">SELECT</code> 權限。
       </p></td></tr></tbody></table>

<br>

### 警示

為了避免阻擋從同一個序列取得數字的並行交易，如果呼叫的交易之後中止，由 `nextval` 取得的值不會被收回重複使用。這表示交易中止或資料庫當機，可能會使指派出去的值序列中出現間隙。即使沒有交易中止，這種情況也可能發生。例如，帶有 `ON CONFLICT` 子句的 `INSERT`，會在偵測到任何會使它改為遵循 `ON CONFLICT` 規則的衝突之前，先計算要插入的 tuple，包括進行任何必要的 `nextval` 呼叫。因此，PostgreSQL 的序列物件*無法用來取得「無間隙」的序列*。

同樣地，由 `setval` 所做的序列狀態變更，會立即對其他交易可見，而且即使呼叫的交易回復，也不會被撤銷。

如果資料庫叢集在包含 `nextval` 或 `setval` 呼叫的交易提交之前當機，序列狀態的變更可能還沒有寫入持久性儲存體，因此在叢集重新啟動之後，無法確定序列會處於原本的狀態還是更新後的狀態。對於在資料庫內部使用序列而言，這並無害處，因為未提交交易的其他效果同樣也不會可見。不過，如果你想將序列值用於資料庫外部的持久性用途，請確定 `nextval` 呼叫已經提交之後再這麼做。

序列函式所要操作的序列，是由一個 `regclass` 引數指定的，它就是該序列在 `pg_class` 系統目錄中的 OID。不過，你不需要手動查找 OID，因為 `regclass` 資料型別的輸入轉換器會替你完成這項工作。詳情請參閱[第 8.19 節](../datatype/datatype-oid.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-sequence.html)（原文版本：18.6；核對日期：2026-09-11）
