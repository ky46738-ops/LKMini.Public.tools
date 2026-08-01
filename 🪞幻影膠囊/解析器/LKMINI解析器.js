export class LKMINI解析器 {
  static 內部協議 = "LKMINI://";

  解析內部本體(原文) {
    const 文件 = new DOMParser().parseFromString(原文, "application/xml");
    const 根 = 文件.documentElement;

    if (根.namespaceURI !== LKMINI解析器.內部協議) {
      throw new Error("錯誤：不是 LKMINI 內部本體");
    }

    const 公理 = 根.getElementsByTagNameNS(LKMINI解析器.內部協議, "公理")[0]?.textContent ?? "";
    if (公理.replace(/\s+/g, "") !== "A=A") {
      throw new Error("錯誤：A=A 驗證失敗");
    }

    const 位置 = [...根.getElementsByTagNameNS(LKMINI解析器.內部協議, "位置")];
    const 動作 = [...根.getElementsByTagNameNS(LKMINI解析器.內部協議, "動作")];

    if (位置.length !== 9) throw new Error("錯誤：抽象位置不是九個");
    if (動作.length !== 10) throw new Error("錯誤：抽象動作不是十個");

    return {
      文件,
      根,
      名稱: 根.getElementsByTagNameNS(LKMINI解析器.內部協議, "名稱")[0]?.textContent ?? "",
      定義: 根.getElementsByTagNameNS(LKMINI解析器.內部協議, "定義")[0]?.textContent ?? "",
      公理: "A=A",
      位置,
      動作,
      畫面: 根.getElementsByTagNameNS(LKMINI解析器.內部協議, "畫面")[0] ?? null
    };
  }

  內部顯影(本體, 內部顯影器) {
    return 內部顯影器.顯影(本體);
  }

  對外投影(本體, 外部轉接器) {
    return 外部轉接器.轉換(本體);
  }
}
