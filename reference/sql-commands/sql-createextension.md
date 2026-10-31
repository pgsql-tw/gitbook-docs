<a id="SQL-CREATEEXTENSION"></a><a id="id-1.9.3.64.1"></a>

## CREATE EXTENSION

CREATE EXTENSION — 安裝擴充功能

<a id="id-1.9.3.64.4"></a>

## 語法

```

CREATE EXTENSION [ IF NOT EXISTS ] extension_name
    [ WITH ] [ SCHEMA schema_name ]
             [ VERSION version ]
             [ CASCADE ]
```

<a id="id-1.9.3.64.5"></a>

## 說明

`CREATE EXTENSION` 會將新的擴充功能載入目前的資料庫。資料庫中不得已載入同名的擴充功能。

載入擴充功能基本上就等於執行該擴充功能的腳本檔。這個腳本通常會建立新的 SQL 物件，例如函式、資料型別、運算子與索引支援方法。`CREATE EXTENSION` 另外還會記錄所有被建立之物件的識別資訊，以便在發出 `DROP EXTENSION` 時能再次將它們移除。

執行 `CREATE EXTENSION` 的使用者會成為該擴充功能的擁有者（用於日後的權限檢查），而且通常也會成為該擴充功能腳本所建立之任何物件的擁有者。

載入擴充功能通常需要的權限，與建立其組成物件所需的權限相同。對許多擴充功能而言，這表示需要超級使用者權限。不過，若擴充功能在其控制檔中被標記為 *trusted*（受信任），則任何在目前資料庫上具有 `CREATE` 權限的使用者都可以安裝它。在這種情況下，擴充功能物件本身將由呼叫的使用者擁有，但其中包含的物件將由啟動用超級使用者（bootstrap superuser）擁有（除非擴充功能的腳本明確地將它們指派給呼叫的使用者）。這種設定讓呼叫的使用者有權移除該擴充功能，但無權修改其中的個別物件。

<a id="id-1.9.3.64.6"></a>

## 參數

`IF NOT EXISTS`
:   已存在同名的擴充功能時不擲出錯誤；此情況會發出 notice。請注意，並不保證現有的擴充功能和以目前可用之腳本檔所建立的擴充功能有任何相似之處。

*`extension_name`*
:   要安裝之擴充功能的名稱。PostgreSQL 會使用檔案 `extension_name.control` 中的詳細資訊來建立擴充功能，該檔案是透過伺服器的擴充功能控制路徑（由 [extension_control_path](../../server-administration/runtime-config/runtime-config-client.md#GUC-EXTENSION-CONTROL-PATH) 設定）找到的。

*`schema_name`*

在擴充功能允許其內容被重新安置的前提下，要將擴充功能物件安裝到其中之綱要的名稱。指定的綱要必須已存在。若未指定，且擴充功能的控制檔也未指定綱要，則使用目前預設的物件建立綱要。

若擴充功能在其控制檔中指定了 `schema` 參數，則該綱要不能用 `SCHEMA` 子句覆寫。通常，若給定了 `SCHEMA` 子句，且它與擴充功能的 `schema` 參數衝突，就會引發錯誤。不過，若同時也給定了 `CASCADE` 子句，則在衝突時會忽略 *`schema_name`*。給定的 *`schema_name`* 將用於安裝任何需要的、且未在其控制檔中指定 `schema` 的擴充功能。

請記住，擴充功能本身並不被視為位於任何綱要之內：擴充功能具有未經限定的名稱，而且必須在整個資料庫中是唯一的。但屬於擴充功能的物件可以位於綱要之內。

*`version`*
:   要安裝之擴充功能的版本。可以寫成識別字或字串常值。預設版本是擴充功能控制檔中所指定的版本。

`CASCADE`
:   自動安裝此擴充功能所相依、但尚未安裝的任何擴充功能。它們的相依項目同樣會以遞迴方式自動安裝。`SCHEMA` 子句（若有給定）會套用到所有以這種方式安裝的擴充功能。此陳述式的其他選項不會套用到自動安裝的擴充功能；特別是，一律會選擇它們的預設版本。

<a id="id-1.9.3.64.7"></a>

## 注意事項

在你可以使用 `CREATE EXTENSION` 將擴充功能載入資料庫之前，必須先安裝該擴充功能的支援檔案。關於安裝 PostgreSQL 所附擴充功能的資訊，可以在[附加提供的模組](../../appendixes/contrib/README.md)中找到。

目前可供載入的擴充功能，可以從
[`pg_available_extensions`](../../internals/views/view-pg-available-extensions.md)
或
[`pg_available_extension_versions`](../../internals/views/view-pg-available-extension-versions.md)
系統檢視表中查得。

<a id="id-1.9.3.64.7.4"></a>

### 注意 [#](#xiao-xin) <a href="#xiao-xin" id="xiao-xin"></a>

{% hint style="warning" %}
以超級使用者身分安裝擴充功能，需要信任擴充功能的作者以安全的方式撰寫了擴充功能安裝腳本。對惡意使用者而言，建立特洛伊木馬物件並不是非常困難，這些物件會危害日後執行的、撰寫不夠謹慎的擴充功能腳本，讓該使用者取得超級使用者權限。不過，特洛伊木馬物件只有在腳本執行期間位於 `search_path` 中時才會有危險，也就是說，它們位於擴充功能的安裝目標綱要中，或位於其所相依之某個擴充功能的綱要中。因此，在處理腳本尚未經過仔細審查的擴充功能時，一個好的經驗法則是：只將它們安裝到從未、也將不會授予任何不受信任使用者 CREATE 權限的綱要中。它們所相依的任何擴充功能也是如此。

PostgreSQL 所附的擴充功能被認為能抵禦這類安裝時期的攻擊，但相依於其他擴充功能的少數幾個除外。如這些擴充功能的文件所述，它們應該安裝到安全的綱要中，或安裝到與它們所相依之擴充功能相同的綱要中，或兩者兼具。
{% endhint %}

關於撰寫新擴充功能的資訊，請參閱[第 36.17 節](../../server-programming/extend/extend-extensions.md)。

<a id="id-1.9.3.64.8"></a>

## 範例

將 [hstore](../../appendixes/contrib/hstore.md) 擴充功能安裝到目前的資料庫，並將其物件放在綱要 `addons` 中：

```

CREATE EXTENSION hstore SCHEMA addons;
```

達成相同目的的另一種方式：

```

SET search_path = addons;
CREATE EXTENSION hstore;
```

<a id="id-1.9.3.64.9"></a>

## 相容性

`CREATE EXTENSION` 是 PostgreSQL 的擴充語法。

<a id="id-1.9.3.64.10"></a>

## 另請參閱

[ALTER EXTENSION](sql-alterextension.md), [DROP EXTENSION](sql-dropextension.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-createextension.html)（原文版本：18.6；核對日期：2026-10-04）
