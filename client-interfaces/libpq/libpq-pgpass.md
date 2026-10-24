<a id="LIBPQ-PGPASS"></a>

## 32.16. 密碼檔 [#](#libpq-pgpass) <a href="#libpq-pgpass" id="libpq-pgpass"></a>

<a id="id-1.7.3.23.2"></a><a id="id-1.7.3.23.3"></a>

使用者家目錄中的檔案 `.pgpass` 可以
包含密碼，供連線需要密碼（且未以其他方式指定密碼）時
使用。在 Unix 系統上，此目錄可以由
`HOME` 環境變數指定；若未定義，則為
有效使用者的家目錄。在 Microsoft Windows 上，此檔案名為
`%APPDATA%\postgresql\pgpass.conf`（其中
`%APPDATA%` 指的是使用者設定檔中的 Application Data 子目錄）。
另外，也可以使用連線參數 [passfile](libpq-connect.md#LIBPQ-CONNECT-PASSFILE)
或環境變數 `PGPASSFILE` 指定要使用的密碼檔。

此檔案應該包含下列格式的行：

```

hostname:port:database:username:password
```

（你可以複製上面這一行，並在行首加上 `#`，
在檔案中加入一行提醒用的註解。）
前四個欄位中的每一個都可以是字面值，或是
可比對任何內容的 `*`。會使用第一個符合
目前連線參數之行的密碼欄位。
（因此，使用萬用字元時，請把較具體的項目放在前面。）若項目需要包含 `:` 或
`\`，請以 `\` 跳脫該字元。
主機名稱欄位在有指定 `host` 連線
參數時與其比對，否則在有指定
`hostaddr` 參數時與其比對；若兩者都未給定，
則搜尋主機名稱 `localhost`。
當連線為 Unix 網域通訊端連線，且
`host` 參數
符合 libpq 的預設通訊端目錄路徑時，也會搜尋主機名稱 `localhost`。
在備用伺服器上，資料庫欄位為 `replication` 時，
會比對連往主要伺服器的串流複寫連線。
除此之外，資料庫欄位的用處有限，因為使用者在同一個叢集中的
所有資料庫都使用相同的密碼。

在 Unix 系統上，密碼檔的權限必須
禁止所有其他使用者（world）與群組的任何存取；可以用
`chmod 0600 ~/.pgpass` 之類的命令達成。若權限比這個
寬鬆，此檔案將被忽略。在 Microsoft Windows 上，
會假設此檔案存放在安全的目錄中，因此
不會進行特殊的權限檢查。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/libpq-pgpass.html)（原文版本：18.6；核對日期：2026-10-17）
