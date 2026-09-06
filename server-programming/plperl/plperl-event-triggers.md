## 43.7. PL/Perl 事件觸發器 [#](#PLPERL-EVENT-TRIGGERS)

PL/Perl 可用來撰寫事件觸發器函式。在事件觸發器函式中，雜湊參照 `$_TD` 包含目前觸發事件的資訊。`$_TD` 是全域變數，但每次呼叫觸發器時都會取得獨立的區域值。`$_TD` 雜湊參照的欄位如下：

`$_TD->{event}`
:   引發此觸發器的事件名稱。

`$_TD->{tag}`
:   引發此觸發器的命令標籤。

觸發器函式的回傳值會被忽略。

以下事件觸發器函式範例示範了上述部分功能：

```

CREATE OR REPLACE FUNCTION perlsnitch() RETURNS event_trigger AS $$
  elog(NOTICE, "perlsnitch: " . $_TD->{event} . " " . $_TD->{tag} . " ");
$$ LANGUAGE plperl;

CREATE EVENT TRIGGER perl_a_snitch
    ON ddl_command_start
    EXECUTE FUNCTION perlsnitch();
```

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/plperl-event-triggers.html)（原文版本：18.6；核對日期：2026-09-07）
