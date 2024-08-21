import webbrowser
from datetime import datetime
from tkinter import *
from tkinter import filedialog, colorchooser, messagebox, ttk
import os
import sys
import time
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import jedi
import langid
import requests
import json
import string
from textblob import TextBlob
from collections import Counter
import random

# Class for advanced AI functionalities
class AdvancedAI:
    def __init__(self):
        self.conversation_history = []

    def preprocess(self, text):
        """
        Preprocess the input text by making it lowercase and removing punctuation.
        """
        text = text.lower()
        text = ''.join([char for char in text if char not in string.punctuation])
        tokens = text.split()
        return tokens

    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of the text using TextBlob.
        Returns the sentiment polarity.
        """
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        return sentiment

    def extract_keywords(self, text):
        """
        Extract keywords from the text.
        Returns the top 5 common words.
        """
        tokens = self.preprocess(text)
        counter = Counter(tokens)
        most_common = counter.most_common(5)
        keywords = [word for word, freq in most_common]
        return keywords

    def generate_response(self, user_input):
        """
        Generate a response based on user input.
        Handles various text commands for word count, character count,
        text transformation, sentiment analysis, and keyword extraction.
        """
        tokens = self.preprocess(user_input)
        processed_input = ' '.join(tokens)

        # Example of handling a specific user input
        if "word count" in processed_input:
            word_count = len(text.get("1.0", END).split())
            return f"The current word count is {word_count}."
        elif "character count" in processed_input:
            char_count = len(text.get("1.0", END)) - 1
            return f"The current character count is {char_count}."
        elif "uppercase" in processed_input:
            current_text = text.get("1.0", END)
            text.delete("1.0", END)
            text.insert(END, current_text.upper())
            return "Text converted to uppercase."
        elif "lowercase" in processed_input:
            current_text = text.get("1.0", END)
            text.delete("1.0", END)
            text.insert(END, current_text.lower())
            return "Text converted to lowercase."
        # Add additional handling for other inputs...

        # Default response for unrecognized input
        return random.choice([
            "I'm not sure how to respond to that. Can you rephrase?",
            "That's an interesting point. Can you elaborate?",
            "I'm still learning. What else can you tell me about that?",
            "I don't have enough information to respond accurately. Can you provide more context?"
        ])

# Function to create and manage the Advanced AI Assistant window
def custom_ai_assistant():
    ai = AdvancedAI()
    ai_window = Toplevel(root)
    ai_window.title("Advanced AI Assistant")
    ai_window.geometry("500x600")

    # Chat frame and text widget for displaying conversation
    chat_frame = Frame(ai_window)
    chat_frame.pack(fill=BOTH, expand=True)
    chat_text = Text(chat_frame, state='disabled', wrap=WORD)
    chat_text.pack(side=LEFT, fill=BOTH, expand=True)
    chat_scrollbar = Scrollbar(chat_frame, command=chat_text.yview)
    chat_scrollbar.pack(side=RIGHT, fill=Y)
    chat_text.config(yscrollcommand=chat_scrollbar.set)

    # Input frame and entry widget for user input
    input_frame = Frame(ai_window)
    input_frame.pack(fill=X, side=BOTTOM)
    input_field = Entry(input_frame)
    input_field.pack(side=LEFT, fill=X, expand=True)

    def send_message():
        """
        Send the user message to the AI and display the response.
        """
        user_message = input_field.get()
        input_field.delete(0, END)
        chat_text.config(state='normal')
        chat_text.insert(END, f"You: {user_message}\n")
        ai_reply = ai.generate_response(user_message)
        chat_text.insert(END, f"AI: {ai_reply}\n\n")
        chat_text.config(state='disabled')
        chat_text.see(END)

    send_button = Button(input_frame, text="Send", command=send_message)
    send_button.pack(side=RIGHT)
    input_field.bind("<Return>", lambda event: send_message())

    def show_help():
        """
        Show help dialog for using the Advanced AI Assistant.
        """
        help_text = (
            "Advanced AI Assistant Help:\n\n"
            "- Word count: Get the current word count\n"
            "- Character count: Get the current character count\n"
            "- Uppercase: Convert text to uppercase\n"
            "- Lowercase: Convert text to lowercase\n"
            "- Clear: Clear all text\n"
            "- Sentiment: Analyze the sentiment of the text\n"
            "- Keywords: Extract top keywords from the text\n"
            "\nYou can also have a conversation with the AI about various topics!"
        )
        messagebox.showinfo("AI Assistant Help", help_text)

    help_button = Button(input_frame, text="Help", command=show_help)
    help_button.pack(side=RIGHT)

# Function to setup the menu with AI interaction options
def setup_menu(root, text, main_menu):
    ai_menu = Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label="AI", menu=ai_menu)
    ai_menu.add_command(label="Open Advanced AI Assistant", command=custom_ai_assistant)

def api_interaction():
    """
    Create a window for API interaction with multiple tabs:
    - Fetch and display posts
    - Fetch and display users
    - Create a new post
    """
    api_window = Toplevel(root)
    api_window.title("API Interaction")
    api_window.geometry("500x600")

    # Create a notebook (tabbed interface)
    notebook = ttk.Notebook(api_window)
    notebook.pack(fill=BOTH, expand=True)

    # Posts tab
    posts_frame = ttk.Frame(notebook)
    notebook.add(posts_frame, text="Posts")
    posts_text = Text(posts_frame, wrap=WORD)
    posts_text.pack(fill=BOTH, expand=True)

    def fetch_posts():
        """
        Fetch posts from an external API and display them in the text widget.
        """
        try:
            response = requests.get("https://jsonplaceholder.typicode.com/posts")
            posts = response.json()
            posts_text.delete('1.0', END)
            posts_text.insert(END, json.dumps(posts, indent=2))
        except Exception as e:
            posts_text.delete('1.0', END)
            posts_text.insert(END, f"Error: {str(e)}")

    fetch_posts_button = Button(posts_frame, text="Fetch Posts", command=fetch_posts)
    fetch_posts_button.pack()

    # Users tab
    users_frame = ttk.Frame(notebook)
    notebook.add(users_frame, text="Users")
    users_text = Text(users_frame, wrap=WORD)
    users_text.pack(fill=BOTH, expand=True)

    def fetch_users():
        """
        Fetch users from an external API and display them in the text widget.
        """
        try:
            response = requests.get("https://jsonplaceholder.typicode.com/users")
            users = response.json()
            users_text.delete('1.0', END)
            users_text.insert(END, json.dumps(users, indent=2))
        except Exception as e:
            users_text.delete('1.0', END)
            users_text.insert(END, f"Error: {str(e)}")

    fetch_users_button = Button(users_frame, text="Fetch Users", command=fetch_users)
    fetch_users_button.pack()

    # Create Post tab
    create_post_frame = ttk.Frame(notebook)
    notebook.add(create_post_frame, text="Create Post")
    title_label = Label(create_post_frame, text="Title:")
    title_label.pack()
    title_entry = Entry(create_post_frame)
    title_entry.pack()
    body_label = Label(create_post_frame, text="Body:")
    body_label.pack()
    body_text = Text(create_post_frame, height=5)
    body_text.pack()
    result_text = Text(create_post_frame, wrap=WORD)
    result_text.pack(fill=BOTH, expand=True)

    def create_post():
        """
        Create a new post using an external API and display the response.
        """
        try:
            data = {
                'title': title_entry.get(),
                'body': body_text.get('1.0', END).strip(),
                'userId': 1  # Using a default userId
            }
            response = requests.post("https://jsonplaceholder.typicode.com/posts", json=data)
            result = response.json()
            result_text.delete('1.0', END)
            result_text.insert(END, json.dumps(result, indent=2))
        except Exception as e:
            result_text.delete('1.0', END)
            result_text.insert(END, f"Error: {str(e)}")
    create_post_button = Button(create_post_frame, text="Create Post", command=create_post)
    create_post_button.pack()

# Function to create a new file
def new_file():
    global filename
    if askyesno("NotPad", "Save Existing Work?"):
        filename = filedialog.asksaveasfilename()
        if filename:
            all_text = text.get(1.0, END)
            open(filename, "w").write(all_text)
    if askyesno("NotPad", "Open Existing Work?"):
        text.delete(1.0, END)
        file = open(filedialog.askopenfilename(), "r")
        if file != "":
            txt = file.read()
            text.insert(INSERT, txt)
        else:
            text.delete(1.0, END)

# Function to open an existing file
def open_file():
    global filename
    text.delete(1.0, END)
    file = open(filedialog.askopenfilename(), "r")
    if file != "":
        txt = file.read()
        text.insert(INSERT, txt)
        filename = filedialog.askopenfilename()
    else:
        pass

# Function to save the current file with a new name
def save_as():
    global filename
    filename = filedialog.asksaveasfilename()
    if filename:
        all_text = text.get(1.0, END)
        open(filename, "w").write(all_text)

# Function to close the application, optionally saving the current work
def close():
    global filename
    if askyesno("NotPad", "Save Existing Work?"):
        filename = filedialog.asksaveasfilename()
        if filename:
            all_text = text.get(1.0, END)
            open(filename, "w").write(all_text)
        root.destroy()
    else:
        root.destroy()

# Function to cut the selected text
def cut():
    text.clipboard_clear()
    text.clipboard_append(text.selection_get())
    selection = text.get(SEL_FIRST, SEL_LAST)
    text.delete(SEL_FIRST, SEL_LAST)

# Function to copy the selected text
def copy():
    text.clipboard_clear()
    text.clipboard_append(text.selection_get())

# Function to paste text from the clipboard
def paste():
    try:
        txt = text.selection_get(selection="CLIPBOARD")
        text.insert(INSERT, txt)
    except:
        pass

# Function to delete the selected text
def erase():
    selection = text.get(SEL_FIRST, SEL_LAST)
    text.delete(SEL_FIRST, SEL_LAST)

# Function to clear the entire text widget
def clear_screen():
    text.delete(1.0, END)

# Function to insert the current date
def date():
    data = datetime.today()
    text.insert(INSERT, data)

# Function to change the text color
def text_color():
    (triple, color) = colorchooser.askcolor()
    if color:
        text.config(foreground=color)

# Function to reset text formatting to the default
def no_format():
    text.config(font=("Arial", 20))

# Function to toggle fullscreen mode
def toggle_fullscreen(event=None):
    state = root.state()
    if state == "normal":
        root.state("zoomed")
    else:
        root.state("normal")

# Function to apply bold formatting to the selected text
def bold():
    current_tags = text.tag_names("sel.first")
    if "bt" in current_tags:
        text.tag_remove("bt", "sel.first", "sel.last")
        text.tag_config("bt", font=("Arial", 20, "bold"))
    else:
        text.tag_add("bt", "sel.first", "sel.last")
        text.tag_config("bt", font=("Arial", 20, "bold"))

# Function to apply italic formatting to the selected text
def italic():
    current_tags = text.tag_names("sel.first")
    if "bt" in current_tags:
        text.tag_remove("bt", "sel.first", "sel.last")
        text.tag_config("bt", font=("Arial", 20, "italic"))
    else:
        text.tag_add("bt", "sel.first", "sel.last")
        text.tag_config("bt", font=("Arial", 20, "italic"))

# Function to apply underline formatting to the selected text
def underline():
    text.tag_add("here", "1.0", "1.4")
    text.tag_config("here", font=("Arial", 20, "underline"))

# Function to change the background color
def background():
    (triple, color) = colorchooser.askcolor()
    if color:
        text.config(background=color)

# Function to open online help
def online_help():
    def search_web():
        query = search_entry.get()
        if query:
            webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
            help_window.destroy()
    help_window = Toplevel(root)
    help_window.title("Online Help")
    search_label = Label(help_window, text="What seems to be the problem?")
    search_label.pack(pady=10)
    search_entry = Entry(help_window)
    search_entry.pack()
    search_button = Button(help_window, text="Search", command=search_web)
    search_button.pack(pady=10)
    search_entry.focus_set()

# Function to auto-save the file every minute
def auto_save():
    global filename
    if filename:
        all_text = text.get(1.0, END)
        open(filename, "w").write(all_text)
    root.after(60000, auto_save)

# Function to show the line numbers in the text widget
def show_line_numbers(event=None):
    line_number_label.config(text=text.index("@0,0 line"))

# Function to update the status bar with the current line and column
def update_status_bar(event=None):
    line, column = map(int, text.index("@0,0").split("."))
    status_bar.config(text=f"Line: {line + 1}, Column: {column + 1}")

# Function to toggle word wrap in the text widget
def toggle_word_wrap(event=None):
    if word_wrap_var.get():
        text.config(wrap=WORD)
    else:
        text.config(wrap=NONE)

# Function to change the font of the text widget
def change_font(event=None):
    selected_font = font_var.get()
    text.config(font=(selected_font, 10))  # Adjust font size as needed

# Function to align the selected text to the left
def align_left():
    text.tag_add("left", "sel.first", "sel.last")
    text.tag_config("left", justify="left")

# Function to align the selected text to the center
def align_center():
    text.tag_add("center", "sel.first", "sel.last")
    text.tag_config("center", justify="center")

# Function to align the selected text to the right
def align_right():
    text.tag_add("right", "sel.first", "sel.last")
    text.tag_config("right", justify="right")

# Function to create a numbered list from the selected text
def create_numbered_list():
    selected_text = text.get("sel.first", "sel.last")
    lines = selected_text.splitlines()
    numbered_list = "\n".join(f"{i+1}. {line}" for i, line in enumerate(lines))
    text.delete("sel.first", "sel.last")
    text.insert("sel.first", numbered_list)

# Function to create a bulleted list from the selected text
def create_bulleted_list():
    selected_text = text.get("sel.first", "sel.last")
    lines = selected_text.splitlines()
    bulleted_list = "\n".join(f"- {line}" for line in lines)
    text.delete("sel.first", "sel.last")
    text.insert("sel.first", bulleted_list)

# Function to indent the selected text
def indent():
    text.insert("insert", "    ")

# Function to unindent the selected text
def unindent():
    start_index = "insert linestart"
    end_index = "insert lineend"
    selected_text = text.get(start_index, end_index)
    if selected_text.startswith("    "):
        text.delete(start_index, end_index)
        text.insert(start_index, selected_text[4:])

# Function to create a table
def create_table():
    def insert_table():
        rows = int(rows_entry.get())
        cols = int(cols_entry.get())
        table_frame = Frame(root)
        for row in range(rows):
            for col in range(cols):
                cell = Entry(table_frame)
                cell.grid(row=row, column=col, padx=5, pady=5)
        table_frame.pack()
        text.insert("insert", "\n")
        table_window.destroy()
    table_window = Toplevel(root)
    table_window.title("Create Table")
    rows_label = Label(table_window, text="Number of Rows:")
    rows_label.grid(row=0, column=0, padx=5, pady=5)
    rows_entry = Entry(table_window)
    rows_entry.grid(row=0, column=1, padx=5, pady=5)
    cols_label = Label(table_window, text="Number of Columns:")
    cols_label.grid(row=1, column=0, padx=5, pady=5)
    cols_entry = Entry(table_window)
    cols_entry.grid(row=1, column=1, padx=5, pady=5)
    create_button = Button(table_window, text="Create", command=insert_table)
    create_button.grid(row=2, columnspan=2, padx=5, pady=5)

# Function to handle resizing of the window
def on_resize(event):
    text.config(width=event.width, height=event.height)

# Function to handle find and replace operations
def find_and_replace_wrapper(text):
    def replace_all():
        """
        Replace all occurrences of the search term with the replace term.
        """
        start = "1.0"
        while True:
            start = text.search(find_entry.get(), start, END, nocase=case_var.get())
            if not start:
                break
            text.delete(start, "%s+%dc" % (start, len(find_entry.get())))
            text.insert(start, replace_entry.get())
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

# Initialize Tkinter root
root = Tk()
root.title("NotPad")
root.geometry("800x600")

# Create main menu
main_menu = Menu(root)
commands = Menu(main_menu)
root.config(menu=main_menu)
main_menu.add_cascade(label="File", menu=commands)
commands.add_command(label="New File", command=new_file)
commands.add_command(label="Open", command=open_file)
commands.add_command(label="Save As", command=save_as)
commands.add_command(label="Close", command=close)

# Edit menu setup
edit_menu = Menu(main_menu)
main_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Delete", command=erase)
edit_menu.add_command(label="Clear Screen", command=clear_screen)
edit_menu.add_command(label="Find and Replace", command=lambda: find_and_replace_wrapper(text))

# View menu setup
view_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Toggle Fullscreen", command=toggle_fullscreen)

# Insert menu setup
insert_menu = Menu(main_menu)
main_menu.add_cascade(label="Insert", menu=insert_menu)
insert_menu.add_command(label="Current Date", command=date)

# Format menu setup
change_format = Menu(main_menu)
main_menu.add_cascade(label="Format", menu=change_format)
change_format.add_command(label="Font", command=text_color)
change_format.add_command(label="No Format", command=no_format)
change_format.add_command(label="Bold", command=bold)
change_format.add_command(label="Italic", command=italic)
change_format.add_command(label="Underline", command=underline)
change_format.add_separator()
change_format.add_command(label="Align Left", command=align_left)
change_format.add_command(label="Align Center", command=align_center)
change_format.add_command(label="Align Right", command=align_right)
change_format.add_separator()
change_format.add_command(label="Numbered List", command=create_numbered_list)
change_format.add_command(label="Bulleted List", command=create_bulleted_list)
change_format.add_separator()
change_format.add_command(label="Create Table", command=create_table)

# Personalize menu setup
personalize = Menu(main_menu)
main_menu.add_cascade(label="Personalize", menu=personalize)
personalize.add_command(label="Background", command=background)

# Help menu setup
user_help = Menu(main_menu)
main_menu.add_cascade(label="Help", menu=user_help)
user_help.add_command(label="Online Help", command=online_help)

# AI menu and API menu setup
setup_menu(root, Text, main_menu)

# Text widget setup
text = Text(root, height=40, width=100, font=("Arial", 10))
scroll_bar = Scrollbar(root, command=text.yview)
text.config(yscrollcommand=scroll_bar.set)
scroll_bar.pack(side=RIGHT, fill=Y)
text.pack()

# Line Number Frame
line_number_frame = Frame(root, width=30)
line_number_frame.pack(side=LEFT, fill=Y)
line_number_label = Label(line_number_frame, text="1", font=("Arial", 10), anchor="nw")
line_number_label.pack(side=TOP, fill=Y)

# Status Bar
status_bar = Label(root, text="NotPad", anchor=W)
status_bar.pack(side=BOTTOM, fill=X)

# Word Wrap Option
word_wrap_var = BooleanVar(value=False)
word_wrap_check = Checkbutton(root, text="Word Wrap", variable=word_wrap_var, command=toggle_word_wrap)
word_wrap_check.pack(side=BOTTOM, anchor=W)

# Font Selection OptionMenu
font_var = StringVar(root)
font_var.set("Arial")
font_options = ["Arial", "Courier", "Times New Roman", "Verdana"]
font_menu = OptionMenu(root, font_var, *font_options, command=change_font)
font_menu.pack(side=BOTTOM, anchor=W)

# Indent and Unindent Buttons
indent_button = Button(root, text="Indent", command=indent)
indent_button.pack(side=BOTTOM, anchor=W)
unindent_button = Button(root, text="Unindent", command=unindent)
unindent_button.pack(side=BOTTOM, anchor=W)

# Set filename to None initially
filename = None

# Auto-save setup
auto_save()

# Bindings for line numbers and status bar updates
text.bind("<KeyRelease>", update_status_bar)
text.bind("<Return>", show_line_numbers)
text.bind("<BackSpace>", show_line_numbers)
text.bind("<Delete>", show_line_numbers)
text.bind("<Control-a>", show_line_numbers)
text.bind("<Control-Home>", show_line_numbers)

# Bindings for toggle fullscreen and resize events
root.bind("<F11>", toggle_fullscreen)
root.bind("<Configure>", on_resize)
api_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="API", menu=api_menu)
api_menu.add_command(label="Open API Interface", command=api_interaction)
# Main loop
if __name__ == "__main__":
    root.mainloop()

