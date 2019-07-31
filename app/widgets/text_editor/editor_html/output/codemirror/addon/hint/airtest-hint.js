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

  CodeMirror.registerHelper("hint", "airtest", function(editor, options) {
    var cur = editor.getCursor(), curLine = editor.getLine(cur.line);
    var word = options && options.word || WORD;
    var end = cur.ch, start = end;
    while (start && word.test(curLine.charAt(start - 1))) --start;
    var curWord = start != end && curLine.slice(start, end);

    /*
    var list = [{
        text: "timeout=20",
        displayText: "timeout=20  // 语句识别超时时间",
        className: "propertyClass"
    }, {
        text: "delay=0",
        displayText: "delay=0  // 点击后等待(x)s再继续执行",
        className: "propertyClass"
    }, {
        text: "duration=0.01",
        displayText: "duration=0.01  // 默认点击按钮的长按时间",
        className: "propertyClass"
    }, {
        text: "if_exists=False",
        displayText: "if_exists=False  // 如果设为True，只有图片存在才点击，不存在不会报错",
        className: "propertyClass"
    },{
        text: "times=1",
        displayText: "times=1  // 点击次数",
        className: "propertyClass"
    }, {
        text: "right_click=False",
        displayText: "right_click=False  // 右键点击（仅windows下有效）",
        className: "propertyClass"
    }];
    */
    var list = [{
        text: "duration=0.01",
        displayText: "duration=0.01  // 默认点击按钮的长按时间",
        className: "propertyClass"
    }, {
        text: "times=1",
        displayText: "times=1  // 点击次数",
        className: "propertyClass"
    }]
    return {list: list, from: CodeMirror.Pos(cur.line, start), to: CodeMirror.Pos(cur.line, end)};
  });
});
