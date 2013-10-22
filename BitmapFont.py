import pygame


class _BitmapChar():
    def __init__(self, font_surface, character, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.character = character

    def get_width(self):
        return self.right - self.left

    def get_height(self):
        return self.bottom - self.top


class BitmapFont:
    def __init__(self):
        # index starts at 0x20h
        self.ascii_table = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        self.char_dict = {} # contains all coordinates of every char in the font bitmap
        self.font_surface = None # surface of bitmap font
        self.surf_arr = None # surface as array
        self.SEARCH_NEXT_CHAR, self.GET_CHAR_WIDTH = range(2) # state machine for bitmap font parser

    def load_bitmap_font(self, path):
        self.font_surface = pygame.image.load(path).convert() # convert bitmap format to screen formal (pixel depth etc...)
        self.surf_arr = pygame.surfarray.array2d(self.font_surface.convert(8))
        self._scan_letter_coords()
        
    def draw_bitmap_text(self, surface, x_pos, y_pos, text):
        cur_x_pos = x_pos
        cur_y_pos = y_pos

        for char in text:
            self.put_bitmap_char(surface, cur_x_pos, cur_y_pos, char)
            char_width = self.char_dict[char].get_width()
            cur_x_pos += char_width
 
    def put_bitmap_char(self, surface, x_pos, y_pos, char, x_offset = 0, width = None):
        char = self.char_dict[char]
        


        surface.blit(self.font_surface, (x_pos, y_pos), pygame.Rect(char.left, char.top, char.get_width(), char.get_height()))


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
                print "Debug: found letter: '%s' between: (x:%d, y:%d) - (x:%d, y:%d)" % (char.character, char.left, char.top, char.right, char.bottom)
            else:
                all_chars_found = True
                print "end of bitmap."

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

                    char = _BitmapChar(self.font_surface, self.ascii_table[self._cur_char_index], x_pos_start, 1, x_pos_end - 1, self.font_surface.get_height())
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


class BitmapFontScroller:
    def __init__(self, target_surface, font_path, x_pos, y_pos):
        self.scroller_surf = pygame.Surface((200, 30))
        self.scroller_surf.fill(pygame.Color("red"))
        self.bf = BitmapFont()
        self.bf.load_bitmap_font(font_path)
        self.text = "COON"
        self.cur_char_index = 0
        self.target_surface = target_surface
        self.x_pos = x_pos
        self.y_pos = y_pos


    def set_text(self, text):
        self.text = text
        self.cur_char_index = 0

    def _drop_char(self, char):
        cur_char = self.text[self.cur_char_index]

        cur_char = self.bf.char_dict['C']
        self.bf.put_bitmap_char(self.scroller_surf, self.scroller_surf.get_width() - cur_char.get_width(), 0, char)

    def tick(self):
        self.scroller_surf.blit(self.scroller_surf, (-1, 0))

        self.scroller_surf.fill(pygame.Color("red"),
                                pygame.Rect(self.scroller_surf.get_width() - 1,
                                            0,
                                            1,
                                            self.scroller_surf.get_height()))

        self.target_surface.blit(self.scroller_surf, (self.x_pos, self.y_pos))






