<a id="PGCRYPTO"></a>

# F.28. pgcrypto

[F.28.1. General Hashing Functions](#id-1.11.7.37.7)

[F.28.2. Password Hashing Functions](#id-1.11.7.37.8)

[F.28.3. PGP Encryption Functions](#id-1.11.7.37.9)

[F.28.4. Raw Encryption Functions](#id-1.11.7.37.10)

[F.28.5. Random-Data Functions](#id-1.11.7.37.11)

[F.28.6. Notes](#id-1.11.7.37.12)

[F.28.7. Author](#id-1.11.7.37.13)

<a id="id-1.11.7.37.2"></a><a id="id-1.11.7.37.3"></a>

The `pgcrypto` module provides cryptographic functions for PostgreSQL.

This module is considered “trusted”, that is, it can be installed by non-superusers who have `CREATE` privilege on the current database.

`pgcrypto` requires OpenSSL and won't be installed if OpenSSL support was not selected when PostgreSQL was built.

<a id="id-1.11.7.37.7"></a>

## F.28.1. General Hashing Functions

<a id="id-1.11.7.37.7.2"></a>

### F.28.1.1. `digest()`

<a id="id-1.11.7.37.7.2.2"></a>

```

digest(data text, type text) returns bytea
digest(data bytea, type text) returns bytea
```

Computes a binary hash of the given <em class="parameter"><code>data</code></em>. <em class="parameter"><code>type</code></em> is the algorithm to use. Standard algorithms are `md5`, `sha1`, `sha224`, `sha256`, `sha384` and `sha512`. Moreover, any digest algorithm OpenSSL supports is automatically picked up.

If you want the digest as a hexadecimal string, use `encode()` on the result. For example:

```

CREATE OR REPLACE FUNCTION sha1(bytea) returns text AS $$
    SELECT encode(digest($1, 'sha1'), 'hex')
$$ LANGUAGE SQL STRICT IMMUTABLE;
```

<a id="id-1.11.7.37.7.3"></a>

### F.28.1.2. `hmac()`

<a id="id-1.11.7.37.7.3.2"></a>

```

hmac(data text, key text, type text) returns bytea
hmac(data bytea, key bytea, type text) returns bytea
```

Calculates hashed MAC for <em class="parameter"><code>data</code></em> with key <em class="parameter"><code>key</code></em>. <em class="parameter"><code>type</code></em> is the same as in `digest()`.

This is similar to `digest()` but the hash can only be recalculated knowing the key. This prevents the scenario of someone altering data and also changing the hash to match.

If the key is larger than the hash block size it will first be hashed and the result will be used as key.

<a id="id-1.11.7.37.8"></a>

## F.28.2. Password Hashing Functions

The functions `crypt()` and `gen_salt()` are specifically designed for hashing passwords. `crypt()` does the hashing and `gen_salt()` prepares algorithm parameters for it.

The algorithms in `crypt()` differ from the usual MD5 or SHA1 hashing algorithms in the following respects:

1. They are slow. As the amount of data is so small, this is the only way to make brute-forcing passwords hard.
2. They use a random value, called the <em class="firstterm">salt</em>, so that users having the same password will have different encrypted passwords. This is also an additional defense against reversing the algorithm.
3. They include the algorithm type in the result, so passwords hashed with different algorithms can co-exist.
4. Some of them are adaptive — that means when computers get faster, you can tune the algorithm to be slower, without introducing incompatibility with existing passwords.

[Table F.16](#PGCRYPTO-CRYPT-ALGORITHMS) lists the algorithms supported by the `crypt()` function.

<a id="PGCRYPTO-CRYPT-ALGORITHMS"></a>

<strong>Table F.16. Supported Algorithms for <code class="function">crypt()</code></strong>

<table border="1" class="table" summary="Supported Algorithms for crypt()">
<colgroup>
<col/>
<col/>
<col/>
<col/>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>Algorithm</th>
<th>Max Password Length</th>
<th>Adaptive?</th>
<th>Salt Bits</th>
<th>Output Length</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code class="literal">bf</code></td>
<td>72</td>
<td>yes</td>
<td>128</td>
<td>60</td>
<td>Blowfish-based, variant 2a</td>
</tr>
<tr>
<td><code class="literal">md5</code></td>
<td>unlimited</td>
<td>no</td>
<td>48</td>
<td>34</td>
<td>MD5-based crypt</td>
</tr>
<tr>
<td><code class="literal">xdes</code></td>
<td>8</td>
<td>yes</td>
<td>24</td>
<td>20</td>
<td>Extended DES</td>
</tr>
<tr>
<td><code class="literal">des</code></td>
<td>8</td>
<td>no</td>
<td>12</td>
<td>13</td>
<td>Original UNIX crypt</td>
</tr>
</tbody>
</table>


<a id="id-1.11.7.37.8.7"></a>

### F.28.2.1. `crypt()`

<a id="id-1.11.7.37.8.7.2"></a>

```

crypt(password text, salt text) returns text
```

Calculates a crypt(3)-style hash of <em class="parameter"><code>password</code></em>. When storing a new password, you need to use `gen_salt()` to generate a new <em class="parameter"><code>salt</code></em> value. To check a password, pass the stored hash value as <em class="parameter"><code>salt</code></em>, and test whether the result matches the stored value.

Example of setting a new password:

```

UPDATE ... SET pswhash = crypt('new password', gen_salt('md5'));
```

Example of authentication:

```

SELECT (pswhash = crypt('entered password', pswhash)) AS pswmatch FROM ... ;
```

This returns `true` if the entered password is correct.

<a id="id-1.11.7.37.8.8"></a>

### F.28.2.2. `gen_salt()`

<a id="id-1.11.7.37.8.8.2"></a>

```

gen_salt(type text [, iter_count integer ]) returns text
```

Generates a new random salt string for use in `crypt()`. The salt string also tells `crypt()` which algorithm to use.

The <em class="parameter"><code>type</code></em> parameter specifies the hashing algorithm. The accepted types are: `des`, `xdes`, `md5` and `bf`.

The <em class="parameter"><code>iter&#95;count</code></em> parameter lets the user specify the iteration count, for algorithms that have one. The higher the count, the more time it takes to hash the password and therefore the more time to break it. Although with too high a count the time to calculate a hash may be several years — which is somewhat impractical. If the <em class="parameter"><code>iter&#95;count</code></em> parameter is omitted, the default iteration count is used. Allowed values for <em class="parameter"><code>iter&#95;count</code></em> depend on the algorithm and are shown in [Table F.17](#PGCRYPTO-ICFC-TABLE).

<a id="PGCRYPTO-ICFC-TABLE"></a>

<strong>Table F.17. Iteration Counts for <code class="function">crypt()</code></strong>

<table border="1" class="table" summary="Iteration Counts for crypt()">
<colgroup>
<col/>
<col/>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>Algorithm</th>
<th>Default</th>
<th>Min</th>
<th>Max</th>
</tr>
</thead>
<tbody>
<tr>
<td><code class="literal">xdes</code></td>
<td>725</td>
<td>1</td>
<td>16777215</td>
</tr>
<tr>
<td><code class="literal">bf</code></td>
<td>6</td>
<td>4</td>
<td>31</td>
</tr>
</tbody>
</table>



For `xdes` there is an additional limitation that the iteration count must be an odd number.

To pick an appropriate iteration count, consider that the original DES crypt was designed to have the speed of 4 hashes per second on the hardware of that time. Slower than 4 hashes per second would probably dampen usability. Faster than 100 hashes per second is probably too fast.

[Table F.18](#PGCRYPTO-HASH-SPEED-TABLE) gives an overview of the relative slowness of different hashing algorithms. The table shows how much time it would take to try all combinations of characters in an 8-character password, assuming that the password contains either only lower case letters, or upper- and lower-case letters and numbers. In the `crypt-bf` entries, the number after a slash is the <em class="parameter"><code>iter&#95;count</code></em> parameter of `gen_salt`.

<a id="PGCRYPTO-HASH-SPEED-TABLE"></a>

<strong>Table F.18. Hash Algorithm Speeds</strong>

<table border="1" class="table" summary="Hash Algorithm Speeds">
<colgroup>
<col/>
<col/>
<col/>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>Algorithm</th>
<th>Hashes/sec</th>
<th>For <code class="literal">[a-z]</code></th>
<th>For <code class="literal">[A-Za-z0-9]</code></th>
<th>Duration relative to <code class="literal">md5 hash</code></th>
</tr>
</thead>
<tbody>
<tr>
<td><code class="literal">crypt-bf/8</code></td>
<td>1792</td>
<td>4 years</td>
<td>3927 years</td>
<td>100k</td>
</tr>
<tr>
<td><code class="literal">crypt-bf/7</code></td>
<td>3648</td>
<td>2 years</td>
<td>1929 years</td>
<td>50k</td>
</tr>
<tr>
<td><code class="literal">crypt-bf/6</code></td>
<td>7168</td>
<td>1 year</td>
<td>982 years</td>
<td>25k</td>
</tr>
<tr>
<td><code class="literal">crypt-bf/5</code></td>
<td>13504</td>
<td>188 days</td>
<td>521 years</td>
<td>12.5k</td>
</tr>
<tr>
<td><code class="literal">crypt-md5</code></td>
<td>171584</td>
<td>15 days</td>
<td>41 years</td>
<td>1k</td>
</tr>
<tr>
<td><code class="literal">crypt-des</code></td>
<td>23221568</td>
<td>157.5 minutes</td>
<td>108 days</td>
<td>7</td>
</tr>
<tr>
<td><code class="literal">sha1</code></td>
<td>37774272</td>
<td>90 minutes</td>
<td>68 days</td>
<td>4</td>
</tr>
<tr>
<td><code class="literal">md5</code> (hash)</td>
<td>150085504</td>
<td>22.5 minutes</td>
<td>17 days</td>
<td>1</td>
</tr>
</tbody>
</table>



Notes:

* The machine used is an Intel Mobile Core i3.
* `crypt-des` and `crypt-md5` algorithm numbers are taken from John the Ripper v1.6.38 `-test` output.
* `md5 hash` numbers are from mdcrack 1.2.
* `sha1` numbers are from lcrack-20031130-beta.
* `crypt-bf` numbers are taken using a simple program that loops over 1000 8-character passwords. That way I can show the speed with different numbers of iterations. For reference: `john -test` shows 13506 loops/sec for `crypt-bf/5`. (The very small difference in results is in accordance with the fact that the `crypt-bf` implementation in `pgcrypto` is the same one used in John the Ripper.)

Note that “try all combinations” is not a realistic exercise. Usually password cracking is done with the help of dictionaries, which contain both regular words and various mutations of them. So, even somewhat word-like passwords could be cracked much faster than the above numbers suggest, while a 6-character non-word-like password may escape cracking. Or not.

<a id="id-1.11.7.37.9"></a>

## F.28.3. PGP Encryption Functions

The functions here implement the encryption part of the OpenPGP ([RFC 4880](https://datatracker.ietf.org/doc/html/rfc4880)) standard. Supported are both symmetric-key and public-key encryption.

An encrypted PGP message consists of 2 parts, or <em class="firstterm">packets</em>:

* Packet containing a session key — either symmetric-key or public-key encrypted.
* Packet containing data encrypted with the session key.

When encrypting with a symmetric key (i.e., a password):

1. The given password is hashed using a String2Key (S2K) algorithm. This is rather similar to `crypt()` algorithms — purposefully slow and with random salt — but it produces a full-length binary key.
2. If a separate session key is requested, a new random key will be generated. Otherwise the S2K key will be used directly as the session key.
3. If the S2K key is to be used directly, then only S2K settings will be put into the session key packet. Otherwise the session key will be encrypted with the S2K key and put into the session key packet.

When encrypting with a public key:

1. A new random session key is generated.
2. It is encrypted using the public key and put into the session key packet.

In either case the data to be encrypted is processed as follows:

1. Optional data-manipulation: compression, conversion to UTF-8, and/or conversion of line-endings.
2. The data is prefixed with a block of random bytes. This is equivalent to using a random IV.
3. A SHA1 hash of the random prefix and data is appended.
4. All this is encrypted with the session key and placed in the data packet.

<a id="id-1.11.7.37.9.11"></a>

### F.28.3.1. `pgp_sym_encrypt()`

<a id="id-1.11.7.37.9.11.2"></a><a id="id-1.11.7.37.9.11.3"></a>

```

pgp_sym_encrypt(data text, psw text [, options text ]) returns bytea
pgp_sym_encrypt_bytea(data bytea, psw text [, options text ]) returns bytea
```

Encrypt <em class="parameter"><code>data</code></em> with a symmetric PGP key <em class="parameter"><code>psw</code></em>. The <em class="parameter"><code>options</code></em> parameter can contain option settings, as described below.

<a id="id-1.11.7.37.9.12"></a>

### F.28.3.2. `pgp_sym_decrypt()`

<a id="id-1.11.7.37.9.12.2"></a><a id="id-1.11.7.37.9.12.3"></a>

```

pgp_sym_decrypt(msg bytea, psw text [, options text ]) returns text
pgp_sym_decrypt_bytea(msg bytea, psw text [, options text ]) returns bytea
```

Decrypt a symmetric-key-encrypted PGP message.

Decrypting `bytea` data with `pgp_sym_decrypt` is disallowed. This is to avoid outputting invalid character data. Decrypting originally textual data with `pgp_sym_decrypt_bytea` is fine.

The <em class="parameter"><code>options</code></em> parameter can contain option settings, as described below.

<a id="id-1.11.7.37.9.13"></a>

### F.28.3.3. `pgp_pub_encrypt()`

<a id="id-1.11.7.37.9.13.2"></a><a id="id-1.11.7.37.9.13.3"></a>

```

pgp_pub_encrypt(data text, key bytea [, options text ]) returns bytea
pgp_pub_encrypt_bytea(data bytea, key bytea [, options text ]) returns bytea
```

Encrypt <em class="parameter"><code>data</code></em> with a public PGP key <em class="parameter"><code>key</code></em>. Giving this function a secret key will produce an error.

The <em class="parameter"><code>options</code></em> parameter can contain option settings, as described below.

<a id="id-1.11.7.37.9.14"></a>

### F.28.3.4. `pgp_pub_decrypt()`

<a id="id-1.11.7.37.9.14.2"></a><a id="id-1.11.7.37.9.14.3"></a>

```

pgp_pub_decrypt(msg bytea, key bytea [, psw text [, options text ]]) returns text
pgp_pub_decrypt_bytea(msg bytea, key bytea [, psw text [, options text ]]) returns bytea
```

Decrypt a public-key-encrypted message. <em class="parameter"><code>key</code></em> must be the secret key corresponding to the public key that was used to encrypt. If the secret key is password-protected, you must give the password in <em class="parameter"><code>psw</code></em>. If there is no password, but you want to specify options, you need to give an empty password.

Decrypting `bytea` data with `pgp_pub_decrypt` is disallowed. This is to avoid outputting invalid character data. Decrypting originally textual data with `pgp_pub_decrypt_bytea` is fine.

The <em class="parameter"><code>options</code></em> parameter can contain option settings, as described below.

<a id="id-1.11.7.37.9.15"></a>

### F.28.3.5. `pgp_key_id()`

<a id="id-1.11.7.37.9.15.2"></a>

```

pgp_key_id(bytea) returns text
```

`pgp_key_id` extracts the key ID of a PGP public or secret key. Or it gives the key ID that was used for encrypting the data, if given an encrypted message.

It can return 2 special key IDs:

* `SYMKEY`

  The message is encrypted with a symmetric key.
* `ANYKEY`

  The message is public-key encrypted, but the key ID has been removed. That means you will need to try all your secret keys on it to see which one decrypts it. `pgcrypto` itself does not produce such messages.

Note that different keys may have the same ID. This is rare but a normal event. The client application should then try to decrypt with each one, to see which fits — like handling `ANYKEY`.

<a id="id-1.11.7.37.9.16"></a>

### F.28.3.6. `armor()`, `dearmor()`

<a id="id-1.11.7.37.9.16.2"></a><a id="id-1.11.7.37.9.16.3"></a>

```

armor(data bytea [ , keys text[], values text[] ]) returns text
dearmor(data text) returns bytea
```

These functions wrap/unwrap binary data into PGP ASCII-armor format, which is basically Base64 with CRC and additional formatting.

If the <em class="parameter"><code>keys</code></em> and <em class="parameter"><code>values</code></em> arrays are specified, an <em class="firstterm">armor header</em> is added to the armored format for each key/value pair. Both arrays must be single-dimensional, and they must be of the same length. The keys and values cannot contain any non-ASCII characters.

<a id="id-1.11.7.37.9.17"></a>

### F.28.3.7. `pgp_armor_headers`

<a id="id-1.11.7.37.9.17.2"></a>

```

pgp_armor_headers(data text, key out text, value out text) returns setof record
```

`pgp_armor_headers()` extracts the armor headers from <em class="parameter"><code>data</code></em>. The return value is a set of rows with two columns, key and value. If the keys or values contain any non-ASCII characters, they are treated as UTF-8.

<a id="id-1.11.7.37.9.18"></a>

### F.28.3.8. Options for PGP Functions

Options are named to be similar to GnuPG. An option's value should be given after an equal sign; separate options from each other with commas. For example:

```

pgp_sym_encrypt(data, psw, 'compress-algo=1, cipher-algo=aes256')
```

All of the options except `convert-crlf` apply only to encrypt functions. Decrypt functions get the parameters from the PGP data.

The most interesting options are probably `compress-algo` and `unicode-mode`. The rest should have reasonable defaults.

<a id="id-1.11.7.37.9.18.5"></a>

#### F.28.3.8.1. cipher-algo

Which cipher algorithm to use.

<br>
Values: bf, aes128, aes192, aes256, 3des, cast5<br>
Default: aes128<br>
Applies to: pgp_sym_encrypt, pgp_pub_encrypt<br>

<a id="id-1.11.7.37.9.18.6"></a>

#### F.28.3.8.2. compress-algo

Which compression algorithm to use. Only available if PostgreSQL was built with zlib.

<br>
Values:<br>
  0 - no compression<br>
  1 - ZIP compression<br>
  2 - ZLIB compression (= ZIP plus meta-data and block CRCs)<br>
Default: 0<br>
Applies to: pgp_sym_encrypt, pgp_pub_encrypt<br>

<a id="id-1.11.7.37.9.18.7"></a>

#### F.28.3.8.3. compress-level

How much to compress. Higher levels compress smaller but are slower. 0 disables compression.

<br>
Values: 0, 1-9<br>
Default: 6<br>
Applies to: pgp_sym_encrypt, pgp_pub_encrypt<br>

<a id="id-1.11.7.37.9.18.8"></a>

#### F.28.3.8.4. convert-crlf

Whether to convert `\n` into `\r\n` when encrypting and `\r\n` to `\n` when decrypting. RFC 4880 specifies that text data should be stored using `\r\n` line-feeds. Use this to get fully RFC-compliant behavior.

<br>
Values: 0, 1<br>
Default: 0<br>
Applies to: pgp_sym_encrypt, pgp_pub_encrypt, pgp_sym_decrypt, pgp_pub_decrypt<br>

<a id="id-1.11.7.37.9.18.9"></a>

#### F.28.3.8.5. disable-mdc

Do not protect data with SHA-1. The only good reason to use this option is to achieve compatibility with ancient PGP products, predating the addition of SHA-1 protected packets to RFC 4880. Recent gnupg.org and pgp.com software supports it fine.

<br>
Values: 0, 1<br>
Default: 0<br>
Applies to: pgp_sym_encrypt, pgp_pub_encrypt<br>

<a id="id-1.11.7.37.9.18.10"></a>

#### F.28.3.8.6. sess-key

Use separate session key. Public-key encryption always uses a separate session key; this option is for symmetric-key encryption, which by default uses the S2K key directly.

<br>
Values: 0, 1<br>
Default: 0<br>
Applies to: pgp_sym_encrypt<br>

<a id="id-1.11.7.37.9.18.11"></a>

#### F.28.3.8.7. s2k-mode

Which S2K algorithm to use.

<br>
Values:<br>
  0 - Without salt.  Dangerous!<br>
  1 - With salt but with fixed iteration count.<br>
  3 - Variable iteration count.<br>
Default: 3<br>
Applies to: pgp_sym_encrypt<br>

<a id="id-1.11.7.37.9.18.12"></a>

#### F.28.3.8.8. s2k-count

The number of iterations of the S2K algorithm to use. It must be a value between 1024 and 65011712, inclusive.

<br>
Default: A random value between 65536 and 253952<br>
Applies to: pgp_sym_encrypt, only with s2k-mode=3<br>

<a id="id-1.11.7.37.9.18.13"></a>

#### F.28.3.8.9. s2k-digest-algo

Which digest algorithm to use in S2K calculation.

<br>
Values: md5, sha1<br>
Default: sha1<br>
Applies to: pgp_sym_encrypt<br>

<a id="id-1.11.7.37.9.18.14"></a>

#### F.28.3.8.10. s2k-cipher-algo

Which cipher to use for encrypting separate session key.

<br>
Values: bf, aes, aes128, aes192, aes256<br>
Default: use cipher-algo<br>
Applies to: pgp_sym_encrypt<br>

<a id="id-1.11.7.37.9.18.15"></a>

#### F.28.3.8.11. unicode-mode

Whether to convert textual data from database internal encoding to UTF-8 and back. If your database already is UTF-8, no conversion will be done, but the message will be tagged as UTF-8. Without this option it will not be.

<br>
Values: 0, 1<br>
Default: 0<br>
Applies to: pgp_sym_encrypt, pgp_pub_encrypt<br>

<a id="PGCRYPTO-PGP-ENC-FUNCS-OPTS-IGNORE-CIPHER-FAILURE"></a>

#### F.28.3.8.12. ignore-cipher-failure

Dangerous! Instructs pgcrypto to use an incorrect decryption algorithm matching the historical behavior prior to the fix for CVE-2026-14663, by completely ignoring failures from the OpenSSL cipher in use. This is intended only for users who need to recover incorrectly-encrypted messages created when the `cipher-algo` was unavailable under the OpenSSL configuration in use. Such faulty messages do not require the correct decryption key when `ignore-cipher-failure` is enabled, so there is no guarantee that the decrypted plaintext actually originated from a holder of the key.

Contrast the case of a message which was correctly encrypted, but the cipher that produced it is unavailable under the current OpenSSL configuration. Recovering such plaintext via `pgcrypto` requires making the actual cipher available to OpenSSL by, for example, enabling the appropriate provider. `ignore-cipher-failure` is not necessary or helpful for that scenario. If “decryption” of a correctly encrypted message with this option happens to pass PGP integrity checks, that result is coincidental and does not make the recovered plaintext trustworthy.

<br>
Values: 0, 1<br>
Default: 0<br>
Applies to: pgp_sym_decrypt, pgp_pub_decrypt<br>

<a id="id-1.11.7.37.9.19"></a>

### F.28.3.9. Generating PGP Keys with GnuPG

To generate a new key:

```

gpg --gen-key
```

The preferred key type is “DSA and Elgamal”.

For RSA encryption you must create either DSA or RSA sign-only key as master and then add an RSA encryption subkey with `gpg --edit-key`.

To list keys:

```

gpg --list-secret-keys
```

To export a public key in ASCII-armor format:

```

gpg -a --export KEYID > public.key
```

To export a secret key in ASCII-armor format:

```

gpg -a --export-secret-keys KEYID > secret.key
```

You need to use `dearmor()` on these keys before giving them to the PGP functions. Or if you can handle binary data, you can drop `-a` from the command.

For more details see `man gpg`, [The GNU Privacy Handbook](https://www.gnupg.org/gph/en/manual.html) and other documentation on <https://www.gnupg.org/>.

<a id="id-1.11.7.37.9.20"></a>

### F.28.3.10. Limitations of PGP Code

* No support for signing. That also means that it is not checked whether the encryption subkey belongs to the master key.
* No support for encryption key as master key. As such practice is generally discouraged, this should not be a problem.
* No support for several subkeys. This may seem like a problem, as this is common practice. On the other hand, you should not use your regular GPG/PGP keys with `pgcrypto`, but create new ones, as the usage scenario is rather different.

<a id="id-1.11.7.37.10"></a>

## F.28.4. Raw Encryption Functions

These functions only run a cipher over data; they don't have any advanced features of PGP encryption. Therefore they have some major problems:

1. They use user key directly as cipher key.
2. They don't provide any integrity checking, to see if the encrypted data was modified.
3. They expect that users manage all encryption parameters themselves, even IV.
4. They don't handle text.

So, with the introduction of PGP encryption, usage of raw encryption functions is discouraged.

<a id="id-1.11.7.37.10.5"></a><a id="id-1.11.7.37.10.6"></a><a id="id-1.11.7.37.10.7"></a><a id="id-1.11.7.37.10.8"></a>

```

encrypt(data bytea, key bytea, type text) returns bytea
decrypt(data bytea, key bytea, type text) returns bytea

encrypt_iv(data bytea, key bytea, iv bytea, type text) returns bytea
decrypt_iv(data bytea, key bytea, iv bytea, type text) returns bytea
```

Encrypt/decrypt data using the cipher method specified by <em class="parameter"><code>type</code></em>. The syntax of the <em class="parameter"><code>type</code></em> string is:

```

algorithm [ - mode ] [ /pad: padding ]
```

where <em class="replaceable"><code>algorithm</code></em> is one of:

* `bf` — Blowfish
* `aes` — AES (Rijndael-128, -192 or -256)

and <em class="replaceable"><code>mode</code></em> is one of:

* `cbc` — next block depends on previous (default)
* `ecb` — each block is encrypted separately (for testing only)

and <em class="replaceable"><code>padding</code></em> is one of:

* `pkcs` — data may be any length (default)
* `none` — data must be multiple of cipher block size

So, for example, these are equivalent:

```

encrypt(data, 'fooz', 'bf')
encrypt(data, 'fooz', 'bf-cbc/pad:pkcs')
```

In `encrypt_iv` and `decrypt_iv`, the <em class="parameter"><code>iv</code></em> parameter is the initial value for the CBC mode; it is ignored for ECB. It is clipped or padded with zeroes if not exactly block size. It defaults to all zeroes in the functions without this parameter.

<a id="id-1.11.7.37.11"></a>

## F.28.5. Random-Data Functions

<a id="id-1.11.7.37.11.2"></a>

```

gen_random_bytes(count integer) returns bytea
```

Returns <em class="parameter"><code>count</code></em> cryptographically strong random bytes. At most 1024 bytes can be extracted at a time. This is to avoid draining the randomness generator pool.

<a id="id-1.11.7.37.11.5"></a>

```

gen_random_uuid() returns uuid
```

Returns a version 4 (random) UUID. (Obsolete, this function internally calls the [core function](../../the-sql-language/functions-and-operators/uuid-functions.md) of the same name.)

<a id="id-1.11.7.37.12"></a>

## F.28.6. Notes

<a id="id-1.11.7.37.12.2"></a>

### F.28.6.1. Configuration

`pgcrypto` configures itself according to the findings of the main PostgreSQL `configure` script. The options that affect it are `--with-zlib` and `--with-ssl=openssl`.

When compiled with zlib, PGP encryption functions are able to compress data before encrypting.

`pgcrypto` requires OpenSSL. Otherwise, it will not be built or installed.

When compiled against OpenSSL 3.0.0 and later versions, the legacy provider must be activated in the `openssl.cnf` configuration file in order to use older ciphers like DES or Blowfish.

<a id="id-1.11.7.37.12.3"></a>

### F.28.6.2. NULL Handling

As is standard in SQL, all functions return NULL, if any of the arguments are NULL. This may create security risks on careless usage.

<a id="id-1.11.7.37.12.4"></a>

### F.28.6.3. Security Limitations

All `pgcrypto` functions run inside the database server. That means that all the data and passwords move between `pgcrypto` and client applications in clear text. Thus you must:

1. Connect locally or use SSL connections.
2. Trust both system and database administrator.

If you cannot, then better do crypto inside client application.

The implementation does not resist [side-channel attacks](https://en.wikipedia.org/wiki/Side-channel_attack). For example, the time required for a `pgcrypto` decryption function to complete varies among ciphertexts of a given size.

<a id="id-1.11.7.37.13"></a>

## F.28.7. Author

Marko Kreen <code class="email">&lt;<a class="email" href="mailto:markokr@gmail.com">markokr@gmail.com</a>&gt;</code>

`pgcrypto` uses code from the following sources:

<table border="1" class="informaltable">
<colgroup>
<col/>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th>Algorithm</th>
<th>Author</th>
<th>Source origin</th>
</tr>
</thead>
<tbody>
<tr>
<td>DES crypt</td>
<td>David Burren and others</td>
<td>FreeBSD libcrypt</td>
</tr>
<tr>
<td>MD5 crypt</td>
<td>Poul-Henning Kamp</td>
<td>FreeBSD libcrypt</td>
</tr>
<tr>
<td>Blowfish crypt</td>
<td>Solar Designer</td>
<td>www.openwall.com</td>
</tr>
</tbody>
</table>

---

原文：[PostgreSQL 15.19 Documentation](pgcrypto.md)（英文原文，待翻譯）
