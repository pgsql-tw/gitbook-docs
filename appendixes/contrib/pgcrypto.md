<a id="PGCRYPTO"></a>

## F.26. pgcrypto — 密碼學函式 [#](#pgcrypto) <a href="#pgcrypto" id="pgcrypto"></a>

[F.26.1. 一般雜湊函式](pgcrypto.md#pgcrypto-general-hashing-funcs)

[F.26.2. 密碼雜湊函式](pgcrypto.md#pgcrypto-password-hashing-funcs)

[F.26.3. PGP 加密函式](pgcrypto.md#pgcrypto-pgp-enc-funcs)

[F.26.4. 原始加密函式](pgcrypto.md#pgcrypto-raw-enc-funcs)

[F.26.5. 隨機資料函式](pgcrypto.md#pgcrypto-random-data-funcs)

[F.26.6. OpenSSL 支援函式](pgcrypto.md#pgcrypto-openssl-support-funcs)

[F.26.7. 設定參數](pgcrypto.md#pgcrypto-configuration-parameters)

[F.26.8. 注意事項](pgcrypto.md#pgcrypto-notes)

[F.26.9. 作者](pgcrypto.md#pgcrypto-author)

<a id="id-1.11.7.36.2"></a><a id="id-1.11.7.36.3"></a>

`pgcrypto` 模組為 PostgreSQL 提供密碼學函式。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

`pgcrypto` 需要 OpenSSL；若建置 PostgreSQL 時未選擇 OpenSSL 支援，就不會安裝此模組。

<a id="PGCRYPTO-GENERAL-HASHING-FUNCS"></a>

### F.26.1. 一般雜湊函式 [#](#pgcrypto-general-hashing-funcs) <a href="#pgcrypto-general-hashing-funcs" id="pgcrypto-general-hashing-funcs"></a>

<a id="PGCRYPTO-GENERAL-HASHING-FUNCS-DIGEST"></a>

#### F.26.1.1. `digest()` [#](#PGCRYPTO-GENERAL-HASHING-FUNCS-DIGEST)

<a id="id-1.11.7.36.7.2.2"></a>

```

digest(data text, type text) returns bytea
digest(data bytea, type text) returns bytea
```

計算給定 *`data`* 的二進位雜湊值。*`type`* 是要使用的演算法。標準演算法有 `md5`、`sha1`、`sha224`、`sha256`、`sha384` 與 `sha512`。此外，OpenSSL 所支援的任何摘要演算法都會自動被採用。

若你希望摘要以十六進位字串表示，請對結果使用 `encode()`。例如：

```

CREATE OR REPLACE FUNCTION sha1(bytea) returns text AS $$
    SELECT encode(digest($1, 'sha1'), 'hex')
$$ LANGUAGE SQL STRICT IMMUTABLE;
```

<a id="PGCRYPTO-GENERAL-HASHING-FUNCS-HMAC"></a>

#### F.26.1.2. `hmac()` [#](#PGCRYPTO-GENERAL-HASHING-FUNCS-HMAC)

<a id="id-1.11.7.36.7.3.2"></a>

```

hmac(data text, key text, type text) returns bytea
hmac(data bytea, key bytea, type text) returns bytea
```

以金鑰 *`key`* 計算 *`data`* 的雜湊 MAC。*`type`* 與 `digest()` 中的相同。

這與 `digest()` 類似，但只有知道金鑰才能重新計算雜湊值。這可以防止有人竄改資料、同時也修改雜湊值使其相符的情況。

若金鑰大於雜湊區塊大小，會先對金鑰進行雜湊，再以其結果作為金鑰。

<a id="PGCRYPTO-PASSWORD-HASHING-FUNCS"></a>

### F.26.2. 密碼雜湊函式 [#](#pgcrypto-password-hashing-funcs) <a href="#pgcrypto-password-hashing-funcs" id="pgcrypto-password-hashing-funcs"></a>

函式 `crypt()` 與 `gen_salt()` 是專為雜湊密碼而設計的。`crypt()` 負責進行雜湊，`gen_salt()` 則為其準備演算法參數。

`crypt()` 中的演算法在以下幾個方面與一般的 MD5 或 SHA-1 雜湊演算法不同：

1. 它們很慢。由於資料量很小，這是讓暴力破解密碼變得困難的唯一方法。
2. 它們使用一個稱為*鹽值*（salt）的隨機值，讓密碼相同的使用者具有不同的加密後密碼。這也是防止演算法被反推的額外防禦。
3. 它們會在結果中包含演算法類型，因此以不同演算法雜湊的密碼可以並存。
4. 其中有些是可調適的——也就是說，當電腦變得更快時，你可以調整演算法使其變慢，而不會與現有密碼產生不相容。

[表 F.18](pgcrypto.md#PGCRYPTO-CRYPT-ALGORITHMS)列出 `crypt()` 函式所支援的演算法。

<a id="PGCRYPTO-CRYPT-ALGORITHMS"></a>

**表 F.18. `crypt()` 支援的演算法**

<table border="1" class="table" summary="表 F.18. crypt() 支援的演算法"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/><col class="col5"/><col class="col6"/></colgroup><thead><tr><th>演算法</th><th>密碼最大長度</th><th>可調適？</th><th>鹽值位元數</th><th>輸出長度</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">bf</code></td><td>72</td><td>是</td><td>128</td><td>60</td><td>以 Blowfish 為基礎，2a 變體</td></tr><tr><td><code class="literal">md5</code></td><td>無限制</td><td>否</td><td>48</td><td>34</td><td>以 MD5 為基礎的 crypt</td></tr><tr><td><code class="literal">xdes</code></td><td>8</td><td>是</td><td>24</td><td>20</td><td>擴充 DES</td></tr><tr><td><code class="literal">des</code></td><td>8</td><td>否</td><td>12</td><td>13</td><td>原始的 UNIX crypt</td></tr><tr><td><code class="literal">sha256crypt</code></td><td>無限制</td><td>是</td><td>最多 32</td><td>80</td><td>改編自公開的參考實作
       <a class="ulink" href="https://www.akkadia.org/drepper/SHA-crypt.txt" target="_top">使用 SHA-256 與 SHA-512 的 Unix crypt
       </a>
</td></tr><tr><td><code class="literal">sha512crypt</code></td><td>無限制</td><td>是</td><td>最多 32</td><td>123</td><td>改編自公開的參考實作
       <a class="ulink" href="https://www.akkadia.org/drepper/SHA-crypt.txt" target="_top">使用 SHA-256 與 SHA-512 的 Unix crypt
       </a>
</td></tr></tbody></table>

<br>

<a id="PGCRYPTO-PASSWORD-HASHING-FUNCS-CRYPT"></a>

#### F.26.2.1. `crypt()` [#](#PGCRYPTO-PASSWORD-HASHING-FUNCS-CRYPT)

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

#### F.26.2.2. `gen_salt()` [#](#PGCRYPTO-PASSWORD-HASHING-FUNCS-GEN-SALT)

<a id="id-1.11.7.36.8.8.2"></a>

```

gen_salt(type text [, iter_count integer ]) returns text
```

產生新的隨機鹽值字串，供 `crypt()` 使用。鹽值字串也會告訴 `crypt()` 要使用哪一種演算法。

*`type`* 參數指定雜湊演算法。可接受的類型有：`des`、`xdes`、`md5`、`bf`、`sha256crypt` 與 `sha512crypt`。最後兩種 `sha256crypt` 與 `sha512crypt`，是以 `SHA-2` 為基礎的現代密碼雜湊。

對於具有迭代次數的演算法，*`iter_count`* 參數讓使用者指定迭代次數。次數越高，雜湊密碼所需的時間就越長，因此破解所需的時間也越長。不過，若次數過高，計算一次雜湊的時間可能長達數年——這有點不切實際。若省略 *`iter_count`* 參數，則使用預設的迭代次數。*`iter_count`* 的允許值取決於演算法，列於[表 F.19](pgcrypto.md#PGCRYPTO-ICFC-TABLE)。

<a id="PGCRYPTO-ICFC-TABLE"></a>

**表 F.19. `crypt()` 的迭代次數**

<table border="1" class="table" summary="表 F.19. crypt() 的迭代次數"><colgroup><col/><col/><col/><col/></colgroup><thead><tr><th>演算法</th><th>預設值</th><th>最小值</th><th>最大值</th></tr></thead><tbody><tr><td><code class="literal">xdes</code></td><td>725</td><td>1</td><td>16777215</td></tr><tr><td><code class="literal">bf</code></td><td>6</td><td>4</td><td>31</td></tr><tr><td><code class="literal">sha256crypt, sha512crypt</code></td><td>5000</td><td>1000</td><td>999999999</td></tr></tbody></table>

<br>

對於 `xdes`，還有一項額外限制：迭代次數必須是奇數。

要選擇適當的迭代次數，請考慮原始的 DES crypt 在設計上，是讓當時的硬體每秒執行 4 次雜湊。比每秒 4 次雜湊更慢，可能會降低可用性；比每秒 100 次雜湊更快，則可能太快了。

[表 F.20](pgcrypto.md#PGCRYPTO-HASH-SPEED-TABLE)概述不同雜湊演算法的相對緩慢程度。此表顯示，在假設密碼只包含小寫字母，或包含大小寫字母與數字的情況下，嘗試 8 個字元之密碼的所有字元組合需要多少時間。在 `crypt-bf` 項目中，斜線後面的數字是 `gen_salt` 的 *`iter_count`* 參數。

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

<a id="PGCRYPTO-PGP-ENC-FUNCS"></a>

### F.26.3. PGP 加密函式 [#](#pgcrypto-pgp-enc-funcs) <a href="#pgcrypto-pgp-enc-funcs" id="pgcrypto-pgp-enc-funcs"></a>

這裡的函式實作了 OpenPGP（[RFC 4880](https://datatracker.ietf.org/doc/html/rfc4880)）標準中的加密部分。對稱金鑰加密與公開金鑰加密都有支援。

一則加密的 PGP 訊息由 2 個部分（或稱*封包*）組成：

* 包含工作階段金鑰的封包——以對稱金鑰或公開金鑰加密。
* 包含以工作階段金鑰加密之資料的封包。

以對稱金鑰（亦即密碼）加密時：

1. 給定的密碼會使用 String2Key（S2K）演算法進行雜湊。這與 `crypt()` 的演算法相當類似——刻意設計得很慢，並使用隨機鹽值——但它會產生完整長度的二進位金鑰。
2. 若要求使用獨立的工作階段金鑰，會產生一個新的隨機金鑰。否則，S2K 金鑰會直接作為工作階段金鑰使用。
3. 若要直接使用 S2K 金鑰，則只會將 S2K 設定放入工作階段金鑰封包中。否則，工作階段金鑰會以 S2K 金鑰加密，再放入工作階段金鑰封包中。

以公開金鑰加密時：

1. 產生新的隨機工作階段金鑰。
2. 以公開金鑰將其加密，並放入工作階段金鑰封包中。

無論哪一種情況，要加密的資料都會依下列方式處理：

1. 選擇性的資料處理：壓縮、轉換為 UTF-8，以及／或轉換行尾字元。
2. 在資料前面加上一個由隨機位元組組成的區塊。這相當於使用隨機的 IV（初始化向量）。
3. 附加隨機前綴與資料的 SHA-1 雜湊值。
4. 以上全部內容會以工作階段金鑰加密，並放入資料封包中。

<a id="PGCRYPTO-PGP-ENC-FUNCS-PGP-SYM-ENCRYPT"></a>

#### F.26.3.1. `pgp_sym_encrypt()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-SYM-ENCRYPT)

<a id="id-1.11.7.36.9.11.2"></a><a id="id-1.11.7.36.9.11.3"></a>

```

pgp_sym_encrypt(data text, psw text [, options text ]) returns bytea
pgp_sym_encrypt_bytea(data bytea, psw text [, options text ]) returns bytea
```

以對稱 PGP 金鑰 *`psw`* 加密 *`data`*。
*`options`* 參數可以包含選項設定，如下文所述。

<a id="PGCRYPTO-PGP-ENC-FUNCS-PGP-SYM-DECRYPT"></a>

#### F.26.3.2. `pgp_sym_decrypt()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-SYM-DECRYPT)

<a id="id-1.11.7.36.9.12.2"></a><a id="id-1.11.7.36.9.12.3"></a>

```

pgp_sym_decrypt(msg bytea, psw text [, options text ]) returns text
pgp_sym_decrypt_bytea(msg bytea, psw text [, options text ]) returns bytea
```

解密以對稱金鑰加密的 PGP 訊息。

不允許使用 `pgp_sym_decrypt` 解密 `bytea` 資料。這是為了避免輸出無效的字元資料。使用 `pgp_sym_decrypt_bytea` 解密原本為文字的資料則沒有問題。

*`options`* 參數可以包含選項設定，如下文所述。

<a id="PGCRYPTO-PGP-ENC-FUNCS-PGP-PUB-ENCRYPT"></a>

#### F.26.3.3. `pgp_pub_encrypt()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-PUB-ENCRYPT)

<a id="id-1.11.7.36.9.13.2"></a><a id="id-1.11.7.36.9.13.3"></a>

```

pgp_pub_encrypt(data text, key bytea [, options text ]) returns bytea
pgp_pub_encrypt_bytea(data bytea, key bytea [, options text ]) returns bytea
```

以 PGP 公開金鑰 *`key`* 加密 *`data`*。若傳給此函式的是私密金鑰（secret key），會產生錯誤。

*`options`* 參數可以包含選項設定，如下文所述。

<a id="PGCRYPTO-PGP-ENC-FUNCS-PGP-PUB-DECRYPT"></a>

#### F.26.3.4. `pgp_pub_decrypt()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-PUB-DECRYPT)

<a id="id-1.11.7.36.9.14.2"></a><a id="id-1.11.7.36.9.14.3"></a>

```

pgp_pub_decrypt(msg bytea, key bytea [, psw text [, options text ]]) returns text
pgp_pub_decrypt_bytea(msg bytea, key bytea [, psw text [, options text ]]) returns bytea
```

解密以公開金鑰加密的訊息。*`key`* 必須是與加密時所用公開金鑰相對應的私密金鑰。若私密金鑰受密碼保護，你必須在 *`psw`* 中提供密碼。若沒有密碼，但你想要指定選項，則需要提供空密碼。

不允許使用 `pgp_pub_decrypt` 解密 `bytea` 資料。這是為了避免輸出無效的字元資料。使用 `pgp_pub_decrypt_bytea` 解密原本為文字的資料則沒有問題。

*`options`* 參數可以包含選項設定，如下文所述。

<a id="PGCRYPTO-PGP-ENC-FUNCS-PGP-KEY-ID"></a>

#### F.26.3.5. `pgp_key_id()` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-KEY-ID)

<a id="id-1.11.7.36.9.15.2"></a>

```

pgp_key_id(bytea) returns text
```

`pgp_key_id` 會擷取 PGP 公開金鑰或私密金鑰的金鑰 ID。若給定的是加密訊息，則會傳回加密該資料時所用的金鑰 ID。

它可能傳回 2 個特殊的金鑰 ID：

* `SYMKEY`

  該訊息以對稱金鑰加密。
* `ANYKEY`

  該訊息以公開金鑰加密，但金鑰 ID 已被移除。這表示你必須用你所有的私密金鑰逐一嘗試，才能知道哪一把可以解密。`pgcrypto` 本身不會產生這種訊息。

請注意，不同的金鑰可能具有相同的 ID。這種情況很少見，但屬於正常現象。此時用戶端應用程式應該逐一嘗試以每把金鑰解密，看看哪一把適用——就像處理 `ANYKEY` 一樣。

<a id="PGCRYPTO-PGP-ENC-FUNCS-ARMOR"></a>

#### F.26.3.6. `armor()`, `dearmor()` [#](#PGCRYPTO-PGP-ENC-FUNCS-ARMOR)

<a id="id-1.11.7.36.9.16.2"></a><a id="id-1.11.7.36.9.16.3"></a>

```

armor(data bytea [ , keys text[], values text[] ]) returns text
dearmor(data text) returns bytea
```

這些函式將二進位資料包裝成 PGP ASCII-armor 格式，或從該格式解開；此格式基本上就是附帶 CRC 與額外格式的 Base64。

若指定了 *`keys`* 與 *`values`* 陣列，則會針對每一組鍵／值，在 armor 格式中加入一個 *armor 標頭*（armor header）。兩個陣列都必須是一維的，而且長度必須相同。鍵與值不能包含任何非 ASCII 字元。

<a id="PGCRYPTO-PGP-ENC-FUNCS-PGP-ARMOR-HEADERS"></a>

#### F.26.3.7. `pgp_armor_headers` [#](#PGCRYPTO-PGP-ENC-FUNCS-PGP-ARMOR-HEADERS)

<a id="id-1.11.7.36.9.17.2"></a>

```

pgp_armor_headers(data text, key out text, value out text) returns setof record
```

`pgp_armor_headers()` 會從 *`data`* 中擷取 armor 標頭。傳回值是一組資料列，具有鍵（key）與值（value）兩個欄位。若鍵或值包含任何非 ASCII 字元，會被視為 UTF-8。

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS"></a>

#### F.26.3.8. PGP 函式的選項 [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS)

選項的命名與 GnuPG 類似。選項的值應該寫在等號之後；各選項之間以逗號分隔。例如：

```

pgp_sym_encrypt(data, psw, 'compress-algo=1, cipher-algo=aes256')
```

除了 `convert-crlf` 之外，所有選項都只適用於加密函式。解密函式會從 PGP 資料中取得參數。

譯註：原文此句未將下文的 ignore-cipher-failure 選項列為例外；依該選項的「適用於」說明（F.26.3.8.12），它只適用於 pgp_sym_decrypt 與 pgp_pub_decrypt 這兩個解密函式。

最值得關注的選項大概是 `compress-algo` 與 `unicode-mode`。其餘選項應該都有合理的預設值。

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS-CIPHER-ALGO"></a>

##### F.26.3.8.1. cipher-algo [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-CIPHER-ALGO)

要使用的加密演算法。

<br>
值：bf, aes128, aes192, aes256, 3des, cast5<br>
預設：aes128<br>
適用於：pgp_sym_encrypt, pgp_pub_encrypt<br>

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS-COMPRESS-ALGO"></a>

##### F.26.3.8.2. compress-algo [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-COMPRESS-ALGO)

要使用的壓縮演算法。只有在 PostgreSQL 以 zlib 建置時才可使用。

<br>
值：<br>
  0 - 不壓縮<br>
  1 - ZIP 壓縮<br>
  2 - ZLIB 壓縮（= ZIP 加上中繼資料與區塊 CRC）<br>
預設：0<br>
適用於：pgp_sym_encrypt, pgp_pub_encrypt<br>

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS-COMPRESS-LEVEL"></a>

##### F.26.3.8.3. compress-level [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-COMPRESS-LEVEL)

壓縮的程度。等級越高，壓縮後越小，但速度較慢。0 會停用壓縮。

<br>
值：0, 1-9<br>
預設：6<br>
適用於：pgp_sym_encrypt, pgp_pub_encrypt<br>

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS-CONVERT-CRLF"></a>

##### F.26.3.8.4. convert-crlf [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-CONVERT-CRLF)

是否在加密時將 `\n` 轉換為 `\r\n`，並在解密時將 `\r\n` 轉換為 `\n`。RFC 4880 規定文字資料應該使用 `\r\n` 換行字元儲存。使用此選項可獲得完全符合 RFC 的行為。

<br>
值：0, 1<br>
預設：0<br>
適用於：pgp_sym_encrypt, pgp_pub_encrypt, pgp_sym_decrypt, pgp_pub_decrypt<br>

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS-DISABLE-MDC"></a>

##### F.26.3.8.5. disable-mdc [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-DISABLE-MDC)

不使用 SHA-1 保護資料。使用此選項唯一的正當理由，是為了與早於 RFC 4880 加入受 SHA-1 保護之封包的老舊 PGP 產品相容。近期的 gnupg.org 與 pgp.com 軟體都能良好支援受 SHA-1 保護的封包。

<br>
值：0, 1<br>
預設：0<br>
適用於：pgp_sym_encrypt, pgp_pub_encrypt<br>

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS-SESS-KEY"></a>

##### F.26.3.8.6. sess-key [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-SESS-KEY)

使用獨立的工作階段金鑰。公開金鑰加密一律使用獨立的工作階段金鑰；此選項是供對稱金鑰加密使用，對稱金鑰加密預設會直接使用 S2K 金鑰。

<br>
值：0, 1<br>
預設：0<br>
適用於：pgp_sym_encrypt<br>

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-MODE"></a>

##### F.26.3.8.7. s2k-mode [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-MODE)

要使用的 S2K 演算法。

<br>
值：<br>
  0 - 不使用鹽值。危險！<br>
  1 - 使用鹽值，但迭代次數固定。<br>
  3 - 可變迭代次數。<br>
預設：3<br>
適用於：pgp_sym_encrypt<br>

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-COUNT"></a>

##### F.26.3.8.8. s2k-count [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-COUNT)

S2K 演算法要使用的迭代次數。它必須是介於 1024 與 65011712 之間（含兩端）的值。

<br>
預設：介於 65536 與 253952 之間的隨機值<br>
適用於：pgp_sym_encrypt，且僅限 s2k-mode=3 時<br>

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-DIGEST-ALGO"></a>

##### F.26.3.8.9. s2k-digest-algo [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-DIGEST-ALGO)

S2K 計算中要使用的摘要演算法。

<br>
值：md5, sha1<br>
預設：sha1<br>
適用於：pgp_sym_encrypt<br>

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-CIPHER-ALGO"></a>

##### F.26.3.8.10. s2k-cipher-algo [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-S2K-CIPHER-ALGO)

加密獨立工作階段金鑰時要使用的加密演算法。

<br>
值：bf, aes, aes128, aes192, aes256<br>
預設：使用 cipher-algo 的設定<br>
適用於：pgp_sym_encrypt<br>

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS-UNICODE-MODE"></a>

##### F.26.3.8.11. unicode-mode [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-UNICODE-MODE)

是否將文字資料從資料庫內部編碼轉換為 UTF-8，以及反向轉換回來。若你的資料庫已經是 UTF-8，則不會進行轉換，但訊息會被標記為 UTF-8。若未使用此選項，則不會加上此標記。

<br>
值：0, 1<br>
預設：0<br>
適用於：pgp_sym_encrypt, pgp_pub_encrypt<br>

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS-IGNORE-CIPHER-FAILURE"></a>

##### F.26.3.8.12. ignore-cipher-failure [#](#PGCRYPTO-PGP-ENC-FUNCS-OPTS-IGNORE-CIPHER-FAILURE)

危險！指示 pgcrypto 完全忽略所用 OpenSSL 加密演算法的失敗，藉此使用一種不正確的解密演算法，其行為與 CVE-2026-14663 修正之前的歷史行為相符。此選項僅供需要復原錯誤加密訊息的使用者使用；這類訊息是在當時指定的 `cipher-algo` 於所用的 OpenSSL 設定下無法使用時所建立的。啟用 `ignore-cipher-failure` 時，此類有缺陷的訊息不需要正確的解密金鑰即可解密，因此無法保證解密後的明文確實出自金鑰持有者。

與此相對的情況是：訊息已正確加密，但產生它的加密演算法在目前的 OpenSSL 設定下無法使用。要透過 `pgcrypto` 復原這類明文，必須讓 OpenSSL 能使用實際的加密演算法，例如啟用適當的提供者（provider）。在這種情況下，`ignore-cipher-failure` 既非必要，也沒有幫助。若使用此選項對正確加密之訊息所做的「解密」碰巧通過了 PGP 完整性檢查，該結果只是巧合，並不代表復原的明文值得信任。

<br>
值：0, 1<br>
預設：0<br>
適用於：pgp_sym_decrypt, pgp_pub_decrypt<br>

<a id="PGCRYPTO-PGP-ENC-FUNCS-GNUPG"></a>

#### F.26.3.9. 使用 GnuPG 產生 PGP 金鑰 [#](#PGCRYPTO-PGP-ENC-FUNCS-GNUPG)

產生新金鑰：

```

gpg --gen-key
```

建議的金鑰類型為「DSA and Elgamal」。

若要使用 RSA 加密，你必須先建立 DSA 或 RSA 的僅簽章金鑰作為主金鑰，然後使用 `gpg --edit-key` 加入 RSA 加密子金鑰。

列出金鑰：

```

gpg --list-secret-keys
```

以 ASCII-armor 格式匯出公開金鑰：

```

gpg -a --export KEYID > public.key
```

以 ASCII-armor 格式匯出私密金鑰：

```

gpg -a --export-secret-keys KEYID > secret.key
```

將這些金鑰交給 PGP 函式之前，你需要先對它們使用 `dearmor()`。或者，若你能處理二進位資料，也可以從命令中省略 `-a`。

更多細節請參閱 `man gpg`、[The GNU Privacy Handbook](https://www.gnupg.org/gph/en/manual.html)，以及 <https://www.gnupg.org/> 上的其他文件。

<a id="PGCRYPTO-PGP-ENC-FUNCS-LIMITATIONS"></a>

#### F.26.3.10. PGP 程式碼的限制 [#](#PGCRYPTO-PGP-ENC-FUNCS-LIMITATIONS)

* 不支援簽章。這也表示不會檢查加密子金鑰是否屬於主金鑰。
* 不支援以加密金鑰作為主金鑰。由於一般不建議這種做法，這應該不成問題。
* 不支援多個子金鑰。由於這是常見的做法，這看起來可能是個問題。另一方面，你不應該將平常使用的 GPG/PGP 金鑰用於 `pgcrypto`，而應該建立新的金鑰，因為使用情境相當不同。

<a id="PGCRYPTO-RAW-ENC-FUNCS"></a>

### F.26.4. 原始加密函式 [#](#pgcrypto-raw-enc-funcs) <a href="#pgcrypto-raw-enc-funcs" id="pgcrypto-raw-enc-funcs"></a>

這些函式只會對資料執行加密演算法，不具備 PGP 加密的任何進階功能。因此它們有幾個主要問題：

1. 它們直接將使用者金鑰作為加密金鑰。
2. 它們不提供任何完整性檢查，無法得知加密資料是否遭到修改。
3. 它們預期使用者自行管理所有加密參數，甚至包括 IV。
4. 它們不處理文字。

因此，在引入 PGP 加密之後，不建議使用原始加密函式。

<a id="id-1.11.7.36.10.5"></a><a id="id-1.11.7.36.10.6"></a><a id="id-1.11.7.36.10.7"></a><a id="id-1.11.7.36.10.8"></a>

```

encrypt(data bytea, key bytea, type text) returns bytea
decrypt(data bytea, key bytea, type text) returns bytea

encrypt_iv(data bytea, key bytea, iv bytea, type text) returns bytea
decrypt_iv(data bytea, key bytea, iv bytea, type text) returns bytea
```

使用 *`type`* 所指定的加密方法加密／解密資料。*`type`* 字串的語法為：

```

algorithm [ - mode ] [ /pad: padding ]
```

其中 *`algorithm`* 為下列之一：

* `bf` — Blowfish
* `aes` — AES（Rijndael-128、-192 或 -256）

而 *`mode`* 為下列之一：

* `cbc` — 下一個區塊取決於前一個區塊（預設）
* `cfb` — 下一個區塊取決於前一個已加密的區塊
* `ecb` — 每個區塊分別加密（僅供測試）

而 *`padding`* 為下列之一：

* `pkcs` — 資料可以是任意長度（預設）
* `none` — 資料長度必須是加密區塊大小的倍數

因此，舉例來說，以下兩者是等價的：

```

encrypt(data, 'fooz', 'bf')
encrypt(data, 'fooz', 'bf-cbc/pad:pkcs')
```

在 `encrypt_iv` 與 `decrypt_iv` 中，*`iv`* 參數是 CBC 與 CFB 模式的初始值；ECB 模式會忽略此參數。若其長度不恰好等於區塊大小，會被截斷或以零填補。在沒有此參數的函式中，其預設為全零。

<a id="PGCRYPTO-RANDOM-DATA-FUNCS"></a>

### F.26.5. 隨機資料函式 [#](#pgcrypto-random-data-funcs) <a href="#pgcrypto-random-data-funcs" id="pgcrypto-random-data-funcs"></a>

<a id="id-1.11.7.36.11.2"></a>

```

gen_random_bytes(count integer) returns bytea
```

傳回 *`count`* 個密碼學強度的隨機位元組。每次最多可以取出 1024 個位元組。這是為了避免耗盡隨機數產生器的熵池。

<a id="id-1.11.7.36.11.5"></a>

```

gen_random_uuid() returns uuid
```

傳回第 4 版（隨機）UUID。（已過時，此函式在內部會呼叫同名的[核心函式](../../the-sql-language/functions/functions-uuid.md)。）

<a id="PGCRYPTO-OPENSSL-SUPPORT-FUNCS"></a>

### F.26.6. OpenSSL 支援函式 [#](#pgcrypto-openssl-support-funcs) <a href="#pgcrypto-openssl-support-funcs" id="pgcrypto-openssl-support-funcs"></a>

<a id="id-1.11.7.36.12.2"></a>

```

fips_mode() returns boolean
```

若 OpenSSL 在啟用 FIPS 模式下執行，則傳回 `true`，否則傳回 `false`。

<a id="PGCRYPTO-CONFIGURATION-PARAMETERS"></a>

### F.26.7. 設定參數 [#](#pgcrypto-configuration-parameters) <a href="#pgcrypto-configuration-parameters" id="pgcrypto-configuration-parameters"></a>

有一個設定參數可控制 `pgcrypto` 的行為。

<a id="PGCRYPTO-CONFIGURATION-PARAMETERS-BUILTIN_CRYPTO_ENABLED"></a>

`pgcrypto.builtin_crypto_enabled` (`enum`) <a id="id-1.11.7.36.13.3.1.1.3"></a> [#](#PGCRYPTO-CONFIGURATION-PARAMETERS-BUILTIN_CRYPTO_ENABLED)

`pgcrypto.builtin_crypto_enabled` 決定內建的密碼學函式 `gen_salt()` 與 `crypt()` 是否可供使用。設為 `off` 會停用這些函式。`on`（預設值）讓這些函式正常運作。`fips` 則會在偵測到 OpenSSL 以 FIPS 模式運作時停用這些函式。

`pgp_sym_encrypt()` 與 `pgp_pub_encrypt()` 不使用內建的密碼學實作，因此不受影響。

一般使用時，此參數是在 `postgresql.conf` 中設定，不過超級使用者也可以在自己的工作階段中即時變更它。

<a id="PGCRYPTO-NOTES"></a>

### F.26.8. 注意事項 [#](#pgcrypto-notes) <a href="#pgcrypto-notes" id="pgcrypto-notes"></a>

<a id="PGCRYPTO-NOTES-CONFIG"></a>

#### F.26.8.1. 設定 [#](#PGCRYPTO-NOTES-CONFIG)

`pgcrypto` 會依據 PostgreSQL 主要 `configure` 指令碼的偵測結果自行設定。會影響它的選項有 `--with-zlib` 與 `--with-ssl=openssl`。

以 zlib 編譯時，PGP 加密函式可以在加密前先壓縮資料。

`pgcrypto` 需要 OpenSSL。否則，它不會被建置或安裝。

以 OpenSSL 3.0.0 及之後的版本編譯時，必須在 `openssl.cnf` 設定檔中啟用名為 legacy 的提供者（provider），才能使用 DES 或 Blowfish 等較舊的加密演算法。

<a id="PGCRYPTO-NOTES-NULL-HANDLING"></a>

#### F.26.8.2. NULL 處理 [#](#PGCRYPTO-NOTES-NULL-HANDLING)

依照 SQL 的標準做法，只要有任何引數為 NULL，所有函式都會傳回 NULL。若使用時不夠謹慎，這可能造成安全風險。

<a id="PGCRYPTO-NOTES-SEC-LIMITS"></a>

#### F.26.8.3. 安全性限制 [#](#PGCRYPTO-NOTES-SEC-LIMITS)

所有 `pgcrypto` 函式都在資料庫伺服器內執行。這表示所有資料與密碼都會以明文在 `pgcrypto` 與用戶端應用程式之間傳遞。因此你必須：

1. 在本機連線，或使用 SSL 連線。
2. 同時信任系統管理員與資料庫管理員。

若無法做到，最好在用戶端應用程式內進行加解密。

此實作無法抵禦[旁通道攻擊](https://en.wikipedia.org/wiki/Side-channel_attack)。例如，對於給定大小的不同密文，`pgcrypto` 解密函式完成所需的時間會有所不同。

<a id="PGCRYPTO-AUTHOR"></a>

### F.26.9. 作者 [#](#pgcrypto-author) <a href="#pgcrypto-author" id="pgcrypto-author"></a>

Marko Kreen `<markokr@gmail.com>`

`pgcrypto` 使用了下列來源的程式碼：

<table border="1" class="informaltable"><colgroup><col/><col/><col/></colgroup><thead><tr><th>演算法</th><th>作者</th><th>來源</th></tr></thead><tbody><tr><td>DES crypt</td><td>David Burren 等人</td><td>FreeBSD libcrypt</td></tr><tr><td>MD5 crypt</td><td>Poul-Henning Kamp</td><td>FreeBSD libcrypt</td></tr><tr><td>Blowfish crypt</td><td>Solar Designer</td><td>www.openwall.com</td></tr></tbody></table>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgcrypto.html)（原文版本：18.6；核對日期：2026-10-23）
