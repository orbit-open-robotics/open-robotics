import { EditorState } from "@codemirror/state";

import {
  EditorView,
  keymap,
  lineNumbers,
  highlightActiveLine,
  highlightSpecialChars,
  drawSelection
} from "@codemirror/view";

import {
  defaultKeymap,
  history,
  historyKeymap
} from "@codemirror/commands";

import {
  indentOnInput,
  bracketMatching,
  foldGutter
} from "@codemirror/language";

import { python } from "@codemirror/lang-python";
import { autocompletion } from "@codemirror/autocomplete";
import { oneDark } from "@codemirror/theme-one-dark";

const starterCode = `def greet(name):
    print(f"Hello, {name}!")

def main():
    for i in range(3):
        greet("World")

if __name__ == "__main__":
    main()
`;

const state = EditorState.create({
    doc: starterCode,
    extensions: [
        lineNumbers(),
        highlightSpecialChars(),
        history(),
        drawSelection(),
        indentOnInput(),
        bracketMatching(),
        foldGutter(),
        highlightActiveLine(),

        keymap.of([
            ...defaultKeymap,
            ...historyKeymap
        ]),

        python(),
        autocompletion(),
        oneDark
    ]
});

new EditorView({
    state,
    parent: document.getElementById("editor")
});