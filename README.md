# 十胡：從規則到戰術

台灣四色牌「十胡」的專書。先講規則，從胡數表推導整局的戰略，再用電腦對局量每一個戰術決定。規則和數據來自 [tsap-oo](https://github.com/jdh8/tsap-oo)。

## 本機建置

```sh
cargo install mdbook mdbook-replace
mdbook serve --open
```

## 寫作慣例

排版規則和資料的規矩寫在 [CLAUDE.md](CLAUDE.md)。原始檔一段一行；寫作時斷了行，就跑 `python3 cjk.py src/*.md` 把換行接起來，再檢查 diff。
