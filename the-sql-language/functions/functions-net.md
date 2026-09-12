<a id="FUNCTIONS-NET"></a>

## 9.12. 網路位址函式與運算子 [#](#FUNCTIONS-NET)

IP 網路位址型別 `cidr` 與 `inet`，支援[表 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) 所列的一般比較運算子，以及[表 9.39](functions-net.md#CIDR-INET-OPERATORS-TABLE) 與[表 9.40](functions-net.md#CIDR-INET-FUNCTIONS-TABLE) 所列的特殊運算子與函式。

任何 `cidr` 值都可以隱含地轉換為 `inet`；因此，下面所列作用在 `inet` 上的運算子與函式，也適用於 `cidr` 值。（對 `inet` 與 `cidr` 分別有不同函式的地方，是因為這兩種情況的行為應該有所不同。）此外，也允許將 `inet` 值轉換為 `cidr`。這麼做時，網路遮罩右邊的所有位元都會被默默地清為零，以建立有效的 `cidr` 值。

<a id="CIDR-INET-OPERATORS-TABLE"></a>

**表 9.39. IP 位址運算子**

<table border="1" class="table" summary="IP Address Operators"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        運算子
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">&lt;&lt;</code> <code class="type">inet</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        子網路是否被另一個子網路嚴格包含？這個運算子與接下來的四個運算子，用來檢驗子網路的包含關係。它們只考慮兩個位址的網路部分（忽略網路遮罩右邊的任何位元），並判斷一個網路是否與另一個相同，或是另一個的子網路。
       </p>
<p>
<code class="literal">inet '192.168.1.5' &lt;&lt; inet '192.168.1/24'</code>
        → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">inet '192.168.0.5' &lt;&lt; inet '192.168.1/24'</code>
        → <code class="returnvalue">f</code>
</p>
<p>
<code class="literal">inet '192.168.1/24' &lt;&lt; inet '192.168.1/24'</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">&lt;&lt;=</code> <code class="type">inet</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        子網路是否被另一個子網路包含或與之相等？
       </p>
<p>
<code class="literal">inet '192.168.1/24' &lt;&lt;= inet '192.168.1/24'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">&gt;&gt;</code> <code class="type">inet</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        子網路是否嚴格包含另一個子網路？
       </p>
<p>
<code class="literal">inet '192.168.1/24' &gt;&gt; inet '192.168.1.5'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">&gt;&gt;=</code> <code class="type">inet</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        子網路是否包含另一個子網路或與之相等？
       </p>
<p>
<code class="literal">inet '192.168.1/24' &gt;&gt;= inet '192.168.1/24'</code>
        → <code class="returnvalue">t</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">&amp;&amp;</code> <code class="type">inet</code>
        → <code class="returnvalue">boolean</code>
</p>
<p>
        是否有一個子網路包含另一個或與之相等？
       </p>
<p>
<code class="literal">inet '192.168.1/24' &amp;&amp; inet '192.168.1.80/28'</code>
        → <code class="returnvalue">t</code>
</p>
<p>
<code class="literal">inet '192.168.1/24' &amp;&amp; inet '192.168.2.0/28'</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="literal">~</code> <code class="type">inet</code>
        → <code class="returnvalue">inet</code>
</p>
<p>
        計算位元 NOT。
       </p>
<p>
<code class="literal">~ inet '192.168.1.6'</code>
        → <code class="returnvalue">63.87.254.249</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">&amp;</code> <code class="type">inet</code>
        → <code class="returnvalue">inet</code>
</p>
<p>
        計算位元 AND。
       </p>
<p>
<code class="literal">inet '192.168.1.6' &amp; inet '0.0.0.255'</code>
        → <code class="returnvalue">0.0.0.6</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">|</code> <code class="type">inet</code>
        → <code class="returnvalue">inet</code>
</p>
<p>
        計算位元 OR。
       </p>
<p>
<code class="literal">inet '192.168.1.6' | inet '0.0.0.255'</code>
        → <code class="returnvalue">192.168.1.255</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">+</code> <code class="type">bigint</code>
        → <code class="returnvalue">inet</code>
</p>
<p>
        為位址加上一個位移量。
       </p>
<p>
<code class="literal">inet '192.168.1.6' + 25</code>
        → <code class="returnvalue">192.168.1.31</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">bigint</code> <code class="literal">+</code> <code class="type">inet</code>
        → <code class="returnvalue">inet</code>
</p>
<p>
        為位址加上一個位移量。
       </p>
<p>
<code class="literal">200 + inet '::ffff:fff0:1'</code>
        → <code class="returnvalue">::ffff:255.240.0.201</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">-</code> <code class="type">bigint</code>
        → <code class="returnvalue">inet</code>
</p>
<p>
        從位址減去一個位移量。
       </p>
<p>
<code class="literal">inet '192.168.1.43' - 36</code>
        → <code class="returnvalue">192.168.1.7</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="type">inet</code> <code class="literal">-</code> <code class="type">inet</code>
        → <code class="returnvalue">bigint</code>
</p>
<p>
        計算兩個位址的差值。
       </p>
<p>
<code class="literal">inet '192.168.1.43' - inet '192.168.1.19'</code>
        → <code class="returnvalue">24</code>
</p>
<p>
<code class="literal">inet '::1' - inet '::ffff:1'</code>
        → <code class="returnvalue">-4294901760</code>
</p></td></tr></tbody></table>

<br><a id="CIDR-INET-FUNCTIONS-TABLE"></a>

**表 9.40. IP 位址函式**

<table border="1" class="table" summary="IP Address Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.1.1.1.1"></a>
<code class="function">abbrev</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        以文字形式建立縮寫的顯示格式。（其結果與 <code class="type">inet</code> 輸出函式所產生的相同；它只是相對於明確轉換為 <code class="type">text</code> 的結果而言是<span class="quote">“<span class="quote">縮寫</span>”</span>的，因為基於歷史原因，明確轉換為 text 永遠不會省略網路遮罩部分。）
       </p>
<p>
<code class="literal">abbrev(inet '10.1.0.0/32')</code>
        → <code class="returnvalue">10.1.0.0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">abbrev</code> ( <code class="type">cidr</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        以文字形式建立縮寫的顯示格式。（縮寫的方式是去除網路遮罩右邊全為零的八位元組；更多範例請見<a class="xref" href="../datatype/datatype-net-types.md#DATATYPE-NET-CIDR-TABLE">表 8.22</a>。）
       </p>
<p>
<code class="literal">abbrev(cidr '10.1.0.0/16')</code>
        → <code class="returnvalue">10.1/16</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.3.1.1.1"></a>
<code class="function">broadcast</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">inet</code>
</p>
<p>
        計算該位址所屬網路的廣播位址。
       </p>
<p>
<code class="literal">broadcast(inet '192.168.1.5/24')</code>
        → <code class="returnvalue">192.168.1.255/24</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.4.1.1.1"></a>
<code class="function">family</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        回傳位址的家族：IPv4 為 <code class="literal">4</code>，IPv6 為 <code class="literal">6</code>。
       </p>
<p>
<code class="literal">family(inet '::1')</code>
        → <code class="returnvalue">6</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.5.1.1.1"></a>
<code class="function">host</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        以文字形式回傳 IP 位址，忽略網路遮罩。
       </p>
<p>
<code class="literal">host(inet '192.168.1.0/24')</code>
        → <code class="returnvalue">192.168.1.0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.6.1.1.1"></a>
<code class="function">hostmask</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">inet</code>
</p>
<p>
        計算該位址所屬網路的主機遮罩。
       </p>
<p>
<code class="literal">hostmask(inet '192.168.23.20/30')</code>
        → <code class="returnvalue">0.0.0.3</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.7.1.1.1"></a>
<code class="function">inet_merge</code> ( <code class="type">inet</code>, <code class="type">inet</code> )
        → <code class="returnvalue">cidr</code>
</p>
<p>
        計算同時包含兩個給定網路的最小網路。
       </p>
<p>
<code class="literal">inet_merge(inet '192.168.1.5/24', inet '192.168.2.5/24')</code>
        → <code class="returnvalue">192.168.0.0/22</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.8.1.1.1"></a>
<code class="function">inet_same_family</code> ( <code class="type">inet</code>, <code class="type">inet</code> )
        → <code class="returnvalue">boolean</code>
</p>
<p>
        檢驗兩個位址是否屬於同一個 IP 家族。
       </p>
<p>
<code class="literal">inet_same_family(inet '192.168.1.5/24', inet '::1')</code>
        → <code class="returnvalue">f</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.9.1.1.1"></a>
<code class="function">masklen</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">integer</code>
</p>
<p>
        以位元為單位回傳網路遮罩長度。
       </p>
<p>
<code class="literal">masklen(inet '192.168.1.5/24')</code>
        → <code class="returnvalue">24</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.10.1.1.1"></a>
<code class="function">netmask</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">inet</code>
</p>
<p>
        計算該位址所屬網路的網路遮罩。
       </p>
<p>
<code class="literal">netmask(inet '192.168.1.5/24')</code>
        → <code class="returnvalue">255.255.255.0</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.11.1.1.1"></a>
<code class="function">network</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">cidr</code>
</p>
<p>
        回傳位址的網路部分，並將網路遮罩右邊的部分清為零。（這等同於將該值轉換為 <code class="type">cidr</code>。）
       </p>
<p>
<code class="literal">network(inet '192.168.1.5/24')</code>
        → <code class="returnvalue">192.168.1.0/24</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.12.1.1.1"></a>
<code class="function">set_masklen</code> ( <code class="type">inet</code>, <code class="type">integer</code> )
        → <code class="returnvalue">inet</code>
</p>
<p>
        設定 <code class="type">inet</code> 值的網路遮罩長度。位址部分不會改變。
       </p>
<p>
<code class="literal">set_masklen(inet '192.168.1.5/24', 16)</code>
        → <code class="returnvalue">192.168.1.5/16</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">set_masklen</code> ( <code class="type">cidr</code>, <code class="type">integer</code> )
        → <code class="returnvalue">cidr</code>
</p>
<p>
        設定 <code class="type">cidr</code> 值的網路遮罩長度。新網路遮罩右邊的位址位元會被設為零。
       </p>
<p>
<code class="literal">set_masklen(cidr '192.168.1.0/24', 16)</code>
        → <code class="returnvalue">192.168.0.0/16</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.5.2.2.14.1.1.1"></a>
<code class="function">text</code> ( <code class="type">inet</code> )
        → <code class="returnvalue">text</code>
</p>
<p>
        以文字形式回傳未縮寫的 IP 位址與網路遮罩長度。（其結果與明確轉換為 <code class="type">text</code> 相同。）
       </p>
<p>
<code class="literal">text(inet '192.168.1.5')</code>
        → <code class="returnvalue">192.168.1.5/32</code>
</p></td></tr></tbody></table>

<br>

### 提示

`abbrev`、`host` 與 `text` 函式的主要用途，是為 IP 位址提供其他的顯示格式。

MAC 位址型別 `macaddr` 與 `macaddr8`，支援[表 9.1](functions-comparison.md#FUNCTIONS-COMPARISON-OP-TABLE) 所列的一般比較運算子，以及[表 9.41](functions-net.md#MACADDR-FUNCTIONS-TABLE) 所列的特殊函式。此外，就像上面 IP 位址所示範的一樣，它們也支援位元邏輯運算子 `~`、`&` 與 `|`（NOT、AND 與 OR）。

<a id="MACADDR-FUNCTIONS-TABLE"></a>

**表 9.41. MAC 位址函式**

<table border="1" class="table" summary="MAC Address Functions"><colgroup><col/></colgroup><thead><tr><th class="func_table_entry"><p class="func_signature">
        函式
       </p>
<p>
        說明
       </p>
<p>
        範例
       </p></th></tr></thead><tbody><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.8.2.2.1.1.1.1"></a>
<code class="function">trunc</code> ( <code class="type">macaddr</code> )
        → <code class="returnvalue">macaddr</code>
</p>
<p>
        將位址的最後 3 個位元組設為零。剩下的前綴可以對應到特定的製造商（使用 <span class="productname">PostgreSQL</span> 未包含的資料）。
       </p>
<p>
<code class="literal">trunc(macaddr '12:34:56:78:90:ab')</code>
        → <code class="returnvalue">12:34:56:00:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<code class="function">trunc</code> ( <code class="type">macaddr8</code> )
        → <code class="returnvalue">macaddr8</code>
</p>
<p>
        將位址的最後 5 個位元組設為零。剩下的前綴可以對應到特定的製造商（使用 <span class="productname">PostgreSQL</span> 未包含的資料）。
       </p>
<p>
<code class="literal">trunc(macaddr8 '12:34:56:78:90:ab:cd:ef')</code>
        → <code class="returnvalue">12:34:56:00:00:00:00:00</code>
</p></td></tr><tr><td class="func_table_entry"><p class="func_signature">
<a class="indexterm" id="id-1.5.8.18.8.2.2.3.1.1.1"></a>
<code class="function">macaddr8_set7bit</code> ( <code class="type">macaddr8</code> )
        → <code class="returnvalue">macaddr8</code>
</p>
<p>
        將位址的第 7 個位元設為一，產生所謂的修正版 EUI-64，以便放入 IPv6 位址中。
       </p>
<p>
<code class="literal">macaddr8_set7bit(macaddr8 '00:34:56:ab:cd:ef')</code>
        → <code class="returnvalue">02:34:56:ff:fe:ab:cd:ef</code>
</p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/functions-net.html)（原文版本：18.6；核對日期：2026-09-11）
