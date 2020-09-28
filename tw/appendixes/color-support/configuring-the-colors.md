# N.2. Configuring the Colors

The actual colors to be used are configured using the environment variable `PG_COLORS` \(note plural\). The value is a colon-separated list of _`key`_=_`value`_ pairs. The keys specify what the color is to be used for. The values are SGR \(Select Graphic Rendition\) specifications, which are interpreted by the terminal.

The following keys are currently in use:`error`

used to highlight the text “error” in error messages`warning`

used to highlight the text “warning” in warning messages`locus`

used to highlight location information \(e.g., program name and file name\) in messages

The default value is `error=01;31:warning=01;35:locus=01` \(`01;31` = bold red, `01;35` = bold magenta, `01` = bold default color\).

{% hint style="info" %}
此色彩規範格式也廣為其他軟體套件所使用，例如 GCC，GNU coreutils 和 GNU grep。
{% endhint %}

