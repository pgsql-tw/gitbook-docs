## 23.3. Character Set Support [#](#MULTIBYTE)

[23.3.1. Supported Character Sets](multibyte.md#MULTIBYTE-CHARSET-SUPPORTED)

[23.3.2. Setting the Character Set](multibyte.md#MULTIBYTE-SETTING)

[23.3.3. Automatic Character Set Conversion Between Server and Client](multibyte.md#MULTIBYTE-AUTOMATIC-CONVERSION)

[23.3.4. Available Character Set Conversions](multibyte.md#MULTIBYTE-CONVERSIONS-SUPPORTED)

[23.3.5. Further Reading](multibyte.md#MULTIBYTE-FURTHER-READING)

<a id="id-1.6.10.5.2"></a>

The character set support in PostgreSQL
allows you to store text in a variety of character sets (also called
encodings), including
single-byte character sets such as the ISO 8859 series and
multiple-byte character sets such as EUC (Extended Unix
Code), UTF-8, and Mule internal code. All supported character sets
can be used transparently by clients, but a few are not supported
for use within the server (that is, as a server-side encoding).
The default character set is selected while
initializing your PostgreSQL database
cluster using `initdb`. It can be overridden when you
create a database, so you can have multiple
databases each with a different character set.

An important restriction, however, is that each database's character set
must be compatible with the database's `LC_CTYPE` (character
classification) and `LC_COLLATE` (string sort order) locale
settings. For `C` or
`POSIX` locale, any character set is allowed, but for other
libc-provided locales there is only one character set that will work
correctly.
(On Windows, however, UTF-8 encoding can be used with any locale.)
If you have ICU support configured, ICU-provided locales can be used
with most but not all server-side encodings.

<a id="MULTIBYTE-CHARSET-SUPPORTED"></a>

### 23.3.1. Supported Character Sets [#](#MULTIBYTE-CHARSET-SUPPORTED)

[Table 23.3](multibyte.md#CHARSET-TABLE) shows the character sets available
for use in PostgreSQL.

<a id="CHARSET-TABLE"></a>

**Table 23.3. PostgreSQL Character Sets**

<table border="1" class="table" summary="PostgreSQL Character Sets"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/><col class="col4"/><col class="col5"/><col class="col6"/><col class="col7"/></colgroup><thead><tr><th>Name</th><th>Description</th><th>Language</th><th>Server?</th><th>ICU?</th><th>Bytes/​Char</th><th>Aliases</th></tr></thead><tbody><tr><td><code class="literal">BIG5</code></td><td>Big Five</td><td>Traditional Chinese</td><td>No</td><td>No</td><td>1–2</td><td><code class="literal">WIN950</code>, <code class="literal">Windows950</code></td></tr><tr><td><code class="literal">EUC_CN</code></td><td>Extended UNIX Code-CN</td><td>Simplified Chinese</td><td>Yes</td><td>Yes</td><td>1–3</td><td> </td></tr><tr><td><code class="literal">EUC_JP</code></td><td>Extended UNIX Code-JP</td><td>Japanese</td><td>Yes</td><td>Yes</td><td>1–3</td><td> </td></tr><tr><td><code class="literal">EUC_JIS_2004</code></td><td>Extended UNIX Code-JP, JIS X 0213</td><td>Japanese</td><td>Yes</td><td>No</td><td>1–3</td><td> </td></tr><tr><td><code class="literal">EUC_KR</code></td><td>Extended UNIX Code-KR</td><td>Korean</td><td>Yes</td><td>Yes</td><td>1–3</td><td> </td></tr><tr><td><code class="literal">EUC_TW</code></td><td>Extended UNIX Code-TW</td><td>Traditional Chinese, Taiwanese</td><td>Yes</td><td>Yes</td><td>1–4</td><td> </td></tr><tr><td><code class="literal">GB18030</code></td><td>National Standard</td><td>Chinese</td><td>No</td><td>No</td><td>1–4</td><td> </td></tr><tr><td><code class="literal">GBK</code></td><td>Extended National Standard</td><td>Simplified Chinese</td><td>No</td><td>No</td><td>1–2</td><td><code class="literal">WIN936</code>, <code class="literal">Windows936</code></td></tr><tr><td><code class="literal">ISO_8859_5</code></td><td>ISO 8859-5, <acronym class="acronym">ECMA</acronym> 113</td><td>Latin/Cyrillic</td><td>Yes</td><td>Yes</td><td>1</td><td> </td></tr><tr><td><code class="literal">ISO_8859_6</code></td><td>ISO 8859-6, <acronym class="acronym">ECMA</acronym> 114</td><td>Latin/Arabic</td><td>Yes</td><td>Yes</td><td>1</td><td> </td></tr><tr><td><code class="literal">ISO_8859_7</code></td><td>ISO 8859-7, <acronym class="acronym">ECMA</acronym> 118</td><td>Latin/Greek</td><td>Yes</td><td>Yes</td><td>1</td><td> </td></tr><tr><td><code class="literal">ISO_8859_8</code></td><td>ISO 8859-8, <acronym class="acronym">ECMA</acronym> 121</td><td>Latin/Hebrew</td><td>Yes</td><td>Yes</td><td>1</td><td> </td></tr><tr><td><code class="literal">JOHAB</code></td><td><acronym class="acronym">JOHAB</acronym></td><td>Korean (Hangul)</td><td>No</td><td>No</td><td>1–3</td><td> </td></tr><tr><td><code class="literal">KOI8R</code></td><td><acronym class="acronym">KOI</acronym>8-R</td><td>Cyrillic (Russian)</td><td>Yes</td><td>Yes</td><td>1</td><td><code class="literal">KOI8</code></td></tr><tr><td><code class="literal">KOI8U</code></td><td><acronym class="acronym">KOI</acronym>8-U</td><td>Cyrillic (Ukrainian)</td><td>Yes</td><td>Yes</td><td>1</td><td> </td></tr><tr><td><code class="literal">LATIN1</code></td><td>ISO 8859-1, <acronym class="acronym">ECMA</acronym> 94</td><td>Western European</td><td>Yes</td><td>Yes</td><td>1</td><td><code class="literal">ISO88591</code></td></tr><tr><td><code class="literal">LATIN2</code></td><td>ISO 8859-2, <acronym class="acronym">ECMA</acronym> 94</td><td>Central European</td><td>Yes</td><td>Yes</td><td>1</td><td><code class="literal">ISO88592</code></td></tr><tr><td><code class="literal">LATIN3</code></td><td>ISO 8859-3, <acronym class="acronym">ECMA</acronym> 94</td><td>South European</td><td>Yes</td><td>Yes</td><td>1</td><td><code class="literal">ISO88593</code></td></tr><tr><td><code class="literal">LATIN4</code></td><td>ISO 8859-4, <acronym class="acronym">ECMA</acronym> 94</td><td>North European</td><td>Yes</td><td>Yes</td><td>1</td><td><code class="literal">ISO88594</code></td></tr><tr><td><code class="literal">LATIN5</code></td><td>ISO 8859-9, <acronym class="acronym">ECMA</acronym> 128</td><td>Turkish</td><td>Yes</td><td>Yes</td><td>1</td><td><code class="literal">ISO88599</code></td></tr><tr><td><code class="literal">LATIN6</code></td><td>ISO 8859-10, <acronym class="acronym">ECMA</acronym> 144</td><td>Nordic</td><td>Yes</td><td>Yes</td><td>1</td><td><code class="literal">ISO885910</code></td></tr><tr><td><code class="literal">LATIN7</code></td><td>ISO 8859-13</td><td>Baltic</td><td>Yes</td><td>Yes</td><td>1</td><td><code class="literal">ISO885913</code></td></tr><tr><td><code class="literal">LATIN8</code></td><td>ISO 8859-14</td><td>Celtic</td><td>Yes</td><td>Yes</td><td>1</td><td><code class="literal">ISO885914</code></td></tr><tr><td><code class="literal">LATIN9</code></td><td>ISO 8859-15</td><td>LATIN1 with Euro and accents</td><td>Yes</td><td>Yes</td><td>1</td><td><code class="literal">ISO885915</code></td></tr><tr><td><code class="literal">LATIN10</code></td><td>ISO 8859-16, <acronym class="acronym">ASRO</acronym> SR 14111</td><td>Romanian</td><td>Yes</td><td>No</td><td>1</td><td><code class="literal">ISO885916</code></td></tr><tr><td><code class="literal">MULE_INTERNAL</code></td><td>Mule internal code</td><td>Multilingual Emacs</td><td>Yes</td><td>No</td><td>1–4</td><td> </td></tr><tr><td><code class="literal">SJIS</code></td><td>Shift JIS</td><td>Japanese</td><td>No</td><td>No</td><td>1–2</td><td><code class="literal">Mskanji</code>, <code class="literal">ShiftJIS</code>, <code class="literal">WIN932</code>, <code class="literal">Windows932</code></td></tr><tr><td><code class="literal">SHIFT_JIS_2004</code></td><td>Shift JIS, JIS X 0213</td><td>Japanese</td><td>No</td><td>No</td><td>1–2</td><td> </td></tr><tr><td><code class="literal">SQL_ASCII</code></td><td>unspecified (see text)</td><td><span class="emphasis"><em>any</em></span></td><td>Yes</td><td>No</td><td>1</td><td> </td></tr><tr><td><code class="literal">UHC</code></td><td>Unified Hangul Code</td><td>Korean</td><td>No</td><td>No</td><td>1–2</td><td><code class="literal">WIN949</code>, <code class="literal">Windows949</code></td></tr><tr><td><code class="literal">UTF8</code></td><td>Unicode, 8-bit</td><td><span class="emphasis"><em>all</em></span></td><td>Yes</td><td>Yes</td><td>1–4</td><td><code class="literal">Unicode</code></td></tr><tr><td><code class="literal">WIN866</code></td><td>Windows CP866</td><td>Cyrillic</td><td>Yes</td><td>Yes</td><td>1</td><td><code class="literal">ALT</code></td></tr><tr><td><code class="literal">WIN874</code></td><td>Windows CP874</td><td>Thai</td><td>Yes</td><td>No</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1250</code></td><td>Windows CP1250</td><td>Central European</td><td>Yes</td><td>Yes</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1251</code></td><td>Windows CP1251</td><td>Cyrillic</td><td>Yes</td><td>Yes</td><td>1</td><td><code class="literal">WIN</code></td></tr><tr><td><code class="literal">WIN1252</code></td><td>Windows CP1252</td><td>Western European</td><td>Yes</td><td>Yes</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1253</code></td><td>Windows CP1253</td><td>Greek</td><td>Yes</td><td>Yes</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1254</code></td><td>Windows CP1254</td><td>Turkish</td><td>Yes</td><td>Yes</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1255</code></td><td>Windows CP1255</td><td>Hebrew</td><td>Yes</td><td>Yes</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1256</code></td><td>Windows CP1256</td><td>Arabic</td><td>Yes</td><td>Yes</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1257</code></td><td>Windows CP1257</td><td>Baltic</td><td>Yes</td><td>Yes</td><td>1</td><td> </td></tr><tr><td><code class="literal">WIN1258</code></td><td>Windows CP1258</td><td>Vietnamese</td><td>Yes</td><td>Yes</td><td>1</td><td><code class="literal">ABC</code>, <code class="literal">TCVN</code>, <code class="literal">TCVN5712</code>, <code class="literal">VSCII</code></td></tr></tbody></table>

<br>

Not all client APIs support all the listed character sets. For example, the
PostgreSQL
JDBC driver does not support `MULE_INTERNAL`, `LATIN6`,
`LATIN8`, and `LATIN10`.

The `SQL_ASCII` setting behaves considerably differently
from the other settings. When the server character set is
`SQL_ASCII`, the server interprets byte values 0–127
according to the ASCII standard, while byte values 128–255 are taken
as uninterpreted characters. No encoding conversion will be done when
the setting is `SQL_ASCII`. Thus, this setting is not so
much a declaration that a specific encoding is in use, as a declaration
of ignorance about the encoding. In most cases, if you are
working with any non-ASCII data, it is unwise to use the
`SQL_ASCII` setting because
PostgreSQL will be unable to help you by
converting or validating non-ASCII characters.

<a id="MULTIBYTE-SETTING"></a>

### 23.3.2. Setting the Character Set [#](#MULTIBYTE-SETTING)

`initdb` defines the default character set (encoding)
for a PostgreSQL cluster. For example,

```

initdb -E EUC_JP
```

sets the default character set to
`EUC_JP` (Extended Unix Code for Japanese). You
can use `--encoding` instead of
`-E` if you prefer longer option strings.
If no `-E` or `--encoding` option is
given, `initdb` attempts to determine the appropriate
encoding to use based on the specified or default locale.

You can specify a non-default encoding at database creation time,
provided that the encoding is compatible with the selected locale:

```

createdb -E EUC_KR -T template0 --lc-collate=ko_KR.euckr --lc-ctype=ko_KR.euckr korean
```

This will create a database named `korean` that
uses the character set `EUC_KR`, and locale `ko_KR`.
Another way to accomplish this is to use this SQL command:

```

CREATE DATABASE korean WITH ENCODING 'EUC_KR' LC_COLLATE='ko_KR.euckr' LC_CTYPE='ko_KR.euckr' TEMPLATE=template0;
```

Notice that the above commands specify copying the `template0`
database. When copying any other database, the encoding and locale
settings cannot be changed from those of the source database, because
that might result in corrupt data. For more information see
[Section 22.3](../managing-databases/manage-ag-templatedbs.md).

The encoding for a database is stored in the system catalog
`pg_database`. You can see it by using the
`psql` `-l` option or the
`\l` command.

```

$ psql -l
                                         List of databases
   Name    |  Owner   | Encoding  |  Collation  |    Ctype    |          Access Privileges
-----------+----------+-----------+-------------+-------------+-------------------------------------
 clocaledb | hlinnaka | SQL_ASCII | C           | C           |
 englishdb | hlinnaka | UTF8      | en_GB.UTF8  | en_GB.UTF8  |
 japanese  | hlinnaka | UTF8      | ja_JP.UTF8  | ja_JP.UTF8  |
 korean    | hlinnaka | EUC_KR    | ko_KR.euckr | ko_KR.euckr |
 postgres  | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  |
 template0 | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  | {=c/hlinnaka,hlinnaka=CTc/hlinnaka}
 template1 | hlinnaka | UTF8      | fi_FI.UTF8  | fi_FI.UTF8  | {=c/hlinnaka,hlinnaka=CTc/hlinnaka}
(7 rows)
```

### Important

On most modern operating systems, PostgreSQL
can determine which character set is implied by the `LC_CTYPE`
setting, and it will enforce that only the matching database encoding is
used. On older systems it is your responsibility to ensure that you use
the encoding expected by the locale you have selected. A mistake in
this area is likely to lead to strange behavior of locale-dependent
operations such as sorting.

PostgreSQL will allow superusers to create
databases with `SQL_ASCII` encoding even when
`LC_CTYPE` is not `C` or `POSIX`. As noted
above, `SQL_ASCII` does not enforce that the data stored in
the database has any particular encoding, and so this choice poses risks
of locale-dependent misbehavior. Using this combination of settings is
deprecated and may someday be forbidden altogether.

<a id="MULTIBYTE-AUTOMATIC-CONVERSION"></a>

### 23.3.3. Automatic Character Set Conversion Between Server and Client [#](#MULTIBYTE-AUTOMATIC-CONVERSION)

PostgreSQL supports automatic character
set conversion between server and client for many combinations of
character sets ([Section 23.3.4](multibyte.md#MULTIBYTE-CONVERSIONS-SUPPORTED)
shows which ones).

To enable automatic character set conversion, you have to
tell PostgreSQL the character set
(encoding) you would like to use in the client. There are several
ways to accomplish this:

* Using the `\encoding` command in
  psql.
  `\encoding` allows you to change client
  encoding on the fly. For
  example, to change the encoding to `SJIS`, type:

  ```

  \encoding SJIS
  ```
* libpq ([Section 32.11](../../client-interfaces/libpq/libpq-control.md)) has functions to control the client encoding.
* Using `SET client_encoding TO`.
  Setting the client encoding can be done with this SQL command:

  ```

  SET CLIENT_ENCODING TO 'value';
  ```

  Also you can use the standard SQL syntax `SET NAMES`
  for this purpose:

  ```

  SET NAMES 'value';
  ```

  To query the current client encoding:

  ```

  SHOW client_encoding;
  ```

  To return to the default encoding:

  ```

  RESET client_encoding;
  ```
* Using `PGCLIENTENCODING`. If the environment variable
  `PGCLIENTENCODING` is defined in the client's
  environment, that client encoding is automatically selected
  when a connection to the server is made. (This can
  subsequently be overridden using any of the other methods
  mentioned above.)
* Using the configuration variable [client_encoding](../runtime-config/runtime-config-client.md#GUC-CLIENT-ENCODING). If the
  `client_encoding` variable is set, that client
  encoding is automatically selected when a connection to the
  server is made. (This can subsequently be overridden using any
  of the other methods mentioned above.)

If the conversion of a particular character is not possible
— suppose you chose `EUC_JP` for the
server and `LATIN1` for the client, and some
Japanese characters are returned that do not have a representation in
`LATIN1` — an error is reported.

If the client character set is defined as `SQL_ASCII`,
encoding conversion is disabled, regardless of the server's character
set. (However, if the server's character set is
not `SQL_ASCII`, the server will still check that
incoming data is valid for that encoding; so the net effect is as
though the client character set were the same as the server's.)
Just as for the server, use of `SQL_ASCII` is unwise
unless you are working with all-ASCII data.

<a id="MULTIBYTE-CONVERSIONS-SUPPORTED"></a>

### 23.3.4. Available Character Set Conversions [#](#MULTIBYTE-CONVERSIONS-SUPPORTED)

PostgreSQL allows conversion between any
two character sets for which a conversion function is listed in the
[`pg_conversion`](../../internals/catalogs/catalog-pg-conversion.md)
system catalog. PostgreSQL comes with
some predefined conversions, as summarized in
[Table 23.4](multibyte.md#MULTIBYTE-TRANSLATION-TABLE) and shown in more
detail in [Table 23.5](multibyte.md#BUILTIN-CONVERSIONS-TABLE). You can
create a new conversion using the SQL command
[CREATE CONVERSION](../../reference/sql-commands/sql-createconversion.md). (To be used for automatic
client/server conversions, a conversion must be marked
as “default” for its character set pair.)

<a id="MULTIBYTE-TRANSLATION-TABLE"></a>

**Table 23.4. Built-in Client/Server Character Set Conversions**

<table border="1" class="table" summary="Built-in Client/Server Character Set Conversions"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>Server Character Set</th><th>Available Client Character Sets</th></tr></thead><tbody><tr><td><code class="literal">BIG5</code></td><td><span class="emphasis"><em>not supported as a server encoding</em></span>
</td></tr><tr><td><code class="literal">EUC_CN</code></td><td><span class="emphasis"><em>EUC_CN</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">EUC_JP</code></td><td><span class="emphasis"><em>EUC_JP</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">SJIS</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">EUC_JIS_2004</code></td><td><span class="emphasis"><em>EUC_JIS_2004</em></span>,
        <code class="literal">SHIFT_JIS_2004</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">EUC_KR</code></td><td><span class="emphasis"><em>EUC_KR</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">EUC_TW</code></td><td><span class="emphasis"><em>EUC_TW</em></span>,
        <code class="literal">BIG5</code>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">GB18030</code></td><td><span class="emphasis"><em>not supported as a server encoding</em></span>
</td></tr><tr><td><code class="literal">GBK</code></td><td><span class="emphasis"><em>not supported as a server encoding</em></span>
</td></tr><tr><td><code class="literal">ISO_8859_5</code></td><td><span class="emphasis"><em>ISO_8859_5</em></span>,
        <code class="literal">KOI8R</code>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>,
        <code class="literal">WIN866</code>,
        <code class="literal">WIN1251</code>
</td></tr><tr><td><code class="literal">ISO_8859_6</code></td><td><span class="emphasis"><em>ISO_8859_6</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">ISO_8859_7</code></td><td><span class="emphasis"><em>ISO_8859_7</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">ISO_8859_8</code></td><td><span class="emphasis"><em>ISO_8859_8</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">JOHAB</code></td><td><span class="emphasis"><em>not supported as a server encoding</em></span>
</td></tr><tr><td><code class="literal">KOI8R</code></td><td><span class="emphasis"><em>KOI8R</em></span>,
        <code class="literal">ISO_8859_5</code>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>,
        <code class="literal">WIN866</code>,
        <code class="literal">WIN1251</code>
</td></tr><tr><td><code class="literal">KOI8U</code></td><td><span class="emphasis"><em>KOI8U</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN1</code></td><td><span class="emphasis"><em>LATIN1</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN2</code></td><td><span class="emphasis"><em>LATIN2</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>,
        <code class="literal">WIN1250</code>
</td></tr><tr><td><code class="literal">LATIN3</code></td><td><span class="emphasis"><em>LATIN3</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN4</code></td><td><span class="emphasis"><em>LATIN4</em></span>,
        <code class="literal">MULE_INTERNAL</code>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN5</code></td><td><span class="emphasis"><em>LATIN5</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN6</code></td><td><span class="emphasis"><em>LATIN6</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN7</code></td><td><span class="emphasis"><em>LATIN7</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN8</code></td><td><span class="emphasis"><em>LATIN8</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN9</code></td><td><span class="emphasis"><em>LATIN9</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">LATIN10</code></td><td><span class="emphasis"><em>LATIN10</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">MULE_INTERNAL</code></td><td><span class="emphasis"><em>MULE_INTERNAL</em></span>,
         <code class="literal">BIG5</code>,
         <code class="literal">EUC_CN</code>,
         <code class="literal">EUC_JP</code>,
         <code class="literal">EUC_KR</code>,
         <code class="literal">EUC_TW</code>,
         <code class="literal">ISO_8859_5</code>,
         <code class="literal">KOI8R</code>,
         <code class="literal">LATIN1</code> to <code class="literal">LATIN4</code>,
         <code class="literal">SJIS</code>,
         <code class="literal">WIN866</code>,
         <code class="literal">WIN1250</code>,
         <code class="literal">WIN1251</code>
</td></tr><tr><td><code class="literal">SJIS</code></td><td><span class="emphasis"><em>not supported as a server encoding</em></span>
</td></tr><tr><td><code class="literal">SHIFT_JIS_2004</code></td><td><span class="emphasis"><em>not supported as a server encoding</em></span>
</td></tr><tr><td><code class="literal">SQL_ASCII</code></td><td><span class="emphasis"><em>any (no conversion will be performed)</em></span>
</td></tr><tr><td><code class="literal">UHC</code></td><td><span class="emphasis"><em>not supported as a server encoding</em></span>
</td></tr><tr><td><code class="literal">UTF8</code></td><td><span class="emphasis"><em>all supported encodings</em></span>
</td></tr><tr><td><code class="literal">WIN866</code></td><td><span class="emphasis"><em>WIN866</em></span>,
         <code class="literal">ISO_8859_5</code>,
         <code class="literal">KOI8R</code>,
         <code class="literal">MULE_INTERNAL</code>,
         <code class="literal">UTF8</code>,
         <code class="literal">WIN1251</code>
</td></tr><tr><td><code class="literal">WIN874</code></td><td><span class="emphasis"><em>WIN874</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1250</code></td><td><span class="emphasis"><em>WIN1250</em></span>,
         <code class="literal">LATIN2</code>,
         <code class="literal">MULE_INTERNAL</code>,
         <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1251</code></td><td><span class="emphasis"><em>WIN1251</em></span>,
         <code class="literal">ISO_8859_5</code>,
         <code class="literal">KOI8R</code>,
         <code class="literal">MULE_INTERNAL</code>,
         <code class="literal">UTF8</code>,
         <code class="literal">WIN866</code>
</td></tr><tr><td><code class="literal">WIN1252</code></td><td><span class="emphasis"><em>WIN1252</em></span>,
         <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1253</code></td><td><span class="emphasis"><em>WIN1253</em></span>,
         <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1254</code></td><td><span class="emphasis"><em>WIN1254</em></span>,
         <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1255</code></td><td><span class="emphasis"><em>WIN1255</em></span>,
         <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1256</code></td><td><span class="emphasis"><em>WIN1256</em></span>,
        <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1257</code></td><td><span class="emphasis"><em>WIN1257</em></span>,
         <code class="literal">UTF8</code>
</td></tr><tr><td><code class="literal">WIN1258</code></td><td><span class="emphasis"><em>WIN1258</em></span>,
        <code class="literal">UTF8</code>
</td></tr></tbody></table>

<br><a id="BUILTIN-CONVERSIONS-TABLE"></a>

**Table 23.5. All Built-in Character Set Conversions**

<table border="1" class="table" summary="All Built-in Character Set Conversions"><colgroup><col class="col1"/><col class="col2"/><col class="col3"/></colgroup><thead><tr><th>Conversion Name
         <a class="footnote" href="#ftn.id-1.6.10.5.8.4.2.4.1.1.1"><sup class="footnote" id="id-1.6.10.5.8.4.2.4.1.1.1">[a]</sup></a>
</th><th>Source Encoding</th><th>Destination Encoding</th></tr></thead><tbody><tr><td><code class="literal">big5_to_euc_tw</code></td><td><code class="literal">BIG5</code></td><td><code class="literal">EUC_TW</code></td></tr><tr><td><code class="literal">big5_to_mic</code></td><td><code class="literal">BIG5</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">big5_to_utf8</code></td><td><code class="literal">BIG5</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_cn_to_mic</code></td><td><code class="literal">EUC_CN</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">euc_cn_to_utf8</code></td><td><code class="literal">EUC_CN</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_jp_to_mic</code></td><td><code class="literal">EUC_JP</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">euc_jp_to_sjis</code></td><td><code class="literal">EUC_JP</code></td><td><code class="literal">SJIS</code></td></tr><tr><td><code class="literal">euc_jp_to_utf8</code></td><td><code class="literal">EUC_JP</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_kr_to_mic</code></td><td><code class="literal">EUC_KR</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">euc_kr_to_utf8</code></td><td><code class="literal">EUC_KR</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_tw_to_big5</code></td><td><code class="literal">EUC_TW</code></td><td><code class="literal">BIG5</code></td></tr><tr><td><code class="literal">euc_tw_to_mic</code></td><td><code class="literal">EUC_TW</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">euc_tw_to_utf8</code></td><td><code class="literal">EUC_TW</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">gb18030_to_utf8</code></td><td><code class="literal">GB18030</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">gbk_to_utf8</code></td><td><code class="literal">GBK</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_10_to_utf8</code></td><td><code class="literal">LATIN6</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_13_to_utf8</code></td><td><code class="literal">LATIN7</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_14_to_utf8</code></td><td><code class="literal">LATIN8</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_15_to_utf8</code></td><td><code class="literal">LATIN9</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_16_to_utf8</code></td><td><code class="literal">LATIN10</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_1_to_mic</code></td><td><code class="literal">LATIN1</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_1_to_utf8</code></td><td><code class="literal">LATIN1</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_2_to_mic</code></td><td><code class="literal">LATIN2</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_2_to_utf8</code></td><td><code class="literal">LATIN2</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_2_to_windows_1250</code></td><td><code class="literal">LATIN2</code></td><td><code class="literal">WIN1250</code></td></tr><tr><td><code class="literal">iso_8859_3_to_mic</code></td><td><code class="literal">LATIN3</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_3_to_utf8</code></td><td><code class="literal">LATIN3</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_4_to_mic</code></td><td><code class="literal">LATIN4</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_4_to_utf8</code></td><td><code class="literal">LATIN4</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_5_to_koi8_r</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">iso_8859_5_to_mic</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">iso_8859_5_to_utf8</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_5_to_windows_1251</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">WIN1251</code></td></tr><tr><td><code class="literal">iso_8859_5_to_windows_866</code></td><td><code class="literal">ISO_8859_5</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">iso_8859_6_to_utf8</code></td><td><code class="literal">ISO_8859_6</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_7_to_utf8</code></td><td><code class="literal">ISO_8859_7</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_8_to_utf8</code></td><td><code class="literal">ISO_8859_8</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">iso_8859_9_to_utf8</code></td><td><code class="literal">LATIN5</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">johab_to_utf8</code></td><td><code class="literal">JOHAB</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">koi8_r_to_iso_8859_5</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">koi8_r_to_mic</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">koi8_r_to_utf8</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">koi8_r_to_windows_1251</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">WIN1251</code></td></tr><tr><td><code class="literal">koi8_r_to_windows_866</code></td><td><code class="literal">KOI8R</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">koi8_u_to_utf8</code></td><td><code class="literal">KOI8U</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">mic_to_big5</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">BIG5</code></td></tr><tr><td><code class="literal">mic_to_euc_cn</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">EUC_CN</code></td></tr><tr><td><code class="literal">mic_to_euc_jp</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">EUC_JP</code></td></tr><tr><td><code class="literal">mic_to_euc_kr</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">EUC_KR</code></td></tr><tr><td><code class="literal">mic_to_euc_tw</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">EUC_TW</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_1</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">LATIN1</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_2</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">LATIN2</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_3</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">LATIN3</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_4</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">LATIN4</code></td></tr><tr><td><code class="literal">mic_to_iso_8859_5</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">mic_to_koi8_r</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">mic_to_sjis</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">SJIS</code></td></tr><tr><td><code class="literal">mic_to_windows_1250</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">WIN1250</code></td></tr><tr><td><code class="literal">mic_to_windows_1251</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">WIN1251</code></td></tr><tr><td><code class="literal">mic_to_windows_866</code></td><td><code class="literal">MULE_INTERNAL</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">sjis_to_euc_jp</code></td><td><code class="literal">SJIS</code></td><td><code class="literal">EUC_JP</code></td></tr><tr><td><code class="literal">sjis_to_mic</code></td><td><code class="literal">SJIS</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">sjis_to_utf8</code></td><td><code class="literal">SJIS</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_1258_to_utf8</code></td><td><code class="literal">WIN1258</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">uhc_to_utf8</code></td><td><code class="literal">UHC</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">utf8_to_big5</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">BIG5</code></td></tr><tr><td><code class="literal">utf8_to_euc_cn</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_CN</code></td></tr><tr><td><code class="literal">utf8_to_euc_jp</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_JP</code></td></tr><tr><td><code class="literal">utf8_to_euc_kr</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_KR</code></td></tr><tr><td><code class="literal">utf8_to_euc_tw</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_TW</code></td></tr><tr><td><code class="literal">utf8_to_gb18030</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">GB18030</code></td></tr><tr><td><code class="literal">utf8_to_gbk</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">GBK</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_1</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN1</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_10</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN6</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_13</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN7</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_14</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN8</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_15</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN9</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_16</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN10</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_2</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN2</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_3</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN3</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_4</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN4</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_5</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_6</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">ISO_8859_6</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_7</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">ISO_8859_7</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_8</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">ISO_8859_8</code></td></tr><tr><td><code class="literal">utf8_to_iso_8859_9</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">LATIN5</code></td></tr><tr><td><code class="literal">utf8_to_johab</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">JOHAB</code></td></tr><tr><td><code class="literal">utf8_to_koi8_r</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">utf8_to_koi8_u</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">KOI8U</code></td></tr><tr><td><code class="literal">utf8_to_sjis</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">SJIS</code></td></tr><tr><td><code class="literal">utf8_to_windows_1258</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1258</code></td></tr><tr><td><code class="literal">utf8_to_uhc</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">UHC</code></td></tr><tr><td><code class="literal">utf8_to_windows_1250</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1250</code></td></tr><tr><td><code class="literal">utf8_to_windows_1251</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1251</code></td></tr><tr><td><code class="literal">utf8_to_windows_1252</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1252</code></td></tr><tr><td><code class="literal">utf8_to_windows_1253</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1253</code></td></tr><tr><td><code class="literal">utf8_to_windows_1254</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1254</code></td></tr><tr><td><code class="literal">utf8_to_windows_1255</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1255</code></td></tr><tr><td><code class="literal">utf8_to_windows_1256</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1256</code></td></tr><tr><td><code class="literal">utf8_to_windows_1257</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN1257</code></td></tr><tr><td><code class="literal">utf8_to_windows_866</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">utf8_to_windows_874</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">WIN874</code></td></tr><tr><td><code class="literal">windows_1250_to_iso_8859_2</code></td><td><code class="literal">WIN1250</code></td><td><code class="literal">LATIN2</code></td></tr><tr><td><code class="literal">windows_1250_to_mic</code></td><td><code class="literal">WIN1250</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">windows_1250_to_utf8</code></td><td><code class="literal">WIN1250</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_1251_to_iso_8859_5</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">windows_1251_to_koi8_r</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">windows_1251_to_mic</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">windows_1251_to_utf8</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_1251_to_windows_866</code></td><td><code class="literal">WIN1251</code></td><td><code class="literal">WIN866</code></td></tr><tr><td><code class="literal">windows_1252_to_utf8</code></td><td><code class="literal">WIN1252</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_1256_to_utf8</code></td><td><code class="literal">WIN1256</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_866_to_iso_8859_5</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">ISO_8859_5</code></td></tr><tr><td><code class="literal">windows_866_to_koi8_r</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">KOI8R</code></td></tr><tr><td><code class="literal">windows_866_to_mic</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">MULE_INTERNAL</code></td></tr><tr><td><code class="literal">windows_866_to_utf8</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">windows_866_to_windows_1251</code></td><td><code class="literal">WIN866</code></td><td><code class="literal">WIN</code></td></tr><tr><td><code class="literal">windows_874_to_utf8</code></td><td><code class="literal">WIN874</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">euc_jis_2004_to_utf8</code></td><td><code class="literal">EUC_JIS_2004</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">utf8_to_euc_jis_2004</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">EUC_JIS_2004</code></td></tr><tr><td><code class="literal">shift_jis_2004_to_utf8</code></td><td><code class="literal">SHIFT_JIS_2004</code></td><td><code class="literal">UTF8</code></td></tr><tr><td><code class="literal">utf8_to_shift_jis_2004</code></td><td><code class="literal">UTF8</code></td><td><code class="literal">SHIFT_JIS_2004</code></td></tr><tr><td><code class="literal">euc_jis_2004_to_shift_jis_2004</code></td><td><code class="literal">EUC_JIS_2004</code></td><td><code class="literal">SHIFT_JIS_2004</code></td></tr><tr><td><code class="literal">shift_jis_2004_to_euc_jis_2004</code></td><td><code class="literal">SHIFT_JIS_2004</code></td><td><code class="literal">EUC_JIS_2004</code></td></tr></tbody><tbody class="footnotes"><tr><td colspan="3"><div class="footnote" id="ftn.id-1.6.10.5.8.4.2.4.1.1.1"><p><a class="para" href="#id-1.6.10.5.8.4.2.4.1.1.1"><sup class="para">[a] </sup></a>
           The conversion names follow a standard naming scheme: The
           official name of the source encoding with all
           non-alphanumeric characters replaced by underscores, followed
           by <code class="literal">_to_</code>, followed by the similarly processed
           destination encoding name.  Therefore, these names sometimes
           deviate from the customary encoding names shown in
           <a class="xref" href="multibyte.md#CHARSET-TABLE">Table 23.3</a>.
          </p></div></td></tr></tbody></table>

<br>

<a id="MULTIBYTE-FURTHER-READING"></a>

### 23.3.5. Further Reading [#](#MULTIBYTE-FURTHER-READING)

These are good sources to start learning about various kinds of encoding
systems.

*CJKV Information Processing: Chinese, Japanese, Korean & Vietnamese Computing*
:   Contains detailed explanations of `EUC_JP`,
    `EUC_CN`, `EUC_KR`,
    `EUC_TW`.

<https://www.unicode.org/>
:   The web site of the Unicode Consortium.

[RFC 3629](https://datatracker.ietf.org/doc/html/rfc3629)
:   UTF-8 (8-bit UCS/Unicode Transformation
    Format) is defined here.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/multibyte.html)（英文原文，待翻譯）
