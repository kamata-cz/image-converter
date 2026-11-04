(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- ダミーのデータ（ブログの月・記事ごとのフォルダ。個人情報なし） ----
  var folders = ['2026-08/hokkaido-roadtrip', '2026-09/cafe-meguri', '2026-09/kyoto-momiji-mae', '2026-10/home-baking', '2026-10/camp-gear-review', '2026-11/autumn-walk'];
  var counts = [24, 18, 30, 16, 22, 18]; // 合計 128
  var files = [];
  folders.forEach(function (f, fi) {
    for (var i = 1; i <= counts[fi]; i++) {
      var name = 'IMG_' + String(4000 + fi * 100 + i) + '.jpg';
      if (fi === 2 && i === 7) name = 'momiji-light-up-at-night-kiyomizu-dera-sannenzaka-ninenzaka-long-exposure-tripod-version-final.jpg';
      var before = 2.4 + ((fi * 7 + i * 13) % 37) / 10; // 2.4〜6.0 MB
      files.push({ path: 'blog-images/' + f + '/', name: name, before: before, w: 4032, h: 3024, status: 'wait' });
    }
  });
  files[37].name = 'IMG_4212.HEIC'; files[37].heic = true;          // 読めない形式（Chromium・Firefox）
  files[90].name = 'chart-screenshot.png'; files[90].png = true;     // 目標を超過しやすい画像
  var TOTAL = files.length, EXCLUDED = 3, FOLDERS = folders.length;

  var st = { state: 'empty', done: 0, timer: null, filter: false, fmt: 'webp', safari: false, stopped: false };

  // ---- 表示の部品 ----
  function mb(x) { return x >= 1 ? x.toFixed(1) + ' MB' : Math.round(x * 1024) + ' KB'; }
  function setBtn(id, on, hintId, hint) {
    var b = $(id); b.disabled = !on;
    if (hintId) { $(hintId).textContent = hint; }
  }
  function toast(msg) {
    var t = $('toast'); $('toast-msg').textContent = msg; t.classList.add('on');
    clearTimeout(toast.h); toast.h = setTimeout(function () { t.classList.remove('on'); }, 4000);
  }
  function live(msg) { $('live').textContent = msg; }

  function finish(f) {
    var target = Number($('target').value) || 300;
    if (f.heic) { f.status = 'bad'; f.why = 'このブラウザは HEIC を読めません。Safari で開くか、JPEG に書き出してから入れてください'; return; }
    if (f.png && !f.retried) { f.status = 'over'; f.after = (target + 112) / 1024; f.why = '画質を最小にしても ' + (target + 112) + ' KB。長い辺を小さくするか、目標を上げてください'; return; }
    f.status = 'ok'; f.after = (target * (0.62 + ((f.before * 10) % 30) / 100)) / 1024; f.w2 = 1600; f.h2 = 1200; f.why = '';
  }
  function statusCell(f) {
    if (f.status === 'ok') return '<span class="Label Label--success">完了</span>';
    if (f.status === 'over') return '<span class="st"><span class="Label Label--attention">目標を超過</span><span class="why">' + f.why + '</span></span>';
    if (f.status === 'bad') return '<span class="st"><span class="Label Label--danger">読めない形式</span><span class="why">' + f.why + '</span></span>';
    if (f.status === 'skip') return '<span class="Label">未処理（中止）</span>';
    return '<span class="Label">待機中</span>';
  }
  function row(f, fresh) {
    var size = f.after ? mb(f.before) + ' → ' + mb(f.after) : (f.status === 'bad' ? mb(f.before) + ' → —' : mb(f.before));
    var dim = f.status === 'ok' ? f.w2 + '×' + f.h2 : (f.status === 'over' ? '1600×1200' : '—');
    return '<tr role="row"' + (fresh ? ' class="fresh"' : '') + '><td role="cell"><span class="path">' + f.path + '</span>' + f.name + '</td><td role="cell" class="num">' + size +
      '</td><td role="cell" class="num">' + dim + '</td><td role="cell">' + statusCell(f) + '</td></tr>';
  }
  function flagged() { return files.filter(function (f) { return f.status === 'over' || f.status === 'bad'; }); }

  function renderRows(freshIndex) {
    var list = st.state === 'empty' ? [] : files;
    if (st.filter) list = flagged();
    $('rows').innerHTML = list.map(function (f, i) { return row(f, i === freshIndex); }).join('');
    $('blank').hidden = list.length > 0;
    $('list-count').textContent = String(list.length);
  }

  function renderSums() {
    var e = st.state === 'empty';
    var processed = files.filter(function (f) { return f.status === 'ok' || f.status === 'over'; }).length;
    var before = files.reduce(function (a, f) { return a + f.before; }, 0);
    var after = files.reduce(function (a, f) { return a + (f.after || 0); }, 0);
    var fl = flagged().length;
    $('v-count').textContent = e ? '—' : processed + ' / ' + TOTAL;
    $('s-count').textContent = e ? '画像を入れると数えます' : '対象外 ' + EXCLUDED + ' 件（画像以外）・フォルダ ' + FOLDERS + ' 個';
    $('v-size').textContent = e ? '—' : (after ? mb(before) + ' → ' + mb(after) : mb(before));
    $('s-size').textContent = e || !after ? '' : '約 ' + Math.round((1 - after / before) * 100) + '% 軽くなりました（処理した分）';
    $('v-flag').textContent = e ? '—' : String(fl);
    $('v-flag').classList.toggle('has', fl > 0);
    var pct = Math.round(st.done / TOTAL * 100);
    $('pbar-fill').style.width = pct + '%';
    $('pbar').setAttribute('aria-valuenow', String(pct));
    $('prog-pct').textContent = e ? '' : st.done + ' / ' + TOTAL;
  }

  function renderControls() {
    var s = st.state, fl = flagged().length;
    var running = s === 'processing';
    var hasResult = s === 'done';
    // 入れる場所
    $('drop-title').textContent = s === 'empty' ? 'フォルダをここにドロップ' : 'blog-images/ を読み込みました（' + TOTAL + ' 枚・フォルダ ' + FOLDERS + ' 個）';
    $('drop-meta').textContent = s === 'empty' ? '下の階層のフォルダまで読み込みます。数枚の画像だけでも使えます。' : '別のフォルダを入れると、今の一覧と入れ替わります。';
    $('pick-folder').disabled = running; $('pick-files').disabled = running;
    // 実行ボタン（位置は同じまま、文言と色だけ変える）
    var run = $('run');
    run.classList.toggle('btn--primary', s === 'loaded' || s === 'safari');
    run.disabled = s === 'empty';
    $('run-ic').setAttribute('href', running ? '#i-stop' : (hasResult ? '#i-sync' : '#i-play'));
    $('run-label').textContent = running ? '中止する' : (st.stopped ? '続きから始める' : (hasResult ? '同じ設定でもう一度' : '軽量化を始める'));
    $('run-hint').textContent = s === 'empty' ? '画像を入れると始められます' : (running ? '中止しても、終わった分は保存できます' : '');
    $('prog-text').textContent = s === 'empty' ? 'まだ画像がありません' : (running ? '処理しています' : (hasResult ? (st.stopped ? '中止しました' : 'すべて処理しました') : '始める準備ができました'));
    // 一覧の絞り込み
    $('filter').disabled = !hasResult;
    $('filter').setAttribute('aria-pressed', String(st.filter));
    $('filter-hint').textContent = hasResult ? (fl ? '要確認 ' + fl + ' 件' : '要確認はありません') : '処理を始めると使えます';
    $('foot-left').textContent = s === 'empty' ? '画像を入れると、ここに件数が出ます' : '表示 ' + $('list-count').textContent + ' 件 / 全 ' + TOTAL + ' 件';
    $('foot-right').textContent = hasResult ? 'ZIP は 500MB ごとに分けます（今回は 1 つ）' : '';
    // 右の列
    setBtn('zip', hasResult, 'zip-hint', s === 'empty' ? '画像を入れると保存できます' : (running ? '処理が終わると保存できます' : (hasResult ? '元と同じフォルダ構成で保存します' : '処理を始めると保存できます')));
    setBtn('redo', hasResult && fl > 0, 'redo-hint', hasResult ? (fl ? '要確認の ' + fl + ' 件だけ、今の設定で処理し直します' : '要確認はありません') : '要確認が出たときに使えます');
    setBtn('csv', hasResult, 'csv-hint', hasResult ? '結果の一覧を Excel で開ける形で保存します' : (s === 'empty' ? '画像を入れると書き出せます' : '処理が終わると書き出せます'));
    ['edge', 'target'].forEach(function (id) { $(id).disabled = running; });
    // 形式（Safari では WebP を選べない）
    Array.prototype.forEach.call(document.querySelectorAll('#fmt-seg button'), function (b) {
      var f = b.getAttribute('data-fmt');
      b.disabled = running || (st.safari && f === 'webp');
      b.setAttribute('aria-pressed', String(st.fmt === f));
    });
    var fh = $('fmt-hint');
    fh.classList.toggle('warn', st.safari);
    fh.textContent = st.safari ? 'Safari では WebP を作れないため、JPEG か PNG を選んでください'
      : ({ webp: 'いちばん軽くなります。ブログで広く使えます', jpeg: '写真向き。どこでも使えます', png: '図や文字の画像向き。写真は重くなります' })[st.fmt];
  }

  function render(freshIndex) { renderRows(freshIndex); renderSums(); renderControls(); }

  // ---- 状態の切り替え ----
  function reset() { clearInterval(st.timer); st.done = 0; st.filter = false; st.stopped = false; files.forEach(function (f) { f.status = 'wait'; f.after = 0; f.retried = false; }); }
  function setState(s) {
    reset();
    st.safari = s === 'safari'; st.fmt = st.safari ? 'jpeg' : 'webp';
    st.state = s === 'safari' ? 'loaded' : s;
    if (s === 'done') { files.forEach(finish); st.done = TOTAL; }
    if (s === 'processing') { start(); return; }
    Array.prototype.forEach.call(document.querySelectorAll('#demo-seg button'), function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-state') === s)); });
    render();
  }
  function markDemo(s) { Array.prototype.forEach.call(document.querySelectorAll('#demo-seg button'), function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-state') === s)); }); }

  function start() {
    st.state = 'processing'; st.stopped = false; markDemo('processing'); render(); live('処理を始めました');
    var step = reduce ? TOTAL : 2;
    st.timer = setInterval(function () {
      for (var k = 0; k < step && st.done < TOTAL; k++) { finish(files[st.done]); st.done++; }
      renderSums(); renderRows(st.done - 1);
      var sc = $('list-scroll'); if (!st.filter) sc.scrollTop = sc.scrollHeight;
      if (st.done % 32 === 0) live(st.done + ' / ' + TOTAL + ' 枚を処理しました');
      if (st.done >= TOTAL) { clearInterval(st.timer); st.state = 'done'; markDemo('done'); render(); live('すべて処理しました。要確認 ' + flagged().length + ' 件'); }
    }, 60);
  }
  function stop() {
    clearInterval(st.timer);
    files.forEach(function (f, i) { if (i >= st.done) f.status = 'skip'; });
    st.state = 'done'; st.stopped = true; markDemo('done'); render(); live('中止しました。' + st.done + ' 枚は保存できます');
  }

  // ---- 操作 ----
  Array.prototype.forEach.call(document.querySelectorAll('#demo-seg button'), function (b) {
    b.addEventListener('click', function () { setState(b.getAttribute('data-state')); });
  });
  function loadDummy() { reset(); st.state = 'loaded'; markDemo(st.safari ? 'safari' : 'loaded'); render(); live(TOTAL + ' 枚を読み込みました'); }
  $('pick-folder').addEventListener('click', loadDummy);
  $('pick-files').addEventListener('click', loadDummy);
  var drop = $('drop');
  drop.addEventListener('dragover', function (e) { e.preventDefault(); drop.classList.add('over'); });
  drop.addEventListener('dragleave', function () { drop.classList.remove('over'); });
  drop.addEventListener('drop', function (e) { e.preventDefault(); drop.classList.remove('over'); if (st.state !== 'processing') loadDummy(); });
  $('run').addEventListener('click', function () {
    if (st.state === 'processing') { stop(); return; }
    if (st.stopped) { files.forEach(function (f) { if (f.status === 'skip') f.status = 'wait'; }); start(); return; }
    if (st.state === 'done') { reset(); }
    start();
  });
  $('filter').addEventListener('click', function () { st.filter = !st.filter; render(); });
  $('redo').addEventListener('click', function () {
    var list = flagged();
    list.forEach(function (f) { f.retried = true; finish(f); });
    render(); var fl = flagged().length;
    toast(list.length + ' 件を処理し直しました。残りの要確認は ' + fl + ' 件');
  });
  $('zip').addEventListener('click', function () { toast('blog-images.zip を保存しました（元と同じフォルダ構成）'); });
  $('csv').addEventListener('click', function () { toast('blog-images-結果.csv を書き出しました'); });
  Array.prototype.forEach.call(document.querySelectorAll('#fmt-seg button'), function (b) {
    b.addEventListener('click', function () { if (!b.disabled) { st.fmt = b.getAttribute('data-fmt'); renderControls(); } });
  });
  function numField(id, boxId, hintId, okHint, min, max, unit) {
    $(id).addEventListener('input', function () {
      var v = $(id).value.trim(), n = Number(v), ok = /^\d+$/.test(v) && n >= min && n <= max;
      $(boxId).classList.toggle('bad', !ok);
      $(id).setAttribute('aria-invalid', String(!ok));
      $(hintId).textContent = ok ? okHint : min + '〜' + max + ' ' + unit + ' の数字で入れてください';
    });
  }
  numField('edge', 'edge-box', 'edge-hint', '小さい画像は大きくしません', 320, 8000, 'px');
  numField('target', 'target-box', 'target-hint', '届かないものは「要確認」になります', 20, 20000, 'KB');

  // URL の #state=done などで初期状態を選べる（撮影用）
  var m = location.hash.match(/^#(?:state=)?(empty|loaded|processing|done|safari)$/);
  setState(m ? m[1] : 'empty');
})();
