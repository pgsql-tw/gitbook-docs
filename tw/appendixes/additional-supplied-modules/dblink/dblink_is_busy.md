# dblink\_is\_busy

dblink\_is\_busy — checks if connection is busy with an async query

### Synopsis

```text
dblink_is_busy(text connname) returns int
```

### Description

`dblink_is_busy` tests whether an async query is in progress.

### Arguments

_`connname`_

Name of the connection to check.

### Return Value

Returns 1 if connection is busy, 0 if it is not busy. If this function returns 0, it is guaranteed that `dblink_get_result` will not block.

### Examples

```text
SELECT dblink_is_busy('dtest1');
```

