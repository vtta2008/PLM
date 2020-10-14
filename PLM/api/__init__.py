# -*- coding: utf-8 -*-
"""

Script Name: api.__init__
Author: Do Trinh/Jimmy - 3D artist.

Description:

    API is the acronym for Application Programming Interface, which is a software intermediary that allows two
    applications to talk to each other. Each time you use an app like Facebook, send an instant message, or check the
    weather on your phone, you’re using an API.

    EXAMPLE OF AN API

    When you use an application on your mobile phone, the application connects to the Internet and sends data to a server.
    The server then retrieves that data, interprets it, performs the necessary actions and sends it back to your phone.
    The application then interprets that data and presents you with the information you wanted in a readable way. This is
    what an API is - all of this happens via API.

    To explain this better, let us take a familiar example.

    Imagine you’re sitting at a table in a restaurant with a menu of choices to order from. The kitchen is the part of
    the “system” that will prepare your order. What is missing is the critical link to communicate your order to the
    kitchen and deliver your food back to your table. That’s where the waiter or API comes in. The waiter is the
    messenger – or API – that takes your request or order and tells the kitchen – the system – what to do. Then the
    waiter delivers the response back to you; in this case, it is the food.

    Here is a real-life API example. You may be familiar with the process of searching flights online. Just like the
    restaurant, you have a variety of options to choose from, including different cities, departure and return dates,
    and more. Let us imagine that you’re booking you are flight on an airline website. You choose a departure city and
    date, a return city and date, cabin class, as well as other variables. In order to book your flight, you interact
    with the airline’s website to access their database and see if any seats are available on those dates and what the
    costs might be.

"""
# -------------------------------------------------------------------------------------------------------------


from .version import Version

# This is API version
__version__ = Version('Incremental', 0, 0, 1)

__title__ = 'API'

__all__ = ['__version__']


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
