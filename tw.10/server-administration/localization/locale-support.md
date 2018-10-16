# 23.1. 語系支援

區域設定支援是指某個應用程序，它提供有關字母、排序、數字格式等文化偏好。PostgreSQL 使用伺服器作業系統提供的標準 ISO C 和 POSIX 區域設定。有關其他訊息，請參閱作業系統文件。

## 23.1.1. 綜觀

使用 initdb 建立資料庫叢集時，將自動初始化語言環境支援。initdb 將預設使用其執行環境的語言環境設定初始化資料庫叢集。因此，如果您的作業系統已設定為使用資料庫叢集中所需的語言環境，那麼您毌須進行任何額外操作。如果要使用其他語言環境（或者您不確定系統設定的語言環境），可以透過指定 --locale 選項指示 initdb 確切使用哪個語言環境。例如：

```text
initdb --locale=sv_SE
```

Unix 系統的這個範例將語言環境設定為瑞典語（SE）中的瑞典語（sv）。其他可能性可能包括 en\_US（美國英語）和 fr\_CA（加拿大法語）。如果可以將多個字元集用於語言環境，則規範可採用 language\_territory.codeset 形式。例如，fr\_BE.UTF-8 表示比利時（BE）中使用的法語（fr），具有 UTF-8 字元集編碼。

系統上可用的區域設定取決於作業系統供應商提供和安裝的內容。在大多數 Unix 系統上，指令 `locale -a` 將提供可用語言環境的列表。Windows 使用更詳細的區域設定名稱，例如 German\_Germany 或 Swedish\_Sweden.1252，但原則是相同的。

有時，混合來自多個語言環境的規則很有用，例如，使用英語校對規則，但使用西班牙語訊息。為了支援這一點，可以存在一組區域設定子類別，它們僅控制本地化規則的某些方面：

| `LC_COLLATE` | String sort order |
| :--- | :--- |
| `LC_CTYPE` | 字元分類（什麼是字母？它的大寫字母是？） |
| `LC_MESSAGES` | 訊息的語言 |
| `LC_MONETARY` | 格式化貨幣金額 |
| `LC_NUMERIC` | 格式化數字 |
| `LC_TIME` | 格式化日期和時間 |

類別名稱轉換為 initdb 選項的名稱，以覆蓋特定類別的區域設定選項。例如，要將語言環境設定為加拿大法語，但使用美國規則格式化貨幣，請使用 `initdb --locale = fr_CA --lc-monetary = en_US`。

如果您希望系統的行為就像它沒有語言環境支援一樣，請使用特殊的語言環境名稱 C 或等效的 POSIX。

建立資料庫時，某些區域設定類別必須固定其值。 您可以對不同的資料庫使用不同的設定，但是一旦建立了資料庫，就無法再為該資料庫更改它們。LC\_COLLATE 和 LC\_CTYPE 是這些類別。它們會影響索引的排序順序，因此必須保持不變，否則文字欄位上的索引會損壞。（但是您可以使用排序規則來緩解此限制，如[第 23.2 節](collation-support.md)中所述。）這些類別的預設值在執行 initdb 時確定，並且在建立新資料庫時使用這些值，除非在 CREATE DATABASE 指令中另行指定。

透過設定與語言環境類別同名的伺服器配置參數，可以隨時更改其他語言環境類別（有關詳細訊息，請參閱[第 19.11.2 節](../server-configuration/19.11.-yong-hu-duan-lian-xian-yu-she-can-shu.md#19-11-2-xi-ge-shi)）。initdb 選擇的值實際上只寫入配置文件 postgresql.conf，以在伺服器啟動時用作預設值。如果從 postgresql.conf 中刪除這些設定，則伺服器將從其執行環境繼承設定。

請注意，服務器的區域設定行為由伺服器看到的環境變數決定，而不是由任何用戶端的環境確定。因此，在啟動伺服器之前，請務必配置正確的區域設定。這樣做的結果是，如果用戶端和伺服器設定在不同的區域設定中，則訊息可能會以不同的語言顯示，具體取決於它們的來源。

**注意**  
當我們談到從執行環境繼承語言環境時，這意味著在大多數作業系統上都有以下內容：對於給定的語言環境類別，比如排序規則，將按此順序查詢以下環境變數，直到找到一個設定：LC\_ALL， LC\_COLLATE（或對應於相應類別的變數），LANG。如果未設定這些環境變數，則語言環境預設為 C.

某些訊息的本地化函式庫還會查看環境變數 LANGUAGE，該變數將覆寫所有其他區域設定，以便設定訊息的語言。如有疑問，請參閱作業系統的文件，特別是有關 gettext 的文件。

要使訊息能夠轉換為用戶的偏好語言，必須在編譯時選擇 NLS（`configure --enable-nls`）。所有其他語言環境支援都是自動編譯的。

## 23.1.2. Behavior

The locale settings influence the following SQL features:

* Sort order in queries using `ORDER BY` or the standard comparison operators on textual data
* The `upper`, `lower`, and `initcap` functions
* Pattern matching operators \(`LIKE`, `SIMILAR TO`, and POSIX-style regular expressions\); locales affect both case insensitive matching and the classification of characters by character-class regular expressions
* The `to_char` family of functions
* The ability to use indexes with `LIKE` clauses

The drawback of using locales other than `C` or `POSIX` in PostgreSQL is its performance impact. It slows character handling and prevents ordinary indexes from being used by `LIKE`. For this reason use locales only if you actually need them.

As a workaround to allow PostgreSQL to use indexes with `LIKE` clauses under a non-C locale, several custom operator classes exist. These allow the creation of an index that performs a strict character-by-character comparison, ignoring locale comparison rules. Refer to [Section 11.9](https://www.postgresql.org/docs/10/static/indexes-opclass.html) for more information. Another approach is to create indexes using the `C` collation, as discussed in [Section 23.2](https://www.postgresql.org/docs/10/static/collation.html).

## 23.1.3. Problems

If locale support doesn't work according to the explanation above, check that the locale support in your operating system is correctly configured. To check what locales are installed on your system, you can use the command `locale -a` if your operating system provides it.

Check that PostgreSQL is actually using the locale that you think it is. The `LC_COLLATE` and `LC_CTYPE` settings are determined when a database is created, and cannot be changed except by creating a new database. Other locale settings including `LC_MESSAGES` and `LC_MONETARY` are initially determined by the environment the server is started in, but can be changed on-the-fly. You can check the active locale settings using the `SHOW` command.

The directory `src/test/locale` in the source distribution contains a test suite for PostgreSQL's locale support.

Client applications that handle server-side errors by parsing the text of the error message will obviously have problems when the server's messages are in a different language. Authors of such applications are advised to make use of the error code scheme instead.

Maintaining catalogs of message translations requires the on-going efforts of many volunteers that want to see PostgreSQL speak their preferred language well. If messages in your language are currently not available or not fully translated, your assistance would be appreciated. If you want to help, refer to [Chapter 54](https://www.postgresql.org/docs/10/static/nls.html) or write to the developers' mailing list.

