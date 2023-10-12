import sys

print("  ____    _____    ____")
print(" / __ \  |  __ \  |  _ \ ")
print("| |  | | | |  | | | |_) |")
print("| |  | | | |  | | |  _ < ")
print("| |__| | | |__| | | |_) |")
print(" \____/  |_____/  |____/ ")
print("")
print("Version 0.1.3 Alpha")
print(" ")

smbios_to_secureboot = {
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

secureboot_to_smbios = {model: smbios for smbios, model in smbios_to_secureboot.items()}

secureboot_to_macos = {
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

def main():
    user_input = input("Enter the SMBIOS or SecureBootModel: ")

    if user_input in smbios_to_secureboot:
        secure_boot_model = smbios_to_secureboot[user_input]
        min_macos_version = secureboot_to_macos[user_input]
        print(f"SecureBootModel: {secure_boot_model}")
        print(f"Minimum macOS Version: {min_macos_version}")
    elif user_input in secureboot_to_smbios:
        smbios_values = secureboot_to_smbios[user_input]
        min_macos_version = secureboot_to_macos[smbios_values]
        print(f"SMBIOS values for {user_input}: {smbios_values}")
        print(f"Minimum macOS Version: {min_macos_version}")
    else:
        print(f"'{user_input}' doesn't have the T2 Chip")

if __name__ == "__main__":
    main()
