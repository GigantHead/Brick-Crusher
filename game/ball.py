import pygame
import settings
import math
from .brick import Brick

class Ball:
    def __init__(self):
        self.image = pygame.Surface((20,20))
        self.image.fill(settings.WHITE)
        self.rect = self.image.get_rect(center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 120)) # initialize the ball right above the paddle
        self.speed = 5
        self.angle = 0
        self.velocity_x = self.speed * math.sin(self.angle)
        self.velocity_y = -self.speed * math.cos(self.angle)
        self.history = []

    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y 
        
    def check_collision_with_paddle(self, paddle):
        if self.rect.colliderect(paddle.rect):
            # code for handling change in x velocity
            hit_offset = self.rect.centerx - paddle.rect.centerx
            offset_proportion = hit_offset / (paddle.rect.width / 2) # normalized offset [-1, 1]
            new_angle = offset_proportion * math.radians(45)  # max angle change of 45 degrees
            
            # Update the velocities based on the new angle
            self.velocity_x = self.speed * math.sin(new_angle)
            self.velocity_y = -self.speed * math.cos(new_angle)  # Reverse the y-direction    
    
    def check_collision_with_bricks(self, bricks):
        collided_bricks = pygame.sprite.spritecollide(self, bricks, False)
        if not collided_bricks:
            return []

        # Find the nearest brick
        nearest_brick = min(collided_bricks, key=lambda b: pygame.math.Vector2(b.rect.center).distance_to(self.rect.center))
        
        # Calculate collision point
        collision_point = self.get_collision_point(nearest_brick)
        
        # Determine collision side
        if collision_point.x <= nearest_brick.rect.left or collision_point.x >= nearest_brick.rect.right:
            self.velocity_x *= -1
        if collision_point.y <= nearest_brick.rect.top or collision_point.y >= nearest_brick.rect.bottom:
            self.velocity_y *= -1

        return collided_bricks

    def get_collision_point(self, brick):
        # Calculate the collision point
        center = pygame.math.Vector2(self.rect.center)
        direction = pygame.math.Vector2(self.velocity_x, self.velocity_y).normalize()
        radius = self.rect.width / 2

        # Check each side of the brick
        sides = [
            (pygame.math.Vector2(brick.rect.topleft), pygame.math.Vector2(brick.rect.bottomleft)),
            (pygame.math.Vector2(brick.rect.topleft), pygame.math.Vector2(brick.rect.topright)),
            (pygame.math.Vector2(brick.rect.topright), pygame.math.Vector2(brick.rect.bottomright)),
            (pygame.math.Vector2(brick.rect.bottomleft), pygame.math.Vector2(brick.rect.bottomright))
        ]

        closest_point = None
        min_distance = float('inf')

        for start, end in sides:
            intersection = self.line_intersection(center, center + direction * radius, start, end)
            if intersection:
                distance = center.distance_to(intersection)
                if distance < min_distance:
                    min_distance = distance
                    closest_point = intersection

        return closest_point if closest_point else center

    @staticmethod
    def line_intersection(line1_start, line1_end, line2_start, line2_end):
        x1, y1 = line1_start
        x2, y2 = line1_end
        x3, y3 = line2_start
        x4, y4 = line2_end

        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominator == 0:
            return None  # Lines are parallel

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 0 <= t <= 1 and 0 <= u <= 1:
            return pygame.math.Vector2(x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        return None

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Update history for trail
        self.history.append(self.rect.center)
        if len(self.history) > 10:
            self.history.pop(0)

        # Bounce off side walls
        if self.rect.left <= 0 or self.rect.right >= settings.SCREEN_WIDTH:
            self.velocity_x *= -1
        
        # Bounce off top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= settings.SCREEN_HEIGHT:
            self.velocity_y *= -1

        # Ensure the ball stays within the screen
        self.rect.clamp_ip(pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    def draw(self, screen):
        # Draw trail
        for i, pos in enumerate(self.history):
             alpha = int((i / len(self.history)) * 255)
             trail_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
             pygame.draw.circle(trail_surface, (*settings.WHITE, alpha), (self.rect.width//2, self.rect.height//2), self.rect.width//2)
             screen.blit(trail_surface, (pos[0] - self.rect.width//2, pos[1] - self.rect.height//2))

        screen.blit(self.image, self.rect)
        
    def handle_brick_collision(self, brick):
        # Determine collision side
        if self.rect.right <= brick.rect.left or self.rect.left >= brick.rect.right:
            self.velocity_x *= -1
        else:
            self.velocity_y *= -1
