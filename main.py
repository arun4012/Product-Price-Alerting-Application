from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from backend import amazon, add_product, flipkart, alert_system
import os
import csv
from kivy.clock import Clock

Builder.load_file('Product_Price_Alterter.kv')


class MyLayout(Widget):

    def add_product(self):

        if os.path.exists("./price.csv"):
            rows = []
            with open("price.csv", 'r') as file:
                csvreader = csv.reader(file)
                header = next(csvreader)
                for row in csvreader:
                    rows.append(row)

            self.ids.email.text = row[1]
            self.ids.link.text = row[5]
            self.ids.set_price.text = row[3]

            self.ids.disable_add_product_button.disabled = True
            self.ids.disable_remove_product_button.disabled = False
            self.ids.disable_start_track_button.disabled = False

        else:

            if self.ids.email.text == '' or self.ids.link.text == '' or self.ids.set_price.text == '':

                self.ids.output_label.text = f'Kindly fill the required information'

            else:

                get = amazon(self.ids.link.text) if 'amazon' in self.ids.link.text else flipkart(self.ids.link.text) if \
                    'flipkart' in self.ids.link.text else None

                if get and self.ids.email.text.endswith('@gmail.com') and self.ids.set_price.text.isnumeric():

                    price, product = get[0], get[1]
                    self.ids.set_price_text = int(self.ids.set_price.text)
                    add_product(self.ids.email.text, product, self.ids.set_price.text, price, self.ids.link.text)
                    self.ids.output_label.text = f'Product Successfully Added' \
                                                 f'\nTo start tracking click \'Start Tracking\' button'
                    self.ids.disable_add_product_button.disabled = True
                    self.ids.disable_remove_product_button.disabled = False
                    self.ids.disable_start_track_button.disabled = False


                elif get and self.ids.set_price.text.isnumeric() and not self.ids.email.text.endswith('@gmail.com'):

                    self.ids.output_label.text = f'Invalid email'
                    self.ids.email.text = ""

                elif not get and self.ids.set_price.text.isnumeric() and self.ids.email.text.endswith('@gmail.com'):

                    self.ids.output_label.text = f'Invalid Link'
                    self.ids.link.text = ""


                elif get and not self.ids.set_price.text.isnumeric() and self.ids.email.text.endswith('@gmail.com'):

                    self.ids.output_label.text = f'Invalid Set Price'
                    self.ids.set_price.text = ""

                elif get and not self.ids.set_price.text.isnumeric() and not self.ids.email.text.endswith('@gmail.com'):

                    self.ids.output_label.text = f'Invalid Set Price' \
                                                 f'\nInvalid Email'
                    self.ids.email.text = ""
                    self.ids.set_price.text = ""

                elif not get and self.ids.set_price.text.isnumeric() and not self.ids.email.text.endswith('@gmail.com'):

                    self.ids.output_label.text = f'Invalid Link' \
                                                 f'\nInvalid Email'
                    self.ids.email.text = ""
                    self.ids.link.text = ""

                elif not get and not self.ids.set_price.text.isnumeric() and self.ids.email.text.endswith('@gmail.com'):

                    self.ids.output_label.text = f'Invalid Link' \
                                                 f'\nInvalid Set Price'
                    self.ids.link.text = ""
                    self.ids.set_price.text = ""

                else:

                    self.ids.output_label.text = f'Invalid Link' \
                                                 f'\nInvalid email' \
                                                 f'\nInvaid Set Price'
                    self.ids.link.text = ""
                    self.ids.email.text = ""
                    self.ids.set_price.text = ""

    def remove_product(self):

        self.ids.disable_add_product_button.disabled = False
        self.ids.disable_remove_product_button.disabled = True
        self.ids.disable_start_track_button.disabled = True

        os.remove("price.csv")

        self.ids.email.text = ""
        self.ids.set_price.text = ""
        self.ids.link.text = ""
        self.ids.output_label.text = f'Product Successfully Removed'

    def start(self, dt):

        if 'amazon' in self.ids.link.text:
            info = amazon(self.ids.link.text)
        elif 'flipkart' in self.ids.link.text:
            info = flipkart(self.ids.link.text)
        price, product = info[0], info[1]
        print(price)
        if price <= int(self.ids.set_price.text):
            #alert_system(product, self.ids.link.text, self.ids.email.text)
            self.ids.output_label.text = f'Product: {product}' \
                                         f'\nPrice Drop Alert' \
                                         f'\nPrice Dropped to {price}' \
                                         f'\nMail Sent.' \
                                         f' Tracking Stopped'
            self.ids.disable_start_track_button.disabled = True
            self.ids.disable_stop_track_button.disabled = True
            Clock.unschedule(self.start)

    def start_track(self):
        self.ids.output_label.text = f'Tracking....'
        self.ids.disable_stop_track_button.disabled = False
        self.ids.disable_remove_product_button.disabled = True
        Clock.schedule_interval(self.start, 10)
        self.ids.disable_remove_product_button.disabled = False

    def stop_track(self):
        Clock.unschedule(self.start)
        self.ids.output_label.text = f'Tracking Stopped....'
        self.ids.disable_stop_track_button.disabled = True
        self.ids.disable_remove_product_button.disabled = False


class Product_Price_AlterterApp(App):

    def build(self):
        return MyLayout()


Product_Price_AlterterApp().run()
