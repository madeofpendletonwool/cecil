import datetime
from datetime import datetime, timedelta



windows_name = '3RTFS01'
windows_domain = '3RTNETWORKS.COM'
windows_user = 'cpendleton'
windows_pass = '6ybuKu58UqNkGf'
windows_file_path = '/CollinFiles'
# windows_cron = ft.TextField(label="How Often should the check job run? (In cron)", hint_text="0 0 * * *")
windows_check_frequency = '24'


page = '1'


class Module_Change:
    def __init__(self, page, windows_name=None, windows_domain=None, windows_user=None, windows_pass=None, windows_file_path=None, windows_cron=None, windows_check_frequency=None):
        # Windows File Checker Vars
        self.windows_name = windows_name
        self.windows_domain = windows_domain
        self.windows_user = windows_user
        self.windows_pass = windows_pass
        self.windows_file_path = windows_file_path
        self.windows_cron = windows_cron
        self.windows_check_frequency = windows_check_frequency

    def setup_wfc(self):
        from smb.SMBConnection import SMBConnection
        import os

        def authenticate_windows_machine(username, password, domain, server_name):
            print(f"username: {username}")  # Add this print statement
            print(f"password: {password}")  # Add this print statement
            print(f"domain: {domain}")      # Add this print statement
            print(f"server_name: {server_name}")  # Add this print statement
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

        def list_files_in_share(conn, share_name, path):
            try:
                files = conn.listPath(share_name, path)
                print(f"Files in '{share_name}{path}':")
                for file_info in files:
                    print(file_info.filename)
            except Exception as e:
                print(f"Error while listing files in share: {e}")

        conn = authenticate_windows_machine(self.windows_user, self.windows_pass, self.windows_domain, self.windows_name)

        if conn is None:
            print("Cannot perform the file check due to authentication failure")
            return

        # Check if any new files have been created in the specified folder within the last specified hours
        try:
            shares = conn.listShares()
            print("Available shares:")
            for share in shares:
                print(f"Share name: {share.name}")
        except Exception as e:
            print(f"Error while listing shares: {e}")

        # Specify the share_name and path
        share_name = "CollinFiles"
        path = "/"

        # List files in the share
        list_files_in_share(conn, share_name, path)




user_modules = Module_Change(page)
user_modules.windows_name = windows_name
user_modules.windows_domain = windows_domain
user_modules.windows_user = windows_user
user_modules.windows_pass = windows_pass
user_modules.windows_file_path = windows_file_path
user_modules.windows_check_frequency = windows_check_frequency

user_modules.setup_wfc()