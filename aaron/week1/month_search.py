import sys
class month_search:

    def __init__(self, month, char, num):
        self.month = month
        self.char = char
        self.num = num

    def char_search(self):
        
        my_dict = {}

        if not self.char.isalpha():
          
            print('請輸入英文')
            sys.exit()

        for key, value in self.month.items():

            if self.char == format(key)[self.num - 1:self.num]:

                my_dict[format(key)] = format(value)
    
        return my_dict
    