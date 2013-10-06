import pygame


class BitmapChar():
    def __init__(self, font_surface, width, height):
        self.font_surface = font_surface
        self.width = width
        self.height = height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


class BitmapFont:
    def __init__(self):
        # index starts at 0x20h
        self.ascii_table = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        self.letter_pos_dict = {}

    def load_bitmap_font(self, path):
        self.font_surface = pygame.image.load(path).convert() # convert bitmap format to screen formal (pixel depth etc...)
        self.surf_arr = pygame.surfarray.array2d(self.font_surface.convert(8))
        print "Debug: surf_arr: "
        print self.surf_arr

        self._scan_letter_coords()
        
    def draw_bitmap_text(self, surface, x_pos, y_pos, text):
        cur_x_pos = x_pos
        cur_y_pos = y_pos

        for char in text:
            self.put_bitmap_char(surface, cur_x_pos, cur_y_pos, char)
            char_width = self.letter_pos_dict[char][1][0] - self.letter_pos_dict[char][0][0] - 1
            cur_x_pos += char_width
 
    def put_bitmap_char(self, surface, x_pos, y_pos, char):
        letter_info = self.letter_pos_dict[char]

        if letter_info != None:
            font_x_pos1 = letter_info[0][0]
            font_y_pos1 = letter_info[0][1]
            font_x_pos2 = letter_info[1][0]
            font_y_pos2 = letter_info[1][1]

            surface.blit(self.font_surface, 
                        (x_pos, y_pos), pygame.Rect( (font_x_pos1 + 1, font_y_pos1 + 1), (font_x_pos2 - font_x_pos1 - 1, font_y_pos2)))

    def _scan_letter_coords(self):  
        self.letter_pos_dict = {}

        self.SEARCH_NEXT_LETTER, self.GET_LETTER_LENGTH = range(2)
        self.state = self.SEARCH_NEXT_LETTER
        all_letters_found = False
        self._cur_x_pos = 0
        self._last_letter_x_pos = 0
        self._cur_letter_index  = -1

        while(not all_letters_found):
            letter_info = self._get_next_letter()

            if letter_info != None:
                letter = letter_info[0]
                x_pos1 = letter_info[1][0][0]
                y_pos1 = letter_info[1][0][1]
                x_pos2 = letter_info[1][1][0]
                y_pos2 = letter_info[1][1][1]

                self.letter_pos_dict[letter] = ( (x_pos1, y_pos1), (x_pos2, y_pos2) )
                print "Debug: found letter: '%s' between: (x:%d, y:%d) - (x:%d, y:%d)" % (letter, x_pos1, y_pos1, x_pos2, y_pos2)
            else:
                print "end of bitmap."

            all_letters_found = True if letter_info == None else False

        # at last fill all undefined letters with rhe default "?" char position.
        #for  self.letter_pos_dict


        return self.letter_pos_dict


    def _get_next_letter(self):
        x_pos_start = 0
        x_pos_end = 0

        end_of_bitmap = False
        while(not end_of_bitmap):
            if self.state == self.SEARCH_NEXT_LETTER:
                x_pos_start = self._last_letter_x_pos
                self.state = self.GET_LETTER_LENGTH

            elif self.state == self.GET_LETTER_LENGTH:
                next_key_pos = self._get_next_key_pixel_x_pos()
                self._cur_letter_index += 1

                if next_key_pos == None:
                    end_of_bitmap = True
                elif next_key_pos - self._last_letter_x_pos > 2:
                    x_pos_start = self._last_letter_x_pos
                    x_pos_end = next_key_pos 
                    self._last_letter_x_pos = x_pos_end
                    
                    return (self.ascii_table[self._cur_letter_index], ((x_pos_start, 0), (x_pos_end, self.font_surface.get_height())))
                else:
                    x_pos_start = next_key_pos
                    self._last_letter_x_pos = x_pos_start 
                    self.state = self.SEARCH_NEXT_LETTER
            
    def _get_next_key_pixel_x_pos(self):
        key_value = 127

        for i in range(self._cur_x_pos, self.font_surface.get_width()):
            if self.surf_arr[i, 0] == key_value:
                self._cur_x_pos = i + 1
                return i
 
        return None


class BitmapFontScroller:
    def __init__(self, target_surface, x_pos, y_pos):
        self.scroller_surf = pygame.Surface((200, 30))
        self.bf = BitmapFont()
        self.bf.load_bitmap_font("fonts/1/coolspot.bmp")
        self.text = ""
        self.cur_text_pos = 0
        self.target_surface = target_surface
        self.x_pos = x_pos
        self.y_pos = y_pos

    def set_text(self, text):
        self.text = text
        self.cur_text_pos = 0

    def _drop_char(self):
        cur_char = self.text[self.cur_text_pos]
        self.bf.put_bitmap_char(self.scroller_surf, 0, cur_char)

    def tick(self):
        self.x_pos -= 1
        self.target_surface.blit(self.scroller_surf, (self.x_pos, self.y_pos))



