def to_utf8(string):
	ss = string
	try:
		ss = string.decode('UTF-8').encode('UTF-8')
	except:
		try:
			ss = string.decode('GB18030').encode('UTF-8')
		except:
			try:
				encoding_info = chardet.detect(string)
				charset = encoding_info['encoding']
				if charset.lower() == 'ascii':
					ss = string.encode('UTF-8')
				else:
					ss = string.decode(charset).encode('UTF-8')
			except:
				return ss
	return ss
