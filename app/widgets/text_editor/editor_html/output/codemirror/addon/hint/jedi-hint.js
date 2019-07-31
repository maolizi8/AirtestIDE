(function(mod) {
  if (typeof exports == "object" && typeof module == "object") // CommonJS
    mod(require("../../lib/codemirror"));
  else if (typeof define == "function" && define.amd) // AMD
    define(["../../lib/codemirror"], mod);
  else // Plain browser env
    mod(CodeMirror);
})(function(CodeMirror) {
  "use strict";
  var WORD = /[\w$]+/, RANGE = 500;

  CodeMirror.registerHelper("hint", "jedi", function(editor, options) {
      var cur = editor.getCursor();
      var token = editor.getTokenAt(cur);
      // If it's not a 'word-style' token, ignore the token.
      if (!/^[\w$_]*$/.test(token.string)) {
          token = {
              start: cur.ch, end: cur.ch, string: "", state: token.state,
              type: token.string == "." ? "property" : null
          };
          if (token.type !== "property") {
              return;
          }
      } else if (token.end > cur.ch) {
          token.end = cur.ch;
          token.string = token.string.slice(0, cur.ch - token.start);
      };

      return new Promise((resolve, reject) => {
        qtbridge.auto_completion(cur.line, cur.ch, function (completions) {
                resolve({
                    from: CodeMirror.Pos(cur.line, token.start),
                    to: CodeMirror.Pos(cur.line, token.end),
                    list: completions
                });

          });
      })

  });
});
