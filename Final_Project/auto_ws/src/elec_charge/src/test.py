def test(a):
    if a == 0:
        return "Zero"
    elif a == 1:
        return "One"

while True:
    a = int(input("Zero or One : "))
    print(test(a))