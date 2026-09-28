<a id="AUTH-IDENT"></a>

## 20.8. Ident 認證 [#](#AUTH-IDENT)

<a id="id-1.6.7.15.2"></a>

ident 認證方法的運作方式，是從 ident 伺服器取得用戶端的
作業系統使用者名稱，並將其作為允許使用的資料庫使用者名稱（可搭配選用的使用者名稱對應）。
此方法僅支援 TCP/IP 連線。

### 注意

當本機（非 TCP/IP）連線指定使用 ident 時，
將改用 peer 認證（見[第 20.9 節](auth-peer.md)）。

`ident` 支援下列組態選項：

`map`
:   允許在系統使用者名稱與資料庫使用者名稱之間進行對應。詳見
    [第 20.2 節](auth-username-maps.md)。

「識別通訊協定」的說明詳見
[RFC 1413](https://datatracker.ietf.org/doc/html/rfc1413)。
幾乎每一種類 Unix
作業系統都內建了在 TCP
埠 113 上監聽的 ident 伺服器。ident 伺服器的基本功能
是回答諸如「從你的埠 *`X`*
發出並連到我的埠 *`Y`* 的連線是由哪個使用者發起的？」
這類問題。
由於 PostgreSQL 在建立實體連線時同時知道 *`X`* 與
*`Y`*，它可以向發起連線的用戶端主機上的 ident 伺服器查詢，
理論上便能判定任何指定連線所對應的作業系統使用者。

這種做法的缺點在於它依賴用戶端的完整性：如果用戶端機器不受信任或已遭入侵，
攻擊者就可以在埠 113 上執行幾乎任何程式，
並回傳他們所選擇的任意使用者名稱。因此，這種認證方法
僅適用於封閉式網路，其中每台用戶端機器都受到嚴格控管，
且資料庫管理者與系統管理者之間保持密切聯繫。換句話說，你必須
信任執行 ident 伺服器的那台機器。
請留意這項警告：

<table border="0" class="blockquote" style="width: 100%; cellspacing: 0; cellpadding: 0;" summary="Block quote"><tr><td valign="top" width="10%"> </td><td valign="top" width="80%"><p>
      識別通訊協定並非用於做為授權或存取控制通訊協定。
     </p></td><td valign="top" width="10%"> </td></tr><tr><td valign="top" width="10%"> </td><td align="right" colspan="2" valign="top">--<span class="attribution">RFC 1413</span></td></tr></table>

部分 ident 伺服器有一個非標準選項，會使回傳的
使用者名稱經過加密，其加密金鑰僅有原始
機器的管理者知悉。在搭配 PostgreSQL 使用 ident 伺服器時，*絕對不可*
使用此選項，
因為 PostgreSQL 沒有任何方法可以解密
回傳的字串以判定實際的使用者名稱。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-ident.html)（原文版本：18.6；核對日期：2026-09-28）
