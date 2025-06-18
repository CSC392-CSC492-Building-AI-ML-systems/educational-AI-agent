// const term = new Terminal({
//         cursorBlink: true,
//         rows: 30,
//         cols: 80,
//       });

// term.open(document.getElementById('terminal'));
// term.focus(); // Ensures the terminal has keyboard focus
// term.write('Hello from \x1B[1;3;31mxterm.js\x1B[0m\r\n$ ');

// let command = '';

// term.onKey(e => {
//   const char = e.key;

//   if (e.domEvent.key === 'Backspace') {
//     if (command.length > 0) {
//       command = command.slice(0, -1);
//       term.write('\b \b');
//     }
//   } else if (e.domEvent.key === 'Enter') {
//     term.write('\r\nYou typed: ' + command + '\r\n$ ');
//     command = '';
//   } else if (e.domEvent.key.length === 1) {
//     command += char;
//     term.write(char);
//   }
// });