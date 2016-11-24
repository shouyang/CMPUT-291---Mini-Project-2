
from sets import Set
class FD:
	def __init__(self, A, B):
		self.A = Set(A)	
		self.B = Set(B)
		self.total = Set(A+B)

	def closure(self, fd):
		if (fd.A.issubset(self.total) and not fd.B.issubset(self.total)):
			self.total = self.total.union(fd.B)
			return True

class Table:
	def __init__(self, Attrs, FDs):
		self.Attrs = Attrs
		self.FDs = FDs

	def findIllDF(self):
		for FD1 in self.FDs:
			for FD2 in self.FDs:
				if (FD1.closure(FD2)):
					FD2 = FD1
			if (not FD1.total.issuperset(self.Attrs)):
				return FD1
		return 0
	
	def decompose(self, df):
		result = []
		attrs1 = df.total
		dfs1 = self.project(attrs1)
		result.append(Table(attrs1,dfs1))
		attrs2 = self.Attrs.difference(attrs1).union(df.A)
		dfs2 = self.project(attrs2)
		result.append(Table(attrs2, dfs2))
		return result

	def project(self, attrs):
		result = [];
		for FD in self.FDs:
			if (FD.A.issubset(attrs) and FD.B.issubset(attrs)):
				result.append(FD)
		return result
		
def getFDs(fds):
	result = []
	for i in fds:
		temp = i.split('-')
		result.append(FD(list(temp[0]), list(temp[1])))
	return result

def formFDs(fds):
	result = ""
	for i in range(len(fds)):
		result += "".join(list(fds[i].A)) + "-" + "".join(list(fds[i].B)) ;
		if (i != len(fds)-1):
			result += ", "
	return result

def BCNFdecomp(fds,attrs):
#if __name__ == "__main__":
	attrs = 'A,B,C,D,E,F,G,H,K'
	attrs = Set(attrs.split(','))
	fds = 'ABH-CK,A-D,C-E,BGH-F,F-AD,E-F,BH-E'
	fds = fds.split(',')
	
	fds = getFDs(fds)
	result = []
	tables = [Table(attrs, fds)]
	final = []
	illDF = tables[0].findIllDF();
	if (illDF == 0):
		pass
	else:
		isBCNF = False
		while(not isBCNF):
			isBCNF = True
			for table in tables:
				illDF = table.findIllDF();
				if (illDF != 0):
					isBCNF = False
					tables += table.decompose(illDF)
					tables.remove(table)
					for i in tables:
						temp = formFDs(i.FDs)
						#print(temp,'temp')
						result.append(temp)
					
					
					break
	#print(result)
	for i in reversed(result):
		final.append(i)
		if i == '':
			final.remove(i)
			break
	finalList = []
	for i in range(len(final)):
		newStr = tuple(final[i].split('-'))
		finalList.append((newStr))
	#print(final)
	#print(finalList)
	return (finalList)