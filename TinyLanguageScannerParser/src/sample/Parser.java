/*
 * Copyright (c) 2020. Mohamed Essam Abdelfatah
 */

package sample;

import javafx.util.Pair;

import java.util.ArrayList;

public class Parser {

    int count = 0, currentTree;
    ArrayList<String> stmts = new ArrayList<>();
    private Keywords keywords;
    private Operators operators;
    private Leaf leaf;
    private SyntaxTree syntaxTree;
    private ArrayList<Token> TOKENS;
    private Token currentToken;

    public void setKeywords(Keywords keywords) {
        this.keywords = keywords;
    }

    public void setOperators(Operators operators) {
        this.operators = operators;
    }

    public void setTOKENS(ArrayList<Token> TOKENS) {
        this.TOKENS = TOKENS;
    }

    public Pair<SyntaxTree, Boolean> parse() {
        Pair<SyntaxTree, Boolean> returned;
        syntaxTree = new SyntaxTree();
        stmts.clear();
        count = 0;
        currentTree = 0;
        TOKENS.add(new Token(new Pair<>("EOS", "EOS")));
        currentToken = TOKENS.get(0);
        if (!(program()).getValue()) {
            returned = new Pair<>(syntaxTree, false);
        } else {
            syntaxTree.getLeaf(0).setRootNode(syntaxTree.getLeaf(0).getNodes().get(0));
            returned = new Pair<>(syntaxTree, true);
        }
        printStmts();
        syntaxTree.printLeafs();
        return returned;
    }

    private boolean match(Token expectedToken) {
        boolean matched = false;
        if (currentToken.equals(expectedToken)) {
            count++;
            if (getNextToken()) {
                matched = true;
            }
        }
        return matched;
    }

    private boolean getNextToken() {
        if (count == TOKENS.size()) {
            return false;
        }
        currentToken = TOKENS.get(count);
        return true;
    }

    private Pair<Node, Boolean> program() {
        return stmt_sequence();
    }

    //stmt-sequence → statement {statement;}
    private Pair<Node, Boolean> stmt_sequence() {
        Pair<Node, Boolean> returned;
        leaf = new Leaf();
        syntaxTree.addLeaf(leaf);
        do {
            if (!(returned = statement()).getValue()) {
                returned = new Pair<>(null, false);
            }
        } while (match(new Token(operators.getOperator("SEMICOLON"))));
        return returned;
    }

    private Pair<Node, Boolean> statement() {
        Pair<Node, Boolean> returned;
        if ((returned = if_stmt()).getValue()) return returned;
        if ((returned = repeat_stmt()).getValue()) return returned;
        if ((returned = assign_stmt()).getValue()) return returned;
        if ((returned = read_stmt()).getValue()) return returned;
        if ((returned = write_stmt()).getValue()) return returned;
        return returned;
    }

    //if exp then stmt-sequence [else stmt-sequence] end
    private Pair<Node, Boolean> if_stmt() {
        Pair<Node, Boolean> returned = new Pair<>(null, false), temp;
        int tempCount = count, tempLeaf;

        if (match(new Token(keywords.getKeyword("IF")))) {
            if ((temp = exp()).getValue()) {
                Node ifNode = leaf.addStmt("if");
                ifNode.setFirst(temp.getKey());

                if (match(new Token(keywords.getKeyword("THEN")))) {
                    tempLeaf = syntaxTree.getCurrentLeafIndex();

                    if (stmt_sequence().getValue()) {
                        ifNode.setSecond(syntaxTree.getLeaf(tempLeaf).getNodes().get(0));
                        leaf = syntaxTree.getLeaf(tempLeaf - 1);
                        syntaxTree.getLeaf(tempLeaf).setRootNode(ifNode);

                        if (match(new Token(keywords.getKeyword("ELSE")))) {
                            tempLeaf = syntaxTree.getCurrentLeafIndex();

                            if ((stmt_sequence()).getValue()) {
                                ifNode.setThird(syntaxTree.getLeaf(tempLeaf).getNodes().get(0));
                                leaf = syntaxTree.getLeaf(tempLeaf - 2);
                                syntaxTree.getLeaf(tempLeaf).setRootNode(ifNode);

                                if (match(new Token(keywords.getKeyword("END")))) {
                                    stmts.add("if_stmt");
                                    returned = new Pair<>(ifNode, true);
                                    //returned = true;
                                }
                            }
                        } else {
                            if (match(new Token(keywords.getKeyword("END")))) {
                                stmts.add("if_stmt");
                                returned = new Pair<>(ifNode, true);
                                //returned = true;
                            }
                        }
                    }
                }
            }
        }

        if (!returned.getValue()) {
            count = tempCount;
            getNextToken();
        }
        return returned;
    }

    //repeat stmt-sequence until exp
    private Pair<Node, Boolean> repeat_stmt() {
        Pair<Node, Boolean> returned = new Pair<>(null, false), temp;
        int tempCount = count, tempLeaf;

        if (match(new Token(keywords.getKeyword("REPEAT")))) {
            Node repeatNode = leaf.addStmt("repeat");
            tempLeaf = syntaxTree.getCurrentLeafIndex();

            if (stmt_sequence().getValue()) {
                repeatNode.setFirst(syntaxTree.getLeaf(tempLeaf).getNodes().get(0));
                leaf = syntaxTree.getLeaf(tempLeaf - 1);
                syntaxTree.getLeaf(tempLeaf).setRootNode(repeatNode);

                if (match(new Token(keywords.getKeyword("UNTIL")))) {

                    if ((temp = exp()).getValue()) {
                        stmts.add("repeat_stmt");
                        repeatNode.setThird(temp.getKey());
                        returned = new Pair<>(repeatNode, true);
                    }
                }
            }
        }

        if (!returned.getValue()) {
            count = tempCount;
            getNextToken();
        }
        return returned;
    }

    //identifier := exp
    private Pair<Node, Boolean> assign_stmt() {
        Pair<Node, Boolean> returned = new Pair<>(null, false), temp;
        int tempCount = count;

        if (match(new Token(new Pair<>("IDENTIFIER", "")))) {

            if (match(new Token(operators.getOperator("ASSIGN")))) {

                if ((temp = exp()).getValue()) {
                    stmts.add("assign_stmt");
                    returned = new Pair<>(leaf.addStmt("assign"), true);
                    returned.getKey().setFirst(new Node(TOKENS.get(tempCount).getToken().getValue(), "exp"));
                    returned.getKey().setSecond(temp.getKey());
                    //returned = true;
                }
            }
        }

        if (!returned.getValue()) {
            count = tempCount;
            getNextToken();
        }
        return returned;
    }

    //read identifier
    private Pair<Node, Boolean> read_stmt() {
        Pair<Node, Boolean> returned = new Pair<>(null, false);
        int tempCount = count;

        if (match(new Token(keywords.getKeyword("READ")))) {

            if (match(new Token(new Pair<>("IDENTIFIER", "")))) {
                stmts.add("read_stmt");
                returned = new Pair<>(leaf.addStmt("read"), true);
                returned.getKey().setFirst(new Node(TOKENS.get(tempCount + 1).getToken().getValue(), "exp"));
                //returned = true;
            }
        }

        if (!returned.getValue()) {
            count = tempCount;
            getNextToken();
        }
        return returned;
    }

    //write exp
    private Pair<Node, Boolean> write_stmt() {
        Pair<Node, Boolean> returned = new Pair<>(null, false), temp;
        int tempCount = count;

        if (match(new Token(keywords.getKeyword("WRITE")))) {

            if ((temp = exp()).getValue()) {
                stmts.add("write_stmt");
                returned = new Pair<>(leaf.addStmt("write"), true);
                returned.getKey().setFirst(temp.getKey());
                //returned = true;
            }
        }

        if (!returned.getValue()) {
            count = tempCount;
            getNextToken();
        }
        return returned;
    }

    //simple_exp [comparison_op simple_exp]
    private Pair<Node, Boolean> exp() {
        Pair<Node, Boolean> returned, temp;

        if ((returned = simple_exp()).getValue()) {

            if ((temp = comparison_op()).getValue()) {
                temp.getKey().setFirst(returned.getKey());
                returned = temp;

                if ((temp = simple_exp()).getValue()) {
                    returned.getKey().setSecond(temp.getKey());
                } else {
                    returned = new Pair<>(null, false);
                }
            }
        }
        return returned;
    }

    //term {addop term}
    private Pair<Node, Boolean> simple_exp() {
        Pair<Node, Boolean> returned, temp;

        if ((returned = term()).getValue()) {

            while ((temp = addop()).getValue()) {
                temp.getKey().setFirst(returned.getKey());
                returned = temp;

                if (!(temp = term()).getValue()) {
                    returned = new Pair<>(null, false);
                    break;
                }
                returned.getKey().setSecond(temp.getKey());
            }
        }
        return returned;
    }

    //factor {mulop factor}
    private Pair<Node, Boolean> term() {
        Pair<Node, Boolean> returned, temp;

        if ((returned = factor()).getValue()) {

            while ((temp = mulop()).getValue()) {
                temp.getKey().setFirst(returned.getKey());
                returned = temp;

                if (!(temp = factor()).getValue()) {
                    returned = new Pair<>(null, false);
                    break;
                }
                returned.getKey().setSecond(temp.getKey());
            }
        }
        return returned;
    }

    private Pair<Node, Boolean> factor() {
        Pair<Node, Boolean> returned = new Pair<>(null, false), temp;

        if (match(new Token(operators.getOperator("OPENBRACKET")))) {

            if ((temp = exp()).getValue()) {

                if (match(new Token(operators.getOperator("CLOSEDBRACKET")))) {
                    returned = temp;
                }
            }
        } else if (match(new Token(new Pair<>("IDENTIFIER", "")))) {
            returned = new Pair<>(new Node(TOKENS.get(count - 1).getToken().getValue(), "exp"), true);
        } else if (match(new Token(new Pair<>("NUMBER", "")))) {
            returned = new Pair<>(new Node(TOKENS.get(count - 1).getToken().getValue(), "exp"), true);
        }
        return returned;
    }

    private Pair<Node, Boolean> comparison_op() {
        Pair<Node, Boolean> returned = new Pair<>(null, false);
        if (match(new Token(operators.getOperator("LESSTHAN")))) {
            returned = new Pair<>(new Node("<", "exp"), true);
        } else if (match(new Token(operators.getOperator("ISEQUAL")))) {
            returned = new Pair<>(new Node("==", "exp"), true);
        } else if (match(new Token(operators.getOperator("GREATERTHAN")))) {
            returned = new Pair<>(new Node(">", "exp"), true);
        }
        return returned;
    }

    private Pair<Node, Boolean> addop() {
        Pair<Node, Boolean> returned = new Pair<>(null, false);
        if (match(new Token(operators.getOperator("PLUS")))) {
            returned = new Pair<>(new Node("+", "exp"), true);
        } else if (match(new Token(operators.getOperator("MINUS")))) {
            returned = new Pair<>(new Node("-", "exp"), true);
        }
        return returned;
    }

    private Pair<Node, Boolean> mulop() {
        Pair<Node, Boolean> returned = new Pair<>(null, false);
        if (match(new Token(operators.getOperator("MULT")))) {
            returned = new Pair<>(new Node("*", "exp"), true);
        } else if (match(new Token(operators.getOperator("DIV")))) {
            returned = new Pair<>(new Node("/", "exp"), true);
        }
        return returned;
    }

    private void printStmts() {
        for (String stmt :
                stmts) {
            System.out.println(stmt);
        }
    }
}
