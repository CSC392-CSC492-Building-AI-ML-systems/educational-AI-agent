// asciinemaUtils.js serves as a utility module for handling functions
// relating to asciinema recordings.
// It provides functions to generate asciinema-type recording files from
// the website's terminal to be used by the models.

/**
 * Generates the Asciinema header object.
 *
 * @param {number} version - Asciinema recording version (usually 2).
 * @param {number} width - Terminal width in characters.
 * @param {number} height - Terminal height in characters.
 * @param {number} timestamp - UNIX timestamp for the start of the recording.
 * @param {string} SHELL - Shell type (e.g., '/bin/bash').
 * @param {string} TERM - Terminal type (e.g., 'xterm').
 * @returns {object} - Asciinema header object.
 */
function createAsciinemaHeader(version, width, height, timestamp, SHELL, TERM) {
    return {
        "version": version,
        "width": width,
        "height": height,
        "timestamp": timestamp,
        "env": {
        "SHELL": SHELL,
        "TERM": TERM
        }
    };
}

/**
 * Converts a user input event to an asciinema-formatted line.
 * @param {string} inputString - The character or string input from the user.
 * @param {number} timestamp - The time the input occurred in seconds after start.
 * @returns {Array} An asciinema-formatted event array: [timestamp, "i", input]
 */
function convertInputEvent(inputString, timestamp) {
  return [timestamp, "i", inputString];
}

/**
 * Converts a user output event to an asciinema-formatted line.
 * @param {string} outputString - The character or string output from the terminal.
 * @param {number} timestamp - The time the output occurred in seconds after start.
 * @returns {Array} An asciinema-formatted event array: [timestamp, "o", output]
 */
function convertOutputEvent(outputString, timestamp) {
  return [timestamp, "o", outputString];
}