from proj.tasks import add

print("start task 2+2")
res = add.delay(2, 2)
print("current state: " + res.state)
print("result: " + str(res.get(timeout=1)))
print("source id: " + res.id)
print("current state: " + res.state)