# F.26.2. 密碼雜湊函式

<a id="PGCRYPTO-PASSWORD-HASHING-FUNCS"></a>

## F.26.2. 密碼雜湊函式 [#](#pgcrypto-password-hashing-funcs) <a href="#pgcrypto-password-hashing-funcs" id="pgcrypto-password-hashing-funcs"></a>

函式 `crypt()` 與 `gen_salt()` 是專為雜湊密碼而設計的。`crypt()` 負責進行雜湊，`gen_salt()` 則為其準備演算法參數。

`crypt()` 中的演算法在以下幾個方面與一般的 MD5 或 SHA-1 雜湊演算法不同：

1. 它們很慢。由於資料量很小，這是讓暴力破解密碼變得困難的唯一方法。
2. 它們使用一個稱為*鹽值*（salt）的隨機值，讓密碼相同的使用者具有不同的加密後密碼。這也是防止演算法被反推的額外防禦。
3. 它們會在結果中包含演算法類型，因此以不同演算法雜湊的密碼可以並存。
4. 其中有些是可調適的——也就是說，當電腦變得更快時，你可以調整演算法使其變慢，而不會與現有密碼產生不相容。

[表 F.18](#pgcrypto-crypt-algorithms)列出 `crypt()` 函式所支援的演算法。

<a id="PGCRYPTO-CRYPT-ALGORITHMS"></a>

### 表 F.18. `crypt()` 支援的演算法 [#](#pgcrypto-crypt-algorithms) <a href="#pgcrypto-crypt-algorithms" id="pgcrypto-crypt-algorithms"></a>

<table border="1" class="table" summary="表 F.18. crypt() 支援的演算法"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/><col class="col5"/><col class="col6"/></colgroup><thead><tr><th>演算法</th><th>密碼最大長度</th><th>可調適？</th><th>鹽值位元數</th><th>輸出長度</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">bf</code></td><td>72</td><td>是</td><td>128</td><td>60</td><td>以 Blowfish 為基礎，2a 變體</td></tr><tr><td><code class="literal">md5</code></td><td>無限制</td><td>否</td><td>48</td><td>34</td><td>以 MD5 為基礎的 crypt</td></tr><tr><td><code class="literal">xdes</code></td><td>8</td><td>是</td><td>24</td><td>20</td><td>擴充 DES</td></tr><tr><td><code class="literal">des</code></td><td>8</td><td>否</td><td>12</td><td>13</td><td>原始的 UNIX crypt</td></tr><tr><td><code class="literal">sha256crypt</code></td><td>無限制</td><td>是</td><td>最多 32</td><td>80</td><td>改編自公開的參考實作
       <a class="ulink" href="https://www.akkadia.org/drepper/SHA-crypt.txt" target="_top">使用 SHA-256 與 SHA-512 的 Unix crypt
       </a>
</td></tr><tr><td><code class="literal">sha512crypt</code></td><td>無限制</td><td>是</td><td>最多 32</td><td>123</td><td>改編自公開的參考實作
       <a class="ulink" href="https://www.akkadia.org/drepper/SHA-crypt.txt" target="_top">使用 SHA-256 與 SHA-512 的 Unix crypt
       </a>
</td></tr></tbody></table>

<br>

<a id="PGCRYPTO-PASSWORD-HASHING-FUNCS-CRYPT"></a>

### F.26.2.1. `crypt()` [#](#pgcrypto-password-hashing-funcs-crypt) <a href="#pgcrypto-password-hashing-funcs-crypt" id="pgcrypto-password-hashing-funcs-crypt"></a>

<a id="id-1.11.7.36.8.7.2"></a>

```

crypt(password text, salt text) returns text
```

計算 *`password`* 的 crypt(3) 風格雜湊值。儲存新密碼時，你需要使用 `gen_salt()` 產生新的 *`salt`* 值。要檢查密碼時，請將儲存的雜湊值作為 *`salt`* 傳入，並測試結果是否與儲存的值相符。

設定新密碼的範例：

```

UPDATE ... SET pswhash = crypt('new password', gen_salt('md5'));
```

驗證的範例：

```

SELECT (pswhash = crypt('entered password', pswhash)) AS pswmatch FROM ... ;
```

若輸入的密碼正確，這會傳回 `true`。

<a id="PGCRYPTO-PASSWORD-HASHING-FUNCS-GEN-SALT"></a>

### F.26.2.2. `gen_salt()` [#](#pgcrypto-password-hashing-funcs-gen-salt) <a href="#pgcrypto-password-hashing-funcs-gen-salt" id="pgcrypto-password-hashing-funcs-gen-salt"></a>

<a id="id-1.11.7.36.8.8.2"></a>

```

gen_salt(type text [, iter_count integer ]) returns text
```

產生新的隨機鹽值字串，供 `crypt()` 使用。鹽值字串也會告訴 `crypt()` 要使用哪一種演算法。

*`type`* 參數指定雜湊演算法。可接受的類型有：`des`、`xdes`、`md5`、`bf`、`sha256crypt` 與 `sha512crypt`。最後兩種 `sha256crypt` 與 `sha512crypt`，是以 `SHA-2` 為基礎的現代密碼雜湊。

對於具有迭代次數的演算法，*`iter_count`* 參數讓使用者指定迭代次數。次數越高，雜湊密碼所需的時間就越長，因此破解所需的時間也越長。不過，若次數過高，計算一次雜湊的時間可能長達數年——這有點不切實際。若省略 *`iter_count`* 參數，則使用預設的迭代次數。*`iter_count`* 的允許值取決於演算法，列於[表 F.19](#PGCRYPTO-ICFC-TABLE)。

<a id="PGCRYPTO-ICFC-TABLE"></a>

**表 F.19. `crypt()` 的迭代次數**

<table border="1" class="table" summary="表 F.19. crypt() 的迭代次數"><colgroup><col/><col/><col/><col/></colgroup><thead><tr><th>演算法</th><th>預設值</th><th>最小值</th><th>最大值</th></tr></thead><tbody><tr><td><code class="literal">xdes</code></td><td>725</td><td>1</td><td>16777215</td></tr><tr><td><code class="literal">bf</code></td><td>6</td><td>4</td><td>31</td></tr><tr><td><code class="literal">sha256crypt, sha512crypt</code></td><td>5000</td><td>1000</td><td>999999999</td></tr></tbody></table>

<br>

對於 `xdes`，還有一項額外限制：迭代次數必須是奇數。

要選擇適當的迭代次數，請考慮原始的 DES crypt 在設計上，是讓當時的硬體每秒執行 4 次雜湊。比每秒 4 次雜湊更慢，可能會降低可用性；比每秒 100 次雜湊更快，則可能太快了。

[表 F.20](#PGCRYPTO-HASH-SPEED-TABLE)概述不同雜湊演算法的相對緩慢程度。此表顯示，在假設密碼只包含小寫字母，或包含大小寫字母與數字的情況下，嘗試 8 個字元之密碼的所有字元組合需要多少時間。在 `crypt-bf` 項目中，斜線後面的數字是 `gen_salt` 的 *`iter_count`* 參數。

`sha256crypt` 與 `sha512crypt` 的預設 *`iter_count`* 為 `5000`，對現代硬體而言被認為過低，但可以調整以產生更強的密碼雜湊。除此之外，`sha256crypt` 與 `sha512crypt` 這兩種雜湊都被認為是安全的。

<a id="PGCRYPTO-HASH-SPEED-TABLE"></a>

**表 F.20. 雜湊演算法速度**

<table border="1" class="table" summary="表 F.20. 雜湊演算法速度"><colgroup><col/><col/><col/><col/><col/></colgroup><thead><tr><th>演算法</th><th>每秒雜湊次數</th><th><code class="literal">[a-z]</code> 所需時間</th><th><code class="literal">[A-Za-z0-9]</code> 所需時間</th><th>相對於 <code class="literal">md5 hash</code> 的耗時</th></tr></thead><tbody><tr><td><code class="literal">crypt-bf/8</code></td><td>1792</td><td>4 年</td><td>3927 年</td><td>100k</td></tr><tr><td><code class="literal">crypt-bf/7</code></td><td>3648</td><td>2 年</td><td>1929 年</td><td>50k</td></tr><tr><td><code class="literal">crypt-bf/6</code></td><td>7168</td><td>1 年</td><td>982 年</td><td>25k</td></tr><tr><td><code class="literal">crypt-bf/5</code></td><td>13504</td><td>188 天</td><td>521 年</td><td>12.5k</td></tr><tr><td><code class="literal">crypt-md5</code></td><td>171584</td><td>15 天</td><td>41 年</td><td>1k</td></tr><tr><td><code class="literal">crypt-des</code></td><td>23221568</td><td>157.5 分鐘</td><td>108 天</td><td>7</td></tr><tr><td><code class="literal">sha1</code></td><td>37774272</td><td>90 分鐘</td><td>68 天</td><td>4</td></tr><tr><td><code class="literal">md5</code>（雜湊）</td><td>150085504</td><td>22.5 分鐘</td><td>17 天</td><td>1</td></tr></tbody></table>

<br>

附註：


* 所使用的機器為 Intel Mobile Core i3。
* `crypt-des` 與 `crypt-md5` 演算法的數據取自「John the Ripper」v1.6.38 的 `-test` 輸出。
* `md5 hash` 的數據來自 mdcrack 1.2。
* `sha1` 的數據來自 lcrack-20031130-beta。
* `crypt-bf` 的數據是使用一個對 1000 組 8 字元密碼執行迴圈的簡單程式測得的。如此便能呈現不同迭代次數下的速度。作為參考：`john
  -test` 顯示 `crypt-bf/5` 為每秒 13506 次迴圈。（結果之間的差異非常小，這與 `pgcrypto` 中的 `crypt-bf` 實作和「John the Ripper」所使用的是同一套實作相符。）

請注意，「嘗試所有組合」並不是符合實際的做法。密碼破解通常會借助字典進行，字典中既包含一般單字，也包含這些單字的各種變形。因此，即使是有點像單字的密碼，被破解的速度也可能遠比上述數字所示快得多；而一個 6 個字元、不像單字的密碼則可能逃過破解。也可能逃不過。

[返回 F.26. pgcrypto — 密碼學函式](../pgcrypto.md#pgcrypto)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgcrypto.html)（原文版本：18.6；核對日期：2026-10-23）
