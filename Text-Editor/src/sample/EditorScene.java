/*
 * Copyright (c) 2020. Mohamed Essam Abdelfattah
 */

package sample;

import javafx.application.Platform;
import javafx.concurrent.Task;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.layout.BorderPane;
import javafx.stage.DirectoryChooser;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.util.Pair;

import java.io.*;


public class EditorScene {
    static Stage window;
    FindScene findScene;
    LoadingScene loadingScene;
    int tabCount = 2;
    Indexer indexer;


    @FXML
    private TabPane tabPane;
    @FXML
    private BorderPane borderPane;
    @FXML
    Label wordLabel;
    @FXML
    ListView<String> documentList;
    @FXML
    ListView<Integer> locationList;

    public static void getStage(Stage temp) {
        window = temp;
    }

    public void initialize() {
        indexer = new Indexer();
        loadingScene = new LoadingScene();
        findScene = new FindScene();
        findScene.setIndexer(indexer);
        findScene.setLabel(wordLabel);
        findScene.setListView(documentList, locationList);
        MenuBar menuBar = new MenuBar();
        Menu fileMenu = new Menu("File");
        Menu editMenu = new Menu("Edit");
        MenuItem save = new MenuItem("Save");
        MenuItem open = new MenuItem("Open");
        MenuItem load = new MenuItem("Load");
        MenuItem findNext = new MenuItem("Find next");
        MenuItem find = new MenuItem("Find");
        MenuItem newFile = new MenuItem("New");
        tabPane.getTabs().add(new Tab("New", new TextArea()));
        tabPane.setTabClosingPolicy(TabPane.TabClosingPolicy.ALL_TABS);
        fileMenu.getItems().addAll(newFile, open, save, load);
        editMenu.getItems().addAll(find, findNext);
        menuBar.getMenus().addAll(fileMenu, editMenu);
        borderPane.setTop(menuBar);


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

        load.setOnAction(event -> {
            File file = new DirectoryChooser().showDialog(window);
            if (file != null) {
                File[] files = file.listFiles((dir, name) -> name.endsWith(".txt"));
                if (files != null) {
                    try {
                        loadingScene.display(files.length);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    Task<Void> task = new Task<>() {
                        @Override
                        protected Void call() {
                            for (File file :
                                    files) {
                                index(loadFile(file));
                            }
                            return null;
                        }
                    };
                    Thread thread = new Thread(task);
                    thread.setDaemon(true);
                    thread.start();
                }
            }
        });

        find.setOnAction(event -> {
            findScene.setIsFindNext(false);
            try {
                findScene.display();
            } catch (Exception e) {
                e.printStackTrace();
            }
        });

        findNext.setOnAction(event -> {

            findScene.setFilename(tabPane.getSelectionModel().getSelectedItem().getText());
            findScene.getTextArea((TextArea) tabPane.getSelectionModel().getSelectedItem().getContent());
            findScene.setIsFindNext(true);
            try {
                findScene.display();
            } catch (Exception e) {
                e.printStackTrace();
            }
        });

        documentList.setOnMouseClicked(event -> {
            if (event.getClickCount() == 2) {
                TextArea textArea = openFile(new File(documentList.getSelectionModel().getSelectedItem()));
                locationList.getSelectionModel().select(documentList.getSelectionModel().getSelectedIndex());
                int loc = locationList.getSelectionModel().getSelectedItem();
                textArea.selectRange(loc, loc + wordLabel.getText().length());
            }

        });

    }

    private void index(Pair<String, String> key) {
        String key1 = key.getKey();
        String value = key.getValue();
        int index, count = 0;

        Platform.runLater(() -> {
            loadingScene.setFileName(value);
            loadingScene.setLoadingBar();
        });
        for (String s1 :
                key1.split("\n")) {
            index = 0;
            for (String s2 :
                    s1.split(" ")) {
                index = s1.indexOf(s2, index);
                indexer.addWord(s2.toLowerCase(), value, index + count);
                index += s2.length() + 1;
            }
            count = s1.length() + 1;
        }
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

    private TextArea openFile(File file) {
        if (file != null) {
            try {
                loadingScene.display(1);
            } catch (Exception e) {
                e.printStackTrace();
            }
            Pair<String, String> temp = loadFile(file);
            addTab(false, temp.getValue());
            TextArea textArea = (TextArea) tabPane.getSelectionModel().getSelectedItem().getContent();
            textArea.setText(temp.getKey());
            tabPane.getSelectionModel().getSelectedItem().setText(temp.getValue());
            index(temp);
            return textArea;
        }
        return null;
    }

    private void saveFile(File file, TextArea textArea) {
        if (file != null) {
            try {
                loadingScene.display(1);
            } catch (Exception e) {
                e.printStackTrace();
            }
            index(saveFile(file, textArea.getText()));
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

    private Pair<String, String> saveFile(File file, String text) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(file))) {
            bw.write(text);
            System.out.println(text);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return new Pair<>(text, file.getPath());
    }
}
