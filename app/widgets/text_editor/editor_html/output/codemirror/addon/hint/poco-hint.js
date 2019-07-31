// CodeMirror, copyright (c) by Marijn Haverbeke and others
// Distributed under an MIT license: http://codemirror.net/LICENSE

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

  CodeMirror.registerHelper("hint", "poco", function(editor, options) {
    var cur = editor.getCursor(), curLine = editor.getLine(cur.line);
    var token = editor.getTokenAt(cur);
    var pocofw_module = "add_post_action_callback add_pre_action_callback agent click freeze get_screen_size long_click "
    + "sleep_for_polling_interval snapshot wait_for_all swipe wait_for_any wait_stable";
    var pocoxy_module = "attr child children click drag_to exists focus get_bounds get_name get_position get_size "
    + "get_text invalidate nodes offspring set_text setattr sibling swipe wait wait_for_appearance wait_for_disappearance ";
      token.state = CodeMirror.innerMode(editor.getMode(), token.state).state;

    // If it's not a 'word-style' token, ignore the token.
    if (!/^[\w$_]*$/.test(token.string)) {
      token = {start: cur.ch, end: cur.ch, string: "", state: token.state,
               type: token.string == "." ? "property" : null};
    } else if (token.end > cur.ch) {
      token.end = cur.ch;
      token.string = token.string.slice(0, cur.ch - token.start);
    }

    var tprop = token;
    var token_type = tprop.type;
    var pocoHint = false;
    // 包含了poco在行中的property才需要显示poco的下拉接口
    if (tprop.type == "property" && curLine.indexOf("poco") !== -1) {
        // If it is a property, find out what it is a property of.
        while (tprop.type == "property") {
            tprop = editor.getTokenAt(CodeMirror.Pos(cur.line, tprop.start));
            if (tprop.string != ".") return;
            tprop = editor.getTokenAt(CodeMirror.Pos(cur.line, tprop.start));
            pocoHint = true;
        }
    }

    var list = pocofw_module + pocoxy_module;
    var context = [];
    if (pocoHint) {
      list = list.split(" ");
      for (var i=0, len=list.length; i<len; i++){
        if (list[i].indexOf(token.string) != -1) {
          context.push(list[i]);
        }
      }
      return {from: CodeMirror.Pos(cur.line, token.start), to: CodeMirror.Pos(cur.line, token.end), list: context}
    } else {
      var orig = CodeMirror.hint.python;
      var anyword = CodeMirror.hint.anyword;
      var ret = orig(editor);
      if (token_type == "variable") {
        ret.list = ret.list.concat(anyword(editor).list);
      }
      return ret;
    }
  });
});
