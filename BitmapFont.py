import pygame
import math


class BitmapChar():
    def __init__(self, font_surface, character, left, top, right, bottom):
        self.character = character
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def get_width(self):
        return self.right - self.left

    def get_height(self):
        return self.bottom - self.top


class BitmapFont:
    def __init__(self):
        # index starts at 0x20h
        self.ascii_table = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ "
        self.char_dict = {} # contains all coordinates of every char in the font bitmap
        self.font_surface = None # surface of bitmap font
        self.surf_arr = None # surface as array
        self.SEARCH_NEXT_CHAR, self.GET_CHAR_WIDTH = range(2) # state machine for bitmap font parser

    def load_bitmap_font(self, path, space_width_letter = 'A'):
        self.font_surface = pygame.image.load(path).convert() # convert bitmap format to screen formal (pixel depth etc...)
        self.surf_arr = pygame.surfarray.array2d(self.font_surface.convert(8))
        self._scan_letter_coords()
        self.space_width_letter = space_width_letter
 
    def put_bitmap_char(self, surface, x_pos, y_pos, char, x_offset = 0, width = None):
        char = self.char_dict[char]
        char_width = char.get_width() - x_offset if width == None else width
        surface.blit(self.font_surface, (x_pos, y_pos), pygame.Rect(char.left + x_offset, char.top, char_width, char.get_height()))

        return char.get_width() - x_offset #+ char_width

    def _scan_letter_coords(self):
        self.state = self.SEARCH_NEXT_CHAR
        self._cur_x_pos = 0
        self._last_char_x_pos = 0
        self._cur_char_index  = -2

        all_chars_found = False
        while(not all_chars_found):
            char = self._get_next_char()

            if char != None:
                self.char_dict[char.character] = char
           #     print "Debug: found letter: '%s' between: (x:%d, y:%d) - (x:%d, y:%d)" % (char.character, char.left, char.top, char.right, char.bottom)
            else:
                all_chars_found = True
           #     print "end of bitmap."

        # at last fill all undefined letters with rhe default "?" char position.
        # for self.letter_pos_dict


    def _get_next_char(self):
        x_pos_start = 0
        x_pos_end = 0

        end_of_bitmap = False
        while(not end_of_bitmap):
            if self.state == self.SEARCH_NEXT_CHAR:
                x_pos_start = self._last_char_x_pos
                self.state = self.GET_CHAR_WIDTH

            elif self.state == self.GET_CHAR_WIDTH:
                next_key_pos = self._get_next_key_pixel_x_pos()
                self._cur_char_index += 1

                if next_key_pos == None:
                    end_of_bitmap = True
                elif next_key_pos - self._last_char_x_pos > 2:
                    x_pos_start = self._last_char_x_pos
                    x_pos_end = next_key_pos
                    self._last_char_x_pos = x_pos_end

                    char = BitmapChar(self.font_surface, self.ascii_table[self._cur_char_index], x_pos_start + 1, 1, x_pos_end, self.font_surface.get_height())
                    return char
                else:
                    x_pos_start = next_key_pos
                    self._last_letter_x_pos = x_pos_start
                    self.state = self.SEARCH_NEXT_CHAR
            
    def _get_next_key_pixel_x_pos(self):
        key_value = 127

        for i in range(self._cur_x_pos, self.font_surface.get_width()):
            if self.surf_arr[i, 0] == key_value:
                self._cur_x_pos = i + 1
                return i
 
        return None


class BitmapString:
    def __init__(self, font_path, text):
        self.bitmap_font = BitmapFont()
        self.bitmap_font.load_bitmap_font(font_path)
        self.text = text

    def draw_bitmap_text(self, surface, x_pos, y_pos):
        cur_x_pos = x_pos
        cur_y_pos = y_pos

        for char in self.text:
            self.put_bitmap_char(surface, cur_x_pos, cur_y_pos, char)
            char_width = self.char_dict[char].get_width()
            cur_x_pos += char_width


class BitmapFontScroller:
    def __init__(self, target_surface, font_path, x_pos, y_pos):
        self.scroller_surface = pygame.Surface((640, 300))
        self.effect_surface = pygame.Surface((self.scroller_surface.get_width(),
                                              self.scroller_surface.get_height()))
        #self.scroller_surface.fill(pygame.Color("black"))
        self.target_surface = target_surface


        self.bf = BitmapFont()
        self.bf.load_bitmap_font(font_path)
        self.text = ""
        self.cur_char_index = 0
        self.cur_char_pixel_pos = 0
        self.pixel_underflow = 0

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.scrollsinus1 = 0
        self.scrollsinus2 = 0

    def set_text(self, text):
        self.text = text
        self.cur_char_index = 0

    #def _drop_partial_char(self, char):
    #    cur_char = self.bf.char_dict[char]
    #    self.bf.put_bitmap_char(self.scroller_surf, self.scroller_surf.get_width() - cur_char.get_width(), 0, char)

    def scroll(self, pixels_per_second):
        # scroll whole scroller one pixel to the left and make 1 pixel row space for
        # the next partial drawing.
        self.scroller_surface.blit(self.scroller_surface, (-pixels_per_second, 0))
        self.scroller_surface.fill(pygame.Color("black"),
                                pygame.Rect(self.scroller_surface.get_width() - pixels_per_second,
                                            0,
                                            pixels_per_second,
                                            self.scroller_surface.get_height()))

        # draw partial pixel row of current char
        # TODO: cosmetc refactoring (DRY)
        pixel_underflow = 0
        while pixel_underflow == 0:
            pixel_underflow = self.bf.put_bitmap_char(self.scroller_surface,
                                                          self.scroller_surface.get_width() - pixels_per_second,
                                                          self.scroller_surface.get_height() / 8,
                                                          self.text[self.cur_char_index],
                                                          self.cur_char_pixel_pos)
            print pixel_underflow

            if pixel_underflow < 0:
                print "underflow!"
                self.cur_char_index = (self.cur_char_index + 1) % len(self.text)
                self.cur_char_pixel_pos = 0

            self.cur_char_pixel_pos += pixels_per_second
            self.target_surface.blit(self.scroller_surface, (self.x_pos, self.y_pos))

            # use carry for next character
            if pixel_underflow < 0:
                pixel_underflow = self.bf.put_bitmap_char(self.scroller_surface,
                                                          self.scroller_surface.get_width() - abs(pixel_underflow),
                                                          self.scroller_surface.get_height() / 8,
                                                          self.text[self.cur_char_index],
                                                          self.cur_char_pixel_pos)

            # sine effect
            amplitude = 60
            frequency = 12
            factor = frequency / 100.0

            # 2-Pixel Sinescroll
            # Take the standard scroller in the background as source and blit it to the front screen
            # Blitting in 250 steps, changing y coord so we have a sinewave

            #PatBlt(hEffectDC, 0, 0, canvasDimX, canvasDimY, 0);
            self.scrollsinus2 = self.scrollsinus1
            for i in range(0, self.effect_surface.get_width(), 2):
                tar_x = i
                tar_y = amplitude + int(amplitude * math.sin(self.scrollsinus2))

                self.effect_surface.blit(self.scroller_surface,
                                         (tar_x, tar_y),
                                         pygame.Rect(i, 0,
                                                     2, self.effect_surface.get_height(),
                                                     )

                )
                self.scrollsinus2 += .022

            self.scrollsinus1 += factor
            self.target_surface.blit(self.effect_surface, (self.x_pos, self.y_pos))

    def tick(self):
        self.scroll(1)


