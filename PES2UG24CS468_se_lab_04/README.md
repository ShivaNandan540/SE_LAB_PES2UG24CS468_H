# Galaga Repair Lab

This project is a single-file Galaga-lite clone using **Pygame**. It introduces students to Bézier-curve motion, wave-based enemy spawning, and projectile collision using a small, readable object-oriented codebase.

---

## What's Provided

A working Galaga-lite game with:

- A player ship (or two, after certain kills) that moves left/right and fires
- Enemies that fly in on curved entry paths, settle into a swaying formation, then dive at the player and fire back
- Wave-based spawning that gets harder as waves progress
- Lives, scoring, and collision handling for bullets, enemy shots, and diving enemies

It has **one deliberate bug** and **three optional features** left as empty functions. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python game.py
```

**Controls:** Left/Right to move, Space to fire, `R` to reset.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the entry/dive path bug

> Enemy entry and dive paths are drawn as cubic Bézier curves, which should pass exactly through their start point at `t=0` and their end point at `t=1`, while bulging smoothly through two control points in between. In the current build, the curves noticeably bulge or overshoot mid-flight in a way that looks wrong, even though the start and end points are still correct — which is what makes this one tricky to spot just by checking the endpoints. Compare the `bezier()` function's four weighted terms against the standard cubic Bézier formula, and check the exponents on `u` and `t` in each of the two middle terms.

### Task 2: Implement `enemy_tint(kind)`

> Called once per visible enemy per frame in `draw`, as `color = enemy_tint(enemy.kind) or ENEMY_COLORS[enemy.kind]`. `kind` is `"boss"`, `"red"`, or `"blue"`. Return an `(r, g, b)` override, or `None` to keep the default from `ENEMY_COLORS`. Idea: recolor enemies by wave number so later waves look visually distinct.

### Task 3: Implement `on_wave_start(wave)`

> Called once from `spawn_wave(wave)`, right after that wave's enemy list is built — both at game start and every time a wave is cleared. It receives the 1-indexed wave number. Its return value is ignored. Idea: show a "WAVE 3" banner for a second, or ramp up the dive rate.

### Task 4: Implement `shield_charges(wave)`

> Called at game start and at the start of every new wave, as `self.shield = shield_charges(self.wave) or 0`. It receives the current wave number and should return an integer number of hits the player can absorb this wave before losing a ship, or `None`/`0` to disable the shield. The logic that consumes a shield charge in `hit_player()` is already implemented — you only need to decide how many charges to grant. Idea: grant 1 shield charge every 3 waves.

---

## Expected Behavior

- Enemies enter along a smooth curved path and settle into a gently swaying formation
- Enemies periodically peel off to dive at the player and fire back while diving
- Each bullet destroys at most one enemy; the boss enemy takes two hits to destroy
- Losing all ships costs a life; the player gains a second ship after certain kills
- The game ends when lives reach zero; otherwise waves continue indefinitely and get harder over time

---

## Folder Structure

```
galaga/
├── game.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
