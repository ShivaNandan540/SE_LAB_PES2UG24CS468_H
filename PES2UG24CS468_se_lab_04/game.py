import math
import random
import pygame

WIDTH, HEIGHT = 600, 700
PLAYER_Y, PLAYER_SPEED, SHIP_GAP = HEIGHT - 50, 300, 30
ENTRY_TIME = 2.0

# ============================================================
# TASK 2: Wave-based enemy colours
# ============================================================
CURRENT_WAVE = 1

# ============================================================
# TASK 3: Wave-start banner
# ============================================================
WAVE_BANNER_TIME = 1.0
wave_banner = ""
wave_banner_timer = 0.0


# ============================================================
# TASK 1: Correct cubic Bézier curve
# Standard formula:
# B(t) = (1-t)^3 P0 + 3(1-t)^2 t P1
#      + 3(1-t)t^2 P2 + t^3 P3
# ============================================================
def bezier(p0, p1, p2, p3, t):
    u = 1 - t

    x = (
        u ** 3 * p0[0]
        + 3 * u ** 2 * t * p1[0]
        + 3 * u * t ** 2 * p2[0]
        + t ** 3 * p3[0]
    )

    y = (
        u ** 3 * p0[1]
        + 3 * u ** 2 * t * p1[1]
        + 3 * u * t ** 2 * p2[1]
        + t ** 3 * p3[1]
    )

    return pygame.Vector2(x, y)


# ============================================================
# TASK 2: Recolour enemies according to wave number
# Called once per visible enemy per frame from draw().
# ============================================================
def enemy_tint(kind):
    if CURRENT_WAVE == 1:
        return None

    if CURRENT_WAVE % 3 == 2:
        colors = {
            "boss": (180, 80, 220),
            "red": (255, 100, 100),
            "blue": (100, 200, 255),
        }
    elif CURRENT_WAVE % 3 == 0:
        colors = {
            "boss": (255, 170, 60),
            "red": (255, 130, 50),
            "blue": (80, 220, 180),
        }
    else:
        colors = {
            "boss": (240, 220, 70),
            "red": (220, 70, 180),
            "blue": (120, 100, 255),
        }

    return colors[kind]


# ============================================================
# TASK 3: Called at the start of every wave.
# Shows a WAVE X banner for one second.
# ============================================================
def on_wave_start(wave):
    global CURRENT_WAVE, wave_banner, wave_banner_timer

    CURRENT_WAVE = wave
    wave_banner = f"WAVE {wave}"
    wave_banner_timer = WAVE_BANNER_TIME


# ============================================================
# TASK 4: Grant 1 shield charge every 3 waves.
# Return 0 to disable the shield on other waves.
# ============================================================
def shield_charges(wave):
    if wave % 3 == 0:
        return 1
    return 0


ENEMY_COLORS = {
    "boss": (90, 220, 90),
    "red": (230, 70, 70),
    "blue": (80, 140, 240),
}


# ============================================================
# ORIGINAL GAME: Enemy
# ============================================================
class Enemy:
    def __init__(self, kind, home, index, from_left):
        self.kind = kind
        self.home = pygame.Vector2(home)

        self.hp = 2 if kind == "boss" else 1

        self.state = "entry"
        self.t = 0.0
        self.delay = index * 0.12

        self.pos = pygame.Vector2(
            -40 if from_left else WIDTH + 40,
            120
        )

        side = 1 if from_left else -1

        self.path = (
            (self.pos.x, 120),
            (self.pos.x + side * 250, 420),
            (WIDTH / 2 - side * 200, 60),
            (home[0], home[1]),
        )

        self.duration = ENTRY_TIME

    def start_dive(self, player_x):
        side = random.choice([-1, 1])

        end = (
            random.randint(60, WIDTH - 60),
            HEIGHT + 40,
        )

        self.path = (
            tuple(self.pos),
            (
                self.pos.x + side * 160,
                self.pos.y + 160,
            ),
            (player_x, HEIGHT - 200),
            end,
        )

        self.state = "dive"
        self.t = 0.0
        self.duration = 2.6

    def start_return(self):
        top = (self.home.x, -30)

        self.path = (
            top,
            (top[0] + 80, 120),
            (self.home.x - 80, 200),
            tuple(self.home),
        )

        self.state = "entry"
        self.t = 0.0
        self.duration = 1.5
        self.pos = pygame.Vector2(top)

    def update(self, dt, sway, player_x, shots):
        if self.delay > 0:
            self.delay -= dt
            return

        if self.state == "formation":
            self.pos = self.home + pygame.Vector2(sway, 0)
            return

        self.t += dt / self.duration

        if (
            self.state == "dive"
            and random.random() < dt * 0.8
            and self.pos.y < HEIGHT - 250
        ):
            shots.append(pygame.Vector2(self.pos))

        if self.t >= 1:
            if self.state == "dive":
                self.start_return()
            else:
                self.state = "formation"

            return

        self.pos = bezier(*self.path, self.t)


# ============================================================
# ORIGINAL GAME: Spawn a wave
# on_wave_start() is called after the enemy list is built.
# ============================================================
def spawn_wave(wave):
    enemies = []
    index = 0

    layout = [
        ("boss", 4, 90),
        ("red", 8, 130),
        ("red", 8, 170),
        ("blue", 8, 210),
    ]

    for kind, count, y in layout:
        for i in range(count):
            x = WIDTH / 2 + (i - (count - 1) / 2) * 52

            enemies.append(
                Enemy(
                    kind,
                    (x, y),
                    index,
                    index % 2 == 0,
                )
            )

            index += 1

    on_wave_start(wave)

    return enemies


# ============================================================
# ORIGINAL GAME: Game
# ============================================================
class Game:
    def __init__(self):
        self.stars = [
            [
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.uniform(30, 120),
            ]
            for _ in range(70)
        ]

        self.reset()

    def reset(self):
        self.x = WIDTH / 2
        self.ships = 1
        self.lives = 3

        self.score = 0
        self.wave = 1
        self.time = 0.0

        self.bullets = []
        self.shots = []

        self.cooldown = 0.0
        self.invulnerable = 0.0
        self.dive_timer = 3.0

        self.enemies = spawn_wave(self.wave)

        # TASK 4: Shield is determined by the current wave.
        self.shield = shield_charges(self.wave) or 0

        self.state = "play"

    def ship_xs(self):
        return [
            self.x + i * SHIP_GAP
            for i in range(self.ships)
        ]

    def fire(self):
        if (
            self.cooldown <= 0
            and len(self.bullets) < 4 * self.ships
        ):
            for sx in self.ship_xs():
                self.bullets.append(
                    pygame.Vector2(
                        sx,
                        PLAYER_Y - 16
                    )
                )

            self.cooldown = 0.25

    def hit_player(self):
        if self.invulnerable > 0:
            return

        # Existing shield consumption logic.
        if self.shield > 0:
            self.shield -= 1
            self.invulnerable = 1.0
            return

        if self.ships > 1:
            self.ships -= 1
        else:
            self.lives -= 1

            if self.lives <= 0:
                self.state = "lose"

        self.invulnerable = 2.0

    def kill(self, enemy):
        self.enemies.remove(enemy)

        self.score += (
            100 if enemy.state == "dive"
            else 50
        )

        if (
            enemy.kind == "boss"
            and enemy.state == "dive"
        ):
            self.ships = 2

    def update(self, dt, keys):
        global wave_banner_timer

        if self.state != "play":
            return

        self.time += dt
        self.cooldown -= dt

        self.invulnerable = max(
            0.0,
            self.invulnerable - dt
        )

        # TASK 3: Count down the wave banner.
        wave_banner_timer = max(
            0.0,
            wave_banner_timer - dt
        )

        span = SHIP_GAP * (self.ships - 1)

        move = (
            keys[pygame.K_RIGHT]
            - keys[pygame.K_LEFT]
        )

        self.x = max(
            20,
            min(
                WIDTH - 20 - span,
                self.x + move * PLAYER_SPEED * dt,
            ),
        )

        if keys[pygame.K_SPACE]:
            self.fire()

        # Move stars.
        for star in self.stars:
            star[1] = (
                star[1] + star[2] * dt
            ) % HEIGHT

        # Enemy movement.
        sway = math.sin(
            self.time * 1.3
        ) * 24

        for enemy in self.enemies:
            enemy.update(
                dt,
                sway,
                self.x,
                self.shots,
            )

        # Enemy diving.
        self.dive_timer -= dt

        ready = [
            e
            for e in self.enemies
            if e.state == "formation"
        ]

        if self.dive_timer <= 0 and ready:
            random.choice(ready).start_dive(self.x)

            self.dive_timer = max(
                0.8,
                3.0 - self.wave * 0.3,
            )

        self.update_projectiles(dt)

        # Start the next wave.
        if not self.enemies:
            self.wave += 1

            self.enemies = spawn_wave(
                self.wave
            )

            # TASK 4: Grant shield according to new wave.
            self.shield = (
                shield_charges(self.wave) or 0
            )

    def update_projectiles(self, dt):
        # Player bullets.
        for bullet in self.bullets[:]:
            bullet.y -= 520 * dt

            for enemy in self.enemies:
                if (
                    enemy.delay <= 0
                    and enemy.pos.distance_to(bullet) < 18
                ):
                    enemy.hp -= 1

                    if enemy.hp <= 0:
                        self.kill(enemy)

                    self.bullets.remove(bullet)
                    break

        self.bullets = [
            b
            for b in self.bullets
            if b.y > -10
        ]

        # Enemy shots.
        for shot in self.shots:
            shot.y += 260 * dt

        self.shots = [
            s
            for s in self.shots
            if s.y < HEIGHT
        ]

        # Player collision.
        for sx in self.ship_xs():
            target = pygame.Vector2(
                sx,
                PLAYER_Y
            )

            if any(
                s.distance_to(target) < 14
                for s in self.shots
            ):
                self.shots = [
                    s
                    for s in self.shots
                    if s.distance_to(target) >= 14
                ]

                self.hit_player()

            for enemy in self.enemies:
                if (
                    enemy.state == "dive"
                    and enemy.pos.distance_to(target) < 22
                ):
                    self.kill(enemy)
                    self.hit_player()
                    break

    def draw(self, screen, font):
        global wave_banner_timer

        screen.fill((5, 5, 20))

        # Stars.
        for x, y, speed in self.stars:
            shade = int(80 + speed)

            pygame.draw.circle(
                screen,
                (shade, shade, shade),
                (int(x), int(y)),
                1,
            )

        # Enemies.
        for enemy in self.enemies:
            if enemy.delay > 0:
                continue

            # TASK 2: Apply wave-based enemy colour.
            color = (
                enemy_tint(enemy.kind)
                or ENEMY_COLORS[enemy.kind]
            )

            if (
                enemy.kind == "boss"
                and enemy.hp == 1
            ):
                color = (170, 90, 220)

            x, y = enemy.pos

            pygame.draw.polygon(
                screen,
                color,
                [
                    (x - 14, y - 8),
                    (x + 14, y - 8),
                    (x + 8, y + 10),
                    (x - 8, y + 10),
                ],
            )

            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (int(x - 5), int(y - 2)),
                2,
            )

            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (int(x + 5), int(y - 2)),
                2,
            )

        # Player bullets.
        for bullet in self.bullets:
            pygame.draw.rect(
                screen,
                (255, 255, 120),
                (
                    bullet.x - 2,
                    bullet.y - 8,
                    4,
                    14,
                ),
            )

        # Enemy shots.
        for shot in self.shots:
            pygame.draw.circle(
                screen,
                (255, 120, 60),
                (int(shot.x), int(shot.y)),
                4,
            )

        # Player ship.
        if (
            self.invulnerable <= 0
            or int(self.invulnerable * 10) % 2 == 0
        ):
            for sx in self.ship_xs():
                pygame.draw.polygon(
                    screen,
                    (230, 230, 240),
                    [
                        (sx, PLAYER_Y - 18),
                        (sx + 14, PLAYER_Y + 12),
                        (sx - 14, PLAYER_Y + 12),
                    ],
                )

                pygame.draw.polygon(
                    screen,
                    (220, 60, 60),
                    [
                        (sx - 14, PLAYER_Y + 12),
                        (sx - 6, PLAYER_Y - 2),
                        (sx - 4, PLAYER_Y + 12),
                    ],
                )

        # HUD.
        hud = font.render(
            f"Score {self.score}  "
            f"Lives {self.lives}  "
            f"Wave {self.wave}  "
            f"R = reset",
            True,
            (240, 240, 240),
        )

        screen.blit(hud, (10, 8))

        # TASK 3: Draw the wave banner for one second.
        if wave_banner_timer > 0:
            banner_font = pygame.font.Font(
                None,
                64,
            )

            banner = banner_font.render(
                wave_banner,
                True,
                (255, 255, 120),
            )

            screen.blit(
                banner,
                banner.get_rect(
                    center=(
                        WIDTH // 2,
                        HEIGHT // 2 - 80,
                    )
                ),
            )

        # Game over.
        if self.state == "lose":
            label = font.render(
                "GAME OVER - Press R",
                True,
                (255, 255, 120),
            )

            screen.blit(
                label,
                label.get_rect(
                    center=(
                        WIDTH // 2,
                        HEIGHT // 2,
                    )
                ),
            )


def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    pygame.display.set_caption("Galaga")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 26)

    game = Game()
    running = True

    while running:
        dt = min(
            clock.tick(60) / 1000,
            0.05,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
            ):
                game.reset()

        game.update(
            dt,
            pygame.key.get_pressed(),
        )

        game.draw(
            screen,
            font,
        )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
