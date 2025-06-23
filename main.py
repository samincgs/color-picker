import pygame
import sys
import pyperclip

from tkinter import filedialog

RENDER_SCALE = 2
SCROLL_SPEED = 5
ZOOM_LEVEL = 1

class ColorPicker:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Color Picker')
        
        self.clock = pygame.Clock()
        self.screen = pygame.display.set_mode((1200, 900))        
        file_name = filedialog.askopenfilename(title='Select an Image', filetypes=(('all files', '*.*'), ('jpeg files', '*.jpg'), ('gif files', '*.gif*'), ('png files', '*.png')))
        if not file_name:
            self.quit()

        self.img = pygame.image.load(file_name).convert()
        
        # self.screen = pygame.display.set_mode((self.img.get_width() * RENDER_SCALE, self.img.get_height() * RENDER_SCALE))
        self.display = pygame.Surface((600, 450))
        
        self.mpos = (0, 0)
        
        self.scroll_direction = {'up': False, 'down': False, 'right': False, 'left': False}
        self.scroll = [0, 0]
        
        self.default_mode = 'rgb'
        self.color = None
        self.current_color = None
        
        # print(pygame.font.get_fonts())
        self.font = pygame.font.SysFont('Arial', 20, True)
    
    def hex_to_rgb(self, hex):
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, rgb):
         return ('#' + '{:02X}' * 3).format(*rgb)
    
      
    def quit(self):
        pygame.quit()
        sys.exit()
    
    def run(self):
        while True:
            
            self.display.fill((0, 0, 0))
            self.mpos = pygame.mouse.get_pos()
            self.mpos = (self.mpos[0] // RENDER_SCALE, self.mpos[1] // RENDER_SCALE)
            if self.scroll_direction['left']:
                self.scroll[0] -= SCROLL_SPEED
            if self.scroll_direction['right']:
                self.scroll[0] += SCROLL_SPEED
            if self.scroll_direction['up']:
                self.scroll[1] -= SCROLL_SPEED
            if self.scroll_direction['down']:
                self.scroll[1] += SCROLL_SPEED
            
            self.scroll = [max(self.scroll[0], 0), max(self.scroll[1], 0)]
            
            self.display.blit(self.img, (-self.scroll[0], -self.scroll[1]))
            
            if self.color:
                if self.default_mode == 'rgb':
                    self.current_color = self.color
                else:
                    self.current_color = self.rgb_to_hex(self.color)
            
            # ui
            chosen_color_surf = self.font.render('Chosen Color: ' + str(self.current_color), True, (255, 255, 255))
            self.screen.blit(chosen_color_surf, (self.screen.get_width() - chosen_color_surf.get_width() - 5, 15))
            color_mode_surf = self.font.render('Mode: ' + str(self.default_mode), True, (255, 255, 255))
            self.screen.blit(color_mode_surf, (self.screen.get_width() - color_mode_surf.get_width() - 5, 45))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                    if event.key == pygame.K_a:
                        self.scroll_direction['left'] = True
                    if event.key == pygame.K_d:
                        self.scroll_direction['right'] = True
                    if event.key == pygame.K_w:
                        self.scroll_direction['up'] = True
                    if event.key == pygame.K_s:
                        self.scroll_direction['down'] = True
                    if event.key == pygame.K_m:
                        self.default_mode = 'rgb' if self.default_mode != 'rgb' else 'hex'                       
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.scroll_direction['left'] = False
                    if event.key == pygame.K_d:
                        self.scroll_direction['right'] = False
                    if event.key == pygame.K_w:
                        self.scroll_direction['up'] = False
                    if event.key == pygame.K_s:
                        self.scroll_direction['down'] = False
                    if event.key == pygame.K_c:
                        pyperclip.copy(str(self.current_color))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.color = self.display.get_at(self.mpos)[:3]

                               
            pygame.display.update()
            self.clock.tick(60)
            if ZOOM_LEVEL == 1:
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
    
if __name__ == '__main__':
    ColorPicker().run()