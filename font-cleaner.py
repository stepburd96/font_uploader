import fontforge, re, os

desktopPath = "/Users/stephenburden/Desktop"; # to change to user's path

pathRel = str(input("Input relative path to virgin folder in /fonts: "))
ignore = str(input("Input string to ignore in final font names: ")) # latinotype - mangueira font for Affirm ticket https://movableink.zendesk.com/agent/tickets/176310 whose font names included latinotype but that shouldn't show in the human readable version

path = desktopPath + "/fonts/" + pathRel + "/"
processedDirPath = desktopPath + "/processed-fonts/" + pathRel
ext = ("otf", "ttf");

failedFiles = []
failedFilesLog = []
cleanedFontsLog = []
cleanedFonts = []
cleanedFontsLog = []
#badExtension = []

### Functions

def fontCleaning(file) : # Assumes font has passed validation

    try :
        font = fontforge.open(path + file)

        sfnt_names = font.sfnt_names;
        for name in sfnt_names :
            font.appendSFNTName(name[0], name[1], '')
        # Replace font name, family name, and full name with only alpha numberic characters
        font.fontname = re.sub("[^a-zA-Z0-9]", "", font.fontname)
        font.familyname = re.sub("[^a-zA-Z0-9]", "", font.familyname)
        font.fullname = re.sub("[^a-zA-Z0-9]", "", font.fullname)

        # Remove sfntRevision, version, and weight
        font.sfntRevision = None;
        font.weight = ""
        font.version = ""

        
        
        # Font File Name Clean
        fontFileName = re.sub("[^a-zA-Z0-9.]", "", file)
        fontFileName = re.sub(f"{ignore}", "", fontFileName)
        
        #Output gathering
        cleanedFonts.append(fontFileName)
        cleanedFontsLog.append([("fontname",font.fontname), ("familyname", font.familyname), ("fullname",font.fullname), ("sfntRevision",font.sfntRevision), ("weight", font.weight), ("version",font.version) ]) #append a list so the final log will be a nested list
        
        # Save the font to local directory - fontFileName does not have to be file 
        font.generate(processedDirPath + "/" + fontFileName);
    except OSError :
        failedFilesLog.append([file, str(OSError)])
        failedFiles.append(file)

def outputPod (list, type) :
    if type == "failed" :
        if list[0][0] == '.DS_Store' :
            list.pop(0)
        if len(failedFiles) > 0 :   
            for x in range(len(failedFiles)-1) :
                print(f'>{list[x][0]}')
    elif type == "clean" :
        for font in list :
            print(f">> {list.index(font)+1}")
            print(f'>> {font[0][1]} :')
            for spec in range(len(font)) :
                print(f">> |- {font[spec][0].title()} > {font[spec][1]}")
            print(f">>")

def userExperience() :
    print(" ")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # print(f">> Directory: {os.listdir(path)}, {len(os.listdir(path))}")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(f">> Cleaned Fonts Log --- {len(cleanedFonts)} ")
    print(outputPod(cleanedFontsLog, 'clean'))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(" ")
    if len(failedFilesLog) > 0 :
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(f">> Failed Files Log --- {len(failedFiles)}")
        print(outputPod(failedFilesLog, 'failed'))
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(" ")

### Script Body
if not os.path.exists(processedDirPath) :
    os.mkdir(desktopPath + "/processed-fonts/" + pathRel)

for file in os.listdir(path) :
    print(f">> File from OS --- {file}")
    fontCleaning(file)


userExperience()