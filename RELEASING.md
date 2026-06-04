# リリース手順

本リポジトリは、`v*` タグの push を契機に GitHub Actions が起動し、
PyPI の **Trusted Publishing (OIDC)** を用いてパッケージを公開します。
API トークンをシークレットとして保持する必要はありません。

## 前提

- PyPI 側で本プロジェクトの Trusted Publisher（GitHub Actions / 対象リポジトリ /
  リリースワークフロー / 環境名）が設定済みであること。
- メインブランチが公開対象の状態でグリーン（テストが通っている）であること。

## リリースの流れ

### 1. バージョンを更新する

バージョンは `pylogiless/pylogiless/__init__.py` の `__version__` を単一の真実とし、
`pyproject.toml` は `dynamic = ["version"]` でここを参照します。

```python
# pylogiless/pylogiless/__init__.py
__version__ = "0.3.0"
```

新しいリリース番号（[セマンティックバージョニング](https://semver.org/lang/ja/)に従う）へ更新します。

### 2. CHANGELOG を更新する

`CHANGELOG.md` の先頭に、新しいバージョンの見出しと変更点を追記します。

```markdown
## [0.3.0] - 2026-06-04

### 追加
- ...
```

### 3. 変更をコミットしてメインに反映する

```bash
git add pylogiless/pylogiless/__init__.py CHANGELOG.md
git commit -m "chore: release 0.3.0"
git push origin main
```

### 4. テストを確認する

リポジトリ直下で実行します。

```bash
python3 -m pytest -q
```

### 5. タグを付けて push する

`__version__` と一致する `v` プレフィックス付きのタグを作成し、push します。
この push が公開ワークフローのトリガになります。

```bash
git tag v0.3.0
git push origin v0.3.0
```

### 6. 公開を確認する

- GitHub Actions のリリースワークフローが成功していることを確認します。
- [PyPI のプロジェクトページ](https://pypi.org/project/pylogiless/) に
  新しいバージョンが表示されることを確認します。

## チェックリスト

- [ ] `pylogiless/pylogiless/__init__.py` の `__version__` を更新した
- [ ] `CHANGELOG.md` に新バージョンのエントリを追加した
- [ ] テスト（`python3 -m pytest -q`）が通っている
- [ ] 変更を main に push した
- [ ] `vX.Y.Z` タグを push した
- [ ] GitHub Actions のリリースが成功した
- [ ] PyPI に新バージョンが公開された
