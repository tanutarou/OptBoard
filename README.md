# OptBoard
A web-based dashboard for parameters optimization

機械学習手法や最適化手法のパラメータチューニングを助けるツール。

- 実行時のパラメータとその時の評価値の管理
- パラメータの変化に対する評価値の変化をプロットやヒートマップで可視化
- localでの利用を想定

![main](https://user-images.githubusercontent.com/7645600/29746826-8f7844e6-8b21-11e7-8d99-93fc7e483849.png)

# Usage
1. 右上にある[New Project]を押してプロジェクトを作成する
2. 作成したプロジェクト右にある[Open]によりプロジェクトを開く
3. Solver(実行するプログラム)がないと始まらないので、上部のナビゲータから[Solver]を押してSolverを登録する
4. Homeに戻り、parameterのところに実行したいパラメータを入力(数字, list, rangeが利用可)し、[Run]を押すとプログラムが実行され、結果が下の一覧に登録される。
5. [Sort]や[Analysis1D], [Analysis2D]を利用してどのパラメータが強い影響を持っているか調べる

## Solverの登録
- Solverはコマンドライン引数でパラメータをとるような形式のプログラムで作成すること
- 出力の最終行の実数値が評価値として判断される
- (Solverは現状1ファイルしか対応していない)

SolverのParams infoはパラメータの情報を登録する部分で、pythonの辞書形式で登録を行う(正確に書くこと!)
```
{"パラメータ1の名前":"パラメータ1の説明", "パラメータ2の名前":"パラメータ2の説明"}
```

## Analysis1D
ある１つのパラメータに対する評価値のグラフを作成する

![analysis1d](https://user-images.githubusercontent.com/7645600/29746832-bf0756b6-8b21-11e7-9eb7-b7f6e029fa43.png)

## Analysis2D
2つのパラメータに対する評価値をヒートマップで表示

![analysis2d](https://user-images.githubusercontent.com/7645600/29746834-d440b1a8-8b21-11e7-9c83-10ab32d1395e.png)
