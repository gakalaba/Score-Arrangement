def fib(n, depth=0):
    print("   "*depth, "fib(", n, " )")
    if (n < 2):
        result = 1
    else:
        result = fib(n-1, depth+1) + fib(n-2, depth+1)
    print("   "*depth, "-->", result)
    return result
fib(4)