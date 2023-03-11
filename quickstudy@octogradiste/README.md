# QuickStudy

## TODO
- Dropdowns for every course. If a course event is occuring it should already be open.
- Action buttons to reload and load a config file.
- Week counter automatically set.
- Toggle auto open
- Button to auto open manually.

## config.json

```json
{
    "name": "NAME",
    "basePath": "PATH",
    "weekToNum": {
        "YYYY-WW": 1,
    },
    "courses": [
        {
            "fullName": "FULL NAME",
            "shortName": "SHORT NAME",
            "urls": [
                {
                    "name": "NAME",
                    "url": "URI",
                    "quick": true,
                }
            ],
            "apps": [
                {
                    "name": "NAME",
                    "cmd": "CMD",
                    "args": [
                        "ARG",
                    ],
                    "quick": true,
                }
            ],
            "structure": [
                {
                    "name": "NAME",
                    "path": "PATH",
                    "template": "PATH",
                    "quick": true,
                }
            ],
            "events": [
                {
                    "day": "WEEK DAY",
                    "start": "HH:MM",
                    "end": "HH:MM",
                    "location": "LOCATION",
                    "type": "TYPE",
                    "autoOpen": [
                        "url-NAME",
                        "app-NAME",
                        "structure-NAME",
                    ]
                }
            ],
        }
    ]
}
```

## Special Tokens
- `$w` is replaced by the current week number.
- `$W` is replaced by the current week number padded with a 0.
- `$n` is the short name of the course.
- `$N` is the name of the course.
- `$b` and `$B` is the base path of the course.

If such tokens is in `PATH`, `URI`, `CMD`, `ARG` or a `NAME` it will be replaced by the value of the token.