import asyncio
import aiohttp
from seshat import seshat

seshat.home("/Users/adrianloh/Desktop")

@seshat.record
def call_with_args(a, b, c):
	pass

@seshat.record
def call_with_kwargs(a, b, c, d=None, e=None):
	pass

@seshat.record
def call_with_return_one(o):
	return o

@seshat.record
def call_with_return_many(o1, o2):
	return o1, o2

@seshat.record
def call_generator(length):
	for i in range(length):
		yield i

@seshat.record
async def http_get(url):
	res = await aiohttp.get(url)
	if res.status == 200:
		return await res.json()
	else:
		return None

# TESTS

def test_call_with_args(T):
	call_with_args(1, 2, 3)

class A: pass
def b(): pass

def test_call_with_kwargs(T):
	call_with_kwargs(1, 2, 3, d=A(), e=b)

def test_call_with_return(T):
	o = dict(a=1, b=2, c=3)
	a = call_with_return_one(o)
	if a != o:
		T.fail()

def test_call_with_return_many(T):
	o1 = dict(a=1, b=2, c=3)
	o2 = dict(d=4, e=5, f=6)
	a, b = call_with_return_many(o1, o2)
	if a != o1 or b != o2:
		T.fail()

def test_call_generator(T):
	collect = []
	length = 10
	for i in call_generator(length):
		collect.append(i)
	if len(collect) != length:
		T.fail()

def test_call_async(T):
	loop = asyncio.get_event_loop()
	loop.run_until_complete(http_get("https://httpbin.org/get"))
	loop.close()

def test_log(T):
	def calling_from_here():
		seshat.info("Hello world")
		seshat.warn("This is not going to end well...")
		seshat.error("Told you so")
	calling_from_here()


class D:

	def __init__(self):
		self.name = "Caya Sama Lu"
		self.age = 12
		self.address = "5th Avenue"

	def info(self):
		return self.name


def test_tracker(T):

	def c(d):
		return d.info()

	def b(d):
		x = d.name
		p = c(d)

	def a(d):
		d.age = 10
		b(d)

	import proxy

	d = D()
	d = seshat.track(d, "dman")
	a(d)
	print(type(d))