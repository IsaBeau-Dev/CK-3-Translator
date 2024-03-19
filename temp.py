import argostranslate.translate as at
import argostranslate.package


from_code = "en"
to_code = "de"

# Download and install Argos Translate package
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()

for i in range(len(available_packages)):
    argostranslate.package.install_from_path(available_packages[i].download())
    print("Installed: "+available_packages[i].from_code+"->"+available_packages[i].to_code)


s = at.translate("Hello there you dumb shit, I am sitting here looking at you",from_code="en",to_code="de")
print(s)