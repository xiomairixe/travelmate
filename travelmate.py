from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton, MDFloatingActionButton, MDTextButton
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.scrollview import ScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.uix.button import Button
from kivy.uix.widget import Widget, WidgetException
from kivymd.uix.list import MDList, OneLineListItem, OneLineAvatarListItem, OneLineIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivy.uix.textinput import TextInput
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.uix.screenmanager import ScreenManager, Screen
from functools import partial
from kivy.uix.stencilview import StencilView
from kivy.uix.relativelayout import RelativeLayout
import requests
import sqlite3

# Set the window size to mobile dimensions for desktop testing
Window.size = (360, 640)

# Database connection function
def connect_db():
    conn = sqlite3.connect('users.db')
    return conn

# LANDING PAGE
class TravelMate(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=[20, 20, 20, 20],
            spacing=10,
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
        )

        # Add Image above the title
        image = Image(
            source="car.png", 
            size_hint=(None, None),
            size=(260, 260),
            pos_hint={'center_x': 0.5},
        )
        main_layout.add_widget(image)

        # Title Layout
        title_label = MDLabel(
            text='TravelMate',
            font_style='H4',
            halign="center",
            size_hint_y=None,
            height=40,
        )
        main_layout.add_widget(title_label)

        # Subtitle Layout
        subtitle_label = MDLabel(
            text='"Your Adventure Awaits"',
            font_style='Caption',
            halign="center",
            size_hint_y=None,
            height=20,
        )
        main_layout.add_widget(subtitle_label)

        # Circular Button with Arrow Icon
        arrow_button = MDFloatingActionButton(
            icon="chevron-right",
            pos_hint={'center_x': 0.5},
            md_bg_color=get_color_from_hex("#FA4032"),  
        )
        arrow_button.bind(on_press=self.go_to_login)
        main_layout.add_widget(arrow_button)

        # Add the main layout to the screen
        self.add_widget(main_layout)

    def go_to_login(self, instance):
        """Navigate to the login screen."""
        self.manager.current = 'login'

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
            c.execute("SELECT user_id, email, password FROM users WHERE email=? AND password=?", (email, password))
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

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize booking dialog and menu
        self.booking_dialog = None
        self.duration_menu = None

        # Scrollable layout for the whole screen
        self.scroll_view = MDScrollView()

        # Main vertical layout inside the scroll view
        main_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[0, 0, 0, 0],
            spacing=20,
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # Top bar with search container
        top_bar = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=55,
            padding=[0, 0, 0, 0],
            spacing=10
        )

        search_container = MDCard(
            orientation='horizontal',
            size_hint=(1, None),
            height=50,
            md_bg_color=[1, 1, 1, 1],
            radius=[10],
            padding=[2, 5, 5, 0],
        )
        search_button = MDIconButton(
            icon="magnify",
            pos_hint={"center_y": 0.5},
            on_release=self.search_action
        )
        search_container.add_widget(search_button)

        self.search_input = TextInput(
            hint_text="Search...",
            size_hint=(0, None),
            height=40,
            multiline=False,
            font_size=16,
            background_color=(0, 0, 0, 0),
            padding=[0, 10, 0, 10],
            opacity=0
        )
        search_container.add_widget(self.search_input)
        top_bar.add_widget(search_container)
        main_layout.add_widget(top_bar)

        # Content Section
        content_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=0,
            padding=[5,25,0,0],
            size_hint_y=None,
        )

        title_layout = MDBoxLayout(
            orientation="vertical",
            spacing=3,
            padding=[5,0,0,0],
            size_hint_y=None,
        )

        subtitle_label = MDLabel(
            markup=True,
            text="[b]Let's Find Cool Places! [/b]",
            font_style="H4",
            halign="left",
            theme_text_color="Primary"
        )

        # Add map-marker button
        map_marker_button = MDIconButton(
            icon="map-marker",
            icon_size="60dp",
            pos_hint={"center_y": 0.9},
            on_release=self.scroll_to_explore  # Scroll function
        )
        
        content_layout.add_widget(title_layout)
        title_layout.add_widget(subtitle_label)
        main_layout.add_widget(content_layout)
        content_layout.add_widget(map_marker_button)

        # SCROLLING CARD SECTION
        self.story_scroll_view = MDScrollView(
            size_hint_y=None,
            height=300,
            bar_width=5,
            scroll_type=['content'],
            
        )
        self.story_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=20,
            padding=[40, 0, 0, 0],
            size_hint_x=None,
        )
        self.story_card_size = 210
        self.num_stories = 6
        self.story_layout.width = (self.story_card_size + 20) * self.num_stories

        # Placeholder for story images
        def fetch_places():
            conn = sqlite3.connect('users.db')  # Replace with your database connection
            cursor = conn.cursor()
            cursor.execute("SELECT name, image, description FROM places")  # Add description
            results = cursor.fetchall()
            conn.close()
            return results  # Return list of tuples: [(name, image_path, description), ...]

        image_data = fetch_places()  # Fetch image paths, names, and descriptions

        self.story_images = []  # Clear the placeholder
        for i, (place_name, image_path, description) in enumerate(image_data):
            story_item = MDBoxLayout(
                orientation='vertical',
                size_hint=(None, None),
                size=(self.story_card_size, 200),
            )
            # Card with rounded corners
            story_image_card = MDCard(
                size_hint=(None, None),
                size=(self.story_card_size, 265),
                elevation=2,
                radius=[20, 20, 20, 20],  # Rounded corners
                ripple_behavior=True,
                md_bg_color=[1, 1, 1, 1],
                on_release=self.show_booking_form
            )
            # Create a RelativeLayout for overlaying the icon
            relative_layout = RelativeLayout()

            # Image for the card
            stencil_view = StencilView(size_hint=(1, 1))
            story_image = Image(
                source=image_path if image_path else "default.jpg",  # Fallback to default
                allow_stretch=True,
                keep_ratio=False,  # Ignore aspect ratio to fill the card
            )
            relative_layout.add_widget(story_image)  # Add the image first

            # Detail icon overlay
            detail_icon = MDIconButton(
                icon="information-outline",
                pos_hint={"right": 1, "top": 1},  # Position in the top-right corner
                size_hint=(None, None),
                size=(30, 30),
                on_release=lambda instance, name=place_name, desc=description: self.show_details(name, desc)
            )
            relative_layout.add_widget(detail_icon)  # Add the icon on top

            # Add the relative layout to the card
            story_image_card.add_widget(relative_layout)
            story_item.add_widget(story_image_card)

            # Add label below the card
            story_label = MDLabel(
                markup=True,
                text=f"[b]{place_name}[/b]",
                font_style="Caption",
                halign="center",
                size_hint_y=None,
                height=30,
            )
            story_item.add_widget(story_label)
            self.story_layout.add_widget(story_item)

        # Add story layout to scroll view
        self.story_scroll_view.add_widget(self.story_layout)
        main_layout.add_widget(self.story_scroll_view)


        # BUTTONS SECTION
        button_layout = MDGridLayout(
            cols=3,
            spacing=20,
            padding=[10, 10, 8, 10],
            pos_hint={'center_x': .70},
            size_hint_y=None,
            height=20
        )

        # Function to handle hover effect
        def on_hover(instance, value):
            if value:  # If the mouse is over the widget
                instance.text_color = [1, 0.251, 0.196, 1]  # Change to hover color
            else:
                instance.text_color = [0.869, 0.561, 0.373, 1]  # Change back to default color

        # Create buttons with hover functionality
        popular_button = MDTextButton(
            text="Popular",
            font_style="H6",
            size_hint=(None, None),
            text_color=[0.869, 0.561, 0.373, 1],
            on_release=lambda instance: self.change_images("popular")
        )
        popular_button.bind(on_enter=lambda instance: on_hover(popular_button, True))
        popular_button.bind(on_leave=lambda instance: on_hover(popular_button, False))

        suggested_button = MDTextButton(
            text="Suggested",
            font_style="H6",
            size_hint=(None, None),
            text_color=[0.869, 0.561, 0.373, 1],
            on_release=lambda instance: self.change_images("suggested")
        )
        suggested_button.bind(on_enter=lambda instance: on_hover(suggested_button, True))
        suggested_button.bind(on_leave=lambda instance: on_hover(suggested_button, False))

        saved_button = MDTextButton(
            text="Saved",
            font_style="H6",
            size_hint=(None, None),
            text_color=[0.869, 0.561, 0.373, 1],
            on_release=lambda instance: self.change_images("saved")
        )
        saved_button.bind(on_enter=lambda instance: on_hover(saved_button, True))
        saved_button.bind(on_leave=lambda instance: on_hover(saved_button, False))

        # Add buttons to layout
        button_layout.add_widget(popular_button)
        button_layout.add_widget(suggested_button)
        button_layout.add_widget(saved_button)
        main_layout.add_widget(button_layout)


        def fetch_places():
            conn = sqlite3.connect('users.db')  # Replace with your database connection
            cursor = conn.cursor()
            cursor.execute("SELECT name, description, image FROM places")  # Adjust column names as necessary
            results = cursor.fetchall()
            conn.close()
            return results  # List of tuples: (destination_name, image_path)

        # "Explore More" Section - Added under buttons
        explore_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,  # Allow dynamic height
            padding=[10, 10, 10, 10],
            spacing=10,
        )

        # Label for the "Explore More" section
        explore_label = MDLabel(
            markup=True,
            text="[b]Discover[/b]",
            font_style="H5",
            halign="left",
        )
        explore_layout.add_widget(explore_label)

        # Fetch the destinations and their images from the database
        places = fetch_places()  # This will return a list of tuples: [(destination_name, image_path), ...]

        destinations_list = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint_y=None,  # Allow dynamic height
            padding=[5, 5, 5, 5],
        )

        # Calculate the dynamic height of the destinations list
        card_height = 250  # Height of each destination card
        spacing_height = 20  # Spacing between cards
        destinations_list.height = len(places) * (card_height + spacing_height)

        # Dynamically populate cards for each destination
        for name, destination, image_path in places:
            destination_card = MDCard(
                size_hint=(None, None),
                size=(400, 250),  # Card size
                elevation=4,
                radius=[20],
                md_bg_color=[1, 1, 1, 1],
                ripple_behavior=True,
            )
            destination_layout = MDBoxLayout(
                orientation='horizontal',
                padding=[15, 10, 10, 20],
                spacing=10,
            )

            # Image for the destination on the left
            destination_image = Image(
                source=image_path if image_path else "default_image.jpg",  # Fallback to a default image
                size_hint=(None, None),
                size=(180, 210), 
                allow_stretch=True,
                keep_ratio=False,
            )
            destination_layout.add_widget(destination_image)

            # Layout for destination name and button on the right
            title_layout = MDBoxLayout(
                orientation="vertical",
                spacing=10,
                size_hint_y=None,
                size=(200, 210), 
            )

            # Destination name
            destination_label = MDLabel(
                text=name,
                pos_hint={"center_y": 0.9},
                font_style="H6",
                halign="center",
                size_hint_y=None,
                height=40, 
            )
            description_label = MDLabel(
                text=destination,
                font_style="Caption",
                halign="center",
                size_hint_y=None,
                height=50,
            )
            title_layout.add_widget(destination_label)
            title_layout.add_widget(description_label)

            # "Book Now" button at the bottom
            book_button = MDRaisedButton(
                text="Book Now",
                size_hint=(None, None),
                width=120,
                height=40,
                pos_hint={"center_x": 0.5},
                md_bg_color=[0, 0, 1, 1],
                text_color=[1, 1, 1, 1],
                on_release=self.show_booking_form,  # Link to the booking handler
            )
            title_layout.add_widget(book_button)

            # Add the right-side layout to the main destination layout
            destination_layout.add_widget(title_layout)

            # Add the destination layout to the card
            destination_card.add_widget(destination_layout)

            # Add the card to the destinations list
            destinations_list.add_widget(destination_card)

        # Add the destination list to the explore layout
        explore_layout.add_widget(destinations_list)

        # Adjust the height of the explore layout dynamically
        explore_layout.height = destinations_list.height + 100  # Include label and padding

        # Add the explore section under the buttons layout
        main_layout.add_widget(explore_layout)

        # Add the main layout to the scroll view
        self.scroll_view.add_widget(main_layout)
        self.add_widget(self.scroll_view)

    # Function to display details in a popup
    def show_details(self, name, description):
            """Show a dialog with details of the place."""
            dialog = MDDialog(
                title=name,
                text=description,
                buttons=[
                    MDRaisedButton(
                        text="Close",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()

    def change_images(self, category):
        """Update images based on the selected category."""
        if category == "popular":
            new_images = ["island1.jpg"] * 6
        elif category == "suggested":
            new_images = ["mountain.jpg"] * 6 
        elif category == "saved":
            new_images = ["city.jpg"] * 6
        else:
            new_images = ["default.jpg"] * 10

        for i, image_widget in enumerate(self.story_images):
            image_widget.source = new_images[i]
            image_widget.reload()

    def search_action(self, instance):
        if self.search_input.opacity == 0:
            self.search_input.opacity = 1
            self.search_input.focus = True
        else:
            query = self.search_input.text.strip()
            if query:
                print(f"Performing search for: {query}")
            else:
                print("Search query is empty.")
            self.search_input.opacity = 0

    def scroll_to_explore(self, instance):
        self.scroll_view.scroll_y = .7  # Scroll to the bottom

    def show_booking_form(self, instance):
        """Show the booking form when an image is clicked."""

        if not self.booking_dialog:
            self.booking_dialog = MDDialog(
                title="Booking Form",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(
                        hint_text="Name",
                        size_hint_y=None,
                        height=dp(40),
                    ),
                    MDTextField(
                        hint_text="Contact Number",
                        size_hint_y=None,
                        height=dp(40),
                    ),
                    MDTextField(
                        hint_text="Email Address",
                        size_hint_y=None,
                        height=dp(40),
                    ),
                    MDTextField(
                        hint_text="Date",
                        size_hint_y=None,
                        height=dp(40),
                    ),
                    orientation="vertical",
                    spacing=dp(10),
                    padding=[dp(20), dp(60), dp(20), dp(20)],
                    size_hint=(0.9, None), 
                    adaptive_height=True,
                ),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda x: self.booking_dialog.dismiss(),
                    ),
                    MDFlatButton(
                        text="BOOK NOW",
                        on_release=self.submit_booking,
                    ),
                    MDFlatButton(
                        text="Save",
                        on_release=self.save,
                    ),
                ],
            )
        self.booking_dialog.open()

    def submit_booking(self, instance):
        """Submit the booking form."""
        print("Booking Submitted")
        self.booking_dialog.dismiss()

    def save (self, instance):
        print("The Place succesfully saved")

class AnnouncementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout for dashboard screen, vertically organized
        layout = MDBoxLayout(orientation='vertical', spacing=10)

        # Scrollable view for announcements
        scroll_view = MDScrollView()
        self.announcement_content = MDBoxLayout(
            orientation='vertical',
            spacing=15,
            padding=[0, 15, 0, 0],
            size_hint_y=None
        )
        self.announcement_content.bind(minimum_height=self.announcement_content.setter('height'))

        # Add content to scroll view
        scroll_view.add_widget(self.announcement_content)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

        # Load announcements from the database
        self.load_announcements()

    def load_announcements(self):
        """Fetch data from the database and populate the UI."""
        try:
            conn = sqlite3.connect('users.db')  # Replace with your database file
            cursor = conn.cursor()
            cursor.execute("SELECT title, details FROM deals")  # Fetch title and description
            results = cursor.fetchall()
            conn.close()

            for title, description in results:
                self.add_announcement_card(title, description)

        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def add_announcement_card(self, title, description):
        """Dynamically create a card for each announcement."""
        card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height=150,
            padding=[20, 10, 20, 10],
            elevation=4,
        )
        card.add_widget(MDLabel(text=title, font_style="H6", halign="left"))
        card.add_widget(MDLabel(text=description, theme_text_color="Secondary", halign="left"))

        self.announcement_content.add_widget(card)

# SCREEN FIR WEATHER SCREEN
class WeatherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout for weather screen
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=[0, 0, 0, 0])

        # Label for displaying the weather info
        self.weather_label = MDLabel(
            text="Loading weather...",
            halign="center",
            theme_text_color="Primary"
        )
        layout.add_widget(self.weather_label)
        
        self.add_widget(layout)
        
        # Fetch weather data
        self.fetch_weather()

    def fetch_weather(self):
        # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
        api_key = "YOUR_API_KEY"
        city = "New York"  # You can make this dynamic or ask the user for their city
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                # Extract weather data
                temp = data['main']['temp']
                weather_description = data['weather'][0]['description']
                self.weather_label.text = f"City: {city}\nTemperature: {temp}°C\nCondition: {weather_description}"
            else:
                self.weather_label.text = "Failed to fetch weather data."
        except Exception as e:
            print("Error fetching weather data:", e)
            self.weather_label.text = "Error fetching weather data."

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout for the screen
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=[0, 0, 0, 0])

        # Create a ScrollView to hold the MDList
        scroll_view = ScrollView(size_hint=(1, 1))  # Ensure it fills the parent layout
        self.history_list = MDList()
        scroll_view.add_widget(self.history_list)

        # Add the ScrollView to the main layout
        layout.add_widget(scroll_view)

        # Add the main layout to the screen
        self.add_widget(layout)

        # Sample data for testing
        history_data = [
            {
                "location": "Manila",
                "date": "20/11/2023",
                "time": "1:00 PM",
                "head_count": 40,
                "paid": 3000,
                "duration": "3.5 hours"
            },
            {
                "location": "Quezon City",
                "date": "22/11/2023",
                "time": "11:00 AM",
                "head_count": 25,
                "paid": 2000,
                "duration": "2 hours"
            },
            {
                "location": "Tagaytay",
                "date": "18/10/2023",
                "time": "10:30 AM",
                "head_count": 15,
                "paid": 1500,
                "duration": "12 hours"
            },
            {
                "location": "Boracay",
                "date": "05/12/2023",
                "time": "9:00 AM",
                "head_count": 60,
                "paid": 4500,
                "duration": "24 hours"
            },
            {
                "location": "Davao City",
                "date": "10/11/2023",
                "time": "3:00 PM",
                "head_count": 30,
                "paid": 2500,
                "duration": "3days"
            }
        ]

        # Populate the history list with sample data
        self.populate_history(history_data)

    def populate_history(self, history_items):
        """
        Populate the MDList with dynamic data.

        :param history_items: A list of dictionaries containing history data.
        """
        # Clear the existing list to avoid duplicates
        self.history_list.clear_widgets()

        # Check if data is available
        if not history_items:
            # If no data, display a placeholder message
            self.history_list.add_widget(
                OneLineListItem(
                    text="No history available.",
                    size_hint_y=None,
                    height=50
                )
            )
            return

        # Loop through the history data and add items to the MDList
        for entry in history_items:
            list_item = OneLineListItem(
                text=f"{entry['location']} - {entry['date']}",
                size_hint_y=None,
                height=50,  # Ensure the item has a fixed height
                on_release=partial(self.show_details, entry)  # Pass data to the show_details method
            )
            self.history_list.add_widget(list_item)  # Add each item to the MDList

    def show_details(self, entry, *args):
        """Show the full details in a pop-up dialog when an item is clicked."""

        # Scrollable content inside the dialog
        scroll = ScrollView(size_hint=(1, None), size=("500dp", "500dp"))  # Make dialog scrollable

        # Create a vertical layout for details
        content = MDBoxLayout(orientation="vertical", padding=20, spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))  # Dynamically adjust height

        # Add labels with the details
        content.add_widget(MDLabel(text=f"Location: {entry['location']}", size_hint_y=None, height=40, font_style="Body1"))
        content.add_widget(MDLabel(text=f"Date: {entry['date']}", size_hint_y=None, height=40, font_style="Body1"))
        content.add_widget(MDLabel(text=f"Time: {entry['time']}", size_hint_y=None, height=40, font_style="Body1"))
        content.add_widget(MDLabel(text=f"Head Count: {entry['head_count']}", size_hint_y=None, height=40, font_style="Body1"))
        content.add_widget(MDLabel(text=f"Paid: ${entry['paid']}", size_hint_y=None, height=40, font_style="Body1"))
        content.add_widget(MDLabel(text=f"Duration: {entry['duration']}", size_hint_y=None, height=40, font_style="Body1"))

        # Add the content to the scroll view
        scroll.add_widget(content)

        # Create a dialog with its own close button
        self.dialog = MDDialog(
            title="History Details",
            type="custom",
            content_cls=scroll,
            size_hint=(0.95, None),
            height="600dp",  # Larger dialog size
            auto_dismiss=False,
            buttons=[
                MDRaisedButton(
                    text="Close",
                    on_press=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout inside a ScrollView
        scroll_view = MDScrollView(size_hint=(1, 1))
        layout = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=20, padding=[0, 0, 0, 0])
        layout.bind(minimum_height=layout.setter('height'))  # Ensures the layout resizes according to its content

        # Header
        header = MDTopAppBar(
            title="Profile",
            anchor_title="center",
            elevation=4,
            md_bg_color=get_color_from_hex("#FA4032"),
            right_action_items=[["account-edit", lambda x: self.enable_edit_mode()]]
        )
        header.left_action_items = [["arrow-left", lambda x: self.go_back_to_dashboard()]]
        layout.add_widget(header)

        # Profile fields
        self.email_field = MDTextField(
            hint_text="Email", text="", mode="rectangle",
            size_hint_x=.9, disabled=True, pos_hint={"center_x":.5}
        )
        self.first_name_field = MDTextField(
            hint_text="First Name", text="", mode="rectangle",
            size_hint_x=.9, disabled=True, pos_hint={"center_x":.5}
        )
        self.middle_name_field = MDTextField(
            hint_text="Middle Name", text="", mode="rectangle",
            size_hint_x=.9, disabled=True, pos_hint={"center_x":.5}
        )
        self.last_name_field = MDTextField(
            hint_text="Last Name", text="", mode="rectangle",
            size_hint_x=.9, disabled=True, pos_hint={"center_x":.5}
        )
        self.gender_field = MDTextField(
            hint_text="Gender", text="", mode="rectangle",
            size_hint_x=.9, disabled=True, pos_hint={"center_x":.5}
        )
        self.address_field = MDTextField(
            hint_text="Address", text="", mode="rectangle",
            size_hint_x=.9, disabled=True, pos_hint={"center_x":.5}
        )
        self.phone_field = MDTextField(
            hint_text="Phone", text="", mode="rectangle",
            size_hint_x=.9, disabled=True, pos_hint={"center_x":.5}
        )

        # Add fields to layout
        layout.add_widget(self.first_name_field)
        layout.add_widget(self.middle_name_field)
        layout.add_widget(self.last_name_field)
        layout.add_widget(self.gender_field)
        layout.add_widget(self.address_field)
        layout.add_widget(self.email_field)
        layout.add_widget(self.phone_field)

        # Save button, hidden by default
        self.save_button = MDRaisedButton(
            text="Save", pos_hint={'center_x': 0.5}, size_hint=(0.5, None), height=50, md_bg_color=get_color_from_hex("#FA4032"),
            on_press=self.save_profile_changes
        )
        self.save_button.opacity = 0  # Hide the save button initially
        layout.add_widget(self.save_button)

        # Add layout to scroll view and then to the screen
        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def enable_edit_mode(self):
        """Toggle edit mode for all fields and show the save button."""
        # Enable all text fields for editing
        self.first_name_field.disabled = False
        self.middle_name_field.disabled = False
        self.last_name_field.disabled = False
        self.gender_field.disabled = False
        self.address_field.disabled = False
        self.email_field.disabled = False
        self.phone_field.disabled = False

        # Show the save button
        self.save_button.opacity = 1

    def save_profile_changes(self, instance):
        """Save the profile changes and switch back to view mode."""
        # Save logic here (e.g., save to a database or local storage)
        print("Profile saved.")

        # Disable all text fields to return to view mode
        self.first_name_field.disabled = True
        self.middle_name_field.disabled = True
        self.last_name_field.disabled = True
        self.gender_field.disabled = True
        self.address_field.disabled = True
        self.email_field.disabled = True
        self.phone_field.disabled = True

        # Hide the save button
        self.save_button.opacity = 0


    def go_back_to_dashboard(self):
        """Navigate back to the dashboard."""
        self.manager.current = 'home'

    def show_message(self, message):
        """Display a message to the user."""
        dialog = MDDialog(
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout with no padding and filling the entire screen
        layout = MDBoxLayout(orientation="vertical", spacing=0, padding=[0, 0, 0, 0])

        # Header with MDTopAppBar at the top
        header = MDTopAppBar(
            title="Settings",
            anchor_title="center",
            elevation=4,
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            md_bg_color=get_color_from_hex("#FA4032")
        )
        layout.add_widget(header)

        # Scrollable area for settings options
        scroll_view = MDScrollView()
        settings_list = MDList()

        # Notifications Toggle
        notification_item = OneLineListItem(
            text="Enable Notifications"
        )
        notification_switch = MDSwitch()
        notification_switch.pos_hint = {"center_x": .85, "center_y":0.4}
        notification_item.add_widget(notification_switch)
        settings_list.add_widget(notification_item)

        # Dark Mode Toggle
        dark_mode_item = OneLineListItem(
            text="Dark Mode"
        )
        dark_mode_switch = MDSwitch()
        dark_mode_switch.pos_hint = {"center_x": .85, "center_y":0.3}
        dark_mode_item.add_widget(dark_mode_switch)
        settings_list.add_widget(dark_mode_item)

        # App Version Info
        version_item = OneLineListItem(
            text="App Version: 1.0.0"
        )
        settings_list.add_widget(version_item)

        # Add settings list inside the scroll view
        scroll_view.add_widget(settings_list)

        # Add scroll view to the layout
        layout.add_widget(scroll_view)

        # Add the entire layout to the screen
        self.add_widget(layout)

    def go_back(self):
        self.manager.current = "home"

class AboutPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout with no padding
        layout = MDBoxLayout(orientation="vertical", spacing=0, padding=[0, 0, 0, 0])

        # Header with MDTopAppBar
        header = MDTopAppBar(
            title="About TravelMate",
            anchor_title="center",
            elevation=4,
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            md_bg_color=get_color_from_hex("#FA4032")
        )
        layout.add_widget(header)

        # Scrollable area for the content
        scroll_view = MDScrollView()
        content_layout = MDBoxLayout(
            orientation="vertical", 
            padding=[20, 20, 20, 20],  # Padding for a clean look
            spacing=15, 
            size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter("height"))  # Extend to fit content

        # About Content
        content_layout.add_widget(
            MDLabel(
                text="**Welcome to TravelMate!**",
                halign="center",
                font_style="H5",
                size_hint_y=None,
                height=50
            )
        )
        content_layout.add_widget(
            MDLabel(
                text=(
                    "TravelMate is your ultimate companion for exploring the world. "
                    "Whether you're planning a weekend getaway, a cross-country adventure, "
                    "or just keeping track of your travel history, TravelMate is here to assist you."
                ),
                halign="justify",
                size_hint_y=None,
                height=100
            )
        )
        content_layout.add_widget(
            MDLabel(
                text=(
                    "With features like weather updates, announcements, and goal setting, "
                    "we aim to make your travels seamless and stress-free. "
                    "Enjoy using TravelMate and make every journey unforgettable!"
                ),
                halign="justify",
                size_hint_y=None,
                height=100
            )
        )
        content_layout.add_widget(
            MDLabel(
                text="**Features:**",
                halign="left",
                font_style="H6",
                size_hint_y=None,
                height=30
            )
        )
        content_layout.add_widget(
            MDLabel(
                text=(
                    "- Dashboard for quick access to key information.\n"
                    "- Live weather updates for your destinations.\n"
                    "- Announcements to keep you informed.\n"
                    "- History tracking for past travels.\n"
                    "- Goal setting to inspire your adventures."
                ),
                halign="left",
                size_hint_y=None,
                height=150
            )
        )
        content_layout.add_widget(
            MDLabel(
                text="**App Version:** 1.0.0",
                halign="center",
                size_hint_y=None,
                height=30
            )
        )
        content_layout.add_widget(
            MDLabel(
                text="Developed with ❤️ by the TravelMate Team.",
                halign="center",
                size_hint_y=None,
                height=30
            )
        )

        # Add content to the scroll view
        scroll_view.add_widget(content_layout)

        # Add scroll view to the layout
        layout.add_widget(scroll_view)

        # Add the entire layout to the screen
        self.add_widget(layout)

    def go_back(self):
        self.manager.current = "home"

class HelpSupportPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout
        layout = MDBoxLayout(orientation="vertical", spacing=0, padding=[0, 0, 0, 0])

        # Header with MDTopAppBar
        header = MDTopAppBar(
            title="Help & Support",
            anchor_title="center",
            elevation=4,
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            md_bg_color=get_color_from_hex("#FA4032")
        )
        layout.add_widget(header)

        # Scrollable content
        scroll_view = MDScrollView()
        content_layout = MDBoxLayout(
            orientation="vertical",
            padding=[20, 20, 20, 20],
            spacing=25,
            size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter("height"))  # Extend layout as needed

        # Add a title
        content_layout.add_widget(
            MDLabel(
                text="How can we help you?",
                halign="center",
                font_style="H5",
                size_hint_y=None,
                height=50
            )
        )

        # FAQ Section
        content_layout.add_widget(
            MDLabel(
                text="Frequently Asked Questions",
                halign="left",
                font_style="H6",
                size_hint_y=None,
                height=30
            )
        )

        faq_items = [
            {"icon": "help-circle", "text": "How to use the app?"},
            {"icon": "map-marker-question", "text": "How to check the weather for a location?"},
            {"icon": "history", "text": "Where can I see my travel history?"},
        ]

        for item in faq_items:
            faq_item = OneLineIconListItem(text=item["text"])
            faq_icon = IconLeftWidget(icon=item["icon"])
            faq_item.add_widget(faq_icon)
            content_layout.add_widget(faq_item)

        # Contact Section
        content_layout.add_widget(
            MDLabel(
                text="Contact Us",
                halign="left",
                font_style="H6",
                size_hint_y=None,
                height=30
            )
        )

        contact_items = [
            {"icon": "email", "text": "Email: support@travelmate.com"},
            {"icon": "phone", "text": "Phone: 99999999999"},
            {"icon": "web", "text": "Website: www.travelmate.com"},
        ]

        for item in contact_items:
            contact_item = OneLineIconListItem(text=item["text"])
            contact_icon = IconLeftWidget(icon=item["icon"])
            contact_item.add_widget(contact_icon)
            content_layout.add_widget(contact_item)

        # Feedback Section
        content_layout.add_widget(
            MDLabel(
                text="Feedback",
                halign="left",
                font_style="H6",
                size_hint_y=None,
                height=30
            )
        )
        content_layout.add_widget(
            MDLabel(
                text=(
                    "We value your feedback! If you have suggestions, questions, or "
                    "issues, feel free to reach out via email or phone. You can also "
                    "leave feedback on our website."
                ),
                halign="justify",
                size_hint_y=None,
                height=100
            )
        )

        # Add content to the scroll view
        scroll_view.add_widget(content_layout)

        # Add scroll view to the layout
        layout.add_widget(scroll_view)

        # Add the entire layout to the screen
        self.add_widget(layout)

    def go_back(self):
        self.manager.current = "home"

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
        self.sm.add_widget(WeatherScreen(name="weather"))
        self.sm.add_widget(HistoryScreen(name="history"))

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
        bottom_navigation.add_widget(
            MDBottomNavigationItem(name="weather", text="Weather", icon="weather-partly-cloudy",
            on_tab_press=lambda *args: self.go_to_weather())
        )
        bottom_navigation.add_widget(
            MDBottomNavigationItem(name="history", text="History", icon="history",
            on_tab_press=lambda *args: self.go_to_history())
        )

        main_layout.add_widget(bottom_navigation)

        self.add_widget(main_layout)

    def go_to_dashboard(self):
        self.sm.current = "dashboard"

    def go_to_announcement(self):
        self.sm.current = "announcement"

    def go_to_weather(self):
        self.sm.current = "weather"

    def go_to_history(self):
        self.sm.current = "history"

    def go_to_profile(self):
        self.manager.current = "profile"

    def open_settings(self):
        self.manager.current = "settings"

    def open_help(self):
        self.manager.current = "help"

    def open_about(self):
        self.manager.current = "about"

    def logout(self):
        self.manager.current = "login"

# Main App Class
class TravelMateApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TravelMate(name='TravelMate'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(AboutPage(name='about'))
        sm.add_widget(HelpSupportPage(name='help'))

        sm.current = 'TravelMate'
        return sm

if __name__ == '__main__':
    TravelMateApp().run()   