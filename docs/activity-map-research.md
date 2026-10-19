# Cut week one to fifteen deeper games

The research supports a smaller, deeper week 1. Instead of 20 one-shot activities, run **15 activities, 12 of them scored**, and repeat **5 of them** across days 4–7, so that every module the plan engine reads has at least two observations before a rule can fire. The reason is reliability. One brief child task usually reaches test-retest reliability of only about **.4–.7**, while composites and multi-occasion scores reach much higher. In 4-year-olds, single EF Touch tablet tasks averaged **r ≈ .60**, against a battery factor of **φ ≈ .95** ([FPG/UNC](https://fpg.unc.edu/publications/test-retest-reliability-new-executive-function-battery-use-early-childhood)). Activity by activity, the evidence says: keep the two attention cores (`stars_not_clouds`, `watch_the_pond`) as two phases of one game; fold `distraction_garden` into them as a distractor condition; drop `wait_for_the_bell` from week 1. Keep both working-memory tasks and `story_and_questions`, and gate `read_and_answer` behind a decoding check, because in Sindh **60% of grade-2 children scored zero on Urdu reading comprehension** ([EGRA Sindh 2024](https://rsusindh.gov.pk/rsusindh.gov.pk/contents/SELECT/EGRA_Baseline_Assessment_Report_Sindh.pdf)). In week 1, record audio for the speech tasks but do not score it. Move `which_word` from `articulation` to a new `speech_perception` dimension. Rename what `what_would_you_do` measures to `social_problem_solving`, and defer `chat_with_a_character`. Keep `mood_check_in` and `sensory_setup` as context and comfort signals, not as skill scores. The result is a 12-key skill model with **9 dimensions scored in week 1**, 2 captured for later scoring and 1 reserved. This has a direct consequence: the `speech_language` module cannot be assigned from week-1 data alone until a human-validated speech scoring pipeline exists. Almost every numeric parameter below is a literature estimate borrowed from a different population or a design proposal. A pilot test-retest study is required before any threshold is trusted.

**Reading conventions.** Every number in this report carries one of three tags. **[LIT]** means a literature estimate, with its source cited inline. **[DP]** means a design proposal with no direct source, to be tuned in the pilot. **[CALC]** means an illustrative calculation from a standard formula, not a measured property of this app. The hard constraints from the research notes and `PROJECT.md` apply throughout. No item wording, ordering or scoring is taken from any proprietary instrument; where one is cited (K-CPT, Raven matrices, CELF-type tests, SRS-2 and similar), only its published aggregate findings are used. No output contains a diagnosis label: "ADHD" and "autism" appear here only as research populations whose patterns affect design and confounds, never as child attributes. No activity has a fail state. Progress is compared only with the child's own baseline.

## Twenty one-shot games cannot carry twelve reliable scores

### Brief tasks are individually noisy, aggregates are not

The core problem with the current week-1 design is not total screen time; 10–15 minutes a day is modest. The problem is how few trials each dimension gets. The "reliability paradox" explains why. Classic cognitive tasks produce robust group effects precisely because people differ little on them, and low between-person variance gives low test-retest reliability. Across seven classic tasks, retest reliability ranged **from 0 to .82** [LIT], even with **600–720 trials per session** in adults ([Hedge, Powell & Sumner 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5990556)). The more stable measures were accuracy- and error-based. **Go/no-go commission errors reached ICC .76** in both studies, whereas RT-difference costs (.40–.66) and SSRT (.36/.49) were weaker [LIT] ([Hedge et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5990556)). In children, NIH Toolbox raw scores had **7–21-day ICCs of .76–.99** but only **.48–.64 over three years**, and **14–78% of children shifted by more than 1 SD** between years. Composites were more stable than single tests [LIT] ([Anokhin et al. 2022, PMC8589010](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589010/)).

Two design rules follow. First, aggregate: a second session, or a second task on the same dimension, is the cheapest large gain. Spearman–Brown gives **r = .50 → .67 with two sessions and .75 with three**, and **r = .60 → .75 with two** [CALC]. Second, prefer accuracy and commission counts over RT difference scores as baseline anchors. A 2–4-minute child task probably lands at **.4–.65** [CALC, inferred from EF Touch single-task r of .52–.66 and Hedge et al.]. On the current design, several of the 12 dimensions therefore sit below .6 and should be reported as low-confidence, not hidden.

Breadth also buys little action. The plan engine fires only when `score < 40 AND confidence ≥ 0.5`, so a noisy dimension mostly yields low confidence and never fires. Depth on the dimensions the rules actually read buys more. Gamified tests also tend to measure more than one domain at once. A Whack-a-Mole game correlated **r = .60 with inhibition and .35 with updating** [LIT] ([Lumsden et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4967181)), so many shallow, game-rich tasks risk mixed-domain scores. The recommendation is **about 12–14 scored tasks rather than 20**, with **4–5 repeats spread over days 4–7, not 2 on day 7** [DP]. That way each rule-driving module group (attention/impulse, social-emotional, self-confidence, and working memory once it is wired to a rule) gets at least two observations, and one bad day cannot sink every repeat.

### Fixed order, practice absorption and the day-7 repeat

Practice gains are largest from the first to the second exposure, especially in younger participants. Alternate forms do not remove them ([eScholarship repeated-testing study](https://escholarship.org/content/qt5032v9rb/qt5032v9rb.pdf)). For a baseline whose only purpose is comparing a child with themselves later, **a fixed order is correct**. Counterbalancing hides order effects inside individual scores rather than removing them ([MSU course notes](https://web.mnstate.edu/malonech/Psy633/Notes/633%20Experimental%20designs%20-%20Within%20groups.doc)). If every child and every 6-week re-evaluation uses the same order and the same within-day position, the order confound stays constant within each child and cancels out. Three mitigations make the fixed order safe [DP]:

1. **An unscored tutorial block before each task's first scored trials.** This absorbs the interface-learning jump.
2. **Attention-heavy tasks early in each day's session.** Children in the ADHD research population decline with time on task where controls do not ([Bordeaux Neurocampus](https://www.bordeaux-neurocampus.fr/?p=90347)).
3. **Day-7-minus-day-1 treated as a "practice-inflated retest", not growth.** The first 6-week re-evaluation will also show some gain from practice alone.

### Engagement without contaminating measurement

A systematic review of **33 studies covering 31 gamified tasks** found no evidence that gamification improves data quality, and some indication that it worsens it [LIT] ([Lumsden et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4967181)). Adding sound effects to a visual search task slowed reaction times without raising engagement. One gamified test failed to detect deficits that the traditional version identified. Engagement can still help reliability through volume: children in the ADHD research population completed **≈199 vs ≈134 trials, at 69% vs 51% accuracy**, in a gamified version [LIT] ([Lumsden et al. 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4967181)). The design rules that follow [DP] are:

- Rewards and animations only between trials or blocks, at a fixed length, so inter-trial timing stays constant.
- Effort-based rewards for finishing a block, never for accuracy.
- No buzzers, red marks or "wrong" signals; a trial simply advances.
- The same art skin for every child during week 1. Theme personalisation starts only after the baseline and stays pinned while scores are trended, as `PROJECT.md` §12 already requires.
- A child-controlled pause that freezes the trial clock.
- Sensory settings logged on every run as a measurement covariate.

Skips and quits are almost certainly missing-not-at-random: children quit the tasks they find hardest. Imputing zero biases the score down, and silently scoring only completed trials biases it up. The recommended handling [DP]:

- Score from completed trials only.
- Cut confidence in proportion to the missing fraction.
- Record the skip or quit as a comfort signal.
- Offer the task once more later in the week, non-punitively.
- Never convert a quit into a low skill score. A partial block still contributes, weighted by its trial count.

### Confidence should equal estimated reliability after quality penalties

Classical test theory gives a usable confidence model. SEM = SD·√(1 − r), and a Jacobson–Truax reliable change needs |Δ| > 1.96·√2·SEM ([psyctc.org](https://www.psyctc.org/stats/rcsc.htm)). The proposed confidence function [DP] works as follows:

1. Start from a per-task reference reliability r₀ at a reference trial count n₀. Use a literature placeholder until pilot ICCs exist.
2. Adjust to this child's actual trial count n, and number of sessions or tasks k, with Spearman–Brown.
3. Multiply by data-quality factors in [0, 1]:
   - completion fraction
   - validity flags (implausibly fast responses under ~150–200 ms [DP]; all-same response runs)
   - interruptions and pauses
   - ambient noise on audio tasks
   - device or language change
4. Set confidence = the adjusted reliability × the quality product, and store every component in `skill_scores.evidence` (rule #7).

The existing `confidence ≥ 0.5` gate then has a meaning: estimated reliability of at least .5 after quality penalties. On a 0–100 scale with an assumed SD of 15, reliable-change thresholds are large:

| Reliability r | SEM | SE of difference | Reliable change (95%) |
|---|---|---|---|
| .50 | ≈10.6 | ≈15.0 | **≈29 points** [CALC] |
| .60 | ≈9.5 | ≈13.4 | **≈26 points** [CALC] |
| .70 | ≈8.2 | ≈11.6 | **≈23 points** [CALC] |
| .80 | ≈6.7 | ≈9.5 | **≈19 points** [CALC] |

The lesson for parent-facing reporting is simple. With single brief tasks, only large changes can honestly be called improvement. Raising reliability from .5 to .75 by aggregating two sessions cuts the threshold by about a third [CALC]. Change should be reported only when |Δ − expected practice gain| exceeds the reliable-change threshold computed from the less reliable of the two occasions. Otherwise the message is "no clear change yet". A 90% criterion (1.645) can support a "possible change" message, labelled tentative [DP]. Low-confidence dimensions should appear as "still learning about this area", never as low scores, with a plain-language reason ("only a few rounds played", "it was noisy").

### Pakistan's constraints shape the whole week

According to HIES 2024–25 press coverage, **96% of Pakistani households have a mobile or smartphone**, but only **50% of individuals own one** and **57% use the internet** [LIT] ([PBS HIES 2024–25](https://www.pbs.gov.pk/wp-content/uploads/2020/07/Final-Results-Presentation-HIES-2024-25-website-1.pdf); [FAFEN](https://fafen.org/pslm-mobile-internet-access-rises-computer-ownership-stays-flat/)). Shared devices and intermittent connectivity should therefore be expected. Proposed responses [DP]:

- A "who is playing?" avatar tap at the start of every session. A session played by the wrong child corrupts the baseline more than a missed session does.
- Device model and screen size logged, with a device change treated as a comparability event, like a theme change.
- Offline-first scoring that never needs a live connection during a task.
- Voice-led Urdu or English instructions with icons for both child and guardian.
- The instruction language pinned between baseline and re-evaluations.
- Calendar span and time of day logged; if week 1 stretches beyond about 3 weeks, that is flagged in the evidence.

Spreading tasks over days is itself supported. Measurement-burst designs gain precision from aggregating across occasions ([PMC3633558](https://pmc.ncbi.nlm.nih.gov/articles/PMC3633558)), and short-interval retest reliability stays high ([PMC8589010](https://pmc.ncbi.nlm.nih.gov/articles/PMC8589010/)).

## Attention games: keep two cores, fold in distraction, drop the bell

The four attention activities map onto two empirically separable factors plus two weaker constructs. Clark et al.'s open "fishing game" (catch fish, avoid sharks) gave **452 children aged 3–12** a go/no-go phase and a CPT phase. Factor analysis produced two latent factors, **response inhibition and sustained attention**. Floor and ceiling effects were limited, and the scores were developmentally sensitive ([Clark et al. 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10041761)). That design is the template for this group. The proposal is to implement `stars_not_clouds` and `watch_the_pond` as **two phases of one game engine with one art style, played on different days**. This saves setup time and keeps each day's run near 4 minutes instead of Clark's ~8 [DP].

| Parameter | 5–7 | 8–10 | 11–12 | Basis |
|---|---|---|---|---|
| Stimulus / ISI | 750 / 750 ms | 500 / 500 ms | 500 / 500 ms, plus jittered ISI or lower no-go rate against ceiling | [LIT] Clark v2 (5–6 y) and v3 (7+ y); 11–12 adjustment [DP], informed by SART 1-in-9 no-go at 400 + 750 ms in ages 11–18 ([Dunning et al. 2021](https://www.mrc-cbu.cam.ac.uk/wp-content/uploads/www/sites/3/2021/06/Dunning-et-al.-2021.-SART.pdf)) |
| Scored trials per phase | ~80 | ~100 | ~100 | [LIT] Clark v2 / v3 |
| Go/no-go phase | 25% no-go | 25% no-go | ~11–25% no-go | [LIT] Clark; SART |
| CPT phase | targets rare, 25% | 25% | 25% | [LIT] Clark |
| Expected internal consistency | ω ≈ .64–.67 | ω ≈ .83–.85 (overall sample) | same | [LIT] Clark |
| Practice | short, animated, unscored | same | same | [DP] |

Applying 7+ timing to 7-year-olds would follow Clark's split, but it breaks the app's 5–7 band. Starting the whole 5–7 band at 750 ms is a design proposal.

### stars_not_clouds: the impulse_control anchor

This is a frequent-go **go/no-go** paradigm. Its validity for `impulse_control` is the best supported of any activity in the app: go/no-go commission errors were the most stable measure in Hedge et al. (**ICC .76**) [LIT]. In the meta-analysis of 47 child studies, commission errors showed a corrected effect of **δ ≈ 0.98** in the ADHD research population [LIT] ([Huang-Pollock et al. 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3664643)).

**Scoring [DP].** Compute commission rate, d′ (with a log-linear correction for 0% or 100% rates) and RT variability on correct go trials (ex-Gaussian τ or a robust CV). Map each to 0–100 with fixed, pre-declared anchors within the child's age-band version, for example **d′ 0 → 0 and d′ ≥ 3 → 100**. Clark's age-adjusted versions kept commission rates at **.28–.33 across bands, with d′ of 1.84, 1.68 and 1.24** (from the youngest to the oldest version) [LIT]. Those values come from progressively harder versions, so they cannot be used as developmental norms.

**Confidence [DP].** Cap a single 5–7 run near the **~.65** internal consistency that Clark found for that age [LIT anchor]. Allow up to ~.85 only after the repeat run. Raw scores, not norm-referenced ones, are the right currency: CPT raw-score ICCs of **.62–.82** fell to **.33–.65** for normed T-scores [LIT] ([PMC2899676](https://pmc.ncbi.nlm.nih.gov/articles/PMC2899676)). That fits rule #3.

**Confounds.** RT variability is the most robust signal in the ADHD research population (**g = 0.76** vs typical peers) but is barely specific (**g = 0.25** vs other clinical groups). Stimulants reduce it [LIT] ([Kofler et al. 2013](https://sciences.ucf.edu/psychology/childrenslearningclinic/wp-content/uploads/sites/24/2013/05/Kofler-et-al.-2013-RT-Variability-Meta-analysis.pdf)). In the autism research population, inhibition accuracy is relatively intact but RT variability and premature responses are elevated ([IMFAR 2010](https://imfar.confex.com/imfar/2010/webprogram/Paper6503.html)). RT variability is therefore a skill signal, never a marker. Medication on test day is real noise.

**Feedback.** Clark's game used buzzer and broken-net feedback on errors, which rule #5 forbids. The redesign uses a neutral pass (the star simply drifts by). That departs from the validated design, so reliability must be re-checked in the pilot.

**Localisation.** EF Touch, adapted for Pakistani preschoolers with Urdu audio, achieved **79–100% task completion**, showed **no DIF across income groups**, and hit a **21.7% ceiling on a 40-item go/no-go** [LIT] ([Toor & Hanif 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9477268/)). That ceiling argues for faster versions for older children. Experts replaced the pig stimulus. Stars and clouds are culturally neutral.

**Verdict: KEEP**, as the core `impulse_control` task, run twice (days 1 and 4).

### watch_the_pond: the sustained_attention anchor

This is a **rare-target CPT**. Meta-analytic effects in the ADHD research population are large for **omissions (δ 1.34)** and **SD-RT (0.93)**. **Performance-over-time effects are small (0.22–0.54)** even in 10–30-minute CPTs [LIT] ([Huang-Pollock et al. 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3664643)). At about 3–4 minutes, a first-half vs second-half decrement would rest on roughly 15 targets per half [CALC]. It should therefore be logged as an exploratory field and kept out of the 0–100 score.

**Scoring [DP].** Omission rate, d′, and τ or CV on hits, using the same anchor and confidence approach as `stars_not_clouds`.

**Development.** Sustained attention improves sharply between 6 and 8 and keeps improving towards about 15 ([J Abnorm Child Psychol 2020](https://www.doi.org/10.1007/s10802-020-00698-5); [Dunning et al. 2021](https://www.mrc-cbu.cam.ac.uk/wp-content/uploads/www/sites/3/2021/06/Dunning-et-al.-2021.-SART.pdf)). That supports age-banded timing. A change of band is a baseline reset.

**Verdict: KEEP**, as the CPT phase of the shared engine, run twice (days 2 and 6), and as the host for the distractor condition.

### distraction_garden: becomes a condition, not a game

This maps to the **irrelevant-distractor paradigm**. In adults, cartoon pop-ups on **10% of 480 trials** produced more than double the interference in the ADHD research group (**η²p = .231**), and high perceptual load removed distraction equally in both groups [LIT] ([Forster et al., PMC3906797](https://pmc.ncbi.nlm.nih.gov/articles/PMC3906797)). Children show the same effect at lower difficulty: 7-year-olds stop being distracted at a lower load than adults ([Frontiers for Young Minds 2017](https://kids.frontiersin.org/articles/10.3389/frym.2017.00008)). Novel environmental sounds distract children more than repeated ones, and distraction declines across ages 7–10 ([PMC7935912](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7935912/)).

Three problems weaken a stand-alone `distractibility` score. A difference score is less reliable than either of its parts. A short game yields few distractor trials. And children habituate to repeated distractors, which builds a practice confound into any day-1 vs day-7 comparison.

**Redesign [DP].** Place visual pop-ups and novel sounds on about 10% of `watch_the_pond` trials, on a fixed schedule that is the same for every child. Use **a different (fixed) distractor set on each run**. Score `sustained_attention` from clean trials only. Report "distractor cost" as a provisional sub-score in evidence. Perceptual load changes the cost, so a change of age band (which changes difficulty) resets the comparison.

**Verdict: MERGE** into `watch_the_pond`. Park `distractibility` as a scored dimension unless the pilot shows acceptable reliability for the cost score.

### wait_for_the_bell: a real construct, but a poor week-1 measure

This maps to **delay aversion** (DeFT-like waiting). The dual-pathway model separates inhibition from delay aversion, but delay-of-gratification measures cross-load on both ([PMC2565443](https://pmc.ncbi.nlm.nih.gov/articles/PMC2565443)). Children in the ADHD research population respond more during imposed delays ([Chan et al. 2024, PMC12062859](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12062859/)). Early taps are low-frequency events. No child reliability data for waiting tasks were found. Early taps are also ambiguous: premature responding (autism research population) and delay frustration (ADHD research population) both inflate them, for different reasons.

**Verdict: DROP from week 1 (defer).** Its time is better spent on the `stars_not_clouds` repeat. If the owner wants it, keep at most a ~1-minute provisional contributor to `impulse_control`, with low confidence [DP].

## Memory and comprehension: keep all four, but gate reading

### follow_instructions: verbal working memory through enactment

This is Gathercole and colleagues' non-proprietary **following-instructions paradigm** ("touch the red pencil, then…"). Children are reliably better at enacting the sequence than at repeating it ([PMC3901937](https://pmc.ncbi.nlm.nih.gov/articles/PMC3901937)), which makes tap-it-out a natural fit for a tablet. Screen-based versions were closely linked with verbal working memory in **42 children aged 7–11** [LIT] ([Jaroslawska et al., UEA](https://ueaeprints.uea.ac.uk/id/eprint/81797)).

**Structure [DP], following the paradigm.**
- A fixed array of 6–9 coloured shapes.
- The spoken instruction plays as fixed recorded audio while the board is inert.
- After a "go" cue, the child taps the sequence.
- Lengths start at 2 actions, after a 1-action practice item, and rise by 1.
- Bands: 5–7 uses lengths 1–5; 8–10 goes up to 6–7 with spatial and temporal words ("before", "under"); 11–12 adds conditionals.

Sequence length and linguistic complexity are logged as separate parameters.

**Scoring.** Use **partial credit** (actions in the correct serial position) plus highest length fully correct. All-or-nothing span scoring is significantly less reliable ([Conway et al. 2005](https://link.springer.com/article/10.3758%2FBF03196772)). In **34 children aged 8–13 from the ADHD research population**, giving all trials and counting items correct improved validity, while traditional scores predicted neither criterion working memory nor achievement [LIT] ([Wells, Kofler et al. 2018](https://psy.fsu.edu/clc/Publications/Wells2018.pdf)). The proposed 0–100 score is 100 × (partial-credit items ÷ items presented across the band's length range) [DP].

**Confound.** For 5–7-year-olds and bilingual children, colour and shape vocabulary is a confound. A receptive pre-check ("tap the red one") in the instruction language should run first. Failures are logged as a language flag, not a working-memory score. Separately from errors, log repeat requests, early taps and lapses (no response within a set time).

**Gaps.** No Urdu study and no per-year norms were found.

**Verdict: KEEP.** It feeds `working_memory` (`wm_verbal` sub-score), and `auditory_comprehension` only when the vocabulary check passes.

### copy_the_pattern: the most sensitive task in the battery

This is **Corsi block-tapping**, the standard non-proprietary visuospatial span task. On a tablet, eCorsi produced spans essentially equivalent to the physical board in **107 adults** [LIT] ([Brunetti et al. 2014](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4151195/)). Visuospatial central-executive working memory showed the largest difference in the ADHD research population of any working-memory domain, **effect size 1.06 (CI 0.72–1.39)** [LIT] ([Martinussen et al. 2005](https://pubmed.ncbi.nlm.nih.gov/15782085/)). Span rises with age and plateaus in early adolescence, with **no difference between 14 and 21** in 340 participants [LIT] ([Farrell Pagulayan et al. 2006, via summary](https://en.wikipedia.org/wiki/Corsi_block-tapping_test)). The 11–12 band is therefore close to, but not at, the ceiling.

**Structure [DP], on eCorsi defaults [LIT].**
- 9 identical locations in an irregular layout.
- Start at length 2, with **2 trials per length**.
- Continue while at least 1 of the 2 trials is correct.
- Give **one extra length past the discontinue point**, and score partial credit (Wells/Conway).
- Present lengths as "levels" with a neutral end, and keep the stop rule invisible to the child.

Locations stay identical, with no colours or tones. Simon-style colour and tone coding invites verbal recoding and blurs the task into `follow_instructions`. **Forward span only for 5–7.** An optional backward block for 8+ provides headroom, but it is not a separate construct: forward and backward span load on one short-term memory factor ([Wells et al. 2018](https://psy.fsu.edu/clc/Publications/Wells2018.pdf)). Adaptive spans cannot use α, so reliability has to come from the repeat.

**Confidence [DP].** At most ~0.5 after one run. Average the span across days 3 and 7.

**Gaps.** Per-year Corsi spans for ages 5–12 were not retrievable. The commonly quoted "3–4 at age 5, rising to 5–6" is unverified and must be checked against Farrell Pagulayan's tables before floors and ceilings are set.

**Verdict: KEEP.** It feeds `working_memory` (`wm_visuospatial` sub-score) and is repeated. Keep both working-memory tasks: verbal and visuospatial storage are separable from age 4–6 ([Alloway, Gathercole & Pickering](https://durham-repository.worktribe.com/output/1555279/verbal-and-visuospatial-short-term-and-working-memory-in-children-are-they-separable); [Gathercole et al. 2004](https://eprints.whiterose.ac.uk/5942/)). A verbal–spatial discrepancy is useful plan-engine information, not a label.

### story_and_questions: the comprehension measure that works for every child

This is **narrative listening comprehension with literal and inferential questions**. Portuguese grade 1–4 tests reached **α > .70 with 30 Rasch-scaled items** (n = 1,042 narrative, 848 expository), but early versions lacked hard items [LIT] ([Santos et al. 2015](https://www.cambridge.org/core/journals/spanish-journal-of-psychology/article/development-of-listening-comprehension-tests-with-narrative-and-expository-texts-for-portuguese-students/1CB8A3441312304564AA82C2771AE127)). The ICNA uses **19 within-story causal-inference questions** for ages 3–6, is explicitly criterion-referenced, and notes that young children respond better when an adult asks the questions [LIT] ([ICNA manual](https://lel.crires.ulaval.ca/cms/1691721704987-techical-manuel_icna_jan-2023.pdf)). EGRA's **3 questions** are built for population monitoring and are far too few for an individual score. They still show how strongly language matters: Sindh grade-2 children scored **2.30/3 in Urdu-medium schools vs 1.66/3 in Sindhi-medium schools** [LIT] ([EGRA Sindh 2024](https://rsusindh.gov.pk/rsusindh.gov.pk/contents/SELECT/EGRA_Baseline_Assessment_Report_Sindh.pdf)).

**Structure [DP].**
- 4 stories across week 1, two each on days 2 and 6.
- 60–120 seconds of fixed recorded narration each, with 2–4 illustrations.
- 4–5 picture-choice questions per story, giving **~16–20 items in week 1** and reaching 20–30 by the first re-evaluation.
- About 40% literal and 60% inferential questions, each tagged literal/inferential and social/non-social.
- Story length by band: 5–7 at 80–150 words with one goal; 8–10 at 150–250 words with two characters; 11–12 at 250–400 words with a mental-state twist for headroom.

**Pilot each question without the story** to remove passage-independent items. Allow **one replay**, logged, and score first-attempt and post-replay separately.

**Scoring [DP].** Score = 100 × proportion correct, with Rasch equating later. Confidence runs from about **0.3 at 5 items to about 0.8 at ~25 items**, anchored on the 30-item benchmark.

**Patterns in the autism research population.** Inferential comprehension is the area of difficulty even when word- and sentence-level language is adequate (**35 vs 32 children aged 5–6**) ([Griffith repository](https://research-repository.griffith.edu.au/items/9be2d792-2ac7-4900-a514-01d5715d9bf4)). Highly social texts are harder ([Brown, Oram-Cardy & Johnson 2013](https://imfar.confex.com/imfar/2012/webprogram/Paper9964.html)). The literal/inferential and social/non-social sub-scores therefore belong in evidence.

**Localisation.** Native-speaker narration; Pakistani settings (home, bazaar, school, cricket, Eid); no stories that hinge on fear or loss; story language pinned for the baseline.

**Verdict: KEEP.** It feeds `auditory_comprehension` and is the only comprehension estimate for non-readers.

### read_and_answer: must not produce a sea of zeros

This is **passage reading with comprehension questions**. Reading comprehension is decoding × language comprehension, and popular tests differ dramatically in how much each drives the score ([Keenan, Betjemann & Olson 2008](https://experts.colorado.edu/display/pubid_53767)). In the autism research population, the mean deficit is **g = −0.7**, but semantic knowledge and decoding predicted **57% and 55% of the variance**, and autism status alone does not predict a deficit [LIT] ([Brown et al. 2013](https://imfar.confex.com/imfar/2012/webprogram/Paper9964.html)). Hyperlexia (decoding far ahead of comprehension) is reported in **6–21%** of that population [LIT] ([Ostrolenk et al., INSAR 2018](https://insar.confex.com/insar/2018/webprogram/Paper28551.html)).

The decisive fact is local. In Sindh, Urdu-medium grade-2 children read a mean of **19.25 correct words per minute against a 50–80 standard**. **45% scored zero on fluency and 60% scored zero on comprehension** [LIT] ([EGRA Sindh 2024](https://rsusindh.gov.pk/rsusindh.gov.pk/contents/SELECT/EGRA_Baseline_Assessment_Report_Sindh.pdf)). Nationally, only **50% of grade-5 children could read a grade-2 Urdu story** in ASER 2023 (Sindh 38.5%, Punjab 65.1%) [LIT] ([Business Recorder](https://www.brecorder.com/news/amp/40232775)). An ungated reading task would floor for most 5–7-year-olds. A zero-heavy score has no reliability and is effectively a fail experience.

**Redesign [DP].**
1. **Decoding probe.** A 30–60-second probe that mirrors the ASER letter → word → sentence → story ladder, using the app's own items.
2. **Passages only for readers.** Children at sentence level or above get 3–5 levelled passages with 4–6 questions each.
3. **No score below sentence level.** Every other child gets `reading_comprehension` = "insufficient evidence" (confidence 0), not a low score that would push the plan engine.
4. **Decoding support logged.** Tap-to-hear-a-word is allowed and logged.
5. **Listening–reading gap.** One listening-equivalent passage gives this gap. A large gap points to decoding; reading well above listening suggests a hyperlexia-like profile, recorded as skills and never as a label.

**Localisation.** Large Nastaliq type. Diacritics at beginner levels, because Urdu without diacritics is less transparent, and words were named more slowly in Urdu than in Hindi ([Rao et al. 2011](https://oaktrust.library.tamu.edu/bitstream/1969.1/158732/1/Rao%2C%20Vaid%2C%20Srinivasan%20and%20Chen%202011.pdf)). Run the decoding gate and score separately per language, because levels differ across languages ([StoryWeaver](https://storyweaver.org.in/v0/blog_posts/19-re-levelling-stories-on-storyweaver)). No Urdu readability formula exists, so passages are levelled by length, word familiarity and sentence length.

**Verdict: REDESIGN** as decoding-gated and reader-only, on day 7.

## Speech tasks record audio now and score later; which_word changes dimension

The speech group has a measurement problem that no amount of task design can fix in week 1: **automatic scoring of Urdu child speech does not exist yet**. Child English ASR is still imperfect. Fine-tuning brought Whisper-Small's child WER from **13.93% to 9.11%** [LIT] ([arXiv 2309.07927](https://arxiv.org/pdf/2309.07927)). Primary-age read speech still ran **14.8% WER**, and non-native secondary-age read speech **24.8%** [LIT] ([University of Galway](https://research.universityofgalway.ie/en/publications/exploring-native-and-non-native-english-child-speech-recognition-/)). Adult Urdu reached only **33.68% WER after low-resource fine-tuning of Whisper-Small** [LIT] ([arXiv 2409.11252](https://arxiv.org/pdf/2409.11252)). ASR is least reliable on disordered child speech, which is exactly where articulation errors are ([ICLR-W 2025](https://mlanthology.org/iclrw/2025/adeyeyekayode2025iclrw-evaluating)).

The recommended path [DP] has three phases:
- **Phase A, week 1.** On-device voice-activity features (onset latency, speaking time, pauses, attempt vs no response) are emitted as events. Audio is stored via `POST /media/upload-url` only with audio consent (rule #6). No `skill_scores` are written for speak, name or retell. Any latency-only evidence is capped at **confidence ≤ 0.3**, so `p.low()` cannot fire on it.
- **Phase B.** A human rater scores a sample of recordings with a non-proprietary rubric, establishing ground truth and inter-rater reliability.
- **Phase C.** ASR plus LLM scoring, English first, marked `source=agent`/provisional until it agrees with Phase B ratings. Urdu comes last, pending a child Urdu speech corpus.

No-response trials are excluded from accuracy denominators and recorded as comfort signals. Shyness is a willingness signal, not a language score.

### speak_this_line: the best-evidenced language measure per minute

This is **sentence repetition (SR)**. In a multilevel meta-analysis covering **46 studies, 19 languages, 39 SR tasks and 4 scoring methods**, typically developing children outperformed children with developmental language disorder by **2.08 SD**. SR's usefulness held up across most task and study variations [LIT] ([Ward, Polišenská & Bannard 2024](https://openaccess.city.ac.uk/32966/1/WARD%20et%20al%20-%20meta%20analysis.pdf)). SR primarily tests lexical phonology and morphosyntax, plus verbal working memory. Because SR is robust across scoring methods, a cheap scheme is acceptable later: 0–3 per sentence, or proportion of words correct. Sensitivity and specificity fell below clinical thresholds in some samples ([ASHA Evidence Map](https://apps.asha.org/EvidenceMaps/Articles/ArticleSummary/f849b558-e711-44c1-84fa-37353619497f)), which supports using SR as a skill measure, never as a classifier.

**Structure [DP; no item-count source found].**
- **10–14 graded sentences**, from 3–4 words with a single clause up to 8–12+ words with embedding, negation, tense and plural morphology.
- Early stop after a run of low-scoring items.
- **Independently built Urdu and English sets, not translations.** LITMUS builds language-specific sets for the same reason ([PMC11202042](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11202042/)).

**Confounds.** Echolalia is not a confound here, because exact repetition is the correct response. Attention lapses in the ADHD research population depress SR, so use short items, a practice item and repeat-on-request.

**Verdict: KEEP**, capture-only, once in week 1 (day 4). The original day-7 repeat is reassigned to scorable dimensions; a second capture comes at re-evaluation.

### name_the_picture: retrieval latency plus an articulation sample

This is **confrontation naming**. Naming latency carries information that standard language tests miss in children with word-finding difficulties ([Open University ORO 16570](https://oro.open.ac.uk/16570)). Error types (semantic, formal, omission) separate groups ([PolyU](https://research.polyu.edu.hk/en/publications/picture-naming-in-children-with-and-without-specific-language-imp/)).

**Structure [DP].** **15–20 items**, chosen so that each picture also elicits a planned target phoneme in initial, medial or final position. One task then serves `expressive_language` (retrieval) and `articulation` (single words), which absorbs the separate articulation probe.

**Age-gating articulation [DP, from LIT].** Across 27 languages (none Urdu), **at least 93% of consonants are correct by 5;0**, and trills, flaps, fricatives and affricates come last [LIT] ([McLeod & Crowe 2018](https://pubs.asha.org/doi/10.1044/2018_AJSLP-17-0100)). In Urdu, **aspirated consonants are acquired last** ([JSLHR 2021 21-00148](https://pubs.asha.org/doi/10.1044/2021_JSLHR-21-00148)). Only **9 qualifying studies of Urdu speech-sound development** exist across 40 years. The claim that /ɽ/ and /ɣ/ may not be mastered until 5–7 comes only from a secondary practitioner site ([Bilinguistics](https://bilinguistics.com/languages/urdu-speech-and-language-development/)). The proposed gating:
- **5–7:** aspirates, retroflexes, /ɽ/, /ɣ/, fricatives, affricates and trills count as "emerging", not as errors.
- **8–10:** residual late-sound errors are low weight.
- **11–12:** near ceiling on single words, so SR and retell carry the sensitivity.

**Localisation.** A correct word in the other language counts as a correct retrieval, tagged `language=other`. Items need **name-agreement piloting** in Pakistan (roti, chappal, rickshaw, cricket bat, mango). The Pakistani USAT covers Urdu sounds, but its licence is unknown, so its items must not be copied ([JRCRS 2024](https://jrcrs.riphah.edu.pk/wp-content/uploads/2024/03/2024120104.pdf)).

**Verdict: KEEP and narrow**, capture-only, absorbing the articulation probe.

### which_word: measures hearing sounds, not producing them

This is **minimal-pair discrimination** (picture pointing). Children with speech-sound disorders tend to discriminate less well, but **the direction of the perception–production link is unresolved**: some children discriminate contrasts they cannot produce, and some do not ([PMC7201332](https://pmc.ncbi.nlm.nih.gov/articles/PMC7201332)). Feeding perception scores into `articulation` would move a production score on evidence about perception.

**Remap** it to a new `speech_perception` dimension. This is also the **only speech task fully scorable on the device today**, and the only one a child who declines the microphone can still do.

**Structure [DP].** **16–24 two-choice trials** across 3–4 contrasts, in the child's dominant language, with the second language optional.

**Urdu contrasts** that English lacks ([Redalyc](https://www.redalyc.org/journal/6638/663872611009/663872611009.pdf); [MIT fieldwork notes](https://people.csail.mit.edu/namin/oldschool/linguistics/fieldwork1.pdf)):
- aspiration (/p/–/pʰ/, /t̪/–/t̪ʰ/, /k/–/kʰ/)
- dental vs retroflex (/t̪/–/ʈ/, /d̪/–/ɖ/)
- voicing (/pal/–/bal/, where /bal/ "hair" can be pictured)

Items need picturable nouns and native-speaker and SLP review. For English, use voicing (pea/bee) and /s/–/ʃ/ (ship/chip). Avoid contrasts Pakistani English may not maintain. /v/–/w/ and /θ/–/t̪/ are an *unsourced hypothesis* to check, because scoring accent as error would break rule #3's spirit.

**Scoring [DP].** Chance-corrected: score = 100 × max(0, (p − .5)/.5). Confidence rises with trial count and falls if the RT pattern suggests random tapping.

**Verdict: KEEP and REMAP** to `speech_perception`.

### retell_the_story: richest data, highest scoring cost

This is **narrative retell scored for macrostructure** (story grammar: setting, initiating event, internal response, attempt, outcome). Fiction retell separated age groups better and had higher reliability than the comparison condition ([J Psycholinguist Res 2023](https://link.springer.com/article/10.1007/s10936-023-10007-y)). In the ADHD research population, a meta-analysis of **16 studies (n = 1,015)** found **less coherent narratives, a medium effect** [LIT] ([ADHD Evidence summary](https://adhdevidence.org/blog/meta-analysis-finds-narrative-language-impairment-in-youths-with-adhd)). Theme and outcome elements are the weak points ([CoDAS](https://scielo.br/j/codas/a/PK9GvdMh8gBLRHks9rcDP5M/?lang=en)), and methylphenidate improves retelling ([Bar-Ilan](https://cris.biu.ac.il/en/publications/methylphenidate-selectively-improves-story-retelling-in-children-/)), so retell is state-sensitive. Narratives in the autism research population contain fewer story elements, and the gap shrinks when demands are reduced ([IMFAR 2016](https://imfar.confex.com/imfar/2016/webprogram/Paper21377.html)).

MAIN offers a free, multilingual structure for ages 3–12: **4 stories in 2 parallel sets, 6 pictures each**. An **Urdu adaptation** exists that accounts for SOV order and postpositions ([Chan et al. 2020](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7714944/fullTextXML)).

**Design [DP].** Use MAIN's *structure* (a 6-picture goal–attempt–outcome story) with the app's own stories. Check MAIN's licence before reusing any of its content. Capture one story in week 1, then a parallel story at re-evaluation. A future scorer should mark chunks copied verbatim from the model story, which handles echolalia.

**Verdict: KEEP as capture-only** on day 7, with scoring **deferred** to Phase B/C.

## Social tasks: recognition and reasoning are scorable, conversation is not yet

### how_does_she_feel: valid paradigm, wrong faces available

This is **forced-choice basic-emotion labelling**, a valid non-proprietary paradigm for `emotion_recognition`. The obstacle is stimuli. The only well-validated child set found with South Asian models, CAFE, has **11 South Asian models out of 154**, and its licence for commercial app use is unverified ([CAFE-Ss paper](https://repository.nie.edu.sg/bitstreams/17f63782-2651-4137-8404-240c7f24bf12/download); [Princeton face database guide](https://libguides.princeton.edu/facedatabases)). Own-group faces matter: across 97 studies, recognition was **9.3% more accurate for own-culture expressions** [LIT] ([Elfenbein & Ambady 2002 via SWOV](https://swov.nl/en/publicatie/universality-and-cultural-specificity-emotion-recognition-meta-analysis)).

**Stimuli [DP].** Commission an original illustrated South Asian child-face set:
- several characters × 6 emotions plus neutral, at 2–3 intensities
- a range of skin tones, plus hijab, dupatta and topi variants
- validation with Pakistani adult raters (CAFE's **66–81%** adult agreement is a reference point [LIT], [Frontiers 2020](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.554821/full))

Illustrated faces also suit the autism research population: autistic children matched to controls recognised cartoon faces as accurately as controls, using a configural strategy they did not use for real faces ([Rosset et al.](https://mijn.bsl.nl/typical-emotion-processing-for-cartoon-but-not-for-real-faces-in/547186)). The corollary is that high cartoon accuracy should not be read as real-world emotion reading, and the evidence text should say so.

**Reliability needs volume.** A Tunisian test reached **α .88 with 114 static items**. FELT used **360 trials** for test-retest of **.76–.85**. Per-category subscales were less reliable (**.53–.75**) than totals [LIT] ([PMC8645551](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8645551/); [PMC5568997](https://pmc.ncbi.nlm.nih.gov/articles/PMC5568997); [Buffalo record](https://researchconnect.buffalo.edu/en/publications/psychometric-properties-of-the-cambridge-mindreading-face-voice-b/)).

**Structure [DP].**
- **12–18 trials per session**, run twice (days 2 and 6, with parallel sets A and B).
- One aggregate accuracy score. Per-emotion breakdowns go to evidence only.
- Confidence low to moderate, growing over sessions.
- Spoken label plus an icon button, so no reading is needed.
- Anticipatory taps under ~200 ms flagged [DP].

**Bands [DP from LIT].** Recognition of happy, sad and angry is high by age 5. Accuracy on scared and surprised rises from about **20–30% at 5 to 60–70% by 11**, and disgust barely improves (French-Canadian children, free labelling, overall **51% at 5 to 76% at 11**) [LIT] ([Maassarani et al. 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4044975)). The bands:
- **5–7:** happy, sad, angry and scared.
- **8–10:** add surprised and disgusted, with disgust down-weighted, plus face-in-context items.
- **11–12:** add intensity morphs (40/70/100%) for headroom.

**Confounds.** In the autism research population, the effect is **d = 0.80 shrinking to 0.41 after publication-bias correction** [LIT] ([Uljarevic & Hamilton 2013](https://mijn.bsl.nl/recognition-of-emotions-in-autism-a-formal-meta-analysis/555206)). In adults it is better explained by alexithymia than by autism itself ([Cook et al. 2013](https://openaccess.city.ac.uk/id/eprint/4539/)). In the ADHD research population, **SMD = 0.63** across 142 studies, largest for anger and fear [LIT] ([PubMed 38860431](https://pubmed.ncbi.nlm.nih.gov/38860431/); [Eur Child Adolesc Psychiatry](https://link.springer.com/article/10.1007/s00787-020-01709-y)). Part of that may be inattention, hence the RT quality flags.

**Localisation.** Child familiarity with the Urdu emotion words (khush, udaas, ghussa, dar, hairaan, and especially the word for disgust) needs local review.

**Verdict: KEEP and REDESIGN the stimuli**, repeated.

### what_would_you_do: measures social reasoning, not communication

This is a **social information processing (SIP) vignette**. A multiple-choice vignette taps interpretation, goals and response *evaluation and selection* (SIP steps 2–5). It does not tap real-time *enactment* (step 6) ([PMC8361679](https://pmc.ncbi.nlm.nih.gov/articles/PMC8361679)). The honest dimension name is therefore **`social_problem_solving`**, not `social_communication`. Published SIP work used **8 vignettes** (provocation and group entry) in a longitudinal study of **387 children**, coding open responses into categories with **κ = .91** [LIT] ([PMC2791956](https://pmc.ncbi.nlm.nih.gov/articles/PMC2791956)). That κ applies to coding open responses. No reliability exists for picture-choice versions in 5–7-year-olds.

**Original rubric [DP], using generic SIP vocabulary only.**
- Each illustrated, narrated scene offers one option per function, shuffled: assertive-prosocial, help-seeking, withdraw/avoid, retaliate.
- An optional "by accident / on purpose / don't know" intent question is recorded descriptively, never as a penalty.
- Scoring produces a **response-profile vector** and a **flexibility index**: does the child choose functions that fit the context?
- Any 0–100 summary is the proportion of context-appropriate choices, with appropriateness per scene set in advance by a **Pakistani reviewer panel**. Help-seeking from an elder or teacher counts as competent in many scenes rather than as "dependent".
- **6–8 vignettes across 3–4 context types**, run once on day 5. 5–7 gets 2–3 options.
- Every choice gets a neutral "what happens next", never "wrong".

**Confound.** The knowing-vs-doing gap: an anxious or older child can pick the "nice" option without being able to enact it ([Harms et al. 2010](https://www.researchgate.net/profile/Gregory_Wallace/publication/46108941_Facial_emotion_recognition_in_autism_spectrum_disorders_a_review_of_behavioral_and_neuroimaging_studies/links/0fcfd513e40bc00914000000.pdf)).

**Localisation.** Scenes such as joint-family sharing, the classroom "Miss", Eidi, cricket in the gali, and being teased about Urdu or English.

**Verdict: KEEP and RENAME/RESCOPE** to `social_problem_solving`. Do not merge with `how_does_she_feel`; face-in-context items bridge the two.

### chat_with_a_character: timing is ambiguous, content needs ASR

Without ASR, only voice-activity timing is available: turn taken or not, latency, overlap and turn duration. In the best study found, children in the autism research population responded *faster* than typical peers (**735 vs 871 ms**). Unfamiliar partners slowed responses by **186–353 ms**, and within-context test-retest was only **r ≈ .36–.66**. The authors warn that latency is not a competence proxy, since overlaps can signal shared attention [LIT] ([Cox, Fusaroli et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12517399/)). Another study reports the opposite direction for pauses ([Interspeech 2012](https://www.isca-archive.org/interspeech_2012/lunsford12_interspeech.html)). An animated character is an unfamiliar partner, so first-session latencies partly measure comfort. On-topic content, reciprocity and pragmatics need ASR plus NLP or human coding. On tablets, echo cancellation is needed for overlap detection.

**Verdict: DEFER** out of the week-1 schedule. Scoring of `social_communication` waits for the Phase 3 speech pipeline and SLP/teacher validation, consistent with D4 and `PROJECT.md` §12. If the activity runs later, compute timing on the device without storing audio, and never map latency onto a better/worse scale.

## Confidence and comfort: three behavioural facets, two context signals

### about_me: self-report is positive and coarse until about 8

Children under 5 cannot validly self-report. Those aged 7 and under think dichotomously and need about two options, and their face-scale answers are skewed to the extremes. From about 8, children can use 4–5-point scales [LIT] ([Coombes et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8233251/)). Social comparison and more accurate self-appraisal arrive around 8 ([Belsky](https://digfir-published.macmillanusa.com/belsky4e/belsky4e_ch6_3.html)). Young children distinguish only two broad self-concept factors, general competence and social acceptance ([PMC5969031](https://pmc.ncbi.nlm.nih.gov/articles/PMC5969031)). The "some kids… other kids" format has mixed support. An adolescent meta-analysis found **lower criterion validity** and higher cognitive load than direct questions ([Yeager & Krosnick](https://web.stanford.edu/dept/communication/faculty/krosnick/docs/2011/Some%20other%20adolescents%20-%20Developmental%20Psych%20PUBLISHED.pdf)), so it should not be the default.

The positive illusory bias, where children inflate their own competence, is confined to a subgroup of the ADHD research population; cluster analysis found positive-bias, negative-bias and (largest) accurate groups ([ADHD Atten Def Hyp Disord 2010](https://link.springer.com/doi/10.1007/s12402-010-0043-x)).

**Redesign [DP].**
- **6–8 original two-picture items**, each a concrete behaviour (keeps trying a puzzle vs stops), not an abstract trait.
- Half the items reverse-keyed, to detect same-side and all-positive runs.
- Pictures balanced so the lower-confidence option is not drawn sad. Pictures carry their own meaning ([Reynolds-Keefer & Johnson](https://www.semanticscholar.org/paper/Validity-Issues-in-the-Use-of-Pictorial-Likert-Reynolds-Keefer/f9f1c6f3e6b12f23041709bf4b251fad5be77e6f)).
- Identical items at every re-evaluation.
- Score = proportion of confidence-keyed choices.
- **Confidence caps of 0.3 / 0.5 / 0.7 for the three bands**, lowered further when an acquiescence run is detected.
- Behaviour items preferred over feeling items, because alexithymia affects feeling items.

**Verdict: REDESIGN.** Never the sole input to `self_confidence`.

### oops_try_again: the most behavioural confidence input

This is a **persistence-after-setback paradigm**, from the Dweck tradition. In Mueller & Dweck's canonical study, **128 children aged 10–12** did **3 sets of 10 problems, 4 minutes each**, with a much harder second set. Post-setback persistence was a **self-rated intention** (1–6): **3.25 after intelligence praise vs 4.53 after effort praise** (control 4.30). No differences appeared after success alone [LIT] ([Mueller & Dweck 1998](https://www.columbia.edu/cu/psychology/courses/3615/Readings/Mueller_Dweck.pdf)). The effect is contested: Li & Bates (2019) tested 624 children and found no harm from intelligence praise, and Dweck & Yeager disputed the replication protocol ([Li & Bates preprint](https://Www.Gwern.net/doc/psychology/2020-li.pdf)). The app's behavioural measure is therefore an extension of this work, not a replication. The original used Raven matrices, which the app must not use.

Quitting is confounded. Youth in the ADHD research population quit a frustration-tolerance task more often, independent of ODD ([Seymour et al.](https://pubmed.ncbi.nlm.nih.gov/27282378/)), and gave up on more puzzles after an insolvable set, an effect stimulants prevented ([Milich et al.](https://uknowledge.uky.edu/psychology_facpub/25)). In the autism research population, repeated retries may be perseveration.

**Redesign [DP].**
- A 2-minute mini-game (a tower builder) in which one round is quietly made harder.
- A playful neutral outcome ("the tower wobbled!"), with "try again" and "do something else" equally prominent.
- An effort reward for either choice.
- **Always end on a success round**, mirroring the original study's debrief principle.
- Effort and strategy praise only, with wording held constant.
- **3 setbacks on 3 days in 2 skins.**
- Persistence index = proportion of setbacks followed by a voluntary retry (capped at 3 retries), with decision latency as a tie-breaker.
- Setbacks that coincide with low mood or calm-mode activation are down-weighted.

**Verdict: KEEP** with redesign, internally labelled "persistence after difficulty".

### level_choice: score calibration, not bravado

Atkinson's model predicts that success-motivated people prefer intermediate difficulty, while avoidance-motivated people choose very easy *or* very hard tasks ([Slade & Rush 1991](https://www.interruptions.net/literature/Slade-JP&SP91.pdf)). Preschoolers' choices track goals (pleasing adults, interest, the value of success), not only confidence ([Acta Psychologica Sinica 2004](https://journal.psych.ac.cn/acps/EN/Y2004/V36/I06/744)). Choices drift harder with repetition.

**Redesign [DP].**
- **4–6 three-door choice points** ("practice / fun / big challenge"), embedded in the same tower mini-game so that each choice can be compared with the child's demonstrated success rate.
- Equal effort rewards for every door, and no visual privileging of the challenge option. This follows Mueller & Dweck's device for offsetting social desirability.
- Door positions counterbalanced, because 5–7-year-olds pick by position.
- Calibration index = chosen level minus the level the child's success supports. Choosing at or slightly above that level scores highest; extreme under- or over-choice scores lower.

**Verdict: KEEP** with redesigned scoring.

**The composite is defensible as a provisional, baseline-relative score.** `about_me`, `oops_try_again` and `level_choice` capture three facets (self-perception, response to difficulty, challenge-seeking) with different method biases. Proposed weights [DP]: **20/40/40 for 5–7**, interpolated for 8–10, and **33/33/33 for 11–12**. Each facet is stored and shown separately, so that a low composite driven entirely by quits can be recognised as a likely frustration-tolerance or attention pattern. It should be validated against teacher and parent ratings before it drives plan weighting strongly.

### mood_check_in: context, not a skill

No source reports the test-retest reliability of a single-item face mood rating at ages 5–12. A talking-character EMA app for 4–10-year-olds achieved **~89% valid responses**, but its parent–child agreement (**r = .89–.97**) concerned behavioural questions, not mood, and 8–10-year-olds found the narration too slow [LIT] ([PMC10468030](https://pmc.ncbi.nlm.nih.gov/articles/PMC10468030/)). Alexithymia is elevated in the autism research population ([PMC9839896](https://pmc.ncbi.nlm.nih.gov/articles/PMC9839896)), so a face choice may reflect a guess. Urdu emotion constructs can be validated, as the Urdu Children's Emotion Management Scales show (internal consistency **.808–.904**, n = 683) ([Baig et al.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11008575/)). The Urdu evidence found covers ages 8+ only.

**Design [DP].**
- A band-independent valence from −2 to +2.
- **5–7:** 2 faces (happy / not happy), plus an optional "tired or worried" tap.
- **8–10:** 5 faces.
- **11–12:** 5 faces plus an optional calm/excited arousal choice.
- Faces differ only in mouth and eyes, with neutral colouring.
- Right-to-left direction checked for the Urdu UI.
- Run at every session start and end, using the existing `sessions.mood_before` and `mood_after` fields.

Mood is used three ways: as a covariate on that session's scores, as a delivery trigger (calm mode, shorter session), and as a pattern a human can review. Persistently low mood is a candidate for the safety-review queue after Phase 0 clinical input.

**Verdict: KEEP as context; do not score.** Remove it from the `sensory_regulation` evidence mapping.

### sensory_setup: a comfort preference, not a measurement

Sensory differences are real and common in the autism research population (**~60% auditory over-responsivity** in a survey of 4,000+ autistic youth) [LIT] ([brief report](https://antoniusacademie.mijn.bsl.nl/brief-report-prevalence-and-severity-of-auditory-sensory-over-re/19078432)). Over-responsivity also occurs in **8–15% of typically developing children** [LIT] ([sensoryhealth.org](https://sensoryhealth.org/sites/default/files/publications/DiagnosticvalidityofSOR.pdf)). The largest autism-vs-typical difference is in **under-responsivity**, and the difference peaks at **ages 6–9** [LIT] ([Ben-Sasson et al. 2009](https://pubmed.ncbi.nlm.nih.gov/18512135/)). A calm-mode or volume-down rate cannot capture under-responsivity at all.

Device-behaviour studies are group-discrimination experiments, not individual measures ([Feel and Touch](https://www.citedrive.com/en/discovery/smartphone-haptics-can-uncover-differences-in-touch-interactions-between-asd-and-neurotypicals)). Repurposing them would conflict with rule #1. Settings are also confounded by home noise, harsh speakers, siblings, adult choices and week-1 novelty. Scoring "low" for choosing a quieter setting would penalise adaptive self-management, which conflicts with rule #5.

**Design [DP].**
- Day-1 picture choices for sound and animation, with a live preview.
- An always-visible calm button.
- A one-tap re-offer at each session start.
- Every change logged with its context.
- Settings drive delivery immediately.
- Patterns are surfaced to adults descriptively ("often turns sounds down during X").

**Verdict: REFRAME and PARK the score.**

## A twelve-key skill model with nine dimensions scored in week 1

The research argues for renaming two dimensions, adding one, moving two out of the scored set into evidence or context, and stating openly which dimensions week 1 cannot score yet. The proposal below keeps 12 keys.

| # | Key | Status | Week-1 sources | Change from current draft |
|---|---|---|---|---|
| 1 | `sustained_attention` | Scored | watch_the_pond ×2 (clean trials); RT variability from stars_not_clouds | Absorbs `distractibility` as an evidence sub-score ("distractor cost") |
| 2 | `impulse_control` | Scored | stars_not_clouds ×2 | wait_for_the_bell removed from week 1 |
| 3 | `working_memory` | Scored | copy_the_pattern ×2, follow_instructions | Sub-scores `wm_verbal` / `wm_visuospatial` in evidence |
| 4 | `auditory_comprehension` | Scored | story_and_questions (4 stories); follow_instructions only if the vocabulary check passes | Literal/inferential and social/non-social sub-scores |
| 5 | `reading_comprehension` | Scored for readers only | read_and_answer (gated) | Below sentence level = "insufficient evidence", confidence 0; per language |
| 6 | `speech_perception` | **New**, scored | which_word | Replaces which_word → `articulation` |
| 7 | `emotion_recognition` | Scored | how_does_she_feel ×2 | Illustrated South Asian faces; aggregate score |
| 8 | `social_problem_solving` | **New/renamed**, scored | what_would_you_do | Takes over the vignette evidence from `social_communication` |
| 9 | `self_confidence` | Scored (provisional composite) | about_me, oops_try_again ×3, level_choice ×4–6 | Labelled "confidence & persistence"; facets shown separately |
| 10 | `articulation` | Captured, scored later | name_the_picture audio | No week-1 score until Phase B/C |
| 11 | `expressive_language` | Captured, scored later | speak_this_line, name_the_picture latency, retell audio | No week-1 score; latency evidence capped at ≤0.3 |
| 12 | `social_communication` | Reserved | none in week 1 | Enacted conversation only, after the Phase 3 speech pipeline |
| — | `distractibility` | Parked → evidence sub-score | distractor trials in watch_the_pond | Restore only if pilot reliability is acceptable |
| — | `sensory_regulation` | Parked → comfort-preferences profile | sensory_setup, calm-mode log, mood | Not scored; informs delivery and human review |

Two candidate dimensions logged in an earlier research pass, rigidity and cognitive flexibility, stay out of scope for week 1.

**Plan-engine consequences.** These are inferences, and the owner should decide them.
- **`low_attention`** is unchanged.
- **`confidence_need`** reads the composite.
- **`social_need`** should read `social_problem_solving` or `emotion_recognition` instead of `social_communication`.
- **`sensory_need`** can no longer read a computed `p.sensory_sensitive()`. It needs a guardian or therapist input, or a pattern flag a human confirms.
- **`speech_need`**: `articulation` and `expressive_language` will not reach confidence 0.5 in week 1, so the `speech_language` module **cannot fire from week-1 data alone**. The options are (a) accept this and assign speech support after human-rated audio in Phase B; (b) allow a guardian or teacher concern to trigger it under human review; or (c) let low `speech_perception` trigger it provisionally. Option (c) is weakest, because the perception–production link is unresolved.

Once confidence comes from the reliability function above, the existing "fallback when nothing fires" path (confidence_builder 0.5 + focus_attention 0.5) will be used more often than the current design assumes. That should be expected.

## A revised seven-day schedule with five spread repeats

The proposed schedule [DP] follows these principles:
- the same fixed order and within-day position for every child and every re-evaluation
- attention-heavy tasks first in the session on the days they appear
- an unscored tutorial before each task's first scored block
- 10–15 minutes a day
- `mood_check_in` (one tap) at the start and end of every session, and a one-tap comfort re-offer after day 1
- skipped tasks re-offered once later in the week
- completion-based day progression, as already built

Five tasks repeat across days 4–7: `stars_not_clouds`, `watch_the_pond`, `how_does_she_feel`, `copy_the_pattern`, and the tower mini-game (`oops_try_again` + `level_choice`, 3 runs). That gives every scored, rule-driving dimension at least two observations.

| Day | Activities, in fixed order | Approx. minutes [DP] | Purpose |
|---|---|---|---|
| 1 | sensory_setup → stars_not_clouds (run 1) → which_word | ~11 | Comfort first; impulse anchor; no-speech speech data |
| 2 | watch_the_pond (run 1, with fixed distractor set A) → how_does_she_feel (set A) → story_and_questions (stories 1–2) | ~13 | Sustained-attention anchor; emotion; listening |
| 3 | copy_the_pattern (run 1) → follow_instructions → tower mini-game (setback 1, choice points 1–2) | ~12 | Working memory, both modalities; first confidence facets |
| 4 | stars_not_clouds (run 2) → speak_this_line (capture) → name_the_picture (capture) | ~12 | **Repeat 1**; speech audio (consent-gated; neutral skip without audio consent) |
| 5 | what_would_you_do (6–8 vignettes) → about_me → tower mini-game (setback 2, choice points 3–4) | ~11 | Social reasoning; self-perception; **repeat 2** |
| 6 | watch_the_pond (run 2, distractor set B) → how_does_she_feel (set B) → story_and_questions (stories 3–4) | ~13 | **Repeats 3–4**; listening items reach ~16–20 |
| 7 | copy_the_pattern (run 2) → read_and_answer (decoding probe; passages only at sentence level+) → retell_the_story (capture) → tower mini-game (setback 3, choice points 5–6) | ~14 | **Repeat 5** plus the final confidence run; reading for readers only |

For the 5–7 band, keep the same activities and order but trim items within each task so the day stays near 10–12 minutes [DP]. For most 5–7-year-olds in Pakistan, the day-7 reading task will end after the ~1-minute probe.

Compared with `backend/app/week1/schedule.py`:
- Removed: `wait_for_the_bell`, `chat_with_a_character` and the stand-alone `distraction_garden`.
- `mood_check_in` moves to session level.
- The `speak_this_line` repeat is reassigned to scorable dimensions.
- Day 6 drops from four activities to three.

## Summary table: twenty activities, one verdict each

| Activity | Paradigm | Revised dimension | Week-1 status | Key parameters | Verdict |
|---|---|---|---|---|---|
| stars_not_clouds | Go/no-go, frequent go | impulse_control | Scored, ×2 | 80–100 trials; 25% no-go; 750 ms (5–7) / 500 ms (8+) [LIT Clark] | **KEEP** |
| watch_the_pond | Rare-target CPT | sustained_attention | Scored, ×2 | 25% targets [LIT Clark]; no decrement score; hosts distractors | **KEEP** (shared engine) |
| wait_for_the_bell | Delay aversion (DeFT-like) | (impulse_control, provisional) | Not in week 1 | No child reliability data | **DROP from week 1 / DEFER** |
| distraction_garden | Irrelevant-distractor interference | sustained_attention (cost sub-score) | Condition inside pond | ~10% distractor trials [LIT Forster]; new set per run [DP] | **MERGE** |
| follow_instructions | Following-instructions (Gathercole) | working_memory (verbal) | Scored, ×1 | Lengths 1–5 / to 7; partial credit [LIT Wells/Conway] | **KEEP** |
| copy_the_pattern | Corsi block-tapping | working_memory (visuospatial) | Scored, ×2 | Start 2, 2 trials/length, +1 past stop [LIT eCorsi/Wells] | **KEEP** |
| story_and_questions | Narrative listening comprehension | auditory_comprehension | Scored, 4 stories | 20–30 items for α > .70 [LIT Santos]; 40/60 literal/inferential [DP] | **KEEP** |
| read_and_answer | Passage reading comprehension | reading_comprehension | Readers only | Decoding gate; 3–5 passages × 4–6 Qs [DP] | **REDESIGN** |
| speak_this_line | Sentence repetition | expressive_language (+ verbal WM) | Capture only | 10–14 graded sentences [DP]; 2.08 SD group gap [LIT Ward] | **KEEP** (score later) |
| name_the_picture | Confrontation naming | expressive_language + articulation | Capture only (latency on device) | 15–20 items with target phonemes [DP] | **KEEP** (narrowed; absorbs articulation probe) |
| which_word | Minimal-pair discrimination | **speech_perception** (new) | Scored, ×1 | 16–24 trials, 3–4 contrasts; chance-corrected [DP] | **KEEP + REMAP** |
| retell_the_story | Narrative retell (macrostructure) | expressive_language | Capture only, 1 story | MAIN-style 6-picture structure, own content | **KEEP capture / DEFER scoring** |
| chat_with_a_character | Conversational turn-taking | social_communication | Not in week 1 | Latency retest .36–.66 [LIT Cox] | **DEFER** |
| how_does_she_feel | Forced-choice emotion labelling | emotion_recognition | Scored, ×2 | 12–18 trials/session [DP]; 4 → 6 emotions → morphs by band | **KEEP** (new stimuli) |
| what_would_you_do | SIP vignettes (evaluation/selection) | **social_problem_solving** (renamed) | Scored, ×1 | 6–8 vignettes [DP; 8 in LIT]; local-panel appropriateness | **KEEP + RENAME** |
| about_me | Pictorial self-perception | self_confidence (facet) | Scored, capped | 6–8 two-picture items; caps .3/.5/.7 [DP] | **REDESIGN** |
| oops_try_again | Persistence after setback | self_confidence (facet) | Scored, ×3 | 3 setbacks, always ends on success [DP] | **KEEP** (redesign) |
| level_choice | Task choice / risk preference | self_confidence (facet) | Scored, 4–6 choices | Calibration vs demonstrated skill [DP] | **KEEP** (rescored) |
| mood_check_in | Single-item pictorial mood | — (context) | Every session, not scored | 2 / 5 / 5+arousal options by band [LIT Coombes; DP] | **KEEP as context** |
| sensory_setup | Comfort preference setting | — (comfort profile) | Not scored | Live-preview choices; logged changes | **REFRAME + PARK score** |

## Open gaps: what still needs a pilot

The biggest gap is that **no reference reliability exists for any of this app's tasks**. Every r₀, every confidence cap and every reliable-change threshold above is a placeholder. The first pilot should be a test-retest study: the same tasks at a 1–2-week interval, in a modest sample (the notes suggest **≥30 children** [DP]). It should run in Urdu and English, and in Pakistani homes, because none of the reliability figures cited come from South Asian children aged 5–12. The pilot should produce:
- ICCs per task and per age band
- the expected practice gain from day 1 to day 7 and from week 1 to week 7, which feeds the practice-adjusted reliable-change thresholds
- the SD of each 0–100 score, replacing the arbitrary SD of 15
- trials-to-reliability curves; the [Kadlec et al. reliability web tool](https://jankawis.github.io/reliability-web-app/) can estimate these from pilot data

Several design changes depart from validated designs and need their own checks:
- Neutral feedback in place of the error feedback Clark et al. used. No study has measured go/no-go reliability without error feedback in children.
- The two-phase shared attention engine, split across days.
- Whether a distractor-cost score is reliable enough to justify a `distractibility` dimension.
- Whether 5–7-year-olds tolerate ~4-minute attention blocks.
- Whether illustrated South Asian faces reach adequate adult and child agreement, and whether picture-choice SIP vignettes relate to observed classroom behaviour (validate against teacher ratings).
- Whether the confidence composite agrees with teacher and parent ratings.

On the speech side, the speech_language module is effectively unassignable from week-1 data until three things exist: voice-onset detection validated against hand-marked onsets, a non-proprietary human rating rubric for SR, naming and retell with inter-rater reliability, and any child Urdu ASR benchmark.

Several content and localisation inputs are also missing from the literature:
- per-year Corsi spans for ages 5–12 (Farrell Pagulayan 2006 tables)
- per-consonant Urdu acquisition ages (the HKU JSLHR 2021 full text)
- Urdu picture-naming name agreement and minimal-pair perception items
- which English contrasts Pakistani English maintains
- Urdu child mood and emotion vocabulary norms for 5–7-year-olds
- Pakistani display rules and teacher and parent views of competent social responses (the largest localisation gap, best filled by Phase 0 interviews)
- reading levels of urban private-school 5–7-year-olds, the likely early adopters
- Urdu readability levelling
- confirmation that a right-to-left UI does not distort face scales

Three licences must be checked before any use: CAFE (commercial use), MAIN (story content) and USAT (items). No source gave a minimum number of setback occasions or choice points for a reliable persistence or challenge score. Finally, nothing tells us how often typical children toggle comfort settings out of novelty, which a sensory pattern flag would need as its baseline.

## Conclusion

The research changes what week 1 is for. It cannot be a broad 12-dimension snapshot with each dimension measured once. It should be a short **measurement burst**: deep, repeated observation of the 9 dimensions the app can actually score, plus clearly labelled capture and context for the rest. The practical gain is that the existing `confidence ≥ 0.5` gate stops being an arbitrary number and becomes a statement about estimated reliability. Honest "still learning about this area" messages then become a feature rather than an embarrassment. Two consequences need decisions from the owner now rather than after the pilot. First, the speech module cannot be assigned from week-1 data without a human in the loop. Second, social and sensory needs must be re-wired to `social_problem_solving` and to human-confirmed comfort patterns.

The research also shows that much of what looked like content work is measurement work. Swapping stimuli (South Asian faces, Urdu contrasts, Nastaliq passages, culturally neutral targets) changes scores independently of skill: by about 9% for faces from another culture, and by the large Urdu-medium vs Sindhi-medium gap in listening comprehension. Language, device, art skin and age band therefore belong in the same category as theme changes, as logged comparability events that reset the baseline. They cannot be treated as cosmetic details.

## Sources

**Attention and impulse**
- Clark et al. 2023, combined go/no-go + CPT in ages 3–12 — https://pmc.ncbi.nlm.nih.gov/articles/PMC10041761
- Huang-Pollock et al. 2012, CPT meta-analysis — https://pmc.ncbi.nlm.nih.gov/articles/PMC3664643
- CPT test-retest, raw vs T-scores — https://pmc.ncbi.nlm.nih.gov/articles/PMC2899676
- Dunning et al. 2021, SART — https://www.mrc-cbu.cam.ac.uk/wp-content/uploads/www/sites/3/2021/06/Dunning-et-al.-2021.-SART.pdf
- Sustained-attention development 2020 — https://www.doi.org/10.1007/s10802-020-00698-5
- Kofler et al. 2013, RT variability meta-analysis — https://sciences.ucf.edu/psychology/childrenslearningclinic/wp-content/uploads/sites/24/2013/05/Kofler-et-al.-2013-RT-Variability-Meta-analysis.pdf
- IMFAR 2010, go/no-go in autism — https://imfar.confex.com/imfar/2010/webprogram/Paper6503.html
- Forster et al., irrelevant distractors — https://pmc.ncbi.nlm.nih.gov/articles/PMC3906797
- Frontiers for Young Minds 2017, perceptual load in children — https://kids.frontiersin.org/articles/10.3389/frym.2017.00008
- Novel-sound distraction 7–10 y — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7935912/
- Dual-pathway / delay aversion — https://pmc.ncbi.nlm.nih.gov/articles/PMC2565443
- Chan et al. 2024, Delay Frustration Task — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12062859/
- Toor & Hanif 2022, EF Touch in Pakistan — https://pmc.ncbi.nlm.nih.gov/articles/PMC9477268/

**Memory and comprehension**
- Gathercole et al., following instructions — https://pmc.ncbi.nlm.nih.gov/articles/PMC3901937
- Jaroslawska et al., following instructions on screen — https://ueaeprints.uea.ac.uk/id/eprint/81797
- Alloway, Gathercole & Pickering — https://durham-repository.worktribe.com/output/1555279/verbal-and-visuospatial-short-term-and-working-memory-in-children-are-they-separable
- Gathercole et al. 2004 — https://eprints.whiterose.ac.uk/5942/
- Wells, Kofler et al. 2018, span scoring — https://psy.fsu.edu/clc/Publications/Wells2018.pdf
- Conway et al. 2005 — https://link.springer.com/article/10.3758%2FBF03196772
- eCorsi, Brunetti et al. 2014 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4151195/
- Corsi norms summary — https://en.wikipedia.org/wiki/Corsi_block-tapping_test
- Martinussen et al. 2005 — https://pubmed.ncbi.nlm.nih.gov/15782085/
- Santos et al. 2015, listening comprehension tests — https://www.cambridge.org/core/journals/spanish-journal-of-psychology/article/development-of-listening-comprehension-tests-with-narrative-and-expository-texts-for-portuguese-students/1CB8A3441312304564AA82C2771AE127
- ICNA manual — https://lel.crires.ulaval.ca/cms/1691721704987-techical-manuel_icna_jan-2023.pdf
- EGRA Sindh 2024 — https://rsusindh.gov.pk/rsusindh.gov.pk/contents/SELECT/EGRA_Baseline_Assessment_Report_Sindh.pdf
- Autism inferential comprehension — https://research-repository.griffith.edu.au/items/9be2d792-2ac7-4900-a514-01d5715d9bf4
- Brown, Oram-Cardy & Johnson 2013 — https://imfar.confex.com/imfar/2012/webprogram/Paper9964.html
- Keenan, Betjemann & Olson 2008 — https://experts.colorado.edu/display/pubid_53767
- Ostrolenk et al., hyperlexia — https://insar.confex.com/insar/2018/webprogram/Paper28551.html
- ASER 2023 via Business Recorder — https://www.brecorder.com/news/amp/40232775
- Rao et al. 2011, Urdu vs Hindi — https://oaktrust.library.tamu.edu/bitstream/1969.1/158732/1/Rao%2C%20Vaid%2C%20Srinivasan%20and%20Chen%202011.pdf
- StoryWeaver levelling — https://storyweaver.org.in/v0/blog_posts/19-re-levelling-stories-on-storyweaver

**Speech and language**
- Ward, Polišenská & Bannard 2024 — https://openaccess.city.ac.uk/32966/1/WARD%20et%20al%20-%20meta%20analysis.pdf
- ASHA Evidence Map — https://apps.asha.org/EvidenceMaps/Articles/ArticleSummary/f849b558-e711-44c1-84fa-37353619497f
- LITMUS study — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11202042/
- Naming latency — https://oro.open.ac.uk/16570
- Naming errors — https://research.polyu.edu.hk/en/publications/picture-naming-in-children-with-and-without-specific-language-imp/
- Perception–production — https://pmc.ncbi.nlm.nih.gov/articles/PMC7201332
- Retell reliability — https://link.springer.com/article/10.1007/s10936-023-10007-y
- MAIN / Urdu MAIN, Chan et al. 2020 — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7714944/fullTextXML
- Narratives in ADHD, meta-analysis summary — https://adhdevidence.org/blog/meta-analysis-finds-narrative-language-impairment-in-youths-with-adhd
- CoDAS — https://scielo.br/j/codas/a/PK9GvdMh8gBLRHks9rcDP5M/?lang=en
- Methylphenidate and retell — https://cris.biu.ac.il/en/publications/methylphenidate-selectively-improves-story-retelling-in-children-/
- Narratives in autism — https://imfar.confex.com/imfar/2016/webprogram/Paper21377.html
- Urdu stops — https://www.redalyc.org/journal/6638/663872611009/663872611009.pdf
- MIT fieldwork notes on Urdu — https://people.csail.mit.edu/namin/oldschool/linguistics/fieldwork1.pdf
- Urdu acquisition — https://pubs.asha.org/doi/10.1044/2021_JSLHR-21-00148
- Urdu development (secondary) — https://bilinguistics.com/languages/urdu-speech-and-language-development/
- USAT — https://jrcrs.riphah.edu.pk/wp-content/uploads/2024/03/2024120104.pdf
- McLeod & Crowe 2018 — https://pubs.asha.org/doi/10.1044/2018_AJSLP-17-0100
- Child Whisper — https://arxiv.org/pdf/2309.07927
- Native and non-native child ASR — https://research.universityofgalway.ie/en/publications/exploring-native-and-non-native-english-child-speech-recognition-/
- Disordered speech ASR — https://mlanthology.org/iclrw/2025/adeyeyekayode2025iclrw-evaluating
- Urdu ASR benchmark — https://arxiv.org/pdf/2409.11252

**Social-emotional**
- CAFE — https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.01532/pdf
- CAFE-Ss — https://repository.nie.edu.sg/bitstreams/17f63782-2651-4137-8404-240c7f24bf12/download
- Princeton face database guide — https://libguides.princeton.edu/facedatabases
- Qingdao set — https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.554821/full
- Elfenbein & Ambady 2002 — https://swov.nl/en/publicatie/universality-and-cultural-specificity-emotion-recognition-meta-analysis
- Tunisian FER test — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8645551/
- FELT — https://pmc.ncbi.nlm.nih.gov/articles/PMC5568997
- Faces/voices battery psychometrics — https://researchconnect.buffalo.edu/en/publications/psychometric-properties-of-the-cambridge-mindreading-face-voice-b/
- Maassarani et al. 2014 — https://pmc.ncbi.nlm.nih.gov/articles/PMC4044975
- Uljarevic & Hamilton 2013 — https://mijn.bsl.nl/recognition-of-emotions-in-autism-a-formal-meta-analysis/555206
- Harms, Martin & Wallace 2010 — https://www.researchgate.net/profile/Gregory_Wallace/publication/46108941_Facial_emotion_recognition_in_autism_spectrum_disorders_a_review_of_behavioral_and_neuroimaging_studies/links/0fcfd513e40bc00914000000.pdf
- Cook et al. 2013 — https://openaccess.city.ac.uk/id/eprint/4539/
- Rosset et al. — https://mijn.bsl.nl/typical-emotion-processing-for-cartoon-but-not-for-real-faces-in/547186
- ADHD FER meta-analysis — https://pubmed.ncbi.nlm.nih.gov/38860431/
- ADHD per-emotion effects — https://link.springer.com/article/10.1007/s00787-020-01709-y
- SIP steps — https://pmc.ncbi.nlm.nih.gov/articles/PMC8361679
- SIP vignettes — https://pmc.ncbi.nlm.nih.gov/articles/PMC2791956
- Cox, Fusaroli et al. 2025 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12517399/
- Lunsford et al. 2012 — https://www.isca-archive.org/interspeech_2012/lunsford12_interspeech.html

**Confidence and comfort**
- Coombes et al. 2021 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8233251/
- Belsky — https://digfir-published.macmillanusa.com/belsky4e/belsky4e_ch6_3.html
- Harter–Pike factor structure — https://pmc.ncbi.nlm.nih.gov/articles/PMC5969031
- Yeager & Krosnick — https://web.stanford.edu/dept/communication/faculty/krosnick/docs/2011/Some%20other%20adolescents%20-%20Developmental%20Psych%20PUBLISHED.pdf
- Reynolds-Keefer & Johnson — https://www.semanticscholar.org/paper/Validity-Issues-in-the-Use-of-Pictorial-Likert-Reynolds-Keefer/f9f1c6f3e6b12f23041709bf4b251fad5be77e6f
- Positive illusory bias — https://link.springer.com/doi/10.1007/s12402-010-0043-x
- Mueller & Dweck 1998 — https://www.columbia.edu/cu/psychology/courses/3615/Readings/Mueller_Dweck.pdf
- Li & Bates — https://Www.Gwern.net/doc/psychology/2020-li.pdf
- Seymour et al., frustration tolerance — https://pubmed.ncbi.nlm.nih.gov/27282378/
- Milich et al. — https://uknowledge.uky.edu/psychology_facpub/25
- Slade & Rush 1991 — https://www.interruptions.net/literature/Slade-JP&SP91.pdf
- Acta Psychologica Sinica 2004 — https://journal.psych.ac.cn/acps/EN/Y2004/V36/I06/744
- EMA app for 4–10-year-olds — https://pmc.ncbi.nlm.nih.gov/articles/PMC10468030/
- Alexithymia in autism — https://pmc.ncbi.nlm.nih.gov/articles/PMC9839896
- Urdu CEMS — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11008575/
- Auditory over-responsivity prevalence — https://antoniusacademie.mijn.bsl.nl/brief-report-prevalence-and-severity-of-auditory-sensory-over-re/19078432
- Sensory over-responsivity review — https://sensoryhealth.org/sites/default/files/publications/DiagnosticvalidityofSOR.pdf
- Ben-Sasson et al. 2009 — https://pubmed.ncbi.nlm.nih.gov/18512135/
- Feel and Touch — https://www.citedrive.com/en/discovery/smartphone-haptics-can-uncover-differences-in-touch-interactions-between-asd-and-neurotypicals

**Week-1 design**
- Hedge, Powell & Sumner 2018 — https://pmc.ncbi.nlm.nih.gov/articles/PMC5990556
- EF Touch retest — https://fpg.unc.edu/publications/test-retest-reliability-new-executive-function-battery-use-early-childhood
- NIH Toolbox, Anokhin et al. 2022 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8589010/
- Burst designs — https://pmc.ncbi.nlm.nih.gov/articles/PMC3633558
- Kadlec et al. 2024 — https://communities.springernature.com/posts/behind-the-paper-a-measure-of-reliability-convergence-to-select-and-optimize-cognitive-tasks-for-individual-differences-research
- Repeated-testing practice effects — https://escholarship.org/content/qt5032v9rb/qt5032v9rb.pdf
- Counterbalancing notes — https://web.mnstate.edu/malonech/Psy633/Notes/633%20Experimental%20designs%20-%20Within%20groups.doc
- ADHD time-on-task — https://www.bordeaux-neurocampus.fr/?p=90347
- Lumsden et al. 2016 — https://pmc.ncbi.nlm.nih.gov/articles/PMC4967181
- Jacobson–Truax reliable change — https://www.psyctc.org/stats/rcsc.htm
- PBS HIES 2024–25 — https://www.pbs.gov.pk/wp-content/uploads/2020/07/Final-Results-Presentation-HIES-2024-25-website-1.pdf
- FAFEN on PSLM — https://fafen.org/pslm-mobile-internet-access-rises-computer-ownership-stays-flat/
