/*
 * Copyright (c) 2020. Mohamed Essam Abdelfattah
 */

package sample;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.stage.Stage;

import java.util.ArrayList;


public class FindScene {

    static String filename;
    static PairItem<Integer, Integer> location;
    private static Stage findWindow;
    private static Indexer indexer;
    private static TextArea textArea;
    private static Label label;
    private static ListView<String> listView;
    private static ListView<Integer> listView2;
    private static boolean isFindNext;
    int i = 0;
    ArrayList<PairItem<String, Integer>> wordIndex;
    String text = " ";

    public void setIsFindNext(boolean isFindNext) {
        FindScene.isFindNext = isFindNext;
    }

    @FXML
    TextField wordFind;
    @FXML
    Button findBTN;

    public void display() throws Exception {
        Parent root = FXMLLoader.load(FindScene.class.getResource("findScene.fxml"));
        findWindow = new Stage();
        findWindow.setTitle("Find");
        findWindow.setScene(new Scene(root, 313, 131));
        findWindow.showAndWait();
    }

    public void initialize() {
        if (isFindNext) {
            findBTN.setText("Find next");
        } else {
            findBTN.setText("Find");
        }
        Node n1 = listView.lookup(".scroll-bar");
        if (n1 instanceof ScrollBar) {
            final ScrollBar bar1 = (ScrollBar) n1;
            Node n2 = listView2.lookup(".scroll-bar");
            if (n2 instanceof ScrollBar) {
                final ScrollBar bar2 = (ScrollBar) n2;
                bar1.valueProperty().bindBidirectional(bar2.valueProperty());
            }
        }


        location = new PairItem<>(-1, -1);
        findBTN.setOnAction(event -> findNext());
    }

    public void setIndexer(Indexer temp) {
        FindScene.indexer = temp;
    }

    public void setFilename(String filename) {
        if (!filename.equals(" ")) {
            FindScene.filename = filename;
        }
    }

    public void getTextArea(TextArea content) {
        FindScene.textArea = content;
    }

    public void setLabel(Label label) {
        FindScene.label = label;
    }


    public void setListView(ListView<String> listView1, ListView<Integer> listView2) {
        FindScene.listView = listView1;
        FindScene.listView2 = listView2;
    }

    private void findNext() {
        if (isFindNext) {
            if (!(text.equals(wordFind.getText()))) {
                text = wordFind.getText();
                i = 0;
                for (Word temp :
                        indexer.getWords()) {
                    if (temp.getWord().equals(text)) {
                        wordIndex = temp.getWordIndex();
                        break;
                    }
                }
            }
            for (; i < wordIndex.size(); i++) {
                if (wordIndex.get(i).getKey().equals(filename)) {
                    location = new PairItem<>(wordIndex.get(i).getValue(), wordIndex.get(i).getValue() + text.length());
                    i++;
                    break;
                }
            }
            textArea.selectRange(location.getKey(), location.getValue());
        } else {
            listView.getItems().clear();
            listView2.getItems().clear();
            text = wordFind.getText();
            label.setText(text);
            for (Word temp :
                    indexer.getWords()) {
                if (temp.getWord().equals(text)) {
                    wordIndex = temp.getWordIndex();
                    break;
                }
            }
            for (PairItem<String, Integer> pair :
                    wordIndex) {
                listView.getItems().add(pair.getKey());
                listView2.getItems().add(pair.getValue());
            }
            findWindow.close();
        }
    }


}
