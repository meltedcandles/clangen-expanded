import re
from random import choice
import pygame_gui

from .base_screens import Screens, cat_profiles
import pygame
from scripts.events import events_class
from scripts.utility import draw, get_text_box_theme, get_living_cat_count
# from scripts.game_structure.text import *
from scripts.game_structure.image_button import IDImageButton
from scripts.game_structure.game_essentials import *
from ..cat.cats import Cat
from ..game_structure import image_cache
from scripts.event_class import Single_Event


class EventsScreen(Screens):
    event_display_type = "all events"
    all_events = ""
    ceremony_events = ""
    birth_death_events = ""
    relation_events = ""
    health_events = ""
    other_clans_events = ""
    misc_events = ""
    display_text = "<center> Check this page to see which events are currently happening in the Clan.</center>"
    display_events = ""

    def __init__(self, name=None):
        super().__init__(name)
        self.misc_alert = None
        self.other_clans_alert = None
        self.health_alert = None
        self.relation_alert = None
        self.birth_death_alert = None
        self.ceremony_alert = None
        self.misc_events_button = None
        self.other_clans_events_button = None
        self.health_events_button = None
        self.birth_death_events_button = None
        self.ceremonies_events_button = None
        self.all_events_button = None
        self.relationship_events_button = None
        self.events_list_box = None
        self.toggle_borders_button = None
        self.timeskip_button = None
        self.events_frame = None
        self.clan_age = None
        self.season = None
        self.heading = None
        self.display_events_elements = {}
        self.involved_cat_buttons = []
        self.cat_profile_buttons = {}

        # Stores the involved cat button that currently has its cat profile buttons open
        self.open_involved_cat_button = None

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.timeskip_button:
                events_class.one_moon()
                if get_living_cat_count(Cat) == 0:
                    GameOver('events screen')

                self.event_display_type = 'all events'
                self.all_events_button.disable()
                self.all_events = [x for x in game.cur_events_list if "interaction" not in x.types]

                self.ceremonies_events_button.enable()
                if self.ceremony_alert:
                    self.ceremony_alert.kill()
                self.ceremony_events = [x for x in game.cur_events_list if "ceremony" in x.types]
                if self.ceremony_events:
                    self.ceremony_alert = pygame_gui.elements.UIImage(pygame.Rect((44, 340), (4, 22)),
                                                                      image_cache.load_image(
                                                                          "resources/images/alert_mark.png"
                                                                      ))

                if self.birth_death_alert:
                    self.birth_death_alert.kill()
                self.birth_death_events_button.enable()
                self.birth_death_events = [x for x in game.cur_events_list if "birth_death" in x.types]
                if self.birth_death_events:
                    self.birth_death_alert = pygame_gui.elements.UIImage(pygame.Rect((44, 390), (4, 22)),
                                                                         image_cache.load_image(
                                                                             "resources/images/alert_mark.png"
                                                                         ))

                if self.relation_alert:
                    self.relation_alert.kill()
                self.relationship_events_button.enable()
                self.relation_events = [x for x in game.cur_events_list if "relation" in x.types]
                if self.relation_events:
                    self.relation_alert = pygame_gui.elements.UIImage(pygame.Rect((44, 440), (4, 22)),
                                                                      image_cache.load_image(
                                                                          "resources/images/alert_mark.png"
                                                                      ))

                if self.health_alert:
                    self.health_alert.kill()
                self.health_events_button.enable()
                self.health_events = [x for x in game.cur_events_list if "health" in x.types]
                if self.health_events:
                    self.health_alert = pygame_gui.elements.UIImage(pygame.Rect((44, 490), (4, 22)),
                                                                    image_cache.load_image(
                                                                        "resources/images/alert_mark.png"
                                                                    ))

                if self.other_clans_alert:
                    self.other_clans_alert.kill()
                self.other_clans_events_button.enable()
                self.other_clans_events = [x for x in game.cur_events_list if "other_clans" in x.types]
                if self.other_clans_events:
                    self.other_clans_alert = pygame_gui.elements.UIImage(pygame.Rect((44, 540), (4, 22)),
                                                                         image_cache.load_image(
                                                                             "resources/images/alert_mark.png"
                                                                         ))

                if self.misc_alert:
                    self.misc_alert.kill()
                self.misc_events_button.enable()
                self.misc_events = [x for x in game.cur_events_list if "misc" in x.types]
                if self.misc_events:
                    self.misc_alert = pygame_gui.elements.UIImage(pygame.Rect((44, 590), (4, 22)),
                                                                  image_cache.load_image(
                                                                      "resources/images/alert_mark.png"
                                                                  ))

                if self.event_display_type == "all events":
                    # if events list is empty, add a single message the says nothing interesting happened
                    if not self.all_events:
                        self.all_events.append(Single_Event("Nothing interesting happened this moon"))
                    self.display_events = self.all_events
                elif self.event_display_type == "ceremony events":
                    self.display_events = self.ceremony_events
                elif self.event_display_type == "birth death events":
                    self.display_events = self.birth_death_events
                elif self.event_display_type == "relationship events":
                    self.display_events = self.relation_events
                elif self.event_display_type == "health events":
                    self.display_events = self.health_events
                elif self.event_display_type == "other clans events":
                    self.display_events = self.other_clans_events
                elif self.event_display_type == "misc events":
                    self.display_events = self.misc_events

                self.update_events_display()

            elif event.ui_element == self.toggle_borders_button:
                if game.clan.closed_borders:
                    game.clan.closed_borders = False
                    self.toggle_borders_button.set_text("Close Clan Borders")
                else:
                    game.clan.closed_borders = True
                    self.toggle_borders_button.set_text("Open Clan Borders")

            # Change the type of events displayed
            elif event.ui_element == self.all_events_button:
                self.event_display_type = "all events"
                # Update Display
                self.update_list_buttons(self.all_events_button)
                self.display_events = self.all_events
                self.update_events_display()
            elif event.ui_element == self.ceremonies_events_button:
                self.event_display_type = "ceremony events"
                self.ceremonies_events_button.disable()
                # Update Display
                self.update_list_buttons(self.ceremonies_events_button, self.ceremony_alert)
                self.display_events = self.ceremony_events
                self.update_events_display()
            elif event.ui_element == self.birth_death_events_button:
                self.event_display_type = "birth death events"
                self.birth_death_events_button.enable()
                # Update Display
                self.update_list_buttons(self.birth_death_events_button, self.birth_death_alert)
                self.display_events = self.birth_death_events
                self.update_events_display()
            elif event.ui_element == self.relationship_events_button:
                self.event_display_type = "relationship events"
                self.relationship_events_button.enable()
                # Update Display
                self.update_list_buttons(self.relationship_events_button, self.relation_alert)
                self.display_events = self.relation_events
                self.update_events_display()
            elif event.ui_element == self.health_events_button:
                self.event_display_type = "health events"
                self.health_events_button.disable()
                # Update Display
                self.update_list_buttons(self.health_events_button, self.health_alert)
                self.display_events = self.health_events
                self.update_events_display()
            elif event.ui_element == self.other_clans_events_button:
                self.event_display_type = "other clans events"
                self.other_clans_events_button.disable()
                # Update Display
                self.update_list_buttons(self.other_clans_events_button, self.other_clans_alert)
                self.display_events = self.other_clans_events
                self.update_events_display()
            elif event.ui_element == self.misc_events_button:
                self.event_display_type = "misc events"
                self.misc_events_button.disable()
                # Update Display
                self.update_list_buttons(self.misc_events_button, self.misc_alert)
                self.display_events = self.misc_events
                self.update_events_display()
            elif event.ui_element in self.involved_cat_buttons:
                self.make_cat_buttons(event.ui_element)
            elif event.ui_element in self.cat_profile_buttons:
                cat_profiles()
                game.switches['cat'] = event.ui_element.ids
                self.change_screen('profile screen')
            else:
                self.menu_button_pressed(event)

    def screen_switches(self):
        cat_profiles()

        self.heading = pygame_gui.elements.UITextBox("Check this page to see which events are currently happening in the "
                                                     "Clan",
                                                     pygame.Rect((100, 110), (600, 40)),
                                                     object_id=get_text_box_theme())
        self.season = pygame_gui.elements.UITextBox(f'Current season: {str(game.clan.current_season)}',
                                                    pygame.Rect((100, 140), (600, 40)),
                                                    object_id=get_text_box_theme())
        self.clan_age = pygame_gui.elements.UITextBox("",
                                                      pygame.Rect((100, 170), (600, 40)),
                                                      object_id=get_text_box_theme())
        self.events_frame = pygame_gui.elements.UIImage(pygame.Rect((206, 266), (534, 370)),
                                                        image_cache.load_image(
                                                            "resources/images/event_page_frame.png").convert_alpha())
        self.events_frame.disable()
        # Set text for clan age
        if game.clan.age == 1:
            self.clan_age.set_text(f'Clan age: {str(game.clan.age)} moon')
        if game.clan.age != 1:
            self.clan_age.set_text(f'Clan age: {str(game.clan.age)} moons')

        self.timeskip_button = UIImageButton(pygame.Rect((310, 218), (180, 30)), "", object_id="#timeskip_button")

        # commenting out for now as there seems to be a consensus that it isn't needed anymore?
        #if game.clan.closed_borders:
        #    self.toggle_borders_button = pygame_gui.elements.UIButton(pygame.Rect((500, 210), (200, 30)),
        #                                                              "Open Clan Borders")
        #else:
        #    self.toggle_borders_button = pygame_gui.elements.UIButton(pygame.Rect((500, 210), (200, 30)),
        #                                                              "Close Clan Borders")

        # Sets up the buttons to switch between the event types.
        self.all_events_button = UIImageButton(
            pygame.Rect((60, 286,), (150, 30)),
            "",
            object_id="#all_events_button")
        self.ceremonies_events_button = UIImageButton(
            pygame.Rect((60, 336), (150, 30)),
            "",
            object_id="#ceremony_events_button")
        self.birth_death_events_button = UIImageButton(
            pygame.Rect((60, 386), (150, 30)),
            "",
            object_id="#birth_death_events_button")
        self.relationship_events_button = UIImageButton(
            pygame.Rect((60, 436), (150, 30)),
            "",
            object_id="#relationship_events_button")
        self.health_events_button = UIImageButton(
            pygame.Rect((60, 486), (150, 30)),
            "",
            object_id="#health_events_button")
        self.other_clans_events_button = UIImageButton(
            pygame.Rect((60, 536), (150, 30)),
            "",
            object_id="#other_clans_events_button")
        self.misc_events_button = UIImageButton(
            pygame.Rect((60, 586), (150, 30)),
            "",
            object_id="#misc_events_button")

        if self.event_display_type == "all events":
            self.all_events_button.disable()
        elif self.event_display_type == "ceremony events":
            self.ceremonies_events_button.disable()
        elif self.event_display_type == "birth death events":
            self.birth_death_events_button.disable()
        elif self.event_display_type == "relationship events":
            self.relationship_events_button.disable()
        elif self.event_display_type == "health events":
            self.health_events_button.disable()
        elif self.event_display_type == "other clans events":
            self.other_clans_events_button.disable()
        elif self.event_display_type == "misc events":
            self.misc_events_button.disable()

        self.misc_alert = None
        self.other_clans_alert = None
        self.health_alert = None
        self.relation_alert = None
        self.birth_death_alert = None
        self.ceremony_alert = None

        self.open_involved_cat_button = None
        self.make_events_container()
        self.events_container_y = self.event_container.get_relative_rect()[3]

        """self.events_list_box = pygame_gui.elements.UITextBox(
            self.display_events,
            pygame.Rect((218, 271), (514, 360)),
            object_id=get_text_box_theme("#events_box"))"""

        # Display text
        # self.explain_text = pygame_gui.elements.UITextBox(self.display_text, pygame.Rect((25,110),(750,40)))

        # Draw and disable the correct menu buttons.
        self.set_disabled_menu_buttons(["events_screen"])
        self.show_menu_buttons()
        self.update_events_display()

    def exit_screen(self):
        self.open_involved_cat_button = None

        self.timeskip_button.kill()
        del self.timeskip_button
        #self.toggle_borders_button.kill()
        #del self.toggle_borders_button
        self.all_events_button.kill()
        del self.all_events_button
        self.ceremonies_events_button.kill()
        del self.ceremonies_events_button
        if self.ceremony_alert:
            self.ceremony_alert.kill()
            del self.ceremony_alert
        self.birth_death_events_button.kill()
        del self.birth_death_events_button
        if self.birth_death_alert:
            self.birth_death_alert.kill()
            del self.birth_death_alert
        self.relationship_events_button.kill()
        del self.relationship_events_button
        if self.relation_alert:
            self.relation_alert.kill()
            del self.relation_alert
        self.health_events_button.kill()
        del self.health_events_button
        if self.health_alert:
            self.health_alert.kill()
            del self.health_alert
        self.other_clans_events_button.kill()
        del self.other_clans_events_button
        if self.other_clans_alert:
            self.other_clans_alert.kill()
            del self.other_clans_alert
        self.misc_events_button.kill()
        del self.misc_events_button
        if self.misc_alert:
            self.misc_alert.kill()
            del self.misc_alert
        self.events_frame.kill()
        del self.events_frame
        self.clan_age.kill()
        del self.clan_age
        self.heading.kill()
        del self.heading
        self.season.kill()
        del self.season
        self.event_container.kill()

        for ele in self.display_events_elements:
            self.display_events_elements[ele].kill()
        self.display_events_elements = {}

        for ele in self.involved_cat_buttons:
            ele.kill()
        self.involved_cat_buttons = []

        for ele in self.cat_profile_buttons:
            ele.kill()
        self.cat_profile_buttons = []

        # self.hide_menu_buttons()

    def on_use(self):
        # What does this do?
        if game.switches['events_left'] == 0:
            self.timeskip_button.enable()
        else:
            self.timeskip_button.disable()

    def update_list_buttons(self, current_list, current_alert=None):
        """ handles the disabling and enabling of the list buttons """

        # enable all the buttons
        self.all_events_button.enable()
        self.ceremonies_events_button.enable()
        self.birth_death_events_button.enable()
        self.relationship_events_button.enable()
        self.health_events_button.enable()
        self.other_clans_events_button.enable()
        self.misc_events_button.enable()

        # disable the current button
        current_list.disable()
        if current_alert:
            current_alert.kill()

    def update_events_display(self):

        self.season.set_text(f'Current season: {str(game.clan.current_season)}')
        if game.clan.age == 1:
            self.clan_age.set_text(f'Clan age: {str(game.clan.age)} moon')
        if game.clan.age != 1:
            self.clan_age.set_text(f'Clan age: {str(game.clan.age)} moons')

        for ele in self.display_events_elements:
            self.display_events_elements[ele].kill()
        self.display_events_elements = {}

        for ele in self.involved_cat_buttons:
            ele.kill()
        self.involved_cat_buttons = []

        for ele in self.cat_profile_buttons:
            ele.kill()
        self.cat_profile_buttons = []

        # In order to set-set the scroll-bar postion, we have to remake the scrolling container
        self.event_container.kill()
        self.make_events_container()

        # Make display, with buttons and all that.
        box_length = self.event_container.get_relative_rect()[2]
        i = 0
        y = 0
        for ev in self.display_events:
            if isinstance(ev.text, str):  # Check to make sure text is a string.
                self.display_events_elements["event" + str(i)] = pygame_gui.elements.UITextBox(ev.text,
                                                                                               pygame.Rect((0, y), (box_length - 20, -1)),
                                                                                               object_id=get_text_box_theme("#events_box"),
                                                                                               container=self.event_container,
                                                                                               layer_starting_height=2)
                self.display_events_elements["event" + str(i)].disable()
                # Find the next y-height by finding the height of the text box, and adding 35 for the cats button

                if i % 2 == 0:
                    if game.settings["dark mode"]:
                        self.display_events_elements["shading" + str(i)] = pygame_gui.elements.UIImage(
                            pygame.Rect((0, y),
                                        (box_length + 50, self.display_events_elements["event" + str(i)].get_relative_rect()[3] + 35)),
                            image_cache.load_image("resources/images/shading_dark.png"), container=self.event_container)
                    else:
                        self.display_events_elements["shading" + str(i)] = pygame_gui.elements.UIImage(
                            pygame.Rect((0, y),
                                        (box_length + 50,
                                         self.display_events_elements["event" + str(i)].get_relative_rect()[3] + 35)),
                            image_cache.load_image("resources/images/shading.png"), container=self.event_container)

                    self.display_events_elements["shading" + str(i)].disable()

                y += self.display_events_elements["event" + str(i)].get_relative_rect()[3]

                self.involved_cat_buttons.append(IDImageButton(pygame.Rect(
                    (self.event_container.get_relative_rect()[2] - 40, y - 5), (34, 34)),
                    ids=ev.cats_involved, container=self.event_container, layer_starting_height=2,
                    object_id="#events_cat_button"))

                y += 35
                i += 1



        # Set scrolling container length
        # This is a hack-y solution, but it was the easiest way to have the shading go all the way across the box
        self.event_container.set_scrollable_area_dimensions((box_length, y + 15))

        if self.event_container.vert_scroll_bar:
            for ele in self.involved_cat_buttons:
                ele.set_relative_position((ele.get_relative_rect()[0] - 20, ele.get_relative_rect()[1]))

        if self.event_container.horiz_scroll_bar:
            self.event_container.set_dimensions((box_length, self.events_container_y + 20))
            self.event_container.horiz_scroll_bar.hide()
        else:
            self.event_container.set_dimensions((box_length, self.events_container_y))

    def make_cat_buttons(self, button_pressed):
        """ Makes the buttons that take you to the profile. """

        # Check if the button you pressed doesn't have it cat profile buttons currently displayed.
        # If it doesn't have it's buttons displayed, set the current open involved_cat_button to the pressed button,
        # clear all other buttons, and open the cat profile buttons.
        if self.open_involved_cat_button != button_pressed:
            self.open_involved_cat_button = button_pressed
            for ele in self.cat_profile_buttons:
                ele.kill()
            self.cat_profile_buttons = []

            pressed_button_pos = (button_pressed.get_relative_rect()[0], button_pressed.get_relative_rect()[1])

            i = 1
            for ev in button_pressed.ids:
                cat_ob = Cat.fetch_cat(ev)
                if cat_ob:
                    # Shorten name if needed
                    name = str(cat_ob.name)
                    if len(name) > 10:
                        name = name[:9] + ".."

                    self.cat_profile_buttons.append(
                        IDImageButton(pygame.Rect((pressed_button_pos[0] - (120 * i) - 1,
                                                   pressed_button_pos[1] + 2),
                                                   (116, 30)),
                                      text=name, ids=ev, container=self.event_container,
                                      object_id="#events_cat_profile_button")
                    )
                    # There is only room for about four buttons.
                    if i > 4:
                        break
                    i += 1

        # If the button pressed does have its cat profile buttons open, just close the buttons.
        else:
            self.open_involved_cat_button = None
            for ele in self.cat_profile_buttons:
                ele.kill()
            self.cat_profile_buttons = []

    def make_events_container(self):
        """ In its own function so that there is only one place the box size is set"""
        self.event_container = pygame_gui.elements.UIScrollingContainer(pygame.Rect((216, 276), (514, 350)))
