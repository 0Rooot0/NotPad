import webbrowser
from datetime import datetime
from tkinter import *
import os
import sys
from tkinter import filedialog, colorchooser, messagebox, font
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import jedi
import langid

# Custom TextEditor class inheriting from tkinter's Text widget
class TextEditor(Text):
    def __init__(self, *args, **kwargs):
        # Initialize the superclass
        super().__init__(*args, **kwargs)
        self._orig = ""
        self._undo_stack = []  # Stack to manage undo operations
        self._redo_stack = []  # Stack to manage redo operations
        self._setup_bindings()

    def _setup_bindings(self):
        """
        Sets up key bindings for undo, redo, save, find and replace, autocomplete, and handle return operations.
        """
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)
        self.bind("<Control-s>", self.save)
        self.bind("<Control-f>", self.find_and_replace)
        self.bind("<KeyRelease>", self.update_autocomplete)  # Bind autocomplete
        self.bind("<Return>", self.handle_return)  # For newlines in table

    def undo(self, event=None):
        """
        Undo the last action.
        """
        if self._undo_stack:
            self._redo_stack.append(self.get(1.0, END))
            self.delete(1.0, END)
            self.insert(1.0, self._undo_stack.pop())
            self._orig = self.get(1.0, END)
        else:
            self._redo_stack.append(self.get(1.0, END))
            self.delete(1.0, END)
            self.insert(1.0, self._orig)

    def redo(self, event=None):
        """
        Redo the previously undone action.
        """
        if self._redo_stack:
            self._undo_stack.append(self.get(1.0, END))
            self.delete(1.0, END)
            self.insert(1.0, self._redo_stack.pop())
        else:
            self._undo_stack.append(self.get(1.0, END))
            self.delete(1.0, END)
            self.insert(1.0, self._orig)

    def save(self, event=None):
        """
        Save the content of the editor to a file.
        """
        global filename
        if filename:
            all_text = self.get(1.0, END)
            open(filename, "w").write(all_text)

    def find_and_replace(self, event=None):
        """
        Find and replace functionality.
        """
        def replace_all():
            """
            Replace all occurrences in the text.
            """
            start = "1.0"
            while True:
                start = self.search(find_entry.get(), start, END, nocase=case_var.get())
                if not start:
                    break
                self.delete(start, "%s+%dc" % (start, len(find_entry.get())))
                self.insert(start, replace_entry.get())
                start = "%s+%dc" % (start, len(replace_entry.get()))

        # Create a top-level window for search/replace
        find_replace_window = Toplevel(root)
        find_replace_window.title("Find and Replace")
        find_label = Label(find_replace_window, text="Find:")
        find_label.grid(row=0, column=0, padx=5, pady=5)
        find_entry = Entry(find_replace_window)
        find_entry.grid(row=0, column=1, padx=5, pady=5)
        replace_label = Label(find_replace_window, text="Replace with:")
        replace_label.grid(row=1, column=0, padx=5, pady=5)
        replace_entry = Entry(find_replace_window)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)
        case_var = BooleanVar(value=False)
        case_check = Checkbutton(find_replace_window, text="Match Case", variable=case_var)
        case_check.grid(row=2, columnspan=2, padx=5, pady=5)
        replace_button = Button(find_replace_window, text="Replace", command=replace_all)
        replace_button.grid(row=3, column=0, padx=5, pady=5)
        close_button = Button(find_replace_window, text="Close", command=find_replace_window.destroy)
        close_button.grid(row=3, column=1, padx=5, pady=5)

    def highlight_code(self, code):
        """
        Highlight code syntax using Pygments.
        """
        try:
            lexer = get_lexer_by_name(self.get_language(), stripall=True)
            formatter = HtmlFormatter(style='monokai')  # Choose a style
            highlighted_html = highlight(code, lexer, formatter)
            self.config(state=NORMAL)
            self.delete("1.0", END)
            self.insert("1.0", highlighted_html)
            self.config(state=DISABLED)  # Prevent direct editing of highlighted HTML
        except Exception as e:
            print(f"Error highlighting code: {e}")

    def get_language(self):
        """
        Get the programming language based on the file extension.
        """
        global filename
        if filename:
            _, ext = os.path.splitext(filename)
            if ext == ".py":
                return "python"
            elif ext in [".cpp", ".c"]:
                return "c++"
            elif ext == ".java":
                return "java"
            else:
                return "text"  # Default to plain text
        else:
            return "text"  # Default to plain text
        try:
            language, _ = langid.classify(code)
            return language
        except Exception as e:
            print(f"Error detecting language: {e}")
            return "text"  # Default to plain text if an error occurs

    def update_autocomplete(self, event):
        """
        Update autocomplete suggestions using Jedi.
        """
        line_num = int(self.index("insert").split(".")[0])
        column_num = int(self.index("insert").split(".")[1])
        code_lines = self.get("1.0", END).splitlines()
        current_line = code_lines[line_num - 1]
        script = jedi.Script(source=self.get("1.0", END), line=line_num, column=column_num, path="my_file.py")
        completions = script.complete()
        self.delete("insert -1c", "insert")
        for completion in completions:
            self.insert("insert", f"{completion.name} ")

    def handle_return(self, event):
        """
        Handle the Return key for table input.
        """
        line_num = int(self.index("insert").split(".")[0])
        column_num = int(self.index("insert").split(".")[1])
        if self.compare("insert", "==", f"{line_num}.{column_num}"):
            # For newlines in table mode
            global current_row, current_col, rows, cols, table_frame, table_window
            if hasattr(self, "table_frame") and self.table_frame is not None:
                current_col += 1
                if current_col >= cols:
                    current_row += 1
                    current_col = 0
                    if current_row >= rows:
                        table_string = self._create_table_string()
                        self._insert_table_into_text(table_string)
                        table_window.destroy()
                        self.table_frame.destroy()
                        del self.table_frame
                        return "break"
                next_cell = self.table_frame.grid_slaves(row=current_row, column=current_col)[0]
                next_cell.focus_set()
                return "break"
        else:
            return "break"

    def _create_table_string(self):
        """
        Create a string representation of the table from Entry widgets.
        """
        table_string = ""
        for row in range(rows):
            row_string = ""
            for col in range(cols):
                cell_content = self.table_frame.grid_slaves(row=row, column=col)[0].get()
                row_string += f"| {cell_content} "
            table_string += row_string + "|\n"
        return table_string

    def _insert_table_into_text(self, table_string):
        """
        Insert the table string into the text widget.
        """
        self.insert("insert", table_string)  # Insert the table string
        self.insert("insert", "\n")  # Add a newline for better formatting

# import webbrowser
# from datetime import datetime
# from fileinput import filename
# from tkinter import *
# import os
# import sys
# from tkinter import filedialog
# from tkinter.colorchooser import askcolor
# from tkinter.messagebox import askyesno
# import time
# from tkinter import font
# from pygments import highlight
# from pygments.lexers import get_lexer_by_name
# from pygments.formatters import HtmlFormatter
# import jedi
# import langid
#
# class TextEditor(Text):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._orig = ""
#         self._undo_stack = []
#         self._redo_stack = []
#         self.bind("<Control-z>", self.undo)
#         self.bind("<Control-y>", self.redo)
#         self.bind("<Control-s>", self.save)
#         self.bind("<Control-f>", self.find_and_replace)
#         self.bind("<KeyRelease>", self.update_autocomplete) # Bind autocomplete
#         self.bind("<Return>", self.handle_return)  # For newlines in table
#     def undo(self, event=None):
#         if self._undo_stack:
#             self._redo_stack.append(self.get(1.0, END))
#             self.delete(1.0, END)
#             self.insert(1.0, self._undo_stack.pop())
#             self._orig = self.get(1.0, END)
#         else:
#             self._redo_stack.append(self.get(1.0, END))
#             self.delete(1.0, END)
#             self.insert(1.0, self._orig)
#     def redo(self, event=None):
#         if self._redo_stack:
#             self._undo_stack.append(self.get(1.0, END))
#             self.delete(1.0, END)
#             self.insert(1.0, self._redo_stack.pop())
#         else:
#             self._undo_stack.append(self.get(1.0, END))
#             self.delete(1.0, END)
#             self.insert(1.0, self._orig)
#     def save(self, event=None):
#         global filename
#         if filename:
#             all_text = self.get(1.0, END)
#             open(filename, "w").write(all_text)
#
#     def find_and_replace(self, event=None):
#         def replace_all():
#             # Replace all occurrences in the text
#             start = "1.0"
#             while True:
#                 start = text.search(find_entry.get(), start, END, nocase=case_var.get())
#                 if not start:
#                     break
#                 text.delete(start, "%s+%dc" % (start, len(find_entry.get())))
#                 text.insert(start, replace_entry.get())
#                 start = "%s+%dc" % (start, len(replace_entry.get()))
#
#         # Create a top-level window for search/replace
#         find_replace_window = Toplevel(root)
#         find_replace_window.title("Find and Replace")
#         find_label = Label(find_replace_window, text="Find:")
#         find_label.grid(row=0, column=0, padx=5, pady=5)
#         find_entry = Entry(find_replace_window)
#         find_entry.grid(row=0, column=1, padx=5, pady=5)
#         replace_label = Label(find_replace_window, text="Replace with:")
#         replace_label.grid(row=1, column=0, padx=5, pady=5)
#         replace_entry = Entry(find_replace_window)
#         replace_entry.grid(row=1, column=1, padx=5, pady=5)
#         case_var = BooleanVar(value=False)
#         case_check = Checkbutton(find_replace_window, text="Match Case", variable=case_var)
#         case_check.grid(row=2, columnspan=2, padx=5, pady=5)
#         replace_button = Button(find_replace_window, text="Replace", command=replace_all)
#         replace_button.grid(row=3, column=0, padx=5, pady=5)
#         close_button = Button(find_replace_window, text="Close", command=find_replace_window.destroy)
#         close_button.grid(row=3, column=1, padx=5, pady=5)
#
#     def highlight_code(self, code):
#         try:
#             lexer = get_lexer_by_name(self.get_language(), stripall=True)
#             formatter = HtmlFormatter(style='monokai')  # Choose a style
#             highlighted_html = highlight(code, lexer, formatter)
#             self.config(state=NORMAL)
#             self.delete("1.0", END)
#             self.insert("1.0", highlighted_html)
#             self.config(state=DISABLED)  # Prevent direct editing of highlighted HTML
#         except Exception as e:
#             print(f"Error highlighting code: {e}")
#
#     def get_language(self):
#         global filename  # Access the global filename
#         if filename:
#             _, ext = os.path.splitext(filename)
#             if ext == ".py":
#                 return "python"
#             elif ext == ".cpp" or ext == ".c":
#                 return "c++"  # Or "c" for C language
#             elif ext == ".java":
#                 return "java"
#             else:
#                 return "text"  # Default to plain text
#         else:
#             return "text"  # Default to plain text
#         try:
#             language, _ = langid.classify(code)  # Use langid.classify
#             return language  # Return the detected language code
#         except Exception as e:
#             print(f"Error detecting language: {e}")
#             return "text"  # Default to plain text if an error occurs
#
#     def update_autocomplete(self, event):
#         line_num = int(self.index("@0,0 line"))  # Get current line number
#         column_num = int(self.index("@0,0").split(".")[1])  # Get current column
#         code_lines = self.get("1.0", END).splitlines()  # Get all lines of code
#         current_line = code_lines[line_num - 1]  # Get the current line
#         script = jedi.Script(current_line, path="my_file.py")  # Create Jedi script
#         completions = script.completions()  # Get code completions
#         self.delete("insert -1c", "insert")  # Clear any existing suggestions
#         for completion in completions:
#             self.insert("insert", f"{completion.name} ")  # Add suggestions
#
#     # def handle_return(self, event):
#     #     line_num = int(self.index("@0,0 line"))
#     #     column_num = int(self.index("@0,0").split(".")[1])
#     #     if self.compare("insert", "==", f"{line_num}.{column_num}"):
#     #         # If at the beginning of a new line in table mode, handle table
#     #         global current_row, current_col, rows, cols, table_frame
#     #         if hasattr(self, "table_frame") and table_frame is not None:
#     #             current_col += 1
#     #             if current_col >= cols:
#     #                 current_row += 1
#     #                 current_col = 0
#     #             if current_row >= rows:
#     #                 # Get the table content from the Entry widgets and create the string
#     #                 table_string = ""
#     #                 for row in range(rows):
#     #                     row_string = ""
#     #                     for col in range(cols):
#     #                         cell_content = table_frame.grid_slaves(row=row, column=col)[0].get()
#     #                         row_string += f"| {cell_content} "
#     #                     table_string += row_string + "|\n"
#     #                 # Insert the table string into the text widget
#     #                 self.insert("insert", table_string)  # Insert the table string
#     #                 # Update the text widget to include the table
#     #                 self.insert("insert", "\n")  # Add a newline for better formatting
#     #                 table_window.destroy()
#     #                 table_frame.destroy()  # Destroy the table frame
#     #                 del self.table_frame  # Remove the table_frame attribute
#     #                 return "break"
#     #             next_cell = table_frame.grid_slaves(row=current_row, column=current_col)[0]
#     #             next_cell.focus_set()
#     #             return "break"
#     #     else:
#     #         return "break"
#     def handle_return(self, event):
#         line_num = int(self.index("@0,0 line"))
#         column_num = int(self.index("@0,0").split(".")[1])
#         if self.compare("insert", "==", f"{line_num}.{column_num}"):
#             # If at the beginning of a new line in table mode, handle table
#             global current_row, current_col, rows, cols, table_frame, table_window
#             if hasattr(self, "table_frame") and self.table_frame is not None:
#                 current_col += 1
#                 if current_col >= cols:
#                     current_row += 1
#                     current_col = 0
#                     if current_row >= rows:
#                         # Get the table content from the Entry widgets and create the string
#                         table_string = ""
#                         for row in range(rows):
#                             row_string = ""
#                             for col in range(cols):
#                                 cell_content = self.table_frame.grid_slaves(row=row, column=col)[0].get()
#                                 row_string += f"| {cell_content} "
#                             table_string += row_string + "|\n"
#                         # Insert the table string into the text widget
#                         self.insert("insert", table_string)  # Insert the table string
#                         # Update the text widget to include the table
#                         self.insert("insert", "\n")  # Add a newline for better formatting
#                         table_window.destroy()
#                         self.table_frame.destroy()  # Destroy the table frame
#                         del self.table_frame  # Remove the table_frame attribute
#                         return "break"
#                 next_cell = self.table_frame.grid_slaves(row=current_row, column=current_col)[0]
#                 next_cell.focus_set()
#                 return "break"
#         else:
#             return "break"
#
