const ExtensionUtils = imports.misc.extensionUtils;
const Me = ExtensionUtils.getCurrentExtension();

function logMessage(message) {
    log(`[${Me.metadata.name}] ${message}`);
}
