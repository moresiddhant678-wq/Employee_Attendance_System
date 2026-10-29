import json
import os
from datetime import datetime

FILE_NAME = "attendance.txt" 

def load_data():
    """Load employee data from attendance.txt at application start."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as file:
            data = file.read().strip()
            if not data:
                return []
            return json.loads(data)
    except Exception:
        return []

def save_data(employees):
    """Save the current employee records list to attendance.txt."""
    with open(FILE_NAME, "w") as file:
        json.dump(employees, file, indent=4)

def generate_next_id(employees):
    """Generate sequential employee IDs starting from E101."""
    if not employees:
        return "E101"
    
    
    max_id = 100
    for emp in employees:
        emp_id = emp.get("id", "")
        if emp_id.startswith("E") and emp_id[1:].isdigit():
            val = int(emp_id[1:])
            if val > max_id:
                max_id = val
    return f"E{max_id + 1}"

def find_employee(employees, emp_id):
    """Find an employee dictionary by ID."""
    for emp in employees:
        if emp["id"] == emp_id:
            return emp
    return None

def add_employee(employees):
    """Menu Option 1: Add a new employee."""
    name = input("Name: ").strip()
    new_id = generate_next_id(employees)
    
    new_employee = {
        "id": new_id,
        "name": name,
        "records": {}  
    }
    employees.append(new_employee)
    save_data(employees)
    print(f"Employee added: {new_id} | {name}")

def mark_attendance(employees):
    """Menu Option 2: Mark daily attendance with validation checks."""
    emp_id = input("Employee ID: ").strip()
    emp = find_employee(employees, emp_id)
    if not emp:
        print(f"Employee {emp_id} not found.")
        return

    date_str = input("Date (YYYY-MM-DD): ").strip()
    try:
        
        valid_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        if date_str != valid_date.strftime("%Y-%m-%d"):
            print("Invalid date. Use YYYY-MM-DD.")
            return
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    status = input("Status (P/A/L): ").strip().upper()
    if status not in ["P", "A", "L"]:
        print("Invalid status. Enter P, A or L.")
        return

    
    if date_str in emp["records"]:
        print(f"Attendance for {date_str} is already marked.")
        return

    emp["records"][date_str] = status
    save_data(employees)
    print(f"Attendance marked for {emp['name']} on {date_str} as {status}.")

def view_report(employees):
    """Menu Option 3: View an employee's attendance report."""
    emp_id = input("Employee ID: ").strip()
    emp = find_employee(employees, emp_id)
    if not emp:
        print(f"Employee {emp_id} not found.")
        return

    records = emp.get("records", {})
    present_count = sum(1 for s in records.values() if s == "P")
    absent_count = sum(1 for s in records.values() if s == "A")
    leave_count = sum(1 for s in records.values() if s == "L")
    total_marked = len(records)

    print(f"{emp['name']}: Present {present_count} | Absent {absent_count} | Leave {leave_count}")
    

    if total_marked == 0:
        print("Attendance: 0.00% (no records)")
    else:
        percentage = (present_count / total_marked) * 100
        print(f"Attendance: {percentage:.2f}%")

def main():
    employees = load_data()
    
    while True:
        print("\n--- Employee Attendance System ---")
        print("1. Add Employee")
        print("2. Mark Attendance")
        print("3. View Attendance Report")
        print("4. Exit")
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            add_employee(employees)
        elif choice == "2":
            mark_attendance(employees)
        elif choice == "3":
            view_report(employees)
        elif choice == "4":
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
