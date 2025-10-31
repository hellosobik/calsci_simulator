class BaseUploader:
    def __init__(self, disp_out, chrs):
        self.disp_out=disp_out
        self.chrs=chrs
        self.disp_out.clear_display()
    def update(self, buffer):
        raise NotImplementedError("To be overridden!")
    def refresh(self, state="default"):
        raise NotImplementedError("To be overridden!")

    
    def _print_character(self, chtr, invert=False):
        chtr_byte_data = self.chrs.Chr2bytes(chtr)
        cursor_line = 0b00000000
        if invert:
            chtr_byte_data=self.chrs.invert_letter(chtr)
            cursor_line = 0b11111111
        for k in chtr_byte_data:
            self.disp_out.write_data(k)
        self.disp_out.write_data(cursor_line)
    
    def _display_bar(self, state):
        self.disp_out.set_page_address(7)
        self.disp_out.set_column_address(0)
        state = state+" "*(len("default")-len(state))
        j_counter=0
        for j in state:
            chtr=j
            chtr_byte_data=self.chrs.invert_letter(chtr)
            cursor_line=0b11111111
            for k in chtr_byte_data:
                self.disp_out.write_data(k)
            self.disp_out.write_data(cursor_line)
            j_counter+=1
    
    def _clear_row_display(self, row):
        self.disp_out.set_page_address(row)
        self.disp_out.set_column_address(0)

class TextUploader(BaseUploader):
    def __init__(self, disp_out, chrs, t_b):
        super().__init__(disp_out=disp_out, chrs=chrs)
        self.buffer_klass = t_b


    def update(self, t_b_new):
        self.buffer_klass=t_b_new
    

    def refresh(self, state="default"):
        buf = self.buffer_klass.buffer()
        ref_ar = self.buffer_klass.ref_ar()
        start_row = ref_ar[0]//self.buffer_klass.cols
        end_row = ref_ar[1]//self.buffer_klass.cols
        print(start_row, end_row)
        print(buf)
        for i in range(start_row, end_row):
            self._clear_row_display(i)
            print(len(buf), i)
            if buf[i].strip()!="" or self.buffer_klass.cursor()//self.buffer_klass.cols==i:
                j_counter=0
                for j in buf[i]:
                    if j_counter+i*self.buffer_klass.cols==self.buffer_klass.cursor():
                        self._print_character(j, invert=True)
                    else:
                        self._print_character(j, invert=False)
                    j_counter+=1
            else:
                self._print_character(" ", invert=False)

        self._display_bar(state)
