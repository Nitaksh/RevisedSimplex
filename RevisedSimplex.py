import tkinter as tk
import numpy as np

#creating the window
window = tk.Tk()
window.title("Revised Simplex Method")
window.geometry("400x400")

#creating the labels
l1 = tk.Label(window, text="Enter the number of variables:")
l1.grid(column=0, row=0)

l2 = tk.Label(window, text="Enter the number of constraints:")
l2.grid(column=0, row=1)

#creating the entry boxes
e1 = tk.Entry(window)
e1.grid(column=1, row=0)

e2 = tk.Entry(window)
e2.grid(column=1, row=1)

obj_coeff = []
const_coeff = []
rhs = []

#creating the function to get the input from the user
def get_input():
    n = int(e1.get())
    m = int(e2.get())

    #creating the labels for the objective function
    l3 = tk.Label(window, text="Enter the coefficients of the objective function:")
    l3.grid(column=0, row=2)

    #creating the entry boxes for the objective function
    for i in range(n):
        obj_coeff.append(tk.Entry(window))
        obj_coeff[i].grid(column=i, row=3)

    #creating the labels for the constraints
    l4 = tk.Label(window, text="Enter the coefficients of the constraints:")
    l4.grid(column=0, row=4)

    #creating the entry boxes for the constraints
    for i in range(m):
        const_coeff.append([])
        for j in range(n):
            const_coeff[i].append(tk.Entry(window))
            const_coeff[i][j].grid(column=j, row=i+5)

    #creating the label for the right-hand side of the constraints
    l5 = tk.Label(window, text="Enter the right-hand side of the constraints:")
    l5.grid(column=0, row=m+5)

    #creating the entry boxes for the right-hand side of the constraints
    for i in range(m):
        rhs.append(tk.Entry(window))
        rhs[i].grid(column=n, row=i+5)

    #creating the button to solve the problem
    b1 = tk.Button(window, text="Maximize", command=solve_max)
    b1.grid(column=0, row=m+6)
    b2 = tk.Button(window, text="Minimize", command=solve_min)
    b2.grid(column=1, row=m+6)

#creating the function to solve the maximization problem
def solve_max():
    n = int(e1.get())
    m = int(e2.get())
    obj_coeff1 = []
    for i in range(n):
        obj_coeff1.append(float(obj_coeff[i].get()))
    const_coeff1 = []
    for i in range(m):
        const_coeff1.append([])
        for j in range(n):
            const_coeff1[i].append(float(const_coeff[i][j].get()))
    rhs1 = []
    for i in range(m):
        rhs1.append(float(rhs[i].get()))

    A = np.array(const_coeff1)
    b = np.array(rhs1)
    c = np.array(obj_coeff1)
    c = np.append(c, 0)
    A = np.column_stack((A, b))
    A = np.row_stack((A, c))

    basic_var = []
    non_basic_var = []
    for i in range(m):
       basic_var.append(n + i)
    for i in range(n):
        non_basic_var.append(i)
    # Implementing the revised simplex method
    iteration = 1
    while True:
        print(f"Iteration {iteration}:")
        print("Current basic variables:", basic_var)
        print("Current non-basic variables:", non_basic_var)
        print("Current tableau:")
        print(A)

        # Finding the entering variable
        c_b = A[-1][:-1]
        c_nb = A[-1][-1]
        entering_var = np.argmax(c_b - c_nb)

        # Finding the leaving variable
        ratio = []
        for i in range(m):
            if A[i][entering_var] > 0:
                ratio.append(A[i][-1] / A[i][entering_var])
            else:
                ratio.append(float('inf'))
        leaving_var = np.argmin(ratio)

        # Checking for unboundedness
        if all(x == float('inf') for x in ratio):
            print("Unbounded solution!")
            return

        # Updating the basic and non-basic variables
        basic_var[leaving_var] = entering_var
        non_basic_var[entering_var] = leaving_var

        # Updating the augmented matrix
        pivot = A[leaving_var][entering_var]
        A[leaving_var] = A[leaving_var] / pivot
        for i in range(m + 1):
            if i != leaving_var:
                A[i] = A[i] - A[i][entering_var] * A[leaving_var]

        # Checking for optimality (maximization)
        if np.all(A[-1][:-1] <= 0):
            break

        iteration += 1

    # Printing the optimal solution
    print("\nOptimal Solution:")
    for i in range(n):
        if i in basic_var:
            print(f"x{i + 1} = {A[basic_var.index(i)][-1]}")
        else:
            print(f"x{i + 1} = 0")
    print(f"Optimal Value = {A[-1][-1] * -1}")
def solve_min():
    n = int(e1.get())
    m = int(e2.get())
    obj_coeff1 = []
    for i in range(n):
        obj_coeff1.append(float(obj_coeff[i].get()) * -1)
        const_coeff1 = []
    for i in range(m):
         const_coeff1.append([])
         for j in range(n):  
            const_coeff1[i].append(float(const_coeff[i][j].get()))
    rhs1 = []
    for i in range(m):
        rhs1.append(float(rhs[i].get()))
    A = np.array(const_coeff1)
    b = np.array(rhs1)
    c = np.array(obj_coeff1)
    c = np.append(c, 0)
    A = np.column_stack((A, b))
    A = np.row_stack((A, c))

    basic_var = []
    non_basic_var = []
    for i in range(m):
        basic_var.append(n + i)
    for i in range(n):
        non_basic_var.append(i)

    # Implementing the revised simplex method
    iteration = 1
    while True:
        print(f"Iteration {iteration}:")
        print("Current basic variables:", basic_var)
        print("Current non-basic variables:", non_basic_var)
        print("Current tableau:")
        print(A)

        # Finding the entering variable
        c_b = A[-1][:-1]
        c_nb = A[-1][-1]
        entering_var=np.argmin(c_b - c_nb)
            # Finding the leaving variable
        ratio = []
        for i in range(m):
            if A[i][entering_var] > 0:
                ratio.append(A[i][-1] / A[i][entering_var])
            else:
                ratio.append(float('inf'))
        leaving_var = np.argmin(ratio)

        # Checking for unboundedness
        if all(x == float('inf') for x in ratio):
            print("Unbounded solution!")
            return

        # Updating the basic and non-basic variables
        basic_var[leaving_var] = entering_var
        non_basic_var[entering_var] = leaving_var

        # Updating the augmented matrix
        pivot = A[leaving_var][entering_var]
        A[leaving_var] = A[leaving_var] / pivot
        for i in range(m + 1):
            if i != leaving_var:
                A[i] = A[i] - A[i][entering_var] * A[leaving_var]

        # Checking for optimality (minimization)
        if np.all(A[-1][:-1] >= 0):
            break

        iteration += 1

    # Printing the optimal solution
    print("\nOptimal Solution:")
    for i in range(n):
        if i in basic_var:
            print(f"x{i + 1} = {A[basic_var.index(i)][-1]}")
        else:
            print(f"x{i + 1} = 0")
    print(f"Optimal Value = {A[-1][-1]}")

b = tk.Button(window, text="Submit", command=get_input)
b.grid(column=1, row=2)
window.mainloop()
