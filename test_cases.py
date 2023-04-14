#identify tests
from identify import identify

#error test
test = "abcdefgh.ijklmnop(123456)"
out = identify(test)
print(out)

test = ".moveX(123456)"
out = identify(test)
print(out)

test = "abcdefgh.moveX()"
out = identify(test)
print(out)

#identifinig test
test = "abcdefgh.moveX(123456)"
out = identify(test)
print(out)

test = "abcdefgh.moveX(-123456)"
out = identify(test)
print(out)

test = "abcdefgh.moveY(123456)"
out = identify(test)
print(out)

test = "abcdefgh.moveY(-123456)"
out = identify(test)
print(out)