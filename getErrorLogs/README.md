# getErrorLog
後でREADMEは更新する


## Usage
### 初回ダウンロード時
1. Config設定
2. UserConfig設定

### Log収集開始時
1. dataフォルダ作成
2. srcフォルダに移動
3. コマンド実行
```python
python getErrorLog.py --init --app {APP名} 
```

### Log更新時 ※随時
1. srcフォルダに移動
2. コマンド実行
```python
※単体
python getErrorLog.py --update --app {APP名} 
※まとめて
python getErrorLog.py -d
```

### Log更新時 ※定期実行(batファイルをスケジューリング実行)
1. スケジュール設定
2. 後は頑張る