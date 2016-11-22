import sqlite3

# Author: Daniel Zhou
# November 2016



def Get_Checked_Input(Prompt, Accepted_Values, QuitOption):
    while True:
        user_input = raw_input(Prompt)
        if user_input in Accepted_Values:
            return (False,user_input)
        elif user_input == QuitOption:
            return (True,0)
        else:
            print ( "Choice Invalid - Choice is case sensitive, " + QuitOption + " To Quit" )
            print ( "Options: ")
            print ( " ".join(Accepted_Values) )
            continue
        
def Get_Tables_List(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT name,sql FROM SQLITE_MASTER WHERE name NOT LIKE '%FDS%';")
    
    tables = []
    for i in cursor:
        tables.append( (str(i[0]) , str(i[1])) ) #n Unicode Strings hence Conversion
    
    return tables

def Make_Numeric_Lookup(iterable):
    out = []
    
    for i in range(0, len(iterable) ):
        out.append( ( str(i+1) , iterable[i]) )

    return out

def closure(R,F): #R should be the LHS of whatever F you start with
    old = set(R)
    count = 0
    while True: # Used to ensure an encompassing search
        for i in F:
            LHS = set(i[0])
            RHS = set(i[1])
            if LHS.issubset(old) and not RHS.issubset(old):
                old = old.union(RHS)
                count = 0
            else:
                count += 1
        if count > 1*len(F): # By setting count = 0 and breaking once count is higher than the length we ensure that each addition can be compared to each other element.
            break
    return old # old is a set, this set is the elements entailed from R

def removeComma(string):
    string = string.replace(',', '')
    return string
def main():
    # Create Database Connection
    path = raw_input("Enter Database Path Or Leave Blank For Default: ")
    if path == "":
        conn = sqlite3.connect('Example.db')
    else:
        conn = sqlite3.connect(path)
    # Handle User Input
    print("Options")
    print("A - Read About Relation")
    print("B - Perform  3NF Decomposition on a Relation")
    print("C - Perform BCNF Decomposition on a Relation")
    print("D - Select Relation and Determine Attribute Closure")
    print("E - Determine if two Functional Dependencies are Equal")
    print("Q - Quit")
    
    isQuit, User_input = Get_Checked_Input("Select An Option: ", ["A","B","C","D","E"], "Q")
    print("\n\n")
    
    if not ( isQuit ):
        if User_input == "A":
            # Get Tables From DB, make corressponding list of values.
            List_Values, List_Tables = zip(*Make_Numeric_Lookup(Get_Tables_List(conn)))
            
            # Display mapping
            print ("Tables: ")
            for i in range(0, len(List_Values) ):
                print ( List_Values[i] + " - " + List_Tables[i][0] )
            # Get User selection
            isQuit_,User_Selection = Get_Checked_Input("Select An Option: ", List_Values, "Q")
            if (isQuit ):
                return
            else:
                # User_Selection -> (Name,Schema)
                User_Selection =  List_Tables[ int(User_Selection) - 1 ]
                print(User_Selection[1])
                # Sel_FD_Table Table Name Adjustment 
                Sel_FD_Table = User_Selection[0].replace("_","_FDs_")
                # Functional Dependencies 
                print("Functional Dependencies")
                for row in conn.execute("SELECT * FROM ?".replace("?",Sel_FD_Table) ):
                    print ( str(row[0]) + "->" + str(row[1]) )
        if User_input == "B":
            pass
        if User_input == "C":
            pass
        if User_input == "D":
            pass
        if User_input == "E":
            #Gets first set of FD's "FD1"
            User_input = raw_input("Please enter the name of the table containing the first set of FDs(F1): ")
            cursor = conn.cursor()
            running = True
            temp = []
            FD1 = []
            while not temp:
                cursor.execute("SELECT * FROM %s;" %(User_input))
                for i in cursor:
                    temp.append(i)
                for i in range(len(temp)):
                    left = str(temp[i][0])
                    right = str(temp[i][1])
                    left = left.replace(',','')
                    right = right.replace(',','')
                    FD1.append((left,right))


            #Gets second set of FD's "FD2"
            User_input = raw_input("Please enter the name of the table containing the second set of FDs(F2): ")
            cursor = conn.cursor()
            running = True
            temp = []
            FD2 = []
            while not temp: #To try to loop until a good input is found (NOT WORKING)
                cursor.execute("SELECT * FROM %s;" %(User_input))
                for i in cursor:
                    temp.append(i)
                for i in range(len(temp)):
                    left = str(temp[i][0])
                    right = str(temp[i][1])
                    left = left.replace(',','')
                    right = right.replace(',','')
                    FD2.append((left,right))

                        
            #Meat of the program: Actually checks shit

            #Part 1, Checking whether all FDs of FD1 are present in FD2
            for i in range(len(FD1)):
                FDclosure = closure(FD1[i][0], FD2)
                check = True
                for x in range(len(FD1[i][0])):
                    if not (FD1[i][0][x] in FDclosure): #Iterates through the left hand string
                        check = False

                for x in range(len(FD1[i][1])): #Iterates through the right hand string
                    if not (FD1[i][1][x] in FDclosure):
                        check = False

            if check:
                print("All FDs of F1 are present in F2")
            else:
                print("Not all FDs of F1 are present in F2")


            #Part 2, Checking whether all FDs of FD2 are present in FD1
            for i in range(len(FD2)):
                FDclosure = closure(FD2[i][0], FD1)#AM HERE
                check2 = True
                for x in range(len(FD2[i][0])):
                    if not (FD2[i][0][x] in FDclosure): #Iterates through the left hand string
                        check2 = False

                for x in range(len(FD2[i][1])): #Iterates through the right hand string
                    if not (FD2[i][1][x] in FDclosure):
                        check2 = False
            if check2:
                print("All FDs of F2 are present in F1")
            else:
                print("Not all FDs of F2 are present in F1")

            if check and check2:
                print("F1 and F2 are equivalent!")
            else:
                print("F1 and F2 are not equivalent!")

                
                

            pass
    # Handle Closure
    print ("Quit Selected")
    pass
if __name__  == "__main__":
    main()

