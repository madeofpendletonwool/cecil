import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, icons, ProgressBar, ButtonStyle, IconButton, TextButton, Row
from flet.control_event import ControlEvent
import time




def main(page: Page):

    def change_theme(e):
        """
        When the button(to change theme) is clicked, the progress bar is made visible, the theme is changed,
        the progress bar is made invisible, and the page is updated

        :param e: The event that triggered the function
        """
        # page.splash.visible = True
        page.update()
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        # page.splash.visible = False
        theme_icon_button.selected = not theme_icon_button.selected
        time.sleep(.3)
        page.update()

    page.title = "Cecil"
    page.theme_mode = "light"


    theme_icon_button = ft.IconButton(icons.DARK_MODE, selected_icon=icons.LIGHT_MODE, icon_color=colors.BLACK,
                                   icon_size=35, tooltip="change theme", on_click=change_theme,
                                   style=ButtonStyle(color={"": colors.BLACK, "selected": colors.WHITE}, ), )

    page.appbar = AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], )

    def open_mail_settings(e):
        page.go("/settings/mail")

    def open_settings(e):
        page.go("/settings")



    def route_change(e):
        print("Route change:", e.route)
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], ),
                    ElevatedButton("Go to settings", on_click=open_settings),
                ],
            )
        )
        if page.route == "/settings" or page.route == "/settings/mail":
            page.views.append(
                View(
                    "/settings",
                    [
                        AppBar(title=Text("Settings"), bgcolor=colors.SURFACE_VARIANT),
                        Text("Settings!", style="bodyMedium"),
                        ElevatedButton(
                            "Go to mail settings", on_click=open_mail_settings
                        ),
                    ],
                )
            )
        if page.route == "/settings/mail":
            page.views.append(
                View(
                    "/settings/mail",
                    [
                        AppBar(
                            title=Text("Mail Settings"), bgcolor=colors.SURFACE_VARIANT
                        ),
                        Text("Mail settings!"),
                    ],
                )
            )
        page.update()

    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    test = Text("Hello")
    page.add(test, ElevatedButton("Go to settings", on_click=open_settings))

    # page.go(page.route)




    # def route_change(e):
    #     print("Route change:", e.route)
    #     page.views.clear()
    #     page.views.append(
    #         View(
    #             "/",
    #             [
    #                 AppBar(title=Text("Cecil - Alerts, Monitoring, and Home for Information"), center_title=True),
    #                 ElevatedButton("Go to settings", on_click=open_settings),
    #             ],
    #         )
    #     )
    #     if page.route == "/settings" or page.route == "/settings/mail":
    #         page.views.append(
    #             View(
    #                 "/settings",
    #                 [
    #                     AppBar(title=Text("Settings"), bgcolor=colors.SURFACE_VARIANT),
    #                     Text("Settings!", style="bodyMedium"),
    #                     ElevatedButton(
    #                         "Go to mail settings", on_click=open_mail_settings
    #                     ),
    #                 ],
    #             )
    #         )
    #     if page.route == "/settings/mail":
    #         page.views.append(
    #             View(
    #                 "/settings/mail",
    #                 [
    #                     AppBar(
    #                         title=Text("Mail Settings"), bgcolor=colors.SURFACE_VARIANT
    #                     ),
    #                     Text("Mail settings!"),
    #                 ],
    #             )
    #         )
    #     page.update()

    # def view_pop(e):
    #     print("View pop:", e.view)
    #     page.views.pop()
    #     top_view = page.views[-1]
    #     page.go(top_view.route)

    # page.on_route_change = route_change
    # page.on_view_pop = view_pop

    # page.go(page.route)


ft.app(target=main, view=ft.WEB_BROWSER)