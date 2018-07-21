import os
import sys
import inspect
from datetime import datetime
import pprint
from functools import wraps, partial
from threading import Lock
from . import proxy


class Sesat:

	def __init__(self):
		self._home_ = os.getenv('HOME')
		self._lock_ = Lock()
		pp = pprint.PrettyPrinter(stream=self)
		self._print_ = pp.pprint
		self.record = partial(self._record_, self)  # decorator
		self.write = partial(self._write_, self)  # called by pp
		self._writeline_ = partial(self._write_, self, indent=0)
		self._file_ = None
		self._trackers_ = {}

	def home(self, path):
		self._home_ = path
		self._file_ = open(os.path.join(self._home_, "seshat.log"), 'a')

	def track(self, obj, name):
		if name not in self._trackers_:
			proxied = proxy.Proxy(obj)
			self._trackers_[name] = proxied
			return proxied
		else:
			return obj

	def _log_function_(self, module_name, func_name):
		message = u'\U000026A1 {} [{}] << {} >>\n'.format(datetime.now(), module_name, func_name)
		self._writeline_(message)

	def _log_(self, caller_module, caller, message, symbol):
		message = '{} {} [{}] << {} >> : {}\n'.format(symbol, datetime.now(), caller_module, caller, message)
		self._lock_.acquire()
		self._writeline_(message)
		self._lock_.release()

	def info(self, message):
		caller = inspect.stack()[1][3]
		frm = inspect.stack()[1]
		caller_module = inspect.getmodule(frm[0]).__name__
		self._log_(caller_module, caller, message, u'\U0001F4C4')

	def warn(self, message):
		caller = inspect.stack()[1][3]
		frm = inspect.stack()[1]
		caller_module = inspect.getmodule(frm[0]).__name__
		self._log_(caller_module, caller, message, u'\U0001F4A3')

	def error(self, message):
		caller = inspect.stack()[1][3]
		frm = inspect.stack()[1]
		caller_module = inspect.getmodule(frm[0]).__name__
		self._log_(caller_module, caller, message, u'\U0001F494')

	@staticmethod
	def _write_(self, stream, indent=1):
		spacer = '\t' * indent
		sys.stdout.write(spacer + stream)
		if self._file_ is not None:
			self._file_.write(spacer + stream)

	@staticmethod
	def _record_(self, func):
		frm = inspect.stack()[1]
		caller_module = inspect.getmodule(frm[0])
		func_name = func.__name__

		@wraps(func)
		def interceptor(*args, **kwargs):
			self._lock_.acquire()
			self._log_function_(caller_module.__name__, func_name)
			if args:
				self._writeline_("args:\n")
				self._print_(args)
			if kwargs:
				self._writeline_("kwargs:\n")
				self._print_(kwargs)
			_return_ = (func(*args, **kwargs))
			if _return_:
				self._writeline_("return:\n")
				self._print_(_return_)
			self._lock_.release()
			return _return_
		return interceptor

sesat = Sesat()