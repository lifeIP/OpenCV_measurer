import os,sys,re,importlib.machinery,types,json
from datetime import datetime, MINYEAR
from copy import deepcopy as dc

def redir():
	class red(object):
		def __init__(self):
			self.stream = None
			self.f = None
		def __enter__(self):
			self.stream = sys.stdout
			self.f = open(os.devnull, 'w')
			sys.stdout = self.f
			return self
		def __exit__(self,a=None,b=None,c=None):
			sys.stdout = self.stream
	return red()

def isinstances(object, *classes):
	output = False
	if isinstance(classes, list):
		for classe in classes:
			return output or isinstances(object, classe)
	return output or isinstance(object, classes)

styr = lambda some_string:string.of(some_string)

def of_list(obj: object, functor=lambda x:x) -> list:
	if isinstance(obj, list):
		return [functor(x) for x in obj]
	else:
		return [functor(obj)]

class backup_dir(object):
	#https://rszalski.github.io/magicmethods/ < Helpful Link
	def __init__(self, core_dir:str, prefix=5,enter:bool=False,clean:bool=False):
		self.core_dir = core_dir
		self.prefix=prefix
		self.enter=enter
		self.clean=clean
		self.start_dir = os.getcwd()
		self.used_dir = None

	def __floordiv__(self, other):return self.core_dir + "_" + str("*" if other == "*" else str(other).zfill(self.prefix))
	def __div__(self, other):return None if (other not in self) else str(self // other)
	def __truediv__(self,other):return self.__div__(other) #Python3 uses truediv and not div?? simply redirect to __div__
	def __invert__(self):top = int(self);os.mkdir(self.__floordiv__(top));top = str(self // top);return "".join(top)
	def __abs__(self):from glob import glob as re;output = re(self.core_dir+"_*");output.sort();return output
	def __contains__(self, other):return any([str(other).lower() in _dir.lower() for _dir in abs(self)])
	def __enter__(self, num=None):
		path = self // num if num is not None else ~self
		if self.enter:
			os.chdir(path)
			self.used_dir = path
		return path
	def __exit__(self,exception_type=None, exception_value=None, traceback=None):
		if self.enter:
			os.chdir(self.start_dir)
		if self.clean and self.used_dir:
			import shutil
			shutil.rmtree(self.used_dir)
		return
	def __len__(self):return abs(self).__len__()
	def __max__(self):return str(self.__abs__()[-1])
	def __min__(self):return str(self.__abs__()[0])
	def __int__(self):return 0 if len(self) == 0 else (+self + 1)
	def __pos__(self):return 0 if len(self) == 0 else int(self.__max__().replace(self.core_dir, "").replace("_",""))
	def __neg__(self):return 0 if len(self) == 0 else int(self.__min__().replace(self.core_dir, "").replace("_",""))


def levenshtein_distance(first, second, percent=True):
	if isinstance(first, list):
		first = "".join(first)
	if isinstance(second, list):
		second = "".join(second)

	"""Find the Levenshtein distance between two strings."""
	#https://stackoverflow.com/questions/3106994/algorithm-to-calculate-percent-difference-between-two-blobs-of-text
	if len(first) > len(second):
		first, second = second, first
	if len(second) == 0:
		return len(first)
	first_length = len(first) + 1
	second_length = len(second) + 1
	distance_matrix = [[0] * second_length for x in range(first_length)]
	for i in range(first_length):
		distance_matrix[i][0] = i
	for j in range(second_length):
		distance_matrix[0][j]=j
	for i in range(1, first_length):
		for j in range(1, second_length):
			deletion = distance_matrix[i-1][j] + 1
			insertion = distance_matrix[i][j-1] + 1
			substitution = distance_matrix[i-1][j-1]
			if first[i-1] != second[j-1]:
				substitution += 1
			distance_matrix[i][j] = min(insertion, deletion, substitution)

	diff_value = distance_matrix[first_length-1][second_length-1]
	if percent:
		return 100*(diff_value / float(max(len(first), len(second))))
	else:
		return diff_value

def exec(command, display=True, lines=False):
	return string.of(command).exec(display=display, lines=lines)

def imp(package, display=True, lines=False):
	return exec("{0} -m pip install --upgrade {1}".format(sys.executable, package), display=True, lines=False)

class string(str):
	def equals(self,*args, upper_check=False, lower_check=False):
		matches = [lambda x:x]
		if upper_check:
			matches += [lambda x:x.upper()]
		if lower_check:
			matches += [lambda x:x.lower()]
		
		for shiftr in matches:
			for arg in args:
				if shiftr(self) == shiftr(arg):
					return True
		return False

	def replace(self,x,y='', num_occurences=None):
		if num_occurences:
			return string(super().replace(x,y,num_occurences))
		else:
			return string(super().replace(x,y))

	def path_add(self, other):return string(os.path.join(self, string(other)))#;return self
	def __div__(self, other):return self.path_add(other)
	def __truediv__(self,other):return self.path_add(other) #Python3 uses truediv and not div?? simply redirect to __div__
	def __idiv__(self, other):self = string(self / string(other));return self
	def __rand__(self, other):return string(self + string(other))#;return self
	def __iand__(self, other):self = self & string(other);return self

	def rep(self,substring):
		self = self.replace(substring,'')
		return self

	def rep_surrounding(self, start_and_end, end=None):
		if self.startswith(start_and_end):
			self = string(self[len(start_and_end):])
		if (end and self.endswith(end)) or self.endswith(start_and_end):
			to_replace = end or start_and_end
			self = string(self[:-len(to_replace)])
		return self
	
	def rep_surroundings(self, *start_and_end):
		for arg in start_and_end:
			self = self.rep_surrounding(arg)
		return self

	def rreplace(self,x,y='', num_occurences=None):
		return string(y.join(self.rsplit(x,-1 if num_occurences is not None else num_occurences)))

	def reps(self,*args):
		for arg in args:
			self = self.rep(arg)
		return self

	def repsies(self,*args):
		for arg in args:
			self = self.rep(arg)
		return self

	def nquotes(self):
		return self.reps("'",'"', "`")

	def fixnulines(self):
		for nuline in ["\\\\n", "\\\n", "\\n"]:
			self = self.replace(nuline, "\n")
		return self

	def percent_diff(self, string, func=levenshtein_distance, use_percent=True):
		return func(self, string, use_percent)

	def rep_end(self, substring):
		if self.endswith(substring):
			self = string(self[:-1 * len(substring)])
		return self
	
	def repsies_end(self,*args):
		for arg in args:
			self = self.rep_end(arg)
		return self
	
	def rep_fromend(self, substring):
		#From https://stackoverflow.com/questions/3675318/how-to-replace-some-characters-from-the-end-of-a-string
		head, _sep, tail = self.rpartition(substring)
		self = string(head + tail)
		return self
	
	def repsies_fromend(self,*args):
		for arg in args:
			self = self.rep_fromend(arg)
		return self

	def exec(self, display=True, lines=False):
		import subprocess

		output_contents = ""
		if display:
			print(self)
		process = subprocess.Popen(self,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,bufsize=1,encoding='utf-8', universal_newlines=True, close_fds=True)
		while True:
			out = process.stdout.readline()
			if out == '' and process.poll() != None:
				break
			if out != '':
				if display:
					sys.stdout.write(out)
				output_contents += out
				sys.stdout.flush()
		
		if not lines:
			return string(output_contents)
		else:
			return lyst([string(x) for x in output_contents.split('\n') if not string(x).empty])

	@property
	def isvalidpy(self):
		import ast
		output = False
		try:
			ast.parse(str(self))
			output = True
		except:
			pass
		return output

	def eval(self):
		if self.isvalidpy:
			eval(self)

	@property
	def irregularstrip(self):
		#for arg in ['.','(',')','[',']','-',',','/','"',"'","’","#",]:
		#	self = self.rep(arg)
		self = string(re.sub(r'\W+', '', self))
		return self
	
	@property
	def deplete(self):
		self = self.trim.irregularstrip.trim
		if self.empty:
			self = None
		return self

	def ad(self, value):
		self = string(self + getattr(self, 'delim', "")  + value)
		return self

	def delim(self, value):
		self.delim = value

	def pre(self, value):
		self = string(value + getattr(self, 'delim', "")  + self)
		return self

	def pres(self, *args):
		for arg in args:
			self = self.pre(arg)
		return self

	def startswiths(self, *args):
		for arg in args:
			if self.startswith(arg):
				return True
		return False

	@property
	def trim(self):
		self = string(self.strip())
		if self == '':
			self = None
		return self

	@staticmethod
	def empty_values():
		return ['nan', 'none', 'null','n/a','na','non-applicable']

	@staticmethod
	def null_values():
		return string.empty_values() + ['']

	@property
	def empty(self):
		return any([
			exhaustive_equal(self,x) for x in string.null_values()
		]) or self == None

	@property
	def notempty(self):
		return not self.empty

	def format(self, numstyle='06'):
		return format(int(self),numstyle)

	def splitsies(self,*args,joiner=":"):
		output_list = []
		for splitter_itr, splitter in enumerate(args):
			if splitter_itr == 0:
				output_list = self.split(splitter)
			else:
				temp_list = string(joiner.join(output_list)).splitsies(splitter,joiner=joiner)
				output_list = []
				for temp_item in temp_list:
					for temp_split_item in temp_item.split(joiner):
						output_list.append(temp_split_item)

		return [string(x) for x in output_list]

	def tohash(self, hash_type='sha512', encoding='utf-8'):
		import hashlib
		return string(getattr(hashlib, hash_type)(self.encode(encoding)).hexdigest())

	def tobase64(self, encoding='utf-8', prefix=False):
		import base64
		return string(
			string("b64:" if prefix else "")
			+
			string(base64.b64encode(self.encode(encoding)).decode(encoding))
		)

	@staticmethod
	def frombase64(strang, encoding='utf-8'):
		import base64
		return string(base64.b64decode(strang.encode(encoding)).decode(encoding))

	@staticmethod
	def of(strung):
		if strung == None:
			strung = ""

		strung = str(strung)

		if strung.startswith('b64:'):
			return string.frombase64(strung.replace('b64:','',1))

		if strung.startswith('json:'):
			return strung.replace("json:",'',1)

		try:
			return string.frombase64(strung)
		except:
			pass

		return string(strung)

	def matches(self, regex:str, at_most:int=-1) -> bool:
		try:
			grps = [
				match.group() for idx,match in enumerate(regex.finditer(str(self)))
			]
			return (at_most > -1 and len(grps) <= at_most) or (at_most == -1 and len(grps) > 0)
		except Exception as e:
			print("Error grabbing regex: {0}".format(e))
			return False

	@property
	def isfile(self):
		return os.path.isfile(self)

	@property
	def isdir(self):
		return os.path.isdir(self)

	@property
	def file_name(self):
		file_name, file_ext = os.path.splitext(self)
		return os.path.basename(file_name)

	@property
	def filedir_name(self):
		file_name, file_ext = os.path.splitext(self)
		return file_name

	@property
	def ext(self):
		file_name, file_ext = os.path.splitext(self)
		return file_ext

	def aspy(self):
		#https://stackoverflow.com/questions/19009932/import-arbitrary-python-source-file-python-3-3#answer-19011259
		loader = importlib.machinery.SourceFileLoader(self.file_name, os.path.abspath(self))
		mod = types.ModuleType(loader.name)
		loader.exec_module(mod)
		return mod

	def progLangName(self, upper:bool=False):
		for rawName, cleanName in {
			"#":"Sharp",
			"+":"Plus",
			"*":"Asterik",
			".":"Dot",
			"-":"Dash",
			"_":"underscore",
			"/":"Slash",
			"\\":"Slash",
		}.items():
			self = self.replace(rawName, cleanName.upper() if upper else cleanName)

		return string(self)

	def deepClean(self, perma:bool=False):
		self = self.trim
		valid_kar = lambda kar: (ord('0') <= ord(kar) and ord(kar) <= ord('9')) or (ord('A') <= ord(kar) and ord(kar) <= ord('z'))
		output = None
		if perma:
			output = ''.join([i for i in self if valid_kar(i)])
		else:
			output = self.replace(' ', '\ ').replace('&','\&')

		self = string(string(output).trim)
		return self

	def shellCore(self):
		return string.of("import base64;exec(base64.b64decode('{cmd}').decode())".format(cmd=self.tobase64()))

	def shellPrep(self,prefix="/usr/bin/env python3 -c "):
		return string.of("{prefix} \"{cmd}\"".format(prefix=prefix, cmd=self.shellCore()))

	def shellAlias(self, aliasName="ALIASNAME", prefix="/usr/bin/env python3 -c"):
		return string.of(
			"""alias {0}='{1}'""".format(
				aliasName,
				self.shellPrep(prefix=prefix).replace("'","'\\''")
			)
		)

	def noNewLine(self, replaceWith=""):
		return string(self.replace("\r\n","\n").replace("\n", replaceWith))
	
	def escapeTab(self, replaceWith=""):
		return string(self.replace("\t",replaceWith))

def flatten_list(lyst: list) -> list:
	if not lyst:
		return []

	big_list = len(lyst) > 1
	if isinstance(lyst[0], list):
		return flatten_list(lyst[0]) + (big_list * flatten_list(lyst[1:]))
	else:
		return [lyst[0]] + (big_list * flatten_list(lyst[1:]))

def string_appliers():
	return [lambda x:x, lambda x:x.upper(), lambda x:x.lower(), lambda x:x.rstrip(), lambda x:x.lstrip(), lambda x:x.strip()]

def exhaustive_quoted():
	return [
		lambda value:value,
		lambda value:'"' + value + '"',
		lambda value:"'" + value + "'",
		lambda value:'"""' + value + '"""',
		lambda value:'"""' + value.replace('"""','\"\"\"') + '"""',
	]

def full_wrapping(*strings_to_wrap, extra_string_appliers=[], quoting_or_wrapping=[]):
	output = []
	for string_to_wrap in flatten_list(strings_to_wrap): 
		for string_applier in string_appliers() + extra_string_appliers:
			for wrappr in exhaustive_quoted() + quoting_or_wrapping:
				output += [
					wrappr(
						string_applier(
							string_to_wrap
						)
					)
				]
	return output

def exhaustive_equals(string_one, *string_two_provider):
	for string_to_check in flatten_list(string_two_provider):
		if exhaustive_equal(string_one, string_to_check):
			return True
	return False

def exhaustive_equal(string_one,string_two):
	for applier_one in string_appliers():
		for applier_two in string_appliers():
			if applier_one(string_one) == applier_two(string_two):
				return True
	return False

def exhaustive_string_contain(string_value, whole_string, empty_values=string.empty_values(), extra_string_appliers=[]):
	full_string_appliers = string_appliers() + extra_string_appliers
	for quote_appl in exhaustive_quoted():
		for string_applier in full_string_appliers:
			for null_value in empty_values:
				appliers = lambda x:quote_appl(string_applier(x))
				for x_applier in [lambda x:x, lambda x:appliers(x)]:
					for y_applier in [lambda x:x, lambda x:appliers(x)]:
						string_to_look_for = x_applier(string_value)+":"+y_applier(null_value)
						trim_whole_string = whole_string.strip().replace(" :", ":").replace(": ", ":")
						if string_to_look_for in trim_whole_string or string_to_look_for == trim_whole_string:
							return True
	return False

def obj_to_string(obj, prefix=None):
	import json
	output = string(
		json.dumps(
			obj
		)
	)
	if prefix:
		output = string(prefix + output)
	return output

def ofInteger(obj:any, cast:bool=True) -> int:
	obj = string.of(obj)
	is_int = False

	try:
		int(obj)
		is_int=True
	except:pass

	if is_int:
		return int(obj) if cast else True
	return None if cast else False

def bool_true_values():
	return ["true", 1, "1", "active", "high"]

def bool_false_values():
	return ["false", 0, "0", "inactive", "low"]

def bool_values():
	return bool_true_values() + bool_false_values()

def ofBoolean(obj:any, cast:bool=True) -> bool:
	obj = string.of(obj)

	active_values = bool_true_values()
	inactive_values = bool_false_values()

	if cast:
		if obj.empty:
			return False

		return obj.trim.lower() in active_values
	else:
		obj = obj.trim.lower()
		if obj in active_values:
			return True
		elif obj in inactive_values:
			return False
		else:
			return None


class integer(int):

	@staticmethod
	def of(obj:any, default:int = -1) -> int:
		obj = string.of(obj)

		if obj.empty:
			return integer(default)
		
		try:
			return int(obj)
		except:
			return integer(default)

class obj(object):
	#https://python-patterns.guide/gang-of-four/decorator-pattern/
	#https://stackoverflow.com/questions/1957780/how-to-override-the-operator-in-python
	def __init__(self, data:object):
		self.data = data

	@staticmethod
	def of(data):
		return obj.__init__(data=data)

	def __iter__(self):
		return self.data.__iter__()

	def __next__(self):
		return self.data.__next__()

	def __getattr__(self, attr):
		if attr in self.data.__dict__:
			return getattr(self.data, attr)
		return None

	def __delattr__(self, name):
		if name in self.data.__dict__:
			delattr(self.data.__dict__, name)

	def __getitem__(self, key):
		if isinstance(key, str):
			return self.data.__getattr__(key)
		return self.data.__getitem__(key)
	
	def __setitem__(self,key,value):
		if isinstance(key, str):
			return self.data.__getattr__(key)
		else:
			self.data.__setattr__(key,value)
	
	def __delitem__(self,key):
		if isinstance(key, str):
			return self.data.__getattr__(key)
		else:
			self.data.__delitem__(key)

	@staticmethod
	def isEmpty(obj:object):
		if obj is None:
			return True
		return string(obj).empty

	@staticmethod
	def safe_get_check(obj, attr, default=None):
		if hasattr(obj,attr) and getattr(obj,attr) is not None and getattr(obj,attr).strip().lower() not in ['','none','na']:
			return getattr(obj,attr)
		else:
			return default

from dateutil.parser import parse
import datetime

current_date = lambda:datetime.datetime.now(datetime.timezone.utc)
date_to_iso = lambda x:x.astimezone().isoformat('T')

utc_date_to_iso = lambda x:str(x.isoformat('T',timespec='microseconds'))
now_utc_to_iso = lambda:utc_date_to_iso(current_date())
utc_date_from_iso = lambda x:datetime.datetime.fromisoformat(x)

class timestamp(datetime.datetime):

	@staticmethod
	def of(obj:any):
		obj = string.of(obj)

		if obj.empty:
			return None

		try:
			return timestamp(datetime.fromisoformat(obj))
		except: pass

		try:
			return timestamp(parse(obj))
		except:
			return None

	def toIso(self):
		tz = self.astimezone()
		return string(tz.isoformat())

	@staticmethod
	def now():
		return datetime.datetime.now(datetime.timezone.utc)

try:
	import pandas as pd
	import sqlite3
	class frame(pd.DataFrame):
		def __init__(self,*args,**kwargs):
			super(frame,self).__init__(*args,**kwargs)

		@property
		def num_rows(self):return len(self.index)

		@property
		def num_cols(self):return len(self.kols)

		def dyff(self, obj, match_column='index'):
			if not isinstances(obj, frame, pd.DataFrame):
				print("The object it's being compared to is not a dataframe")
				return self

			if not isinstance(obj, frame):
				obj = frame(obj)

			shared_kolz = list(
				set(self.cols).intersection(set(obj.cols))
			)

			if len(shared_kolz) == 0:
				print("There are no shared columns")
				return self
			
			output = []
			for match_column_value in self[match_column].unique().tolist():
				t_output = {
					"MatchedColumn":match_column_value
				}
				has_any = False

				old_compared = self[self[match_column] == match_column_value]
				old_compared_num_rows = len(old_compared.index)
				old_compared_rows = frame(old_compared).arr()

				new_compared = obj[obj[match_column] == match_column_value]
				new_compared_num_rows = len(new_compared.index)
				new_compared_rows = frame(new_compared).arr()

				for shared_kol in shared_kolz:
					if old_compared_num_rows != 1 or new_compared_num_rows != 1:
						t_output["OLD:"+shared_kol] = "Num Columns Don't Match and/or not unique"
						t_output["NEW:"+shared_kol] = "Num Columns Don't Match and/or not unique"
					else:
						if str(old_compared_rows[0][shared_kol]) != str(new_compared_rows[0][shared_kol]):
							has_any = True

						t_output["OLD:"+shared_kol] = old_compared_rows[0][shared_kol]
						t_output["NEW:"+shared_kol] = new_compared_rows[0][shared_kol]

				if has_any:
					output += [t_output]

			return frame.from_arr(output) if len(output) > 0 else frame(pd.DataFrame())

		def col_exists(self,column):
			return column in self.columns

		def col_no_exists(self,column):
			return not(self.col_exists(column))

		def column_decimal_to_percent(self,column):
			self[column] = round(round(
				(self[column]),2
			) * 100,0).astype(int).astype(str).replace('.0','') + "%"
			return self

		def move_column(self, column, position):
			if self.col_no_exists(column):
				return
			colz = [col for col in self.columns if col != column]
			colz.insert(position, column)
			self = frame(self[colz])
			return self

		def rename_column(self, columnfrom, columnto):
			if self.col_no_exists(columnfrom):
				return
			self.rename(columns={columnfrom: columnto},inplace=True)
			return self

		def rename_columns(self, dyct):
			for key,value in dyct.items():
				if self.col_exists(key):
					self.rename(columns={key: value},inplace=True)
			return self

		def rename_value_in_column(self, column, fromname, fromto):
			if self.col_no_exists(column):
				return
			self[column] = self[column].str.replace(fromname, fromto)
			return self

		def drop_value_in_column(self, column, value,isstring=True):
			if self.col_no_exists(column):
				return
			self = frame(self.query("{0} != {1}".format(column, 
				"'" + value + "'" if isstring else value
			)))
			return self

		def cast_column(self, column, klass):
			if self.col_no_exists(column):
				return
			self[column] = self[column].astype(klass)
			return self
	
		def search(self, string):
			return frame(self.query(string))
	
		def arr(self):
			self_arr = self.to_dict('records')
			return self_arr

		def add_confusion_matrix(self,TP:str='TP',FP:str='FP',TN:str='TN',FN:str='FN', use_percent:bool=False):
			prep = lambda x:frame.percent(x, 100) if use_percent else x

			self['Precision_PPV'] = prep(self[TP]/(self[TP]+self[FP]))
			self['Recall'] = prep(self[TP]/(self[TP]+self[FN]))
			self['Specificity_TNR'] = prep(self[TN]/(self[TN]+self[FP]))
			self['FNR'] = prep(self[FN]/(self[FN]+self[TP]))
			self['FPR'] = prep(self[FP]/(self[FP]+self[TN]))
			self['FDR'] = prep(self[FP]/(self[FP]+self[TP]))
			self['FOR'] = prep(self[FN]/(self[FN]+self[TN]))
			self['TS'] = prep(self[TP]/(self[TP]+self[FP]+self[FN]))
			self['Accuracy'] = prep((self[TP]+self[TN])/(self[TP]+self[FP]+self[TN]+self[FN]))
			self['PPCR'] = prep((self[TP]+self[FP])/(self[TP]+self[FP]+self[TN]+self[FN]))
			self['F1'] = prep(2 * ((self['Precision_PPV'] * self['Recall'])/(self['Precision_PPV'] + self['Recall'])))

			return self
		
		def confusion_matrix_sum(self,TP:str='TP',FP:str='FP',TN:str='TN',FN:str='FN'):
			return (self[TP].sum() + self[TN].sum() + self[FN].sum())  

		def verify_confusion_matrix_bool(self,TotalCases:int=0,TP:str='TP',FP:str='FP',TN:str='TN',FN:str='FN'):
			return TotalCases == self.confusion_matrix_sum(TP=TP,FP=FP,TN=TN,FN=FN)

		def verify_confusion_matrix(self,TotalCases:int=0, TP:str='TP',FP:str='FP',TN:str='TN',FN:str='FN'):
			return "Total Cases {0} sum(TP,TN,FN)".format(
				"===" if self.verify_confusion_matrix_bool(TotalCases=TotalCases,TP=TP,FP=FP,TN=TN,FN=FN) else "=/="
			) 

		@staticmethod
		def percent(x,y):
			return ("{0:.2f}").format(100 * (x / float(y)))

		@staticmethod
		def from_csv(string):
			return frame(pd.read_csv(string, low_memory=False))

		@staticmethod
		def from_json(string):
			return frame(pd.read_json(string))

		@staticmethod
		def from_arr(arr):
			def dictionaries_to_pandas_helper(raw_dyct,deepcopy:bool=True):
				from copy import deepcopy as dc
				dyct = dc(raw_dyct) if deepcopy else raw_dyct
				for key in list(raw_dyct.keys()):
					dyct[key] = [dyct[key]]
				return pd.DataFrame.from_dict(dyct)

			return frame(
				pd.concat( list(map( dictionaries_to_pandas_helper,arr )), ignore_index=True )
			)
		
		@staticmethod
		def from_dbhub_query(query:str, dbhub_apikey, dbhub_owner, dbhub_name):
			from ephfile import ephfile
			import pydbhub.dbhub as dbhub
			with ephfile("config.ini") as eph:
				eph += f"""[dbhub]
	api_key = {dbhub_apikey}
	db_owner = {dbhub_owner}
	db_name = {dbhub_name}
			"""
				try:
					db = dbhub.Dbhub(config_file=eph())

					r, err = db.Query(
						dbhub_owner,
						dbhub_name,
						query
					)
					if err is not None:
						print(f"[ERROR] {err}")
						sys.exit(1)
					return frame.from_arr(r)
				except Exception as e:
					print(e)
		
		@staticmethod
		def from_dbhub_table(table_name, dbhub_apikey, dbhub_owner, dbhub_name):
			return frame.from_dbhub_query(
				'''
				SELECT * 
				FROM {0}
				'''.format(table_name),
				dbhub_apikey, dbhub_owner, dbhub_name
			)

		@staticmethod
		def export_datetime(object):
			if isinstance(object, datetime):
				return str(object.isoformat('T'))
			elif isinstance(object, str):
				from dateutil.parser import parse
				return framecase.export_datetime(parse(object))
			else:
				return None
			return None

		def to_raw_json(self):
			arrs = self.arr()
			for row in arrs:
				for key,value in row.items():
					from datetime import datetime
					if isinstance(value, datetime):
						value = frame.export_datetime(value)
			return json.dumps(arrs)

		@property
		def roll(self):
			class SubSeries(pd.Series):
				def setindexdata(self, index, data):
					self.custom__index = index
					self.custom__data = data
					return self

				def __setitem__(self, key, value):
					super(SubSeries, self).__setitem__(key, value)
					self.custom__data.at[self.custom__index,key] = value

			self.current_index=0
			while self.current_index < self.shape[0]:
				x = SubSeries(self.iloc[self.current_index]).setindexdata(self.current_index, self)

				self.current_index += 1
				yield x

		@property
		def readRoll(self):
			self.current_index=0
			while self.current_index < self.shape[0]:
				x = obj(self.iloc[self.current_index]).setindexdata(self.current_index, self)
				self.current_index += 1
				yield x

		def tobase64(self, encoding='utf-8'):
			import base64
			return "b64:"+base64.b64encode(self.to_json().encode(encoding)).decode(encoding)

		@staticmethod
		def frombase64(string, encoding='utf-8'):
			import base64
			return frame.from_json(base64.b64decode(string.replace("b64:","").encode(encoding)).decode(encoding))
		
		def quick_heatmap(self,cmap ='viridis',properties={'font-size': '20px'}):
			return self.style.background_gradient(cmap=cmap).set_properties(**properties) 

		def heatmap(self, columns,x_label='',y_label='',title=''):
			import seaborn as sns
			import matplotlib.pyplot as plt
			sns.set()
			SMALL_SIZE = 15
			MEDIUM_SIZE = 20
			BIGGER_SIZE = 25

			plt.rc('font', size=MEDIUM_SIZE)		  # controls default text sizes
			plt.rc('axes', titlesize=MEDIUM_SIZE)	 # fontsize of the axes title
			plt.rc('axes', labelsize=MEDIUM_SIZE)	# fontsize of the x and y labels
			plt.rc('xtick', labelsize=SMALL_SIZE)	# fontsize of the tick labels
			plt.rc('ytick', labelsize=SMALL_SIZE)	# fontsize of the tick labels
			plt.rc('legend', fontsize=SMALL_SIZE)	# legend fontsize
			plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

			temp_frame = self.copy()
			mask = temp_frame.columns.isin(columns)

			temp_frame.loc[:, ~mask] = 0
			vmin, vmax = 0,0

			for col in columns:
				vmax = max(vmax, self[col].max())

			sns.heatmap(temp_frame, annot=True, fmt="d", vmin=vmin, vmax=vmax, cmap="Blues")
			plt.xlabel(x_label) 
			plt.ylabel(y_label) 

			# displaying the title
			plt.title(title)
			plt.rcParams["figure.figsize"] = (40,30)

			if False:
				plt.savefig(
					'get_size.png',
					format='png',
					dpi=height/fig.get_size_inches()[1]
				)
			plt.show()
		
		@property
		def df(self):
			from copy import deepcopy as dc
			return pd.DataFrame(dc(self))
		
		def dup(self):
			from copy import deepcopy as dc
			return frame(dc(self))
		
		@staticmethod
		def dupof(dataframe):
			from copy import deepcopy as dc
			return frame(dc(dataframe))
		
		@property
		def dummies(self):
			return pd.get_dummies(data = self)

		@property
		def kolz(self):
			return lyst(self.columns.tolist())

		@property
		def kols(self):return self.kolz

		@property
		def cols(self):return self.kolz
		
		def enumerate_kol(self):
			for column_itr, column in enumerate(self.kolz):
				self.rename_column(column, str(column_itr)+"_"+column)
			return self

		@staticmethod
		def from_sqlite(file="out.sqlite", table_name="main"):
			output = pd.DataFrame()

			if not os.path.exists(file):
				return frame(output)
			db_tables = frame.of_sheet_names(file)
			if table_name not in db_tables:
				print("table {0} not within [{1}]".format(table_name, ', '.join(db_tables)))
				return frame(output)

			connection = sqlite3.connect(file)
			current_cursor = connection.cursor()
			output = pd.read_sql_query("SELECT * FROM {0}".format(table_name), connection)
			current_cursor = None
			connection.close()

			return frame(output)

		def to_sqlite(self, file="out.sqlite", table_name="default", append=False):
			import sqlite3 as sql
			conn = sql.connect(file)
			try:
				cursor = conn.cursor()
				self.to_sql(name=table_name, con=conn, if_exists="append" if append else "replace", index=False)
			except Exception as e:
				print(e)
			finally:
				conn.close()
			return file

		def to_sqlcreate(self, file="out.sql", name="temp", number_columnz = False, every_x_rows=-1):
			working = self.dup()

			if number_columnz:
				working.enumerate_kol()
				#columns = working.kolz
				#for column_itr, column in enumerate(columns):
				#	working.rename_column(column, str(column_itr)+"_"+column)

			if every_x_rows is None or every_x_rows == -1:
				#https://stackoverflow.com/questions/31071952/generate-sql-statements-from-a-pandas-dataframe
				with open(file,"w+") as writer:
					writer.write(pd.io.sql.get_schema(working.reset_index(), name))
					writer.write("\n\n")
					for index, row in working.iterrows():
						writer.write('INSERT INTO '+name+' ('+ str(', '.join(working.columns))+ ') VALUES '+ str(tuple(row.values)))
						writer.write("\n")
			else:
				#https://stackoverflow.com/questions/31071952/generate-sql-statements-from-a-pandas-dataframe
				ktr = 0
				nu_file = file.replace('.sql', '_' + str(ktr).zfill(5) + '.sql')

				with open(nu_file,"w+") as writer:
					writer.write(pd.io.sql.get_schema(working.reset_index(), name))
					writer.write("\n\n")

				for index, row in working.iterrows():
					if index % every_x_rows == 0:
						ktr = ktr + 1
						nu_file = file.replace('.sql', '_' + str(ktr).zfill(5) + '.sql')

					with open(nu_file,"a+" if os.path.exists(nu_file) else "w+") as writer:
						writer.write("\n")
						writer.write('INSERT INTO '+name+' ('+ str(', '.join(working.columns))+ ') VALUES '+ str(tuple(row.values)))
						writer.write("\n")

		def ofQuery(self, query:str):
			return frame(self.query(query))

		@staticmethod
		def of_sheet_names(obj_or_file_path):
			output = []
			if isinstance(obj_or_file_path, str) and os.path.exists(obj_or_file_path):
				from pathlib import Path
				ext = Path(obj_or_file_path).suffix
				if ext == ".excel" or ext == ".xlsx":
					from openpyxl import load_workbook
					for sheet_name in load_workbook(obj_or_file_path, read_only=True, keep_links=False).sheetnames:
						output += [sheet_name]
				elif ext == ".sqlite":
					connection = sqlite3.connect(obj_or_file_path)
					current_cursor = connection.cursor()
					current_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table';")
					for name in current_cursor.fetchall():
						output += [name[0]]
					current_cursor = None
					connection.close()
			return output

		@staticmethod
		def of(obj_or_file_path, sheet_name:str="Sheet1", dbhub_apikey=None, dbhub_owner=None, dbhub_name=None):
			data = None
			#return frame(pd.read_csv(file_path, low_memory=False))
			if isinstance(obj_or_file_path, pd.DataFrame):
				return frame(obj_or_file_path)
			elif isinstance(obj_or_file_path, str):
				if os.path.exists(obj_or_file_path):
					from pathlib import Path
					ext = Path(obj_or_file_path).suffix

					if ext == ".pkl":
						data = frame(pd.read_pickle(obj_or_file_path, low_memory=False))
					elif ext == ".csv":
						data = frame.from_csv(obj_or_file_path)
					elif ext == ".tsv":
						data = pd.read_csv(obj_or_file_path,seperator='	')
					elif ext == ".excel" or ext == ".xlsx":
						data = frame(pd.read_excel(obj_or_file_path, sheet_name=sheet_name, engine="openpyxl"))
					elif ext == ".json":
						data = frame.from_json(obj_or_file_path)
					elif ext == ".sqlite":
						data = frame.from_sqlite(obj_or_file_path, table_name=sheet_name)
					elif ext == ".dbhub":
						data = frame.from_dbhub_table(obj_or_file_path, dbhub_apikey=dbhub_apikey, dbhub_owner=dbhub_owner, dbhub_name=dbhub_name)
				elif obj_or_file_path.startswith("b64:"):
					data = frame.frombase64(obj_or_file_path.replace("b64:",""))
				elif obj_or_file_path.startswith("https://"):
					data = frame(pd.read_html(obj_or_file_path))
			elif isinstance(obj_or_file_path, list):
				data = frame.from_arr(obj_or_file_path)

			return data

		def write_to(self, file_path, sheet_name:str="Sheet1"):
			if isinstance(file_path, str):
				from pathlib import Path
				ext = Path(file_path).suffix

				if ext == ".pkl":
					self.to_pickle(file_path)
				elif ext == ".csv":
					self.to_csv(file_path)
				elif ext == ".excel":
					with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
						self.to_excel(writer, sheet_name=sheet_name, startrow=1, header=True)
				elif ext == ".xlsx":
					with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
						self.to_excel(writer, sheet_name=sheet_name, startrow=1, header=True)
				elif ext == ".json":
					self.to_json(file_path)
				elif ext == ".sqlite":
					self.to_sqlite(file_path, table_name=sheet_name)

			return

		def add_dyct(self, dyct):
			if not isinstance(dyct, dict):
				print("Object passed in needs to be a dictionary")
				return
			
			if list(dyct.keys()) != self.kolz:
				print("The dictionary keys must match the columns of the dataframe")
				return

			self = frame.from_arr(self.arr() + [dyct])
			return self

		def on(self, string):
			from copy import deepcopy as dc
			self = frame(dc(self).query(string))
			return self

	class framecase(object):
		#https://rszalski.github.io/magicmethods/
		def __init__(self, file_out_to=None, base_name="unknown_data"):
			self.dyct = {}
			self.base = base_name
			self.file_out_to = file_out_to

		def add_frame(self, obj, obj_name=None):
			frame_to_add = None
			if isinstance(obj, frame):
				frame_to_add = dc(obj)
			elif isinstance(obj, pd.DataFrame):
				frame_to_add = frame(obj)
			elif isinstance(obj, str):
				try:
					output = frame.of(obj, sheet_name=obj_name)
					if output is not None:
						frame_to_add = output
				except:pass

			if frame_to_add is not None:
				self.dyct[obj_name or self.__nu_name()] = frame_to_add

		def __iadd__(self, other):
			self.add_frame(other)
			return self

		def arx(self):
			for key,value in self.items():
				value.write_to(file_out_to, sheet_name=key)
		
		def query(self, query_string:str):
			output = {}
			for key,value in self.items():
				sub_output = None
				try:sub_output=frame(value.query(query_string))
				except:pass
				output[key] = sub_output
			return output
		
		@staticmethod
		def of(obj):
			output = framecase()
			if isinstance(obj, str) and os.path.exists(obj):
				from pathlib import Path
				ext = Path(obj).suffix
				if ext == ".excel" or ext == ".xlsx":
					for sheet_name in frame.of_sheet_names(obj):
						output.add_frame(obj, sheet_name)
				elif ext == ".json":
					contents = None
					with open(obj, "r") as reader:
						contents = json.load(reader)
					output._set_from_raw(contents)
				elif ext == ".sqlite":
					for sheet_name in frame.of_sheet_names(obj):
						output.add_frame(obj, sheet_name)
			return output

		def write_to(self, override_writeto:str=None):
			for key,value in self.items():
				value.write_to(override_writeto, sheet_name = key)
			return

		def _set_from_raw(self, dyct:dict):
			for key,value in dyct.items():
				output[key] = value

		@staticmethod
		def from_raw(self, dyct:dict):
			output = framecase()
			output._set_from_raw(dyct)
			return output
		def to_raw(self, b64:bool=False):return {key:(value.to_raw_json() if not b64 else value.tobase64()) for  key,value in self.dyct.items()}
		#Overridden methods
		def __str__(self):return json.dumps(self.to_raw())
		def __len__(self):return len(self.dyct.values())
		def __getitem__(self, key):return pd.DataFrame() if key not in self else self.dyct[key]
		def __setitem__(self, key, value):self.add_frame(obj=value, obj_name=key)
		def __delitem__(self, key):del self.dyct[key]
		def __iter__(self):return iter(self.dyct.values())
		def __reversed__(self):return reversed(self.dyct.values())
		def __contains__(self, item):return item in self.dyct.keys()
		#def __getattr__(self, name):return self[name]
		#def __setattr__(self, name, value):self[name] = value
		#def __delattr__(self, name): del self[name]
		def __int__(self):return len(self)
		def __enter__(self):return self
		def __exit__(self, exception_type=None,exception_value=None,traceback=None):self.arx()
		def __deepcopy__(self, memodict={}): return dc(self.dyct)
		def items(self):return list(self.dyct.items())
		def keys(self):return list(self.dyct.keys())
		def values(self):return list(self.dyct.values())
		def __getstate__(self):return self.to_raw()
		def __setstate__(self, state):self._set_from_raw(state)


		def equal_cols(self):
			sample_kolz = self.values()[0].kolz
			for value in self.values():
				if len(list( set(value.kolz)-set(sample_kolz)  )) > 0:
					return False
			return True

		def __nu_name(self):
			name = base_name
			itr = 0
			while str(name+"_"+str(itr)) in self.dyct:
				itr += 1
			return str(name+"_"+str(itr))

	from abc import ABC, abstractmethod
	from copy import deepcopy as dc
	class framepipe(ABC):
		def __init__(self, columns_needed=[], break_flow:bool=False):
			super().__init__()
			self.columns_needed = [x for x in columns_needed if x is not None]
			self.break_flow = break_flow
			self.iterated = None
			self.__etherial = None

		def rows(self, frame_or_dataframe):
			frame_or_dataframe_arr = frame_or_dataframe.arr()
			for row in frame_or_dataframe_arr:
				yield row
			self.iterated = frame.from_arr(frame_or_dataframe_arr)

		@abstractmethod
		def apply(self, frame_or_dataframe):
			pass

		def __call__(self, frame_or_dataframe):
			my_frame = None
			if isinstance(frame_or_dataframe, frame):
				my_frame = frame_or_dataframe
			elif isinstance(frame_or_dataframe, pd.DataFrame):
				my_frame = frame(frame_or_dataframe)
			else:
				msg = "Frame isn't either a dataframe or mystring.frame"
				if self.break_flow:
					raise Exception(msg)
				print(msg)
				return frame_or_dataframe

			if self.columns_needed != []:
				frame_kols = list(my_frame.kols)
				for column_needed in self.columns_needed:
					if column_needed not in frame_kols:
						msg = "Frame doesn't at least include the column: {0}".format(column_needed)
						if self.break_flow:
							raise Exception(msg)
						print(msg)
						return my_frame

			return self.apply(my_frame)

		def __getitem__(self, item):
			return self.etherial()[item]
		def __setitem__(self, item, value):
			self.etherial()[item] = value
		def __delitem__(self, item):
			del self.etherial()[item]
		def __contains__(self, item):
			return item in self.etherial()

		def etherial(self, hugg_repo=None, *foils):
			if self.__etherial is None:
				class py_util(object):
					def __init__(self, repo, foils):
						self.repo = repo
						self.foils = foils
					def __enter__(self):
						import json, os, sys
						output = {}
						for foil in self.foils:
							output[foil.replace('.py','').replace('/','.')] = self.repo.impor(foil, delete=True)
							output[foil.replace('.py','')] = self.repo.impor(foil, delete=True)
							#Double up incase using slashy boys
						return output
					def __exit__(self, a=None,b=None,c=None):
						import json, os, sys
						for foil in self.foils:
							if os.path.exists(foil):
								os.remove(foil)
					def __getitem__(self, item):
						import json, os, sys
						return None if item not in self else json.loads(os.environ[item])
					def __setitem__(self, item, value):
						import json, os, sys
						os.environ[item] = json.dumps(value)
					def __delitem__(self, item):
						import json, os, sys
						if item in self:
							del os.environ[item]
					def __contains__(self, item):
						return item in os.environ
				self.__etherial = py_util(repo=hugg_repo, foils=foils)
			return self.__etherial
except:
	pass

class lyst(list):
	def __init__(self,*args,**kwargs):
		super(lyst,self).__init__(*args,**kwargs)
	
	def trims(self, filterlambda=None):
		to_drop = []

		for x_itr,x in enumerate(self):
			if(
				(filterlambda != None and filterlambda(x))
				or
				(filterlambda == None and x == None)
			):
				to_drop += [x_itr]
		
		to_drop.reverse()
		for to_drop_itr in to_drop:
			self.pop(to_drop_itr)
		
		return self
	
	@property
	def length(self):
		return len(self)

	def roll(self, kast=None,filter_lambda = None):
		for item in self:
			if kast:
				item = kast(item)

			if filter_lambda==None or filter_lambda(item):
				yield item
	
	def joins(self,on=","):
		return on.join(self)
	
	def execs(self):
		return [string(x).exec() for x in self if isinstance(x, str)]

	@staticmethod
	def of(obj: object, functor=None) -> list:
		if not functor or functor is None:
			def functor(x):
				return x

		if isinstance(obj, list):
			return lyst([functor(x) for x in obj])
		else:
			return lyst([functor(obj)])

import multiprocessing
import time
class timeout(object):
	"""
	with mystring.timeout(6*10, func=callr.pull) as exe:
	if not exe.timeout:
		resultr = exe.output
	"""
	#https://stackoverflow.com/questions/10415028/how-to-get-the-return-value-of-a-function-passed-to-multiprocessing-process/10415215#10415215
	#https://stackoverflow.com/questions/492519/timeout-on-a-function-call
	def __init__(self, number_of_seconds, func, *args, **kwargs):
		self.queue = multiprocessing.Queue()
		self.num_sec = number_of_seconds
		self.proc = multiprocessing.Process(target=self._wrapper, args=[func, self.queue, args, kwargs])
		
		self.exe = False
		self.timeout = False
		self.output = None

	@staticmethod
	def _wrapper(func, queue, args, kwargs):
		ret = func(*args, **kwargs)
		queue.put(ret)
	
	def run(self):
		if not self.exe and self.proc is not None:
			print("Processing")
			self.exe = True
			self.proc.start()
			self.proc.join(self.num_sec)
			self.timeout = self.proc.is_alive()

			if self.timeout:
				# or self.proc.terminate() for safely killing thread
				self.proc.kill()
				self.proc.join()
			else:
				self.output = self.queue.get()
				try:
					import pandas as pd
					if isinstance(self.output, pd.DataFrame):
						self.output = frame(self.output)
				except:
					pass
				if isinstance(self.output, list):
					self.output = lyst(self.output)
				elif isinstance(self.output, str):
					self.output = string(self.output)
	
	def __enter__(self):
		self.run()
		return self
	
	def __exit__(self, type, value, traceback):
		return

import hashlib,base64,json
from fileinput import FileInput as finput
class foil(object):
	def __init__(self, path, preload=False):
		self.path = path
		if preload:
			with open(self.path, "r") as reader:
				self._content = lyst([string(x) for x in reader.readlines()])
		else:
			self._content = lyst([])

	@property
	def impor(self):

		import_name = str(self.path.split('/')[-1]).replace('.py','')
		#https://stackoverflow.com/questions/19009932/import-arbitrary-python-source-file-python-3-3#answer-19011259
		loader = importlib.machinery.SourceFileLoader(import_name, os.path.abspath(self.path))
		mod = types.ModuleType(loader.name)
		loader.exec_module(mod)

		return mod

	def __enter__(self, append=False):
		self._content = lyst([])
		yield finput(self.path, inplace=True)
	
	def __exit__(self,type, value, traceback):
		return
	
	@property
	def content(self):
		if self._content.length == 0:
			with open(self.path, "r") as reader:
				self._content = lyst([string(x) for x in reader.readlines()])
		return self._content
	
	def reload(self):
		self._content = lyst([])
		return self.content

	def hash_content(self,hashtype=hashlib.sha512, encoding="utf-8"):
		hashing = hashtype()
		with open(self.path, 'rb') as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hashing.update(chunk)
		return hashing.hexdigest()

	def b64_content(self, encoding="utf-8"):
		return base64.b64encode(self.content.joins("\n").encode(encoding)).decode(encoding)

	def tob64(self):
		newName = self.path+".64"
		with open(self.path, 'rb') as fin, open(newName, 'w') as fout:
			base64.encode(fin, fout)
		return newName

	@staticmethod
	def fromb64(path):
		newName = path.replace(".64",'')
		with open(self.path, 'rb') as fin, open(newName, 'w') as fout:
			base64.decode(fin, fout)
		return foil(newName)

	def structured(self):
		return str(json.dumps({
			'header':False,
			'file':self.path,
			'hash':self.hash_content(),
			'base64':self.b64_content()
		}))

	@property
	def linez(self):
		from fileinput import FileInput as finput
		yield finput(self.path, inplace=True, backup=False)
	
	@staticmethod
	def is_bin(foil):
		#https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
		textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
		is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
		return is_binary_string(open(foil, 'rb').read(1024))

	@staticmethod
	def loadJson(foil):
		if not foil.isJson(foil):
			return None
		import json
		with open(foil, 'r') as reader:
			return json.load(reader)

	@staticmethod
	def getExt(path:str):
		import pathlib
		return pathlib.Path(path).suffix

	@staticmethod
	def isJson(path:str):
		return any([foil.getExt(path) == x for x in [
			".json"
		]])

	@staticmethod
	def isJava(path:str):
		return any([foil.getExt(path) == x for x in [
			".java",".jsp"
		]])

	@staticmethod
	def isScala(path:str):
		return any([foil.getExt(path) == x for x in [
			".scala"
		]])

	@staticmethod
	def isPython(path:str):
		return any([foil.getExt(path) == x for x in [
			".py",".pyi"
		]])

	@staticmethod
	def isRust(path:str):
		return any([foil.getExt(path) == x for x in [
			".rs"
		]])

	@staticmethod
	def isJs(path:str):
		return any([foil.getExt(path) == x for x in [
			".js"
		]])

class foldentre(object):
	def __init__(self,new_path:str,ini_path:str = os.path.abspath(os.curdir), clean:bool=True):
		self.ini_path = ini_path
		self.new_path = new_path
		self.clean = clean
		self.path = None
		self.__set_strings()

	def __set_strings(self):
		self.ini_path = string.of(self.ini_path)
		self.new_path = string.of(self.new_path)
		self.clean = string.of(self.clean)

	def __enter__(self):
		if not os.path.exists(self.new_path):
			os.mkdir(self.new_path)
		os.chdir(self.new_path)
		self.path = self.new_path
		self.__set_strings()
		return self.path
	
	def __exit__(self,type=None, value=None, traceback=None):
		os.chdir(self.ini_path)
		if self.clean:
			import shutil
			shutil.rmtree(self.new_path)
		self.path = self.ini_path
		self.__set_strings()
		return self

def from_b64(contents,file=None):
	string_contents = string.frombase64(contents)
	if file:
		with open(file,'w+') as writer:
			writer.write(string_contents)
		return foil(file)
	else:
		return string_contents

class wrapper:
	def __init__(self, *, typing, default, b64=False):
		self._typing = typing
		self._default = default
		self._b64=b64

	def __set_name__(self, owner, name):
		self._name = "_" + name

	def __get__(self, obj, type):
		if obj is None:
			return self._default

		value = self.typing(getattr(obj, self._name, self._default))
		if self._b64:
			value = mystring.from_b64(value)
		return value

	def __set__(self, obj, value):
		if not obj.isEmpty(value):
			if self._b64:
				value = string(value).tobase64()
			setattr(obj, self._name, self._typing(value))

	def __type__(self):
		return self._typing

import datetime,time
class Timer(object):
	def __init__(self):
		self.start_datetime = None
		self.end_datetime = None
	
	def __enter__(self):
		self.start_datetime = datetime.datetime.now(datetime.timezone.utc)
		self.start_datetime = self.start_datetime.replace(tzinfo=datetime.timezone.utc).timestamp()
		return self
	
	def __exit__(self,type, value, traceback):
		self.end_datetime = datetime.datetime.now(datetime.timezone.utc)
		self.end_datetime = self.end_datetime.replace(tzinfo=datetime.timezone.utc).timestamp()
		return self
	
	def __dict__(self):
		return {
			"start_datetime_UTC": self.start_datetime,
			"end_datetime_UTC": self.end_datetime,
			"durationS": (self.end_datetime - self.start_datetime).seconds,
			"durationMS": (self.end_datetime - self.start_datetime).microseconds,
		}

import threading, queue, time
from typing import Dict, List, Union, Callable
class MyThread(threading.Thread):
	def __init__(self, func, threadLimiter=None, group=None, target=None, name=None,args=(), kwargs=None):
		super(MyThread,self).__init__(group=group, target=target, name=name)
		self.func = func
		self.threadLimiter = threadLimiter
		self.args = args
		self.kwargs = kwargs
		return

	def run(self): 
		if self.threadLimiter:
			self.threadLimiter.acquire() 
		try: 
			self.func() 
		finally: 
			if self.threadLimiter:
				self.threadLimiter.release() 

class MyThreads(object):
	def __init__(self, num_threads):
		self.num_threads = num_threads
		self.threadLimiter = threading.BoundedSemaphore(self.num_threads)
		self.threads = queue.Queue()

	def __iadd__(self, obj: Union[Callable]):
		if isinstance(obj, Callable):
			obj = MyThread(obj, self.threadLimiter)
		
		if not isinstance(obj, MyThread):
			print("Cannot add a-none function")
			return self
		
		self.threads.put(obj)
		obj.start()
		return self
	
	@property
	def complete(self):
		if self.threads.qsize() > 0:
			for tread in iter(self.threads.get, None):
				if tread != None and tread.isAlive():
					return False
		return True

	def wait_until_done(self, printout=False):
		if printout:
			print("[",end='',flush=True)

		while not self.complete:
			time.sleep(1)
			if printout:
				print(".",end='',flush=True)

		if printout:
			print("]",flush=True)

class session(object):
	def __init__(self, lock, onCall=None, onOpen=None, onClose=None):
		self.lock = lock
		self.onCall = onCall
		self.onOpen = onOpen
		self.onClose = onClose

	def __enter__(self):
		self.lock.acquire()

		if self.onOpen:
			self.onOpen()

		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.onClose:
			self.onClose()

		self.lock.release()

	def __call__(self, string: object):
		if self.onCall:
			return self.onCall(string)
		else:
			return string

class shelving(object):
	@staticmethod
	def load(path):
		output = None
		import shelve
		try:
			with shelve.open(path) as db:
				output = db
		except Exception as e:
			print("Could not shelf {0} due to exception {1}".format(key, str(e)))
		return output

	@staticmethod
	def save(path):
		import shelve
		with shelve.open(path, 'n+') as shelf:
			for key in dir():
				try:
					shelf[key] = globals()[key]
				except TypeError:
					print("Could not shelf {0} due to type error".format(key))
				except Exception as e:
					print("Could not shelf {0} due to exception {1}".format(key, str(e)))
		return path

def walker(path:str=".", eachFile=None, eachFolder=None):
	import os
	for root, dirnames, fnames in os.walk(path):
		for dirname in dirnames:
			if eachFolder is not None:
				eachFolder(os.path.join(root,dirname))

		for fname in fnames:
			if eachFile is not None:
				eachFile(os.path.join(root,fname))

def my_ip():
	import socket
	ip=None;s=None
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		ip = str(s.getsockname()[0])
		s.close()
	except:
		pass
	finally:
		if s != None:
			try:
				s.close()
			except:
				pass
	return ip


def gh_file_to_raw_url(self, owner_repo, filepath,branch:str="main"):
	return string.of("https://raw.githubusercontent.com") / owner_repo / branch / filepath

try:
	import requests, pause
	class gh_api_status(object):
		def __init__(self):
			self.cur_status = None
			self.now = None
			self.resetdate = None

		@property
		def status(self):
			# curl -I https://api.github.com/users/octocat|grep x-ratelimit-reset
			self.cur_status, self.now = requests.get("https://api.github.com/users/octocat").headers, datetime.datetime.now()
			return {
				'Reset': self.cur_status['X-RateLimit-Reset'],
				'Used': self.cur_status['X-RateLimit-Used'],
				'Total': self.cur_status['X-RateLimit-Limit'],
				'Remaining': self.cur_status['X-RateLimit-Remaining'],
				'RemainingDate':datetime.datetime.fromtimestamp(int(self.cur_status['X-RateLimit-Reset'])),
				'WaitFor':datetime.datetime.fromtimestamp(int(self.cur_status['X-RateLimit-Reset'])) - self.now,
				'WaitForSec':(datetime.datetime.fromtimestamp(int(self.cur_status['X-RateLimit-Reset'])) - self.now).seconds,
				'WaitForNow':lambda :(datetime.datetime.fromtimestamp(int(self.cur_status['X-RateLimit-Reset'])) - datetime.datetime.now()).seconds,
			}

		@property
		def timing(self):
			import time
			if not hasattr(self, 'remaining') or self.remaining is None:
				stats = self.status
				print(stats)
				self.remaining = int(stats['Remaining'])
				self.wait_until = stats['WaitForNow']
				self.resetdate = stats['RemainingDate']
				self.timing
			elif self.remaining >= 10:
				self.remaining = self.remaining - 1
			else:
				print("Waiting until: {0}".format(self.resetdate))
				pause.until(self.resetdate)
				delattr(self, 'remaining')
				delattr(self, 'wait_until')
			return
except: pass


try:
	import waybackpy

	class gh_url(object):
		def __init__(self,url,token=None,verify=True,commit=None,tag=None):
			self.url = string(url)
			self.token = string(token)
			self.verify = verify
			self.stringurl = string(url)
			self.commit = string(commit)
			self.tag = string(tag)
			self.api_watch = gh_api_status()

			url = string(url).repsies('https://','http://','github.com/').repsies_end('.git')
			self.owner, self.reponame = url.split("/")
			self.owner, self.reponame = string(self.owner), string(self.reponame)

			if not self.tag.empty:
				self.stringurl = string(self.stringurl + "<b>" + self.tag)
			if not self.commit.empty:
				self.stringurl = string(self.stringurl + "<#>" + self.commit)

		@property
		def dir(self):
			return string(self.reponame+"/")

		@property
		def core(self):
			return string("{0}/{1}".format(self.owner, self.reponame))

		@property
		def furl(self):
			return string("https://github.com/{0}".format(self.core))

		def filewebinfo(self, filepath, lineno=None):
			baseurl = "https://github.com/{0}/blob/{1}/{2}".format(self.core, self.commit,filepath.replace(str(self.reponame) + "/", '', 1))
			if lineno:
				baseurl += "#L{0}".format(int(lineno))

			return string(baseurl)

		#Transforming this into a cloning function
		def __call__(self,return_error=False, json=True, baserun=False,headers = {}):
			string("git clone {0}".format(self.furl)).exec(True)

			if self.commit:
				with foldentre()(self.dir):
					string("git checkout {0}".format(self.commit)).exec(True)
			return self.dir

		def __enter__(self):
			self()
			return self

		def __exit__(self, exc_type, exc_val, exc_tb):
			string("yes|rm -r {0}".format(self.dir)).exec(True)
			return self

		def find_asset(self,asset_check=None, accept="application/vnd.github+json", print_info=False):
			if asset_check is None:
				asset_check = lambda x:False

			def req(string, verify=self.verify, accept=accept, auth=self.token, print_info=print_info):
				try:
					output = requests.get(string, verify=verify, headers={
						"Accept": accept,
						"Authorization":"Bearer {}".format(auth)
					})
					if print_info:
						print(output)
					return output.json()
				except Exception as e:
					if print_info:
						print(e)
					pass

			latest_version = req("https://api.github.com/repos/{0}/releases/latest".format(self.core))
			release_information = req(latest_version['url'])
			for asset in release_information['assets']:
				if asset_check(asset['name']):
					return asset
			return None

		def download_asset(self, url, save_path, chunk_size=128, accept="application/octet-stream"):
			r = requests.get(url, stream=True, verify=self.verify, headers={
				"Accept": accept,
				"Authorization":"Bearer {0}".format(self.token)
			})
			with open(save_path, 'wb') as fd:
				for chunk in r.iter_content(chunk_size=chunk_size):
					fd.write(chunk)
			return save_path

		def get_date_from_commit_url(self, accept="application/vnd.github+json"):
			req = requests.get(self.furl, headers={
				"Accept": accept,
				"Authorization":"Bearer {0}".format(self.token)
			}).json()
			return datetime.datetime.strptime(req['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")

		def get_commits_of_repo(self, from_date=None, to_date=None, accept="application/vnd.github+json"):
			params = []
			if from_date:
				params += ["since={0}".format(from_date)]
			if from_date:
				params += ["until={0}".format(to_date)]
			request_url = "https://api.github.com/repos/{0}/commits?{1}".format(self.core, '&'.join(params))
			req = requests.get(request_url, headers={
				"Accept": accept,
				"Authorization":"Bearer {0}".format(self.token)
			})
			return req.json()

		@property
		def zip_url(self):
			url_builder = self.furl + "/archive"
			if self.commit:
				url_builder += f"/{self.commit}.zip"
			elif self.tag:
				url_builder += f"/{self.tag}.zip"

			self.zip_url_base = url_builder
			return self.zip_url_base

		@property
		def static_webarchive_save_url(self):
			return string("https://web.archive.org/save/" + self.zip_url)

		def save_on_webarchive(self, user_agent="Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"):
			"""
			https://github.com/akamhy/waybackpy#save-api-aka-savepagenow
			"""
			from waybackpy import WaybackMachineSaveAPI
			save_url = WaybackMachineSaveAPI(
				self.zip_url,
				user_agent
			).save()
			return save_url
		
		def commits_by_date(self, _to_,_from_=None,verify=True):
			if _from_ is None:
				new_to = _to_ - timedelta(days=2)
				return nicepy("{}/commits?until={}".format(self.furl,_to_.strftime("%Y-%m-%dT%H:%M:00")))['data']
			else:
				return nicepy("{}/commits?since={}&until={}".format(self.furl,_from_.strftime("%Y-%m-%dT%H:%M:%S"),_to_.strftime("%Y-%m-%dT%H:%M:%S")))['data']
except:
	pass

try:
	import requests
	class package_aide(object):
		def __init__(self, package, extras_strings=None, install_live=False):
			self.package = package
			self.install_live = install_live
			self.extras_strings = extras_strings

		@property
		def has(self):
			try:
				__import__(self.package)
			except:
				print("Package {0} is not installed".format(self.package))
				self.update

		@property
		def update(self):
			if self.install_live:
				import os,sys;os.system("{0} -m pip install --upgrade {1}{2}".format(
					sys.executable, self.package,
					"[{0}]".format(self.extras_strings) if self.extras_strings else ""
				))

		@property
		def latest(self):
			self.has
			output = None
			try:
				output = requests.get("https://pypi.org/pypi/{0}/json".format(self.package)).json()['info']['version']
			except:pass
			return output

		@property
		def current(self):
			self.has
			output = None
			try:
				import importlib.metadata
				output = importlib.metadata.version(self.package)
			except:pass
			return output
	
		def at_latest(self):
			return self.current == self.latest

		def update_to_latest(self):
			if not self.at_latest():
				self.update
			return self.latest
except:pass


class pretty(object):
	def __init__(self):
		pass

	@staticmethod
	def num_prune(number):
		if isinstance(number, str):
			while number.startswith("0") and number != "0":
				number = number[1:]
		return int(number)

	@staticmethod
	def num_flate(number, fill_to_length=2):
		number = str(number)
		while len(number) < fill_to_length:
			number = "0"+number
		return number

	@staticmethod
	def num_commas(number):
		return "{:,}".format(number)

	@staticmethod
	def percent(number):
		return "%{0}".format(round(number*100,2))