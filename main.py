# -*- coding: utf-8 -*-
"""
【Python笔试】

提交时间：尽快提交，最晚不超过48小时。
要求：不得抄袭，一经发现，终止应聘。
"""

import pygame
from pygame.locals import *
from utils import Caption, InputArea
import time


class GUI:
    def __init__(self, textSource):
        self.speedLimit = 70
        self.clock = pygame.time.Clock()
        self.screenRect = Rect(0, 0, 640, 480)
        self.screen = pygame.display.set_mode(self.screenRect.size)
        self.background = pygame.Surface(self.screenRect.size).convert()
        self.elements = pygame.sprite.RenderUpdates()
        self.inputArea = InputArea(textSource)
        self.caption = Caption()
        self.elements.add(self.caption)
        self.background.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        self.flag = True
        self.TimeLimit = 60
        pygame.display.set_caption('SUPER TYPIST')
        pygame.display.update()

    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    if len(event.unicode) > 0:
                        self.inputArea.keyin(event.unicode)
                        self.flag = self.inputArea.flag
            count_down2 = self.inputArea.count_down_time

            if count_down2 < self.TimeLimit:
                typing_speed = self.inputArea.speed
                words = self.inputArea.words
                corr_words = self.inputArea.wordsCorr

            if count_down2 > self.TimeLimit:
                count_down2 = self.TimeLimit
            self.caption.setText(typing_speed, words, corr_words, count_down2)


            if typing_speed > self.speedLimit:
                typing_speed = self.speedLimit
            colors = [0, 191, 255] if not self.flag else [int(255 - 255 * typing_speed / self.speedLimit),
                                                          int(255 * typing_speed / self.speedLimit), 0]
            self.screen.fill(colors)
            self.inputArea.update()
            self.elements.update()
            self.elements.draw(self.screen)
            pygame.display.update()
            self.clock.tick(5)


if __name__ == '__main__':
    """
       题目：利用面向对象的方式实现逻辑层显示层分离，用pygame完成响应键盘敲击速度的游戏：随机截取一段英文短文。
       统计一分钟内用户对照输入的正确的单词数量并实时根据键盘敲击的速度显示屏幕背景色。
       越快屏幕颜色就越偏向绿色。越慢越偏向红色。
       ps：如果输入完了一整段一分钟还没到就换下一段。不可以用faker和pygame-text-input
       """
    pygame.init()
    procedure = GUI('ALittleReunion.txt')
    procedure.run()
