/* Alpine component เล็ก ๆ ของหน้าเว็บ  [ผู้รับผิดชอบ: คนที่ 6 / Frontend]
 *
 * งานหนักทั้งหมดอยู่ฝั่ง server แล้ว (HTMX คืน HTML มาให้เลย)
 * ไฟล์นี้เก็บเฉพาะ state ที่เป็นเรื่องของ UI ล้วน ๆ
 */
function maskApp() {
  return {
    // TODO(คนที่ 6): เพิ่ม state เช่น โหมด "เทียบก่อน/หลัง", นับตัวอักษร
    charCount: 0,
  };
}

document.addEventListener("alpine:init", () => {
  window.maskApp = maskApp;
});

// ตัวอย่าง hook ของ HTMX เผื่อต้องทำอะไรหลังผลลัพธ์กลับมา
document.body?.addEventListener("htmx:afterSwap", (event) => {
  if (event.detail.target.id === "result") {
    // TODO(คนที่ 6): scroll ไปที่ผลลัพธ์บนจอมือถือ
  }
});
