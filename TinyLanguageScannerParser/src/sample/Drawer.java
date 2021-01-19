/*
 * Copyright (c) 2020. Mohamed Essam Abdelfatah
 */

package sample;

import javafx.scene.Group;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;
import javafx.util.Pair;

import java.util.ArrayList;

public class Drawer {
    private final double recWidth = 70;
    private final double recHeight = 40;
    private final double circleRadius = 30;

    private Group group;

    public Group drawSyntaxTree(SyntaxTree tree) {

        ArrayList<Leaf> leaves = tree.getLeaves();
        double x, y, stretch = 1;
        int count = 1;
        group = new Group();
        leaves.get(0).getRootNode().setCoordinates(new Pair<>(250.0, 0.0));

        for (int i = 0, leavesSize = leaves.size(); i < leavesSize; i++) {
            Leaf leaf = leaves.get(i);
            drawLeaf(leaf);
            if (i != (leavesSize - 1)) {
                x = leaves.get(i + 1).getRootNode().getCoordinates().getKey();
                y = leaves.get(i + 1).getRootNode().getCoordinates().getValue();
                if (leaves.get(i + 1).getRootNode().getData().equals("if")) {
                    if (count == 2) {
                        stretch = 2;
                    }
                    count++;
                }
                group.getChildren().add(new Line(x + (recWidth / 2), y + (recHeight), (x + (recWidth / 2)) * stretch, (y + (recHeight * 5)) / stretch));
                leaves.get(i + 1).getNodes().get(0).setCoordinates(new Pair<>((x + (recWidth / 2)) * stretch, (y + (recHeight * 5)) / stretch));
            }
        }
        return group;
    }

    private void drawLeaf(Leaf leaf) {

        ArrayList<Node> nodes = leaf.getNodes();
        double x, y;

        for (int i = 0, nodesSize = nodes.size(); i < nodesSize; i++) {
            Node node = nodes.get(i);
            drawNode(node);
            x = node.getCoordinates().getKey();
            y = node.getCoordinates().getValue();
            if (i != (nodesSize - 1)) {
                group.getChildren().add(new Line(x + (recWidth), y + (recHeight / 2), x + (recWidth * 4), y + (recHeight / 2)));
                nodes.get(i + 1).setCoordinates(new Pair<>(x + (recWidth * 4), y + (recHeight / 2)));
            }
        }
    }

    private void drawNode(Node node) {

        Node left = node.getFirst();
        Node middle = node.getSecond();
        Node right = node.getThird();
        double x = node.getCoordinates().getKey(), y = node.getCoordinates().getValue(), linex, liney;
        Text text;

        if (node.getType().equals("stmt")) {
            Rectangle rectangle = new Rectangle(x, y, recWidth, recHeight);
            rectangle.setFill(Color.RED);
            text = new Text(x + (recWidth / 2), y + (recHeight / 2), node.getData());
            text.setFill(Color.WHITE);
            text.setFont(Font.font(null, FontWeight.BOLD, 10));
            group.getChildren().addAll(rectangle, text);
            linex = recWidth;
            liney = recHeight;
        } else {
            Circle circle = new Circle(x, y, circleRadius);
            circle.setFill(Color.BLUE);
            text = new Text(x, y, node.getData());
            text.setFill(Color.WHITE);
            text.setFont(Font.font(null, FontWeight.BOLD, 10));
            group.getChildren().addAll(circle, text);
            linex = 0;
            liney = circleRadius;
        }
        if ((left != null) && (!left.getType().equals("stmt"))) {
            group.getChildren().add(new Line(x + (linex / 2), y + (liney), x - (3 * recWidth / 2), y + (4 * recHeight / 2)));
            left.setCoordinates(new Pair<>(x - (3 * recWidth / 2), y + (4 * recHeight / 2)));
            drawNode(left);
        }
        if ((middle != null) && (!middle.getType().equals("stmt"))) {
            group.getChildren().add(new Line(x + (linex / 2), y + (liney), x + (recWidth / 2), y + (3 * recHeight)));
            middle.setCoordinates(new Pair<>(x + (recWidth / 2), y + (3 * recHeight)));
            drawNode(middle);
        }
        if ((right != null) && (!right.getType().equals("stmt"))) {
            group.getChildren().add(new Line(x + (linex / 2), y + (liney), x + (3 * recWidth / 2), y + (3 * recHeight / 2)));
            right.setCoordinates(new Pair<>(x + (3 * recWidth / 2), y + (3 * recHeight / 2)));
            drawNode(right);
        }
    }
}
