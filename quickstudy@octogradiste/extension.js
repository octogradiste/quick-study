const Main = imports.ui.main;

const ExtensionUtils = imports.misc.extensionUtils;
const Me = ExtensionUtils.getCurrentExtension();

const logMessage = Me.imports.src.utils.logMessage;
const Indicator = Me.imports.src.indicator.Indicator;

const Gtk = imports.gi.Gtk;

class Extension {
    constructor() {
        this._indicator = null;
        this._fileChooser = null;
    }
    
    enable() {
        logMessage('enabling extension...');

        this._indicator = new Indicator();
        Main.panel.addToStatusArea(Me.metadata.uuid, this._indicator);
    }
    
    disable() {
        logMessage('disabling extension...');

        this._indicator.destroy();
        this._indicator = null;
    }
}


function init() {
    logMessage('initializing extension...');
    
    return new Extension();
}
