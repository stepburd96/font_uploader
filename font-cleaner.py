import fontforge, re, os, json


desktopPath = "/Users/stephenburden/Desktop"; # to change to user's path
processedDirPath = desktopPath + "/processed-fonts/" + pathRel
ext = ("otf", "ttf");

failedFiles = []
failedFilesLog = []
cleanedFontsLog = []
cleanedFonts = []
cleanedFontsLog = []
#badExtension = []

### Functions

def fontCleaning(file, testing) : # Assumes font has passed validation
    try :
        font = fontforge.open(path + file)
        
        file_extension = (os.path.splitext(file))[1]
        # file_extension = split_tup[1]
        
        if file_extension not in ext :
            failedFiles.append(file)
            failedFilesLog.append([file, 'Bad File Type'])

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
         
        if testing == True :
            return #dont generate a font file if in testing mode
        
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
        


# still need to establish the ignore str

def setup() :
    f = open('./font-cleaner-config.json')
    data = json.load(f)
    return data
    
    

def cleanLoop(dir='./test-fonts') : 
    path = os.listdir(dir)
    if not os.path.exists(processedDirPath) & dir != './test-fonts' :
        os.mkdir(desktopPath + "/processed-fonts/" + pathRel)
    for file in os.listdir(path) :
        print(f">> File from OS --- {file}")
        fontCleaning(file)

setup = setup()

if setup.testing.mode == "off" :
    for file in os.listdir(path) :
        fontCleaning(file)
else : 
    print('foo')
cleanLoop(dir)
userExperience()

# Current idea is to run all the setup questions and then pass the font cleaning loop a test file if specified otherwise run the files in the dir specified by the user