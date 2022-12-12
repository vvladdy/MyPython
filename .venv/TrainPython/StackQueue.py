from queue import Queue

q = Queue()
q.put(3)
q.put(True)
q.put('ttt')
print(q.get(), q.qsize())
print(q.get(), q.qsize())

from collections import deque

dq = deque()

dq.append('el1')
dq.append('el2')
dq.append('el3')
dq.append('el4')
el = dq.pop()
elleft = dq.popleft()
print(elleft)
print(len(dq))

from pythonds.basic import Stack

print('-'*8)
print('Stack pythonds.basic')
s = Stack()
s.push('steck1')
s.push('steck2')
s.push('steck3')
s.push('steck4')
s.push('steck5')
print(s.isEmpty())
eltop = s.peek()
print('Output top element: ', eltop, ', Stack size', s.size())
eltop = s.pop()
print('Delete top element: ', eltop, ', Stack size',  s.size())


