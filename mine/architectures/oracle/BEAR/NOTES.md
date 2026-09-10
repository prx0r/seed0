# prx0r/BEAR

sha=7fd978fcb70614e2a2c097a205d728cb5fafeed4

## README excerpt

# BEAR — Hyperliquid Relative-Value Trading Engine

## Thesis (Section 76)

The most profitable long-short equity strategies have always been built on a simple insight:
**when you're long the best and short the worst, you can profit from both sides of the market**.
BEAR applies this to crypto perpetuals on Hyperliquid.

Crypto perps are uniquely suited to relative-value trading because:

1. **Funding rates create a structural edge.** Perpetual markets systematically overpay
   shorts during euphoria and overpay longs during panic. By being long quality and
   short garbage, we collect funding from the retail leverage on both sides.

2. **Dispersion is extreme.** A 10x move in a small-cap is common while BTC does 2x.
   This dispersion is harvestable — the cross-section of perp returns has far more
   variance than equity indices.

3. **Lending markets are thin.** Unlike equities where borrow costs are well-known and
   priced in, crypto borrow is fragmented and opaque. Tokens with high retail demand
   (meme coins, leveraged plays) carry hidden borrow costs that create short alpha.

4. **Survivorship bias works in our favor.** Most altcoins trend to zero. Being short
   the ones with poor tokenomics, declining usage, and high emission is a negative-carry
   bet with positive expected value.

BEAR implements a systematic relative-value strategy:

- **Long basket:** Top-tier crypto assets (BTC, ETH, high-quality L1s/DeFi)
- **Short basket:** Worst-tier assets ranked by tokenomi
