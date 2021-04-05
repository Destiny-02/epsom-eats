# note times will need to be changed to 2359 for program to run outside valid times

from tkinter import *
from tkinter import ttk
from functools import partial
from itertools import zip_longest
import csv
import datetime
import time

class food:
    def __init__(self, row, header):
        #initiates each row as an instance and headings as their attributes -(from https://stackoverflow.com/questions/47445586/how-to-read-the-contents-of-a-csv-file-into-a-class-with-each-csv-row-as-a-class)
        self.__dict__ = dict(zip(header, row)) 

    # methods to access attributes using index 
    def find_food_name(i):
        return(foods[i].food_name)
    def find_category(i):
        return(foods[i].category)
    def find_price(i):
        return(foods[i].price)
    def find_description(i):
        return(foods[i].description)

    # find index of food based on food name 
    def find_index(i):
        count = 0
        for food in foods:
            if food.food_name == i:
                break
            else:
                count += 1
        return count

    # adds each food_name into their respective list based on category
    def categorise():
        hot_food_names = []
        chilled_food_names = []
        treats_food_names = []
        for i in range(len(foods)):
            if food.find_category(i) == "Chilled":
                chilled_food_names.append(food.find_food_name(i))
            elif food.find_category(i) == "Hot":
                hot_food_names.append(food.find_food_name(i))
            else:
                treats_food_names.append(food.find_food_name(i))
        return chilled_food_names, hot_food_names, treats_food_names

class pageGrid:
    def __init__(self, parent):
        self.frame_header = ttk.Frame(parent, style='white.TFrame')
        self.frame_header.grid()
        self.body = ttk.Frame(parent, style='white.TFrame')
        self.body.grid()
        ttk.Label(self.frame_header, text = "EPSOM EATS", font=('verdana', 20, 'bold'),style='darkred.TLabel').grid(row = 0, column = 1)
        ttk.Label(self.frame_header, text = "Please select the item to order",style='darkred.TLabel').grid(row = 2, column = 1)
        Button(self.frame_header, text = "FINISH", width = 20, command = partial(orderConfirm, root),font=('verdana', 10, 'bold'), activeforeground="#691822",foreground="#691822", activebackground="#fdd4b7", background="#fdd4b7").grid(row = 2, column = 2, sticky = W, padx = 100, ipadx = 10, pady = 5)
        Button(self.frame_header, text = "CANCEL", width = 20, command = restart,font=('verdana', 10, 'bold'), activeforeground="#691822",foreground="#691822", activebackground="#fdd4b7", background="#fdd4b7").grid(row = 2, column = 0, sticky = E, padx = 100, ipadx = 10, pady = 5)

        # place category headings

        ttk.Label(self.body, text = "CHILLED", style='menufont.TLabel').grid(row = 0, column = 0)
        ttk.Label(self.body, text = "HOT", style='menufont.TLabel').grid(row = 0, column = 1)
        ttk.Label(self.body, text = "TREATS", style='menufont.TLabel').grid(row = 0, column = 2)
        
        # places category frames in window
        self.chilled_content = ttk.Frame(self.body, style='white.TFrame')
        self.chilled_content.grid(row = 1, column = 0, padx = 7, sticky = NW)
        self.hot_content = ttk.Frame(self.body,style='white.TFrame')
        self.hot_content.grid(row = 1, column = 1, padx = 7, sticky = NW)
        self.treats_content = ttk.Frame(self.body, style='white.TFrame')
        self.treats_content.grid(row = 1, column = 2, padx = 7, sticky = NW)
        
        # places button groups in their respective categories
        buttonGrid(self.chilled_content, chilled_button_string)
        buttonGrid(self.hot_content, hot_button_string)
        buttonGrid(self.treats_content, treats_button_string)

# places a category of buttons
class buttonGrid():

    def __init__(self, parent, food_names): 
        
        self.parent = parent
        self.food_names = food_names
        num_rows = self.calculate_rows(food_names)
        NUM_COLS = 2
        buttons = []
        count = 0
        for c in range(NUM_COLS):
            for r in range(num_rows):
                if count < len(food_names):
                    food_name = food_names[count]
                    # prepares food name and price in a tidy format 
                    output = "{} \n${:.2f}".format(food_name[0], float(food_name[1]))
                    # partial code module from https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter/22290388
                    buttons.append(Button(parent, text = output, width = 17,height=1, background="#fcd682" ,activebackground="#fcd682", command = partial(quantityDialogue, root, food_name[0])))
                    buttons[count].grid(row = r, column = c, ipady=5, ipadx=5)
                    count += 1
                
    # number of rows required to format all food names into two columns                 
    def calculate_rows(self, food_names):
            rows = len(food_names) / 2
            if len(food_names) % 2 != 0:
                rows += 0.5
            return int(rows)

    # to be used on button output
    def food_name_price(food_names):
        return_string = []
        for i in food_names:
            sub_list = []
            # adds food name and its corresponding price as a sublist into the returned string
            # adds food name
            sub_list.append(i)
            # finds corresponding index then price
            sub_list.append(food.find_price(food.find_index(i))) 
            return_string.append(sub_list)
        return return_string

class quantityDialogue(): 

    def __init__(self, parent, food_name):
        
        self.top = Toplevel(parent)
        self.top.grab_set()
        self.top.attributes("-topmost", True) #stays on top
        coord = center_window(350, 200)
        self.top.geometry("350x200+{}+{}".format(str(coord[0]), str(coord[1])))
        self.top.title("")
        self.food_name = food_name
        self.price = self.food_name_price_des(food_name)[1]
        self.description = self.food_name_price_des(food_name)[2]
        self.option = IntVar(value=0) #default option is 0
        self.options = [0, 0, 1, 2, 3, 4, 5]

        # set default to current quantity if already in cart
        for item in orders:
            if item[0] == self.food_name:
                self.option = IntVar(value=item[2])
        
        ttk.Label(self.top, text = "{} - ${:.2f}".format(food_name, float(self.price)), style='darkredpopup.TLabel').grid(row = 0, column = 0, columnspan = 4, pady = 10, padx = 50)
        ttk.Label(self.top, text = "{}".format(self.description),  font=('verdana', 8)).grid(row = 1, column = 0, columnspan = 4, pady = 5, padx = 50)
        ttk.Label(self.top, text = "Quantity                  ", style='popupfont.TLabel').grid(row = 3, column = 1, columnspan = 2)
        self.dropdown = ttk.OptionMenu(self.top, self.option, *self.options)
        self.dropdown.grid(row = 3, column = 2)
        # place holder for error message text 
        self.place_holder = Label(self.top).grid(row = 2, column = 0, columnspan = 4, pady = 5, padx = 50) 
        self.top.resizable(0,0)

        ok_button = ttk.Button(self.top, text = "Ok", command = partial(self.ok), style='blue.TButton')
        ok_button.grid(row = 4, column = 0, columnspan = 2, pady = 30, padx = 50)
        cancel_button = ttk.Button(self.top, text = "Cancel", command = self.cancel)
        cancel_button.grid(row = 4, column = 2, columnspan = 2, pady = 30, padx = 50)
        self.check_disable()

    # to find to information needed for the quantity selection dialogue 
    def food_name_price_des(self, food_name):
        return_string = []
        # adds food name and its corresponding info into list 
        return_string.append(food_name)
        # finds corresponding index then other related information
        return_string.append(food.find_price(food.find_index(food_name)))
        return_string.append(food.find_description(food.find_index(food_name)))
        return return_string

    # disables dropdown and displays erorr msg if limit met
    def check_disable(self):
        # allows users to edit quantity of foods already added to cart
        if len(orders) >= 3 and not any(self.food_name in sublist for sublist in orders):
            self.error_msg = ttk.Label(self.top, text = "Limit of 3 types of food items per order", style='rederror.TLabel').grid(row = 2, column = 0, columnspan = 4, padx = 50)
            self.dropdown.configure(state = "disabled")
        else:
            self.dropdown.configure(state = "enabled")       

    def ok(self):
        item_order = []
        value = int(self.option.get())

        # update quantity if it has already been added to cart (editing)
        for item in orders:
            if item[0] == self.food_name:
                item[2] = value
                item[3] = round(value*float(self.price), 1)
                if value == 0:
                    orders.remove(item)
                self.top.destroy()
                return None

        # don't save an order of zero quantity 
        if value == 0:
            self.top.destroy()
            return None
        
        item_order.append(self.food_name)
        item_order.append(self.price)
        item_order.append(value)
        item_order.append(round(value*float(self.price), 1))
        orders.append(item_order)
        self.top.destroy()
        return None
        
    def cancel(self):
        self.top.destroy()

class payment:
    def __init__(self, parent):
        self.top = Toplevel(parent)
        self.top.grab_set()
        self.top.attributes("-topmost", True) #stays on top
        coord = center_window(350, 200)
        self.top.geometry("350x200+{}+{}".format(str(coord[0]), str(coord[1])))
        self.top.resizable(0,0)
        self.top.title("")
        
        self.logo = PhotoImage(file = 'arrow.png')
        
        total = find_total()
        
        ttk.Label(self.top, text = "Please pay below",style='darkredbigpopup.TLabel').grid(row = 0, column = 0, columnspan = 4, pady = 5, padx = 50)
        ttk.Label(self.top, text="Due ${:.2f}".format(float(total)),style='popupfont.TLabel').grid(row = 1, column = 0, columnspan = 4, padx = 50)
        Label(self.top, image = self.logo).grid(row = 2, column = 1, columnspan = 2, padx = 50)
        
        # note that paid button will not be displayed in actual program, paymentAccepted will be commanded through connection to the EFTPOS machines 
        ttk.Button(self.top, text = "<paid>", command = self.paid).grid(row = 3, column = 0, columnspan = 2, padx = 50)
        ttk.Button(self.top, text = "Cancel", command = self.cancel).grid(row = 3, column = 2, columnspan = 2, padx = 50)

    def paid(self):
        self.top.destroy()
        paymentAccepted(root)
        
    def cancel(self):
        self.top.destroy()

class orderConfirm:
    def __init__(self, parent):

        # don't do anything if the user hasn't ordered anything
        if len(orders) == 0:
            return None

        self.top = Toplevel(parent)
        self.top.grab_set()
        self.top.attributes("-topmost", True) #stays on top
        coord = center_window(350, 200)
        self.top.geometry("350x200+{}+{}".format(str(coord[0]), str(coord[1])))
        self.top.resizable(0,0)

        # content must be orgainised in frames to keep order table separate from ok/cancel otherwise ok/cancel will shift depending on length of food name (width of columns)
        self.body = ttk.Frame(self.top)
        self.body.grid(sticky=W)
        self.okcancel = ttk.Frame(self.top)
        self.okcancel.grid()

        self.top.title("")
        title = ttk.Label(self.body, text = "Order Confirmation",style='darkredpopup.TLabel').grid(row = 0, column = 0, pady = 3, sticky = N, padx = 5, columnspan = 4)
        heading_1 = ttk.Label(self.body, text = "Item\n ", style='styleconfirm.TLabel').grid(row = 1, column = 0, sticky = W, padx = 14)
        heading_2 = ttk.Label(self.body, text = "Price\n ", style='styleconfirm.TLabel').grid(row = 1, column = 1, sticky = W, padx = 10)
        heading_3 = ttk.Label(self.body, text = "Quantity\n ", style='styleconfirm.TLabel').grid(row = 1, column = 2, sticky = W, padx = 10)
        heading_4 = ttk.Label(self.body, text = "Total\n ", style='styleconfirm.TLabel').grid(row = 1, column = 3, sticky = W, padx = 10)

        for rows in range(len(orders)):
            Label(self.body, text = (orders[rows][0])).grid(row = (rows+2), column = 0, sticky = W, padx = 14)
            Label(self.body, text = "${:.2f}".format(float(orders[rows][1]))).grid(row = (rows+2), column = 1, sticky = W, padx = 10)
            Label(self.body, text = (orders[rows][2])).grid(row = (rows+2), column = 2, sticky = W, padx = 10)
            Label(self.body, text = "${:.2f}".format(float(orders[rows][3]))).grid(row = (rows+2), column = 3, sticky = W, padx = 10)

        ttk.Label(self.body, text = "Total: ${:.2f}".format(float(find_total())), style='styleconfirm.TLabel').grid(row = 5, column = 0, sticky = W, padx = 14, pady = 5)

        # insert placeholders here based on size of orders list
        for i in range(3 - len(orders)):
            Label(self.body, text = "").grid(row = (7+i))

        ttk.Button(self.okcancel, text = "Ok", style='blue.TButton', command = self.ok).grid(row = 0, column = 0, padx = 50)
        ttk.Button(self.okcancel, text = "Cancel", command = self.cancel).grid(row = 0, column = 1, padx = 50)

    def ok(self):
        self.top.destroy()
        payment(root)

    def cancel(self):
        self.top.destroy()


class paymentAccepted:
    def __init__(self, parent):
        self.top = Toplevel(parent)
        self.top.grab_set()
        self.top.attributes("-topmost", True) #stays on top
        coord = center_window(350, 200)
        self.top.geometry("350x200+{}+{}".format(str(coord[0]), str(coord[1])))
        self.top.resizable(0,0)

        self.top.title("")

        self.logo = PhotoImage(file = 'tick.png')

        self.paid_msg = ttk.Label(self.top, text = "Payment accepted", style='darkredbigpopup.TLabel')
        self.paid_msg.grid(row = 0, column = 0, pady= 10, padx = 80)
        self.tick_img = Label(self.top, image = self.logo)
        self.tick_img.grid(row = 1, column = 0, padx = 80)
        
        # 2 second delay
        self.top.after(2000, self.order_number)

    def order_number(self):
        self.paid_msg.destroy()
        self.tick_img.destroy()

        order_num = find_order_num()
        ttk.Label(self.top, text = "Thank you!", style='darkredbigpopup.TLabel').grid(row=0,column=0, padx=40,pady=5)
        ttk.Label(self.top, text = "Your order number is", style='popupfont.TLabel').grid(row=1,column=0,padx=40,pady=5)
        order_num_txt = ttk.Label(self.top, text = "{}".format(order_num), style='darkredorderno.TLabel')
        order_num_txt.grid(row=2,column=0, padx=40,pady=5)
        ttk.Label(self.top, text = "Please pick up your order at the front counter", style='popupfont.TLabel').grid(row=3,column=0, padx=20,pady=5)

        for order in orders:
            food_name = order[0]
            quantity = order[2]
            update_sales_count(food_name, quantity)

        print_receipt(orders, order_num)

        # 5 second delay
        self.top.after(2000, self.finish)

    def finish(self):
        self.top.destroy()
        restart()
        
class preorderDialogue:
    def __init__(self, parent):

        self.top = Toplevel(parent)
        self.top.grab_set()
        self.top.attributes("-topmost", True) #stays on top
        coord = center_window(350, 200)
        self.top.geometry("350x200+{}+{}".format(str(coord[0]), str(coord[1])))
        self.top.resizable(0,0)
        
        self.top.title("")
        self.prompt = ttk.Label(self.top, text = "Enter your student ID below",  style='darkredpopup.TLabel').grid(row = 0, column = 0, columnspan = 4, pady = 30, padx = 50)
        
        self.entry_field = Entry(self.top)
        self.entry_field.grid(row = 1, column = 0, columnspan = 4, padx = 50)
        # place holder for error message text 
        self.place_holder = Label(self.top).grid(row = 2, column = 0, columnspan = 4, pady = 5, padx = 50) 
        ttk.Button(self.top, text = "Ok", command = self.ok, style='blue.TButton').grid(row = 3, column = 0, columnspan = 2, pady = 20, padx = 50)
        ttk.Button(self.top, text = "Cancel", command = self.cancel).grid(row = 3, column = 2, columnspan = 2, pady = 20, padx = 50)

    def ok(self):
        global preorder_id

        # checks for valid input
        try: 
            preorder_id = int(self.entry_field.get())

            if 15000 <= preorder_id <= 19999:
                start_menu()
                self.top.destroy()
                return preorder_id
            else:
                # clear input field
                self.entry_field.delete(0, 'end') 
                self.error_msg = ttk.Label(self.top, text = "Please enter a valid student ID",style='rederror.TLabel').grid(row = 2, column = 0, columnspan = 4, pady = 5, padx = 37.5)

        except ValueError:
            self.entry_field.delete(0, 'end')
            self.error_msg = ttk.Label(self.top, text = "Please enter a valid student ID", style='rederror.TLabel').grid(row = 2, column = 0, columnspan = 4, pady = 5, padx = 37.5)

    def cancel(self):

        preorder_id = 0
        self.top.destroy()
        return None


def live_time():
    # keeps time ticking
    global time1
    time1 = ''
    global clock
    clock = ttk.Label(root, style='darkorange.TLabel')
    clock.grid(row = 0, sticky = NW, padx = 10, pady = 5)
    tick()

# clock code below modified from https://stackoverflow.com/questions/15689667/digital-clock-in-status-bar-in-python-3-and-tkinter
def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%I:%M %p').lstrip("0").replace(" 0", " ")
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself to the time display as needed
    clock.after(1000, tick)

def start_screen():
    global orders
    orders = []
    global title
    title = ttk.Label(root, text = "EPSOM EATS",style='darkorange.TLabel', font=('verdana', 50))
    global preorder_button
    preorder_button = Button(root, text = "PRE ORDER", state = check_preorder_time(), command = partial(preorder), font=('verdana', 20, 'bold'), width=15, foreground='#691822',activeforeground="#691822", activebackground="#fdd4b7", background="#fdd4b7")
    global start_button
    
    start_button = Button(root, text = "START ORDER", state = check_startorder_time(), command = partial(start_menu), font=('verdana', 20, 'bold'), width=15, foreground='#691822',activeforeground="#691822", activebackground="#fdd4b7", background="#fdd4b7")
    preorder_button.grid(row = 3, padx = 300, pady = 15)
    start_button.grid(row = 2, padx = 300)
    title.grid(row = 1, padx = 300, pady = 150)
        
    update_buttons()

def start_menu():
    global page_grid
    page_grid = pageGrid(root)
    # remove not needed start screen widgets 
    preorder_button.grid_forget()
    start_button.grid_forget()
    title.grid_forget()


def preorder():
    preorder_dialogue = preorderDialogue(root)


def restart():
    global preorder_id
    orders = []
    preorder_id = 0
    page_grid.frame_header.grid_forget()
    page_grid.body.grid_forget()
    start_screen()

def update_buttons():
    preorder_button.config(state = check_preorder_time())
    preorder_button.update()
    start_button.config(state = check_startorder_time())
    start_button.update()
    root.after(1000, update_buttons)

def check_preorder_time():
    deadlines = [1225, 1225, 1235, 1225, 1250]
    deadline = deadlines[datetime.datetime.today().weekday()] # finds day of the week as index
    if int(time.strftime('%H%M')) >= deadline:
        return "disabled"
    else:
        return "active"

def check_startorder_time():
    deadlines = [1255, 1255, 1305, 1255, 1245]
    deadline = deadlines[datetime.datetime.today().weekday()] # finds day of the week as index
    if int(time.strftime('%H%M')) >= deadline:
        return "disabled"
    else:
        return "active"
    
def find_order_num():
    order_num = ""
    global order_count
    order_count += 1
    
    if preorder_id != 0:
        return str(preorder_id)+str(order_count)
    else: 
        return str(order_count)

def find_total():
    # calculate total for order
    total = 0
    for i in range(len(orders)):
        total += orders[i][3]
    return total
        
def center_window(window_width, window_height):

    coord = []
    pos_right = int(root.winfo_screenwidth()/2 - window_width/2)
    pos_down = int(root.winfo_screenheight()/2 - window_height/2)
    coord.append(pos_right)
    coord.append(pos_down)
    return coord

# updates the sale count on csv file
def update_sales_count(food_name, quantity):
    with open('sales_summary.csv', 'r') as sales_read:
        reader = csv.reader(sales_read)
        output = []
        for line in reader:
            if line[0] == food_name:
                line[1] = str(int(line[1])+ quantity)
            output.append(line)

    with open('sales_summary.csv', 'w', newline='') as sales_write:
        writer = csv.writer(sales_write)
        writer.writerows(output)

def print_receipt(orders, order_num):
    # set up file and insert headings
    receipts = open("receipts.txt","a")
    receipts.write(str("*****Order Number: {}*****\n \n".format(order_num)))
    contents = []
    headings = [change_length("Item", 25), change_length("Price ($)", 15), change_length("Quantity", 14), change_length("Total ($)", 11)]
    contents.append(headings)
    contents.append("")

    total = find_total()

    # format orders into rows 
    for item in orders:
        row = []
        row.append(change_length("{}".format(item[0]), 25))
        row.append(change_length("{:.2f}".format(float(item[1])), 15))
        row.append(change_length("{}".format(item[2]), 14))
        row.append(change_length("{:.2f}".format(item[3]), 11))
        contents.append(row)
        
    for i in contents:
        for x in i:
            receipts.write(str(x)+"")
        receipts.write("\n")
    receipts.write("\nTotal paid: ${:.2f} \n \n".format(float(total)))

    receipts.close()

def change_length(cell_name, character_limit):

    cell_name += (" " * (character_limit-len(cell_name)))  # to fill in the extra spaces 
    return cell_name

if __name__ == "__main__":

    root = Tk()
    root.overrideredirect(1) # clears min/max buttons, close buttons
    coord = center_window(1000, 650)
    root.geometry("1000x650+{}+{}".format(str(coord[0]), str(coord[1]-20))) 

    # Styling
    ttk.Style().configure("TButton", justify = "center")
    ttk.Style().configure("TLabel", justify = "center", font=('verdana', 10))
    ttk.Style().configure("white.TFrame", background='white')
    ttk.Style().configure('blue.TButton', background ='#29ade4')
    ttk.Style().configure('darkorange.TLabel',foreground='#d55435', background='white')
    ttk.Style().configure('darkred.TLabel', foreground='#691822', background='white')
    ttk.Style().configure('darkredpopup.TLabel', foreground='#691822', font=('verdana', 10, 'bold'))
    ttk.Style().configure('styleconfirm.TLabel', forground = '#000000', font=('verdana', 10, 'bold'))
    ttk.Style().configure('darkredbigpopup.TLabel',  foreground='#691822', font=('verdana', 15, 'bold'))
    ttk.Style().configure('darkredorderno.TLabel',  foreground='#691822', font=('verdana', 23,'bold'))
    ttk.Style().configure('rederror.TLabel', foreground ='#ed2024', font=('verdana', 8, 'italic'))
    ttk.Style().configure('menufont.TLabel', font=('verdana', 10, 'bold'),background='white')
    ttk.Style().configure('popupfont.TLabel', font=('verdana', 10))
    root.configure(background="white")

    #opens menu file 
    data = list(csv.reader(open('menu.csv')))
    #passes in heading and rest of rows and collects instances into list
    foods = [food(i, data[0]) for i in data[1:]]

    # extracts food_names as lists in each category
    chilled_button_string = buttonGrid.food_name_price(food.categorise()[0])
    hot_button_string = buttonGrid.food_name_price(food.categorise()[1])
    treats_button_string = buttonGrid.food_name_price(food.categorise()[2])

    # extracts food names as list for summary csv
    food_names = []
    for lines in data:
        food_names.append(lines[0])
    food_names.remove(food_names[0]) # removes heading

    # creates list of 0s
    zero = []
    for i in range(len(food_names)):
        zero.append("0")

    summary_columns = [food_names, zero]

    # places start screen contents
    global order_count
    order_count = 0
    global preorder_id
    preorder_id = 0

    # clear contents from previous day
    receipts = open("receipts.txt","w")
    receipts.close()
    sales_summary = open("sales_summary.csv","w")
    sales_summary.close()

    # resets the amount sold back to zero for the new day (1 day starts when the program is run)
    # code modified from https://stackoverflow.com/questions/17704244/writing-python-lists-to-columns-in-csv
    export_data = zip_longest(*summary_columns, fillvalue = '')
    with open('sales_summary.csv','w', newline='') as sales_write: 
        wr = csv.writer(sales_write)
        wr.writerows(export_data)
    sales_write.close()

    # starts program    
    live_time = live_time()
    start = start_screen()

    root.mainloop()
