import argostranslate.package
import os

os.system("py -m ensurepip --upgrade")
os.system("py -m pip install --upgrade pip")
# os.system("pip install -r requirements.txt")
os.system("pip install argostranslate")
os.system("pip install customtkinter")

# Download and install all Argos Translate package
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()

print("Starting Download of Argostranslate Packages")

for i in range(len(available_packages)):
    argostranslate.package.install_from_path(available_packages[i].download())
    print("Installed: "+available_packages[i].from_code+"->"+available_packages[i].to_code)


print("Finished")