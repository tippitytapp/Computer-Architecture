'''
def fun2():
    print('hi')
    return

def fun1():
    fun2()
    print("hello") # return_point_1
    return

fun1()
print("bye") # return_point_2

Call Stack
return_point_2
return_point_1
'''

"""
Rules:
When you call a function, push the return addr on the stack
when you return, pop the return address off the stack (and store it in the PC)

Stack:
699: a = 2      |
698: b = ??     | main's stack frame
697: [addr1]    |

696: x = 2      |
695: y = 7      | mult2's stack frame
694: z = 14     |
693: [addr2]    |

"""

'''
def mult2(x, y):
    z = x * y
    return z

def main():
    a = 2

    # [addr2]
    # v
    b = mult2(a, 7)
    print(b)
    return

main()
# [addr1]
# v
print('Done')
'''

'''
Recursive Stack
----------------
699: n = 4
698: [add1]
697: n = 3
696: [add2]
695: n = 2
694: [add2]
693: n = 1
692: [add2]
691: n = 0
690: [add2]
689: n = -1
688: [add2]
'''


# def looper(n):
#     if n<0:
#         return
#     print(n)
#     looper(n-1)
# looper(4)

'''
Interrupts
------------
Analogous to callbacks on event listeners
When some external event happens, call a subroutine (known as the interrupt handler)
Interrupts used with peripherals
'''