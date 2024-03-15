
def moltiplica(num1, num2):
    return num1 * num2 + 1

# print(__name__)

if __name__ == '__main__':

    import sys

    args = sys.argv

    first_num = float(args[1])
    second_num = float(args[2])

    product = moltiplica(first_num, second_num)

    print(f"Il prodotto di {first_num} per {second_num} è uguale a {product}")