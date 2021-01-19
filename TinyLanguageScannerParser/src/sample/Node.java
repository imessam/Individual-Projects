/*
 * Copyright (c) 2020. Mohamed Essam Abdelfatah
 */

package sample;

import javafx.util.Pair;

public class Node {
    private final String data, type;
    private Node first, second, third;
    private Pair<Double, Double> coordinates;

    public Node(String data, String type) {
        this.data = data;
        this.type = type;
    }

    public Pair<Double, Double> getCoordinates() {
        return coordinates;
    }

    public void setCoordinates(Pair<Double, Double> coordinates) {
        this.coordinates = coordinates;
    }

    public Node getFirst() {
        return first;
    }

    public void setFirst(Node first) {
        this.first = first;
    }

    public Node getSecond() {
        return second;
    }

    public void setSecond(Node second) {
        this.second = second;
    }

    public Node getThird() {
        return third;
    }

    public void setThird(Node third) {
        this.third = third;
    }

    public String getData() {
        return data;
    }

    public String getType() {
        return type;
    }

    public String printNode() {
        String s = "\t" + this.data;
        if (this.first != null) {
            s += "\n\t first : " + this.first.printNode();
        }
        if (this.second != null) {
            s += " \n\t second : " + this.second.printNode();
        }
        if (this.third != null) {
            s += " \n\t third : " + this.third.printNode();
        }
        return s;
    }
}
