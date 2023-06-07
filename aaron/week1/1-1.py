class Sort():

    def __init__(self, nu):
        self.nu = nu

    def bubble_sort(self):
        nu_len = len(self.nu)
        while nu_len > 1:
            nu_len -= 1

            for i in range(nu_len):

                if self.nu[i] > self.nu[i+1]:
                    self.nu[i], self.nu[i+1] = self.nu[i+1], self.nu[i]
        return nu

    def sort(self):
        nu.sort()
        return nu


if __name__ == '__main__':
    nu = [2, -6, 3, 1, -5, 20, -3, 10, 9, 32]
    result = Sort(nu)
    print(f'Bubble_Sort: \n {result.bubble_sort()}')
    print(f'Sort:        \n {result.sort()}')
