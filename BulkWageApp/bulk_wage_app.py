from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import process_data
import constant
from transmitter import Transmitter


class BulkWageApp(Tk):

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)

        self.transmitter = None
        self.employers = []
        self.employer_filenames = []
        self.num_employers = 0
        self.report = None
        self.report_name = ''

        # creating a container
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Root, EnterReportName, SelectNumFiles, SelectFiles, ProcessingPage, ExitPage):
            frame = F(container, self)

            # initializing frame of that object from root, processing page,
            # and processed page respectively with for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")


        #self.show_frame(Root)
        self.show_frame(EnterReportName)

    def add_employer(self, employer):
        self.employers.append(employer)

    # to display the current frame passed as a parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def select_files_load(self, app):
        frame = self.frames[SelectFiles]
        frame.load_buttons(self.num_employers, app)

    def process_data_files(self, app):
        frame = self.frames[ProcessingPage]
        frame.process_files(app)


class Root(Frame):

    def __init__(self, parent, app):
        Frame.__init__(self, parent)

        def create_transmitter():
            is_empty = False
            entry_list = [name, ein, mailing_address, city, state_code, zip_code, contact_name, contact_phone]

            for entry in entry_list:
                is_empty = is_empty or entry_is_empty(entry.get())

            if is_empty:
                instruction_text.set('All entries must be filled')
            else:
                app.transmitter = Transmitter(name.get(), ein.get(), mailing_address.get(), city.get(), state_code.get(),
                                          zip_code.get(), contact_name.get(), contact_phone.get())
                app.show_frame(EnterReportName)

        def entry_is_empty(entry_text):
            return entry_text == ""


        # The variables that we'll need to create the transmitter
        name = StringVar()
        ein = StringVar()
        mailing_address = StringVar()
        city = StringVar()
        state_code = StringVar()
        zip_code = StringVar()
        contact_name = StringVar()
        contact_phone = StringVar()
        instruction_text = StringVar()

        instruction_text.set('Please enter information about the transmitting organization')

        ttk.Label(self, font=('arial', 20, 'bold'), text='Welcome').grid(row=1, column=1)
        ttk.Label(self, font=('arial', 10, 'bold'), textvariable=instruction_text, width=60)\
            .grid(row=2, column=0, columnspan=3, pady=20, padx=25)

        ttk.Label(self, font=('arial', 10), text='Organization Name').grid(row=3, column=0, sticky=E)
        ttk.Label(self, font=('arial', 10), text='EIN').grid(row=3, column=0, columnspan=2, sticky=E)
        ttk.Label(self, font=('arial', 10), text='Mailing Address').grid(row=4, column=0, sticky=E)
        ttk.Label(self, font=('arial', 10), text='City').grid(row=5, column=0, sticky=E)
        ttk.Label(self, font=('arial', 10), text='State Code').grid(row=6, column=1, sticky=E)
        ttk.Label(self, font=('arial', 10), text='Zip').grid(row=6, column=0, sticky=E)
        ttk.Label(self, font=('arial', 10), text='Contact Name').grid(row=7, column=0, sticky=E)
        ttk.Label(self, font=('arial', 10), text='Contact Phone').grid(row=8, column=0)

        alpha = self.register(alpha_check)
        digit = self.register(digit_check)

        ttk.Entry(self, name='name', width=20, textvariable=name).grid(row=3, column=1, padx=15, pady=5, sticky=W)
        ttk.Entry(self, name='ein', width=9, textvariable=ein, validate='key', validatecommand=(digit, '%P', '%W'))\
            .grid(row=3, column=2, padx=15, pady=5, sticky=W)
        ttk.Entry(self, name='mailing_address', width=25, textvariable=mailing_address)\
            .grid(row=4, column=1, padx=15, pady=5, sticky=W)
        ttk.Entry(self, name='city', width=25, textvariable=city, validate='all',
                  validatecommand=(alpha, '%s', '%P', '%d', '%W')).grid(row=5, column=1, padx=15, pady=5, sticky=W)

        # Should the state code be a drop-down? What about international organizations? Make a check box, perhaps
        ttk.Entry(self, name='state_code', width=4, textvariable=state_code, validate='all',
                  validatecommand=(alpha, '%s', '%P', '%d', '%W')).grid(row=6, column=2, padx=15, pady=5, sticky=W)
        ttk.Entry(self, name='zip', width=10, textvariable=zip_code, validate='key',
                  validatecommand=(digit, '%P', '%W')).grid(row=6, column=1, padx=15, pady=5, sticky=W)
        ttk.Entry(self, name='contact_name', width=20, textvariable=contact_name, validate='all',
                  validatecommand=(alpha, '%s', '%P', '%d', '%W')).grid(row=7, column=1, padx=15, pady=5, sticky=W)

        # How to format this correctly...
        ttk.Entry(self, name='contact_phone', width=14, textvariable=contact_phone, validate='key',
                  validatecommand=(digit, '%P', '%W')).grid(row=8, column=1, padx=15, pady=5, sticky=W)

        ttk.Button(self, text='Next', command=create_transmitter).grid(row=9, column=1, pady=20)


class EnterReportName(Frame):
    def __init__(self, parent, app):

        Frame.__init__(self, parent)


        def enter_report_name(name):
            if name.get() != '':
                app.report_name = name.get()
                app.show_frame(SelectNumFiles)
                report_name.set('')


        report_name = StringVar()
        report_name.set('')

        ttk.Label(self, font=('arial', 10, 'bold'), text='Provide a Name for the Report', width=30).grid(row=0, column=0, padx=120, pady=10)
        ttk.Entry(self, textvariable=report_name, width=25).grid(row=1, column=0, padx=10, pady=10)

        ttk.Button(self, text='Next', command=lambda: enter_report_name(report_name)).grid(row=2, column=0, pady=10)


class SelectNumFiles(Frame):

    def __init__(self, parent, app):

        Frame.__init__(self, parent)

        def check_num_employers():
            if num_emps.get() != '':
                num = int(num_emps.get())
                if 0 < num < 21:
                    app.num_employers = num
                    app.show_frame(SelectFiles)
                    app.select_files_load(app)

        def change_report_name():
            num_emps.set('')
            app.report_name = ''
            app.show_frame(EnterReportName)

        digit = self.register(digit_check)
        num_emps = StringVar()
        instruction_text = 'Enter the number of employers in this file (1-20)'

        ttk.Label(self, font=('arial', 10, 'bold'), text=instruction_text).grid(row=0, column=0, columnspan=3, pady=10, padx=75, sticky=E)
        ttk.Entry(self, width=5, textvariable=num_emps, validate='key', validatecommand=(digit, '%P', '%W'))\
            .grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(self, text='Next', command=check_num_employers).grid(row=9, column=2, pady=20)
        ttk.Button(self, text='Back', command=change_report_name).grid(row=9, column=0, pady=10)


class SelectFiles(Frame):

    def __init__(self, parent, app):
        Frame.__init__(self, parent)

        self.filename_text = StringVar()
        self.filename_text.set('')

    def load_buttons(self, num_rows, app):
        app.employer_filenames = [None] * num_rows
        widgets = []
        for i in range(num_rows):
            file_num = ttk.Label(self, text='file {}:'.format(i + 1), font=('arial', 10))
            file_num.grid(row=i, column=0, padx=10, pady=5)
            widgets.append(file_num)

            file_name = ttk.Label(self, text='', width=40, font=('arial', 10))
            file_name.grid(row=i, column=1, padx=20, pady=5)
            widgets.append(file_name)

            button = ttk.Button(self, text='Browse')
            button.grid(row=i, column=2, padx=15, pady=10, sticky=E)
            button.configure(command=lambda b=button, f=file_name: self.browse_files(app, b, f))
            widgets.append(button)

        example = ttk.Button(self, text='File Format Example', command=lambda: self.open_example(app))
        example.grid(row=num_rows + 1, column=1, pady=20)
        widgets.append(example)

        process = ttk.Button(self, text='Process Data', command=lambda: self.process_employer_data(app))
        process.grid(row=num_rows + 2, column=2, pady=10)
        widgets.append(process)

        back = ttk.Button(self, text='Back')
        back.grid(row=num_rows + 2, column=0, pady=10)
        back.configure(command=lambda w=widgets: self.clear_buttons(app, w))
        widgets.append(back)


    @staticmethod
    def clear_buttons(app, widgets):
        for widget in widgets:
            widget.destroy()
        app.show_frame(SelectNumFiles)


    @staticmethod
    def browse_files(app, button, label):
        filename = filedialog.askopenfilename(initialdir='/', title='Select a File',
                                              filetypes=[('CSV files', '*.csv*')])
        short_name = filename.split('/')[-1]
        index = button.grid_info()['row']
        app.employer_filenames[index] = filename
        label['text'] = short_name

        #print(app.employer_filenames)


    @staticmethod
    def open_example():
        f = open("example_file.xlsx", "r")


    @staticmethod
    def process_employer_data(app):
        if None not in app.employer_filenames:
            app.show_frame(ProcessingPage)
            app.process_data_files(app)


class ProcessingPage(Frame):
    def __init__(self, parent, app):
        Frame.__init__(self, parent)

        welcome_text = ttk.Label(self, font=('arial', 20, 'bold'), text='Processing...')
        welcome_text.grid(row=1, column=2, padx=25)

    @staticmethod
    def process_files(app):
        process_data.write_first_line(app.transmitter)
        for file in app.employer_filenames:
            process_data.ingest_data(file, app.report_name)


class ExitPage(Frame):
    def __init__(self, parent, app):
        Frame.__init__(self, parent)

        welcome_text = ttk.Label(self, font=('arial', 20, 'bold'), text='Welcome')

        welcome_text.grid(row=1, column=2, padx=25)




def digit_check(entry, widget_name):
    proceed = True
    result = False

    if 'ein' in widget_name:
        if len(entry) > constant.EIN_LEN:
            proceed = False
    elif 'employer_num_entry' in widget_name:
        if len(entry) > len(str(constant.NUM_EMPLOYERS_ALLOWED)):
            proceed = False

    if proceed:
        if entry.isdigit():
            if 'employer_num_entry' in widget_name:
                if int(entry) <= constant.NUM_EMPLOYERS_ALLOWED:
                    result = True
            else:
                result = True
        elif entry == "":
            result = True

    return result


def alpha_check(current, changed, why, widget_name):
    proceed = True
    result = False

    if why == '0':
        result = True
    else:
        if 'contact_name' in widget_name:
            if len(changed) > constant.CONTACT_NAME_LEN:
                proceed = False
        elif 'city' in widget_name:
            if len(changed) > constant.ENTITY_CITY_LEN:
                proceed = False
        elif 'name' in widget_name:
            if len(changed) > constant.ENTITY_NAME_LEN:
                proceed = False
        elif 'state_code' in widget_name:
            if len(changed) > constant.STATE_CODE_LEN:
                proceed = False

        if proceed:
            addition = changed
            if current in changed:
                addition = changed.replace(current, '')

            if addition.isalpha() or addition == " ":
                result = True

            elif addition == "":
                result = True

    return result





bulk_app = BulkWageApp()
bulk_app.mainloop()



