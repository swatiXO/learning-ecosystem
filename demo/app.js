// Barebones test harness — not the real app. See demo/README.md.

const state = { childId: null, sessionId: null };

// ---------- tiny helpers ----------

const logEl = document.getElementById("log");
function log(label, data) {
  logEl.textContent += `\n[${new Date().toLocaleTimeString()}] ${label}\n${JSON.stringify(data, null, 2)}\n`;
  logEl.scrollTop = logEl.scrollHeight;
}

async function api(path, method = "GET", body) {
  const opts = { method, headers: {} };
  if (body !== undefined) {
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(body);
  }
  const res = await fetch(path, opts);
  let data = null;
  try {
    data = await res.json();
  } catch {
    /* empty body */
  }
  log(`${method} ${path} -> ${res.status}`, { request: body, response: data });
  if (!res.ok) throw new Error(`${method} ${path} failed (${res.status}): ${JSON.stringify(data)}`);
  return data;
}

const rnd = (min, max) => Math.round(min + Math.random() * (max - min));
const reps = (n, fn) => Array.from({ length: n }, (_, i) => fn(i));
const nowIso = () => new Date().toISOString();
const uuid = () => crypto.randomUUID();

async function sendEventBatch(activity, activityRunId, pairs) {
  if (!pairs.length) return;
  const events = pairs.map(([event_type, payload]) => ({
    event_id: uuid(),
    child_id: state.childId,
    session_id: state.sessionId,
    activity_run_id: activityRunId,
    activity,
    activity_version: "1.0.0",
    event_type,
    ts_client: nowIso(),
    payload,
  }));
  await api("/events/batch", "POST", { events });
}

// ---------- quick-simulate event generators (all 20 activities) ----------
// Shapes match docs/activity-signal-map.md exactly.

const GEN = {
  stars_not_clouds: (q) =>
    q === "good"
      ? reps(10, () => ["tap", { target: "star", correct: true, reaction_ms: rnd(350, 450) }])
      : reps(6, () => ["tap", { target: "star", correct: true, reaction_ms: rnd(200, 900) }]).concat(
          reps(4, () => ["tap", { target: "cloud", correct: false, reaction_ms: rnd(200, 900) }])
        ),
  watch_the_pond: (q) =>
    q === "good"
      ? reps(10, (i) => ["response", { time_bucket: i, correct: true }])
      : reps(10, (i) => ["response", { time_bucket: i, correct: i < 4 }]),
  wait_for_the_bell: (q) =>
    q === "good"
      ? reps(6, () => ["tap", { phase: "bell", early: false, wait_ms: rnd(1000, 1500) }])
      : reps(3, () => ["tap", { phase: "waiting", early: true, wait_ms: null }]).concat(
          reps(3, () => ["tap", { phase: "bell", early: false, wait_ms: rnd(600, 3000) }])
        ),
  distraction_garden: (q) =>
    q === "good"
      ? reps(10, () => ["tap", { target: "on_task" }])
      : reps(4, () => ["tap", { target: "distractor" }])
          .concat(reps(6, () => ["tap", { target: "on_task" }]))
          .concat(reps(2, () => ["response", { return_ms: rnd(2000, 4000) }])),
  follow_instructions: (q) =>
    q === "good"
      ? reps(5, () => ["response", { n_steps: 3, steps_followed: 3, correct: true, reaction_ms: rnd(500, 900) }])
      : reps(5, () => ["response", { n_steps: 4, steps_followed: 2, correct: false, reaction_ms: rnd(900, 1600) }]).concat(
          reps(2, () => ["hint", {}])
        ),
  copy_the_pattern: (q) =>
    q === "good"
      ? reps(5, (i) => ["response", { sequence_length: 3 + i, correct_order: true }])
      : reps(5, (i) => ["response", { sequence_length: 2, correct_order: i % 2 === 0 }]),
  story_and_questions: (q) =>
    q === "good"
      ? reps(5, () => ["response", { correct: true }])
      : reps(5, () => ["response", { correct: false }]).concat(reps(2, () => ["hint", {}])),
  read_and_answer: (q) =>
    q === "good"
      ? reps(5, () => ["response", { correct: true, time_on_task_ms: rnd(2000, 3000) }])
      : reps(5, () => ["response", { correct: false, time_on_task_ms: rnd(5000, 9000) }]).concat(
          reps(2, () => ["hint", {}])
        ),
  speak_this_line: (q) =>
    q === "good"
      ? [["audio_captured", { storage_key: "demo/audio1", duration_ms: 1500 }]]
      : [["audio_captured", { storage_key: "demo/audio2", duration_ms: 2500 }], ["retry", {}], ["retry", {}]],
  name_the_picture: (q) =>
    (q === "good"
      ? reps(5, () => ["response", { reaction_ms: rnd(400, 700) }])
      : reps(5, () => ["response", { reaction_ms: rnd(2000, 3500) }])
    ).concat([["audio_captured", { storage_key: "demo/audio3" }]]),
  which_word: (q) =>
    q === "good"
      ? reps(6, () => ["response", { target: "ship", selected: "ship", correct: true, reaction_ms: rnd(500, 800) }])
      : reps(3, () => ["response", { target: "ship", selected: "ship", correct: true, reaction_ms: rnd(500, 800) }]).concat(
          reps(3, () => ["response", { target: "ship", selected: "chip", correct: false, reaction_ms: rnd(800, 1500) }])
        ),
  retell_the_story: (q) => [
    ["audio_captured", { storage_key: q === "good" ? "demo/audio5" : "demo/audio6", duration_ms: 4000 }],
  ],
  chat_with_a_character: (q) =>
    q === "good"
      ? reps(4, (i) => ["audio_captured", { storage_key: "demo/chat" + i, turn_index: i, latency_ms: rnd(400, 800), interrupted: false }])
      : reps(4, (i) => ["audio_captured", { storage_key: "demo/chat" + i, turn_index: i, latency_ms: rnd(1500, 3000), interrupted: true }]),
  how_does_she_feel: (q) =>
    q === "good"
      ? reps(5, () => ["response", { correct: true, reaction_ms: rnd(600, 1000) }])
      : reps(5, () => ["response", { correct: false, reaction_ms: rnd(1500, 2500) }]),
  what_would_you_do: (q) => reps(3, () => ["response", { choice: q === "good" ? "kind" : "unkind", reaction_ms: rnd(600, 1200) }]),
  about_me: (q) => reps(3, () => ["response", { choice: q === "good" ? "confident" : "unsure" }]),
  oops_try_again: (q) =>
    q === "good"
      ? reps(4, () => ["retry", { time_to_retry_ms: rnd(500, 1000) }])
      : reps(1, () => ["retry", { time_to_retry_ms: rnd(2000, 4000) }]).concat(reps(3, () => ["quit", {}])),
  level_choice: (q) => [["setting_changed", { chosen_level: q === "good" ? "medium" : "easy" }]],
  mood_check_in: (q) =>
    q === "good"
      ? [["mood", { mood: "happy", phase: "before" }], ["mood", { mood: "happy", phase: "after" }]]
      : [["mood", { mood: "sad", phase: "before" }]].concat(reps(2, () => ["skip", {}])),
  sensory_setup: (q) =>
    q === "good"
      ? [["setting_changed", { setting: "volume", value: "medium" }]]
      : reps(6, () => ["setting_changed", { setting: "calm_mode", value: "on" }]),
};

// ---------- real, actually-playable mini-games (subset) ----------

function showGameCard(html) {
  document.getElementById("game-content").innerHTML = html;
  document.getElementById("game-modal").hidden = false;
}
function hideGameCard() {
  document.getElementById("game-modal").hidden = true;
}

function playStarsNotClouds(onDone) {
  const trials = 10;
  const events = [];
  let i = 0;
  showGameCard(
    `<h3>⭐ Stars, not clouds</h3><p>Tap the ⭐. Don't tap the ☁️.</p><div class="stage" id="stage"></div><p id="progress"></p>`
  );
  const stage = document.getElementById("stage");
  const progress = document.getElementById("progress");

  function nextTrial() {
    if (i >= trials) return finish();
    progress.textContent = `Trial ${i + 1}/${trials}`;
    const isStar = Math.random() > 0.35;
    const el = document.createElement("div");
    el.className = "stimulus";
    el.textContent = isStar ? "⭐" : "☁️";
    el.style.left = rnd(10, 80) + "%";
    el.style.top = rnd(10, 70) + "%";
    const shownAt = performance.now();
    let answered = false;
    el.onclick = () => {
      if (answered) return;
      answered = true;
      const reaction_ms = Math.round(performance.now() - shownAt);
      events.push(["tap", { target: isStar ? "star" : "cloud", correct: isStar, reaction_ms }]);
      el.remove();
      i++;
      setTimeout(nextTrial, 250);
    };
    stage.appendChild(el);
    setTimeout(() => {
      if (!answered) {
        el.remove();
        i++;
        nextTrial(); // a miss on a star, or a correctly-ignored cloud — neither logged
      }
    }, 1000);
  }
  function finish() {
    hideGameCard();
    onDone(events);
  }
  nextTrial();
}

function playWaitForBell(onDone) {
  const trials = 5;
  const events = [];
  let i = 0;
  let bellShownAt = null;
  showGameCard(
    `<h3>🔔 Wait for the bell</h3><p>Don't tap until you see 🔔 — then tap fast.</p><div class="stage" id="stage"></div><p id="progress"></p>`
  );
  const stage = document.getElementById("stage");
  const progress = document.getElementById("progress");

  function nextTrial() {
    if (i >= trials) return finish();
    progress.textContent = `Trial ${i + 1}/${trials}`;
    bellShownAt = null;
    stage.innerHTML =
      '<div id="indicator" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:3rem;cursor:pointer;">⏳</div>';
    const ind = document.getElementById("indicator");
    const delay = rnd(1000, 2500);
    let answered = false;
    ind.onclick = () => {
      if (answered) return;
      answered = true;
      if (bellShownAt === null) {
        events.push(["tap", { phase: "waiting", early: true, wait_ms: null }]);
      } else {
        events.push(["tap", { phase: "bell", early: false, wait_ms: Math.round(performance.now() - bellShownAt) }]);
      }
      i++;
      setTimeout(nextTrial, 250);
    };
    setTimeout(() => {
      if (answered) return;
      bellShownAt = performance.now();
      ind.textContent = "🔔";
    }, delay);
  }
  function finish() {
    hideGameCard();
    onDone(events);
  }
  nextTrial();
}

function playDistractionGarden(onDone) {
  const trials = 10;
  const events = [];
  let i = 0;
  let lastDistractorAt = null;
  showGameCard(`<h3>🌻 Distraction garden</h3><p>Tap 🌻. Ignore 🦋.</p><div class="stage" id="stage"></div><p id="progress"></p>`);
  const stage = document.getElementById("stage");
  const progress = document.getElementById("progress");

  function nextTrial() {
    if (i >= trials) return finish();
    progress.textContent = `Trial ${i + 1}/${trials}`;
    const isDistractor = Math.random() > 0.7;
    const el = document.createElement("div");
    el.className = "stimulus";
    el.textContent = isDistractor ? "🦋" : "🌻";
    el.style.left = rnd(10, 80) + "%";
    el.style.top = rnd(10, 70) + "%";
    let answered = false;
    el.onclick = () => {
      if (answered) return;
      answered = true;
      events.push(["tap", { target: isDistractor ? "distractor" : "on_task" }]);
      if (isDistractor) {
        lastDistractorAt = performance.now();
      } else if (lastDistractorAt !== null) {
        events.push(["response", { return_ms: Math.round(performance.now() - lastDistractorAt) }]);
        lastDistractorAt = null;
      }
      el.remove();
      i++;
      setTimeout(nextTrial, 200);
    };
    stage.appendChild(el);
    setTimeout(() => {
      if (!answered) {
        el.remove();
        i++;
        nextTrial();
      }
    }, 900);
  }
  function finish() {
    hideGameCard();
    onDone(events);
  }
  nextTrial();
}

const REAL_GAMES = {
  stars_not_clouds: playStarsNotClouds,
  wait_for_the_bell: playWaitForBell,
  distraction_garden: playDistractionGarden,
};

// ---------- activity-run lifecycle ----------

async function startActivityRun(activity, dayIndex) {
  const run = await api("/activity-runs", "POST", {
    session_id: state.sessionId,
    activity,
    activity_version: "1.0.0",
    day_index: dayIndex ?? null,
  });
  return run.id;
}

async function finishActivity(runId, status = "completed") {
  await api(`/activity-runs/${runId}`, "PATCH", { status });
  await renderToday();
}

async function playReal(activity, dayIndex) {
  const runId = await startActivityRun(activity, dayIndex);
  REAL_GAMES[activity](async (events) => {
    await sendEventBatch(activity, runId, events);
    await finishActivity(runId, "completed");
  });
}

async function quickSimulate(activity, dayIndex, quality) {
  const runId = await startActivityRun(activity, dayIndex);
  const events = GEN[activity] ? GEN[activity](quality) : [];
  await sendEventBatch(activity, runId, events);
  await finishActivity(runId, "completed");
}

async function skipActivity(activity, dayIndex) {
  const runId = await startActivityRun(activity, dayIndex);
  await finishActivity(runId, "skipped");
}

// ---------- today / profile / plan panels ----------

async function renderToday() {
  const container = document.getElementById("today-content");
  let today;
  try {
    today = await api(`/children/${state.childId}/today`);
  } catch {
    container.textContent = "No plan yet (week 1 not finished, or scoring hasn't run).";
    return;
  }

  container.innerHTML = "";
  const header = document.createElement("p");
  header.innerHTML =
    `Phase: <b>${today.phase}</b>` +
    (today.day_index ? ` — Day ${today.day_index}/7` : "") +
    (today.plan_id ? ` — Plan <code>${today.plan_id.slice(0, 8)}</code>` : "");
  container.appendChild(header);

  if (today.activities.length === 0) {
    container.appendChild(
      document.createTextNode(
        today.phase === "plan" ? "No activities mapped for this plan's modules." : "No activities scheduled."
      )
    );
    return;
  }

  for (const activity of today.activities) {
    const row = document.createElement("div");
    row.className = "activity-row";
    const hasRealGame = !!REAL_GAMES[activity];
    row.innerHTML = `
      <span class="name">${activity}</span>
      ${hasRealGame ? `<button data-act="real">▶ Play</button>` : ""}
      <button data-act="good">✅ Simulate good</button>
      <button data-act="poor">⚠️ Simulate poor</button>
      <button data-act="skip">⏭ Skip</button>
    `;
    row.querySelectorAll("button").forEach((btn) => {
      btn.onclick = async () => {
        row.querySelectorAll("button").forEach((b) => (b.disabled = true));
        try {
          const day = today.day_index;
          if (btn.dataset.act === "real") await playReal(activity, day);
          else if (btn.dataset.act === "skip") await skipActivity(activity, day);
          else await quickSimulate(activity, day, btn.dataset.act);
        } catch (e) {
          alert(e.message);
          row.querySelectorAll("button").forEach((b) => (b.disabled = false));
        }
      };
    });
    container.appendChild(row);
  }
}

document.getElementById("refresh-profile").onclick = async () => {
  const el = document.getElementById("profile-content");
  const profile = await api(`/children/${state.childId}/profile`);
  if (!profile.scores.length) {
    el.textContent = "No scores yet.";
    return;
  }
  el.innerHTML =
    `<table><tr><th>Dimension</th><th>Score</th><th>Confidence</th><th>Baseline</th><th>Computed</th></tr>` +
    profile.scores
      .map(
        (s) =>
          `<tr><td>${s.dimension}</td><td>${s.score}</td><td>${s.confidence}</td><td>${s.is_baseline}</td><td>${new Date(
            s.computed_at
          ).toLocaleString()}</td></tr>`
      )
      .join("") +
    `</table>`;
};

document.getElementById("refresh-plan").onclick = async () => {
  const el = document.getElementById("plan-content");
  try {
    const plan = await api(`/children/${state.childId}/plan`);
    el.innerHTML =
      `<p>Version ${plan.version} · created_by=${plan.created_by}</p>` +
      `<table><tr><th>Module</th><th>Weight</th></tr>` +
      plan.modules.map((m) => `<tr><td>${m.module}</td><td>${m.weight}</td></tr>`).join("") +
      `</table><p>Rationale: <code>${JSON.stringify(plan.rationale)}</code></p>`;
  } catch {
    el.textContent = "No active plan yet.";
  }
};

// ---------- onboarding ----------

function fillSelect(name, values) {
  const el = document.querySelector(`[name="${name}"]`);
  for (const v of values) {
    const o = document.createElement("option");
    o.value = v;
    o.textContent = v;
    el.appendChild(o);
  }
}

async function loadOptions() {
  const opts = await api("/onboarding/options");
  fillSelect("guardian_relationship", opts.relationships);
  fillSelect("area", opts.areas);
  fillSelect("grade", opts.grades);
  fillSelect("home_languages", opts.languages);
  fillSelect("gender", opts.genders);
  fillSelect("avatar", opts.avatars);
}

document.querySelector('[name="schooling"]').onchange = (e) => {
  document.getElementById("school-fields").hidden = e.target.value !== "school";
};

document.getElementById("onboarding-form").onsubmit = async (e) => {
  e.preventDefault();
  const form = e.target;
  const isSchool = form.schooling.value === "school";
  const homeLanguages = Array.from(form.home_languages.selectedOptions).map((o) => o.value);
  const payload = {
    guardian_name: form.guardian_name.value,
    guardian_relationship: form.guardian_relationship.value,
    guardian_phone: form.guardian_phone.value,
    locale: form.locale.value || "en",
    child_name: form.child_name.value,
    date_of_birth: form.date_of_birth.value,
    area: form.area.value,
    schooling: form.schooling.value,
    school_name: isSchool ? form.school_name.value || null : null,
    grade: isSchool ? form.grade.value || null : null,
    home_languages: homeLanguages.length ? homeLanguages : [form.home_languages.options[0].value],
    gender: form.gender.value || null,
    avatar: form.avatar.value || null,
    consent: {
      terms: form.terms.checked,
      audio: form.audio.checked,
      video: form.video.checked,
      teacher_share: form.teacher_share.checked,
    },
  };
  const result = await api("/onboarding", "POST", payload);
  state.childId = result.child_id;
  const session = await api("/sessions", "POST", { child_id: state.childId });
  state.sessionId = session.id;

  document.getElementById("onboarding-section").hidden = true;
  document.getElementById("main-section").hidden = false;
  document.getElementById("child-info").textContent = `child_id=${state.childId} · age_band=${result.age_band}`;
  await renderToday();
};

loadOptions().catch((e) => alert("Failed to load onboarding options: " + e.message));
