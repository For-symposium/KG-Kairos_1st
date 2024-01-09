# name1 = "NAME1"
# name2 = "NAME2 NAME2"
# num = 1

# print(f"""name1 = {name1}
# name1_type = {type(name1)}
# name2 = {type(name2)}
# num_type : {type(num)}
# num_id : {id(num)}
# """)

# print(1,2,3,4,5, end = ' : ', sep = '-')

# name3 = input("Put your names : ")
# print(name3, type(name3))

# str1 = "I'm 30 years old this year"
# print(str1[4:6])

# str2 = " abc defgggg a"
# print(str2[len(str2)-1::-1])

# print(str2.count('g'))

# print(str2.strip()) # 맨 앞과 맨 뒤의 공백만 제거

# import random

# # eng_name = input('eng_name = ')
# eng_name = "Jacoby"

# front_name = eng_name[:3]
# # print("front : ", front_name)

# rand_num = random.randint(100, 999)

# norm_id = front_name + str(rand_num)
# print("norm_id : ", norm_id)

# # random하게 자리가 섞이도록 하는 방법?
# rand_id = str()

# web1 = 'http://naver.com'
# web2 = 'http://google.com'
# web3 = 'http://daum.com'

# def web2pw(web):
#     web = web[web.find('//')+2:web.find('.')] # Extract only domian, like "naver.com" and extract until find "."
#     pw = web[:3] + str(len(web)) + str(web.count('e')) + '!' # Concatenate whole things
#     return pw

# print(web2pw(web1))
# print(web2pw(web2))
# print(web2pw(web3))

# min = 2955
# hour = min//60
# min = min%60
# # print(hour)
# day = hour//24
# hour = hour%24
# print(f'{day}D {hour}h {min}m')

# str = "123"
# list1 = [1, 2]
# print(bool(list1), bool(str), (4>5), (1 < 4 < 3))

### Check if it is odd number
# import math

# num_in = int(input("Input number : "))
# num = 8
# operand = 2

# try:
#     if (num == 1): 
#         print("Not an Odd number")
# except:

# for operand in range(math.sqrt(num)):
#     operand

## Problem 1 : Find max number
# num_list = [10, 9, 20]
# max = 0
# for num in num_list:
#     if (num > max):
#         max = num
# print(max)

## Check if Prime number
# num = 131
# cnt = 0

# try:
#     if (num == 1): raise ValueError
#     for i in range(num//2):
#         if (num % (i+1)) == 0:
#             cnt += 1
#             if (cnt == 2):
#                 raise ValueError
#     print("True Prime number")

# except ValueError:
#     print("Not a Prime number")

# except:
#     print("Unknown Error")

# a = 10
# b = 19
# c = 28
# print(a) if (a>=b and a>=c) else print(b) if (b>=a and b>=c) else print(c)
# max_num = a if (a>=b and a>=c) else b if (b>=a and b>=c) else c
# print(max_num)

# def check_valid_cert(cert):
#     result = 0
#     cert_num = []
#     cert_num.append(cert.split('-')[0])
#     cert_num.append(cert.split('-')[1])

#     # Multiply front_num
#     for i in range(len(cert_num[0])):
#         result += int(cert_num[0][i]) * (i+2)

#     # Multiply back_num
#     for i in range(len(cert_num[1])-1):
#         if (i+8 >= 10): 
#             result += int(cert_num[1][i]) * (i)
#         else : 
#             result += int(cert_num[1][i]) * (i+8)
            
#     result %= 11
#     result = 11 - result

#     print("Valid") if (int(cert_num[1][-1]) == result) else print(f"Non-Valid. It should be {result}.")
    

# cert1 = '821010-1635210'
# cert2 = '970825-1551919'
# check_valid_cert(cert1)
# check_valid_cert(cert2)

# ## 윤년 체크
# year = '2024'
# year = int(year)

# def cheeck_youn(year):
#     return True if (year % 4 == 0) and (year % 100 != 0) else False

# ## 할인율 계산
# def discount_rate(price):
#     rate = 0.05 if (10000 <= price < 50000) else 0.075 if (50000 <= price < 100000) else 0.1 if (price >= 100000) else 0
#     return rate

# buy_price = '100000'
# buy_price = int(buy_price)

# print("Discount rate : {}\nTotal cost : {}".format(discount_rate(buy_price), buy_price*(1-discount_rate(buy_price))))

# lst = [1, 2, 3, 4]
# print(lst)
# lst.insert(1, 5) # insert at 3th pos with 5
# print(lst)
# lst.remove(5) # remove by value
# print(lst)
# lst.pop(0) # pop by index
# print(lst)

# lst2 = [555, 666]
# lst3 = lst + lst2 # concatenate list
# print(lst3)
# lst.extend(lst2) # concatenate list
# print(lst)

# import random
# menu = ['a', 'b', 'c', 'd', 'e']
# print(random.choice(menu))

# lst4 = [5, 4, 1, 1, 2]
# lst4.sort()
# print(lst4)
# lst4.reverse()
# print(lst4)

# t0 = (1,) # if without comma, t0 is int type
# t1 = (93, 'b3')
# t2 = (1,2,'b', 201, 8481, 45)
# print(t1[0])
# print(len(t1 + t2))
# print(t2[:3])
# t4 = tuple(range(1, 10, 2))
# print(t4)
# print(1 in t4)

# ## To-do list
# todo = ['Eng', 'Math', 'Python', 'Call']

# def choose_func(i):
#     if (i == 'a'):
#         complete()
#     elif (i == 'b'):
#         add_todo()
#     else:
#         print("Wrong cmd")

# def complete():
#     global todo
#     comp = input("1_Complete : ")
#     if (comp in todo):
#         todo.remove(comp)
#         print(f"Complete Updated! {todo}")
#     else:
#         print("Wrong name")
#         complete()

# def add_todo():
#     global todo
#     add = input("\nIf you need priority, append ' p' at the end.\n2_Add to-do list : ")
#     if (add[-2:] == ' p'):
#         todo.insert(0, '!!'+add[:-2])
#     else:
#         todo.append(add)
#     print(f"Add Updated! {todo}")

# while (True):
#     cmd = input("0_Choose cmd : ")
#     if (cmd == 'x'):
#         print("BREAK!")
#         break;
#     else: choose_func(cmd)
    

# ## for, while
# a = 9
# b = 9
# for i in range(1, a+1):
#     for j in range(1, b+1):
#         print(f"{i} * {j} = {i*j}")
#     print("\n")

# apart = [[101, 102], [201, 202], [301, 302]]
# # print(len(apart))
# for i in range(len(apart)):
#     for j in range(len(apart[i])):
#         print(apart[i][j])

# ### Christmas tree
# def star1(num):
#     for i in range(num):
#         print('*'*i)

# def star2(num):
#     for i in range(num, 0, -1):
#         print('*' * i)

# def star3(num):
#     for i in range(1, num+1):
#         print(' ' * (num-i) + '*' * (i))

# def star4(num):
#     if (num % 2 == 1):
#         for i in range(num):
#             print((' ' * ((2*num+1)//2 - (i+1))) + ('*' * (2*i+1)) + (' ' * ((2*num+1)//2 - (i+1))))
#     else:
#         print("Press odd number")

# def star5(num):
#     if (num%2 == 1):
#         for i in range(num//2+1):
#             print((' ' * (num//2-i)) + ('*' * (2*i+1)) + (' ' * (num//2-i)))
#         for i in range(1, num//2+1):
#             print((' ' * (i)) + ('*' * (num-2*i)) + (' ' * (i)))
#     else:
#         print("Press odd number")

# star1(7)
# star2(7)
# star3(7)
# star4(9)
# star5(9)

# dic_0 = {
#     'name' : 'Daniel',
#     'phone' : '3027',
#     'birth' : '970825'
# }
# print(dic_0)

# dic_0['phone'] = '4515'
# print(dic_0['phone'])

# del dic_0['phone']
# print(dic_0)

# print(dic_0.keys(), len(dic_0.keys()))
# print(dic_0.values(), len(dic_0.values()))
# print(dic_0.items(), len(dic_0.items())) # length of items = 2
# print(len(dic_0)) # -> 2

# for i in dic_0.keys():
#     print(i)

# for i in dic_0.values():
#     print(i)

# for i in dic_0.items():
#     print(i) # ('name', 'Daniel') type

# # print(dir(dic_0)) # given methods of dictionary

# print('Daniel' in dic_0) ## If i didn't type values, it naturally think about keys



# ######### Vocabulary scoring system ############
# voca_dict = {}
# cnt = 0

# def voca_note():
#     global voca_dict
#     while (1):
#         voca_input = input("Voca, Meaning : ")
#         if (voca_input == 'x'):
#             print(voca_dict)
#             break;
#         else : 
#             voca_dict[voca_input.split(" ")[0]] = voca_input.split(" ")[1]
        

# def voca_scoring(inp):
#     global voca_dict
#     global cnt

#     if (inp in voca_dict.keys()):
#         while (1):
#             check = input("Step 2. Press answer : ")
#             result = cross_check(inp, check)
#             if (result == 0): # wrong
#                 print("Wrong answer.")  
#             else: # correct
#                 cnt += 1
#                 print(f"Correect!! Current point is {cnt}")
#                 return cnt
#     else:
#         print(f"There is no voca {inp}")


# def cross_check(inp, check):
#     global voca_dict
#     global cnt

#     if (voca_dict[inp] == str(check)):
#         return 1
#     else:
#         return 0



# ##### Main loop #####

# voca_note() # add voca dictionary

# while (1):
#     eng_key = input("Check your word, English voca : ")
#     if (eng_key == 'x'): 
#         print(f"Exit with score {cnt}")
#         break
#     else: 
#         voca_scoring(eng_key)
    

# ###### Turtle with iteration ######
# from turtle import *
# import time

# def draw_sth(num):
#     for _ in range(num):
#         forward(100)
#         left(360/num)
#     print("Finished")
#     time.sleep(2)

# speed(0)
# sides = int(input("How many sides? "))
# if (sides < 3):
#     print("Sides should be greater than 2")
# else: 
#     draw_sth(sides)

# def sayhello(name, birth):
#     print(f"My name is {name}, and my birth is {birth}")

# sayhello("Daniel", "970825")

# def get_sum_minus(n1, n2):
#     sum = n1 + n2
#     minus = n1 - n2
#     return sum, minus

# for i in get_sum_minus(5, 2):
#     print(i)

# def is_odd_even(n):
#     if (n <= 0): return "Wrong"
#     if (n % 2 == 0): return "Even"
#     else: return "Odd"

# print(is_odd_even(0))

# def greet(name, msg = "Default msg"):
#     print(f"Hi {name}, {msg}")

# greet("Daniel")

# def get_minus(x,y,z):
#     return x-y+z

# print(get_minus(1,2,3))
# print(get_minus(1,z=3,y=2))
# help(print)

# 가변인수 : 인수값을 여러 가지 받아도 괜찮음
# def param1(*args):
#     print(args[-1:])

# dictionary type의 key & value 
# def param2(**kargs):
#     print(kargs)

# a = 1
# b = 2

# def fun1():
#     b = 5
#     print(a, b)

# def fun2():
#     # b = 3
#     print(a, b)

# param1(1, 2, 3)
# param2(a = 4, b = 2, c = 3)
# fun1()
# fun2()

# def coupon_juice(own, need):
#     juice = own // need
#     coupon = own % need
#     coupon += juice # Add the additional coupon
#     while (1):
#         if (coupon >= need): # if 
#             juice += coupon // need
#             coupon = coupon % need
#         else:
#             return juice

# print(coupon_juice(24, 7))

# import call_func as cf

# cf.greet("name", 'greeting!')

#### Taxi calling service
# import random

# def take_passenger():
#     cnt = 0
#     for i in range(1, 51):
#         expected_time = random.randint(5, 50)
#         if (5 <= expected_time <= 15):
#             print(f"[O] {i}th passenger (Expected time : {expected_time})")
#             cnt += 1
#         else:
#             print(f"[ ] {i}th passenger (Expected time : {expected_time})")
#     print(f"Total passenger : {cnt}")

# take_passenger()

# class Human:
#     def __init__(self, name, age, sex):
#         self.name = name
#         self.age = age
#         self.sex = sex

#     def arm(a):
#         return a

# husband = Human("bhg", 27, "male")
# print(husband.name)

# hm1 = Human.arm(5)
# print(hm1)

# import call_func as cf
# from call_func import Human as hm

# hm0 = hm("bhg", 27, "male")
# print(hm0.name)

# hm1 = hm.arm(10)
# print(hm1)

