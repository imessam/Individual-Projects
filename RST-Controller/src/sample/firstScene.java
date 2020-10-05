/*
 * Copyright (c) 2020. Mohamed Essam Abdelfatah
 */

package sample;

import com.mathworks.engine.EngineException;
import com.mathworks.engine.MatlabEngine;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;

import java.io.*;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.concurrent.ExecutionException;

public class firstScene {
    private MatlabEngine engine;
    private double[] pz, az, bz; // Arrays of doubles contains A(z), B(z) and P(z) coefficients.

    @FXML
    private TextField tsIN; // GUI input Ts.
    @FXML
    private TextField w0RegIN; // GUI input regulation w0.
    @FXML
    private TextField zetaRegIN; // GUI input regulation zeta.
    @FXML
    private TextField w0TrIN; // GUI input tracking w0.
    @FXML
    private TextField zetaTrIN; // GUI input tracking zeta.
    @FXML
    private TextField pzIN; // GUI output P(z).
    @FXML
    private TextField azIN; // GUI input A(z).
    @FXML
    private TextField bzIN; // GUI input B(z).
    @FXML
    private TextField rIN; // GUI output R(z).
    @FXML
    private TextField sIN; // GUI output S(z).
    @FXML
    private TextField tIN; // GUI output T(z)/
    @FXML
    private Button pzBTN; // GUI button to generate P(z).
    @FXML
    private Button solveBTN; // GUI button to solve the system and generate the RST parameters and C code.


    /*
    Initialize the GUI.
     */
    public void initialize() {

        File dir = new File("logs");
        dir.mkdir();
        PrintStream out = null;
        try {
            out = new PrintStream(new FileOutputStream("logs\\log.txt"));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        System.setOut(out);

        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setContentText("A new log file and a folder named with the current date has been created.\nCheck them for more details");
        engine = startMatlab();
        solveBTN.setDisable(true);
        pzBTN.setOnAction(event -> {

            /*
             * When the pzBTN get pressed it takes regulation w0 and regulation zeta from the input fields and it calls the function updatePZ()
             * which takes the parameters and generate P(z), then it updates P(z) output field with the generated values.
             */

            pzIN.setText(updatePZ());
            solveBTN.setDisable(false);
        });
        solveBTN.setOnAction(event -> {
            alert.show();

            /*
             * When the solve button get pressed it takes A(z) and B(z) from the input fields and convert
             * them to double arrays the passing them along with other parameters to solve() function
             * , then the it calls updateRST() to update the output fields with the RST parameters generated.
             */

            az = convertToDoubleArr(removeBrackets(azIN.getText()).split(" "));
            bz = convertToDoubleArr(removeBrackets(bzIN.getText()).split(" "));
            Object[] rst = solve(Double.parseDouble(w0TrIN.getText()), Double.parseDouble(zetaTrIN.getText())
                    , Double.parseDouble(tsIN.getText()), pz, az, bz);
            updateRST(rst);

        });
    }


    /*
    Start the matlab engine first before calling it.
     */
    private MatlabEngine startMatlab() {
        System.out.println("##Starting Matlab\n");
        MatlabEngine eng = null;
        try {
            eng = MatlabEngine.startMatlab();
        } catch (EngineException | InterruptedException e) {
            e.printStackTrace();
        }
        return eng;
    }


    /*
     Remove brackets from the input fields.
     */
    private String removeBrackets(String s) {
        return s.substring(1, s.length() - 1);
    }


    /*
    Convert the input fields from strings to doubles.
     */
    private double[] convertToDoubleArr(String[] stArr) {
        double[] temp = new double[stArr.length];
        for (int i = 0; i < stArr.length; i++) {
            temp[i] = Double.parseDouble(stArr[i]);
        }
        return temp;
    }


    /*
    Generates P(z) using a matlab script.
     */
    private String updatePZ() {
        System.out.println("##Generating P(z)\n");
        StringBuilder builder = null;
        try {
            builder = new StringBuilder();
            pz = engine.feval("z_polynomial", Double.parseDouble(w0RegIN.getText()),
                    Double.parseDouble(zetaRegIN.getText()), Double.parseDouble(tsIN.getText()));
            builder.append("[ ");
            for (double d :
                    pz) {
                builder.append(BigDecimal.valueOf(d)
                        .setScale(4, RoundingMode.HALF_UP)
                        .doubleValue()).append(" ");
            }
            builder.append("]");
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }
        return builder.toString();
    }


    /* Solve the system and
     generates RST parameters using matlab script.
     */
    private Object[] solve(double w0, double zeta, double ts, double[] pz, double[] az, double[] bz) {
        System.out.println("##Solving the system\n");

        Object[] rst = new Object[0];
        try {
            rst = engine.feval(3, "control", w0, zeta, ts, pz, az, bz);
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }


        return rst;
    }


    /* Returning an array containing strings of each P(z), A(z)
    and B(z) coefficients used to generate *.h file.
    */
    private ArrayList<String> pabArr(double[][] pab) {
        double value;
        int count;
        String[] rstArr = {"P", "A", "B"};
        ArrayList<String> toHeader = new ArrayList<>();
        StringBuilder fileBuilder = new StringBuilder();
        for (int i = 0; i < pab.length; i++) {
            count = 0;
            for (double num :
                    pab[i]) {
                value = BigDecimal.valueOf(num)
                        .setScale(4, RoundingMode.HALF_UP)
                        .doubleValue();

                fileBuilder.append(rstArr[i]).append(count).append(" ").append(value).append("\n");
                toHeader.add(fileBuilder.toString());
                count++;
                fileBuilder.setLength(0);
            }
        }
        return toHeader;
    }


    /* Updating the RST output fields, and calls the createHeaderFile() to
    generate the headers files *.h .
     */
    private void updateRST(Object[] rst) {
        int count;
        double value;
        TextField[] fields = {rIN, sIN, tIN};
        String[] rstArr = {"R", "S", "T"};
        ArrayList<String> rstCoeff = new ArrayList<>();
        StringBuilder builder = new StringBuilder(), fileBuilder = new StringBuilder();
        for (int i = 0; i < rst.length; i++) {
            count = 0;
            builder.setLength(0);
            builder.append("[ ");
            for (double num :
                    (double[]) rst[i]) {
                value = BigDecimal.valueOf(num)
                        .setScale(4, RoundingMode.HALF_UP)
                        .doubleValue();
                builder.append(value);
                builder.append(" ");

                fileBuilder.append(rstArr[i]).append(count).append(" ").append(value).append("\n");
                rstCoeff.add(fileBuilder.toString());
                count++;
                fileBuilder.setLength(0);
            }
            builder.append("]");
            fields[i].setText(builder.toString());
        }
        createHeaderFile(pabArr(new double[][]{pz, az, bz}), "PZA");
        createHeaderFile(rstCoeff, "RST");
    }


    /* Creating the text to be written to
     the header files.
     */
    private void createHeaderFile(ArrayList<String> arr, String fileName) {
        System.out.println("##Creating header files\n");

        StringBuilder builder = new StringBuilder();
        builder.append("#ifndef ").append(fileName).append("_H").append("\n");
        builder.append("#define ").append(fileName).append("_H").append("\n\n");
        for (String s :
                arr) {
            builder.append("#define ").append(s).append("\n");
        }
        builder.append("#endif //").append(fileName).append("_H");
        saveFile(fileName + ".h", builder.toString());
    }


    /* Creating the header files with filename "<filename>.h"
     and the text written to it is "<text>".
     */
    private void saveFile(String fileName, String text) {
        File file = new File(fileName);
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(file))) {
            bw.write(text);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
