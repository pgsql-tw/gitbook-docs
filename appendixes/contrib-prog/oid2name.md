<a id="id-1.11.8.4.3.1"></a>

## oid2name

oid2name — 解析 PostgreSQL 資料目錄中的 OID 與檔案節點

## 語法

<a id="id-1.11.8.4.3.4.1"></a>

`oid2name` [*`option`*...]

<a id="id-1.11.8.4.3.5"></a>

## 說明

oid2name 是協助管理員檢查 PostgreSQL 所使用檔案結構的工具程式。若要使用它，必須熟悉[第 66 章](../../internals/storage/README.md)所述的資料庫檔案結構。

### 注意

「oid2name」這個名稱源自歷史，實際上相當容易誤導；因為多數使用情況真正關注的是資料表的檔案節點編號（亦即資料庫目錄中可見的檔名）。請務必瞭解資料表 OID 與資料表檔案節點之間的差異！

oid2name 會連線至目標資料庫並擷取 OID、檔案節點及／或資料表名稱資訊。它也可顯示資料庫 OID 或資料表空間 OID。

<a id="id-1.11.8.4.3.6"></a>

## 選項

oid2name 接受下列命令列引數：

`-f filenode`<br>`--filenode=filenode`
:   顯示檔案節點為 *`filenode`* 的資料表資訊。

`-i`<br>`--indexes`
:   在清單中包括索引與序列。

`-o oid`<br>`--oid=oid`
:   顯示 OID 為 *`oid`* 的資料表資訊。

`-q`<br>`--quiet`
:   省略標頭（適合用於指令碼）。

`-s`<br>`--tablespaces`
:   顯示資料表空間 OID。

`-S`<br>`--system-objects`
:   包括系統物件（位於 `information_schema`、`pg_toast` 與 `pg_catalog` schema 中的物件）。

`-t tablename_pattern`<br>`--table=tablename_pattern`
:   顯示符合 *`tablename_pattern`* 的資料表資訊。

`-V`<br>`--version`
:   顯示 oid2name 版本後結束。

`-x`<br>`--extended`
:   顯示每個列出物件的更多資訊：資料表空間名稱、schema 名稱與 OID。

`-?`<br>`--help`
:   顯示 oid2name 命令列引數的說明後結束。

oid2name 也接受下列連線參數的命令列引數：

`-d database`<br>`--dbname=database`
:   要連線的資料庫。

`-h host`<br>`--host=host`
:   資料庫伺服器主機。

`-H host`
:   資料庫伺服器主機。此參數自 PostgreSQL 12 起已*淘汰*。

`-p port`<br>`--port=port`
:   資料庫伺服器連接埠。

`-U username`<br>`--username=username`
:   用於連線的使用者名稱。

若要顯示特定資料表，請用 `-o`、`-f` 及／或 `-t` 選取要顯示的資料表。`-o` 接受 OID，`-f` 接受檔案節點，`-t` 接受資料表名稱（實際上是 `LIKE` 模式，因此可使用 `foo%` 等模式）。這些選項可任意重複使用，清單會包括符合任何選項的所有物件。不過請注意，這些選項只能顯示由 `-d` 指定之資料庫中的物件。

如果未指定 `-o`、`-f` 或 `-t`，但指定了 `-d`，它會列出 `-d` 所指定資料庫中的所有資料表。在此模式中，`-S` 與 `-i` 選項控制要列出的內容。

如果也未指定 `-d`，它會顯示資料庫 OID 清單。或者可指定 `-s` 以取得資料表空間清單。

<a id="id-1.11.8.4.3.7"></a>

## 環境

`PGHOST`<br>`PGPORT`<br>`PGUSER`
:   預設連線參數。

此工具與大多數其他 PostgreSQL 工具一樣，也會使用 libpq 支援的環境變數（請參閱[第 32.15 節](../../client-interfaces/libpq/libpq-envars.md)）。

環境變數 `PG_COLOR` 指定是否在診斷訊息中使用色彩。可用值為 `always`、`auto` 與 `never`。

<a id="id-1.11.8.4.3.8"></a>

## 注意事項

oid2name 需要正在執行且系統目錄未毀損的資料庫伺服器。因此，對於從災難性資料庫毀損情況中復原，它的用途有限。

<a id="id-1.11.8.4.3.9"></a>

## 範例

```

$ # what's in this database server, anyway?
$ oid2name
All databases:
    Oid  Database Name  Tablespace
----------------------------------
  17228       alvherre  pg_default
  17255     regression  pg_default
  17227      template0  pg_default
      1      template1  pg_default

$ oid2name -s
All tablespaces:
     Oid  Tablespace Name
-------------------------
    1663       pg_default
    1664        pg_global
  155151         fastdisk
  155152          bigdisk

$ # OK, let's look into database alvherre
$ cd $PGDATA/base/17228

$ # get top 10 db objects in the default tablespace, ordered by size
$ ls -lS * | head -10
-rw-------  1 alvherre alvherre 136536064 sep 14 09:51 155173
-rw-------  1 alvherre alvherre  17965056 sep 14 09:51 1155291
-rw-------  1 alvherre alvherre   1204224 sep 14 09:51 16717
-rw-------  1 alvherre alvherre    581632 sep  6 17:51 1255
-rw-------  1 alvherre alvherre    237568 sep 14 09:50 16674
-rw-------  1 alvherre alvherre    212992 sep 14 09:51 1249
-rw-------  1 alvherre alvherre    204800 sep 14 09:51 16684
-rw-------  1 alvherre alvherre    196608 sep 14 09:50 16700
-rw-------  1 alvherre alvherre    163840 sep 14 09:50 16699
-rw-------  1 alvherre alvherre    122880 sep  6 17:51 16751

$ # What file is 155173?
$ oid2name -d alvherre -f 155173
From database "alvherre":
  Filenode  Table Name
----------------------
    155173    accounts

$ # you can ask for more than one object
$ oid2name -d alvherre -f 155173 -f 1155291
From database "alvherre":
  Filenode     Table Name
-------------------------
    155173       accounts
   1155291  accounts_pkey

$ # you can mix the options, and get more details with -x
$ oid2name -d alvherre -t accounts -f 1155291 -x
From database "alvherre":
  Filenode     Table Name      Oid  Schema  Tablespace
------------------------------------------------------
    155173       accounts   155173  public  pg_default
   1155291  accounts_pkey  1155291  public  pg_default

$ # show disk space for every db object
$ du [0-9]* |
> while read SIZE FILENODE
> do
>   echo "$SIZE       `oid2name -q -d alvherre -i -f $FILENODE`"
> done
16            1155287  branches_pkey
16            1155289  tellers_pkey
17561            1155291  accounts_pkey
...

$ # same, but sort by size
$ du [0-9]* | sort -rn | while read SIZE FN
> do
>   echo "$SIZE   `oid2name -q -d alvherre -f $FN`"
> done
133466             155173    accounts
17561            1155291  accounts_pkey
1177              16717  pg_proc_proname_args_nsp_index
...

$ # If you want to see what's in tablespaces, use the pg_tblspc directory
$ cd $PGDATA/pg_tblspc
$ oid2name -s
All tablespaces:
     Oid  Tablespace Name
-------------------------
    1663       pg_default
    1664        pg_global
  155151         fastdisk
  155152          bigdisk

$ # what databases have objects in tablespace "fastdisk"?
$ ls -d 155151/*
155151/17228/  155151/PG_VERSION

$ # Oh, what was database 17228 again?
$ oid2name
All databases:
    Oid  Database Name  Tablespace
----------------------------------
  17228       alvherre  pg_default
  17255     regression  pg_default
  17227      template0  pg_default
      1      template1  pg_default

$ # Let's see what objects does this database have in the tablespace.
$ cd 155151/17228
$ ls -l
total 0
-rw-------  1 postgres postgres 0 sep 13 23:20 155156

$ # OK, this is a pretty small table ... but which one is it?
$ oid2name -d alvherre -f 155156
From database "alvherre":
  Filenode  Table Name
----------------------
    155156         foo
```

<a id="id-1.11.8.4.3.10"></a>

## 作者

B. Palmer `<bpalmer@crimelabs.net>`

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/oid2name.html)
