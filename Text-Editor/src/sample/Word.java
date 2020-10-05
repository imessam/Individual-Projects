/*
 * Copyright (c) 2020. Mohamed Essam Abdelfattah
 */

package sample;

import java.util.ArrayList;

public class Word implements Comparable<Word> {
    private final String word;
    private final ArrayList<PairItem<String, Integer>> wordIndex;

    public Word(String word) {
        this.word = word;
        wordIndex = new ArrayList<>();
    }

    public ArrayList<PairItem<String, Integer>> getWordIndex() {
        return wordIndex;
    }

    public String getWord() {
        return word;
    }

    public void addWordIndex(String filename, int location) {
        if (!locationFound(filename, location)) {
            wordIndex.add(new PairItem<>(filename, location));
        }
    }

    private boolean locationFound(String filename, int location) {
        PairItem<String, Integer> temp = new PairItem<>(filename, location);
        for (PairItem<String, Integer> pair :
                wordIndex) {
            if (pair.equals(temp)) {
                return true;
            }
        }
        return false;
    }

    @Override
    public boolean equals(Object obj) {
        Word temp;
        if (this == obj) {
            return true;
        }
        if (obj instanceof Word) {

            temp = (Word) obj;
            return temp.getWord().equalsIgnoreCase(this.word);
        }
        return false;
    }

    @Override
    public int compareTo(Word o) {
        return this.word.compareTo(o.word);
    }
}

