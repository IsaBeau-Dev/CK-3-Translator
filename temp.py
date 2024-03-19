import argostranslate.package


# Download and install all Argos Translate package
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()

for i in range(len(available_packages)):
    argostranslate.package.install_from_path(available_packages[i].download())
    print("Installed: "+available_packages[i].from_code+"->"+available_packages[i].to_code)


print("Finished")