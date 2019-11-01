import pygame
import time
import re


class Caption(pygame.sprite.Sprite):
    """
        Captions
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = "Accuracy 0/0, Speed 0/min, Time 0 "
        self.update()

    def update(self):
        self.image = pygame.font.Font(None, 26).render(self.text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()

    def setText(self, speed, words, corrWords, countDownTime):
        self.text = f"Accuracy {corrWords}/{words}, Speed {speed}/min, Time {countDownTime} "


class TextGeneratorFromFile():
    """
        txt file -> string array
    """

    def __init__(self, path, numWords):
        self.path = path
        self.pos = 0
        self.numWords = numWords
        with open(self.path, 'r', encoding='utf-8') as f:
            self.text = re.findall(r'\w+', f.read())

    def getText(self):
        if self.pos + self.numWords >= len(self.text):
            self.pos = 0
        text = " ".join(self.text[self.pos: self.pos + self.numWords])
        self.pos += self.numWords
        return text


class InputArea:
    """
        Content Part to refresh information.
    """

    def __init__(self, path):
        self.textGenerator = TextGeneratorFromFile(path, 60)
        self.text = self.textGenerator.getText()
        # Logical Part
        self.time = time.time()  # beginning time
        self.words = 0  # the number of words
        self.speed = 0  # tying speed 
        self.flag = True  # correct flag
        self.wordsCorr = 0  # wrong workds
        self.countDownTime = 0  
        # Graphical Part
        self.pos = 0  # input position
        self.wordsPage = 0  # Nb of words passed by in single page
        self.vMargin = 10  
        self.hMargin = 10  
        self.paddingX = 10 
        self.paddingY = 50  
        
        self.space = pygame.font.Font(None, 26).size(' ')[0]
        self.surface = pygame.display.get_surface()
        max_width, _ = self.surface.get_size()
        self.max_width = max_width - self.hMargin
        self.update()

    def _renderWord(self, wordText, color, highlight):
        global x, y
        word_surface = pygame.font.Font(
            None, 36).render(wordText, 1, color)
        word_width, word_height = word_surface.get_size()
        word_height += self.vMargin
        if x + word_width >= self.max_width:
            x = self.paddingX
            y += word_height
        if highlight is not None:
            word_surface.blit(highlight, (0, 0))
        self.surface.blit(word_surface, (x, y))
        x += word_width + self.space
        
    def update(self):
        
        self.speed = self.words / (time.time() - self.time + 1e-6) * 60

        words = self.text.split(' ')
        global x, y
        x, y = self.paddingX, self.paddingY
        count = 0

        # Previous Words
        for i in range(self.wordsPage):
            self._renderWord(words[i], (255, 255, 255), None)
            count += len(words[i]) + 1
            # print(count)

        # Current Word
        highlight = pygame.font.Font(None, 36).render(
            words[self.wordsPage][:self.pos - count], 1, (255, 255, 255))
        self._renderWord(words[self.wordsPage], (0, 0, 0), highlight)

        # the next words
        for i in range(1 + self.wordsPage, len(words)):
            self._renderWord(words[i], (0, 0, 0), None)
        # print(count)

    @property
    def count_down_time(self):
        return time.time() - self.time

    def countWords(self):
        self.words += 1
        self.wordsPage += 1
        if self.flag:
            self.wordsCorr += 1
        self.flag = True

    def keyin(self, key):
        if self.text[self.pos] == " ":
            self.countWords()
        elif key != self.text[self.pos]:
            self.flag = False

        self.pos += 1
        if len(self.text) == self.pos:
            self.pos = 0
            self.text = self.textGenerator.getText()
            self.countWords()
            self.wordsPage = 0
