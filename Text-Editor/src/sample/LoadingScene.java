/*
 * Copyright (c) 2020. Mohamed Essam Abdelfattah
 */

package sample;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.ProgressBar;
import javafx.scene.layout.Pane;
import javafx.stage.Stage;

public class LoadingScene {
    static Stage loadingWindow;
    static double count, size;
    static ProgressBar loadingBar;
    static Label fileName;
    @FXML
    Pane loadingPane;

    public void initialize() {
        count = 1.0;
        loadingBar = new ProgressBar();
        fileName = new Label();
        fileName.setLayoutX(57);
        fileName.setLayoutY(23);
        loadingBar.setLayoutX(57);
        loadingBar.setLayoutY(59);
        loadingPane.getChildren().addAll(fileName, loadingBar);
        if (loadingBar.getProgress() == 1) {
            loadingWindow.close();
        }
    }

    public void setLoadingBar() {
        loadingBar.setProgress(count / LoadingScene.size);
        count++;
    }

    public void setFileName(String fileName) {
        LoadingScene.fileName.setText(fileName);
    }

    public void display(double temp) throws Exception {
        Parent root = FXMLLoader.load(FindScene.class.getResource("loadingScene.fxml"));
        LoadingScene.size = temp;
        loadingWindow = new Stage();
        loadingWindow.setTitle("Loading");
        loadingWindow.setScene(new Scene(root, 421, 135));
        loadingWindow.show();
    }

}
