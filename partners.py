from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivymd.uix.list import MDList, OneLineListItem, OneLineAvatarListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.textinput import TextInput
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.button import MDFloatingActionButton
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from functools import partial
from kivymd.uix.gridlayout import MDGridLayout 
from kivy.uix.widget import WidgetException
import requests
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.uix.stencilview import StencilView
import sqlite3

# Set the window size to mobile dimensions for desktop testing
Window.size = (360, 640)

# Database connection function
def connect_db():
    conn = sqlite3.connect('users.db')
    return conn

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

        # Main Layout
        main_layout = MDBoxLayout(orientation='vertical', padding=[20, 40, 20, 20], spacing=10)

        # Title Layout
        title_layout = MDBoxLayout(height=80, padding=[0, 20, 0, 10])
        title_layout.add_widget(MDLabel(text='JOURNEY', font_style='H4', halign="center"))

        # Form Layout
        form_layout = MDBoxLayout(orientation='vertical', padding=[0, 10, 0, 100], spacing=10)
        self.email = MDTextField(hint_text='Email', mode="rectangle", icon_right= "email",  size_hint_x=0.9, pos_hint={'center_x': 0.5})
        self.password = MDTextField(hint_text='Password', password=True, mode="rectangle",  icon_right= "lock", size_hint_x=0.9, pos_hint={'center_x': 0.5})

        form_layout.add_widget(self.email)
        form_layout.add_widget(self.password)

        form_layout.add_widget(Widget(size_hint_y=None, height=10))
        self.login_button = MDRaisedButton(
            text='Sign In',
            size_hint=(0.8, None),
            height=50,
            pos_hint={'center_x': .5},
            md_bg_color=get_color_from_hex("#FA4032")
        )
        self.login_button.bind(on_press=self.validate_login)
        form_layout.add_widget(self.login_button)

        # Replace the Sign Up button with a label containing clickable text
        signup_layout = MDBoxLayout(size_hint_y=None, height=30, padding=[0, 0, 0, 0])
        signup_label = MDLabel(
            text="Don't have an account? [u][color=#FA4032]Sign up[/color][/u]",
            markup=True,
            halign="center",
            size_hint_y=None,
            height=30
        )
        signup_label.bind(on_touch_down=self.go_to_register)  # Detect clicks on the label
        signup_layout.add_widget(signup_label)
        form_layout.add_widget(signup_layout)

        main_layout.add_widget(title_layout)
        main_layout.add_widget(form_layout)

        self.add_widget(main_layout)

    def validate_login(self, instance):
        """Validate login credentials."""
        email = self.email.text
        password = self.password.text

        # Connect to the database
        conn = connect_db()
        c = conn.cursor()
        try:
            # Fetch user matching the provided email and password
            c.execute("SELECT id, email, password FROM partners WHERE email=? AND password=?", (email, password))
            user = c.fetchone()

            if user:
                # Store the user ID in the app's global state
                app = MDApp.get_running_app()
                app.current_user_id = user[0]
                print("Login successful: User ID:", user[0])

                # Navigate to the dashboard or home screen
                self.manager.current = 'home'
            else:
                self.show_error_message("Invalid email or password.")
        except Exception as e:
            print("Error during login:", e)
            self.show_error_message("An error occurred. Please try again.")
        finally:
            conn.close()

    def go_to_register(self, instance, touch):
        """Navigate to the register screen if the text is clicked."""
        if instance.collide_point(*touch.pos):  # Ensure the click is on the label
            print("Navigating to the registration screen...")
            self.manager.current = 'register'

    def show_error_message(self, message):
        """Display an error dialog."""
        if not self.dialog:  # Prevent creating multiple dialog instances
            self.dialog = MDDialog(
                text=message,
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.text = message
        self.dialog.open()

    def close_dialog(self, instance):
        """Close the error dialog."""
        self.dialog.dismiss()
        self.dialog = None

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None  # Initialize the dialog attribute

        layout = AnchorLayout(anchor_x='center', anchor_y='center') 
        layout = MDBoxLayout(orientation='vertical', padding=[0,0,0,125], spacing=25, size_hint=(1, None))
        layout.height = 400

        self.username = MDTextField(hint_text='Username', mode="rectangle", size_hint_x=0.8, pos_hint={'center_x': 0.5})
        self.email = MDTextField(hint_text='Email', mode="rectangle", size_hint_x=0.8, pos_hint={'center_x': 0.5})
        self.password = MDTextField(hint_text='Password', password=True, mode="rectangle", size_hint_x=0.8, pos_hint={'center_x': 0.5})
        self.confirm_password = MDTextField(hint_text='Confirm Password', password=True, mode="rectangle", size_hint_x=0.8, pos_hint={'center_x': 0.5})
        
        layout.add_widget(MDLabel(text='Register', font_style='H4', halign="center", size_hint_y=None, height=50))
        layout.add_widget(self.username)
        layout.add_widget(self.email)
        layout.add_widget(self.password)
        layout.add_widget(self.confirm_password)
        
        self.register_button = MDRaisedButton(text='Sign Up', size_hint=(0.5, None), height=50, pos_hint={'center_x': .5},  md_bg_color=get_color_from_hex("#FA4032"),)
        self.register_button.bind(on_press=self.register_user)
        layout.add_widget(self.register_button)
        
        self.back_button = MDRaisedButton(text='Back to Login', size_hint=(0.5, None), height=50, pos_hint={'center_x': .5},  md_bg_color=get_color_from_hex("#FA4032"),)
        self.back_button.bind(on_press=self.go_back_to_login)
        layout.add_widget(self.back_button)

        self.add_widget(layout)

    def show_error_message(self, message):
        if not self.dialog:  # Prevent creating multiple dialog instances
            self.dialog = MDDialog(
                text=message,
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.text = message
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()
        self.dialog = None

    def register_user(self, instance):
        email = self.email.text.strip()
        password = self.password.text.strip()
        confirm_password = self.confirm_password.text.strip()

        # Check if any fields are empty
        if not email or not password or not confirm_password:
            self.show_error_message("All fields are required!")
            return

        # Check if passwords match
        if password != confirm_password:
            self.show_error_message("Passwords don't match!")
            return

        # Proceed with database operations if validation passes
        conn = connect_db()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            self.manager.current = 'login'
            self.show_error_message("Succesful!")
        except sqlite3.IntegrityError:
            self.show_error_message("User already exists!")
        finally:
            conn.close()

    def go_back_to_login(self, instance):
        self.manager.current = 'login'

# Your database integration function (replace this with your actual implementation)
def save_to_database(place_name, description, image_path):
    # Add logic to save data to your database
    print(f"Saved: {place_name}, {description}, {image_path}")

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Database connection
def connect_to_database():
    conn = sqlite3.connect("users.db")  # Replace 'places.db' with your database file name
    return conn

def save_to_database(place_name, description, image_path):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO places (name, description, image) VALUES (?, ?, ?)",
            (place_name, description, image_path),
        )
        conn.commit()
        toast("Data saved successfully!")
    except sqlite3.Error as e:
        toast(f"Error: {e}")
    finally:
        conn.close()

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.close_file_manager,
            select_path=self.select_file,
        )

        self.layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # Name input
        self.place_name = MDTextField(
            hint_text="Enter Place Name",
            mode="rectangle",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
        )
        self.layout.add_widget(self.place_name)

        # Description input
        self.description = MDTextField(
            hint_text="Enter Description",
            mode="rectangle",
            multiline=True,
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
        )
        self.layout.add_widget(self.description)

        # Image selection button
        self.image_path = ""
        self.select_image_button = MDRaisedButton(
            text="Select Image",
            size_hint_x=0.5,
            pos_hint={"center_x": 0.5},
            on_release=self.open_file_manager,
        )
        self.layout.add_widget(self.select_image_button)

        # Submit button
        self.submit_button = MDRaisedButton(
            text="Submit",
            size_hint_x=0.5,
            pos_hint={"center_x": 0.5},
            on_release=self.submit_form,
        )
        self.layout.add_widget(self.submit_button)

        self.add_widget(self.layout)

    def open_file_manager(self, *args):
        self.file_manager.show("/")  # Start browsing from the root directory
        self.manager_open = True

    def close_file_manager(self, *args):
        self.file_manager.close()
        self.manager_open = False

    def select_file(self, path):
        self.image_path = path
        toast(f"Selected: {path}")
        self.file_manager.close()

    def submit_form(self, *args):
        place_name = self.place_name.text
        description = self.description.text
        if not (place_name and description and self.image_path):
            toast("Please fill all fields and select an image.")
            return

        save_to_database(place_name, description, self.image_path)
        self.place_name.text = ""
        self.description.text = ""
        self.image_path = ""

class PlacesApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return AddPlaceScreen()

class AnnouncementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Database initialization
        self.database = "partners.db"  # Replace with your database file
        self.initialize_database()

        # Main Layout for the Screen
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10),
        )
        self.add_widget(main_layout)

        # Form Section
        form_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(300),  # Fixed height for the form
        )

        # Title Input
        self.announcement_title = MDTextField(
            hint_text="Enter Announcement Title",
            mode="rectangle",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
        )
        form_layout.add_widget(self.announcement_title)

        # Description Input
        self.announcement_description = MDTextField(
            hint_text="Enter Announcement Description",
            mode="rectangle",
            multiline=True,
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
        )
        form_layout.add_widget(self.announcement_description)

        # Image Selection Button
        self.select_image_button = MDRaisedButton(
            text="Select Image (Optional)",
            size_hint_x=0.5,
            pos_hint={"center_x": 0.5},
            on_release=self.open_file_manager,
        )
        form_layout.add_widget(self.select_image_button)

        # Submit Button
        self.submit_button = MDRaisedButton(
            text="Post Announcement",
            size_hint_x=0.5,
            pos_hint={"center_x": 0.5},
            on_release=self.submit_announcement,
        )
        form_layout.add_widget(self.submit_button)

        # Add Form Layout to Main Layout
        main_layout.add_widget(form_layout)

        # Scrollable Announcement Section
        self.scroll_view = MDScrollView(size_hint=(1, 1))
        self.announcement_list = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=[dp(10), dp(10), dp(10), dp(10)],
            size_hint_y=None,
        )
        self.announcement_list.bind(minimum_height=self.announcement_list.setter("height"))
        self.scroll_view.add_widget(self.announcement_list)

        # Add Scroll View to Main Layout
        main_layout.add_widget(self.scroll_view)

        # Load existing announcements
        self.load_announcements()

    def initialize_database(self):
        """Ensure the deals table exists."""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
      
        conn.commit()
        conn.close()

    def open_file_manager(self, *args):
        print("File Manager Opened")  # Placeholder for file selection logic

    def submit_announcement(self, *args):
        title = self.announcement_title.text.strip()
        description = self.announcement_description.text.strip()

        if not title or not description:
            print("Both title and description are required!")
            return

        # Save to database
        self.save_to_database(title, description)

        # Add announcement to the list
        self.add_announcement_card(title, description)

        # Clear input fields
        self.announcement_title.text = ""
        self.announcement_description.text = ""

    def save_to_database(self, title, description):
        """Save announcement to the database."""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO deals ( title, details) VALUES ( ?, ?)",
            (title, description),
        )
        conn.commit()
        conn.close()

    def load_announcements(self):
        """Load announcements from the database."""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT title, details FROM deals")
        results = cursor.fetchall()
        conn.close()

        for title, description in results:
            self.add_announcement_card(title, description )

    def add_announcement_card(self, title, description):
        """Display an announcement as a card."""
        card = MDCard(
            size_hint=(None, None),
            size=(dp(350), dp(200)),
            elevation=3,
            radius=[15],
        )

        card_layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
        # Title
        card_title = MDLabel(
            text=title,
            font_style="H6",
            halign="center",
            size_hint_y=None,
            height=dp(30),
        )
        card_layout.add_widget(card_title)

        # Description
        card_description = MDLabel(
            text=description,
            font_style="Caption",
            halign="center",
            size_hint_y=None,
            height=dp(50),
        )
        card_layout.add_widget(card_description)

        card.add_widget(card_layout)
        self.announcement_list.add_widget(card)
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main Layout
        main_layout = MDBoxLayout(orientation="vertical", spacing=0, padding=0)

        # Create the menu items
        menu_items = [
            {"text": "Settings", "on_release": lambda x="Settings": (self.open_settings(), self.menu.dismiss())},
            {"text": "Help & Support", "on_release": lambda x="Help & Support": (self.open_help(), self.menu.dismiss())},
            {"text": "About", "on_release": lambda x="About": (self.open_about(), self.menu.dismiss())},
            {"text": "Logout", "on_release": lambda x="Logout": (self.logout(), self.menu.dismiss())},
        ]

        # Initialize the dropdown menu (caller will be set later)
        self.menu = MDDropdownMenu(
            items=menu_items, width_mult=4, pos_hint={"center_y": .74, "center_x":.8}
        )

        # Header
        menu_button = MDIconButton(icon="menu",  pos_hint={"center_y": 0.5})
        menu_button.bind(on_release=self.menu.open)
        header = MDTopAppBar(
            title="[b]TravelMate[/b]",
            anchor_title="center",
            elevation=4,
            right_action_items=[[menu_button.icon, lambda x: self.menu.open()]],
            md_bg_color=get_color_from_hex("#FA4032")
        )
        header.left_action_items = [["account-circle", lambda x: self.go_to_profile()]]
        self.menu.caller = menu_button  # Set the menu button as the caller
        main_layout.add_widget(header)

        # Screen Manager
        self.sm = ScreenManager(size_hint=(1, 5))
        self.sm.add_widget(DashboardScreen(name="dashboard"))
        self.sm.add_widget(AnnouncementScreen(name="announcement"))

        main_layout.add_widget(self.sm)

        # Bottom Navigation
        bottom_navigation = MDBottomNavigation(selected_color_background = (0.980, 0.251, 0.196, 1))
        bottom_navigation.md_bg_color = (0.980, 0.251, 0.196, 1)
        bottom_navigation.add_widget(
            MDBottomNavigationItem(name="dashboard", text="Dashboard", icon="home",
            on_tab_press=lambda *args: self.go_to_dashboard())
        )
        bottom_navigation.add_widget(
            MDBottomNavigationItem(name="announcement", text="Announcement", icon="bullhorn",  
            on_tab_press=lambda *args: self.go_to_announcement())
        )

        main_layout.add_widget(bottom_navigation)

        self.add_widget(main_layout)

    def go_to_dashboard(self):
        self.sm.current = "dashboard"

    def go_to_announcement(self):
        self.sm.current = "announcement"

    def logout(self):
        self.manager.current = "login"

# Main App Class
class TravelMateApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(HomeScreen(name='home'))
        sm.current = 'login'
        return sm

if __name__ == '__main__':
    TravelMateApp().run()   