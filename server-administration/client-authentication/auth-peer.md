## 20.9. Peer 驗證 [#](#AUTH-PEER)

<a id="id-1.6.7.16.2"></a>

Peer 驗證方法會從核心取得用戶端的作業系統使用者名稱，並將其作為允許使用的資料庫使用者名稱（可選擇套用使用者名稱對應）。此方法僅支援本機連線。

`peer` 支援下列設定選項：

`map`
:   允許系統使用者名稱與資料庫使用者名稱之間的對應。詳見[第 20.2 節](auth-username-maps.md)。

Peer 驗證僅適用於提供 `getpeereid()` 函式、`SO_PEERCRED` socket 參數或類似機制的作業系統。目前包括 Linux、多數 BSD 系統（含 macOS）及 Solaris。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/auth-peer.html)（原文版本：18.6；核對日期：2026-09-07）
