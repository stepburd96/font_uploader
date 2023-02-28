# font_uploader

- Project Tracker: [link](https://www.notion.so/movableinkepd/Project-Dashboard-7dc19be25adb4ff1b32c4ad77d7f0ea4?p=9277cbe1300f4f128d4857f8b18ca101&pm=s)

## Setup

Have I successfully annoyed you into using this script just to get me to shut up? Follow these steps to setup the font cleaning script(s).

*Prerequisites*
  - Directories named `fonts` and `processed-fonts` on your Desktop

1. Clone the repo
1. Change the following:
  - `Line 3` - Change the name of the root directory
  - `Lines 8 & 9` - This depends on how you organize your font folders. I recommend creating a directory per client. In that directory you can place the 'unclean' font files. 
    - Example directory layout:
      - ```
        > fonts
            > elastic
                > Montserrat
                > Open Sans
            > plume
                > Work Sans
        > processed-fonts
        ```
  - `Line 9`- named `processed-fonts` on the analogy of a factory line. The same lil bundle of data getting punted around between big mean bully Files.py bois.