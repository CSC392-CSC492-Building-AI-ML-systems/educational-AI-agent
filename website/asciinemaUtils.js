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
    version,
    width,
    height,
    timestamp,
    env: { SHELL, TERM }
  };
}

/**
 * Converts a user input event to an asciinema-formatted line.
 * @param {number} timestamp - Seconds since session start.
 * @param {string} inputString - Raw input (single char or sequence).
 * @returns {Array} [timestamp, "i", input]
 */
function convertInputEvent(timestamp, inputString) {
  return [timestamp, "i", inputString];
}

/**
 * Converts a user output event to an asciinema-formatted line.
 * @param {number} timestamp - Seconds since session start.
 * @param {string} outputString - PTY output chunk.
 * @returns {Array} [timestamp, "o", output]
 */
function convertOutputEvent(timestamp, outputString) {
  return [timestamp, "o", outputString];
}

/**
 * Serialize header + events to an asciinema v2 .cast string.
 * First line is JSON(header), followed by JSON([t, "i"/"o", data]) per line.
 * @param {object} header
 * @param {Array<Array>} events
 * @returns {string}
 */
function toCastString(header, events) {
  const lines = [JSON.stringify(header)];
  for (const ev of events || []) {
    let [t, type, data] = ev;
    if (typeof t !== 'number') t = Number(t) || 0;
    if (type !== 'i' && type !== 'o') type = 'o';
    if (typeof data !== 'string') data = String(data ?? '');
    lines.push(JSON.stringify([t, type, data]));
  }
  return lines.join('\n');
}

/**
 * Convenience: accept a { header, events } object and serialize it.
 * @param {{header: object, events: Array<Array>}} ctx
 * @returns {string}
 */
function getContextCastString(ctx) {
  return toCastString(ctx.header, ctx.events);
}

module.exports = {
  createAsciinemaHeader,
  convertInputEvent,
  convertOutputEvent,
  toCastString,
  getContextCastString
};