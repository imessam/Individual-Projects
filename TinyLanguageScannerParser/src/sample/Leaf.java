/*
 * Copyright (c) 2020. Mohamed Essam Abdelfatah
 */

package sample;

import java.util.ArrayList;

public class Leaf {
    private final ArrayList<Node> nodes = new ArrayList<>();
    private int currentNode;
    private Node rootNode = new Node("null", null);

    public Node getRootNode() {
        return rootNode;
    }

    public void setRootNode(Node rootNode) {
        this.rootNode = rootNode;
    }

    public ArrayList<Node> getNodes() {
        return nodes;
    }

    public Node getCurrentNode() {
        return nodes.get(currentNode - 1);
    }

    public Node addStmt(String stmt) {
        Node node = new Node(stmt, "stmt");
        nodes.add(node);
        currentNode++;
        return node;
    }

    public void printLeaf() {
        System.out.println("\nNew Leaf : root = " + rootNode.getData() + " \n");
        for (Node n :
                nodes) {
            System.out.println("################\n" + n.printNode() + "\n#####################");
        }
    }

}
