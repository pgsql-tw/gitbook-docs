<a id="PGTESTTIMING"></a><a id="id-1.9.5.12.1"></a>

## pg_test_timing

pg_test_timing — 測量計時的額外負擔

## 語法

<a id="id-1.9.5.12.4.1"></a>

`pg_test_timing` [*`option`*...]

<a id="id-1.9.5.12.5"></a>

## 說明

pg_test_timing 是一個工具，用來測量你系統上計時的額外負擔，並確認系統時間從不倒退。收集計時資料較慢的系統，可能會產生較不準確的 `EXPLAIN ANALYZE` 結果。

<a id="id-1.9.5.12.6"></a>

## 選項

pg_test_timing 接受下列命令列選項：

`-d duration`<br>`--duration=duration`
:   指定測試持續時間，以秒為單位。持續時間越長，準確度會稍微好一些，也越有可能發現系統時鐘倒退的問題。預設的測試持續時間為 3 秒。

`-V`<br>`--version`
:   印出 pg_test_timing 版本後結束。

`-?`<br>`--help`
:   顯示 pg_test_timing 命令列引數的說明後結束。

<a id="id-1.9.5.12.7"></a>

## 用法

<a id="id-1.9.5.12.7.2"></a>

### 解讀結果

良好的結果會顯示大多數（>90%）個別計時呼叫耗時少於一微秒。每次迴圈的平均額外負擔會更低，低於 100 奈秒。下面這個來自使用 TSC 時鐘來源之 Intel i7-860 系統的範例，展現了極佳的效能：

```

Testing timing overhead for 3 seconds.
Per loop time including overhead: 35.96 ns
Histogram of timing durations:
  < us   % of total      count
     1     96.40465   80435604
     2      3.59518    2999652
     4      0.00015        126
     8      0.00002         13
    16      0.00000          2
```

請注意，每次迴圈時間所使用的單位與直方圖不同。迴圈的解析度可以達到數奈秒（ns）以內，而個別計時呼叫的解析度只能到一微秒（us）。

<a id="id-1.9.5.12.7.3"></a>

### 測量執行器的計時額外負擔

當查詢執行器使用 `EXPLAIN ANALYZE` 執行陳述式時，除了顯示摘要之外，個別操作也會被計時。你可以用 psql 程式計算資料列數，來檢查你系統的額外負擔：

```

CREATE TABLE t AS SELECT * FROM generate_series(1,100000);
\timing
SELECT COUNT(*) FROM t;
EXPLAIN ANALYZE SELECT COUNT(*) FROM t;
```

所測量的 i7-860 系統執行計數查詢需要 9.8 ms，而 `EXPLAIN ANALYZE` 版本需要 16.6 ms，兩者各處理略多於 100,000 筆資料列。這 6.8 ms 的差異表示每筆資料列的計時額外負擔為 68 ns，約為 pg_test_timing 估計值的兩倍。即使是這麼相對少量的額外負擔，也讓完整計時的計數陳述式多花了將近 70% 的時間。在更有份量的查詢上，計時額外負擔造成的問題會比較小。

<a id="id-1.9.5.12.7.4"></a>

### 變更時間來源

在某些較新的 Linux 系統上，可以隨時變更用來收集計時資料的時鐘來源。第二個範例顯示，在與上述快速結果相同的系統上，切換到較慢的 acpi_pm 時間來源可能造成的減速：

```

# cat /sys/devices/system/clocksource/clocksource0/available_clocksource
tsc hpet acpi_pm
# echo acpi_pm > /sys/devices/system/clocksource/clocksource0/current_clocksource
# pg_test_timing
Per loop time including overhead: 722.92 ns
Histogram of timing durations:
  < us   % of total      count
     1     27.84870    1155682
     2     72.05956    2990371
     4      0.07810       3241
     8      0.01357        563
    16      0.00007          3
```

在此設定下，上述的 `EXPLAIN ANALYZE` 範例需要 115.9 ms。這相當於 1061 ns 的計時額外負擔，同樣是此工具直接測得之值的一個小倍數。這麼多的計時額外負擔，表示實際查詢本身只佔所計入時間的一小部分，大部分時間反而都耗在額外負擔上。在此設定下，任何涉及許多計時操作的 `EXPLAIN ANALYZE` 總計，都會因為計時額外負擔而顯著膨脹。

FreeBSD 也允許即時變更時間來源，並且會記錄開機時所選計時器的相關資訊：

```

# dmesg | grep "Timecounter"
Timecounter "ACPI-fast" frequency 3579545 Hz quality 900
Timecounter "i8254" frequency 1193182 Hz quality 0
Timecounters tick every 10.000 msec
Timecounter "TSC" frequency 2531787134 Hz quality 800
# sysctl kern.timecounter.hardware=TSC
kern.timecounter.hardware: ACPI-fast -> TSC
```

其他系統可能只允許在開機時設定時間來源。在較舊的 Linux 系統上，"clock" 核心設定是進行這類變更的唯一方式。而且即使在某些較新的系統上，你能看到的唯一時鐘來源選項也只有 "jiffies"。Jiffies 是較舊的 Linux 軟體時鐘實作，當它由足夠快的計時硬體支援時，可以有良好的解析度，如本範例所示：

```

$ cat /sys/devices/system/clocksource/clocksource0/available_clocksource
jiffies
$ dmesg | grep time.c
time.c: Using 3.579545 MHz WALL PM GTOD PIT/TSC timer.
time.c: Detected 2400.153 MHz processor.
$ pg_test_timing
Testing timing overhead for 3 seconds.
Per timing duration including loop overhead: 97.75 ns
Histogram of timing durations:
  < us   % of total      count
     1     90.23734   27694571
     2      9.75277    2993204
     4      0.00981       3010
     8      0.00007         22
    16      0.00000          1
    32      0.00000          1
```

<a id="id-1.9.5.12.7.5"></a>

### 時鐘硬體與計時準確度

在電腦上收集準確的計時資訊，通常是透過準確度各不相同的硬體時鐘來完成。在某些硬體上，作業系統可以幾乎直接將系統時鐘時間傳給程式。系統時鐘也可以衍生自單純提供計時中斷（以某個已知時間間隔發出的週期性滴答（tick））的晶片。無論哪一種情況，作業系統核心都會提供一個隱藏這些細節的時鐘來源。但該時鐘來源的準確度，以及它能多快傳回結果，會因底層硬體而異。

不準確的計時可能導致系統不穩定。請非常謹慎地測試對時鐘來源的任何變更。作業系統的預設值有時會為了可靠性而犧牲最佳準確度。而如果你使用的是虛擬機器，請研究與它相容的建議時間來源。虛擬硬體在模擬計時器時會面臨額外的困難，而且廠商通常會針對各個作業系統建議不同的設定。

時間戳記計數器（Time Stamp Counter，TSC）時鐘來源是目前世代 CPU 上可用的最準確時鐘來源。當作業系統支援它且 TSC 時鐘可靠時，它是追蹤系統時間的首選方式。TSC 有好幾種情況可能無法提供準確的計時來源，使其不可靠。較舊的系統可能有會隨 CPU 溫度變化的 TSC 時鐘，使其無法用於計時。在某些較舊的多核心 CPU 上嘗試使用 TSC，可能會在多個核心之間回報不一致的時間。這可能導致時間倒退，而這正是本程式會檢查的問題。而且即使是最新的系統，在非常積極的省電設定下，也可能無法提供準確的 TSC 計時。

較新的作業系統可能會檢查已知的 TSC 問題，並在發現問題時切換到較慢但較穩定的時鐘來源。如果你的系統支援 TSC 時間但預設並未使用它，那麼它可能是基於充分的理由而被停用。而且某些作業系統可能無法正確偵測所有可能的問題，或者即使在已知 TSC 不準確的情況下，仍會允許使用它。

高精度事件計時器（High Precision Event Timer，HPET）是在可用且 TSC 不準確的系統上的首選計時器。計時器晶片本身可程式化，最高可達 100 奈秒的解析度，但你的系統時鐘可能看不到這麼高的準確度。

進階組態與電源介面（Advanced Configuration and Power Interface，ACPI）提供一個電源管理（Power Management，PM）計時器，Linux 稱之為 acpi_pm。衍生自 acpi_pm 的時鐘最多只能提供 300 奈秒的解析度。

較舊 PC 硬體上使用的計時器包括 8254 可程式化間隔計時器（Programmable Interval Timer，PIT）、即時時鐘（real-time clock，RTC）、進階可程式化中斷控制器（Advanced Programmable Interrupt Controller，APIC）計時器，以及 Cyclone 計時器。這些計時器的目標是毫秒等級的解析度。

<a id="id-1.9.5.12.8"></a>

## 另請參閱

[EXPLAIN](../sql-commands/sql-explain.md)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgtesttiming.html)（原文版本：18.6；核對日期：2026-10-05）
