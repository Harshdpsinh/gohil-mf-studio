# Gohil MF Studio

**Download the whole pack (one click):**

https://github.com/Harshdpsinh/gohil-mf-studio/archive/refs/heads/main.zip

Or grab files:

- [MF-Ratings-Engine.html](https://github.com/Harshdpsinh/gohil-mf-studio/raw/main/MF-Ratings-Engine.html)
- [MF-TRI-bundle.json](https://github.com/Harshdpsinh/gohil-mf-studio/raw/main/MF-TRI-bundle.json)
- [GET-TRI-DATA.py](https://github.com/Harshdpsinh/gohil-mf-studio/raw/main/GET-TRI-DATA.py)
- [GET-TRI-DATA.bat](https://github.com/Harshdpsinh/gohil-mf-studio/raw/main/GET-TRI-DATA.bat)
- [Gohil-MF-Studio-Takeaway.zip](https://github.com/Harshdpsinh/gohil-mf-studio/raw/main/Gohil-MF-Studio-Takeaway.zip)

---

Gohil MF Studio — use these files on your PC right now
======================================================

1. python3 GET-TRI-DATA.py     (or double-click GET-TRI-DATA.bat)
2. Open MF-Ratings-Engine.html in Chrome
3. Setup → Load bundle → MF-TRI-bundle.json

This bundle already has 12 series (2016–2026), including debt7.
You can skip step 1 until next month.

Composite TRI (when NSE has no public hybrid feed)
-------------------------------------------------
Never use an index-fund NAV as the hurdle (TER inflates alpha).

  r_debt = (1.07)^(1/250) − 1
  r_arb  = (1.058)^(1/250) − 1
  r_tot  = w_eq * r_eq + w_debt * r_debt + w_arb * r_arb

## Figma skill

Official `figma-use` skill is in [skills/figma-use/SKILL.md](skills/figma-use/SKILL.md). The ratings engine HTML is unchanged. See [FIGMA.md](FIGMA.md).
