/*
 * Copyright (c) 2020. Mohamed Essam Abdelfatah
 */

package sample;

import javafx.util.Pair;

import java.util.ArrayList;

public class Operators {
    private final ArrayList<Pair<String, String>> OPERATORS = new ArrayList<>();

    public Operators() {
        init_operators();
    }

    private void init_operators() {
        String[] separators = new String[]{";", ",", "(", ")", "{", "}", "\""};
        String[] single_operators = new String[]{"*", "/", "+", "-"};
        String[] multi_operators = new String[]{":=", "==", "!=", "<", ">"};
        String[][] operators = new String[][]{separators, single_operators, multi_operators};
        for (int i = 0; i < 3; i++) {
            for (String op :
                    operators[i]) {
                if (i == 0) {
                    switch (op) {
                        case ";":
                            OPERATORS.add(new Pair<>("SEMICOLON", op));
                            break;
                        case ",":
                            OPERATORS.add(new Pair<>("COLON", op));
                            break;
                        case "(":
                            OPERATORS.add(new Pair<>("OPENBRACKET", op));
                            break;
                        case ")":
                            OPERATORS.add(new Pair<>("CLOSEDBRACKET", op));
                            break;
                        case "{":
                            OPERATORS.add(new Pair<>("OPENCOMMENT", op));
                            break;
                        case "}":
                            OPERATORS.add(new Pair<>("CLOSEDCOMMENT", op));
                            break;
                        case "\"":
                            OPERATORS.add(new Pair<>("BEGINDOUBLEQUOTES", op));
                    }
                } else if (i == 1) {
                    switch (op) {
                        case "*":
                            OPERATORS.add(new Pair<>("MULT", op));
                            break;
                        case "/":
                            OPERATORS.add(new Pair<>("DIV", op));
                            break;
                        case "+":
                            OPERATORS.add(new Pair<>("PLUS", op));
                            break;
                        case "-":
                            OPERATORS.add(new Pair<>("MINUS", op));
                            break;
                    }
                } else {
                    switch (op) {
                        case ":=":
                            OPERATORS.add(new Pair<>("ASSIGN", op));
                            break;
                        case "==":
                            OPERATORS.add(new Pair<>("ISEQUAL", op));
                            break;
                        case "!=":
                            OPERATORS.add(new Pair<>("NOTEQUAL", op));
                            break;
                        case "<":
                            OPERATORS.add(new Pair<>("LESSTHAN", op));
                            break;
                        case ">":
                            OPERATORS.add(new Pair<>("GREATERTHAN", op));
                            break;
                    }
                }
            }
        }
    }

    public ArrayList<Pair<String, String>> getOPERATORS() {
        return OPERATORS;
    }

    public Pair<String, String> getOperator(String key) {
        for (Pair<String, String> operator :
                OPERATORS) {
            if (operator.getKey().equals(key)) {
                return operator;
            }
        }
        return null;
    }
}
