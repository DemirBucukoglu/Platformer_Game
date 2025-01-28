import pygame
from weaponclss import Weapon

class Player:
    def __init__(self, x, y, image_path, health=500, ammo=7000):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 70, 70)
        self.image = pygame.transform.scale(self.image, (70, 80))
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.on_ground = False
        self.direction = 1
        
        self.health = health
        self.healthbar = pygame.Rect(self.rect.x, self.rect.y, 100, 200)
        
        self.ammo = ammo
        self.in_boss_arena = False

    def shoot(self, weapons_list):
        if self.ammo > 0:
            new_weapon = Weapon(self.rect.centerx, self.rect.centery, direction=self.direction)
            weapons_list.append(new_weapon)
            self.ammo -= 1

    def move(self, keys):
        speed = 5
        if keys[pygame.K_a]:  # Move left
            self.rect.x -= speed
            self.direction = -1
        if keys[pygame.K_d]:  # Move right
            self.rect.x += speed
            self.direction = 1

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -15
            self.on_ground = False
        self.velocity_y += 1
        self.rect.y += self.velocity_y

    def check_collision(self, platforms, enemies, walls):
        self.on_ground = False

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # Check vertical collision first
                if self.velocity_y >= 0 and self.rect.bottom <= wall.rect.top + self.velocity_y:
                    self.rect.bottom = wall.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                # Then check side collisions
                if self.rect.right > wall.rect.left and self.rect.left < wall.rect.right:
                    # Right side collision
                    if abs(self.rect.right - wall.rect.left) < abs(self.rect.left - wall.rect.right):
                        self.rect.right = wall.rect.left
                    # Left side collision
                    else:
                        self.rect.left = wall.rect.right

        # Check collision with all platforms and walls
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y >= 0 and self.rect.bottom <= platform.rect.top + self.velocity_y:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

        # Check collision with enemies - original version
        # for enemy in enemies:
        #     if self.rect.colliderect(enemy.rect):
        #         if self.velocity_y >= 0 and self.rect.bottom <= enemy.rect.top + abs(self.velocity_y):
        #             # Player lands on top of the enemy
        #             self.rect.bottom = enemy.rect.top
        #             self.velocity_y = 0
        #             self.on_ground = True
              

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            return True
        return False

    def check_boss_arena(self, x_min=2600, x_max=3000):
        # Once in the boss arena, player can't leave
        if not self.in_boss_arena:
            if x_min <= self.rect.x <= x_max:
                self.in_boss_arena = True
        return self.in_boss_arena