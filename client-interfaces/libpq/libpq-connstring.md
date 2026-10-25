<a id="LIBPQ-CONNSTRING"></a>

## 32.1.1. 連線字串 [#](#libpq-connstring) <a href="#libpq-connstring" id="libpq-connstring"></a>

<a id="id-1.7.3.8.3.2"></a><a id="id-1.7.3.8.3.3"></a>

有幾個 libpq 函式會剖析使用者指定的字串以取得連線參數。這些字串有兩種可接受的格式：一般的關鍵字／值字串與 URI。URI 大致上遵循 [RFC
3986](https://datatracker.ietf.org/doc/html/rfc3986)，但允許如下文進一步所述的多主機連線字串。

<a id="LIBPQ-CONNSTRING-KEYWORD-VALUE"></a>

### 32.1.1.1. 關鍵字／值連線字串 [#](#libpq-connstring-keyword-value) <a href="#libpq-connstring-keyword-value" id="libpq-connstring-keyword-value"></a>

在關鍵字／值格式中，每個參數設定的形式為 *`keyword`* `=` *`value`*，設定之間以空白分隔。設定中等號兩側的空白可有可無。要寫入空值或包含空白的值，請以單引號括住，例如 `keyword = 'a value'`。值中的單引號與反斜線必須以反斜線跳脫，也就是 `\'` 與 `\\`。

範例：

```

host=localhost port=5432 dbname=mydb connect_timeout=10
```

可辨識的參數關鍵字列於[第 32.1.2 節](libpq-paramkeywords.md#libpq-paramkeywords)。

<a id="LIBPQ-CONNSTRING-URIS"></a>

### 32.1.1.2. 連線 URI [#](#libpq-connstring-uris) <a href="#libpq-connstring-uris" id="libpq-connstring-uris"></a>

連線 URI 的一般形式為：

```

postgresql://[userspec@][hostspec][/dbname][?paramspec]

where userspec is:

user[:password]

and hostspec is:

[host][:port][,...]

and paramspec is:

name=value[&...]
```

URI 架構（scheme）指示符可以是 `postgresql://` 或 `postgres://`。URI 其餘的每個部分都是選用的。下列範例示範有效的 URI 語法：

```

postgresql://
postgresql://localhost
postgresql://localhost:5433
postgresql://localhost/mydb
postgresql://user@localhost
postgresql://user:secret@localhost
postgresql://other@localhost/otherdb?connect_timeout=10&application_name=myapp
postgresql://host1:123,host2:456/somedb?target_session_attrs=any&application_name=myapp
```

通常出現在 URI 階層部分的值，也可以改用具名參數提供。例如：

```

postgresql:///mydb?host=localhost&port=5433
```

所有具名參數都必須符合[第 32.1.2 節](libpq-paramkeywords.md#libpq-paramkeywords)所列的關鍵字，但為了與 JDBC 連線 URI 相容，`ssl=true` 會被轉換為 `sslmode=require`。

如果連線 URI 的任何部分包含具有特殊意義的符號，就需要以[百分比編碼](https://datatracker.ietf.org/doc/html/rfc3986#section-2.1)進行編碼。以下範例中，等號（`=`）被替換為 `%3D`，空白字元被替換為 `%20`：

```

postgresql://user@localhost:5433/mydb?options=-c%20synchronous_commit%3Doff
```

主機部分可以是主機名稱或 IP 位址。要指定 IPv6 位址，請以方括號括住：

```

postgresql://[2001:db8::1234]/database
```

主機部分的解讀方式與參數 [host](libpq-paramkeywords.md#libpq-connect-host) 的說明相同。特別是，如果主機部分是空的或看起來像絕對路徑名稱，就會選擇 Unix 網域通訊端連線，否則會發起 TCP/IP 連線。不過請注意，斜線在 URI 的階層部分中是保留字元。因此，要指定非標準的 Unix 網域通訊端目錄，可以省略 URI 的主機部分並將主機指定為具名參數，或者在 URI 的主機部分中對路徑進行百分比編碼：

```

postgresql:///dbname?host=/var/lib/postgresql
postgresql://%2Fvar%2Flib%2Fpostgresql/dbname
```

可以在單一 URI 中指定多個主機元件，每個主機元件都可以選擇性地搭配連接埠元件。形式為 `postgresql://host1:port1,host2:port2,host3:port3/` 的 URI，等同於形式為 `host=host1,host2,host3 port=port1,port2,port3` 的連線字串。如下文進一步所述，會依序嘗試每個主機，直到成功建立連線為止。

<a id="LIBPQ-MULTIPLE-HOSTS"></a>

### 32.1.1.3. 指定多個主機 [#](#libpq-multiple-hosts) <a href="#libpq-multiple-hosts" id="libpq-multiple-hosts"></a>

可以指定多個要連線的主機，讓它們依指定的順序嘗試。在關鍵字／值格式中，`host`、`hostaddr` 與 `port` 選項接受以逗號分隔的值清單。在每個有指定的選項中，必須提供相同數量的元素，例如第一個 `hostaddr` 對應第一個主機名稱，第二個 `hostaddr` 對應第二個主機名稱，依此類推。例外的是，如果只指定了一個 `port`，它會套用到所有主機。

在連線 URI 格式中，你可以在 URI 的 `host` 元件中列出多個以逗號分隔的 `host:port` 配對。

無論使用哪種格式，單一主機名稱都可能解析為多個網路位址。常見的例子是一台同時具有 IPv4 與 IPv6 位址的主機。

當指定了多個主機，或單一主機名稱解析為多個位址時，會依序嘗試所有的主機與位址，直到其中一個成功為止。如果所有主機都無法連上，連線就會失敗。如果成功建立了連線但認證失敗，就不會再嘗試清單中其餘的主機。

如果使用密碼檔，你可以為不同的主機設定不同的密碼。其他所有連線選項對清單中的每個主機都相同；例如，無法為不同的主機指定不同的使用者名稱。


[返回 32.1. 資料庫連線控制函式](libpq-connect.md#libpq-connect)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-connect.html)（原文版本：18.6；核對日期：2026-10-18）
