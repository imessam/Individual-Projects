/*
 * Copyright (c) 2020. Mohamed Essam Abdelfatah
 */

package sample;

import java.util.ArrayList;

public class SyntaxTree {
    private final ArrayList<Leaf> leaves = new ArrayList<>();
    private int currentLeafIndex;


    public ArrayList<Leaf> getLeaves() {
        return leaves;
    }

    public int getCurrentLeafIndex() {
        return currentLeafIndex;
    }

    public Leaf getLeaf(int index) {
        return leaves.get(index);
    }

    public void addLeaf(Leaf leaf) {
        leaves.add(leaf);
        currentLeafIndex++;
    }

    public void printLeafs() {
        for (Leaf leaf :
                leaves) {
            leaf.printLeaf();
        }
    }

}
