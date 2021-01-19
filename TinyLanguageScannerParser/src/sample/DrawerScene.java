/*
 * Copyright (c) 2020. Mohamed Essam Abdelfatah
 */

package sample;

import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class DrawerScene {
    static Stage drawerWindow;

    public void display(Group group) {
        drawerWindow = new Stage();
        drawerWindow.setTitle("Syntax Tree");
        drawerWindow.setScene(new Scene(group, 800, 600));
        drawerWindow.show();
    }
}
