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
            pass
    # Handle Closure
    print ("Quit Selected")
    pass
if __name__  == "__main__":
    main()