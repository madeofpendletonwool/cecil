import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, icons, ProgressBar, ButtonStyle, IconButton, TextButton, Row
from flet.control_event import ControlEvent
from flet.auth.providers.github_oauth_provider import GitHubOAuthProvider
import time
from dell_idrac_scan.test_idrac import test_idrac
from basic_modules.test_nfty_urls import test_ntfy_urls
import os
import yaml
import subprocess
import sys
import shutil

clientid = sys.argv[1]
clientsecret = sys.argv[2]

current_path = os.path.dirname(os.path.abspath(__file__))
config_location = current_path + '/config.yaml'
# Create config

if not os.path.exists(config_location):
    open(config_location, 'w').close()
# Writing config
with open(config_location, 'a') as f:
    line1 = '---'
    linenew = '\n'
    line2 = 'Cecil Configuration File. Modules that you configure will store information in here for setup. DO NOT adjust this file seperately. Working through the GUI configuration for each module will do that for'

    f.writelines([line1, linenew, line2])


def main(page: Page):
    print(clientid)
    print(clientsecret)

    provider = GitHubOAuthProvider(
        client_id=clientid,
        client_secret=clientsecret,
        redirect_url="http://localhost:38355/api/oauth/redirect",
    )

#---Defining Modules---------------------------------------------

    def enable_module(module_enable):
        pass
        # if module_enable == 'dynamic_ip_scan':
        #     bash_script = current_path + '/dynamic_ip_scan/enable_scanner.sh' + f'{} {} {}'
        #     subprocess.run(['bash', bash_script])

    def disable_module(module_disable):
        pass
        # if module_disable == 'dynamic_ip_scan':
        #     bash_script = current_path + '/dynamic_ip_scan/disable_scanner.sh'
        #     subprocess.run(['bash', bash_scipt])

    def verify_config():
        if not os.path.exists(config_location):
            open(config_location, "w").close()

    def test_ntfy(ntfy_report, ntfy_monitor):
        return_value = test_ntfy_urls(ntfy_report.value, ntfy_monitor.value)
        page.go("/ntfytest")
        ntfy_temp_path = current_path + '/basic_modules/ntfytemp.yml'
        temp_save = {}
        temp_save['ntfy_report_url'] = ntfy_report.value
        temp_save['ntfy_monitor_url'] = ntfy_monitor.value

        with open(ntfy_temp_path, 'w') as f:
            yaml.dump(temp_save, f)

    def adjust_ntfy_urls():
        # Copy contents of file1.yml to config.yml
        ntfy_temp_path = current_path + '/basic_modules/ntfytemp.yml'
        with open(ntfy_temp_path, 'r') as file_to_append:
            with open(config_location, 'a') as config_file:
                shutil.copyfileobj(file_to_append, config_file)

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("New ntfy urls saved!"),
            actions=[
                ft.TextButton("Go Home", on_click=close_dlg_home)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def test_idrac_button(ip, user, password):
        return_value = test_idrac(ip.value, user.value, password.value)
        # print(return_value)
        page.go("/idractest")
        # print(idrac_ip.value)
        # test_idrac(idrac_ip.value, idrac_user.value, idrac_pass.value)

    def adjust_ipscan_status(e):
        time.sleep(1)

        # Check config to ensure it's valid

        if os.path.exists(config_location) and os.path.isfile(config_location) and os.access(config_location, os.R_OK):
            with open(config_location, 'r') as file_handle:
                file_content = file_handle.read()
        try:
            config = yaml.safe_load(file_content)
        except yaml.YAMLError as e:
            print(f'This does not appear to be a valid cecil config: {e}')
            config = {}
        else:
            print(f'Error: {config_location} does not exist or is not readable')

        # Check if ipscan is currently enabled - if not, enable it.

        if config is None:
            config = {}
        if 'DynamicIPScannerEnabled' not in config:
            config['DynamicIPScannerEnabled'] = True
        elif config['DynamicIPScannerEnabled']:
            config['DynamicIPScannerEnabled'] = False
        else:
            config['DynamicIPScannerEnabled'] = True

        with open(config_location, 'w') as f:
            yaml.dump(config, f)

        with open(config_location, 'r') as file_handle:
            file_content = file_handle.read()
        if config['DynamicIPScannerEnabled']:
            module_enable = 'dynamic_ip_scan'
            enable_module(module_enable)
        else:
            module_disable = 'dynamic_ip_scan'
            disable_module(module_disable)

        page.go("/statusipscan")

    def get_ip_scan_status():
        if os.path.exists(config_location) and os.path.isfile(config_location) and os.access(config_location, os.R_OK):
            with open(config_location, 'r') as file_handle:
                file_content = file_handle.read()
        try:
            config = yaml.safe_load(file_content)
        except yaml.YAMLError as e:
            print(f'This does not appear to be a valid cecil config: {e}')
            config = {}
        else:
            print(f'Error: {config_location} does not exist or is not readable')

        # Check if ipscan is currently enabled - if not, enable it.

        if config is None:
            config = {}

        if 'DynamicIPScannerEnabled' not in config:
            current_status = 'Disabled'
            return current_status

        elif config['DynamicIPScannerEnabled']:
            current_status = 'Enabled'
            return current_status
        else:
            current_status = 'Disabled'
            return current_status

#---Code for Theme Change----------------------------------------------------------------

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

#--Defining Routes---------------------------------------------------

    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def open_ntfy(e):
        page.go("/ntfysettings")

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
    def go_home(e):
        page.go("/")
    def close_dlg_home(e):
        dlg_modal.open = False
        page.update()
        page.go("/")

    def route_change(e):
        print("Route change:", e.route)
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], ),

                    login_row, logout_row, cecil_row, basic_row, basic_modules_row, alert_row, alert_modules_row, monitor_row, report_modules_row
                ],
            )
        )
        if page.route == "/ntfysettings" or page.route == "/ntfysettings":
            verify_config()
            ntfy_report = ft.TextField(label="Report URL", hint_text="ex. https://ntfy.myserver.com/report")
            ntfy_monitor = ft.TextField(label="Monitor URL", hint_text="ex. https://ntfy.myserver.com/monitor")
            ntfy_settings_row = ft.ResponsiveRow([
                ft.Container(ntfy_report, col={"sm": 3, "md": 4, "xl":4}, padding=5),
                ft.Container(ntfy_monitor, col={"sm": 3, "md": 4, "xl":4}, padding=5),
            ])
            ntfy_text = Text("""
            This is simply where you set the ntfy urls that are passed to the modules for monitors and reports. Enter the ntfy urls in the boxes below and click save. You can also test the urls to ensure you are getting the notifications. Then save them after.
            """)
            ntfy_row = Row(alignment=ft.MainAxisAlignment.CENTER, wrap=True, controls=[ntfy_text])
            page.views.append(
                View(
                    "/ntfysettings",
                    [
                        AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], ),
                        ntfy_row,
                        ntfy_settings_row,
                        Row([ft.ElevatedButton(text="Test", on_click=lambda x: test_ntfy(ntfy_report, ntfy_monitor))
                        ])
                    
                    ],
                )
            )
        if page.route == "/ntfytest":
            page.views.append(
                View(
                    "/ntfytest",
                    [
                    AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue", actions=[theme_icon_button], ),
                    Text("Did your servers get the test messages? If so, click save! Otherwise cancel.", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                    Row([ft.ElevatedButton(text="Save", on_click=lambda x: adjust_ntfy_urls()), ft.ElevatedButton(text="Cancel", on_click=go_home)])

                    ],
                )
            )
        if page.route == "/dynamicip" or page.route == "/dynamicip":
            verify_config()
            scanner_text = Text("""
            The Dynamic IP Scanner is a utility that can be used to check for when a public IP address changes. When your public IP changes, the IP scanner will catch it and send an alert with the IP address that it changed to. You simply need to enable it, and the scanner will begin functioning. It runs a check every 20 mins to see if the Ip has changed.
            """)
            scanner_row = Row(alignment=ft.MainAxisAlignment.CENTER, wrap=True, controls=[scanner_text])
            current_status = get_ip_scan_status()
            scanner_enable = ft.Checkbox(label=f'Currently {current_status}!', value=False, on_change=adjust_ipscan_status)
            scanner_enable_text = Text('Enable the Dynamic IP Scanner?')
            scanner_enable_row = Row(alignment=ft.MainAxisAlignment.CENTER, controls=[scanner_enable_text, scanner_enable])
            page.views.append(
                View(
                    "/dynamicip",
                    [
                        AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], ),
                        scanner_row,
                        scanner_enable_row
                    
                    ],
                )
            )
        if page.route == "/statusipscan" or page.route == "/statusipscan":
            status_scanner_text = Text("""
            Thanks for enabling the IP scanner! We'll start checking your IP for any changes and alert you when we see something.
            Have a great day!
            """)
            status_scanner_row = Row(alignment=ft.MainAxisAlignment.CENTER, controls=[status_scanner_text])
            home_button = ft.ElevatedButton("Go home!", icon="home", on_click=go_home)
            home_button_row = Row(alignment=ft.MainAxisAlignment.CENTER, controls=[home_button])
            page.views.append(
                View(
                    "/dynamicip",
                    [
                        AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], ),
                        status_scanner_row,
                        home_button_row
                    
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
            idrac_settings_row = ft.ResponsiveRow([
                ft.Container(idrac_ip, col={"sm": 3, "md": 4, "xl":4}, padding=5),
                ft.Container(idrac_user, col={"sm": 3, "md": 4, "xl":4}, padding=5),
                ft.Container(idrac_pass, col={"sm": 3, "md": 4, "xl":4}, padding=5)
                # controls=[idrac_ip, idrac_user, idrac_pass])
            ])
            idrac_info = """
    The iDrac Report Module. One of my favorities, this module is able to report health status of aspects of servers that have iDrac cards.
    Enter the ip, username, and password of the iDrac you'd like to begin getting reports on. The most recent report collected will begin showing up below.
    """

            idrac_text = ft.Text(idrac_info, style=ft.TextThemeStyle.BODY_MEDIUM, text_align=ft.TextAlign.CENTER, size=16)
            idrac_row = Row(alignment=ft.MainAxisAlignment.CENTER, wrap=True, controls=[idrac_text])
            page.views.append(
                View(
                    "/idrac",
                    [
                    AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue", actions=[theme_icon_button], ),
                    idrac_row,
                    Text("iDrac Server Reports Setup:", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
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
    page.on_route_change = route_change
    page.on_view_pop = view_pop

#-Create Help Banner-----------------------------------------------------------------------
    def close_banner(e):
        page.banner.open = False
        page.update()

    page.banner = ft.Banner(
        bgcolor=ft.colors.BLUE,
        leading=ft.Icon(ft.icons.WAVING_HAND, color=ft.colors.DEEP_ORANGE_500, size=40),
        content=ft.Text("""
    Welcome to Cecil! This application is an alert and monitoring app built to be as generic as possible with 'modules' built-in to provide functionality. Modules can be used, or can also be ignored simply by selecting them and setting them up. Feel free to click around and utilize them to your heart's content. They all simply require a very easy setup and the app will walk you through it!
    Please login, setup the basic configuration (buttons in the basic config row) and then feel free to pick any one of the modules below that to begin setup!
    """, color=colors.BLACK
        ),
        actions=[
            ft.IconButton(icon=ft.icons.EXIT_TO_APP, on_click=close_banner)
        ],
    )

    def show_banner_click(e):
        page.banner.open = True
        page.update()

    banner_button = ft.ElevatedButton("Help!", on_click=show_banner_click)

#----Login Changes------------------------------------------------------------

    def login_click(e):
        page.login(provider)

    def logout_button_click(e):
        page.logout()

    def on_logout(e):
        toggle_login_session()

    # def on_login(e: ft.LoginEvent):
    def on_login(e):
        print("Access token:", page.auth.token.access_token)
        print("User ID:", page.auth.user.id)
        if not e.error:
            toggle_login_session()
        # Allow Route Changes only after login

    page.on_login = on_login
    logout_button = ft.ElevatedButton("Logout", on_click=logout_button_click)
    login_button = ft.ElevatedButton("Login with GitHub", on_click=login_click)
    login_row = Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[login_button, banner_button])
    logout_row = Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[logout_button, banner_button])
    page.add(login_row, logout_row)

    def toggle_login_session():
        cecil_row.visible = page.auth is None
        login_row.visible = page.auth is None
        logout_row.visible = page.auth is not None
        basic_row.visible = page.auth is not None
        basic_modules_row.visible = page.auth is not None
        alert_row.visible = page.auth is not None
        alert_modules_row.visible = page.auth is not None
        monitor_row.visible = page.auth is not None
        report_modules_row.visible = page.auth is not None
        page.update()

#-Define initial elements-----------------------------------------------------------------


    page.title = "Cecil"
    page.theme_mode = "dark"


    theme_icon_button = ft.IconButton(icons.DARK_MODE, selected_icon=icons.LIGHT_MODE, icon_color=colors.BLACK,
                                   icon_size=35, tooltip="change theme", on_click=change_theme,
                                   style=ButtonStyle(color={"": colors.BLACK, "selected": colors.WHITE}, ), )

    page.appbar = AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], )


    cecil_info = "Please Login to Access the Modules!"

    cecil_text = ft.Text(cecil_info, style=ft.TextThemeStyle.DISPLAY_MEDIUM, text_align=ft.TextAlign.CENTER, size=16)
    cecil_row = Row(alignment=ft.MainAxisAlignment.CENTER, controls=[cecil_text])

    basic_text = ft.Text('Basic Config:', style=ft.TextThemeStyle.HEADLINE_MEDIUM)
    basic_row = Row(alignment=ft.MainAxisAlignment.CENTER, controls=[basic_text])
    
    alert_text = ft.Text('Alerts/Monitors:', style=ft.TextThemeStyle.HEADLINE_MEDIUM, )
    alert_row = Row(alignment=ft.MainAxisAlignment.CENTER, controls=[alert_text])

    monitor_text = ft.Text('Reports:', style=ft.TextThemeStyle.HEADLINE_MEDIUM)
    monitor_row = Row(alignment=ft.MainAxisAlignment.CENTER, controls=[monitor_text])

    dell_button = ElevatedButton("iDrac Server Health Report", on_click=open_idrac)
    docker_monitor_button = ElevatedButton("Docker Monitor", on_click=open_dockermon)
    linux_health_button = ElevatedButton("Linux Health Report", on_click=open_linuxhealth)
    Dynamic_ip_button = ElevatedButton("Dynamic IP Checker", on_click=open_dynamicip)
    ntfy_config_button = ElevatedButton("ntfy Setup", on_click=open_ntfy)

    basic_modules_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ntfy_config_button])
    alert_modules_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[docker_monitor_button, Dynamic_ip_button])
    report_modules_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[dell_button, linux_health_button])


    toggle_login_session()
    page.add(cecil_row, basic_row, basic_modules_row, alert_row, alert_modules_row, monitor_row, report_modules_row)

# Browser Version
ft.app(target=main, view=ft.WEB_BROWSER, port=38355)
# ft.app(target=main)
# App Version
# ft.app(target=main, port=8034)