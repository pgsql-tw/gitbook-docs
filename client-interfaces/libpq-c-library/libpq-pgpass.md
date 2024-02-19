# 34.16. 密碼檔

如果連線需要密碼（並且沒有指定密碼），使用者主目錄中的 .pgpass 檔案可以內含要使用的密碼。在 Microsoft Windows 上，該檔案路徑為 ％APPDATA％\postgresql\pgpass.conf（其中 ％APPDATA％ 指使用者組態檔案中的 Application Data 目錄）。或者，可以使用連接參數 passfile 或環境變數 PGPASSFILE 來指定密碼檔案。

該檔案應該包含以下格式的內容：

```
hostname:port:database:username:password
```

（您可以透過複製上面的內容並在 # 之前增加提醒註解到該檔案。）前四個字段中的每一個都可以是一個文字字串，或 \*，它可以匹配任何內容。 將使用匹配目前連線參數第一行中的密碼字串。（因此，在使用通用配對字時首先輸入更具體的項目。）如果項目需要包含「:」或「\」，請使用「\」跳脫字元。localhost 的主機名稱匹配來自本地機器的 TCP（主機名localhost）和 Unix domain socket（pghost 為空或預設的 domain socket 路徑）連線。 在備援伺服器中，複製的資料庫名稱與主服務器上的串流備援連線匹配。資料庫字段的用處有限，因為使用者對同一叢集中的所有資料庫具有相同的密碼。

在 Unix 系統上，密碼檔案的權限必須禁止任何對所有其他人或組群的存取；透過 chmod 0600 \~/.pgpass 等命令來設定。如果權限不是如此嚴格設定，則該檔案將被忽略。在Microsoft Windows上，則假設檔案儲存在安全的目錄中，因此不會進行特殊的權限檢查。
