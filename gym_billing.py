# START
import random
import datetime
from datetime import datetime


def load(filename):
    if filename == "members.txt":
        with open(filename, "r") as f:
            members = f.read()
            members = members.split("\n")
            members = [i.split(",") for i in members]
            members = {i[0]: i[1:] for i in members}
        return members

    if filename == "classes.txt":
        with open(filename, "r") as f:
            classes = f.read()
            classes = classes.split("\n")
            classes = [i.split(",") for i in classes]
            classes = {i[0]: i[1:] for i in classes}
        return classes


def save(filename, ulist):
    if filename == "members.txt":

        with open("members.txt", "w") as f:
            for i in ulist:
                f.write(i + "," + ",".join(ulist[i]) + "\n")

    if filename == "classes.txt":
        with open("classes.txt", "w") as f:
            for i in ulist:
                f.write(i + "," + ",".join(ulist[i]) + "\n")


def class_registrations():
    # Dictionary to store class information - key is class code
    classes = {}
    # Dictionary to store members registered for each class - key is class code
    class_members = {}
    # Dictionary to track total revenue for each class - key is class code
    class_revenue = {}

    # Read classes.txt file
    try:
        with open('classes.txt', 'r') as class_file:
            for line in class_file:
                parts = line.strip().split(',')
                if len(parts) >= 3:  # Ensure we have enough fields
                    class_code = parts[0].strip()
                    class_name = parts[1].strip()
                    class_cost = float(parts[2].strip())  # Cost is in the third position (index 2)

                    classes[class_code] = {
                        'name': class_name,
                        'cost': class_cost
                    }
                    class_members[class_code] = []
                    class_revenue[class_code] = 0.0
    except FileNotFoundError:
        print("Error: classes.txt file not found.")
        return
    except Exception as e:
        print(f"Error reading classes.txt: {e}")
        return

    # Read members.txt file
    try:
        with open('members.txt', 'r') as members_file:
            for line in members_file:
                parts = line.strip().split(',')
                if len(parts) >= 6:  # Ensure we have enough fields
                    first_name = parts[1].strip()
                    last_name = parts[2].strip()
                    class_code = parts[5].strip()

                    # Check if the class code exists
                    if class_code in classes:
                        full_name = f"{first_name} {last_name}"
                        class_members[class_code].append(full_name)
                        class_revenue[class_code] += classes[class_code]['cost']
    except FileNotFoundError:
        print("Error: members.txt file not found.")
        return
    except Exception as e:
        print(f"Error reading members.txt: {e}")
        return

    # Generate and print the report
    print("\n=== CLASS REGISTRATION AND REVENUE REPORT ===\n")

    for class_code in sorted(classes.keys()):
        class_name = classes[class_code]['name']
        cost = classes[class_code]['cost']
        members = class_members[class_code]
        total_revenue = class_revenue[class_code]

        print(f"Class: {class_name} (Code: {class_code})")
        print(f"Cost per Member: ${cost:.2f}")
        print(f"Number of Members: {len(members)}")
        print(f"Total Revenue: ${total_revenue:.2f}")
        print("\nRegistered Members:")

        if members:
            for member in sorted(members):
                print(f"- {member}")
        else:
            print("- No members registered")

        print("\n" + "-" * 50 + "\n")

    # Print summary of all classes
    total_all_revenue = sum(class_revenue.values())
    total_all_members = sum(len(members) for members in class_members.values())

    print("=== SUMMARY ===")
    print(f"Total Number of Classes: {len(classes)}")
    print(f"Total Number of Registrations: {total_all_members}")
    print(f"Total Revenue: ${total_all_revenue:.2f}")


def generate_client_report():
    membership_fees = {
        "Platinum": 10000,
        "Diamond": 7500,
        "Gold": 4000,
        "Standard": 2000
    }

    # Dictionary to store class information - key is class ID
    classes = {}

    # Dictionary to store client information - key is member ID
    clients = {}

    try:
        with open('classes.txt', 'r') as class_file:
            for line in class_file:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    class_id = parts[0].strip()
                    class_name = parts[1].strip()
                    class_cost = float(parts[2].strip())

                    classes[class_id] = {
                        'name': class_name,
                        'cost': class_cost
                    }
    except FileNotFoundError:
        print("Error: classes.txt file not found.")
        return
    except Exception as e:
        print(f"Error reading classes.txt: {e}")
        return

    try:
        with open('members.txt', 'r') as members_file:
            for line in members_file:
                parts = line.strip().split(',')
                if len(parts) >= 6:
                    member_id = parts[0].strip()
                    first_name = parts[1].strip()
                    last_name = parts[2].strip()
                    membership_type = parts[4].strip()
                    class_id = parts[5].strip()

                    # If this is the first time we see this member, initialize their record
                    if member_id not in clients:
                        clients[member_id] = {
                            'first_name': first_name,
                            'last_name': last_name,
                            'membership_type': membership_type,
                            'classes': [],
                            'total_fee': 0.0
                        }

                    # Add class to member's record if it exists
                    if class_id in classes:
                        clients[member_id]['classes'].append({
                            'id': class_id,
                            'name': classes[class_id]['name'],
                            'cost': classes[class_id]['cost']
                        })
    except FileNotFoundError:
        print("Error: members.txt file not found.")
        return
    except Exception as e:
        print(f"Error reading members.txt: {e}")
        return

    # Calculate total monthly fee for each client
    for member_id, client_info in clients.items():
        # Start with the base membership fee
        membership_type = client_info['membership_type']
        if membership_type in membership_fees:
            base_fee = membership_fees[membership_type]
        else:
            base_fee = 0.0
            print(f"Warning: Unknown membership type '{membership_type}' for client {member_id}")

        # Add the cost of all classes
        class_fees = sum(class_info['cost'] for class_info in client_info['classes'])

        # Calculate total fee
        total_fee = base_fee + class_fees
        clients[member_id]['total_fee'] = total_fee

    # Generate and print the report
    print("\n=== GYM CLIENT MONTHLY FEE REPORT ===\n")

    for member_id in sorted(clients.keys()):
        client = clients[member_id]

        print(f"Client ID: {member_id}")
        print(f"Name: {client['first_name']} {client['last_name']}")
        print(f"Membership Type: {client['membership_type']}")

        if client['membership_type'] in membership_fees:
            print(f"Base Membership Fee: ${membership_fees[client['membership_type']]:.2f}")
        else:
            print(f"Base Membership Fee: Unknown (membership type not found)")

        print("\nRegistered Classes:")
        if client['classes']:
            class_total = 0.0
            for class_info in client['classes']:
                print(f"- {class_info['name']} (ID: {class_info['id']}) - ${class_info['cost']:.2f}")
                class_total += class_info['cost']
            print(f"\nTotal Class Fees: ${class_total:.2f}")
        else:
            print("- No additional classes registered")
            print("\nTotal Class Fees: $0.00")

        print(f"\nTOTAL MONTHLY FEE: ${client['total_fee']:.2f}")
        print("\n" + "-" * 50 + "\n")

    # Print summary
    total_clients = len(clients)
    total_revenue = sum(client['total_fee'] for client in clients.values())

    print("=== SUMMARY ===")
    print(f"Total Number of Clients: {total_clients}")
    print(f"Total Monthly Revenue: ${total_revenue:.2f}")


def main():
    def checkin():
        members = load("members.txt")
        classes = load("classes.txt")
        while True:
            membership_id = input("Enter your valid membership number: ").strip()
            if membership_id in members:
                break
            else:
                print("Invalid Membership ID. Please enter a valid membership number.")
        current_date = datetime.now()

        print("\nAvailable Classes for Registration:")
        for cls, names in classes.items():
            print("-", cls, names[0])

        selected_class = input("\nEnter the id of the class you want to register for: ").strip()

        while True:
            if selected_class in classes:
                break
            else:
                print("Invalid class selection. Please choose a valid class.")

        # Step 4: Update the member's record with the selected class
        members[membership_id].append(selected_class)

        # Save the updated members list back to the file
        save("members.txt", members)

        print("Registration Successful!")
        print(f"Membership ID: {membership_id}")
        print(f"Class ID: {selected_class}")
        print(f"Class Registered: {classes.get(selected_class)[0]}")
        print(f"Time Registered: {current_date}")

    def login():
        attempts = 3
        stored_username = "Admin"
        stored_password = "Admin12!"

        while attempts > 0:
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            if username == stored_username and password == stored_password:
                print("Login Successful!\n")
                return True
            else:
                attempts -= 1
                print(f"Login failed! {attempts} attempt(s) left.")

        print("Login failed! System shutting down.")
        return False

    def add_memb():
        members = load("members.txt")
        # Add a new member to the gym
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        while True:
            contact_number = input("Enter contact number: ")
            if contact_number.isdigit() and len(contact_number) == 10:
                break
            else:
                print("Invalid contact number. Please enter a 10 digit number.")
        while True:
            mem_type = input("Enter membership type: ")
            if mem_type in ["Platinum", "Diamond", "Gold", "Standard"]:
                break
            else:
                print("Invalid membership type. Please enter Platinum, Diamond, Gold or Standard.")
        print("Member added successfully.")
        while True:
            mem_number = "M" + str(random.randint(1000, 9999))
            if mem_number not in members:
                break
        print("Membership number: ", mem_number)
        members[mem_number] = [first_name, last_name, contact_number, mem_type]

        if save("members.txt", members):
            print("Member added successfully.")
     
    def add_instruct():
        with open("members.txt", "r") as f:
            members = f.read()
            members = members.split("\n")
            members = [i.split(",") for i in members]
            members = {i[0]: i[1:] for i in members}
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        while True:
            contact_number = input("Enter contact number: ")
            if contact_number.isdigit() and len(contact_number) == 10:
                break
            else:
                print("Invalid contact number. Please enter a 10 digit number.")
        while True:
            trn = input("Enter a valid Tax Registration Number: ")
            if trn.isdigit() and len(trn) == 9:
                break
            else:
                print("Invalid input. Please enter a nine digit number.")

        while True:
            dob = input("Enter date of birth (ddmmyyyy): ")
            if dob.isdigit() and len(dob) == 8:
                break
            else:
                print("Invalid input. Please enter your date of birth in the format ddmmyyyy: ")
        while True:
            mem_number = "I" + str(random.randint(1000, 9999))
            if mem_number not in members:
                break
        print("Instructor identification number: ", mem_number)
        members[mem_number] = [first_name, last_name, contact_number, trn, dob]
        with open("members.txt", "w") as f:
            for i in members:
                f.write(i + "," + ",".join(members[i]) + "\n")
        print("Instructor added successfully.")

    def print_report():
        try:
            members_list = []

            with open("members.txt", "r") as file:
                for line in file:
                    member_data = line.strip().split(",")
                    members_list.append(member_data)
        except FileNotFoundError:
            print("Error: members.txt file not found.")
            return

        try:
            with open("classes.txt", "r") as file:
                class_summary = file.readlines()
        except FileNotFoundError:
            print("Error: classes.txt file not found.")
            return

        membership_fees = {
            "Platinum": 10000,
            "Diamond": 7500,
            "Gold": 4000,
            "Standard": 2000
        }

        # Dictionary to store class information - key is class code
        classes = {}
        # Dictionary to store members registered for each class - key is class code
        class_members = {}
        # Dictionary to track total revenue for each class - key is class code
        class_revenue = {}

        print("REPORTS")
        print("1. Total Members")
        print("2. Class Schedules")
        print("3. Membership Summary")
        print("4. Class Registration Summary")
        print("5. Client Report")
        print("6. Exit")

        choice = input("Enter number: ")

        if choice == '1':
            print(f"Total Members: {len(members_list)}\n")
            print("List of Members:")
            for member in members_list:
                if len(member) >= 3:
                    _, first_name, last_name = member[:3]
                    print(first_name, last_name)
        elif choice == '2':
            print("Class Schedules:\n")  # Initial header with a blank line
            for class_item in class_summary:
                print(class_item, end="\n")
        elif choice == '3':
            if len(member_data) == 5:
                members_list.append(member_data)

            # Organize data by membership type
            membership_data = {}

            for member in members_list:
                member_id, first_name, last_name, monthly_fee, membership_type = member

                # Look up the monthly fee for the membership type
                if membership_type in membership_fees:
                    monthly_fee = membership_fees[membership_type]

                # Initialize the membership type if it doesn't exist
                if membership_type not in membership_data:
                    membership_data[membership_type] = {
                        "members": [],
                        "total_fees": 0
                    }

                # Adds a member to the membership type group
                membership_data[membership_type]["members"].append((first_name, last_name))
                membership_data[membership_type]["total_fees"] += monthly_fee

            print("List of Members with Membership Types:")
            for membership_type, data in membership_data.items():
                print(f"\nMembership Type: {membership_type}")
                print("Members:")
                for first_name, last_name in data["members"]:
                    print(f"- {first_name} {last_name}")
                print(f"Total Members: {len(data['members'])}")
                print(f"Total Monthly Fees: ${data['total_fees']:.2f}")

            # Display overall totals
            total_members = sum(len(data["members"]) for data in membership_data.values())
            total_fees = sum(data["total_fees"] for data in membership_data.values())

            print("\nOverall Totals:")
            print(f"Total Members: {total_members}")
            print(f"Total Monthly Fees: ${total_fees:.2f}")

        elif choice == '4':
            class_registrations()

        elif choice == '5':
            generate_client_report()
        elif choice == '6':
            display_menu()
        else:
            print("Invalid option! Please try again.")

    def exit_program():
        while True:
            user_choice = input("Are you sure you want to exit? (Y/N): ").strip().lower()

            if user_choice == "y":
                print("Exiting the Gym Billing System...")
                exit()  # Terminates the program
            elif user_choice == "n":
                print("Returning to the main menu...")
                break
            else:
                print("Invalid input! Please enter 'Y' for Yes or 'N' for No.")

    def add_update_session():
        sessions = load("classes.txt")
        print("1. Add New Session\n2. Update Existing Session\n3. Exit")
        choice = input("Enter number: ")
        if choice == "1":
        # Add new session
            while True:
                session_id = input("Enter Session ID: ")
                if len(session_id) == 5 and session_id[0] == 'C' and session_id[1:].isdigit():
                    break
                else:
                    print("Invalid input. Please enter the session ID in the format C0000.")
                    
            session_name = input("Enter Session Name: ")
            session_day = input("Enter the Days the Session will be held: ").capitalize()
            session_time = input("Enter the Time: ").capitalize()
            session_cost = input("Enter the Cost of the Session: ")
            instructor = input("Enter the Name of the Instructor: ")
            
            # Match the format in classes.txt: [name, day, time, cost, instructor]
            sessions[session_id] = [session_name, session_day, session_time, session_cost, instructor]
            if save("classes.txt",sessions):
                print("New session successfully added!")
        elif choice == "2":
        # Update session
            while True:
                session_id = input("Enter the Session ID you want to update: ")
                if session_id in sessions:
                    break
                else:
                    print("Invalid input. Please enter a valid session ID.")
            
            new_name = input("Enter New Session Name (or press Enter to keep the current name): ")
            if new_name:
                sessions[session_id][0] = new_name
                
            new_day = input("Enter New Days (or press Enter to keep the current days): ")
            if new_day:
                sessions[session_id][1] = new_day
                
            new_time = input("Enter New Time (or press Enter to keep the current time): ")
            if new_time:
                sessions[session_id][2] = new_time
                
            new_cost = input("Enter New Cost (or press Enter to keep the current cost): ")
            if new_cost:
                sessions[session_id][3] = new_cost
                
            new_instructor = input("Enter New Instructor Name (or press Enter to keep the current instructor): ")
            if new_instructor:
                sessions[session_id][4] = new_instructor

            if save("classes.txt",sessions):    
                print("Session successfully updated!")
            
        else:
            print("Exiting session update menu.")
            return    
        
    def display_menu():
        while True:
            print("\n")
            print("=" * 25)
            print("GYM BILLING SYSTEM")
            print("1. Check-in a Member")
            print("2. Add Member(s)")
            print("3. Add/Update Session")
            print("4. Add Facilitator/Instructor")
            print("5. Print Report")
            print("6. Exit")
            print("=" * 25)

            choice = input("Enter number: ")

            if choice == '1':
                checkin()
            elif choice == '2':
                add_memb()
            elif choice == '3':
                add_update_session()
            elif choice == '4':
                add_instruct()
            elif choice == '5':
                print_report()
            elif choice == '6':
                exit_program()
            else:
                print("Invalid option! Please try again.")

    if login():
        display_menu()
    else:
        print("Exiting program!")
        exit()


main()

# STOP
