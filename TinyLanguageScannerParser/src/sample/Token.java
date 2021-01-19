/*
 * Copyright (c) 2020. Mohamed Essam Abdelfatah
 */

package sample;

import javafx.util.Pair;


public class Token {
    private final Pair<String, String> token;

    public Token(Pair<String, String> token) {
        this.token = token;
    }

    public Pair<String, String> getToken() {
        return token;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Token token1 = (Token) o;
        return (this.token.getKey().equals(token1.getToken().getKey()));
    }

}
