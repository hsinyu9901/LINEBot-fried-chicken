# while Loop
result=0
n=1
while n<=10:
    result+=n
    n+=1
print(result)


# for Loop
# for 變數  in 列表:
result=0
for n in [5,7,2]:
    result+=n
print(result)


result=0
for n in range(1,11):
    result+=n
print(result)


# 函式
def test(n1, n2):
    return n1+n2
result=test(3,4)
print(result)


# 讀取檔案
file = open("data.txt", mode="r")
data=file.read()
file.close()
print(data)