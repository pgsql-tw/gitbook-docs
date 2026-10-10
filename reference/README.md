<a id="REFERENCE"></a>

# 第六部分：參考

<a id="id-1.9.2"></a>

本參考中的各個條目，旨在以合理的篇幅，對各自的主題提供權威、完整且正式的摘要。關於 PostgreSQL 使用方式的更多資訊，以敘述、教學或範例的形式，可以在本書的其他部分找到。請參閱各參考頁面上列出的交叉參照。

這些參考條目也以傳統的「man」頁面形式提供。

**目錄**

[I. SQL 命令](sql-commands/README.md)
:   [ABORT](sql-commands/sql-abort.md) — 中止目前的交易

    [ALTER AGGREGATE](sql-commands/sql-alteraggregate.md) — 變更彙總函式的定義

    [ALTER COLLATION](sql-commands/sql-altercollation.md) — 變更定序的定義

    [ALTER CONVERSION](sql-commands/sql-alterconversion.md) — 變更轉換的定義

    [ALTER DATABASE](sql-commands/sql-alterdatabase.md) — 變更資料庫

    [ALTER DEFAULT PRIVILEGES](sql-commands/sql-alterdefaultprivileges.md) — 定義預設存取權限

    [ALTER DOMAIN](sql-commands/sql-alterdomain.md) — 變更網域的定義

    [ALTER EVENT TRIGGER](sql-commands/sql-altereventtrigger.md) — 變更事件觸發程序的定義

    [ALTER EXTENSION](sql-commands/sql-alterextension.md) — 變更擴充功能的定義

    [ALTER FOREIGN DATA WRAPPER](sql-commands/sql-alterforeigndatawrapper.md) — 變更外部資料包裝器的定義

    [ALTER FOREIGN TABLE](sql-commands/sql-alterforeigntable.md) — 變更外部資料表的定義

    [ALTER FUNCTION](sql-commands/sql-alterfunction.md) — 變更函式的定義

    [ALTER GROUP](sql-commands/sql-altergroup.md) — 變更角色名稱或成員資格

    [ALTER INDEX](sql-commands/sql-alterindex.md) — 變更索引的定義

    [ALTER LANGUAGE](sql-commands/sql-alterlanguage.md) — 變更程序語言的定義

    [ALTER LARGE OBJECT](sql-commands/sql-alterlargeobject.md) — 變更大型物件的定義

    [ALTER MATERIALIZED VIEW](sql-commands/sql-altermaterializedview.md) — 變更具體化檢視表的定義

    [ALTER OPERATOR](sql-commands/sql-alteroperator.md) — 變更運算子的定義

    [ALTER OPERATOR CLASS](sql-commands/sql-alteropclass.md) — 變更運算子類別的定義

    [ALTER OPERATOR FAMILY](sql-commands/sql-alteropfamily.md) — 變更運算子家族的定義

    [ALTER POLICY](sql-commands/sql-alterpolicy.md) — 變更資料列層級安全性政策的定義

    [ALTER PROCEDURE](sql-commands/sql-alterprocedure.md) — 變更程序的定義

    [ALTER PUBLICATION](sql-commands/sql-alterpublication.md) — 變更發佈的定義

    [ALTER ROLE](sql-commands/sql-alterrole.md) — 變更資料庫角色

    [ALTER ROUTINE](sql-commands/sql-alterroutine.md) — 變更常式的定義

    [ALTER RULE](sql-commands/sql-alterrule.md) — 變更規則的定義

    [ALTER SCHEMA](sql-commands/sql-alterschema.md) — 變更綱要的定義

    [ALTER SEQUENCE](sql-commands/sql-altersequence.md) — 變更序列產生器的定義

    [ALTER SERVER](sql-commands/sql-alterserver.md) — 變更外部伺服器的定義

    [ALTER STATISTICS](sql-commands/sql-alterstatistics.md) — 變更擴充統計資訊物件的定義

    [ALTER SUBSCRIPTION](sql-commands/sql-altersubscription.md) — 變更訂閱的定義

    [ALTER SYSTEM](sql-commands/sql-altersystem.md) — 變更伺服器設定參數

    [ALTER TABLE](sql-commands/sql-altertable.md) — 變更資料表的定義

    [ALTER TABLESPACE](sql-commands/sql-altertablespace.md) — 變更資料表空間的定義

    [ALTER TEXT SEARCH CONFIGURATION](sql-commands/sql-altertsconfig.md) — 變更文字搜尋設定的定義

    [ALTER TEXT SEARCH DICTIONARY](sql-commands/sql-altertsdictionary.md) — 變更文字搜尋字典的定義

    [ALTER TEXT SEARCH PARSER](sql-commands/sql-altertsparser.md) — 變更文字搜尋剖析器的定義

    [ALTER TEXT SEARCH TEMPLATE](sql-commands/sql-altertstemplate.md) — 變更文本搜尋模板的定義

    [ALTER TRIGGER](sql-commands/sql-altertrigger.md) — 變更觸發程序的定義

    [ALTER TYPE](sql-commands/sql-altertype.md) — 變更型別的定義

    [ALTER USER](sql-commands/sql-alteruser.md) — 變更資料庫角色

    [ALTER USER MAPPING](sql-commands/sql-alterusermapping.md) — 變更使用者對應的定義

    [ALTER VIEW](sql-commands/sql-alterview.md) — 變更檢視表的定義

    [ANALYZE](sql-commands/sql-analyze.md) — 收集資料庫的統計資訊

    [BEGIN](sql-commands/sql-begin.md) — 開始一個交易區塊

    [CALL](sql-commands/sql-call.md) — 呼叫程序

    [CHECKPOINT](sql-commands/sql-checkpoint.md) — 強制執行預寫式日誌檢查點

    [CLOSE](sql-commands/sql-close.md) — 關閉游標

    [CLUSTER](sql-commands/sql-cluster.md) — 依據索引將資料表叢集化

    [COMMENT](sql-commands/sql-comment.md) — 定義或變更物件的註解

    [COMMIT](sql-commands/sql-commit.md) — 提交目前的交易

    [COMMIT PREPARED](sql-commands/sql-commit-prepared.md) — 提交先前已為兩階段提交而準備的交易

    [COPY](sql-commands/sql-copy.md) — 在檔案與資料表之間複製資料

    [CREATE ACCESS METHOD](sql-commands/sql-create-access-method.md) — 定義新的存取方法

    [CREATE AGGREGATE](sql-commands/sql-createaggregate.md) — 定義新的彙總函式

    [CREATE CAST](sql-commands/sql-createcast.md) — 定義新的型別轉換

    [CREATE COLLATION](sql-commands/sql-createcollation.md) — 定義新的定序

    [CREATE CONVERSION](sql-commands/sql-createconversion.md) — 定義新的編碼轉換

    [CREATE DATABASE](sql-commands/sql-createdatabase.md) — 建立新的資料庫

    [CREATE DOMAIN](sql-commands/sql-createdomain.md) — 定義新的網域

    [CREATE EVENT TRIGGER](sql-commands/sql-createeventtrigger.md) — 定義新的事件觸發程序

    [CREATE EXTENSION](sql-commands/sql-createextension.md) — 安裝擴充功能

    [CREATE FOREIGN DATA WRAPPER](sql-commands/sql-createforeigndatawrapper.md) — 定義新的外部資料包裝器

    [CREATE FOREIGN TABLE](sql-commands/sql-createforeigntable.md) — 定義新的外部資料表

    [CREATE FUNCTION](sql-commands/sql-createfunction.md) — 定義新的函式

    [CREATE GROUP](sql-commands/sql-creategroup.md) — 定義新的資料庫角色

    [CREATE INDEX](sql-commands/sql-createindex.md) — 定義新的索引

    [CREATE LANGUAGE](sql-commands/sql-createlanguage.md) — 定義新的程序語言

    [CREATE MATERIALIZED VIEW](sql-commands/sql-creatematerializedview.md) — 定義新的具體化檢視表

    [CREATE OPERATOR](sql-commands/sql-createoperator.md) — 定義新的運算子

    [CREATE OPERATOR CLASS](sql-commands/sql-createopclass.md) — 定義新的運算子類別

    [CREATE OPERATOR FAMILY](sql-commands/sql-createopfamily.md) — 定義新的運算子家族

    [CREATE POLICY](sql-commands/sql-createpolicy.md) — 為資料表定義新的資料列層級安全性政策

    [CREATE PROCEDURE](sql-commands/sql-createprocedure.md) — 定義新的程序

    [CREATE PUBLICATION](sql-commands/sql-createpublication.md) — 定義新的發佈

    [CREATE ROLE](sql-commands/sql-createrole.md) — 定義新的資料庫角色

    [CREATE RULE](sql-commands/sql-createrule.md) — 定義新的重寫規則

    [CREATE SCHEMA](sql-commands/sql-createschema.md) — 定義新的綱要

    [CREATE SEQUENCE](sql-commands/sql-createsequence.md) — 定義新的序列產生器

    [CREATE SERVER](sql-commands/sql-createserver.md) — 定義新的外部伺服器

    [CREATE STATISTICS](sql-commands/sql-createstatistics.md) — 定義擴充統計資訊

    [CREATE SUBSCRIPTION](sql-commands/sql-createsubscription.md) — 定義新的訂閱

    [CREATE TABLE](sql-commands/sql-createtable.md) — 定義新的資料表

    [CREATE TABLE AS](sql-commands/sql-createtableas.md) — 以查詢的結果定義新的資料表

    [CREATE TABLESPACE](sql-commands/sql-createtablespace.md) — 定義新的資料表空間

    [CREATE TEXT SEARCH CONFIGURATION](sql-commands/sql-createtsconfig.md) — 定義新的文字搜尋設定

    [CREATE TEXT SEARCH DICTIONARY](sql-commands/sql-createtsdictionary.md) — 定義新的文字搜尋字典

    [CREATE TEXT SEARCH PARSER](sql-commands/sql-createtsparser.md) — 定義新的文字搜尋剖析器

    [CREATE TEXT SEARCH TEMPLATE](sql-commands/sql-createtstemplate.md) — 定義新的文字搜尋範本

    [CREATE TRANSFORM](sql-commands/sql-createtransform.md) — 定義新的轉換

    [CREATE TRIGGER](sql-commands/sql-createtrigger.md) — 定義新的觸發程序

    [CREATE TYPE](sql-commands/sql-createtype.md) — 定義新的資料型別

    [CREATE USER](sql-commands/sql-createuser.md) — 定義新的資料庫角色

    [CREATE USER MAPPING](sql-commands/sql-createusermapping.md) — 定義使用者到外部伺服器的新對應

    [CREATE VIEW](sql-commands/sql-createview.md) — 定義新的檢視表

    [DEALLOCATE](sql-commands/sql-deallocate.md) — 釋放預備陳述式

    [DECLARE](sql-commands/sql-declare.md) — 定義游標

    [DELETE](sql-commands/sql-delete.md) — 刪除資料表中的資料列

    [DISCARD](sql-commands/sql-discard.md) — 捨棄工作階段狀態

    [DO](sql-commands/sql-do.md) — 執行匿名程式碼區塊

    [DROP ACCESS METHOD](sql-commands/sql-drop-access-method.md) — 移除存取方法

    [DROP AGGREGATE](sql-commands/sql-dropaggregate.md) — 移除彙總函式

    [DROP CAST](sql-commands/sql-dropcast.md) — 移除型別轉換

    [DROP COLLATION](sql-commands/sql-dropcollation.md) — 移除定序

    [DROP CONVERSION](sql-commands/sql-dropconversion.md) — 移除轉換

    [DROP DATABASE](sql-commands/sql-dropdatabase.md) — 移除資料庫

    [DROP DOMAIN](sql-commands/sql-dropdomain.md) — 移除網域

    [DROP EVENT TRIGGER](sql-commands/sql-dropeventtrigger.md) — 移除事件觸發器

    [DROP EXTENSION](sql-commands/sql-dropextension.md) — 移除擴充功能

    [DROP FOREIGN DATA WRAPPER](sql-commands/sql-dropforeigndatawrapper.md) — 移除外部資料包裝器

    [DROP FOREIGN TABLE](sql-commands/sql-dropforeigntable.md) — 移除外部資料表

    [DROP FUNCTION](sql-commands/sql-dropfunction.md) — 移除函式

    [DROP GROUP](sql-commands/sql-dropgroup.md) — 移除資料庫角色

    [DROP INDEX](sql-commands/sql-dropindex.md) — 移除索引

    [DROP LANGUAGE](sql-commands/sql-droplanguage.md) — 移除程序語言

    [DROP MATERIALIZED VIEW](sql-commands/sql-dropmaterializedview.md) — 移除具體化檢視表

    [DROP OPERATOR](sql-commands/sql-dropoperator.md) — 移除運算子

    [DROP OPERATOR CLASS](sql-commands/sql-dropopclass.md) — 移除運算子類別

    [DROP OPERATOR FAMILY](sql-commands/sql-dropopfamily.md) — 移除運算子家族

    [DROP OWNED](sql-commands/sql-drop-owned.md) — 移除資料庫角色所擁有的資料庫物件

    [DROP POLICY](sql-commands/sql-droppolicy.md) — 從資料表移除資料列層級安全性政策

    [DROP PROCEDURE](sql-commands/sql-dropprocedure.md) — 移除程序

    [DROP PUBLICATION](sql-commands/sql-droppublication.md) — 移除發佈物件

    [DROP ROLE](sql-commands/sql-droprole.md) — 移除資料庫角色

    [DROP ROUTINE](sql-commands/sql-droproutine.md) — 移除常式

    [DROP RULE](sql-commands/sql-droprule.md) — 移除重寫規則

    [DROP SCHEMA](sql-commands/sql-dropschema.md) — 移除綱要

    [DROP SEQUENCE](sql-commands/sql-dropsequence.md) — 移除序列

    [DROP SERVER](sql-commands/sql-dropserver.md) — 移除外部伺服器描述器

    [DROP STATISTICS](sql-commands/sql-dropstatistics.md) — 移除擴充統計資訊

    [DROP SUBSCRIPTION](sql-commands/sql-dropsubscription.md) — 移除訂閱

    [DROP TABLE](sql-commands/sql-droptable.md) — 移除資料表

    [DROP TABLESPACE](sql-commands/sql-droptablespace.md) — 移除資料表空間

    [DROP TEXT SEARCH CONFIGURATION](sql-commands/sql-droptsconfig.md) — 移除文字搜尋設定

    [DROP TEXT SEARCH DICTIONARY](sql-commands/sql-droptsdictionary.md) — 移除文字搜尋字典

    [DROP TEXT SEARCH PARSER](sql-commands/sql-droptsparser.md) — 移除文字搜尋剖析器

    [DROP TEXT SEARCH TEMPLATE](sql-commands/sql-droptstemplate.md) — 移除文字搜尋範本

    [DROP TRANSFORM](sql-commands/sql-droptransform.md) — 移除轉換

    [DROP TRIGGER](sql-commands/sql-droptrigger.md) — 移除觸發程序

    [DROP TYPE](sql-commands/sql-droptype.md) — 移除資料型別

    [DROP USER](sql-commands/sql-dropuser.md) — 移除資料庫角色

    [DROP USER MAPPING](sql-commands/sql-dropusermapping.md) — 移除外部伺服器的使用者對應

    [DROP VIEW](sql-commands/sql-dropview.md) — 移除檢視表

    [END](sql-commands/sql-end.md) — 提交目前的交易

    [EXECUTE](sql-commands/sql-execute.md) — 執行預備陳述式

    [EXPLAIN](sql-commands/sql-explain.md) — 顯示陳述式的執行計畫

    [FETCH](sql-commands/sql-fetch.md) — 使用游標從查詢中取回資料列

    [GRANT](sql-commands/sql-grant.md) — 定義存取權限

    [IMPORT FOREIGN SCHEMA](sql-commands/sql-importforeignschema.md) — 從外部伺服器匯入資料表定義

    [INSERT](sql-commands/sql-insert.md) — 在資料表中建立新的資料列

    [LISTEN](sql-commands/sql-listen.md) — 監聽通知

    [LOAD](sql-commands/sql-load.md) — 載入共享函式庫檔案

    [LOCK](sql-commands/sql-lock.md) — 鎖定一個資料表

    [MERGE](sql-commands/sql-merge.md) — 依條件插入、更新或刪除資料表中的資料列

    [MOVE](sql-commands/sql-move.md) — 定位游標

    [NOTIFY](sql-commands/sql-notify.md) — 產生通知

    [PREPARE](sql-commands/sql-prepare.md) — 準備一則陳述式以供執行

    [PREPARE TRANSACTION](sql-commands/sql-prepare-transaction.md) — 為兩階段提交準備目前的交易

    [REASSIGN OWNED](sql-commands/sql-reassign-owned.md) — 變更某資料庫角色所擁有的資料庫物件之擁有權

    [REFRESH MATERIALIZED VIEW](sql-commands/sql-refreshmaterializedview.md) — 取代一個具體化檢視表的內容

    [REINDEX](sql-commands/sql-reindex.md) — 重建索引

    [RELEASE SAVEPOINT](sql-commands/sql-release-savepoint.md) — 釋放先前定義的一個儲存點

    [RESET](sql-commands/sql-reset.md) — 將某個執行期參數的值還原為預設值

    [REVOKE](sql-commands/sql-revoke.md) — 移除存取權限

    [ROLLBACK](sql-commands/sql-rollback.md) — 中止目前的交易

    [ROLLBACK PREPARED](sql-commands/sql-rollback-prepared.md) — 取消一個先前已為兩階段提交而準備的交易

    [ROLLBACK TO SAVEPOINT](sql-commands/sql-rollback-to.md) — 回復到某個儲存點

    [SAVEPOINT](sql-commands/sql-savepoint.md) — 在目前交易中定義一個新的儲存點

    [SECURITY LABEL](sql-commands/sql-security-label.md) — 定義或變更套用於某個物件的安全性標籤

    [SELECT](sql-commands/sql-select.md) — 從資料表或檢視表擷取資料列

    [SELECT INTO](sql-commands/sql-selectinto.md) — 從查詢結果定義一個新資料表

    [SET](sql-commands/sql-set.md) — 變更一個執行期參數

    [SET CONSTRAINTS](sql-commands/sql-set-constraints.md) — 設定目前交易中限制條件的檢查時機

    [SET ROLE](sql-commands/sql-set-role.md) — 設定目前工作階段的目前使用者識別碼

    [SET SESSION AUTHORIZATION](sql-commands/sql-set-session-authorization.md) — 設定目前工作階段的工作階段使用者識別碼與目前使用者識別碼

    [SET TRANSACTION](sql-commands/sql-set-transaction.md) — 設定目前交易的特性

    [SHOW](sql-commands/sql-show.md) — 顯示執行期參數的值

    [START TRANSACTION](sql-commands/sql-start-transaction.md) — 開始一個交易區塊

    [TRUNCATE](sql-commands/sql-truncate.md) — 清空一個資料表或一組資料表

    [UNLISTEN](sql-commands/sql-unlisten.md) — 停止接聽某個通知頻道

    [UPDATE](sql-commands/sql-update.md) — 更新資料表的資料列

    [VACUUM](sql-commands/sql-vacuum.md) — 資料庫的垃圾回收，並可選擇進行分析

    [VALUES](sql-commands/sql-values.md) — 計算一組資料列

[II. PostgreSQL 用戶端應用程式](reference-client/README.md)
:   [clusterdb](reference-client/app-clusterdb.md) — 將 PostgreSQL 資料庫叢集化

    [createdb](reference-client/app-createdb.md) — 建立新的 PostgreSQL 資料庫

    [createuser](reference-client/app-createuser.md) — 定義新的 PostgreSQL 使用者帳號

    [dropdb](reference-client/app-dropdb.md) — 移除 PostgreSQL 資料庫

    [dropuser](reference-client/app-dropuser.md) — 移除 PostgreSQL 使用者帳號

    [ecpg](reference-client/app-ecpg.md) — 嵌入式 SQL C 前置處理器

    [pg_amcheck](reference-client/app-pgamcheck.md) — 檢查一個或多個 PostgreSQL 資料庫是否有損毀

    [pg_basebackup](reference-client/app-pgbasebackup.md) — 對 PostgreSQL 叢集進行基礎備份

    [pgbench](reference-client/pgbench.md) — 在 PostgreSQL 上執行效能基準測試

    [pg_combinebackup](reference-client/app-pgcombinebackup.md) — 從增量備份及其相依的備份重建完整備份

    [pg_config](reference-client/app-pgconfig.md) — 取得已安裝之 PostgreSQL 版本的相關資訊

    [pg_dump](reference-client/app-pgdump.md) — 將 PostgreSQL 資料庫匯出為 SQL 腳本或其他格式

    [pg_dumpall](reference-client/app-pg-dumpall.md) — 將 PostgreSQL 資料庫叢集擷取到腳本檔中

    [pg_isready](reference-client/app-pg-isready.md) — 檢查 PostgreSQL 伺服器的連線狀態

    [pg_receivewal](reference-client/app-pgreceivewal.md) — 從 PostgreSQL 伺服器串流接收預寫式日誌

    [pg_recvlogical](reference-client/app-pgrecvlogical.md) — 控制 PostgreSQL 邏輯解碼串流

    [pg_restore](reference-client/app-pgrestore.md) — 從 pg_dump 建立的封存檔還原 PostgreSQL 資料庫

    [pg_verifybackup](reference-client/app-pgverifybackup.md) — 驗證 PostgreSQL 叢集之基礎備份的完整性

    [psql](reference-client/app-psql.md) — PostgreSQL 互動式終端機

    [reindexdb](reference-client/app-reindexdb.md) — 重建 PostgreSQL 資料庫的索引

    [vacuumdb](reference-client/app-vacuumdb.md) — 對 PostgreSQL 資料庫進行垃圾回收與分析

[III. PostgreSQL 伺服器應用程式](reference-server/README.md)
:   [initdb](reference-server/app-initdb.md) — 建立新的 PostgreSQL 資料庫叢集

    [pg_archivecleanup](reference-server/pgarchivecleanup.md) — 清理 PostgreSQL WAL 歸檔檔案

    [pg_checksums](reference-server/app-pgchecksums.md) — 在 PostgreSQL 資料庫叢集中啟用、停用或檢查資料校驗和

    [pg_controldata](reference-server/app-pgcontroldata.md) — 顯示 PostgreSQL 資料庫叢集的控制資訊

    [pg_createsubscriber](reference-server/app-pgcreatesubscriber.md) — 將實體複本轉換為新的邏輯複本

    [pg_ctl](reference-server/app-pg-ctl.md) — 初始化、啟動、停止或控制 PostgreSQL 伺服器

    [pg_resetwal](reference-server/app-pgresetwal.md) — 重設 PostgreSQL 資料庫叢集的預寫式日誌及其他控制資訊

    [pg_rewind](reference-server/app-pgrewind.md) — 將 PostgreSQL 資料目錄與另一個從它分岔出去的資料目錄同步

    [pg_test_fsync](reference-server/pgtestfsync.md) — 判定 PostgreSQL 最快的 `wal_sync_method`

    [pg_test_timing](reference-server/pgtesttiming.md) — 測量計時的額外負擔

    [pg_upgrade](reference-server/pgupgrade.md) — 升級 PostgreSQL 伺服器實例

    [pg_waldump](reference-server/pgwaldump.md) — 以人類可讀的形式顯示 PostgreSQL 資料庫叢集的預寫日誌

    [pg_walsummary](reference-server/app-pgwalsummary.md) — 印出 WAL 摘要檔案的內容

    [postgres](reference-server/app-postgres.md) — PostgreSQL 資料庫伺服器

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/reference.html)（原文版本：18.6；核對日期：2026-10-09）
