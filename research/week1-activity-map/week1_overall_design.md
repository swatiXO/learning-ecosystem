# Week-1 Baseline: Overall Design (reliability, order, length, engagement, confidence, Pakistan constraints)

Scope: how to structure the 7-day, game-based baseline week (ages 5–12, Android tablet, Urdu/English) so the 12 skill scores (0–100) and their confidences (0–1) are as reliable and fair as possible for **within-child** tracking. Not diagnostic, no norms, no ranking.

Convention used in these notes: every number is tagged **[lit. estimate: source]** if it comes from a study, or **[illustrative calc]** if I computed it with a standard formula to show scale. Illustrative numbers are NOT measured properties of this app's tasks. They should be replaced by our own pilot estimates.

---

## Q1. What reliability can a 2–4 minute child task realistically reach, and how much does a second session add?

### Takeaway
Single brief experimental tasks typically give test-retest reliability of about 0.4–0.7, even in adults running hundreds of trials. Difference-score measures (RT costs, cueing effects) are often worse, sometimes near 0. Reliability rises a lot when you aggregate: batteries or latent composites in preschoolers reached about 0.95 where single tasks reached about 0.60. A 2–4 minute task given once should be treated as a low-to-moderate reliability measurement. A second session, or a second task on the same dimension, is the cheapest big gain.

### Cited Findings
- **The reliability paradox.** Tasks produce robust group effects precisely *because* between-person variance is low, and low between-person variance gives low test-retest reliability for individual differences. Seven classic tasks (Flanker, Stroop, stop-signal, go/no-go, Posner, Navon, SNARC) showed test-retest reliabilities "ranging from 0 to .82" — [Hedge, Powell & Sumner 2018, Behav Res Methods 50:1166–1186](https://pmc.ncbi.nlm.nih.gov/articles/PMC5990556)
- ICCs over a 3-week interval in adults **[lit. estimate: Hedge et al. 2018]**: Flanker RT cost .40/.57 (Study 1/2); Flanker error cost .58/.72; Stroop RT cost .60/.66; Stroop error cost .48/.44; **go/no-go commission errors .76/.76**; stop-signal SSRT .36/.49; Posner cueing .70; SNARC RT .22, error .03; Navon global RT cost 0, local RT cost .14, local error cost .82 — [Hedge et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5990556)
- Those ICCs came from very long sessions: 720 trials (Flanker/Stroop) and 600 trials (go/no-go, stop-signal) per session **[lit. estimate: Hedge et al. 2018]**. Our 2–4 minute tasks will run far fewer trials. The authors note the field "lack[s] information to guide researchers on how many trials to run" — [Hedge et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5990556)
- The low reliabilities came from low between-person variance, not mainly from high measurement noise — [Hedge et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5990556); summary at [Psychonomic Society featured content](https://featuredcontent.psychonomic.org/reproducible-studies-may-not-generate-reliable-individual-differences/)
- **Children, tablet/touch EF battery (EF Touch).** 140 mostly low-income children (mean age 48 months) did up to 6 tasks twice, a median of 16 days apart. Single-task retest r averaged .60 (range .52–.66). A latent battery factor across time reached φ = .95 **[lit. estimate: Willoughby & Blair, EF Touch retest study]**. The authors conclude battery-derived scores are "appreciably stronger" than single-task scores for intra- and inter-individual differences — [FPG/UNC summary](https://fpg.unc.edu/publications/test-retest-reliability-new-executive-function-battery-use-early-childhood); [RTI record](https://www.rti.org/publication/test-retest-reliability-new-executive-function-battery-use-early-childhood)
- **NIH Toolbox Cognition Battery, short interval.** Earlier validation (Weintraub et al. 2013) with 7–21-day retest in ages 3–15 reported ICCs of 0.76–0.99 on raw scores **[lit. estimate: as summarised by Anokhin et al. 2022]** — [PMC8589010](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589010/)
- **NIH Toolbox, 3-year interval, ages 9–15.** ICCs: Flanker 0.52, DCCS 0.58, Picture Sequence Memory 0.48, List Sorting WM 0.49, Pattern Comparison 0.51, Picture Vocabulary 0.56, Oral Reading 0.64. Composites: Fluid 0.61, Crystallized 0.66, Total 0.62. 14–78% of participants shifted >1 SD in T-score between years **[lit. estimate: PMC8589010]**. Composites again beat single tests — [PMC8589010](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589010/)
- **Aggregation principle.** Measurement error shrinks when analyses use composites rather than single tests, and averaging several change measures gives a more reliable change estimate than any one. This is the basis of "measurement burst" designs: short bursts of intensive repeated assessment — [PMC3633558 (robust cognitive change / burst designs)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3633558); [Penn State, measurement burst design](https://pure.psu.edu/en/publications/measurement-burst-design/)
- Ultra-brief complex-span working-memory tasks given repeatedly on smartphones in a burst design gave "highly reliable" between-person estimates (adult work) — [NAU, ultra-brief WM ambulatory assessment](https://experts.nau.edu/en/publications/ultra-brief-assessment-of-working-memory-capacity-ambulatory-asse/)
- Trial count needed for a target reliability can be predicted per task from population statistics (the "C coefficient"). A free web tool estimates trials needed — [Kadlec et al. 2024, Communications Psychology (author post)](https://communities.springernature.com/posts/behind-the-paper-a-measure-of-reliability-convergence-to-select-and-optimize-cognitive-tasks-for-individual-differences-research); tool: https://jankawis.github.io/reliability-web-app/

### Inferences
- **Spearman–Brown (standard psychometric formula):** reliability of k parallel sessions = k·r / (1 + (k−1)·r). Applying it **[illustrative calc]**:
  - single-session r = 0.50 → 2 sessions ≈ 0.67, 3 sessions ≈ 0.75
  - r = 0.60 → 2 sessions ≈ 0.75
  - r = 0.40 → 2 sessions ≈ 0.57
  So a second administration (or a second parallel task on the same dimension) is worth about +0.15 to +0.17 at the moderate reliabilities children's brief tasks show. This assumes sessions are parallel. Practice effects (Q2) break that assumption somewhat, which is why the day-1 vs day-7 *difference* must also be modelled.
- **Prefer accuracy/commission-count measures over RT difference scores** for the baseline. In Hedge et al., go/no-go commission errors (.76) and error-based costs were generally more stable than RT costs or SSRT. Stars-not-clouds (go/no-go-like) is a reasonable anchor task for `impulse_control`. Navon/SNARC-style difference scores should not be used as single-task baselines.
- A 2–4 minute child task probably lands in the 0.4–0.65 range (inferred from the EF Touch single-task .52–.66 in 4-year-olds and Hedge's adult figures from far longer sessions). Our own pilot must confirm this. **A 12-dimension profile in which most dimensions rest on one brief task given once will have several dimensions below 0.6.** These should be reported with low confidence, not hidden.
- Dimension scores built from ≥2 tasks (e.g., `working_memory` from Copy the pattern + Follow instructions) should be more reliable than single-task dimensions, mirroring the battery-vs-task finding.

### Gaps
- No published test-retest data were found for 2–4 minute gamified tasks in Pakistani or South Asian children, or in Urdu.
- Hedge et al.'s Supplementary Material D (reliability vs trial count curves) was not retrieved. Exact trials-to-reliability figures per task type are therefore not given here. The Kadlec web tool could supply them.
- No reliability data were found specifically for ADHD/autistic child samples on brief tablet tasks. Reliability may differ, because higher within-child variability (common in ADHD) lowers it, and higher between-child variance raises it.

---

## Q2. Practice effects, fatigue/order effects, and fixed order vs counterbalancing

### Takeaway
Practice gains are largest from the first to the second exposure, and they also occur with alternate forms. For a within-child baseline whose purpose is comparison with the *same child later*, a **fixed order is the right choice**: every child, and every re-evaluation, sees the same order. Counterbalancing spreads order effects across people (useful for group means) but adds noise to individual scores. The cost is that fatigue and practice are confounded with day/position, so the fixed order must be designed to limit that confounding.

### Cited Findings
- In repeated computerized testing of youths, "the greatest gains in performance occurred between the first and second sessions, especially in younger participants". Gains continued after that for several functions, and **alternative versions did not eliminate practice effects**. What looked like accelerated development was "in most cases, attributable to learning" — [summary in search results; repeated Penn CNB-type study, eScholarship](https://escholarship.org/content/qt5032v9rb/qt5032v9rb.pdf) (note: the search snippet also reported older participants showing *larger* practice effects. Snippets conflicted on age direction. See Gaps.)
- In 277 children aged 6–13 tested 4 times about 6 months apart, mean processing-speed scores rose (Cross Out 18.41→23.68; Visual Matching 41.41→45.42) **[lit. estimate: Kail, Lervåg & Hulme 2015, Dev Sci]**. This mixes development and practice and cannot separate them — [PMC4860185](https://pmc.ncbi.nlm.nih.gov/articles/PMC4860185)
- Hedge et al. report practice effects as systematic between-session variance in adults over 3 weeks. Individual-difference variance, not practice, was the main reliability problem — [Hedge et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5990556)
- NIH Toolbox reliability improved from Year 2→3 compared with Year 1→2, which the authors read as possible practice effects even at year-long intervals — [PMC8589010](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589010/)
- **Counterbalancing trade-off.** Counterbalancing "does not completely eliminate order effects, it hides them". It can add individual order effects into treatment variance, which increases within-condition variance — [MSU Moorhead course notes on within-groups designs](https://web.mnstate.edu/malonech/Psy633/Notes/633%20Experimental%20designs%20-%20Within%20groups.doc)
- **ADHD and time-on-task.** Controls sustained performance over a virtual-classroom task, but children with ADHD showed a significant decline over time on task. The authors suggest this vulnerability "could explain part of their difficulties" — [Bordeaux Neurocampus summary of virtual-classroom time-on-task study](https://www.bordeaux-neurocampus.fr/?p=90347)

### Inferences
- **Which tasks show the biggest practice gains (inferred from the above plus general psychometric knowledge, needs pilot confirmation):** speeded tasks and novel-rule/strategy tasks (pattern copying, rule-switching, unfamiliar game mechanics) gain the most on second exposure, because children learn the interface and find a strategy. Vocabulary or comprehension-of-content tasks gain less on mechanics but can gain from *item memory* if the same items repeat. Simple go/no-go accuracy is likely more stable.
- **Fixed order is correct for this app, with three mitigations:**
  1. Put a short, unscored warm-up/tutorial before each task's first scored block, so the interface-learning part of the "first-session jump" is absorbed outside the score. This is the cheapest practice-effect control.
  2. Avoid putting the most attention-demanding tasks (sustained attention, distraction) last in a day. In ADHD, time-on-task decline is itself a confound, so position should be early and *consistent across re-evaluations*.
  3. Use the **same order and the same day-position at every 6–8-week re-evaluation**. The confound then becomes constant within child and cancels when comparing the child with themself, which is the only comparison this app makes.
- The day-7 repeat gives a direct within-week estimate of practice + day-to-day noise for those tasks. Day-7 minus day-1 should be modelled as "practice-inflated retest", not as growth.
- Expect the first re-evaluation (week ~7) to show *some* gain from practice alone. The reliable-change threshold (Q6) and a practice-adjustment term are needed before telling a parent "improved".

### Gaps
- No meta-analytic practice-effect sizes (Cohen's d by domain) for 5–12-year-olds on brief tablet tasks were retrieved. Adult meta-analyses exist (e.g., Calamia et al. 2012) but were not fetched and should not be imported without checking.
- The age direction of practice effects (larger in younger vs older children) was contradictory in the retrieved snippets. I could not verify it from the primary text.

---

## Q3. Which tasks benefit most from a day-7 repeat, and is 2 enough?

### Takeaway
Repeat the tasks whose dimensions are (a) highest-stakes for plan assignment, (b) lowest single-session reliability, and (c) most practice/state-sensitive. Two repeats give a consistency check for two dimensions only. To give every *plan-driving* dimension at least two observations, about 4–5 short repeats spread over days 5–7 are better, or a second distinct task per dimension.

### Cited Findings
- Single-task scores in young children were moderate (r ≈ .52–.66) while multi-task/multi-occasion composites were high (φ = .95) **[lit. estimate: EF Touch]** — [FPG/UNC](https://fpg.unc.edu/publications/test-retest-reliability-new-executive-function-battery-use-early-childhood)
- RT-difference and SSRT-type measures were the least stable (.36–.66 RT costs; SSRT .36/.49), while commission-error counts were the most stable (.76) **[lit. estimate: Hedge et al. 2018]** — [PMC5990556](https://pmc.ncbi.nlm.nih.gov/articles/PMC5990556)
- Children with ADHD show time-on-task decrements that controls do not, so attention measures are especially state- and position-sensitive — [Bordeaux Neurocampus](https://www.bordeaux-neurocampus.fr/?p=90347)
- Averaging multiple occasions is the main lever for reliable individual estimates in burst designs — [PMC3633558](https://pmc.ncbi.nlm.nih.gov/articles/PMC3633558)

### Inferences
- **Highest value to repeat (inferred):**
  1. The `sustained_attention`/`impulse_control` anchor (Stars not clouds). It drives the `focus_attention` rule, is state-sensitive in ADHD, and the current design already repeats it.
  2. The `articulation`/`expressive_language` anchor (Speak this line). It drives `speech_language`, and ASR-based scoring adds measurement noise. Already repeated. Keep it, but note it is Phase 3 for scoring.
  3. One `social_communication`/`emotion_recognition` task (How does she feel?). It drives `social_emotional`, and that dimension otherwise rests on few trials.
  4. The `self_confidence` signal (Oops try again / Level choice). It drives `confidence_builder`, which is behavioural and likely day-to-day variable.
  5. `working_memory` (Copy the pattern), if it is to be wired into a rule later.
- Dimensions that are *not* plan-driving yet (e.g., `reading_comprehension`, `distractibility`) can live with one observation and an explicitly low confidence for the first cycle.
- **Two repeats is enough only as a sanity check of the pipeline. It is not enough as a reliability basis for a 5-module plan engine.** Each of the 4 rule-driving module groups should have ≥2 observations (two sessions, or two tasks) before the rule may fire with `confidence ≥ 0.5`.

### Gaps
- No empirical study was found that compares "repeat 2 of N" against "repeat k of N" for child baseline batteries. The recommendation above follows from Spearman–Brown logic and the battery-vs-single-task evidence, not a direct trial.

---

## Q4. Is 20 activities over 7 days too many? Session length and breadth vs depth

### Takeaway
10–15 minutes/day is short compared with clinical norms, and fits well within child attention limits. The problem with 20 activities is not total time. It is **trials per dimension**: about 100 minutes spread over 20 activities gives about 3–5 minutes per activity, and some dimensions get a single brief task. The evidence (composites beat single tasks, more trials raise reliability) favours **fewer, longer, repeated tasks**. About 12–14 tasks, with 4–6 repeated or paired, would likely give more reliable plan-driving scores than 20 one-shot tasks.

### Cited Findings
- Clinical norms: examiners typically avoid sessions longer than about 2 hours for an 8-year-old, and break adolescent testing into about 1.5-hour sessions. Breaks between all tests are advised even when the child says none are needed **[lit. estimate: practitioner guidance, low-quality source]** — [practitioner overview (non-peer-reviewed)](https://sales.communityimpact.com/?p=43112)
- In ADHD, performance declines with time-on-task where controls stay level — [Bordeaux Neurocampus](https://www.bordeaux-neurocampus.fr/?p=90347)
- Battery/composite scores are "appreciably stronger" than single-task scores for individual differences in young children — [FPG/UNC EF Touch](https://fpg.unc.edu/publications/test-retest-reliability-new-executive-function-battery-use-early-childhood)
- Reliable individual-difference estimates need adequate trial counts. The number required differs by task and can be estimated (C coefficient) — [Kadlec et al. 2024](https://communities.springernature.com/posts/behind-the-paper-a-measure-of-reliability-convergence-to-select-and-optimize-cognitive-tasks-for-individual-differences-research)
- Gamified tests often measured more than one domain at once (e.g., a Whack-a-Mole task correlated r = .60 with inhibition and r = .35 with updating) **[lit. estimate: Lumsden et al. 2016]**. Many shallow, game-rich tasks therefore risk mixed-domain scores — [Lumsden et al. 2016, JMIR Serious Games](https://pmc.ncbi.nlm.nih.gov/articles/PMC4967181)

### Inferences
- Total daily time (10–15 min) is appropriate and should not grow. Keep 2–3 activities/day, not 4, for 5–7-year-olds and for children showing comfort signals (skips/quits).
- **Breadth vs depth:** 12 dimensions × a few brief trials each gives a wide but noisy profile. Because the plan engine only fires on `score < 40 AND confidence ≥ 0.5`, noisy dimensions mostly yield low confidence and so do not fire. Breadth then buys little action. Depth on the dimensions the rules actually read (attention/impulse, articulation/expressive, social/emotion, self-confidence, sensory) buys more.
- Candidate consolidation (inferred, for content-team review): merge overlapping tasks where two activities feed the same dimension with similar mechanics. Move tasks for dimensions not yet wired to rules (`reading_comprehension`, parts of `auditory_comprehension`) to after week 1, or keep them as single low-stakes observations.
- Minimum trials per dimension is a pilot question. Literature-guided starting points are in the Recommendations below, labelled as such.

### Gaps
- No peer-reviewed source was retrieved for an "optimal" daily session length for tablet assessment in 5–12-year-olds or in autistic children specifically. The clinical session-length guidance found is non-peer-reviewed.
- No direct evidence was found on autism-specific fatigue curves for tablet tasks.

---

## Q5. Engagement design that does not contaminate measurement

### Takeaway
Gamification reliably raises motivation, but there is **no evidence that it improves data quality, and some evidence that it can worsen it**. Extra game mechanics (sounds, rich feedback) can slow responses or blend domains. Keep game elements minimal and constant across every child and every re-evaluation. Keep them off the timing-critical channel. Treat skips and quits as informative missingness, never as zero scores.

### Cited Findings
- Systematic review of 33 studies / 31 gamified tasks: gamified tests were typically validated against traditional measures (correlations around .45–.60 in simpler studies), but there was "no evidence to support that gamified tests can be used to improve data quality", with indications it "may actually worsen it" **[lit. estimate: Lumsden et al. 2016]** — [PMC4967181](https://pmc.ncbi.nlm.nih.gov/articles/PMC4967181)
- Sound effects added to a visual-search task increased reaction times without improving engagement. "Innocuous" mechanics can harm measurement — [Lumsden et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4967181)
- In a working-memory trainer, the largest training effect came from versions with *minimal* motivational features — [Lumsden et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4967181)
- Children with ADHD using a gamified version completed more trials (≈199 vs ≈134) with higher accuracy (69% vs 51%) than the non-gamified version **[lit. estimate: Lumsden et al. 2016, describing the Supermecha study]**. Engagement can raise trial count, which helps reliability — [Lumsden et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4967181)
- One gamified test ("Retirement Party") failed to detect deficits that traditional tests identified. Game mechanics can *mask* the very differences being measured — [Lumsden et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4967181)
- Only 5 of 33 papers reported power calculations, and most were small pilots — [Lumsden et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4967181)

### Inferences
- **Design rules (inferred from the above):**
  - Feedback and reward animations happen *between* trials or blocks, never during a stimulus/response window. Fixed-length reward animations keep inter-trial timing constant.
  - Effort-based rewards (stars for finishing a block, not for accuracy) satisfy rule #5 (no fail states). They also avoid accuracy-contingent reward changing motivation differently for high and low performers.
  - Neutral, non-punitive response to errors (no buzzer, no red X). The trial simply advances. This also keeps error-related arousal from leaking into the next trials.
  - Sensory settings (calm mode, volume) should be logged per run. If they change stimulus salience on timing tasks, they become a measurement covariate. This connects to the PROJECT.md §12 finding that stimulus salience moves RT/accuracy in autism/ADHD.
  - The same game skin for every child during week 1. Theme personalisation only after baseline, and pinned while trending (already in PROJECT.md §12).
  - Micro-breaks: a child-initiated pause button that freezes the trial clock. Paused time is excluded from RT and logged as a comfort signal.
- **Skips/quits and missing data (inferred, standard missing-data reasoning):**
  - A skip or quit is very likely *missing not at random*: children may quit the tasks they find hardest. Imputing zero, or ignoring the gap and scoring only completed trials, both bias the score, in opposite directions.
  - Recommended handling: score only from completed trials. Reduce confidence in proportion to the missing fraction. Record the skip/quit as its own `self_confidence`/`sensory_regulation`-relevant signal. Offer the task once more later in the week (non-punitively, as "want to try this one again?") before marking the dimension low-confidence. Never convert a quit into a low skill score.
  - A partially completed block (e.g., 12 of 30 trials) should still contribute, weighted by trial count.

### Gaps
- No direct study was found on reward schedules (fixed vs variable ratio) in child cognitive *assessment*, as opposed to training, that measured reliability effects.
- No study was found that quantifies how "no-wrong-signal" feedback changes reliability compared with standard accuracy feedback in children.

---

## Q6. Confidence modelling, SEM and reliable change for within-child tracking

### Takeaway
Use classical test theory. SEM = SD·√(1 − r). Reliable change (Jacobson & Truax) needs |Δ| > 1.96·√2·SEM. With child brief-task reliabilities around 0.5–0.7, the reliable-change threshold is large (roughly 1.5–2 SDs). Confidence should be a function of estimated reliability for *this child's* data (trial count via Spearman–Brown, completion, data-quality flags), and change claims should require crossing the RCI.

### Cited Findings
- Jacobson–Truax: SE of measurement = SD·√(1 − reliability). SE of the difference = √(2·SEM²). Reliable-change criterion = 1.96·SE_diff, i.e., RC = 1.96·SD₁·√2·√(1 − r). |RCI| > 1.96 indicates statistically reliable change at 95% — [psyctc.org, Reliable and clinically significant change](https://www.psyctc.org/stats/rcsc.htm); [psyctc RCSC page](https://www.psyctc.org/psyctc/root/stats/rcsc/)
- Critiques: the JT index is simple but imprecise, and it does not separate individual from group-level benefit — [the Behavior Therapist 2025, Intro to Reliable Treatment Change](https://digitaleditions.sheridan.com/article/Introduction+to+Reliable+Treatment+Change%3A+Individual+and+Group+Applications/4959365/844132/article.html)
- Short-interval reliability (NIH Toolbox 0.76–0.99 at 1–3 weeks) is much higher than long-interval stability (0.48–0.64 at 3 years), and 14–78% of children moved >1 SD between years. True developmental change and noise both enlarge apparent change over long gaps — [PMC8589010](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589010/)
- Practice effects inflate retest scores, so a practice-adjusted RCI (subtracting the expected practice gain) is needed for repeated testing — inferred from the practice-effect evidence in [eScholarship repeated-testing study](https://escholarship.org/content/qt5032v9rb/qt5032v9rb.pdf) and [Hedge et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5990556)

### Inferences
- **Illustrative reliable-change thresholds on a 0–100 score with SD = 15 [illustrative calc; SD is an assumption]:**
  - r = 0.5 → SEM ≈ 10.6, SE_diff ≈ 15.0, RC ≈ **29 points**
  - r = 0.6 → SEM ≈ 9.5, SE_diff ≈ 13.4, RC ≈ **26 points**
  - r = 0.7 → SEM ≈ 8.2, SE_diff ≈ 11.6, RC ≈ **23 points**
  - r = 0.8 → SEM ≈ 6.7, SE_diff ≈ 9.5, RC ≈ **19 points**
  - Implication: with single brief tasks, only large changes can honestly be called "improved". Raising reliability from 0.5 to 0.75 by aggregating two sessions cuts the threshold by about a third.
- **Proposed confidence function (design suggestion, not a published standard):**
  1. Start from a per-task reference reliability r₀ at a reference trial count n₀. Initially take it from the literature ranges above, labelled as a placeholder. Replace it with pilot ICCs.
  2. Adjust for this child's actual trial count n via Spearman–Brown: r_child = (n/n₀)·r₀ / (1 + (n/n₀ − 1)·r₀).
  3. Combine tasks or sessions on the same dimension the same way (k observations).
  4. Multiply by data-quality factors in [0, 1]: completion fraction, a validity flag (e.g., implausibly fast RTs < ~150–200 ms or a response-pattern check such as all-same responses), and an environment flag (paused or interrupted runs).
  5. Map to confidence = r_child × quality. The existing rule `confidence ≥ 0.5` then roughly means "estimated reliability at least 0.5 after quality penalties". This makes the threshold interpretable.
  6. Store r_child, n, k and the quality factors in `skill_scores.evidence` (rule #7, explainable).
- **For within-child change:** report change only when |Δ − expected_practice| > RC computed from the *lower* of the two occasions' reliabilities. Otherwise say "no reliable change yet", which is honest and non-judgemental. Also consider a 90% (1.645) criterion for "possible change" messaging to parents, labelled as tentative.
- Temporal weighting (already logged in PROJECT.md §12 as future work) fits here. Recent sessions can carry more weight in the Learner State, but the baseline itself should stay a fixed snapshot.

### Gaps
- No published reference reliabilities exist for this app's specific tasks. Every r₀ is a placeholder until a pilot test-retest (e.g., ≥30 children, 1–2-week interval) is run.
- A score SD on the 0–100 scale is undefined until the scoring transform is fixed. The illustrative SD = 15 is arbitrary.
- No child-specific literature on practice-adjusted RCI values for brief tablet tasks was retrieved.

---

## Q7. Missed days and multi-day spread

### Takeaway
Spreading tasks over days (a burst design) is supported. Averaging across occasions improves reliability, and short daily sessions limit fatigue, especially in ADHD. Gaps between days within a 1–3-week window are unlikely to matter much. Short-interval retest reliability is high, and the big instability shows up at year-scale intervals. Completion-based day progression (already implemented: a missed calendar day costs nothing) is consistent with this.

### Cited Findings
- Measurement-burst designs (intensive repeated assessment over days/weeks) improve precision through aggregation — [PMC3633558](https://pmc.ncbi.nlm.nih.gov/articles/PMC3633558); [Cambridge Element on burst designs](https://core-cms.cambridgecore.org/core/elements/measurement-burst-designs-to-improve-precision-in-peer-research/41CE5FA0FE9825A8027460F7E309B6CC)
- Short-interval (7–21 day) child retest ICCs of 0.76–0.99 vs 0.48–0.64 at 3 years **[lit. estimate: NIH Toolbox]** — [PMC8589010](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589010/)
- EF Touch retest at a median of 16 days still gave a battery-level φ of .95 in preschoolers — [FPG/UNC](https://fpg.unc.edu/publications/test-retest-reliability-new-executive-function-battery-use-early-childhood)
- Time-on-task decline in ADHD argues against a single long sitting — [Bordeaux Neurocampus](https://www.bordeaux-neurocampus.fr/?p=90347)

### Inferences
- Record *calendar span* (first-to-last day) and time of day per session. If week 1 stretches beyond about 3 weeks, flag it in evidence. Development and life events start to enter, and the day-1 vs day-7 repeat comparison partly reflects true change.
- Time of day is a state covariate (tiredness after school, hunger). Log it and, if feasible, nudge guardians toward a consistent time, without making it a requirement.

### Gaps
- No study was found that directly compares "one sitting" with "spread over a week" for the same child tasks in 5–12-year-olds.

---

## Q8. Practical constraints in Pakistan

### Takeaway
Device access is near-universal at household level, but personal ownership is about half of individuals and internet about 57% of individuals. Expect shared phones and tablets, intermittent connectivity, and guardians with varied literacy. Child reading levels are low (about half of rural grade-5 children read a grade-2 Urdu story), so tasks must not depend on reading unless reading is the construct.

### Cited Findings
- HIES 2024–25 (Pakistan Bureau of Statistics): **96% of households** have a mobile/smartphone. Household internet is **>70%** (34% in 2019). Individual mobile/smartphone *ownership* rose from 45% (2019) to **50% (2025)**. Individual internet use went from 17% to **57%**. Provincial household internet: KP 77%, Punjab 69%, Balochistan 69%, Sindh 67% **[lit. estimate: HIES 2024–25 via press coverage]** — [PBS HIES 2024–25 results presentation](https://www.pbs.gov.pk/wp-content/uploads/2020/07/Final-Results-Presentation-HIES-2024-25-website-1.pdf); [APP news](https://www.app.com.pk/?p=1140479); [FAFEN on PSLM](https://fafen.org/pslm-mobile-internet-access-rises-computer-ownership-stays-flat/)
- ASER Pakistan 2023: 272,370 children aged 3–16 assessed. Only **49% of rural grade-5 children could read a grade-2 story in Urdu/Siraiki**. Out-of-school rate was 18% rural, 12% urban. Technology access has increased, but urban–rural gaps remain large **[lit. estimate: ASER Pakistan 2023]** — [ASER Pakistan 2023 national report (via stateofchildren.com)](https://stateofchildren.com/?p=7343)
- Madrasah enrolment is 13% rural vs 4% urban. Private school attendance is 27% rural, 35% urban — [ASER Pakistan 2023](https://stateofchildren.com/?p=7343)

### Inferences
- **Shared devices:** a household tablet or phone may be used by siblings. Require an explicit "who is playing?" child selector (avatar tap) at each session start, and flag sessions with improbable within-session pattern shifts. Wrong-child sessions corrupt the baseline more than missing sessions do.
- **Device heterogeneity:** the product targets Android tablets, but in practice many families may use a phone. Screen size and touch latency change RT. Log device model and screen size, and keep the baseline device constant for re-evaluations where possible (or flag a device change like a theme change: a baseline-comparability event).
- **Noise:** audio tasks (Speak this line, Story and questions) are most exposed. Measure ambient noise level before audio tasks (with consent) and treat a high-noise run as lower confidence, not lower skill. Visual cues should duplicate audio instructions.
- **Connectivity:** the offline-first event queue (already in the app plan) is essential. Scoring should never depend on a live connection during a task.
- **Guardian literacy:** onboarding and guardian-facing instructions need voice-over in Urdu (and regional language where possible) plus icons, not text alone. Guardian administration should be "hand the tablet to the child" simple.
- **Language of instruction:** keep the child's instruction language constant across baseline and re-evaluations. A language switch is a comparability event. For `reading_comprehension`, the ASER figures imply wide floor effects for younger and rural children. Expect many low-confidence or floor scores there, and do not treat floor as "need".

### Gaps
- No Pakistan-specific study was found on at-home, guardian-administered tablet cognitive assessment of children.
- No data were found on noise levels in Pakistani homes, or on the share of households where a tablet (as opposed to a phone) is available.
- Mothers' literacy figures from ASER/PSLM were not retrieved in this pass.

---

## Concrete recommendations (synthesis; every number is a literature-guided starting point or illustrative and must be replaced by pilot data)

1. **Number of activities: about 12–14 scored tasks instead of 20.** Prioritise the dimensions the plan-engine rules read. Fold overlapping tasks together. Move non-rule dimensions to single low-stakes observations or to post-week-1. Rationale: battery/composite and multi-occasion scores are far more reliable than single brief tasks (EF Touch .60 vs .95; NIH Toolbox composites > single tests).
2. **Repeats: 4–5, not 2.** Give every rule-driving module group at least 2 observations (a repeat session, or two distinct tasks on the same dimension): attention/impulse, speech, social-emotional, self-confidence, plus working memory if it gets wired. Spread repeats over days 4–7 rather than putting them all on day 7, so a single bad day does not sink all the repeats. Rationale: Spearman–Brown, about +0.15 reliability from a second session at r ≈ 0.5–0.6 [illustrative calc].
3. **Schedule principles:**
   - Same fixed order for every child and every re-evaluation, including the same within-day position.
   - Attention-heavy tasks early in each daily session. 2–3 tasks/day for younger children. 10–15 min total per day.
   - An unscored practice/tutorial block before each task's first scored trials.
   - Completion-based progression (already built). Log calendar span and time of day.
   - Child-controlled pause that freezes timing. Offer skipped tasks once more later in the week.
4. **Minimum trials per dimension (literature-guided placeholders, to be set from pilot reliability curves using a tool such as Kadlec et al.'s):** aim for enough trials that the *dimension* reaches estimated reliability ≥ 0.6 after aggregation. Practically, this means doubling exposure (two sessions or two tasks) on rule-driving dimensions rather than lengthening a single session past the child's comfort. Prefer accuracy/commission measures over RT difference scores, because they were more stable in Hedge et al.
5. **Confidence:** compute it as Spearman–Brown-adjusted reliability for this child's trial count and number of observations, times data-quality factors (completion, validity, interruption, noise, device change). Store every component in `evidence`. Keep `confidence ≥ 0.5` as the rule gate, but it now has a meaning.
6. **Reliable change:** report a change to guardians only when it exceeds a practice-adjusted Jacobson–Truax RC. Expect roughly 20–30 points on a 0–100 scale at reliabilities of 0.5–0.8 [illustrative calc, SD = 15 assumed]. Otherwise say "no clear change yet".
7. **Honest reporting of low-confidence dimensions:**
   - Show low-confidence dimensions as "still learning about this area", with a visual uncertainty band, never as a low score.
   - Never let a low-confidence dimension drive a plan module (already enforced by the `confidence ≥ 0.5` gate).
   - Explain *why* confidence is low in plain language ("only a few rounds played", "it was noisy", "this game was skipped") so guardians and therapists see the reason, not a judgement.
   - Skips/quits are never converted into low scores. They are recorded as comfort signals.
8. **Engagement without contamination:** minimal, constant game elements. Feedback and rewards between trials only. Effort-based rewards. No error sounds. Same skin for all children in week 1. Log sensory settings as covariates.
9. **Pakistan fit:** offline-first, voice-led Urdu instructions with icons, a "who is playing?" check each session, device/language/noise logged as comparability factors, and no reading dependence outside the reading task.
10. **Run a pilot test-retest before trusting any threshold:** same tasks, 1–2-week interval, a modest sample. Use it to replace every placeholder reliability, practice-gain and SD figure above.
