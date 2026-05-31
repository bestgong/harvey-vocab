/* ===================== Harvey's Vocabulary — app logic ===================== */
(function () {
  "use strict";

  // ---- Config: live Google Sheet (published CSV). Works once sheet is "anyone with link can view". ----
  var SHEET_ID = "14SHVvp1axGL9hThYTKc2Q78sL5C0pCNIad-16ZZsth0";
  var CSV_URL = "https://docs.google.com/spreadsheets/d/" + SHEET_ID + "/gviz/tq?tqx=out:csv&gid=0";

  // ---- State ----
  var WORDS = [];
  var dataSource = "local"; // 'live' | 'local'
  var accentByPos = { "n.": "var(--sky)", "v.": "var(--leaf)", "adj.": "var(--grape)", "adv.": "var(--sun)", "phr.": "var(--primary)" };

  // ---- Safe storage (sandbox-proof) ----
  var mem = {};
  var STORE = (function () {
    try { var k = "__t"; localStorage.setItem(k, "1"); localStorage.removeItem(k); return localStorage; }
    catch (e) { return { getItem: function (k) { return k in mem ? mem[k] : null; }, setItem: function (k, v) { mem[k] = String(v); }, removeItem: function (k) { delete mem[k]; } }; }
  })();
  function loadProg() { try { return JSON.parse(STORE.getItem("harvey_progress") || "{}"); } catch (e) { return {}; } }
  function saveProg(p) { try { STORE.setItem("harvey_progress", JSON.stringify(p)); } catch (e) {} }
  var prog = loadProg(); // { mastered: {word:true}, mistakes: {word:count} }
  if (!prog.mastered) prog.mastered = {};
  if (!prog.mistakes) prog.mistakes = {};

  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };

  // ---- Theme toggle ----
  (function () {
    var t = document.querySelector("[data-theme-toggle]"), r = document.documentElement;
    var d = matchMedia("(prefers-color-scheme:dark)").matches ? "dark" : "light";
    r.setAttribute("data-theme", d);
    function paint() {
      t.innerHTML = d === "dark"
        ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>'
        : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/></svg>';
    }
    paint();
    t.addEventListener("click", function () { d = d === "dark" ? "light" : "dark"; r.setAttribute("data-theme", d); paint(); });
  })();

  // ---- CSV parser (handles quoted fields, commas, newlines) ----
  function parseCSV(text) {
    var rows = [], row = [], field = "", i = 0, inQ = false, c;
    while (i < text.length) {
      c = text[i];
      if (inQ) {
        if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else inQ = false; }
        else field += c;
      } else {
        if (c === '"') inQ = true;
        else if (c === ",") { row.push(field); field = ""; }
        else if (c === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
        else if (c === "\r") { /* skip */ }
        else field += c;
      }
      i++;
    }
    if (field.length || row.length) { row.push(field); rows.push(row); }
    return rows;
  }

  function rowsToWords(rows) {
    if (!rows.length) return [];
    var headers = rows[0].map(function (h) { return h.trim(); });
    var idx = {};
    headers.forEach(function (h, j) { idx[h] = j; });
    var get = function (r, name) { var j = idx[name]; return j == null ? "" : (r[j] || "").trim(); };
    var out = [];
    for (var k = 1; k < rows.length; k++) {
      var r = rows[k];
      var w = get(r, "单词");
      if (!w) continue;
      out.push({
        id: parseInt(get(r, "序号"), 10) || k,
        word: w, pos: get(r, "词性"), meaning: get(r, "中文释义"),
        example: get(r, "英文例句"), exampleZh: get(r, "例句翻译"),
        note: get(r, "用法备注"), book: get(r, "来源课本"), date: get(r, "添加日期")
      });
    }
    return out;
  }

  // ---- Load data: try live CSV, fall back to bundled ----
  function setSource(src) {
    dataSource = src;
    var dot = $("dataDot"), label = $("dataLabel");
    dot.className = "data-dot " + (src === "live" ? "live" : "local");
    label.textContent = src === "live" ? "在线实时" : "本机数据";
    $("dataPill").title = src === "live"
      ? "已连接到在线表格，显示最新单词"
      : "在线表格未公开，使用打包的离线数据（" + (window.VOCAB_GENERATED || "") + "）";
  }

  function tryLive() {
    return fetch(CSV_URL, { cache: "no-store" }).then(function (res) {
      if (!res.ok) throw new Error("http " + res.status);
      return res.text();
    }).then(function (text) {
      if (/<html/i.test(text) || /DOCTYPE/i.test(text)) throw new Error("not public");
      var words = rowsToWords(parseCSV(text));
      if (words.length < 5) throw new Error("too few");
      return words;
    });
  }

  function init() {
    var bundled = (window.VOCAB_DATA || []);
    var settled = false;
    tryLive().then(function (live) {
      if (settled) {
        // 已先用本地数据启动，现在在线数据回来了 → 升级并重新渲染
        WORDS = live; setSource("live"); rerenderAll();
      } else {
        settled = true; WORDS = live; setSource("live"); boot();
      }
    }).catch(function () {
      if (!settled) { settled = true; WORDS = bundled; setSource("local"); boot(); }
    });
    // 保底：若 12s 内在线数据还没回来，先用本地数据启动（不阻塞使用）
    // 上面的 tryLive 仍会继续试，成功后自动升级为在线
    setTimeout(function () {
      if (!settled) { settled = true; WORDS = bundled; setSource("local"); boot(); }
    }, 12000);
  }
  function rerenderAll() {
    try {
      // 清空筛选下拉里动态生成的选项（保留“全部”首项），避免重复
      ["fBook", "qBook", "fPos"].forEach(function (id) {
        var sel = $(id); if (!sel) return;
        while (sel.options.length > 1) sel.remove(1);
      });
      buildFilters(); renderBrowse(); refreshStats(); updateQuizPoolInfo();
    } catch (e) {}
  }

  var booted = false;
  function boot() {
    if (booted) return; booted = true;
    $("loading").classList.add("hidden");
    buildFilters(); renderBrowse(); refreshStats(); renderMistakes(); updateMistakeBadge();
    updateQuizPoolInfo();
  }

  // ---- Filters population ----
  function uniqueSorted(key) {
    var s = {}; WORDS.forEach(function (w) { if (w[key]) s[w[key]] = 1; });
    return Object.keys(s).sort();
  }
  function buildFilters() {
    var books = uniqueSorted("book"), poss = uniqueSorted("pos");
    function fill(sel, arr) { arr.forEach(function (v) { var o = document.createElement("option"); o.value = v; o.textContent = v; sel.appendChild(o); }); }
    fill($("fBook"), books); fill($("qBook"), books); fill($("fPos"), poss);
  }

  // ---- Browse ----
  function currentFilter() {
    return {
      q: $("search").value.trim().toLowerCase(),
      book: $("fBook").value, pos: $("fPos").value,
      mastery: $("fMastery").value, sort: $("fSort").value
    };
  }
  function applyFilter(list, f) {
    var out = list.filter(function (w) {
      if (f.book && w.book !== f.book) return false;
      if (f.pos && w.pos !== f.pos) return false;
      if (f.mastery === "mastered" && !prog.mastered[w.word]) return false;
      if (f.mastery === "unmastered" && prog.mastered[w.word]) return false;
      if (f.q && w.word.toLowerCase().indexOf(f.q) < 0 && w.meaning.toLowerCase().indexOf(f.q) < 0) return false;
      return true;
    });
    if (f.sort === "az") out.sort(function (a, b) { return a.word.toLowerCase() < b.word.toLowerCase() ? -1 : 1; });
    else if (f.sort === "za") out.sort(function (a, b) { return a.word.toLowerCase() > b.word.toLowerCase() ? -1 : 1; });
    else out.sort(function (a, b) { return a.id - b.id; });
    return out;
  }
  function renderBrowse() {
    var f = currentFilter(), list = applyFilter(WORDS, f), grid = $("grid");
    $("statShown").textContent = list.length;
    if (!list.length) { grid.innerHTML = ""; $("browseEmpty").classList.remove("hidden"); return; }
    $("browseEmpty").classList.add("hidden");
    var max = 600, slice = list.slice(0, max);
    grid.innerHTML = slice.map(function (w) {
      var accent = accentByPos[w.pos] || "var(--primary)";
      // 用 div 代替 button：部分浏览器（如百度内核荣耀浏览器）对 <button> 的 display 处理异常，导致内容错位
      return '<div class="wcard" role="button" tabindex="0" style="--accent:' + accent + '" data-word="' + esc(w.word) + '">' +
        (prog.mastered[w.word] ? '<span class="mastered-badge">⭐</span>' : '') +
        speakBtnHtml(w.word, false) +
        '<span class="word">' + esc(w.word) + '</span>' +
        '<span><span class="tag tag-pos">' + esc(w.pos || "—") + '</span></span>' +
        '<span class="meaning">' + esc(w.meaning) + '</span>' +
        '<span class="book">📖 ' + esc(w.book) + '</span></div>';
    }).join("");
    if (list.length > max) grid.innerHTML += '<div class="empty" style="grid-column:1/-1"><p class="muted">显示前 ' + max + ' 个，缩小筛选范围可查看更多</p></div>';
  }
  function refreshStats() {
    $("statTotal").textContent = WORDS.length;
    $("statBooks").textContent = uniqueSorted("book").length;
    var m = 0; WORDS.forEach(function (w) { if (prog.mastered[w.word]) m++; });
    $("statMastered").textContent = m;
  }

  // ---- 发音（浏览器内置语音合成，免费、离线可用）----
  var TTS_OK = (typeof window !== "undefined") && ("speechSynthesis" in window) && (typeof SpeechSynthesisUtterance !== "undefined");
  var _voices = [];
  function loadVoices() {
    if (!TTS_OK) return;
    try { _voices = window.speechSynthesis.getVoices() || []; } catch (e) { _voices = []; }
  }
  function pickEnVoice() {
    if (!_voices.length) loadVoices();
    // 优先美式英语，其次任意英语
    return _voices.filter(function (v) { return /en[-_]US/i.test(v.lang); })[0] ||
           _voices.filter(function (v) { return /^en/i.test(v.lang); })[0] || null;
  }
  if (TTS_OK) {
    loadVoices();
    // 某些浏览器首次 getVoices() 为空，需等 voiceschanged 事件
    try { window.speechSynthesis.addEventListener("voiceschanged", loadVoices); } catch (e) {}
  }
  // 本地合成音（兼底）
  function _localSpeak(text) {
    if (!TTS_OK || !text) return;
    try {
      if (window.speechSynthesis.paused) window.speechSynthesis.resume();
      var speaking = window.speechSynthesis.speaking || window.speechSynthesis.pending;
      window.speechSynthesis.cancel();
      var doIt = function () {
        try {
          var u = new SpeechSynthesisUtterance(String(text));
          u.lang = "en-US"; u.rate = 0.9;
          var v = pickEnVoice(); if (v) u.voice = v;
          window.speechSynthesis.speak(u);
        } catch (e) {}
      };
      if (speaking) setTimeout(doIt, 120); else doIt();
    } catch (e) {}
  }

  // 方案 B：在线真人词典发音（有道，美音）+ 本地合成音兼底
  var _audio = null;        // 复用一个 audio 对象
  var _audioTimer = null;
  function _onlineAudioUrl(word) {
    // type=2 美音，type=1 英音
    return "https://dict.youdao.com/dictvoice?audio=" + encodeURIComponent(word) + "&type=2";
  }
  function speak(text) {
    if (!text) return;
    var word = String(text).trim();
    // 先停掉上一次的播放与合成
    try { if (TTS_OK) window.speechSynthesis.cancel(); } catch (e) {}
    if (_audioTimer) { clearTimeout(_audioTimer); _audioTimer = null; }
    if (_audio) { try { _audio.pause(); } catch (e) {} _audio = null; }

    var fellBack = false;
    var fallback = function () {
      if (fellBack) return; fellBack = true;
      _localSpeak(word); // 在线失败 → 本地合成音
    };
    try {
      var a = new Audio(_onlineAudioUrl(word));
      _audio = a;
      a.preload = "auto";
      // 3.5s 还没能播 → 兼底
      _audioTimer = setTimeout(fallback, 3500);
      a.addEventListener("playing", function () { if (_audioTimer) { clearTimeout(_audioTimer); _audioTimer = null; } });
      a.addEventListener("error", function () { if (_audioTimer) { clearTimeout(_audioTimer); _audioTimer = null; } fallback(); });
      var p = a.play();
      if (p && typeof p.then === "function") {
        p.then(function () {
          if (_audioTimer) { clearTimeout(_audioTimer); _audioTimer = null; }
        }).catch(function () {
          if (_audioTimer) { clearTimeout(_audioTimer); _audioTimer = null; }
          fallback(); // 自动播放被拦/加载失败 → 兼底
        });
      }
    } catch (e) { fallback(); }
  }
  function speakBtnHtml(word, big) {
    // 方案 B 不依赖本地语音包，按钮始终显示
    return '<button class="speak-btn' + (big ? ' speak-btn-lg' : '') + '" type="button" data-speak="' + esc(word) + '" title="点击发音" aria-label="发音">🔊</button>';
  }

  // ---- Word modal ----
  function openModal(word) {
    var w = WORDS.filter(function (x) { return x.word === word; })[0]; if (!w) return;
    var isM = !!prog.mastered[w.word];
    $("modalBody").innerHTML =
      '<div class="big-word">' + esc(w.word) + ' ' + speakBtnHtml(w.word, true) + '</div>' +
      '<div><span class="tag tag-pos">' + esc(w.pos || "—") + '</span> <span class="muted">📖 ' + esc(w.book) + '</span></div>' +
      '<div class="row"><div class="label">中文释义</div><div style="font-weight:800;font-size:var(--text-lg)">' + esc(w.meaning) + '</div></div>' +
      (w.example ? '<div class="row"><div class="label">例句</div><div class="ex">' + esc(w.example) + '</div>' +
        (w.exampleZh ? '<div class="ex ex-zh">' + esc(w.exampleZh) + '</div>' : '') + '</div>' : '') +
      (w.note ? '<div class="row"><div class="label">用法备注</div><div class="muted">' + esc(w.note) + '</div></div>' : '') +
      '<button class="btn ' + (isM ? "btn-ghost" : "btn-leaf") + ' btn-block gap" id="toggleMaster">' +
        (isM ? "↩️ 标记为未掌握" : "⭐ 标记为已掌握") + '</button>';
    $("toggleMaster").addEventListener("click", function () {
      if (prog.mastered[w.word]) delete prog.mastered[w.word]; else prog.mastered[w.word] = true;
      saveProg(prog); refreshStats(); renderBrowse(); openModal(word);
    });
    $("overlay").classList.add("open");
  }
  function closeModal() { $("overlay").classList.remove("open"); }

  // ===================== QUIZ =====================
  var quiz = null, selectedMode = "zh2en";

  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  function quizPool() {
    var book = $("qBook").value, pool = $("qPool").value;
    var list = WORDS.filter(function (w) {
      if (book && w.book !== book) return false;
      if (pool === "unmastered" && prog.mastered[w.word]) return false;
      if (pool === "mistakes" && !prog.mistakes[w.word]) return false;
      return true;
    });
    return list;
  }
  function updateQuizPoolInfo() {
    var n = quizPool().length;
    var needEx = selectedMode === "cloze";
    var usable = needEx ? quizPool().filter(function (w) { return w.example && w.example.toLowerCase().indexOf(String(w.word).toLowerCase()) >= 0; }).length : n;
    var msg = "当前题库共 " + n + " 个单词";
    if (needEx) msg += "（其中 " + usable + " 个带可用例句）";
    $("quizPoolInfo").textContent = msg;
  }

  function buildQuestions() {
    var mode = selectedMode;
    var pool = quizPool();
    if (mode === "cloze") {
      pool = pool.filter(function (w) { return w.example && w.example.toLowerCase().indexOf(String(w.word).toLowerCase()) >= 0; });
    }
    if (pool.length < 1) return null;
    var count = parseInt($("qCount").value, 10);
    var picked = shuffle(pool);
    if (count > 0) picked = picked.slice(0, count);

    // distractor pool by meaning/word
    return picked.map(function (w) {
      var q = { w: w, mode: mode };
      if (mode === "zh2en" || mode === "en2zh") {
        var others = shuffle(WORDS.filter(function (x) {
          return x.word !== w.word && (mode === "zh2en" ? x.word !== w.word : x.meaning && x.meaning !== w.meaning);
        })).slice(0, 3);
        var opts = others.map(function (x) { return mode === "zh2en" ? x.word : x.meaning; });
        opts.push(mode === "zh2en" ? w.word : w.meaning);
        q.options = shuffle(opts);
        q.answer = mode === "zh2en" ? w.word : w.meaning;
      }
      return q;
    });
  }

  function startQuiz() {
    var qs = buildQuestions();
    if (!qs || !qs.length) { alert("这个题库里没有足够的单词，换个范围试试～"); return; }
    quiz = { qs: qs, i: 0, score: 0, wrong: [] };
    $("quizSetup").classList.add("hidden");
    $("quizResult").classList.add("hidden");
    $("quizPlay").classList.remove("hidden");
    renderQuestion();
  }

  function renderQuestion() {
    var q = quiz.qs[quiz.i], w = q.w, body = $("qBody"), fb = $("qFeedback");
    fb.className = "feedback"; fb.innerHTML = ""; $("qNext").classList.add("hidden");
    $("qIndex").textContent = (quiz.i + 1) + " / " + quiz.qs.length;
    $("qScore").textContent = quiz.score;
    $("qProgress").style.width = (quiz.i / quiz.qs.length * 100) + "%";

    if (q.mode === "zh2en") {
      body.innerHTML = '<div class="q-prompt center">下面哪个单词是这个意思？</div>' +
        '<div class="q-word">' + esc(w.meaning) + '</div>' +
        '<div class="q-sub">' + esc(w.pos || "") + '</div>' +
        '<div class="options" id="opts"></div>';
      renderOptions(q);
    } else if (q.mode === "en2zh") {
      body.innerHTML = '<div class="q-prompt center">这个单词是什么意思？</div>' +
        '<div class="q-word">' + esc(w.word) + '</div>' +
        '<div class="q-sub">' + esc(w.pos || "") + '</div>' +
        '<div class="options" id="opts"></div>';
      renderOptions(q);
    } else if (q.mode === "cloze") {
      var re = new RegExp(w.word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i");
      var sentence = w.example.replace(re, '<span class="blank">____</span>');
      body.innerHTML = '<div class="q-prompt center">在句子空格里填入正确的单词</div>' +
        '<div class="q-example">' + sentence + '</div>' +
        (w.exampleZh ? '<div class="q-sub">' + esc(w.exampleZh) + '</div>' : '') +
        '<div class="type-row"><input class="type-input" id="typeIn" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="在这里输入…" /></div>' +
        '<button class="btn btn-primary btn-block mt4" id="typeSubmit">检查 ✓</button>';
      setupTyping(q);
    } else if (q.mode === "spell") {
      var hint = w.word.split(/\s+/).map(function (tok) {
        if (tok.length <= 1) return tok;
        if (tok.length === 2) return tok[0] + " ·";
        return tok[0] + " " + new Array(tok.length - 1).join("· ") + tok[tok.length - 1];
      }).join("  /  ");
      var letterCount = (w.word.match(/[a-zA-Z]/g) || []).length;
      hint += "   (" + letterCount + " 个字母)";
      body.innerHTML = '<div class="q-prompt center">看中文，拼出英文单词</div>' +
        '<div class="q-word">' + esc(w.meaning) + '</div>' +
        '<div class="q-sub">' + esc(w.pos || "") + '</div>' +
        '<div class="spell-hint">' + esc(hint) + '</div>' +
        '<div class="type-row"><input class="type-input" id="typeIn" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="拼写单词…" /></div>' +
        '<button class="btn btn-primary btn-block mt4" id="typeSubmit">检查 ✓</button>';
      setupTyping(q);
    }
  }

  function renderOptions(q) {
    var box = $("opts");
    box.innerHTML = q.options.map(function (o, j) { return '<button class="option" data-i="' + j + '">' + esc(o) + '</button>'; }).join("");
    Array.prototype.forEach.call(box.querySelectorAll(".option"), function (btn) {
      btn.addEventListener("click", function () {
        var chosen = q.options[+btn.getAttribute("data-i")];
        var correct = chosen === q.answer;
        Array.prototype.forEach.call(box.querySelectorAll(".option"), function (b) {
          b.disabled = true;
          if (q.options[+b.getAttribute("data-i")] === q.answer) b.classList.add("correct");
        });
        if (!correct) btn.classList.add("wrong");
        finishAnswer(q, correct, q.answer);
      });
    });
  }

  function setupTyping(q) {
    var input = $("typeIn"), submit = $("typeSubmit");
    input.focus();
    function go() {
      if (input.disabled) return;
      var val = input.value.trim().toLowerCase();
      var ans = q.w.word.trim().toLowerCase();
      var correct = val === ans;
      input.disabled = true; submit.classList.add("hidden");
      input.style.borderColor = correct ? "var(--leaf)" : "var(--error)";
      finishAnswer(q, correct, q.w.word);
    }
    submit.addEventListener("click", go);
    input.addEventListener("keydown", function (e) { if (e.key === "Enter") go(); });
  }

  function finishAnswer(q, correct, answer) {
    var fb = $("qFeedback");
    if (correct) {
      quiz.score++; $("qScore").textContent = quiz.score;
      fb.className = "feedback ok"; fb.innerHTML = "🎉 答对了！";
      // typed-correct & not previously mistaken → auto mark mastered progress is not auto; keep manual
    } else {
      quiz.wrong.push(q.w);
      prog.mistakes[q.w.word] = (prog.mistakes[q.w.word] || 0) + 1;
      saveProg(prog); updateMistakeBadge();
      fb.className = "feedback no";
      fb.innerHTML = "💪 正确答案：<strong>" + esc(answer) + "</strong>" +
        "<small>" + esc(q.w.word) + " " + esc(q.w.pos) + " — " + esc(q.w.meaning) + "</small>";
    }
    var next = $("qNext");
    next.classList.remove("hidden");
    next.textContent = (quiz.i + 1 >= quiz.qs.length) ? "查看成绩 🏆" : "下一题 →";
  }

  function nextQuestion() {
    quiz.i++;
    if (quiz.i >= quiz.qs.length) showResult();
    else renderQuestion();
  }

  function showResult() {
    $("quizPlay").classList.add("hidden");
    $("quizResult").classList.remove("hidden");
    var total = quiz.qs.length, score = quiz.score, pct = Math.round(score / total * 100);
    $("rPct").textContent = pct + "%";
    $("rRing").style.setProperty("--pct", pct);
    $("rDetail").textContent = "答对 " + score + " / " + total + " 题" + (quiz.wrong.length ? "，错题已加入错题本" : "");
    var emoji = "🎉", title = "太棒了！";
    if (pct === 100) { emoji = "🏆"; title = "满分！完美！"; }
    else if (pct >= 80) { emoji = "🌟"; title = "非常棒！"; }
    else if (pct >= 60) { emoji = "👍"; title = "做得不错！"; }
    else { emoji = "💪"; title = "继续加油！"; }
    $("rEmoji").textContent = emoji; $("rTitle").textContent = title;
    refreshStats(); renderBrowse();
  }

  // ===================== MISTAKES =====================
  function renderMistakes() {
    var list = $("mistakeList"), words = Object.keys(prog.mistakes);
    if (!words.length) { list.innerHTML = ""; $("mistakeEmpty").classList.remove("hidden"); return; }
    $("mistakeEmpty").classList.add("hidden");
    var items = words.map(function (wd) {
      var w = WORDS.filter(function (x) { return x.word === wd; })[0] || { word: wd, meaning: "", pos: "" };
      return { w: w, c: prog.mistakes[wd] };
    }).sort(function (a, b) { return b.c - a.c; });
    list.innerHTML = items.map(function (it) {
      return '<div class="mistake-item" data-word="' + esc(it.w.word) + '" style="cursor:pointer">' +
        '<div><div class="m-word">' + esc(it.w.word) + '</div>' +
        '<div class="m-meaning">' + esc(it.w.pos) + ' ' + esc(it.w.meaning) + '</div></div>' +
        '<div class="m-count">错 ' + it.c + ' 次</div></div>';
    }).join("");
  }
  function updateMistakeBadge() {
    var n = Object.keys(prog.mistakes).length;
    $("mistakeCount").textContent = n ? "(" + n + ")" : "";
  }

  // ===================== Views / nav =====================
  function showView(v) {
    ["browse", "quiz", "mistakes"].forEach(function (name) {
      $("view-" + name).classList.toggle("hidden", name !== v);
    });
    Array.prototype.forEach.call(document.querySelectorAll(".tab"), function (t) {
      t.classList.toggle("active", t.getAttribute("data-view") === v);
    });
    if (v === "quiz") { $("quizSetup").classList.remove("hidden"); $("quizPlay").classList.add("hidden"); $("quizResult").classList.add("hidden"); updateQuizPoolInfo(); }
    if (v === "mistakes") renderMistakes();
  }

  // ===================== Events =====================
  document.addEventListener("click", function (e) {
    var sp = e.target.closest && e.target.closest(".speak-btn");
    if (sp) { e.preventDefault(); e.stopPropagation(); speak(sp.getAttribute("data-speak")); return; }
    var card = e.target.closest && e.target.closest(".wcard"); if (card) openModal(card.getAttribute("data-word"));
    var mi = e.target.closest && e.target.closest(".mistake-item"); if (mi) openModal(mi.getAttribute("data-word"));
    var tab = e.target.closest && e.target.closest(".tab"); if (tab) showView(tab.getAttribute("data-view"));
    var mode = e.target.closest && e.target.closest(".mode-card");
    if (mode) {
      selectedMode = mode.getAttribute("data-mode");
      Array.prototype.forEach.call(document.querySelectorAll(".mode-card"), function (m) { m.classList.toggle("sel", m === mode); });
      updateQuizPoolInfo();
    }
  });
  ["search", "fBook", "fPos", "fMastery", "fSort"].forEach(function (id) {
    $(id).addEventListener("input", renderBrowse);
    $(id).addEventListener("change", renderBrowse);
  });
  ["qBook", "qPool", "qCount"].forEach(function (id) { $(id).addEventListener("change", updateQuizPoolInfo); });
  $("startQuiz").addEventListener("click", startQuiz);
  $("qNext").addEventListener("click", nextQuestion);
  $("rAgain").addEventListener("click", function () { showView("quiz"); });
  $("rReview").addEventListener("click", function () { showView("mistakes"); });
  // 清空错题本需管理员密码（密码以 SHA-256 哈希形式存放，源码中不出现明文）
  var CLEAR_PWD_HASH = "b5fcd904c8f3b83a326f5f594cbd7cc114408a8485a0c4754d78998c177d3554";
  function sha256Hex(str) {
    if (window.crypto && window.crypto.subtle) {
      var data = new TextEncoder().encode(str);
      return window.crypto.subtle.digest("SHA-256", data).then(function (buf) {
        return Array.prototype.map.call(new Uint8Array(buf), function (b) {
          return b.toString(16).padStart(2, "0");
        }).join("");
      });
    }
    return Promise.reject(new Error("no-subtle-crypto"));
  }
  $("clearMistakes").addEventListener("click", function () {
    if (!Object.keys(prog.mistakes).length) { alert("错题本已经是空的啦～"); return; }
    var pwd = prompt("清空错题本需要管理员密码：");
    if (pwd === null) return; // 用户取消
    sha256Hex(pwd).then(function (h) {
      if (h === CLEAR_PWD_HASH) {
        prog.mistakes = {}; saveProg(prog); renderMistakes(); updateMistakeBadge();
        alert("错题本已清空。");
      } else {
        alert("密码不正确，错题本未清空。");
      }
    }).catch(function () {
      alert("当前浏览器不支持密码校验，错题本未清空。");
    });
  });
  $("modalClose").addEventListener("click", closeModal);
  $("overlay").addEventListener("click", function (e) { if (e.target === $("overlay")) closeModal(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeModal(); });
  $("refreshBtn").addEventListener("click", function () {
    var btn = $("refreshBtn"); btn.style.opacity = ".5";
    tryLive().then(function (live) { WORDS = live; setSource("live"); }).catch(function () { setSource(dataSource); })
      .then(function () { buildFilters_reset(); renderBrowse(); refreshStats(); updateQuizPoolInfo(); btn.style.opacity = "1"; });
  });
  function buildFilters_reset() {
    ["fBook", "qBook", "fPos"].forEach(function (id) {
      var keep = $(id).firstElementChild; $(id).innerHTML = ""; $(id).appendChild(keep);
    });
    buildFilters();
  }

  init();
})();
