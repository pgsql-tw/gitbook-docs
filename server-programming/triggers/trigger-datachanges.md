## 37.2. Visibility of Data Changes [#](#TRIGGER-DATACHANGES)

If you execute SQL commands in your trigger function, and these
commands access the table that the trigger is for, then
you need to be aware of the data visibility rules, because they determine
whether these SQL commands will see the data change that the trigger
is fired for. Briefly:

* Statement-level triggers follow simple visibility rules: none of
  the changes made by a statement are visible to statement-level
  `BEFORE` triggers, whereas all
  modifications are visible to statement-level `AFTER`
  triggers.
* The data change (insertion, update, or deletion) causing the
  trigger to fire is naturally *not* visible
  to SQL commands executed in a row-level `BEFORE` trigger,
  because it hasn't happened yet.
* However, SQL commands executed in a row-level `BEFORE`
  trigger *will* see the effects of data
  changes for rows previously processed in the same outer
  command. This requires caution, since the ordering of these
  change events is not in general predictable; an SQL command that
  affects multiple rows can visit the rows in any order.
* Similarly, a row-level `INSTEAD OF` trigger will see the
  effects of data changes made by previous firings of `INSTEAD
  OF` triggers in the same outer command.
* When a row-level `AFTER` trigger is fired, all data
  changes made
  by the outer command are already complete, and are visible to
  the invoked trigger function.

If your trigger function is written in any of the standard procedural
languages, then the above statements apply only if the function is
declared `VOLATILE`. Functions that are declared
`STABLE` or `IMMUTABLE` will not see changes made by
the calling command in any case.

Further information about data visibility rules can be found in
[Section 45.5](../spi/spi-visibility.md). The example in [Section 37.4](trigger-example.md) contains a demonstration of these rules.

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/trigger-datachanges.html)（英文原文，待翻譯）
