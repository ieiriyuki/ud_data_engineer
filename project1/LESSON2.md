# Lesson 2: Relational Data Models

Normalize: 正規化

第一から第四まである。詳細は忘れた。まあイメージは分かるし。

## Exercise 1

正規化されたテーブルを作る。

なんかちがうっぽい。
なにが違うかは知らない。

ちゃんとユニークになっていない模様。

## Denormalize

JOIN が重いから、非正規化する

## Fact & Dimension

Star Scheme: ファクトテーブルにディメンションを紐づけるモデル
一つのテーブルに複数のテーブルが紐づく

Snowflake Scheme: ファクトテーブルにディメンションを広げていくモデル
ディメンションの先にさらにディメンションを紐づけていく
