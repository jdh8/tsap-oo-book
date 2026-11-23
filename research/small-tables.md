# 兩人與三人的規則

查核日期：2026-11-16。問題：十胡有沒有兩人、三人的成文規則，人數少的時候規則改了什麼。

## 各來源的記載

| 來源 | 人數 | 發牌 | 人數少時改了什麼 |
| --- | --- | --- | --- |
| [中文維基〈十胡〉][zhwiki-shihu] | 「可供2人到6人遊戲」 | 「2~5人遊戲時，莊家摸二十一張，閒家摸二十張。6人遊戲時，莊家摸十六張牌，閒家摸十五張。」 | 沒寫。只寫「五人以上稱為五龍，所有賭注（台與底）變為兩倍」，五龍沒有 6 張廢牌 |
| [中文維基〈四色牌〉][zhwiki-sisepai] | 沒寫 | 沒寫 | |
| [國史館臺灣文獻館][thgov] | 「牌搭是二至四人」 | 「依照玩牌人數發牌數量以莊家比其他人多一支為原則」，沒給張數 | 沒寫 |
| [國瑜企業社][guoyu]（牌具廠商） | 四人玩法、五人玩法 | 「一人發20支牌，頭家發20支」（原文如此） | 五人：8 胡以上可胡，牌不好可以放棄。沒有二、三人 |
| [遊戲基地〈四色牌十胡篇〉][gamebase]（存檔） | 「四人版」 | 每人 20 張，莊家 21 張 | 只有四人 |
| Board Game Arena：[中文說明][bga-zh]、[英文說明][bga-en]、[遊戲頁][bga-panel] | 2 至 4 人；遊戲頁的資料是 `player_numbers` [2,3,4]、預設 2 人、排位（arena）2 人 | 每人 7 + 7 + 6 = 20 張，先手 21 張 | 說明頁沒有任何依人數變動的規則 |
| [pagat.com][pagat] | 沒寫 | 沒寫，轉介下面兩頁 | |
| [Wei-Hwa Huang][huang]（存檔） | 「anywhere from 2 to 4 people」；人多時（甚至四人）牌不夠，常減少手牌或混入更多副牌 | 每人 20 張 | 沒寫 |
| [tnt（CMU）][tnt] | 通常四人，有時三人，「只有兩個人玩相當無趣」 | 莊家 21，其餘 20 | 沒寫 |
| [英文維基][enwiki] | 資訊框：4 人（標準牌組有 2 到 3 人的變體）；內文：標準四人，兩人或三人也能玩；超過四人每多一人加一組 28 張 | 20 張，莊家 21 | 沒寫 |
| [越南文維基〈Tứ sắc〉][viwiki] | 適合四人，但兩人或三人都能玩 | 每人 20 張，莊家第一輪多拿一張 | 沒寫。另記順化有一種用同一副牌的三人玩法 bài xệp，是另一種遊戲 |
| [Vinagames Tứ Sắc][vina] | 「for 2-4 people and it is best to play the game with 4 people」 | 每人 20，先手 21 | 沒寫。輸家各自付給贏家 |

## 結論

- **兩人與三人「可以玩」有多個獨立來源**：中文維基、國史館、BGA、Huang、英文與越南文維基、Vinagames。
- **沒有任何來源寫出兩人或三人的規則調整**。發牌一律是每人 20 張、莊家 21 張。中文維基的「2~5 人各 20 張」在五人時只剩 112 − 101 = 11 張牌堆，與同一段「五龍因剩餘牌堆張數較少」的說法一致，但沒有引註。
- **BGA 是唯一可操作的兩人規格，而且它的排位賽就是兩人**。它的規則與人數無關：手裡打出的牌只有下家能吃，摸出的牌是摸牌者與下家都能吃，胡、槓、碰不限座位，達到 10 胡的贏家「跟所有其他玩家收取」。兩個語言版本的收分寫法不同：中文是每家收「胡數減去門檻」，英文是「超過門檻的胡數，加上每家 1 分」。[中文][bga-zh]、[英文][bga-en]
- **把這套規則套到兩人，遊戲會變**。以下是從規則推出來的，來源沒有這樣說。兩人時唯一的對手同時是上家與下家，所以每一張打出的牌、每一張摸出的牌雙方都能吃，吃的座位限制實際上消失。牌堆是 112 − 41 = 71 張，不是四人時的 31 張。贏家只向一家收，輸家付全部，放槍與被自摸的代價相同。
- 開源遊戲 chunhua1972/four-color-game 的規則裡，2 到 4 人同樣發 20／21 張，5、6 人改成 16／17 與 14／15 張。它的文件明說後者是自訂的擴充，不宣稱是傳統規則。[DEVplan.md §3.2][fcg-plan]
- **放槍要不要多賠，各地不同**。tnt 記的賭法裡，放槍的人有時要替另外兩家付。Vinagames 的規則是沒有打出「最差的牌」而放槍的人，替其他輸家付。本書和 tsap-oo 的規則是放槍不多賠。[tnt][tnt]、[Vinagames][vina]

[zhwiki-shihu]: https://zh.wikipedia.org/wiki/%E5%8D%81%E8%83%A1
[zhwiki-sisepai]: https://zh.wikipedia.org/wiki/%E5%9B%9B%E8%89%B2%E7%89%8C
[thgov]: https://dict.th.gov.tw/Print.aspx?ID=2186
[guoyu]: https://www.guoyu.com.tw/zh/qa/1.html
[gamebase]: https://web.archive.org/web/20131005012051/http://www.gamebase.com.tw/wekey/%E5%A4%A7%E8%95%83%E8%96%AF%E9%81%8A%E6%88%B2%E7%B6%B2%E6%88%B0/%E5%9B%9B%E8%89%B2%E7%89%8C%E5%8D%81%E8%83%A1%E7%AF%87/
[bga-zh]: https://zh.doc.boardgamearena.com/Gamehelpfourcolorcards
[bga-en]: https://en.boardgamearena.com/doc/Gamehelpfourcolorcards
[bga-panel]: https://en.boardgamearena.com/gamepanel?game=fourcolorcards
[pagat]: https://www.pagat.com/rummy/si_se_pai.html
[huang]: https://web.archive.org/web/20081210050742/www.ofb.net/~whuang/ugcs/gp/ssp/
[tnt]: https://www.cs.cmu.edu/~tnt/rules.html
[enwiki]: https://en.wikipedia.org/wiki/Four_color_cards
[viwiki]: https://vi.wikipedia.org/wiki/T%E1%BB%A9_s%E1%BA%AFc
[vina]: https://www.vinagames.com/tusac.html
[fcg-plan]: https://github.com/chunhua1972/four-color-game/blob/main/DEVplan.md
