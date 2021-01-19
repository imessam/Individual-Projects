/*
 * Copyright (c) 2020. Mohamed Essam Abdelfatah
 */

package sample;

import javafx.fxml.FXML;
import javafx.scene.Group;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.util.Pair;

import java.io.*;


public class EditorScene {
    static Stage window;
    int tabCount = 2;
    private Alert alert;
    private Keywords keywords;
    private Operators operators;
    private Scanner scanner;
    private Parser parser;
    private SyntaxTree syntaxTree;
    private Drawer drawer;
    private DrawerScene drawerScene;


    @FXML
    private TabPane tabPane;
    @FXML
    private BorderPane borderPane;


    public static void getStage(Stage temp) {
        window = temp;
    }

    public void initialize() {

        VBox vBox = new VBox();
        MenuBar menuBar = new MenuBar();
        ToolBar toolBar = new ToolBar();
        Menu fileMenu = new Menu("File");
        MenuItem save = new MenuItem("Save");
        MenuItem open = new MenuItem("Open");
        MenuItem newFile = new MenuItem("New");
        Button scan = new Button();
        Button parse = new Button();
        Image scanImg = new Image(getClass().getResourceAsStream("scan.png"));
        Image parseImg = new Image(getClass().getResourceAsStream("parsing.png"));

        keywords = new Keywords();
        operators = new Operators();
        scanner = new Scanner();
        parser = new Parser();
        drawer = new Drawer();
        drawerScene = new DrawerScene();
        scanner.setKEYWORDS(keywords.getKEYWORDS());
        scanner.setOPERATORS(operators.getOPERATORS());
        parser.setKeywords(keywords);
        parser.setOperators(operators);

        scan.setGraphic(new ImageView(scanImg));
        parse.setGraphic(new ImageView(parseImg));
        tabPane.getTabs().add(new Tab("New", new TextArea()));
        tabPane.setTabClosingPolicy(TabPane.TabClosingPolicy.ALL_TABS);
        fileMenu.getItems().addAll(newFile, open, save);
        menuBar.getMenus().addAll(fileMenu);
        toolBar.getItems().addAll(scan, parse);
        vBox.getChildren().addAll(menuBar, toolBar);
        borderPane.setTop(vBox);


        newFile.setOnAction(event -> addTab(true, null));

        open.setOnAction(event -> {
            FileChooser fileChooser = new FileChooser();
            fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("Text file", "*.txt"));
            File file = fileChooser.showOpenDialog(window);
            openFile(file);
        });

        save.setOnAction(event -> {
            FileChooser fileChooser = new FileChooser();
            fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("Text file", "*.txt"));
            fileChooser.setInitialFileName(tabPane.getSelectionModel().getSelectedItem().getText());
            TextArea textArea = (TextArea) tabPane.getSelectionModel().getSelectedItem().getContent();
            File file = fileChooser.showSaveDialog(window);
            saveFile(file, textArea);
        });

        scan.setOnAction(event -> {
            TextArea textArea = (TextArea) tabPane.getSelectionModel().getSelectedItem().getContent();
            FileChooser fileChooser = new FileChooser();
            fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("Text file", "*.txt"));
            fileChooser.setInitialFileName(tabPane.getSelectionModel().getSelectedItem().getText());
            File file = fileChooser.showSaveDialog(window);
            saveFile(file, scanner.scan(textArea.getText()));
        });


        parse.setOnAction(event -> {
            Pair<SyntaxTree, Boolean> temp;
            parser.setTOKENS(scanner.getTOKENS());
            if ((temp = parser.parse()).getValue()) {
                alert = new Alert(Alert.AlertType.INFORMATION);
                alert.setTitle("Parsing");
                alert.setHeaderText("Parsed successfully.");
                syntaxTree = temp.getKey();
                Group group = drawer.drawSyntaxTree(syntaxTree);
                drawerScene.display(group);
            } else {
                alert = new Alert(Alert.AlertType.ERROR);
                alert.setTitle("Parsing");
                alert.setHeaderText("Parsing error, incorrect syntax!");
            }
            alert.setContentText(null);
            alert.showAndWait();
        });
    }

    private void addTab(boolean isNew, String name) {
        Tab tab;
        boolean found = false;
        if (isNew) {
            tab = new Tab("New " + tabCount, new TextArea());
            tabPane.getTabs().add(tab);
            tabPane.getSelectionModel().select(tab);
            tabCount++;
        } else {
            for (Tab temp : tabPane.getTabs()) {
                if (temp.getText().equals(name)) {
                    found = true;
                    tabPane.getSelectionModel().select(temp);
                    break;
                }
            }
            if (!found) {
                tab = new Tab("New " + tabCount, new TextArea());
                tabPane.getTabs().add(tab);
                tabPane.getSelectionModel().select(tab);
            }
        }
    }

    private void openFile(File file) {
        if (file != null) {
            Pair<String, String> temp = loadFile(file);
            addTab(false, temp.getValue());
            TextArea textArea = (TextArea) tabPane.getSelectionModel().getSelectedItem().getContent();
            textArea.setText(temp.getKey());
            tabPane.getSelectionModel().getSelectedItem().setText(temp.getValue());
        }
    }

    private void saveFile(File file, TextArea textArea) {
        if (file != null) {
            saveFile(file, textArea.getText());
            tabPane.getSelectionModel().getSelectedItem().setText(file.getPath());
        }


    }

    private Pair<String, String> loadFile(File file) {
        String line;
        StringBuilder s = new StringBuilder();
        try {
            if (file.exists()) {
                try (BufferedReader bw = new BufferedReader(new FileReader(file))) {
                    while ((line = bw.readLine()) != null) {
                        s.append(line);
                        s.append("\n");
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        } catch (NullPointerException e) {
            e.printStackTrace();
        }
        return new Pair<>(s.toString(), file.getPath());
    }

    private void saveFile(File file, String text) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(file))) {
            bw.write(text);
            System.out.println(text);
        } catch (IOException e) {
            e.printStackTrace();
        }
        new Pair<>(text, file.getPath());
    }

}
