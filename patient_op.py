import json
import requests

def run():
    run_p = 1
    run_l = 0
    print("Welcome to CMS!")
    while run_p:
        resp = input("[1] Log In\n"
                     "[2] Sign Up\n"
                     "[X] Exit\n"
                     "Enter number here: ")
        if resp == '1':
            print("Log In")
            name = input("Username:")
            password = input("Password:")
            payload = {'name': name, 'password': password}
            result = requests.get("http://127.0.0.1:8000/Login", params=payload).json()
            print(result)
            if result == "True":
                print("Welcome!")
                run_l = 1
            else:
                print("Log in failed. Try again.")
            while run_l:
                print("---------------------------------------------------------------\n")
                print("What would you like to do today?")
                ui = input("[1] Book Covid-19 Test\n"
                              "[2] Book Covid-19 Vaccine\n"
                              "[3] View Appointments\n"
                              "[4] View Vaccine History\n"
                              "[5] Get Covid Test Results\n"
                              "[X] Log Out\n"
                              "Please enter the number from the options provided above:")
                if ui == '1':
                    print("---------------------------------------------------------------\n")
                    print("Booking Covid Test")
                    clinic, date, time = input("Please enter the clinic name, date and time "
                                               "for you testing appointment separated by spaces: ").split()
                    payload = {'clinic': clinic, 'date': date, 'time': time}
                    print(requests.post("http://127.0.0.1:8000/book/test", params=payload).json())

                elif ui == '2':
                    print("---------------------------------------------------------------\n")
                    print("Booking Covid Vaccine")
                    clinic, date, time = input("Please enter the clinic name, date and time "
                                    "for you vaccine appointment separated by spaces: ").split()
                    choice = input(
                        "[1] Moderna\n"
                        "[2] Pfizer\n"
                        "[3] BioNTech\n"
                        "[4] AstraZeneca\n"
                        "[5] JohnsonAndJohnson\n"
                        "Which vaccine would you prefer?")
                    if choice == '1':
                        vac_type = "Moderna"
                    elif choice == '2':
                        vac_type = "Pfizer"
                    elif choice == '3':
                        vac_type = "BioNTech"
                    elif choice == '4':
                        vac_type = "AstraZeneca"
                    elif choice == '5':
                        vac_type = "JohnsonAndJohnson"
                    else:
                        vac_type = "Pfizer"
                    payload = {'vac_type': vac_type, 'clinic': clinic, 'date': date, 'time': time}
                    print(requests.post("http://127.0.0.1:8000/book/vac", params=payload).json())
                elif ui == '3':
                    print("---------------------------------------------------------------\n")
                    print("View Appointment")
                    print(requests.get("http://127.0.0.1:8000/view/appt").json())
                elif ui == '4':
                    print("---------------------------------------------------------------\n")
                    print("View Vaccine History")
                    print(requests.get("http://127.0.0.1:8000/view/vac").json())
                elif ui == '5':
                    print("---------------------------------------------------------------\n")
                    print("View Covid Test Result")
                    print(requests.get("http://127.0.0.1:8000/view/test").json())
                elif ui == 'X' or ui == 'x':
                    print("---------------------------------------------------------------\n")
                    print("Logging out...")
                    run_l = 0
                else:
                    print("Invalid input.")
        elif resp == '2':
            name, password, hs_num, dob = input("Please enter your name, password, hs_num and date of birth separated by spaces: ").split()
            payload = {'name': name, 'password': password, 'hs_num': hs_num, 'dob': dob}
            print(requests.post("http://127.0.0.1:8000/SignUp", params=payload).json())
        elif resp == 'x' or resp == 'X':
            run_p = 0
            print("Exiting application.")
        else:
            print("Invalid input")


if __name__ == "__main__":
    run()
