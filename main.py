import time
import csv

# options for menus
main_options = ["Explore Parties", "Explore Constituencies", "Explore MPs", "View Statistics", "Exit"]
party_options = ["View MPs in a Party", "View Total Votes of a Party", "View Party Votes as Percentage of Total Votes", "Back to Main Menu"]
con_options = ["View Constituencies in a Region", "View Valid Votes for a Constituency", "View Constituency Votes as a Precentage of Total Votes", "Back to Main Menu"]
mps_options = ["View MP Votes by Name", "List by Party", "List by Region", "Back to Main Menu"]
stats_options = ["View Average Votes per Constituency", "View Total MPs", "View Total Votes Cast", "Save Statistics to File", "Back to Main Menu"]

# lists to store names
mps_list = []

# party class
class Party:
    def __init__(self, name, region):
        self.name = name
        self.region = region
        self.desc = {"Name": self.name, "Region": self.region}
        
    def __str__(self):
        # return a string represntation of the party
        return self.desc["Name"] + " MP, in " + self.desc["Region"] + " Region"

    def get_name(self):
        return self.desc["Name"].lower()

# constituency class
class Constituency:
    def __init__(self, name, region, valid_votes, total_votes, result):
        self.name = name
        self.region = region
        self.valid_votes = valid_votes
        self.total_votes = total_votes
        self.result = result
        self.desc = {"Name": self.name, "Region": self.region, "Valid Votes": self.valid_votes, "Total Votes": self.total_votes, "Result": self.result}
 
    def __str__(self):
        # return a string represntation of the constituency
        return self.desc["Name"] + " Constituency, Region: " + self.desc["Region"] + " Region, Result: " + self.desc["Result"]

    def valid_vote_precentage(self):
        return (self.valid_votes / self.total_votes) * 100

    def get_votes(self):
        return self.desc["Valid Votes"]

    def get_region(self):
        return self.desc["Region"].lower()

    def get_name(self):
        return self.desc["Name"].lower()

# mp class
class MP:
    def __init__(self, name, con, party, gender, region, valid_votes):
        self.party = party
        self.valid_votes = 0
        self.desc = {"Name": name,"Constituency": con,"Party": self.party, "Gender": gender, "Region": region,  "Valid Votes": valid_votes}

    def __str__(self):
        return self.desc["Name"] + " MP, Constituency: " + self.desc["Constituency"] + ", Gender: " + self.desc["Gender"] 

    def get_party(self):
        return self.desc["Party"].lower()

    def get_region(self):
        return self.desc["Region"].lower()

    def get_name(self):
        return self.desc["Name"].lower()

    def add_votes(self,votes):
        self.valid_votes += votes

    def get_votes(self):
        return self.valid_votes

# reads file using csv module
def read_file():
    # dictionaries to store data
    parties = {}
    constituencies = {}
    total = 0

    try:
        with open('FullDataFor20241.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            # gets info of the mp from file
            for row in reader:
                mp_name = row["Member first name"] + ' ' + row["Member surname"]
                con_name = row["Constituency name"]
                party_name = row["First party"]
                valid_votes = int(row["Valid votes"])
                total_votes = valid_votes + int(row["Invalid votes"])
                result = row["Result"]
                gender = row["Member gender"]
                region = row["Region name"]
                
                # create mp, party and con for this row
                this_mp = MP(mp_name, con_name, party_name, gender, region, valid_votes)
                mps_list.append(this_mp)

                # adds info to dictionaries
                constituencies[con_name.lower()] = Constituency(con_name, region, valid_votes, total_votes, result)
                parties[party_name.lower()] = Party(party_name, region)

                # adds votes for a party
                this_mp.add_votes(valid_votes)
            
        csvfile.close()

    # any error handling with the files
    except FileNotFoundError:
        print("File was not found.")
        
    return parties, constituencies # returns dictionaries to use in code

# calculate statistics
def calculate_statistics(constituencies):
    total_votes_cast = sum([c.valid_votes for c in constituencies.values()])
    avg_con_votes = total_votes_cast / len(constituencies)
    total_mps = len(mps_list)

    stats ={
        "Average Votes per Constituency": avg_con_votes,
        "Total Votes Cast": total_votes_cast,
        "Total MPs": total_mps
        }
    
    return stats

# save statistics to a file
def save_statistics(stats):
    try:
        file = open("statistics.txt", "w")
        file.write("Election Statistics\n")
        file.write("------------------------------------\n")
        for key, value in stats.items():
            file.write(f"{key}: {value}\n")
        file.close()
        print("Statistics saved successfully")
    except IOError:
        print("Error saving to file")

# displays menu of items in option list
def display_menu(menu):
    option_num = 0
    for op in menu:
        print(option_num, ":\t", op)
        option_num += 1
        
# exploring parties
def party_menu(parties):
    print("------------------------------------")
    print("Explore Parties")
        
    while True:
        display_menu(party_options)
        
        try:
            answer = int(input("Enter: "))
            if answer == 0:
                # view mps in a party
                print("Parties: Con, Lab, LD, RUK, Green, SNP, PC, DUP, SF, SDLP, UUP, APNI")
                party_name = input("Enter party name: ")
                found = False
                for mp in mps_list:
                    if mp.get_party() == party_name.lower():
                        print(mp)
                        found = True
                if not found:
                    print("Party not found")
                    
            elif answer == 1:
                total = 0
                # view total votes a party
                print("Parties: Con, Lab, LD, RUK, Green, SNP, PC, DUP, SF, SDLP, UUP, APNI")
                party_name = input("Enter party name: ")
                
                if party_name.lower() in parties:
                    total = sum([mp.get_votes() for mp in mps_list if mp.get_party() == party_name.lower()]) # calculates total of specific party
                    print(party_name.capitalize(), "has a total of", total, "votes")
                else:
                    print("Party not found")

            elif answer == 2:
                # view party votes as a precentage of total votes
                party_total = 0
                total_votes = 0
                print("Parties: Con, Lab, LD, RUK, Green, SNP, PC, DUP, SF, SDLP, UUP, APNI")
                party_name = input("Enter party name: ")
                
                if party_name.lower() in parties:   
                    party_total = sum([mp.get_votes() for mp in mps_list if mp.get_party() == party_name.lower()])
                    total_votes = sum([mp.get_votes() for mp in mps_list]) # calculates total votes cast

                    if total_votes > 0:
                        percent = (party_total / total_votes) * 100
                        print(f"{party_name.capitalize()} has {percent:.2f}% votes of total votes cast") # gives precentage as 2dp
                    else:
                        print("No votes cast")
                
                else:
                    print("Party not found")
                
            elif answer == 3:
                # back to main menu
                main_menu()
                break
            else:
                print("Please enter correct value")
        except ValueError:
            print("Please enter a number")
            
# exploring constiuencies
def con_menu(constituencies):
    print("------------------------------------")
    print("Explore Constituencies")
    
    while True:
        display_menu(con_options)
        
        try:
            answer = int(input("Enter: "))
            if answer == 0:
                # list all constits by region
                region_name = input("Enter region name: ")
                found = False
                for con in constituencies.values():
                    if con.get_region() == region_name.lower():
                        print(con)
                        found = True
                if not found:
                    print("Region not found")
                
            elif answer == 1:
                # view valid votes for a constituency
                con_name = input("Enter constituency name: ")
                if con_name.lower() in constituencies:
                    con_votes = constituencies[con_name].get_votes()
                    print(con_name, "has", con_votes, "valid votes")
                else:
                    print("Constituency not found")
                
            elif answer == 2:
                # view const votes as a precentage of total votes
                con_name = input("Enter constituency name: ")
                if con_name.lower() in constituencies:
                    con_precent = constituencies[con_name.lower()].valid_vote_precentage()
                    print(f"{con_name} has {con_precent:.2f}% valid votes of total votes")
                else:
                    print("Constituency not found")
                
            elif answer == 3:
                # back to main menu
                main_menu()
                break
            else:
                print("Please enter correct value")
        except ValueError:
            print("Please enter a number")
            
# exploring mps
def mp_menu():
    print("------------------------------------")
    print("Explore MPs")
    
    while True:
        display_menu(mps_options)
        
        try:
            answer = int(input("Enter: "))
            if answer == 0:
                # get info and votes by name
                mp_name = input("Enter MP name: ")
                found = False
                printed_mps = set()
                for mp in mps_list:
                    if mp.get_name() == mp_name.lower() and mp.get_name() not in printed_mps:
                        print(mp)
                        print("Votes were:", mp.get_votes())
                        found = True
                        printed_mps.add(mp.get_name()) # stops duplicates when printing
                if not found:
                    print("MP not found")
                    
            elif answer == 1:
                # list by party
                print("Parties: Con, Lab, LD, RUK, Green, SNP, PC, DUP, SF, SDLP, UUP, APNI")
                party_name = input("Enter party name: ")
                found = False
                for mp in mps_list:
                    if mp.get_party() == party_name.lower():
                        print(mp)
                        found = True
                if not found:
                    print("MP not found")

            elif answer == 2:
                # list by region
                region_name = input("Enter region name: ")
                found = False
                for mp in mps_list:
                    if mp.get_region() == region_name.lower():
                        print(mp)
                        found = True
                if not found:
                    print("Region not found")
                
            elif answer == 3:
                # back to main menu
                main_menu()
                break
            else:
                print("Please enter correct value")
        except ValueError:
            print("Please enter a number")

def stats_menu(constituencies):
    print("------------------------------------")
    print("View Statistics")
    stats = calculate_statistics(constituencies)

    while True:
        display_menu(stats_options)
        
        try:
            answer = int(input("Enter: "))
            if answer == 0:
                # avg con votes
               print(f"Average Votes per Constituency: {stats['Average Votes per Constituency']:.2f}")
            elif answer == 1:
                # total mp votes
               print(f"Total MPs: {stats['Total MPs']}")
            elif answer == 2:
                # total votes cast
                print(f"Total Votes Cast: {stats['Total Votes Cast']}")
            elif answer == 3:
                # save stats to a file
                save_statistics(stats)
            elif answer == 4:
                # back to main menu
                main_menu()
                break
            else:
                print("Please enter correct value")
        except ValueError:
            print("Please enter a number")


# checks if user's input is in range and opens selected menu
def main_menu():
    print("------------------------------------")
    print("Main Menu")
    display_menu(main_options)
    p,c = read_file() # declares dictionaries 
    
    while True:
        try:
            answer = int(input("Enter: "))
            if answer == 0:
                party_menu(p)
            elif answer == 1:
                con_menu(c)
            elif answer == 2:
                mp_menu()
            elif answer == 3:
                stats_menu(c)
            elif answer == 4:
                print("------------------------------------")
                print("Exiting app...")
                time.sleep(1)
                print("------------------------------------")
                break
            else:
                print("Please enter correct value")
            break
        except ValueError:
            print("Please enter a number")
            

# welcome message
print("------------------------------------")
print("Welcome to the Election Analysis App")
print("------------------------------------")
print("Choose your option depending on the number")

# run program
main_menu()


### Refrences
### Peter Blanchfield (2024), 'OneLastTime' [Program Code], https://olympus.ntu.ac.uk/CMP3BLANCP/OneLastTime/blob/main/MyPythonProject.py
