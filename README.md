# 🌾 Kaggriculture Agents

[![Kaggle Medal](https://img.shields.io/badge/Kaggle-Silver_Medal_(213th_%2F_10148)-silver.svg)](https://www.kaggle.com/competitions/kaggriculture)
[![Search](https://img.shields.io/badge/Search-LNS_%2B_DP-orange)]()
[![Networks](https://img.shields.io/badge/Networks-BC_%2B_PPO-purple)]()

> Our agents for the Kaggle simulation competition **[Kaggriculture](https://www.kaggle.com/competitions/kaggriculture)**, and a summary of how each version works.
> The methods combine ideas from the competition's public code and discussions; see the [competition page](https://www.kaggle.com/competitions/kaggriculture) (Code / Discussion / Writeups) for the original solutions.

<p align="center">
  <img src="./Qize%20He%20-%20Kaggriculture.png" alt="Kaggriculture Silver Medal Certificate - Qize He" width="800"/>
  <!-- teammates: add your certificate here, e.g. <img src="./Your%20Name%20-%20Kaggriculture.png" alt="Kaggriculture Silver Medal Certificate - Your Name" width="800"/> -->
</p>

---

## 📦 Versions

| Folder | How it works | Needs weights |
| :--- | :--- | :--- |
| `v0_original` | **Days 0–9:** an opening schedule fitted on public replays. Each day's animal and crop targets are regression formulas on the shops unlocked so far. **Day 10 onward:** an optimisation planner with per-tile crop DP, column-generation worker routing, a market model that projects the opponent's supply, and an economic simulator for parameter search. | No |
| `v2_hopen10` | **Days 0–9:** the v0 opening. **Day 10 onward:** a heuristic day solver. Every dawn, LNS with simulated annealing plans all workers' routes and the day's production. Future days are projected with a per-tile DP, and the objective is my cash minus the opponent's. | No |
| `v2_hopen12` | Same as `v2_hopen10`, but the solver takes over on day 12. | No |
| `v3_h2e` ⭐ | **Days 0–28:** a HourFormer encoder-decoder network (behaviour cloning, then PPO) plus rules for last-day delivery and wheat trading. **Day 29:** the heuristic day solver plans the final collection and selling. | Yes: `net/player.pt` |
| `v3_h3e` | **Days 0–28:** a Transformer policy (behaviour cloning, then self-play PPO) with post-processing rules (overflow selling, melon replanting, last-day collection). **Day 29:** the heuristic day solver. | Yes: `net/policy.pt` |

Weights are not included. You can train your own, or use the published weights of the top teams, which are linked from the [competition page](https://www.kaggle.com/competitions/kaggriculture). 

`s1/` inside the v2 and v3 folders is the heuristic day solver. Its C++ core (`terminal_search.cpp`) is also shipped prebuilt as `terminal_search.so`, compiled for glibc 2.17.
