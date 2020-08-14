class Employee:
    'Common base class for all employee'
    empCount = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print("Total Employee %d" % Employee.empCount)

    def displayEmployee(self):
        print("Name: ", self.name, ", Salary: ", self.salary)

    def __str__(self):
        print("This is string")


e1 = Employee("dan", "1k")
e1.displayCount()