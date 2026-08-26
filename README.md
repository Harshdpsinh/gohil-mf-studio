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

Key      Name                         Equity  Debt   Arb    Categories
nifty100 NIFTY 100 TRI                live NSE
n500     NIFTY 500 TRI                live NSE
mid150   Midcap 150                   live NSE
small250 Smallcap 250                 live NSE
lm250    LargeMidcap 250              live NSE
mc502525 Multicap 50:25:25            live NSE
hyb6535  Hybrid Composite 65:35       65%     35%    0      Aggressive Hybrid, Multi Asset
hyb5050  Hybrid Composite 50:50       50%     50%    0      Balanced Advantage
hyb1585  Hybrid Composite 15:85       15%     85%    0      Conservative Hybrid
eqsav    Equity Savings TRI           35%     35%    30%    Equity Savings
arb      NIFTY 50 Arbitrage TRI       0       0      100%   Arbitrage
debt7    AAA/G-Sec 7% TR sleeve       0       100%   0      Reference debt curve (peer-only ranking)

Pure debt funds (Liquid, Ultra Short, Short Duration, Corporate Bond, Gilt)
score peer-only. debt7 is the 7% sleeve inside hybrids, not a rank hurdle
(a smooth 7% series would zero every fund on volatility).
