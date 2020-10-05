/*
 * Copyright (c) 2020. Mohamed Essam Abdelfattah
 */

package sample;

public class PairItem<T, K> {

    private final T Key;
    private K Value;

    public PairItem(T key, K value) {
        Key = key;
        Value = value;
    }

    public T getKey() {
        return Key;
    }

    public K getValue() {
        return Value;
    }

    public void updateValue(K newValue) {
        Value = newValue;
    }

    @Override
    public boolean equals(Object obj) {
        PairItem temp;
        if (this == obj) {
            return true;
        }
        if (obj instanceof PairItem) {

            temp = (PairItem) obj;
            return (temp.getKey().equals(this.Key)) && (temp.getValue() == (this.Value));
        }

        return false;
    }


}
