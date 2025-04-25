# Social Experiments with LLM 🧠🎲

A lightweight playground for **simulating classic game‑theory scenarios with large‑language‑model agents**.  
The engine lets you plug in different agent personas, choose one‑shot or multi‑round setups, and capture the full interaction history to JSON for downstream analysis.

## Features
- Core abstractions: `OneShotGame`, `MultiRoundGame`, `SimultaneousGame`, `SequentialGame`
- Ready‑to‑run games: Prisoner’s Dilemma, Public Goods, Trust Game, Ultimatum Game, First‑Bid Auction
- Simple JSON logging to `games/results/`
- Swap LLMs or add new personas with just a few lines of code

## Requirements
| What | Why |
|------|-----|
| **Python ≥ 3.10** | Runtime |
| **[Ollama](https://ollama.com)** | Local LLM runner |
| **`llama3` model** | Default model used by the agents (`ollama pull llama3`) |

*Any other Ollama‑compatible model can be used—just pass its name when you construct an agent.*

## Quick‑start: run the Prisoner’s Dilemma
```bash

git clone https://github.com/ArmenMelkonian/social-experiements-with-llm.gitt
cd social-experiments-with-llm
pip install -r requirements.txt

# ensure the model is available locally
ollama pull llama3          # or another supported model

# fire up the simulation (3 rounds, 5 personas by default)
python games/game_modules/first_bid_auction.py
```

You’ll see console output like:

```
Round 1 (Pair 1/100): competitive_egoist → 100.0, trusting_collaborator → 50.0, impulsive_reactor → 80.5, rational_strategist → 90.0, passive_observer → 50.0
Round 2 (Pair 1/100): competitive_egoist → 99.9, trusting_collaborator → 90.0, impulsive_reactor → 85.5, rational_strategist → 100.0, passive_observer → 80.5
...
```

A full JSON trace is saved to `games/results/prisoner_dilemma_simulation.json`.

## Repository layout
```
agents/              # agent base classes & persona definitions
data/                
  ├── characters/    # prompt templates for each persona
  └── games/         # prompt templates for each game
games/
  ├── game_modules/  # plug‑and‑play game scripts
  ├── base_game.py
  ├── multi_round_game.py
  ├── one_shot_game.py
  ├── sequential_game.py
  └── simultaneous_game.py
results/             # results of simulations
src/
```

## Extending
1. Create a new game class that **multiple‑inherits** from exactly one duration mixin (`OneShotGame` *or* `MultiRoundGame`) **and** one timing mixin (`SimultaneousGame` *or* `SequentialGame`).

   _Example_  
   ```python
   from games import OneShotGame, SequentialGame

   
   class MyCustomGame(OneShotGame, SequentialGame):
       # implement game‑specific logic here
       ...
   ```
2. Point it at any personas defined in `data/characters`.
3. Run and analyse!
