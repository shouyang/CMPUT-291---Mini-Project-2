import sqlite3
from NF3decomp import *  
from closure import *
from bcnfdecomp import *
# Author: Daniel Zhou, Jordan Vogel, Christopher Saunders
# November 2016

#===============================================================================
# Helper Functions

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
        
def dependPreserving(FD1, FD2):
    rValue = ''
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


    if check and check2:
        #print("F1 and F2 are equivalent!")
        rValue = "Decomposition was dependency preserving"
    else:
        #print("F1 and F2 are not equivalent!")
        rValue = "Decomposition was not dependency preserving"

        
        
    return rValue
            
        
def Get_Tables_List(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT name,sql FROM SQLITE_MASTER WHERE name NOT LIKE '%FDS%';")
    
    tables = []
    for i in cursor:
        tables.append( (str(i[0]) , str(i[1])) ) #n Unicode Strings hence Conversion
    
    return tables
def Get_FD_Tables_List(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT name,sql FROM SQLITE_MASTER WHERE name LIKE '%FDS%';")
    
    tables = []
    for i in cursor:
        tables.append( (str(i[0]) , str(i[1])) ) #n Unicode Strings hence Conversion
    
    return tables

def Get_FD_Table_Info(conn,table_name):
    cursor = conn.cursor()
    
    # Get Information From Table
    query = "SELECT * FROM vtable"
    query = query.replace("vtable", table_name)
    
    cursor.execute(query)
    # Convert Table Information Into Deomposition Format
    Row_List = cursor.fetchall()

    # Modify Elements In Row_List To Be In Same Format As The 3NF Decomp Requirements.
    for i in range(0, len(Row_List) ):
        Row = Row_List[i]
        
        # Convert From Unicode for Safety
        LHS = str(Row[0])
        RHS = str(Row[1])
        
        # Replace Commas
        LHS = LHS.replace(",","")
        RHS = RHS.replace(",","")
        
        # Replace Element In List
        Row = (LHS,RHS)
        
        Row_List[i] = Row

    return Row_List

def Make_Numeric_Lookup(iterable):
    out = []
    
    for i in range(0, len(iterable) ):
        out.append( ( str(i+1) , iterable[i]) )

    return out

def Partition_Table(conn,FDependencies, Base_Table):
    '''
    Function Implementation
    
    This function takes a connection, a set of functional dependencies and a base table 
    and makes partitions of the base table into a partition per functional dependency. 
    
    
    '''
    # Adjust Base_Table Schema To Prepare For Conversion
    Base_Table_Name = Base_Table[0]
    Base_Table_SQL  = Base_Table[1]
    
    Base_Table_SQL = Base_Table_SQL.replace("CREATE TABLE","")
    Base_Table_SQL = Base_Table_SQL.replace("(","")
    Base_Table_SQL = Base_Table_SQL.replace(")","")
    Base_Table_SQL = Base_Table_SQL.replace(Base_Table_Name,"")
    
    Base_Table_SQL = Base_Table_SQL.strip()
    Base_Table_SQL = Base_Table_SQL.split()
    
    '''
    Notes
    
    At this point Base_Table_Name is the name of the Table To Be Converted
    
    Base_Table_SQL is a list where one element is the Varable Name, the following
    is the Variable Type. As such there are 2*n number of variables in this list.
    
    '''
    
    # Generate Queries To Perform Decomposition 
    
    
    # Create Table Name Template
    Partition_Name = "Output" + Base_Table_Name
    Partition_Name = Partition_Name.replace("Input","") # This converts the input table name into the Output Table Name
    Partition_Name = Partition_Name + "_" + "VarTemp"   # Safest Choice(?)
    
    '''
    For each Functional Dependency Create Three Queries
    1. Partition Table Storing Partitioned Data, this creates and imports data to the new table.
    2. FDS Table
    3. Insert Entry Query For FDS Table
    '''
    for Dependency in FDependencies:
         
        # LHS & RHS - Used To Determine Variable Set, Also Used To Fill Output_FDS Table
        LHS = Dependency[0]
        RHS = Dependency[1]
        
        # Variables - Used To Change Temp Table Name and Variables For Partition
        Variables = LHS + RHS 
        
        # Make Paritioning Query
        Partition_Query = "CREATE TABLE " + Partition_Name + " AS SELECT vVariables FROM " + Base_Table_Name
        Partition_Query = Partition_Query.replace("VarTemp",Variables)
                
        Variables = list(Variables)
        Variables = ",".join(Variables)
                        
        Partition_Query = Partition_Query.replace("vVariables",Variables) + ";"
        
        # Make Associated FDS Table Query
        Variables = LHS + RHS
        
        Partition_FDS_Query = "CREATE TABLE " + Partition_Name
        Partition_FDS_Query = Partition_FDS_Query.replace("VarTemp",Variables)
        Partition_FDS_Query = Partition_FDS_Query + " (LHS TEXT,RHS TEXT);"
        Partition_FDS_Query = Partition_FDS_Query.replace("Output_", "Output_FDS_")        
        
        # Make FDS Table Insert Query
        Partition_FDS_Insert_Query = Partition_FDS_Query.replace("CREATE TABLE ","INSERT INTO ") # Note This is done on Partition_FDS_Query
        Partition_FDS_Insert_Query = Partition_FDS_Insert_Query.replace(" (LHS TEXT,RHS TEXT);"," VALUES (vLHS,vRHS);")
        Partition_FDS_Insert_Query = Partition_FDS_Insert_Query.replace("vLHS", "'" + LHS + "'")
        Partition_FDS_Insert_Query = Partition_FDS_Insert_Query.replace("vRHS", "'" + RHS + "'")
        
        # Print For User's Sake
        print("A Partition Set:")
        print(Partition_Query)
        print(Partition_FDS_Query)
        print(Partition_FDS_Insert_Query)
        print("Partition End - ! There May Be More Partitions!")
        print("\n")
        
        # Execute Queries
        conn.execute(Partition_Query)
        conn.commit()
        
        conn.execute(Partition_FDS_Query)
        conn.commit()

        conn.execute(Partition_FDS_Insert_Query)
        conn.commit()
        
        print ("Decompsition Finished")
    return 1
#===============================================================================
# Main Functions

def function_A(conn):
    # Get Tables From DB, make corressponding list of values.
    List_Values, List_Tables = zip(*Make_Numeric_Lookup(Get_Tables_List(conn)))
    
    # Display mapping
    print ("Tables: ")
    for i in range(0, len(List_Values) ):
        print ( List_Values[i] + " - " + List_Tables[i][0] )
    
    # Get User selection
    isQuit,User_Selection = Get_Checked_Input("Select An Option: ", List_Values, "Q")
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
        return
def function_B(conn):
    # Display List Of Decomposable Tables
    Tables    = Get_Tables_List(conn)
    FD_Tables = Get_FD_Tables_List(conn)
    
    # Remove SQL Create Table Portion of The FD_Tables List
    FD_Tables_ = []
    
    for row in FD_Tables:
        FD_Tables_.append( row[0] )
        
    FD_Tables = Make_Numeric_Lookup( FD_Tables_ )
    
    # Display Tables
    print ("Tables")
    for row in Tables:
        print (row[0])
    
    # Display Decomposable Tables
    print ("Tables containing decomposition information.")
    for row in FD_Tables:
        print ( row[0] + " - " + row[1] )
        
    # Get User Input
    FD_Tables_Number,FD_Tables_Table = zip(*FD_Tables)

    isQuit,usr_sel = Get_Checked_Input("Select Number: ", FD_Tables_Number, "Q")

    if isQuit == True: # Quit Option Selected
        return
    else: # Go Get Decomposition Information
        usr_sel_FD = FD_Tables_Table[ int(usr_sel)-1]
        
        Row_List = Get_FD_Table_Info(conn,usr_sel_FD)
        
        print ("Database Dependencies: ")
        print (Row_List)
    
        # Push Row_List To Get Module Function For Decomposition
        NF3_Dependencies  = NF3decomp(Row_List)
        
        print ("NF3 Dependencies: ")
        print(NF3_Dependencies)
        
        # Ask For Input Before Performing Decomposition
        isQuit,X = Get_Checked_Input("Perform Decomposition (Y/N)?",["Y"],"N")
        
        if isQuit:
            return
        else:
            usr_sel_Table = Tables[ int(usr_sel)-1 ]
            Partition_Table(conn,NF3_Dependencies,usr_sel_Table)
            return
        
def function_C(conn):
    # Display List Of Decomposable Tables
    Tables    = Get_Tables_List(conn)
    FD_Tables = Get_FD_Tables_List(conn)
    
    # Remove SQL Create Table Portion of The FD_Tables List
    FD_Tables_ = []
    
    for row in FD_Tables:
        FD_Tables_.append( row[0] )
        
    FD_Tables = Make_Numeric_Lookup( FD_Tables_ )
    
    # Display Tables
    print ("Tables")
    for row in Tables:
        print (row[0])
    
    # Display Decomposable Tables
    print ("Tables containing decomposition information.")
    for row in FD_Tables:
        print ( row[0] + " - " + row[1] )
        
    # Get User Input
    FD_Tables_Number,FD_Tables_Table = zip(*FD_Tables)

    isQuit,usr_sel = Get_Checked_Input("Select Number: ", FD_Tables_Number, "Q")

    if isQuit == True: # Quit Option Selected
        return
    else: # Go Get Decomposition Information
        usr_sel_FD = FD_Tables_Table[ int(usr_sel)-1]
        
        Row_List = Get_FD_Table_Info(conn,usr_sel_FD)
        
        print ("Database Dependencies: ")
        print (Row_List)
        
        formatList = ''
        for i in range(len(Row_List)):
            formatList += Row_List[i][0]+'-'+Row_List[i][1]+','
        formatList = formatList[:-1] 
        rList = []
        
        dList = ''
        for r in range(len(Row_List)):
            rList.append(Row_List[r][0])
            rList.append(Row_List[r][1])
            
        newSet = ','.join(set(list(''.join(rList))))
        
        #print(newSet)
        #print(rList)
    
        # Push Row_List To Get Module Function For Decomposition
        BCNFdepends  = BCNFdecomp(formatList,newSet)
        
        print ("BCNF Dependencies: ")
        print(BCNFdepends)
        
        # Ask For Input Before Performing Decomposition
        isQuit,X = Get_Checked_Input("Perform Decomposition (Y/N)?",["Y"],"N")
        
        if isQuit:
            return
        else:
            usr_sel_Table = Tables[ int(usr_sel)-1 ]
            Partition_Table(conn,BCNFdepends,usr_sel_Table)
            print(dependPreserving(BCNFdepends,Row_List))
            return
        
    
    
        
                
    
def function_D(conn):
    cursor = conn.cursor()
    FD_Tables = Get_FD_Tables_List(conn)
    usr_attributes = ""
    usr_FD = []
    
    # Remove SQL Create Table Portion of The FD_Tables List
    FD_Tables_ = []
    
    for row in FD_Tables:
        FD_Tables_.append( row[0] )
        
    FD_Tables = Make_Numeric_Lookup( FD_Tables_ )    
    
    FD_Tables_Number,FD_Tables = zip(*FD_Tables)
    
    while True:
    
        print ("Currently Functional Dependencies (X,Y) = X -> Y: ")
        for FD in usr_FD:
            print(FD)
    
        print ("Currently Selected Attributes: ")
        print (usr_attributes)
    
        print("\n\n")
        
        print ("Options")
        print ("0 - Add Attributes")
        print ("1 - Add Functional Dependencies By Table")
        print ("2 - Add Functional Dependencies By Input")
        print ("3 - Compute Attribute Closure")
        
        isQuit,usr_option = Get_Checked_Input("",  ["0","1","2","3"] ,"Q")
    
        # Option 0
        if usr_option == "0":
            while True:
                usr_input_attribute = raw_input("Add Attribute: ")    
                
                print ( usr_input_attribute )
                
                usr_input_confirm = raw_input("Confirm (Y/N)?")
                if usr_input_confirm == "Y":
                    usr_attributes = usr_attributes + usr_input_attribute
                    break
                else:
                    break    
                
        # Option 1
        elif usr_option == "1":
            # Print all FD Tables In Database
            for i in range(0, len(FD_Tables) ):
                print ( FD_Tables_Number[i] + " - " +  FD_Tables[i])
    
            # Allow user to select one of these tables based upon the displayed value.
            isQuit,usr_table_index = Get_Checked_Input("Select Table By Number: ",FD_Tables_Number,"Q")
            usr_table = FD_Tables[ int(usr_table_index) - 1] # Index Conversion
            
            if isQuit:
                break
            
            # Get FD's From Table
            query = "SELECT * FROM vTable"
            query = query.replace("vTable", usr_table)
            
            cursor.execute(query)
            
            for row in cursor:
                LHS = str(row[0])
                RHS = str(row[1])
                
                LHS = LHS.replace(",","")
                RHS = RHS.replace(",","")
            
                usr_FD.append( (LHS,RHS) )
            
        # Option 2
        elif usr_option == "2":
            while True:
                usr_input_LHS = raw_input("Add FD LHS: ")    
                usr_input_RHS = raw_input("Add FD RHS: ")
                
                print ( (usr_input_LHS,usr_input_RHS) )
                
                usr_input_confirm = raw_input("Confirm (Y/N)?")
                if usr_input_confirm == "Y":
                    usr_FD.append( (usr_input_LHS,usr_input_RHS) )
                    break
                else:
                    break            
        # Option 3
        elif usr_option == "3":
            closure_set = closure.closure(usr_attributes,usr_FD)
            
            closure_string = "".join(closure_set)
            
            print(closure_string)
            
            return 1
        
        elif isQuit == True:
            return 1
        
def function_E(conn):
   #Gets first set of FD's "FD1"
    running = True
    FD1 = []
    FD2 = []
    print("====================")
    print("Please enter a list of tables for FD1: (Enter blank to continue)")
    while running:
        User_input = raw_input()
        if User_input == '' and FD1:
            running = False
        elif User_input == '' and not FD1:
        	print("Please enter at least one table")
        if running and not User_input == '':
                cursor = conn.cursor()
                temp = []
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
    running = True
    print("====================")
    print("Please enter a list of tables for FD2: (Enter blank to continue)")
    while running:
        User_input = raw_input()
        if User_input == '' and FD2:
            running = False
        elif User_input == '' and not FD2:
        	print("Please enter at least one table")
        if running and not User_input == '':
            cursor = conn.cursor()
            
            temp = []
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
    print("====================")
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

    
    




        
def main():
    # Create Database Connection
    path = raw_input("Enter Database Path Or Leave Blank For Default: ")
    if path == "":
        conn = sqlite3.connect('Example.db')
    else:
        conn = sqlite3.connect(path)
   
    # Handle User Input
    while True:
        print("\n\n")
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
                function_A(conn)
            if User_input == "B":
                function_B(conn)
            if User_input == "C":
                function_C(conn)
            if User_input == "D":
                function_D(conn)
            if User_input == "E":
                function_E(conn)
        else:
            break
    # Handle Closure
    print ("Quit Selected")
    conn.commit()
    conn.close()
if __name__  == "__main__":
    main()