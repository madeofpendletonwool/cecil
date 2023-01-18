import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, icons, ProgressBar, ButtonStyle, IconButton, TextButton, Row
from flet.control_event import ControlEvent
import time
from dell_idrac_scan.test_idrac import test_idrac
import os

current_path = os.path.dirname(os.path.abspath(__file__))
print(current_path)


def main(page: Page):

    def test_idrac_button(ip, user, password):
        return_value = test_idrac(ip.value, user.value, password.value)
        # print(return_value)
        print('test')
        page.go("/idractest")
        # print(idrac_ip.value)
        # test_idrac(idrac_ip.value, idrac_user.value, idrac_pass.value)


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

    def open_idrac(e):
        page.go("/idrac")
    def open_idrac_result(e):
        page.go("/idrac/result")

    def open_dockermon(e):
        page.go("/dockermon")
    def open_linuxhealth(e):
        page.go("/linuxhealth")
    def open_dynamicip(e):
        page.go("/dynamicip")

    page.title = "Cecil"
    page.theme_mode = "dark"


    theme_icon_button = ft.IconButton(icons.DARK_MODE, selected_icon=icons.LIGHT_MODE, icon_color=colors.BLACK,
                                   icon_size=35, tooltip="change theme", on_click=change_theme,
                                   style=ButtonStyle(color={"": colors.BLACK, "selected": colors.WHITE}, ), )

    page.appbar = AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], )


    cecil_info = """
    Welcome to Cecil! This application is an alert and monitoring app built to be as generic as possible with 'modules' built-in to provide functionality. 
    Modules can be used, or can also be ignored simply by selecting them and setting them up. Feel free to click around and utilize them to your heart's content. 
    They all simply require a very easy setup and the app will walk you through it!
    Feel free to pick any one of the modules below and begin setup!
    """

    cecil_text = ft.Text(cecil_info, style=ft.TextThemeStyle.BODY_MEDIUM, text_align=ft.TextAlign.CENTER, size=16)
    cecil_row = Row(alignment=ft.MainAxisAlignment.CENTER, controls=[cecil_text])

    alert_text = ft.Text('Alerts/Monitors:', style=ft.TextThemeStyle.HEADLINE_MEDIUM, )
    alert_row = Row(alignment=ft.MainAxisAlignment.CENTER, controls=[alert_text])

    monitor_text = ft.Text('Reports:', style=ft.TextThemeStyle.HEADLINE_MEDIUM)
    monitor_row = Row(alignment=ft.MainAxisAlignment.CENTER, controls=[monitor_text])

    dell_button = ElevatedButton("iDrac Server Health Report", on_click=open_idrac)
    docker_monitor_button = ElevatedButton("Docker Monitor", on_click=open_dockermon)
    linux_health_button = ElevatedButton("Linux Health Report", on_click=open_linuxhealth)
    Dynamic_ip_button = ElevatedButton("Dynamic IP Checker", on_click=open_dynamicip)

    alert_modules_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[docker_monitor_button, Dynamic_ip_button])
    report_modules_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[dell_button, linux_health_button])


    def route_change(e):
        print("Route change:", e.route)
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], ),
                    cecil_row, alert_row, alert_modules_row, monitor_row, report_modules_row
                ],
            )
        )
        if page.route == "/dynamicip" or page.route == "/dynamicip":
            page.views.append(
                View(
                    "/dynamicip",
                    [
                        AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], ),
                    Text('DynamicIP Scanner Setup page!')
                    ],
                )
            )
        if page.route == "/linuxhealth" or page.route == "/linuxhealth":
            page.views.append(
                View(
                    "/linuxhealth",
                    [
                        AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], ),
                    Text('Linux Health Scan Setup page!')
                    ],
                )
            )
        if page.route == "/dockermon":
            page.views.append(
                View(
                    "/dockermon",
                    [
                        AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], ),
                    Text('Docker Monitor Setup page!')
                    ],
                )
            )
        if page.route == "/idrac":
            idrac_ip = ft.TextField(label="IP Address", hint_text="ex. 10.0.0.1")
            idrac_user = ft.TextField(label="Username", hint_text="ex. root")
            idrac_pass = ft.TextField(label="Password", can_reveal_password=True, password=True, hint_text="ex. password1")
            idrac_settings_row = ft.Row(controls=[idrac_ip, idrac_user, idrac_pass])
            idrac_info = """
    The iDrac Report Module. One of my favorities, this module is able to report health status of aspects of servers that have iDrac cards.
    Enter the ip, username, and password of the iDrac you'd like to begin getting reports on. The most recent report collected will begin showing up below.
    """

            idrac_text = ft.Text(idrac_info, style=ft.TextThemeStyle.BODY_MEDIUM, text_align=ft.TextAlign.CENTER, size=16)
            idrac_row = Row(alignment=ft.MainAxisAlignment.CENTER, controls=[idrac_text])
            page.views.append(
                View(
                    "/idrac",
                    [
                    AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue", actions=[theme_icon_button], ),
                    idrac_row,
                    Text("iDrac Setup Settings:", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                    idrac_settings_row,
                    Row([ft.ElevatedButton(text="Test", on_click=lambda x: test_idrac_button(idrac_ip, idrac_user, idrac_pass)), ft.ElevatedButton(text="Save")]),
                    Text("Most Recent Scan Results:", style=ft.TextThemeStyle.HEADLINE_MEDIUM),       
                    ],
                )
            )
        if page.route == "/idractest":
            with open(current_path + '/dell_idrac_scan/idractest.txt', 'r') as file:
                data = file.read()
            test_result = Text(data)
            page.views.append(
                View(
                    "/idractest",
                    [
                    AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue", actions=[theme_icon_button], ),
                    Text("iDrac Test Setup Results:", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                    test_result
                    ],
                )
            )

    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.add(cecil_row, alert_row, alert_modules_row, monitor_row, report_modules_row)

# Browser Version
ft.app(target=main, view=ft.WEB_BROWSER, port=38355)
# App Version
# ft.app(target=main, port=8034)