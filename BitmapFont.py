import pygame




class BitmapFont:
    def __init__(self):
        # index starts at 0x20h
        self.ascii_table = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        
    def load_bitmap_font(self):
        self.font_surface = pygame.image.load("fonts/scroller.bmp")
        self.surf_arr = pygame.surfarray.array2d(self.font_surface)
        self.scan_letter_coords()
        
    def scan_letter_coords(self):
        letter_pos_dict = {}
         
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

                letter_pos_dict[letter] = ( (x_pos1, y_pos1), (x_pos2, y_pos2) )
                print "Debug: found letter: '%s' between: (x:%d, y:%d) - (x:%d, y:%d)" % (letter, x_pos1, y_pos1, x_pos2, y_pos2)
            else:
                print "end of bitmap."

            all_letters_found = True if letter_info == None else False

        return letter_pos_dict


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
                    
                    return (self.ascii_table[self._cur_letter_index], ((x_pos_start, 0), (x_pos_end, 0)))
                else:
                    x_pos_start = next_key_pos
                    self._last_letter_x_pos = x_pos_start 
                    self.state = self.SEARCH_NEXT_LETTER
            
    def _get_next_key_pixel_x_pos(self):
        for i in range(self._cur_x_pos, self.font_surface.get_width()):
            if self.surf_arr[i, 0] == 0:
                self._cur_x_pos = i + 1
                return i
        
        return None

