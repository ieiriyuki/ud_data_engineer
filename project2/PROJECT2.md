# Project 2 : Cassandra

## メモ

- Cassadra: KVS なせいできちんとプライマリーキーやクラスタリングカラムを指定しないと、where 句とかが使えない
- Primary key -> Cluster columns の順
- where 句を使うときは、primary -> cluster の順で指定しなければならない
- JOIN はできない
