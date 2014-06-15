import numpy as np
from Queue import Queue
from threading import *
from itertools import product

def get_input():
	#print str(input("Do you wish to make conversion? [y/n]"))
	return "n"

class Node(object):

	def __init__(self):
		self.q = Queue()

		self.stack_out = []
		self.t = Thread(target=self.run, args=(self))
		self.t.daemon = True
		self.t.start()
	
	def run(self):
		try:
			while True:
				out, is_query = self.q.get()
				self.stack_out.append(out)
				if len(self.stack_out) > 1:
					#print self.stack_out
					combined = np.array(np.mean(self.stack_out, axis=0))
					'''
					print "combined:"
					print combined
					print '---'
					'''
					self.stack_out.append(combined)
				self.q.task_done()
		except Exception, e:
			print e
			for i in self.q.get():
				self.q.task_done()

	def __iter__(self):
		if self.stack_out:
			yield self.stack_out.pop(0)


mem = Node()

for i in xrange(5):
	
	item = []
	for p in product([0, 255], repeat=3):
		item.append(np.array(p))

	
	print 'training', '\n-- '.join(str(p) for p in item)
	mem.q.put((item, False))
	print '-----------'

mem.q.join()       # block until all tasks are done

#print [x for x in mem.stack_out]
print mem.stack_out.pop()
