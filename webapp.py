import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, icons, ProgressBar, ButtonStyle, IconButton, TextButton, Row
# from flet.control_event import ControlEvent
from flet import ControlEvent
from flet.auth.providers.github_oauth_provider import GitHubOAuthProvider
import time
from dell_idrac_scan.test_idrac import test_idrac
from basic_modules.test_nfty_urls import test_ntfy_urls
from basic_modules.functions import send_monitor_notification
from basic_modules.functions import send_alert_notification
from cryptography.fernet import Fernet
import basic_modules.functions
import basic_modules.test_nfty_urls
import os
import yaml
import subprocess
import sys
import shutil
import datetime
from datetime import datetime, timedelta
import schedule
import threading
from croniter import croniter
import pytz
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Python webapp startup')

# Add the arguments
parser.add_argument('--config_path',
                    metavar='config_path',
                    type=str,
                    help='the path to configuration')

parser.add_argument('--client_id',
                    metavar='client_id',
                    type=str,
                    help='the client id')

parser.add_argument('--client_secret',
                    metavar='client_secret',
                    type=str,
                    help='the client secret')

parser.add_argument('--auth_url',
                    metavar='auth_url',
                    type=str,
                    help='the authentication url')

parser.add_argument('--encryption_key',
                    metavar='encryption_key',
                    type=str,
                    help='the encryption key')

parser.add_argument('--username',
                    metavar='username',
                    type=str,
                    help='the username')

parser.add_argument('--password',
                    metavar='password',
                    type=str,
                    help='the password')

# Execute parse_args()
args = parser.parse_args()

# You can access the values with args.<name>, for example:
config_path = args.config_path or '/home/cecil/'
clientid = args.client_id or 'testing'
clientsecret = args.client_secret or 'testing'
authurl = args.auth_url or 'testing'
encryption_key = args.encryption_key or 'testing'
username = args.username or 'cecil'
password = args.password or 'cecil'




cipher_suite = Fernet(encryption_key.encode())


if clientid == False:
    clientid = 'testing'
if clientsecret == False:
    clientsecret = 'testing'
if authurl == False:
    authurl = 'testing'

current_path = os.path.dirname(os.path.abspath(__file__))
config_location = current_path + '/config.yaml'
# Create config
if not os.path.exists(config_location):
    with open(config_location, 'w') as file:
        file.write("---\n")
        file.write("file_metadata:\n")
        file.write("  description: 'Cecil Configuration File. Modules that you configure will store information in here for setup. DO NOT adjust this file seperately. Working through the GUI configuration for each module will do that for'\n")
        file.write("config:\n")

# Open the file and load its contents into a Python object
with open(config_location, 'r') as file:
    file_contents = file.read()


def main(page: Page):
#---Snackbar fucntionality----------------------------------------
    def show_snackbar(page, message):
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
        page.update()

    # Get ntfy urls

    with open(config_location, 'r') as file:
        config_data = yaml.safe_load(file)

    ntfy_monitor_url = config_data.get('ntfy_monitor_url', None)
    ntfy_report_url = config_data.get('ntfy_report_url', None)

    if ntfy_monitor_url:
        print("ntfy_monitor_url:", ntfy_monitor_url)
    else:
        print("ntfy_monitor_url not found in the config")
        message = "ntfy_monitor_url not found in the config. Please Configure this in the ntfy Setup Module prior to using other modules."
        show_snackbar(page, message)

    if ntfy_report_url:
        print("ntfy_report_url:", ntfy_report_url)
    else:
        print("ntfy_report_url not found in the config")
        message = "ntfy_report_url not found in the config.  Please Configure this in the ntfy Setup Module prior to using other modules."
        show_snackbar(page, message)




    print(f'Clientid in python {clientid}')
    print(f'client secret in python {clientsecret}')
    print(f'auth url in python {authurl}')
    try:
        response = requests.get(authurl)
        print("Accessible URL:", response.status_code)
    except:
        print("Inaccessible URL")


    provider = GitHubOAuthProvider(
        client_id=clientid,
        client_secret=clientsecret,
        redirect_url=authurl,
    )
    print(provider)


#---Creating Class for module creation---------------------------



    class Module_Change:
        def __init__(self, page, config_location, windows_name=None, windows_domain=None, windows_user=None, windows_pass=None, windows_file_path=None, windows_cron="* * * * *", windows_check_frequency=None):
            # Windows File Checker Vars
            self.windows_name = windows_name
            self.windows_domain = windows_domain
            self.windows_user = windows_user
            self.windows_pass = windows_pass
            self.windows_file_path = windows_file_path
            self.windows_cron = windows_cron
            self.windows_check_frequency = windows_check_frequency
            self.page = page
            self.config_location = config_location

            # self.setup_wfc()

        def run_schedule(self):
            while True:
                print('run pending')
                schedule.run_pending()
                time.sleep(10)

        def show_info_snackbar(self, message):
            self.page.snack_bar = ft.SnackBar(ft.Text(message))
            self.page.snack_bar.open = True
            self.page.update()

        def run_wfc_and_reschedule(self, cron_iter, job):
            print("Running run_wfc_and_reschedule for", self.windows_file_path)
            self.run_wfc()
            timezone = pytz.timezone("America/Chicago")
            now = datetime.now(timezone)
            next_run = cron_iter.get_next(datetime)  # Already timezone-aware
            interval = (next_run - now).total_seconds()
            print("Rescheduling the job with an interval of", interval, "seconds")

            job.interval = interval


        def setup_wfc(self):
            # ...

            # Create a separate thread to handle scheduling
            scheduler_thread = threading.Thread(target=self.run_schedule, daemon=True)
            scheduler_thread.start()  # ...to here

            def wfc_wrapper():
                print("wfc_wrapper called")  # Add this print statement
                self.run_wfc_and_reschedule(cron_iter, self.job if hasattr(self, 'job') else None)

            cron_string = self.windows_cron
            cron_iter = croniter(cron_string)
            timezone = pytz.timezone("America/Chicago")
            now = datetime.now(timezone)

            # Round the current time down to the nearest minute
            now_rounded = now.replace(second=0, microsecond=0)
            
            next_run = cron_iter.get_next(datetime, start_time=now_rounded)

            # Calculate the interval in seconds
            interval = (next_run - now).total_seconds()
            interval = round(interval)  # Round the interval to remove decimals

            print("cron_string:", cron_string)
            print("interval:", interval)

            # Cancel the existing job if it exists
            if hasattr(self, 'job') and self.job is not None:
                schedule.cancel_job(self.job)

            # Schedule the new job
            self.job = schedule.every(interval).seconds.do(wfc_wrapper)
            print("Job scheduled:", self.job)


        
        def delete_wfc_config(self):
            def close_wfc_dlg(e):
                delete_wfc_dlg.open = False
                self.page.update()

            def delete_wfc(e):
                delete_wfc_dlg.open = False
                self.page.update()

            print('test')

            delete_wfc_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Would you like to delete the WFC for {self.windows_file_path}?"),
            actions=[
            ft.TextButton(content=ft.Text("Delete WFC", color=ft.colors.RED_400), on_click=delete_wfc),
            ft.TextButton("Cancel", on_click=close_wfc_dlg)
            ],
            actions_alignment=ft.MainAxisAlignment.END
            )

            self.page.dialog = delete_wfc_dlg
            delete_wfc_dlg.open = True
            self.page.update()
    

        def run_wfc(self):
            from smb.SMBConnection import SMBConnection
            import os
            print('running wfc')

            def authenticate_windows_machine(username, password, domain, server_name):
                try:
                    conn = SMBConnection(username, password, "client_machine_name", server_name, domain=domain, use_ntlm_v2=True, is_direct_tcp=True)
                    success = conn.connect(server_name, 445)

                    if success:
                        print("Authentication successful")
                        return conn

                    else:
                        print("Authentication failed")
                        return None

                except Exception as e:
                    print("Error:", e)
                    return None

            conn = authenticate_windows_machine(self.windows_user, self.windows_pass, self.windows_domain, self.windows_name)

            if conn is None:
                print("Cannot perform the file check due to authentication failure")
                message = "Cannot perform the file check due to authentication failure"
                show_snackbar(page, message)
                return

            # Check if any new files have been created in the specified folder within the last specified hours
            share_folder = self.windows_file_path
            check_frequency = int(self.windows_check_frequency)

            # Calculate the cutoff datetime
            now = datetime.now()
            cutoff_time = now - timedelta(hours=check_frequency)

            # List files in the shared folder
            _, share_name_and_path = share_folder[2:].split('\\', 1)
            share_name, *folders = share_name_and_path.split('\\')
            path = '/' + '/'.join(folders)  # Convert the path format

            files = conn.listPath(share_name, path)  # Add this line to list the files

            # List all files in the shared folder
            file_list_message = "All files in the shared folder:\n"
            for f in files:
                file_list_message += f"{f.filename} {datetime.fromtimestamp(f.last_attr_change_time)}\n"

            # send_monitor_notification(ntfy_monitor_url, file_list_message)

            cutoff_message = f"Cutoff time: {cutoff_time}"
            # send_monitor_notification(ntfy_monitor_url, file_list_message)

            # Check if any files have NOT been modified within the specified time period
            no_new_files = [f for f in files if f.filename not in ['.', '..'] and datetime.fromtimestamp(f.last_attr_change_time) <= cutoff_time]  # Ignore . and .. files

            # Consolidate messages into a single string
            consolidated_message = f"File check for {self.windows_file_path}:\n\n"
            consolidated_message += f"No new files created within the last {check_frequency} hours. All files in the shared folder:\n" + file_list_message + "\n"
            consolidated_message += "Cutoff time: " + cutoff_message + "\n\n"

            if no_new_files:
                ticket_summary = "No new files found within the specified time period"
                cw_ticket = load_cw_info()

                # Append the summary and content to the ticket only if the CW configuration is available
                if cw_ticket:
                    cw_ticket['ticket_summary'] = ticket_summary
                    cw_ticket['ticket_content'] = consolidated_message

                send_monitor_notification(ntfy_monitor_url, consolidated_message, cw_ticket)


    user_modules = Module_Change(page, config_location)



#---Defining Modules---------------------------------------------
    # Establish basic functionality

    def enable_module(module_enable):
        print(module_enable)
        # Get Monitor Urls
        with open(config_location, 'r') as file:
            config = yaml.safe_load(file)

        monitor_url = config['ntfy_monitor_url']
        report_url = config['ntfy_report_url']

        if module_enable == 'dynamic_ip_scan':

            bash_script = current_path + '/dynamic_ip_scan/enable_scanner.sh'
            subprocess.run(['bash', bash_script, monitor_url])

    def disable_module(module_disable):
        if module_disable == 'dynamic_ip_scan':
            bash_script = current_path + '/dynamic_ip_scan/disable_scanner.sh'
            subprocess.run(['bash', bash_script])


    def verify_config():
        if not os.path.exists(config_location):
            open(config_location, "w").close()

    def load_cw_config(config_location):
        with open(config_location, 'r') as file_handle:
            config = yaml.safe_load(file_handle)

        if config is None or config.get('config') is None:
            print(f"No valid configuration found at {config_location}")
            return []

        cw_config_list = config.get('config', {}).get('cw', [])
        if not isinstance(cw_config_list, list):
            cw_config_list = [cw_config_list]

        # Select only the required keys from the CW config
        filtered_cw_configs = [
            {key: cw_config[key] if not isinstance(cw_config[key], bytes) else cw_config[key].decode() for key in ('board_id', 'company_id', 'domain', 'public_key', 'ticket_company') if key in cw_config}
            for cw_config in cw_config_list
        ]

        return filtered_cw_configs




    def load_cw_info():
        with open(config_location, 'r') as file_handle:
            config = yaml.safe_load(file_handle)
            
        # Extract CW configuration from the loaded config
        cw_config = config.get('config', {}).get('cw', [])[0] if config.get('config', {}).get('cw') else {}

        if cw_config:
            # If 'private_key' and 'clientid' are present, encode and decrypt them
            if 'private_key' in cw_config and 'clientid' in cw_config:
                private_key_encrypted = cw_config.get('private_key').encode()  # If it's not already bytes
                private_key_decrypted = cipher_suite.decrypt(private_key_encrypted).decode()  # Decodes to string

                clientid_encrypted = cw_config.get('clientid').encode()  # If it's not already bytes
                clientid_decrypted = cipher_suite.decrypt(clientid_encrypted).decode()  # Decodes to string
            else:
                print("'private_key' and/or 'clientid' not found in CW configuration.")
                return {}

            # Package the information into a dictionary
            cw_ticket = {
                'company': cw_config.get('ticket_company'),
                'public_key': cw_config.get('public_key'),
                'private_key': private_key_decrypted,
                'domain': cw_config.get('domain'),
                'clientid': clientid_decrypted,
                'board_id': cw_config.get('board_id'),
                'company_id': cw_config.get('company_id')
            }
            return cw_ticket
        else:
            print("No CW configuration found.")
            return {}



    def save_wfc_config(config_location, wfc_config):
        with open(config_location, 'r') as file_handle:
            config = yaml.safe_load(file_handle)

        if config is None:
            config = {'config': {}}

        if 'config' not in config:
            config['config'] = {}
        elif config['config'] is None:
            config['config'] = {}

        if 'wfc' not in config['config']:
            config['config']['wfc'] = []

        config['config']['wfc'].append(wfc_config)

        with open(config_location, 'w') as file_handle:
            yaml.dump(config, file_handle)

    def save_cw_config(page, ticket_company, public_key, private_key, domain, clientid, board_id, company_id):
        en_private_key = cipher_suite.encrypt(private_key.encode("utf-8"))
        en_clientid = cipher_suite.encrypt(clientid.encode("utf-8"))
        cw_config = {
            "ticket_company": ticket_company,
            "public_key": public_key,
            "private_key": en_private_key,
            "domain": domain,
            "clientid": en_clientid,
            "board_id": str(board_id),
            "company_id": str(company_id)
        }

        with open(config_location, 'r') as file_handle:
            config = yaml.safe_load(file_handle)

        if config is None:
            config = {'config': {}}

        if 'config' not in config:
            config['config'] = {}
        elif config['config'] is None:
            config['config'] = {}

        # Replaces the existing 'cw' configuration if it exists, otherwise creates a new one
        config['config']['cw'] = [cw_config]

        with open(config_location, 'w') as file_handle:
            yaml.dump(config, file_handle)

        message = "CW Ticket Config Saved!"
        show_snackbar(page, message)


    def get_cw_config(config_location):
        with open(config_location, 'r') as file_handle:
            config = yaml.safe_load(file_handle)

        if config is None or config.get('config') is None:
            print(f"No 'config' section found in the configuration file at {config_location}")
            return []
                
        wfc_configs = config['config'].get('wfc', [])
        return wfc_configs


    def load_wfc_configs(config_location):
        with open(config_location, 'r') as file_handle:
            config = yaml.safe_load(file_handle)

        if config is None or config.get('config') is None:
            print(f"No 'config' section found in the configuration file at {config_location}")
            return []
                    
        wfc_configs = config['config'].get('wfc', [])

        # Decrypt the windows_pass in each configuration
        for wfc_config in wfc_configs:
            encrypted_pass = wfc_config.get('windows_pass')
            if encrypted_pass:
                wfc_config['windows_pass'] = cipher_suite.decrypt(encrypted_pass).decode('utf-8')

        return wfc_configs



    wfc_configs = load_wfc_configs(config_location)

    if not wfc_configs:
        print("No wfc configs found.")
    else:
        # create a list to hold all module_change_instances
        module_change_instances = []
        for wfc_config in wfc_configs:
            windows_name = wfc_config['windows_name']
            windows_domain = wfc_config['windows_domain']
            windows_user = wfc_config['windows_user']
            windows_pass = wfc_config['windows_pass']
            windows_file_path = wfc_config['windows_file_path']
            windows_cron = wfc_config['windows_cron']
            windows_check_frequency = wfc_config['windows_check_frequency']

            module_change_instance = Module_Change(
                page,
                config_location,
                windows_name=windows_name,
                windows_domain=windows_domain,
                windows_user=windows_user,
                windows_pass=windows_pass,
                windows_file_path=windows_file_path,
                windows_cron=windows_cron,
                windows_check_frequency=windows_check_frequency
            )
            module_change_instances.append(module_change_instance)

        # Now that all properties have been set, we can setup the job for the first instance
        module_change_instances[0].setup_wfc()





    #Funtions for Basic Vars

    def test_ntfy(ntfy_report, ntfy_monitor):
        return_value = test_ntfy_urls(ntfy_report.value, ntfy_monitor.value)
        page.go("/ntfytest")
        ntfy_temp_path = current_path + '/basic_modules/ntfytemp.yml'
        temp_save = {}
        temp_save['ntfy_report_url'] = ntfy_report.value
        temp_save['ntfy_monitor_url'] = ntfy_monitor.value

        with open(ntfy_temp_path, 'w') as f:
            yaml.dump(temp_save, f)

    def get_ntfy_urls():
        with open(config_location, 'r') as file:
            config = yaml.safe_load(file)
        # Check current ntfy servers. Report if not set.

        if 'ntfy_monitor_url' not in config:
            current_monitor_url = 'Not currently set'
            current_report_url = 'Not currently set'
            return current_monitor_url, current_report_url

        elif config['ntfy_monitor_url']:
            current_monitor_url = config['ntfy_monitor_url']
            current_report_url = config['ntfy_report_url']
            return current_monitor_url, current_report_url

    def adjust_ntfy_urls():
        #Function to close the saved dialog
        def close_dlg(e):
            dlg_modal.open = False
            page.update()
        # Set tested urls path
        ntfy_temp_path = current_path + '/basic_modules/ntfytemp.yml'
        # Load config into a dictionary
        with open(config_location, 'r') as file_handle:
            config = yaml.safe_load(file_handle)

        # Update the desired keys in the dictionary
        with open(ntfy_temp_path, 'r') as temp_file:
            temp_config = yaml.safe_load(temp_file)
        config.update(temp_config)

        # Write the updated key-value pairs to a temporary file
        temp_file = current_path + '/temp_config.yaml'
        with open(config_location, 'w') as file_handle:
            yaml.dump(config, file_handle)

        # Rename the temporary file to the original file
        os.rename(temp_file, config_location)
        os.remove(ntfy_temp_path)

            # with open(config_location, 'a') as config_file:
            #     config_file.write('\n')
            #     shutil.copyfileobj(file_to_append, config_file)

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("New ntfy urls saved!"),
            content=ft.Text("You can now return home!"),
            actions=[
                ft.TextButton("Ok", on_click=close_dlg)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    class Idrac:
        def __int__(self):
            self.idrac_host=None
            self.idrac_user=None
            self.idrac_pass=None
        def test_idrac_button(self, ip, user, password):

            self.idrac_host = ip.value
            self.idrac_user = user.value
            self.idrac_pass = password.value

            return_value = test_idrac(self.idrac_host, self.idrac_user, self.idrac_pass)


            def close_idrac_test_dlg(e):
                validate_idrac_dlg.open = False
                page.update()

            validate_idrac_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text(f"iDrac Test Results:"),
                content=ft.Column(controls=[
                    #     ft.Text(f"Setup MFA:", selectable=True),
                    ft.Text(f'{return_value}', selectable=True),
                    # ], tight=True),

                    # actions=[
                    mfa_validate_select_row
                ],
                    tight=True),
                actions_alignment=ft.MainAxisAlignment.END,
            )

            print(return_value)
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
        config = yaml.safe_load(file_content)

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

    def test_cw(page, ticket_company, public_key, private_key, domain, clientid, board_id, company_id):

        pr = ft.ProgressRing()
        progress_stack = ft.Stack([pr], bottom=25, right=30, left=20, expand=True)
        page.overlay.append(progress_stack)
        def close_dlg(e):
            ticket_dlg.open = False
            page.update()
        ticket_summary = "This is a test ticket from Cecil!"
        ticket_content = "Hi from Cecil!"

        ticket_created = basic_modules.functions.create_ticket(ticket_company, public_key, private_key, domain, clientid, board_id, company_id, ticket_summary, ticket_content, encryption_key)
        # ticket_created = "test"

        ticket_dlg = ft.AlertDialog(
            title=ft.Text("Ticket Status"),
            content=ft.Text(ticket_created),
            actions=[
            ft.TextButton("Save", on_click=lambda x: (save_cw_config(page, ticket_company, public_key, private_key, domain, clientid, board_id, company_id), close_dlg)),
            ft.TextButton("Close", on_click=close_dlg),
        ],
        )

        def open_dlg(page):
            page.dialog = ticket_dlg
            ticket_dlg.open = True
            page.update()

        page.overlay.remove(progress_stack)
        open_dlg(page)

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
    def open_ticketing(e):
        page.go("/ticketingsetup")

    def open_idrac(e):
        page.go("/idrac")
    def open_idrac_result(e):
        page.go("/idrac/result")

    def open_wfc(e):
        page.go("/wfc")

    def open_dockermon(e):
        page.go("/dockermon")
    def open_linuxhealth(e):
        page.go("/linuxhealth")
    def open_dynamicip(e):
        page.go("/dynamicip")
    def go_home(e):
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
            current_monitor_url, current_report_url = get_ntfy_urls()
            current_monitor = ft.Text(f'The monitor URL is set to: {current_monitor_url}', style=ft.TextThemeStyle.BODY_MEDIUM, size=32)
            current_report = ft.Text(f'The Report URL is set to: {current_report_url}', style=ft.TextThemeStyle.BODY_MEDIUM, size=32)
            ntfy_sep = ft.Card(content=ft.Container(Text("Current ntfy server Settings", weight="bold", style=ft.TextThemeStyle.BODY_MEDIUM, size=25), padding=8, expand=True))
            page.views.append(
                View(
                    "/ntfysettings",
                    [
                        AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], ),
                        ntfy_row,
                        ntfy_settings_row,
                        Row([ft.ElevatedButton(text="Test", on_click=lambda x: test_ntfy(ntfy_report, ntfy_monitor))]),
                        ntfy_sep,
                        current_monitor,
                        current_report
                    ]
                    ,
                )
            )
        if page.route == "/ticketingsetup" or page.route == "/ticketingsetup":
            # Get current ticketing settings
            cw_configs = load_cw_config(config_location)

            cw_table_rows = []

            for cw_config in cw_configs:
                board_id = cw_config['board_id']
                domain = cw_config['domain']
                company_id = cw_config['company_id']
                public_key = cw_config['public_key']
                ticket_company = cw_config['ticket_company']
                
                print(f"Board ID: {board_id}, Domain: {domain}, Company ID: {company_id}, Public Key: {public_key}, Ticket Company: {ticket_company}")

                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(ticket_company)),
                        ft.DataCell(ft.Text(domain)),
                        ft.DataCell(ft.Text(company_id)),
                        ft.DataCell(ft.Text(board_id)),
                        ft.DataCell(ft.Text(public_key))
                    ],
                    # Add any necessary on_select_changed or other event handlers here
                    on_select_changed=(
                        lambda user_modules_copy: 
                            lambda x: user_modules_copy.delete_wfc_config()
                    )(user_modules)
                )

                cw_table_rows.append(row)

            cw_table = ft.DataTable(
                # Add desired styling options here
                columns=[
                    ft.DataColumn(ft.Text("Ticket Company")),
                    ft.DataColumn(ft.Text("Domain")),
                    ft.DataColumn(ft.Text("Company ID")),
                    ft.DataColumn(ft.Text("Board ID")),
                    ft.DataColumn(ft.Text("Public Key"))
                ],
                rows=cw_table_rows
            )
            # Internal Company Setup
            ticket_private = ft.TextField(label="Private Key", hint_text="ex. https://ntfy.myserver.com/report")
            ticket_public = ft.TextField(label="Public Key", hint_text="ex. https://ntfy.myserver.com/monitor")
            ticket_clientid = ft.TextField(label="Client ID", hint_text="ex. https://ntfy.myserver.com/monitor")
            ticket_company = ft.TextField(label="Company Name", hint_text="ex. https://ntfy.myserver.com/monitor")
            ticket_domain = ft.TextField(label="Domain", hint_text="ex. https://ntfy.myserver.com/monitor")
            # Ticket Setup
            ticket_boardid = ft.TextField(label="Board ID", hint_text="ex. https://ntfy.myserver.com/monitor")
            ticket_clientnumber = ft.TextField(label="Client Number", hint_text="ex. https://ntfy.myserver.com/monitor")

            ticket_setup_row = ft.ResponsiveRow([
                ft.Container(ticket_private, col={"sm": 3, "md": 4, "xl":4}, padding=5),
                ft.Container(ticket_public, col={"sm": 3, "md": 4, "xl":4}, padding=5),
                ft.Container(ticket_clientid, col={"sm": 3, "md": 4, "xl":4}, padding=5),
                ft.Container(ticket_company, col={"sm": 3, "md": 4, "xl":4}, padding=5),
                ft.Container(ticket_domain, col={"sm": 3, "md": 4, "xl":4}, padding=5),
            ])
            client_setup_row = ft.ResponsiveRow([
                ft.Container(ticket_boardid, col={"sm": 3, "md": 4, "xl":4}, padding=5),
                ft.Container(ticket_clientnumber, col={"sm": 3, "md": 4, "xl":4}, padding=5),
            ])
            ticket_info = ft.Text("Fill in info about your connectwise instance below")
            client_info = ft.Text("Fill in info about your connectwise client below. Board to put tickets on, client to put tickets under")
            ticket_text = Text("""
            This is where you can setup ticketing. Currently only Connectwise Ticketing is integrated with options to inegrate with the APIs they offer. It requires a valid Company, Public key, Private Key, and domain. In addition you also need a valid clientid from connectwise directly. That must be requested from them. It's a pain honestly. Read their docs for more information.
            """)
            ticket_row = Row(alignment=ft.MainAxisAlignment.CENTER, wrap=True, controls=[ticket_text])
            # current_monitor_url, current_report_url = get_ntfy_urls()
            # current_monitor = ft.Text(f'The monitor URL is set to: {current_monitor_url}', style=ft.TextThemeStyle.BODY_MEDIUM, size=32)
            # current_report = ft.Text(f'The Report URL is set to: {current_report_url}', style=ft.TextThemeStyle.BODY_MEDIUM, size=32)
            # ntfy_sep = ft.Card(content=ft.Container(Text("Current ntfy server Settings", weight="bold", style=ft.TextThemeStyle.BODY_MEDIUM, size=25), padding=8, expand=True))
            page.views.append(
                View(
                    "/ntfysettings",
                    [
                        AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], ),
                        ticket_row,
                        ticket_info,
                        ticket_setup_row,
                        client_info,
                        client_setup_row,
                        Row([ft.ElevatedButton(text="Test", on_click=lambda x: test_cw(page, ticket_company.value, ticket_public.value, ticket_private.value, ticket_domain.value, ticket_clientid.value, ticket_boardid.value, ticket_clientnumber.value))]),
                        ft.Text("Current Ticketing Settings", weight="bold", style=ft.TextThemeStyle.BODY_MEDIUM, size=18),
                        cw_table
                    ]
                    ,
                )
            )
        if page.route == "/ntfytest":
            page.views.append(
                View(
                    "/ntfytest",
                    [
                    AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue", actions=[theme_icon_button], ),
                    Text("Did your servers get the test messages? If so, click save! Otherwise cancel.", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                    Row([ft.ElevatedButton(text="Save", on_click=lambda x: adjust_ntfy_urls()), ft.ElevatedButton(text="Go Home", on_click=go_home)])

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
            status_scanner_true = Text("""
            Thanks for enabling the IP scanner! We'll start checking your IP for any changes and alert you when we see something.
            Have a great day!
            """)
            status_scanner_false = Text("""
            The IP Scanner has now been disabled. You will no longer receive alerts when the static public IP address has changed.
            """)
            current_status = get_ip_scan_status()
            if current_status == 'Enabled':
                status_scanner_text = status_scanner_true
            else: status_scanner_text = status_scanner_false

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
        if page.route == "/wfc" or page.route == "/wfc":
            def close_banner(e):
                page.banner.open = False
                page.update()

            page.banner = ft.Banner(
                bgcolor=ft.colors.AMBER_100,
                leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
                content=ft.Text(
                    "Welcome to the windows file checker!"
                ),
                actions=[
                    ft.TextButton("Close", on_click=close_banner)
                ],
            )

            wfc_configs = load_wfc_configs(config_location)
            wfc_table_rows = []

            for wfc_config in wfc_configs:
                windows_name = wfc_config['windows_name']
                windows_domain = wfc_config['windows_domain']
                windows_user = wfc_config['windows_user']
                windows_pass = wfc_config['windows_pass']
                windows_file_path = wfc_config['windows_file_path']
                windows_cron = wfc_config['windows_cron']
                windows_check_frequency = wfc_config['windows_check_frequency']

                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(windows_name)),
                        ft.DataCell(ft.Text(windows_domain)),
                        ft.DataCell(ft.Text(windows_user)),
                        ft.DataCell(ft.Text(windows_file_path)),
                        ft.DataCell(ft.Text(windows_cron)),
                        ft.DataCell(ft.Text(windows_check_frequency))
                    ],
                    # Add any necessary on_select_changed or other event handlers here
                    on_select_changed=(
                        lambda user_modules_copy: 
                            lambda x: user_modules_copy.delete_wfc_config()
                    )(user_modules)
                )

                wfc_table_rows.append(row)

            wfc_table = ft.DataTable(
                # Add desired styling options here
                columns=[
                    ft.DataColumn(ft.Text("Windows Name")),
                    ft.DataColumn(ft.Text("Windows Domain")),
                    ft.DataColumn(ft.Text("Windows User")),
                    ft.DataColumn(ft.Text("Windows File Path")),
                    ft.DataColumn(ft.Text("Windows Cron")),
                    ft.DataColumn(ft.Text("Windows Check Frequency")),
                ],
                rows=wfc_table_rows
            )

            def show_banner_click(e):
                page.banner.open = True
                page.update()
            windows_name = ft.TextField(label="Name of system to monitor", hint_text="ex. WINDOWS-01")
            windows_domain = ft.TextField(label="Domain Name", hint_text="ex. MYDOMAIN.LOCAL")
            windows_user = ft.TextField(label="Username to login with", hint_text="ex. username")
            windows_pass = ft.TextField(label="Password to login with", hint_text="ex. Password!", password=True, can_reveal_password=True)
            windows_file_path = ft.TextField(label="Path of Folder to Monitor", hint_text="ex. \\\\TEST-DC01\\testfolder")
            windows_cron = ft.TextField(label="How Often should the check job run? (In cron)", hint_text="0 0 * * *")
            windows_check_frequency = ft.TextField(label="Freqency of update to folder (In hours)", hint_text="24")
            submit_button = ft.ElevatedButton(text="Submit", on_click=lambda e: set_and_run_wfc(user_modules, e))

            def set_and_run_wfc(user_modules, event):
                user_modules.windows_name = windows_name.value
                user_modules.windows_domain = windows_domain.value
                user_modules.windows_user = windows_user.value
                user_modules.windows_pass = windows_pass.value
                user_modules.windows_file_path = windows_file_path.value
                user_modules.windows_cron = windows_cron.value
                user_modules.windows_check_frequency = windows_check_frequency.value

                wfc_config = {
                    'windows_name': windows_name.value,
                    'windows_domain': windows_domain.value,
                    'windows_user': windows_user.value,
                    'windows_pass': cipher_suite.encrypt(windows_pass.value.encode("utf-8")),  # Encrypt the password
                    'windows_file_path': windows_file_path.value,
                    'windows_cron': windows_cron.value,
                    'windows_check_frequency': windows_check_frequency.value,
                }

                save_wfc_config(config_location, wfc_config)

                user_modules.setup_wfc()

                user_modules.show_info_snackbar("Windows File Checker has been scheduled and setup!")
                user_modules.page.update()

            wfc_help = ft.ElevatedButton("Help", on_click=show_banner_click)
            wfc_view = ft.View("/wfc", 
                [
                        AppBar(title=Text("Cecil - Alerting and Monitoring", color="white"), center_title=True, bgcolor="blue",
                        actions=[theme_icon_button], ),
                    wfc_help,
                    Text('Setup a new monitor on a windows system below - Results will appear here after scans kick off'),
                    windows_name,
                    windows_domain, 
                    windows_user,
                    windows_pass,
                    windows_file_path,
                    windows_cron,
                    windows_check_frequency,
                    submit_button,
                    Text('Existing Windows File Checker Scans:', weight="bold", style=ft.TextThemeStyle.BODY_MEDIUM, size=18),
                    wfc_table
                    ]
            )
            wfc_view.scroll = ft.ScrollMode.AUTO
            page.views.append(
                wfc_view
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

    def local_login(e):
        if local_user_var == username:
            if local_pass_var == password:
                cecil_row.visible = False
                login_row.visible = False
                logout_row.visible = True
                basic_row.visible = True
                basic_modules_row.visible = True
                alert_row.visible = True
                alert_modules_row.visible = True
                monitor_row.visible = True
                report_modules_row.visible = True
                local_row.visible = False
                local_submit.visible = False
                page.update()


    def login_values(local_user, local_pass):
        global local_user_var
        global local_pass_var
        local_user_var = local_user
        local_pass_var = local_pass

    login_user_var = None
    login_pass_var = None


    def reveal_local(e):
        local_row.visible = True
        page.update()


    page.on_login = on_login
    local_login_button = ft.ElevatedButton(text='Login Locally', on_click=reveal_local)
    local_text = ft.Text('Login Locally:')
    login_user = ft.TextField(label="Username", hint_text="ex. admin")
    login_pass = ft.TextField(label="Password", can_reveal_password=True, password=True, hint_text="ex. password1")

    local_submit = ft.TextButton(text='Submit', on_click=lambda e: (login_values(login_user.value, login_pass.value), local_login(e)))
    local_row = ft.Row(controls=[local_text, login_user, login_pass, local_submit])
    local_row.visible = False
    logout_button = ft.ElevatedButton("Logout", on_click=logout_button_click)
    
    login_button = ft.ElevatedButton("Login with GitHub", on_click=login_click)
    login_button_row = ft.Row(controls=[login_button, local_login_button])
    login_row = Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[login_button_row, banner_button])
    logout_row = Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[logout_button, banner_button])
    page.add(login_row, logout_row, local_row)


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
    ticket_config_button = ElevatedButton("Ticketing Setup", on_click=open_ticketing)
    windows_file_check_button = ElevatedButton("Windows File Checker", on_click=open_wfc)

    basic_modules_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ntfy_config_button, ticket_config_button])
    alert_modules_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[docker_monitor_button, Dynamic_ip_button, windows_file_check_button])
    report_modules_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[dell_button, linux_health_button])


    toggle_login_session()
    page.add(cecil_row, basic_row, basic_modules_row, alert_row, alert_modules_row, monitor_row, report_modules_row)

# Browser Version
ft.app(target=main, view=ft.WEB_BROWSER, port=38355)
# ft.app(target=main)
# App Version
# ft.app(target=main, port=8035)