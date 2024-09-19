def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Division by zero"
    return x / y

def process_numbers(a, b):
    product = multiply(a, b)
    quotient = divide(a, b)
    return product, quotient

def main():
    num1 = 12
    num2 = 4
    results = process_numbers(num1, num2)
    print(f"Product and Quotient: {results}")

if __name__ == "__main__":
    main()
