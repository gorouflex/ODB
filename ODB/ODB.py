#!/usr/bin/env python
import os, secrets, subprocess, shlex, datetime, time, sys, plistlib, tempfile, shutil, random, uuid, zipfile, json, binascii, urllib3, webbrowser
from Scripts import *
from collections import OrderedDict
if sys.version_info >= (3, 0):
    from urllib.request import urlopen
else:
    from urllib2 import urlopen
    

def get_latest_version():
    latest_version = urllib3.request(url="https://github.com/gorouflex/ODB/releases/latest", method="GET")
    latest_version = latest_version.geturl()
    return latest_version.split("/")[-1]

def check_for_updates():
    local_version = "0.1.7"
    latest_version = get_latest_version()        
    if local_version < latest_version:
        print("A new update has been found!")
        choice = input("Do you want to visit the GitHub page for more details? (Y/N)")        
        if choice.lower() == "y":
           webbrowser.open("https://github.com/gorouflex/ODB/releases/latest")
           print("Exiting...")
           clear_screen()
           sys.exit(0)
        else:
           print("Exiting...")
           time.sleep(2)
           clear_screen()
           sys.exit(0)
     
def open_github():
    webbrowser.open("https://www.github.com/gorouflex/ODB")

def open_releases():
    webbrowser.open(f"https://github.com/gorouflex/ODB/releases/tag/{get_latest_version()}")

def info():
    clear_screen()
    print_logo()
    print()
    print("About ODB")
    print("Main developer: GorouFlex")
    print(f"Latest version on Github: {get_latest_version()}")
    print()
    print("1. Open GitHub")
    print("2. Change logs")
    print("B. Back")
    
def print_logo():
    print(""" ██████╗ ██████╗ ██████╗ 
██╔═══██╗██╔══██╗██╔══██╗
██║   ██║██║  ██║██████╔╝
██║   ██║██║  ██║██╔══██╗
╚██████╔╝██████╔╝██████╔╝
 ╚═════╝ ╚═════╝ ╚═════╝ 
Version 0.1.7 Alpha - CLI Mode""")

def clear_screen():
    if os.name == 'nt':
       _ = os.system('cls')
    else:
       _ = os.system('clear')
        
class ODB:
    def __init__(self):
        self.smbios_to_secureboot = {
            "Disabled": "Unknown",
            "Default": "x86legacy",
            "j137": "iMacPro1,1",
            "j680": "MacBookPro15,1",
            "j132": "MacBookPro15,2",
            "j174": "Macmini8,1",
            "j140k": "MacBookAir8,1",
            "j780": "MacBookPro15,3",
            "j213": "MacBookPro15,4",
            "j140a": "MacBookAir8,2",
            "j152f": "MacBookPro16,1",
            "j160": "MacPro7,1",
            "j230k": "MacBookAir9,1",
            "j214k": "MacBookPro16,2",
            "j223": "MacBookPro16,3",
            "j215": "MacBookPro16,4",
            "j185": "iMac20,1",
            "j185f": "iMac20,2",
            "x86legacy": "VM",
        }

        self.secureboot_to_smbios = {model: smbios for smbios, model in self.smbios_to_secureboot.items()}

        self.secureboot_to_macos = {
            "Disabled": "N/A",
            "Default": "11.0.1 (20B29)",
            "j137": "10.13.2 (17C2111)",
            "j680": "10.13.6 (17G2112)",
            "j132": "10.13.6 (17G2112)",
            "j174": "10.14 (18A2063)",
            "j140k": "10.14.1 (18B2084)",
            "j780": "10.14.5 (18F132)",
            "j213": "10.14.5 (18F2058)",
            "j140a": "10.14.5 (18F2058)",
            "j152f": "10.15.1 (19B2093)",
            "j160": "10.15.1 (19B88)",
            "j230k": "10.15.3 (19D2064)",
            "j214k": "10.15.4 (19E2269)",
            "j223": "10.15.4 (19E2265)",
            "j215": "10.15.5 (19F96)",
            "j185": "10.15.6 (19G2005)",
            "j185f": "10.15.6 (19G2005)",
            "x86legacy": "11.0.1 (20B29)",
        }

    def print_menu(self):
        print("1. Lookup")
        print("2. Generate")
        print("3. About")
        print("")
        print("Q. Quit")

    def print_generate_submenu(self):
        print("1. Generate SMBios")
        print("2. Generate ApECID")
        print("")
        print("B. Back to the main menu")
        
    def main(self):
        s = Smbios(self)
        while True:
            clear_screen()
            print_logo()
            self.print_menu()

            choice = input("Option: ")

            if choice == '1':
                clear_screen()
                print_logo()
                user_input = input("Enter the SMBIOS or SecureBootModel: ")
                if user_input in self.smbios_to_secureboot:
                    secure_boot_model = self.smbios_to_secureboot[user_input]
                    min_macos_version = self.secureboot_to_macos[user_input]
                    print(f"SMBios: {secure_boot_model}")
                    print(f"Minimum macOS Version: {min_macos_version}")
                elif user_input in self.secureboot_to_smbios:
                    smbios_values = self.secureboot_to_smbios[user_input]
                    min_macos_version = self.secureboot_to_macos[smbios_values]
                    print(f"SecureBootModel for {user_input}: {smbios_values}")
                    print(f"Minimum macOS Version: {min_macos_version}")
                else:
                    print(f"'{user_input}' doesn't have the T2 Chip")
                input("Press Enter to continue...")

            elif choice == '2':
                while True:
                    clear_screen()
                    print_logo()
                    self.print_generate_submenu()
                    choice = input("Option: ")

                    if choice == '1':
                        clear_screen()
                        print_logo()                        
                        s.main()
                    elif choice == '2':
                        clear_screen()
                        print_logo()
                        print("Generated ApECID: ")
                        print(secrets.randbits(64))
                        input("Press Enter to continue...")

                    elif choice.lower() == 'b':
                        break
            elif choice == '3' :
                while True:
                   info()
                   choice = input("Option: ")
                   if choice == '1':
                       open_github()
                   elif choice == '2':
                        open_releases()
                   elif choice.lower() == 'b':
                       break

            elif choice.lower() == 'q':
                print("Exiting...")
                time.sleep(2)
                clear_screen()
                sys.exit(0)

class Smbios:
    def __init__(self,odb_instance):
        self.odb = odb_instance
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        self.u = utils.Utils("GenSMBIOS")
        self.d = downloader.Downloader()
        self.r = run.Run()
        self.opencorpgk_url = "https://api.github.com/repos/acidanthera/OpenCorePkg/releases"
        self.scripts = "Scripts"
        self.plist = None
        self.plist_data = None
        self.plist_type = "Unknown"
        self.remote = self._get_remote_version()
        self.okay_keys = [
            "SerialNumber",
            "BoardSerialNumber",
            "SmUUID",
            "ProductName",
            "Trust",
            "Memory"
        ]
        try: self.rom_prefixes = json.load(open(os.path.join(self.scripts,"prefix.json")))
        except: self.rom_prefixes = []
        self.gen_rom = True        

    def _get_macserial_version(self):
        try:
            urlsource = json.loads(self.d.get_string(self.opencorpgk_url,False))
            macserial_h_url = "https://raw.githubusercontent.com/acidanthera/OpenCorePkg/{}/Utilities/macserial/macserial.h".format(urlsource[0]["target_commitish"])
            macserial_h = self.d.get_string(macserial_h_url,False)
            macserial_v = macserial_h.split('#define PROGRAM_VERSION "')[1].split('"')[0]
        except: return None
        return macserial_v

    def _get_macserial_url(self):
        try:
            urlsource = json.loads(self.d.get_string(self.opencorpgk_url,False))
            return next((x.get("browser_download_url",None) for x in urlsource[0].get("assets",[]) if "RELEASE.zip" in x.get("name","")),None)
        except: pass
        return None

    def _get_binary(self,binary_name=None):
        if not binary_name:
            binary_name = ["macserial.exe","macserial32.exe"] if os.name == "nt" else ["macserial.linux","macserial"] if sys.platform.startswith("linux") else ["macserial"]
        cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        path = None
        for name in binary_name:
            if os.path.exists(name):
                path = os.path.join(os.getcwd(), name)
            elif os.path.exists(os.path.join(os.getcwd(), self.scripts, name)):
                path = os.path.join(os.getcwd(),self.scripts,name)
            if path: break
        os.chdir(cwd)
        return path

    def _get_version(self,macserial):
        out, error, code = self.r.run({"args":[macserial]})
        if not len(out):
            return None
        for line in out.split("\n"):
            if not line.lower().startswith("version"):
                continue
            vers = next((x for x in line.lower().strip().split() if len(x) and x[0] in "0123456789"),None)
            if not vers == None and vers[-1] == ".":
                vers = vers[:-1]
            return vers
        return None

    def _download_and_extract(self, temp, url, path_in_zip=[]):
        ztemp = tempfile.mkdtemp(dir=temp)
        zfile = os.path.basename(url)
        print("Downloading {}...".format(os.path.basename(url)))
        self.d.stream_to_file(url, os.path.join(ztemp,zfile), False)
        print(" - Extracting...")
        btemp = tempfile.mkdtemp(dir=temp)
        with zipfile.ZipFile(os.path.join(ztemp,zfile)) as z:
            z.extractall(os.path.join(temp,btemp))
        script_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),self.scripts)
        search_path = os.path.join(temp,btemp)
        if path_in_zip: search_path = os.path.join(search_path,*path_in_zip)
        for x in os.listdir(search_path):
            if "macserial" in x.lower():
                print(" - Found {}".format(x))
                if os.name != "nt":
                    print("   - Chmod +x...")
                    self.r.run({"args":["chmod","+x",os.path.join(search_path,x)]})
                print("   - Copying to {} directory...".format(self.scripts))
                if not os.path.exists(script_dir):
                    os.mkdir(script_dir)
                shutil.copy(os.path.join(search_path,x), os.path.join(script_dir,x))

    def _get_macserial(self):
        clear_screen()
        print_logo()
        print("Powered by GenSMBios")
        print("")
        print("Gathering latest macserial info...")
        url = self._get_macserial_url()
        path_in_zip = ["Utilities","macserial"]
        if not url:
            print("Error checking for updates (network issue)\n")
            self.u.grab("Press [enter] to return...")
            return
        temp = tempfile.mkdtemp()
        cwd  = os.getcwd()
        try:
            print(" - {}".format(url))
            self._download_and_extract(temp,url,path_in_zip)
        except Exception as e:
            print("We ran into some problems :(\n\n{}".format(e))
        print("\nCleaning up...")
        os.chdir(cwd)
        shutil.rmtree(temp)
        self.u.grab("\nDone.",timeout=5)
        return

    def _get_remote_version(self):
        clear_screen()
        print("Getting the latest infomation...")
        vers = self._get_macserial_version()
        if not vers:
            print("Error checking for updates (network issue)\n")
            self.u.grab("Press [enter] to return...")
            return None
        return vers

    def _get_plist(self):
        clear_screen()
        print_logo()
        print("Powered by GenSMBios")
        print("")
        print("Current: {}".format(self.plist))
        print("Type:    {}".format(self.plist_type))
        print("")
        print("C. Clear Selection")
        print("M. Main Menu")
        print("")
        p = self.u.grab("Please drag and drop the target plist:  ")
        if p.lower() == "m":
            return
        elif p.lower() == "c":
            self.plist = None
            self.plist_data = None
            return
        
        pc = self.u.check_path(p)
        if not pc:
            clear_screen()
            print_logo()
            print("Powered by GenSMBios")
            print("")
            print("Plist file not found:\n\n{}".format(p))
            print("")
            self.u.grab("Press [enter] to return...")
            return self._get_plist()
        try:
            with open(pc, "rb") as f:
                self.plist_data = plist.load(f,dict_type=OrderedDict)
        except Exception as e:
            clear_screen()
            print_logo()
            print("Powered by GenSMBios")
            print("")
            print("Plist file malformed:\n\n{}".format(e))
            print("")
            self.u.grab("Press [enter] to return...")
            return self._get_plist()
        detected_type = "OpenCore" if "PlatformInfo" in self.plist_data else "Clover" if "SMBIOS" in self.plist_data else "Unknown"
        if detected_type.lower() == "unknown":
            while True:
                clear_screen()
                print_logo()
                print("Powered by GenSMBios")
                print("")
                print("Could not auto-determine plist type!")
                print("")
                print("1. Clover")
                print("2. OpenCore")
                print("")
                print("M. Return to the Menu")
                print("")
                t = self.u.grab("Please select the target type:  ").lower()
                if t == "m": return self._get_plist()
                elif t in ("1","2"):
                    detected_type = "Clover" if t == "1" else "OpenCore"
                    break
        self.plist_type = detected_type
        if self.plist_type.lower() == "clover":
            key_check = self.plist_data.get("SMBIOS",{})
            new_smbios = {}
            removed_keys = []
            for key in key_check:
                if key not in self.okay_keys:
                    removed_keys.append(key)
                else:
                    new_smbios[key] = key_check[key]
            if "CustomUUID" in self.plist_data.get("SystemParameters",{}):
                removed_keys.append("CustomUUID")
            if len(removed_keys):
                while True:
                    clear_screen()
                    print_logo()
                    print("Powered by GenSMBios")
                    print("")
                    print("The following keys will be removed:\n\n{}\n".format(", ".join(removed_keys)))
                    con = self.u.grab("Continue? (y/n):  ")
                    if con.lower() == "y":
                        self.plist_data["SMBIOS"] = new_smbios
                        self.plist_data.get("SystemParameters",{}).pop("CustomUUID", None)
                        break
                    elif con.lower() == "n":
                        self.plist_data = None
                        return
        self.plist = pc

    def _get_rom(self):
        rom_str = random.choice(self.rom_prefixes) if self.rom_prefixes else ""
        while len(rom_str) < 12: rom_str += random.choice("0123456789ABCDEF")
        return rom_str

    def _get_smbios(self, macserial, smbios_type, times=1):
        total = []
        while len(total) < times:
            total_len = len(total)
            smbios, err, code = self.r.run({"args":[macserial,"-a"]})
            if code != 0:
                return None
            for line in smbios.split("\n"):
                line = line.strip()
                if line.lower().startswith(smbios_type.lower()):
                    total.append(line)
                    if len(total) >= times:
                        break
            if total_len == len(total):
                return False
        output = []
        for sm in total:
            s_list = [x.strip() for x in sm.split("|")]
            s_list.append(str(uuid.uuid4()).upper())
            s_list.append(self._get_rom())
            output.append(s_list)
        return output

    def _generate_smbios(self, macserial):
        if not macserial or not os.path.exists(macserial):
            self._get_macserial()
            macserial = self._get_binary()
            if not macserial or not os.path.exists(macserial):
                clear_screen()
                print_logo()
                print("Powered by GenSMBios")
                print("")
                print("MacSerial binary was not found and failed to download.")
                print("")
                self.u.grab("Press [enter] to return...")
                return
        clear_screen()
        print_logo()
        print("Powered by GenSMBios")
        print("")
        print("M. Main Menu")
        print("")
        print("Please type the SMBIOS to gen and the number")
        menu = self.u.grab("of times to generate [max 20] (i.e. iMac18,3 5):  ")
        if menu.lower() == "m":
            return
        menu = menu.split(" ")
        if len(menu) == 1:
            smtype = menu[0]
            times  = 1
        else:
            smtype = menu[0]
            try:
                times  = int(menu[1])
            except:
                clear_screen()
                print_logo()
                print("Powered by GenSMBios")
                print("")
                print("Incorrect format - must be SMBIOS times - i.e. iMac18,3 5")
                print("")
                self.u.grab("Press [enter] to return...")
                self._generate_smbios(macserial)
                return
        if times < 1:
            times = 1
        if times > 20:
            times = 20
        smbios = self._get_smbios(macserial,smtype,times)
        if smbios == None:
            print("Error - macserial returned an error!")
            self.u.grab("Press [enter] to return...")
            return
        if smbios == False:
            print("\nError - {} not generated by macserial\n".format(smtype))
            self.u.grab("Press [enter] to return...")
            return
        self.u.head("{} SMBIOS Info".format(smbios[0][0]))
        print("")
        f_string = "Type:         {}\nSerial:       {}\nBoard Serial: {}\nSmUUID:       {}"
        if self.gen_rom: f_string += "\nApple ROM:    {}" if self.rom_prefixes else "\nRandom ROM:   {}"
        print("\n\n".join([f_string.format(*x) for x in smbios]))
        if self.plist_data and self.plist and os.path.exists(self.plist):
            if len(smbios) > 1:
                print("\nFlushing first SMBIOS entry to {}".format(self.plist))
            else:
                print("\nFlushing SMBIOS entry to {}".format(self.plist))
            if self.plist_type.lower() == "clover":
                for x in ["SMBIOS","RtVariables","SystemParameters"]:
                    if not x in self.plist_data:
                        self.plist_data[x] = {}
                self.plist_data["SMBIOS"]["ProductName"] = smbios[0][0]
                self.plist_data["SMBIOS"]["SerialNumber"] = smbios[0][1]
                self.plist_data["SMBIOS"]["BoardSerialNumber"] = smbios[0][2]
                self.plist_data["RtVariables"]["MLB"] = smbios[0][2]
                self.plist_data["SMBIOS"]["SmUUID"] = smbios[0][3]
                if self.gen_rom:
                    self.plist_data["RtVariables"]["ROM"] = plist.wrap_data(binascii.unhexlify(smbios[0][4].encode("utf-8")))
                self.plist_data["SystemParameters"]["InjectSystemID"] = True
            elif self.plist_type.lower() == "opencore":
                if not "PlatformInfo" in self.plist_data: self.plist_data["PlatformInfo"] = {}
                if not "Generic" in self.plist_data["PlatformInfo"]: self.plist_data["PlatformInfo"]["Generic"] = {}
                self.plist_data["PlatformInfo"]["Generic"]["SystemProductName"] = smbios[0][0]
                self.plist_data["PlatformInfo"]["Generic"]["SystemSerialNumber"] = smbios[0][1]
                self.plist_data["PlatformInfo"]["Generic"]["MLB"] = smbios[0][2]
                self.plist_data["PlatformInfo"]["Generic"]["SystemUUID"] = smbios[0][3]
                if self.gen_rom:
                    self.plist_data["PlatformInfo"]["Generic"]["ROM"] = plist.wrap_data(binascii.unhexlify(smbios[0][4].encode("utf-8")))
            with open(self.plist, "wb") as f:
                plist.dump(self.plist_data, f, sort_keys=False)
        print("")
        self.u.grab("Press [enter] to return...")

    def _list_current(self, macserial):
        if not macserial or not os.path.exists(macserial):
            clear_screen()
            print_logo()
            print("Powered by GenSMBios")
            print("")
            print("MacSerial binary not found.")
            print("")
            self.u.grab("Press [enter] to return...")
            return
        out, err, code = self.r.run({"args":[macserial]})
        out = "\n".join([x for x in out.split("\n") if not x.lower().startswith("version") and len(x)])
        clear_screen()
        print_logo()
        print("Powered by GenSMBios")
        print("")
        print(out)
        print("")
        self.u.grab("Press [enter] to return...")

    def main(self):
      while True:
        clear_screen()
        print_logo()
        print("Powered by GenSMBios")
        print("")
        macserial = self._get_binary()
        if macserial:
            macserial_v = self._get_version(macserial)
            print("MacSerial v{}".format(macserial_v))
        else:
            macserial_v = "0.0.0"
            print("MacSerial not found!")
        if self.remote and self.u.compare_versions(macserial_v, self.remote):
            print("Remote Version v{}".format(self.remote))
        print("Current plist: {}".format(self.plist))
        print("Plist type:    {}".format(self.plist_type))
        print("")
        print("1. Install/Update MacSerial")
        print("2. Select config.plist")
        print("3. Generate SMBIOS")
        print("4. Generate UUID")
        print("5. Generate ROM")
        print("6. List Current SMBIOS")
        print("7. Generate ROM With SMBIOS (Currently {})".format("Enabled" if self.gen_rom else "Disabled"))
        print("")
        print("Q. Quit")
        print("")
        menu = self.u.grab("Please select an option:  ").lower()
        if not len(menu):
            continue
        if menu == "q":
            return
        elif menu == "1":
            self._get_macserial()
        elif menu == "2":
            self._get_plist()
        elif menu == "3":
            self._generate_smbios(macserial)
        elif menu == "4":
            clear_screen()
            print_logo()
            print("Powered by GenSMBios")
            print("")
            print(str(uuid.uuid4()).upper())
            print("")
            self.u.grab("Press [enter] to return...")
        elif menu == "5":
            clear_screen()
            print_logo()
            print("Powered by GenSMBios")
            print("")
            print("{} ROM: {}".format("Apple" if self.rom_prefixes else "Random", self._get_rom()))
            print("")
            self.u.grab("Press [enter] to return...")
        elif menu == "6":
            self._list_current(macserial)
        elif menu == "7":
            self.gen_rom = not self.gen_rom
            
if __name__ == "__main__":
    check_for_updates()
    odb = ODB()
    odb.main()
