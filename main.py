import os
import xml.etree.ElementTree as et

print("@nayol")

modes = {
    1: "exclude all unused script files (unregistered)",
    2: "actions",
    3: "creaturescripts",
    4: "globalevents",
    5: "monster",
    6: "spells",
    7: "talkactions",
    8: "weapons"
}

unusedScriptsCount = 0

def Populate():
    ret = []
    for index, key in modes.items():
        ret.append(f">> [{index}] = {key}")
    
    ret = "\n".join(ret)
    return ret

def getSelectedMode(n):
    if (n > len(modes)):
        return ""
    
    if (n == 1):
        return "all"
    
    for index, key in modes.items():
        if (index == n):
            return key
    
def getFolders():
    if (selectedMode == ""):
        return True
    
    folders = []

    if (selectedMode == "all"):
        folders.append(os.path.join(os.getcwd(), "data\\actions"))
        folders.append(os.path.join(os.getcwd(), "data\\creaturescripts"))
        folders.append(os.path.join(os.getcwd(), "data\\globalevents"))
        folders.append(os.path.join(os.getcwd(), "data\\monster"))
        folders.append(os.path.join(os.getcwd(), "data\\spells"))
        folders.append(os.path.join(os.getcwd(), "data\\talkactions"))
        folders.append(os.path.join(os.getcwd(), "data\\weapons"))
    else:
        folders.append(os.path.join(os.getcwd(), f"data\\{selectedMode}"))   

    return folders

def cleanFolder(folder):
    usingScripts = set()
    print(f"> Loading {os.path.basename(folder)} xml file...")
    xmlPath = f"{folder}\\{os.path.basename(folder)}.xml"
    if ("monster" in folder):
        xmlPath = f"{folder}\\{os.path.basename(folder)}s.xml"
    xml = et.parse(xmlPath)
    xmlRoot = xml.getroot()
    basename = xmlRoot.iter()

    for e in basename:
        if ("script" in e.attrib):
            usingScripts.add(e.get("script"))
        if ("file" in e.attrib):
            usingScripts.add(e.get("file"))

    print("> Done.")
    def verifyFolder(folder):
        global unusedScriptsCount
        for file in os.listdir(folder):
            if (not os.path.isdir(f"{folder}\\{file}") and not f"scripts/{file}" in usingScripts):
                print(f"!> Found {file}, working...")
                os.remove(f"{folder}\\{file}")
                unusedScriptsCount += 1
                print(f"!> Done.")
    
    def verifyMonstersFolder(folder):
        global unusedScriptsCount
        for file in os.listdir(folder):
            if (not os.path.isdir(f"{folder}\\{file}") and not f"monsters/{file}" in usingScripts):
                print(f"!> Found {file}, working...")
                os.remove(f"{folder}\\{file}")
                unusedScriptsCount += 1
                print(f"!> Done.")

    if ("monster" in folder):
        verifyMonstersFolder(folder + "\\monsters")
    else:
        verifyFolder(folder + "\\scripts")

    print(f">> Done. {unusedScriptsCount} unused scripts were excluded from otserver.")
    



userSelectedMode = input(f"\nSelect mode: \n{Populate()}\nTap a key: ")
if (not userSelectedMode.isdigit() or int(userSelectedMode) > len(modes)):
    raise ValueError("Invalid mode.")

userSelectedMode = int(userSelectedMode)
selectedMode = getSelectedMode(userSelectedMode)
for e in getFolders():
    cleanFolder(e)