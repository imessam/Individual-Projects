/*
 * Copyright (c) 2020. Mohamed Essam Abdelfatah
 */

package sample;

import javafx.util.Pair;

import java.util.ArrayList;

public class Keywords {
    private final ArrayList<Pair<String, String>> KEYWORDS = new ArrayList<>();

    public Keywords() {
        init_keywords();
    }

    private void init_keywords() {
        String[] keywords = new String[]{"WRITE", "READ", "IF", "ELSE", "THEN", "RETURN", "BEGIN", "END", "MAIN", "STRING", "INT", "REAL", "UNTIL", "REPEAT"};
        for (String keyword :
                keywords) {
            KEYWORDS.add(new Pair<>(keyword, keyword.toLowerCase()));
        }
    }

    public ArrayList<Pair<String, String>> getKEYWORDS() {
        return KEYWORDS;
    }

    public Pair<String, String> getKeyword(String key) {
        for (Pair<String, String> keyword :
                KEYWORDS) {
            if (keyword.getKey().equals(key)) {
                return keyword;
            }
        }
        return null;
    }
}
