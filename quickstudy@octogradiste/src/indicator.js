const St = imports.gi.St;
const Clutter = imports.gi.Clutter;
const GObject = imports.gi.GObject;
const Gio = imports.gi.Gio;
const Json = imports.gi.Json;

const ExtensionUtils = imports.misc.extensionUtils;
const Me = ExtensionUtils.getCurrentExtension();
const PanelMenu = imports.ui.panelMenu;
const PopupMenu = imports.ui.popupMenu;

const logMessage = Me.imports.src.utils.logMessage;

/**
 * Returns the current week number in the format "YYYY-WW".
 * 
 * @returns {string} e.g. 2021-01
 */
function getCurrentWeekKey() {
    let today = new Date();
    let year = today.getFullYear();
    let millisecondsInDay = 1000 * 60 * 60 * 24;
    let days = Math.floor((today - new Date(year, 0, 1)) / millisecondsInDay);
    let week = Math.ceil(days / 7);
    return year.toString() + "-" + week.toString().padStart(2, '0');
}

/**
 * Opens the given uri with the default application.
 * 
 * @param {string} uri A url or file path.
 */
function openUriWithDefaultApp(uri) {
    logMessage(`opening ${uri} with default app...`);
    Gio.AppInfo.launch_default_for_uri(uri, null);
}

/**
 * Launches the given app with the given arguments.
 * 
 * @param {string} app The name of the app to launch.
 * @param {string[]} args The arguments to pass to the app.
 */
function launchApp(app, args) {
    logMessage(`launching ${app} with args ${args.join(" ")}.`);
    let cmd = app + " " + args.join(" ");
    Gio.AppInfo.create_from_commandline(cmd, null, 1).launch([], null);
}

/**
 * Creates a function that parses a path string.
 * 
 * @param {string} basePath The base path to the course folder.
 * @param {string} shortName The short name of the course.
 * @param {string} fullName The full name of the course.
 * @param {int} weekNum The current week number.
 * @returns A function that parses a path string.
 */
function getPathParser(basePath, shortName, fullName, weekNum) {
    return (path) => path
        .replace(/\$b/g, basePath)
        .replace(/\$B/g, basePath)
        .replace(/\$c/g, shortName)
        .replace(/\$C/g, fullName)
        .replace(/\$w/g, weekNum.toString())
        .replace(/\$W/g, weekNum.toString().padStart(2, '0'))
        .replace(/\/{2,}/g, '\/'); // Removes duplicate slashes.
    }

/**
 * Loads the config file and returns it as a JSON object.
 * 
 * @returns {Object} The config or null if the config file could not be loaded.
 */
function loadConfig() {
    let parser = new Json.Parser()
    let path = Me.path + '/config.json';
    if (parser.load_from_file(path)) {
        return JSON.parse(Json.to_string(parser.get_root(), true));
    } else {
        return null;
    }
}

const Indicator = GObject.registerClass(
    class Indicator extends PanelMenu.Button {
        _init() {
            super._init(0.0, "QuickStudy Indicator", false);

            this.add_child(new St.Label({
                text: "QuickStudy",
                y_align: Clutter.ActorAlign.CENTER,
            }));

            this._buildMenu();
        }

        _buildMenu() {
            let config = loadConfig()
            if (config === null) {
                logMessage('failed to load config');
            } else {
                this._addCourseItems(config);
                this.menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());
            }

            this.menu.addAction('Reload config file', () => {
                logMessage('reloading config...');

                this.menu.removeAll();
                this._buildMenu();
            });
        }


        _addCourseItems(config) {
            let weekKey = getCurrentWeekKey();
            let weekNum = config['weekToNum'][weekKey];
            
            config['courses'].forEach(course => {
                let name = course['fullName'];
                let item = new PopupMenu.PopupSubMenuMenuItem(name , false);

                let parse = getPathParser(
                    config['basePath'],
                    course['shortName'],
                    course['fullName'],
                    weekNum
                );

                course['urls']
                    .filter(url => url['quick'] === true)
                    .forEach(url => {
                        item.menu.addAction(url['name'], () => {
                            openUriWithDefaultApp(url['url']);
                        });
                    });

                course['apps']
                    .filter(app => app['quick'] === true)
                    .forEach(app => {
                        item.menu.addAction(app['name'], () => {
                            let args = app['args'].map(parse);
                            launchApp(app['cmd'], args)
                        });
                    });

                course['structure']
                    .filter(structure => structure['quick'] === true)
                    .forEach(structure => {
                        item.menu.addAction(structure['name'], () => {
                            let uri = "file://" + parse(structure['path']);
                            openUriWithDefaultApp(uri);
                        });
                    });

                this.menu.addMenuItem(item);
            });
        }
    }
);
