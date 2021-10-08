# CREATE DATABASE

CREATE DATABASE — 建立一個新的資料庫

## 語法

```text
CREATE DATABASE name
    [ [ WITH ] [ OWNER [=] user_name ]
           [ TEMPLATE [=] template ]
           [ ENCODING [=] encoding ]
           [ LC_COLLATE [=] lc_collate ]
           [ LC_CTYPE [=] lc_ctype ]
           [ TABLESPACE [=] tablespace_name ]
           [ ALLOW_CONNECTIONS [=] allowconn ]
           [ CONNECTION LIMIT [=] connlimit ]
           [ IS_TEMPLATE [=] istemplate ] ]
```

## 說明

CREATE DATABASE 建立一個新的 PostgreSQL 資料庫。

要建立資料庫，您必須是超級使用者或具有特殊的 CREATEDB 權限。請參閱 [CREATE USER](create-user.md)。

預設情況下，將透過複製標準系統資料庫 template1 來建立新的資料庫。可以透過修改 TEMPLATE 名稱來指定不同的樣板。特別是，通過修改 TEMPLATE template0，您可以建立一個僅包含您的 PostgreSQL 版本預定義的標準物件的原始資料庫。如果您希望避免複製可能已添加到 template1 的任何本地物件，這將非常有用。

## 參數

_`name`_

要建立的資料庫名稱。

_`user_name`_

將擁有新資料庫的使用者角色名稱，或 DEFAULT 使用預設值（即執行指令的使用者）。要建立由其他角色擁有的資料庫，您必須是該角色的直接或間接成員，或者是超級使用者。

_`template`_

從中建立新資料庫的樣板名稱，或 DEFAULT 以使用預設樣板（template1）。

_`encoding`_

要在新資料庫中使用的字元集編碼。指定字串常數（例如，'SQL\_ASCII'）或整數編碼數字，或指定 DEFAULT 以使用預設編碼（即樣板資料庫的編碼）。 PostgreSQL 伺服器支援的字元集在[第 23.3.1 節](../../server-administration/localization/character-set-support.md#23-3-1-supported-character-sets)中描述。其他限制請參閱下面說明。

_`lc_collate`_

要在新資料庫中使用的排列順序（LC\_COLLATE）。這會影響套用於字串的排序順序，例如在使用 ORDER BY的查詢中，以及在文字欄位索引中使用的順序。預設設定是使用樣板資料庫的排序順序。其他限制請參閱下面說明。

_`lc_ctype`_

要在新資料庫中使用的字元分類（LC\_CTYPE）。這會影響字元的分類，例如小寫、大寫和數字。預設設定是使用樣板資料庫的字元分類。其他限制請參閱下面的說明。

_`tablespace_name`_

將與新資料庫關連的資料表空間名稱，或 DEFAULT 以使用樣板資料庫的資料表空間。此資料表空間將是用於在此資料庫中建立物件的預設資料表空間。有關更多訊息，請參閱 [CREATE TABLESPACE](create-tablespace.md)。

_`allowconn`_

如果為 false，則沒有人可以連線到此資料庫。預設值為 true，允許連線（除非受到其他機制限制，例如 GRANT / REVOKE CONNECT）。

_`connlimit`_

可以對此資料庫建立多少同時連線。 -1（預設值）表示沒有限制。

_`istemplate`_

如果為 true，則任何具有 CREATEDB 權限的使用者都可以複製此資料庫；如果為false（預設值），則只有超級使用者或資料庫的擁有者才能複製它。

選擇性參數可以按任何順序輸入，而不僅僅是上面說明的順序。

## 注意

不能在交易事務區塊內執行 CREATE DATABASE。

「無法初始化資料庫目錄」的錯誤很可能與資料目錄，磁碟空間滿載或其他檔案系統的權限不足問題有關。

使用 [DROP DATABASE](drop-database.md) 移除資料庫。

工具 [createdb](../client-applications/createdb.md) 是一個封裝此指令的程式，為方便起見而提供。

不會從樣板資料庫中複製資料庫級的組態參數（透過 ALTER DATABASE 設定）。

雖然可以透過將其名稱指定為模板來複製除 template1 之外的資料庫，但這並不是（通常）用作通用的「COPY DATABASE」工具。主要限制是在複製樣板資料庫時不能有其他連線到樣板資料庫。如果啟動時存在任何其他連線，則 CREATE DATABASE 將失敗；否則，在 CREATE DATABASE 完成之前，將鎖定與樣版資料庫新的連線。有關更多訊息，請參閱[第 22.3 節](../../server-administration/managing-databases/template-databases.md)。

為新資料庫指定的字元集編碼必須與所選的區域設定（LC\_COLLATE 和 LC\_CTYPE）相容。如果語言環境是 C（或等效 POSIX），則允許所有編碼，但對於其他語言環境設定，只有一種編碼可以正常工作。（不過，在Windows上，UTF-8 編碼可以與任何語言環境一起使用。）CREATE DATABASE 將允許超級使用者指定 SQL\_ASCII 編碼而不管語言環境設定如何，但是這種方式已被棄用。如果資料可能導致字串函數的不當行為，則與語言環境不相容的編碼就會儲存在資料庫中。

編碼和語言環境設定必須與樣板資料庫的設定相符合，除非將 template0 用作樣板。這是因為其他資料庫可能包含與指定編碼不相符合的資料，或者可能包含其排序順序受 LC\_COLLATE 和 LC\_CTYPE 影響的索引。複製此類資料將導致資料庫根據新設定而損壞。總之，template0 不包含任何會受影響的資料或索引。

CONNECTION LIMIT 選項僅近乎強制執行：如果兩個新連線幾乎同時開始，當資料庫只剩下一個連線「插槽」時，則兩者都可能會失敗。此外，不會對超級使用者或後台工作程序強制執行此限制。

## 範例

要建立新資料庫：

```text
CREATE DATABASE lusiadas;
```

使用 salesspace 預設資料表空間並建立由使用者 salesapp 所擁有的資料庫 sales：

```text
CREATE DATABASE sales OWNER salesapp TABLESPACE salesspace;
```

要使用不同的區域設定來建立資料庫 music：

```text
CREATE DATABASE music
    LC_COLLATE 'sv_SE.utf8' LC_CTYPE 'sv_SE.utf8'
    TEMPLATE template0;
```

在此範例中，如果指定的語言環境與 template1 中的語言環境不同，則需要 TEMPLATE template0 子句。（如果不是，則明確指定語言環境是多餘的。）

要建立具有不同區域設定和不同字元集編碼的資料庫 music2：

```text
CREATE DATABASE music2
    LC_COLLATE 'sv_SE.iso885915' LC_CTYPE 'sv_SE.iso885915'
    ENCODING LATIN9
    TEMPLATE template0;
```

指定的區域設定和編碼設定必須相符合，否則將回報錯誤。

請注意，區域設定名稱專屬於作業系統，因此上述指令可能無法在其他地方以相同的方式工作。

## 相容性

SQL 標準中沒有 CREATE DATABASE 語句。資料庫等同於目錄，其建立是實作上定義的。

## 參閱

[ALTER DATABASE](alter-database.md), [DROP DATABASE](drop-database.md)

