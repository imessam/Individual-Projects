/*
 * Copyright (c) 2020. Mohamed Essam Abdelfattah
 */

package sample;

import java.util.ArrayList;
import java.util.Collections;

public class Indexer {
    private final ArrayList<Word> words;


    public Indexer() {
        words = new ArrayList<>();
    }


    public ArrayList<Word> getWords() {
        return words;
    }

    public void addWord(String text, String filename, int location) {
        Word word = new Word(text);
        int loc;
        if ((loc = findWord(word)) >= 0) {
            words.get(loc).addWordIndex(filename, location);
        } else {
            word.addWordIndex(filename, location);
            words.add(word);
            Collections.sort(words);
        }
    }

    private int findWord(Word word) {
        return Collections.binarySearch(words, word);
    }

}
