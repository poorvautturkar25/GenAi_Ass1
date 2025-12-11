def count_even_odd(numbers):
    even = 0
    odd = 0

    for num in numbers:

            if num % 2 == 0:
                even +=1
            else:
                odd +=1
    return even,odd      