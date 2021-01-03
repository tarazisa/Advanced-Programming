from PIL import Image as Img
from PIL import ImageFont, ImageTk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import tksheet
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import seaborn as sb
from scipy.stats import mode


class Prototype(Tk):
    def __init__(self):
        super(Prototype, self).__init__()
        self.initUI()
        self.createWidgets()

    def initUI(self):
        self.title("Prototype")
        self.geometry('1920x1080')
        self.wm_iconbitmap('icon.ico')
        #self.columnconfigure(index=0, weight=1)

    def createWidgets(self):
        self.toolBar()
        self.tabs()
        # self.sheets()

    def toolBar(self):
        self.toolbar = Frame(self, bd=1, relief=RAISED)
        self.img = Img.open("./png/32/Modern3D/objects/exit.png")
        eimg = ImageTk.PhotoImage(self.img)
        exitButton = Button(self.toolbar, image=eimg, relief=FLAT, command=lambda: self.closeApp())
        exitButton.image = eimg
        #exitButton.grid(row=1, column=0, sticky=W)
        #self.toolbar.grid(row=1, column=0, sticky=W)
        exitButton.pack(side=LEFT, padx=2, pady=2)
        self.toolbar.pack(side=TOP, fill=X)

    def closeApp(self):
        result = messagebox.askyesno('Exit', 'Close application?')
        if result:
            self.destroy()

    def onExit(self):
        self.quit()

    def sheets(self) :
        self.sheet = tksheet.Sheet(self.tab3,
                                   page_up_down_select_row=True,
                                    # empty_vertical = 0,
                                    column_width=120,
                                    startup_select=(0, 1, "rows"),
                                    # row_height = "4",
                                    # default_row_index = "numbers",
                                    # default_header = "both",
                                    # empty_horizontal = 0,
                                    # show_vertical_grid = False,
                                    # show_horizontal_grid = False,
                                    # auto_resize_default_row_index = False,
                                    # header_height = "3",
                                    # row_index_width = 100,
                                    # align = "e",
                                    # header_align = "w",
                                    # row_index_align = "w",
                                    # data = [[f"Row {r}, Column {c}\nnewline1\nnewline2" for c in range(50)] for r in range(1000)], #to set sheet data at startup
                                    # headers = [f"Column {c}\nnewline1\nnewline2" for c in range(30)],
                                    # row_index = [f"Row {r}\nnewline1\nnewline2" for r in range(2000)],
                                    # set_all_heights_and_widths = True, #to fit all cell sizes to text at start up
                                    # headers = 0, #to set headers as first row at startup
                                    # headers = [f"Column {c}\nnewline1\nnewline2" for c in range(30)],
                                    # theme = "light green",
                                    # row_index = 0, #to set row_index as first column at startup
                                    # total_rows = 2000, #if you want to set empty sheet dimensions at startup
                                    # total_columns = 30, #if you want to set empty sheet dimensions at startup
                                    height=500,  # height and width arguments are optional
                                    width=1200  # For full startup arguments see DOCUMENTATION.md
                                    )
        self.sheet.grid()
        # table enable choices listed below:
        self.sheet.enable_bindings(("single_select", "row_select", "column_width_resize",
                                    "arrowkeys", "right_click_popup_menu", "rc_select", "rc_insert_row",
                                    "rc_delete_row", "copy", "cut", "paste", "delete", "undo", "edit_cell"))

    def display_figure(self, fig) :
        canvas = FigureCanvasTkAgg(fig, master=self.tab2)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)

    def tabs(self):
        self.tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Initialize')
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text='Clean Up')
        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab3, text='Visualize')
        self.tabControl.pack(expand=1, fill="both")
        #self.tabControl.grid(row=2, column=0, sticky=W)
        # INVENTORY FILE
        ttk.Label(self.tab1, text="Inventory").grid(column=0, row=0,
                                                    padx=10, pady=10,
                                                    sticky=W)
        self.invt_file = StringVar()
        self.invt_file_ent = ttk.Entry(self.tab1, width=50, textvariable=self.invt_file)
        self.invt_file_ent.grid(column=1, row=0, padx=10, pady=10, sticky=W)
        self.invt_browse_btn = ttk.Button(self.tab1, text="Browse",
                                          command=lambda:
                                          self.entrySetText(self.invt_file_ent,
                                                            self.fileDialog()))
        self.invt_browse_btn.grid(column=2, row=0)
        # INSPECTIONS
        ttk.Label(self.tab1, text="Inspections").grid(column=0, row=1, padx=10, pady=10, sticky=W)
        self.insp_file = StringVar()
        self.insp_file_ent = ttk.Entry(self.tab1, width=50, textvariable=self.insp_file)
        self.insp_file_ent.grid(column=1, row=1, padx=10, pady=10)
        self.insp_browse_btn = ttk.Button(self.tab1, text="Browse",
                                          command=lambda:
                                          self.entrySetText(self.insp_file_ent,
                                                            self.fileDialog()))
        self.insp_browse_btn.grid(column=2, row=1)
        # VIOLATIONS
        ttk.Label(self.tab1, text="Violations").grid(column=0, row=2, padx=10, pady=10, sticky=W)
        self.viol_file = StringVar()
        self.entry_viol_file = ttk.Entry(self.tab1, width=50, textvariable=self.viol_file)
        self.entry_viol_file.grid(column=1, row=2, padx=10, pady=10)
        self.viol_browse_btn = ttk.Button(self.tab1, text="Browse",
                                          command=lambda:
                                          self.entrySetText(self.entry_viol_file,
                                                            self.fileDialog()))
        self.viol_browse_btn.grid(column=2, row=2)

    def fileDialog(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select A File",
                                              filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        return filename

    def entrySetText(self, e, text):
        e.delete(0, END)
        e.insert(0, text)

def init():
    # set pd options
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)


def loadData(file_name, parse_dates=None):
    # load the three data sets 
    if parse_dates:
        return pd.read_csv(file_name, parse_dates=parse_dates)
    else:
        return pd.read_csv(file_name)


# create a function to extract and clean up PED 
def extractPED(df):
    df['PE DESCRIPTION'] = df['PE DESCRIPTION'].str.strip()
    ped = df["PE DESCRIPTION"].str.extract("\((.*?)\)").set_axis(['PED'], axis = 1)
    ped["PED"] = ped["PED"].replace({'SQ. FT.': 'SF'}, regex=True)
    ped["PED"].replace({"\d{1,3}(?=(\d{3})+(?!\d))":"\g<0>,"}, regex=True, inplace = True)
    ped[ped["PED"].str.match(".*\,\d{3}\s\+")==True] += " SF"
    return ped


def cleanUpInspectionData(df):
    # find the INACTIVE
    index = df[(df['PROGRAM STATUS']=="INACTIVE")].index
    # drop the rows
    df.drop(index , inplace=True)   
    # extract and clean up PED for two instances
    df['PED'] = extractPED(df)
    # clean up Zip code from +4 as we are interested in the area and not specific address
    df['FACILITY ZIP'] = df['FACILITY ZIP'].str[:5]
    # check for any bad ZIP containing letters
    df["FACILITY ZIP"].replace({"\w*[a-zA-Z]\w*":"99999"}, regex=True, inplace=True)
    # drop the rows that contain a null zip
    index = df[df['FACILITY ZIP'].isnull()].index
    df.drop(index, inplace=True)
    # change to numeric value 
    df["FACILITY ZIP"] = df["FACILITY ZIP"].str[:5].astype(int)


def cleanUpInventoryData(df):
    df['PED'] = extractPED(df)


#insp = loadData("Inspections.csv", parse_dates=['ACTIVITY DATE'])
#viol = loadData("violations.csv")
#invt = loadData("Inventroy.csv")

#cleanUpInspectionData(insp)
#cleanUpInventoryData(invt)

# Produce a suitable graph that displays the number of establishments that have committed
# each type of violation, you may need to consider how you group this data to make visualisation
# feasible.
#left = insp[['FACILITY ID','FACILITY NAME','SERIAL NUMBER','FACILITY ZIP']]
#right = viol[['SERIAL NUMBER','VIOLATION CODE']]
#join = pd.merge(left, right, on='SERIAL NUMBER', how='left')
# setup the plot data
#plot_data = pd.DataFrame()
#plot_data[['Violation Code','Count']] = join.groupby(["VIOLATION CODE"])["FACILITY ID"].count().reset_index()
# setup and generate the graph
#sb.set(style="darkgrid")
#fig, ax = plt.subplots(figsize=(30, 10))
#g = sb.barplot(ax=ax, x="Violation Code", y="Count", data=plot_data)
#color=cmap(norm(plot_data.Count.values))
#plt.xticks(rotation=90)
# self.sheet.set_sheet_data([[f"{ri+cj}" for cj in range(4)] for ri in range(1)])
#print([[f"{ri,cj}" for cj in insp.columns.values] for ri in range(1)])
#print([[f"{str(ri)+str(cj)}" for cj in insp.iloc[ri, :]] for ri in range(10)])

#plt.show()
app = Prototype()
#app.display_figure(fig)
app.mainloop()
