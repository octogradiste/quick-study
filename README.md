# QuickStudy

A gnome shell extension to quickly open files, urls and apps for your courses.

## Installation
To install the extension you need to clone this repository and run the `instal.sh` script.
If you don't have a config file yet, and you study at EPFL you can ask the script to generate one for you.
Just answer that you don't have a config file yet, and that you study at EPFL. Then follow the instructions.

## Features
- Menu to quickly open files, urls and apps for your courses.
- Automatically opens the correct submenu when you have a class. (coming soon)
- Automatically open files, urls and apps when your class starts. (coming soon)
- Quickly trun on/off the automatic opening of files, urls and apps. (coming soon)
- Automatically generate file structure for your courses. (coming soon)
- Quickly reload the config file.

## The config file
The config file is a json file that contains all the information about your courses. It is located at `~/.local/share/gnome-shell/extensions/quickstudy@octogradiste/config.json`. It contains the following fields:

| Key | Type | Description | Required | Special Tokens |
| --- | ---- | ----------- | -------- | ------------------ |
| `name` | `string` | The name of the semester this file represents. | No | No |
| `basePath` | `string` | The path to your study folder. | Yes | No |
| `weekToNum` | `object` | A mapping from a week to a number. | Yes | No |
| `courses` | `array` | An array of courses. | Yes | No |

The `weekToNum` object is a mapping from a week to a number. The week is a string of the form `YYYY-WW` where `YYYY` is the year and `WW` is the week number (padded with a zero if necessary). The number it maps to is the week number of the semester. The first week of the semester should have the number 1.

The `courses` array contains all the courses you have. Each course is an object with the following fields:

| Key | Type | Description | Required | Special Tokens |
| --- | ---- | ----------- | -------- | ------------------ |
| `fullName` | `string` | The full name of the course. | Yes | No |
| `shortName` | `string` | The short name of the course. | Yes | No |
| `urls` | `array` | An array of urls. | Yes | No |
| `apps` | `array` | An array of apps. | Yes | No |
| `structure` | `array` | An array of file structures. | Yes | No |
| `events` | `array` | An array of events. | Yes | No |

### URLs

The `urls` array contains all the urls you want to open for this course. Each url is an object with the following fields:

| Key | Type | Description | Required | Special Tokens |
| --- | ---- | ----------- | -------- | ------------------ |
| `name` | `string` | The name to display inside the menu. | Yes | Yes |
| `url` | `string` | The url to the website. | Yes | Yes |
| `quick` | `boolean` | If `true` this website will be added to the menu. | Yes | No |

### Apps

The `apps` array contains all the apps you want to open for this course. Each app is an object with the following fields:

| Key | Type | Description | Required | Special Tokens |
| --- | ---- | ----------- | -------- | ------------------ |
| `name` | `string` | The name to display inside the menu. | Yes | Yes |
| `cmd` | `string` | The command to run. | Yes | Yes |
| `args` | `array` | An array of arguments (strings) to pass to the command. | Yes | Yes |
| `quick` | `boolean` | If `true` this app will be added to the menu. | Yes | No |

### File Structure

The `structure` array contains all the files and folders you want to open for this course. Each structure is an object with the following fields:

| Key | Type | Description | Required | Special Tokens |
| --- | ---- | ----------- | -------- | ------------------ |
| `name` | `string` | The name to display inside the menu. | Yes | Yes |
| `path` | `string` | The path to the folder. | Yes | Yes |
| `template` | `string` | The name of the template file. | No | Yes |
| `quick` | `boolean` | If `true` this structure will be added to the menu. | Yes | No |

The `template` field is the name of a template file that will be used as a template when automatically generating the file structure.
It is located in the `template` folder of the extension. There are three default template files: `empty.md`, `empty.tex` and `empty.xopp`. 
Feel free to modify them and add your own.

### Events

The `events` array contains all the events you have for this course. Each event is an object with the following fields:

| Key | Type | Description | Required | Special Tokens |
| --- | ---- | ----------- | -------- | ------------------ |
| `day` | `string` | The day of the week. | Yes | No |
| `start` | `string` | The start time of the event in the following format: `HH:MM`. | Yes | No |
| `end` | `string` | The end time of the event in the following format: `HH:MM` | Yes | No |
| `type` | `string` | The type of the event. | No | No |
| `location` | `string` | The location of the event. | No | No |
| `autoOpen` | `array` | An array of strings that represent the items to open when the event starts. | Yes | Yes |

The items of the `autoOpen` array should be strings of the form `type-id` where `type` is either `url`, `app` or `structure` and `id` is equal to the `name` field of an object in the array of the given type.

### Special Tokens
The following tokens will be replced by the corresponding value:
- `$w` is replaced by the current week number.
- `$W` is replaced by the current week number padded with a 0.
- `$n` is the short name of the course.
- `$N` is the name of the course.
- `$b` and `$B` is the base path of the course.

### Basic template

```json
{
    "name": "OPTIONAL",
    "basePath": "PATH",
    "weekToNum": {
        "YYYY-WW": 1
    },
    "courses": [
        {
            "fullName": "FULL NAME",
            "shortName": "SHORT NAME",
            "urls": [
                {
                    "name": "WEBSITE NAME",
                    "url": "URL",
                    "quick": true
                }
            ],
            "apps": [
                {
                    "name": "APP NAME",
                    "cmd": "CMD",
                    "args": [
                        "ARG"
                    ],
                    "quick": true
                }
            ],
            "structure": [
                {
                    "name": "FILE OR FOLDER NAME",
                    "path": "PATH",
                    "template": "OPTIONAL",
                    "quick": true
                }
            ],
            "events": [
                {
                    "day": "WEEK DAY",
                    "start": "HH:MM",
                    "end": "HH:MM",
                    "type": "OPTIONAL",
                    "location": "OPTIONAL",
                    "autoOpen": [
                        "url-WEBSITE NAME",
                        "app-APP NAME",
                        "structure-FILE OR FOLDER NAME"
                    ]
                }
            ]
        }
    ]
}
```
