# Lesson 1: Introduction to Data Modeling

*RDB も NoSQL も GCP と AWS の資格の時にやったよ...*

## 内容
RDBMS の話

- ACID とか
- RDBMS を使うべきとき
  - トランザクションが必要
- RDBMS を使うべきでないとき
  - データが大きいとき
  - データのフォーマットが様々な時
  - 高いスループットが必要なとき
  - 柔軟なスキーマが必要な時
  - 高い可用性が必要な時
  - 水平分散が必要な時

### PostgreSQL

Redshift 使うから紹介しているのだろう

クラウドサーバーの Jupyter Notebook から psycopg2 を使って、
PostgreSQL に接続して、DB の作成、テーブルの作成、インサート、セレクトを行った。

- `create table name` の `name` に DB 名を入れてしまった。ケアレス
- Hive 使っていたので、PostgreSQL では `string` 型ではなく `text` 型なの知らなかった

### NoSQL Database

Cassandra 使うよ。
Cassandra は Facebook 発の NoSQL DB で、今は Apache が取りまとめている。

NoSQL = Not Only SQL

- Cassandra: Partition Row store
- Mongo DB: Document store
  - v4.0 から ACID トランザクションを実行できるらしい
- Dynamo DB: KeyValue store
- HBase: wide Column Store
- Neo4J: Graph Database

~~Bigtable 涙目~~

#### Cassandra

- Partition に分かれる
- Primary Key が Partition を分ける
- Cluster Key で Partition 内のユニークを取得する

利用例

- Uber がバックエンドで使っている
- Netflix がビデオの配信に使っている
- リテールやヘルスケアでのトランザクションログ
- IoT
- 時系列データ
- 書き込み重視なワークロード

アドホックな集計には向かない。よく実行するクエリに合わせてモデリングする。

**Jupyter Notebook を使ったデモ**

1. DB をつくる
1. テーブルを作る
1. インサートする
1. セレクトする

アーティストでクエリする要件があったのに、実装していなかった。反省

最後のセレクト文で、クエリ末尾に `allow filtering` つけろって怒られた
