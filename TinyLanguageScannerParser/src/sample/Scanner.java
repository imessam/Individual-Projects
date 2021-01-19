/*
 * Copyright (c) 2020. Mohamed Essam Abdelfatah
 */


/*
Keywords:   WRITE READ IF ELSE RETURN BEGIN END MAIN STRING INT REAL
Single-character separators:   ;  ,  (   )
Single-character operators:    +  -  *   /
Multi-character operators:    :=  ==   !=
Identifier: An identifier consists of a letter followed by any number of letters or digits. The following are examples of identifiers: x, x2, xx2, x2x, End, END2.Note that End is an identifier while END is a keyword. The following are not identifiers:

    IF, WRITE, READ, .... (keywords are not counted as identifiers)
    2x (identifier can not start with a digit)
    Strings in comments are not identifiers.
*/

package sample;

import javafx.util.Pair;

import java.util.ArrayList;

public class Scanner {


    private final ArrayList<Token> TOKENS = new ArrayList<>();
    private ArrayList<Pair<String, String>> KEYWORDS;
    private ArrayList<Pair<String, String>> OPERATORS;
    private Pair<String, String> tempToken;
    private String waitOP = "", waitedString = "";

    public ArrayList<Token> getTOKENS() {
        return TOKENS;
    }


    public String scan(String text) {
        TOKENS.clear();
        String[] lines = text.split("\n");
        for (String line :
                lines) {
            scanLine(removeRedundantSpaces(line));
        }
        return printTokens();
    }

    public void setKEYWORDS(ArrayList<Pair<String, String>> KEYWORDS) {
        this.KEYWORDS = KEYWORDS;
    }

    public void setOPERATORS(ArrayList<Pair<String, String>> OPERATORS) {
        this.OPERATORS = OPERATORS;
    }

    private String removeRedundantSpaces(String text) {
        String m = "";
        String[] split = text.split("");
        for (int i = 0; i < split.length; i++) {
            if (!split[i].equals(" ")) {
                m = m.concat(split[i]);
            } else {
                if ((!m.isEmpty()) && (!split[i - 1].equals(" "))) {
                    m = m.concat(split[i]);
                }
            }
        }
        return m;
    }

    private boolean isKeyword(String word) {
        for (Pair<String, String> keyword :
                KEYWORDS) {
            if (keyword.getValue().equals(word)) {
                tempToken = keyword;
                return true;
            }
        }
        return false;
    }

    private boolean isOperator(String word) {
        for (Pair<String, String> keyword :
                OPERATORS) {
            if (keyword.getValue().equals(word)) {
                tempToken = keyword;
                return true;
            }
        }
        return false;
    }

    private boolean isNumeric(String word) {
        char[] chars = word.toCharArray();
        for (char c :
                chars) {
            if (!Character.isDigit(c)) {
                return false;
            }
        }
        return true;
    }

    private boolean detectComments() {
        if (tempToken.getValue().equals("{")) {
            waitOP = "}";
            return true;
        }
        return false;
    }

    private boolean detectString() {
        if (tempToken.getValue().equals("\"")) {
            waitOP = "\"";
            return true;
        }
        return false;
    }

    private boolean isWait() {
        return (detectComments() || detectString());
    }

    private boolean endWait(String letter) {
        if (letter.equals(waitOP)) {
            if (waitOP.equals("\"")) {
                TOKENS.add(new Token(new Pair<>("STRING", waitedString)));
                TOKENS.add(new Token(new Pair<>("ENDDOUBLEQUOTES", waitOP)));
            }
            waitedString = "";
            waitOP = "";
            return false;
        } else {
            waitedString = waitedString.concat(letter);
            return true;
        }
    }

    private void addKeyword() {
        TOKENS.add(new Token(tempToken));
    }

    private void addOperator() {
        TOKENS.add(new Token(tempToken));
    }

    private void addIdentifier(String id) {
        if (!id.equals("")) {
            if (isKeyword(id)) {
                addKeyword();
            } else if (isNumeric(id)) {
                TOKENS.add(new Token(new Pair<>("NUMBER", id)));
            } else {
                TOKENS.add(new Token(new Pair<>("IDENTIFIER", id)));
            }
        }
    }

    private void scanLine(String line) {

        String[] s = line.split(" ");
        boolean wait = false;
        Pair<String, String> tempPair;

        for (String word :
                s) {
            if (!wait) {
                if (isKeyword(word)) {
                    addKeyword();
                } else if (isOperator(word)) {
                    wait = isWait();
                    if (!waitOP.equals("}")) {
                        addOperator();
                    }
                } else {
                    String[] split = word.split("");
                    String concat = "";
                    for (String letter :
                            split) {
                        if (!wait) {
                            if (isOperator(letter)) {
                                wait = isWait();
                                tempPair = tempToken;
                                addIdentifier(concat);
                                tempToken = tempPair;
                                addOperator();
                                concat = "";
                            } else {
                                concat = concat.concat(letter);
                            }
                        } else {
                            wait = endWait(letter);
                        }
                    }
                    addIdentifier(concat);
                }
            } else {
                wait = endWait(word);
            }
        }
    }

    private String printTokens() {
        String s = "Token Type : Token Value\n\n";
        for (Token token :
                TOKENS) {
            s = s.concat(token.getToken().getKey() + " : " + token.getToken().getValue() + "\n");
            System.out.println(token.getToken().getKey() + " : " + token.getToken().getValue());
        }
        return s;
    }

}
