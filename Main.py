import sqlite3
from NF3decomp import *  
# Author: Daniel Zhou
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
    print (Row_List)

def Make_Numeric_Lookup(iterable):
    out = []
    
    for i in range(0, len(iterable) ):
        out.append( ( str(i+1) , iterable[i]) )

    return out
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
        usr_sel = FD_Tables_Table[ int(usr_sel)-1]
        
        Get_FD_Table_Info(conn,usr_sel)
def main():
    # Create Database Connection
    path = raw_input("Enter Database Path Or Leave Blank For Default: ")
    if path == "":
        conn = sqlite3.connect('Example.db')
    else:
        conn = sqlite3.connect(path)
   
    # Handle User Input
    while True:
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
                pass
            if User_input == "D":
                pass
            if User_input == "E":
                pass
        else:
            break
    # Handle Closure
    print ("Quit Selected")
    conn.commit()
    conn.close()
if __name__  == "__main__":
    main()