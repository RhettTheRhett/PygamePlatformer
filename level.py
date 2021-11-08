import pygame
from tiles import Tile
from settings import *
from player import Player
class Level:
    def __init__(self,levelData,surface):

        ##level setup
        self.displaySurface = surface
        self.setupLevel(levelData)
        self.worldShift = 0

    def setupLevel(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for rowIndex, row in enumerate(layout):
            for colIndex, cell in enumerate(row):
                x = tileSize * colIndex
                y = tileSize * rowIndex
                if (cell == 'X'):
                    tile = Tile((x, y), tileSize)
                    self.tiles.add(tile)
                if (cell == 'P'):
                    playerSprite = Player((x, y))
                    self.player.add(playerSprite)

    def scrollX(self):
        player = self.player.sprite
        playerX = player.rect.centerx
        directionx = player.direction.x

        if playerX < (screenWidth / 5) and directionx < 0:
            self.worldShift = 8
            player.speed = 0
        elif playerX > (screenWidth - (screenWidth / 5)) and directionx > 0:
            self.worldShift = -8
            player.speed = 0
        else:
            self.worldShift = 0
            player.speed = 8

    def horizontalMovementCollision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = player.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def verticalMovementCollision(self):
        player = self.player.sprite
        player.applyGravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = player.rect.top
                    print("floor")
                    player.direction.y = 0
                    print(player.direction.y)

                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def run(self):
        #tiles
        self.tiles.update(self.worldShift)
        self.tiles.draw(self.displaySurface)
        self.scrollX()
        #player
        self.player.update()
        self.horizontalMovementCollision()
        self.verticalMovementCollision()
        self.player.draw(self.displaySurface)
