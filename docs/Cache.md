The cache is the folder where your subscriptions, the log and the information for the html page is store. It generate during the first utilisation of the command.

### Contents

- [Path](#path)
- [Tree](#Tree)
- [Data](#data)
- [Sub.swy](#sub.swy)
- [Log](#log)


## Path
This folder are create in 
- Windows: ` C:\Users\<name>\.youtube_sm\. `
- Linux/MacOS: `/home/<name>/.cache/youtube_sm/.`

## Tree
```
.
├── data
│   ├── html
│   │   ├── 0
│   │   │   └── 20180605
│   │   │       ├── 195031
│   │   │       └── 200505
│   │   ├── 1
│   │   └── 2
│   └── json
│       ├── 0
│       │   └── 20180605
│       │       ├── 195031
│       │       └── 200505
│       ├── 1
│       └── 2
├── log
└── sub.swy
```

## Data
Data is a folder which is create when you run youtube-sm with the mode html. It serves to store the informations of the html page before the sorting of the videos.

In this folder 3 folders could be create `0/`, `1/` and `2/`. 0 is for the RSS method, 1 is for the options `--html` and 2 is for the options `--ultra-html`. The program could create 3 differents folders because the date wich are retrieve by the RSS method or the HTML method have not the same accuracy. The RSS method could retrieve date with a accuracy to the second and the HTML method retrieve date like this `1 year ago`, `2 weeks ago` so to not create some problems the 3 methods are secluded.

## Sub.swy
`sub.swy` is a list of yours subscriptions. It create with the options `--init`.

This file looks like this :
```
[v][2.0] # The version of the file
[site][youtube] # the platform of the next ids
id	channel
id	channel
[site][daylimotion] # the platform of the next ids
id	channel
id	channel
```

## Log
The log contains the script's time of execution.