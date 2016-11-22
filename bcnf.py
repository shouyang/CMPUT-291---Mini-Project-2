def BCNF(fds,attrs):
    yesBCNF = []
    notBCNF = []
    for i in fds:
        if i[0].isSuperKey():
            yesBCNF.append(i)
        else:
            notBCNF.append(i)
            BCNF(notBCNF,attrs)
    return yesBCNF

def isSuperKey(FD):
    
    
    
    
    pass

SAVED
cursor = conn.cursor()
cursor.execute("SELECT * FROM Input_FDs_R1;")
testInput = cursor.fetchall()
stringInput = []
cursor.execute("PRAGMA table_info(Input_R1)")
relation = cursor.fetchall()
rList = ''
for r in range(len(relation)):
    rList += (str(relation[r][1][0])+',')

for i in range(len(testInput)):
    left = str(testInput[i][0])
    right = str(testInput[i][1])
    left = left.replace(',','')
    right = right.replace(',','')
    stringInput.append([left, right])
    
RHS = []
for i in stringInput:
    for j in i[1]:
        if j not in RHS:
            RHS.append(j)
            
LHS = []
for i in stringInput:
    for j in i[0]:
        if j not in LHS:
            LHS.append(j)
            
formatList = ''
for i in range(len(stringInput)):
    formatList += stringInput[i][0]+'-'+stringInput[i][1]+','
formatList = formatList[:-1]
    
bcnfList = doBCNFDecomp(formatList, rList)
print("Resulting FDs from BCNF decomposition")
    
print(bcnfList)
    
#print(formatList)
#rString = ''.join(rList)
#rint(rList)
#print(rString)   
#print(stringInput)
            