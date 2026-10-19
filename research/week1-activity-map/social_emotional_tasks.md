# Social-emotional tasks: how_does_she_feel, what_would_you_do, chat_with_a_character (ages 5–12, Android tablet, Urdu/English, Pakistan)

Scope note: these notes cover research only. Every numeric parameter is a **literature estimate** with its source, or is marked **[design proposal, unvalidated]**. No item wording, ordering or scoring is taken from proprietary instruments (SRS-2, SCQ, NEPSY Affect Recognition, Reading the Mind in the Eyes child version, CAM-C items, etc.). Where a published study used a proprietary test, only its *aggregate finding* is cited, not its items.

Research budget: about 20 search/fetch calls. Several points below are flagged as Gaps where no primary source was reached in this pass.

---

## Q1. Which open-licensed child face stimulus sets exist (and include South Asian faces)?

### Takeaway
No child face set confirmed in this pass is both **open-licensed for commercial/app use** and **South Asian-rich**. CAFE (LoBue & Thrasher 2015) is the only well-validated child set found with South Asian (Indian/Bangladeshi/Pakistani) models, but only 11 of 154 models, and it is distributed for research use. The other common child sets (Dartmouth, Radboud child models, NIMH-ChEFS) are research-use and predominantly or entirely white. For a shipped app, plan to **commission original illustrated (or consented photographic) South Asian child faces**, validated in-house, rather than rely on a research set.

### Cited Findings
- CAFE: photographs of 2–8-year-old children posing angry, fearful, sad, happy, surprised, disgusted and neutral; nearly 1,200 photographs of 100+ children — [LoBue & Thrasher 2015, Frontiers in Psychology](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.01532/pdf)
- CAFE ethnic composition: 90 female and 64 male models (27 African American, 16 Asian, 77 Caucasian/European American, 23 Latino, **11 South Asian** — Indian/Bangladeshi/Pakistani) — [CAFE-Ss paper, NIE repository](https://repository.nie.edu.sg/bitstreams/17f63782-2651-4137-8404-240c7f24bf12/download); [CAFE validation, ResearchGate](https://www.researchgate.net/publication/271331770_The_Child_Affective_Facial_Expression_CAFE_set_validity_and_reliability_from_untrained_adults)
- CAFE-Ss: two subsets of 140 photographs each, diverse in race/ethnicity and designed to produce variability in naïve observers — [PubMed 33343471](https://pubmed.ncbi.nlm.nih.gov/33343471/)
- Adult-rater agreement (literature estimate): 66% for CAFE full set, 81% for "Subset A" — cited in [Qingdao Preschooler Facial Expression set paper, Frontiers 2020](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.554821/full)
- CAFE access: listed as research use with citation required; Dartmouth Database of Children's Faces (ages 6–16, 80 models, 8 expressions) research use by contact with the curator; LIRIS-CSE (12 "ethnically diverse" children, spontaneous video, six basic emotions) research use via request form; Radboud includes Caucasian children only; the guide lists **no South Asian representation** in the child databases it covers — [Princeton Library face database guide](https://libguides.princeton.edu/facedatabases)
- Qingdao Preschooler Facial Expression set: 712 images, 54 children aged 5–7, 11 emotions (6 basic + 5 positive), Chinese children only, 78.4% agreement on the acceptable subset — [Frontiers 2020](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.554821/full)
- A commercial "South Asian children facial image dataset" exists from a data vendor, built for face recognition (not validated emotion stimuli) — [FutureBeeAI](https://www.futurebeeai.com/dataset/image-dataset/facial-images-minor-south-asian)
- Aggregator of face stimulus sets for further searching — [FSTC face stimulus and tool collection](https://rystoli.github.io/FSTC.html)
- Why own-group faces matter: across 97 studies, emotion recognition was **9.3% more accurate** when judging expressions from one's own cultural group (literature estimate), and the in-group advantage shrinks with exposure between groups — [Elfenbein & Ambady 2002 meta-analysis, summarised by SWOV](https://swov.nl/en/publicatie/universality-and-cultural-specificity-emotion-recognition-meta-analysis); [in-mind.org summary](https://in-mind.org/node/306)

### Inferences
- Using mostly white or East Asian child faces would introduce a known accuracy penalty for Pakistani children that has nothing to do with skill. That breaks score comparability with any later change of stimulus set.
- The 11 South Asian CAFE models are too few to build a varied, repeated-measures item bank (each model would recur across sessions). Research-only terms probably also rule out shipping them in a product. Treat CAFE as a possible **validation reference** (for example, checking that in-house illustrations are recognised at similar rates by adult raters), not as shipped content, and only if its licence permits that.
- Recommended path **[design proposal]**: commission an original illustrated South Asian child-face set (several characters × 6 basic emotions + neutral + 2–3 intensity levels). Validate it with Pakistani adult raters and a pilot child sample before use. Cartoon/illustrated faces also fit the app's existing art direction and the autism evidence in Q5.

### Gaps
- **Exact CAFE licence text** (it is hosted on Databrary, which normally requires an institutional authorisation agreement) was not fetched. Whether commercial app use is allowed is **unverified**. Assume not until checked.
- NIMH-ChEFS licence and composition were not verified in this pass. From memory it is research-use and predominantly white, but that is unconfirmed here.
- No open, Pakistani-specific validated child emotion face set was found. Another search (e.g. Indian child face sets, IFEED, or Pakistani university-hosted sets) might turn one up.

---

## Q2. How many items give a reliable emotion-recognition score in children? (structure + reliability)

### Takeaway
Published child FER tasks that reach good reliability (α ≈ .80–.88, test-retest ≈ .75–.85) use **large item counts (≈36–360 trials)**. Reliability rises markedly when accuracy is **aggregated across emotions and intensities** rather than reported per emotion or per intensity. A tablet game with a 3–5-minute slot cannot get there in one session. Plan for a composite score accumulated over sessions, with confidence growing as items accumulate.

### Cited Findings
- Tunisian facial emotion recognition test (ages 7–12): static subtest of **114 photographs** and dynamic subtest of **36 videos**; Cronbach's α **0.88** (static) and **0.85** (dynamic) — literature estimates — [Validation of the Tunisian Test for Facial Emotions Recognition, PMC8645551](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8645551/)
- Facial Expression Labeling Task (FELT), ages 9–14 (mean 10.78): **360 trials** = 6 trials × 6 basic emotions × 10 morph-intensity levels (10–100%); test-retest of the intercept (overall ability) **0.76–0.85** and of the intensity slope **0.69–0.83** across emotions; aggregating across intensity levels gave substantially higher reliability than per-level scores — literature estimates — [PMC5568997](https://pmc.ncbi.nlm.nih.gov/articles/PMC5568997)
- A faces/voices battery in children (a proprietary battery; only aggregate psychometrics cited here): internal consistency 0.81 for total faces score, 0.72 for complex-emotion faces; test-retest 0.76–0.81 for totals versus **0.53–0.75 for subscales** — literature estimates showing subscale/per-category scores are less reliable — [Psychometric properties, University at Buffalo record](https://researchconnect.buffalo.edu/en/publications/psychometric-properties-of-the-cambridge-mindreading-face-voice-b/) (search-snippet level; full paper not fetched)
- Emotion categories by age: children's labelling lexicon develops roughly happy → sad/angry (~40 months) → fear or surprise (~56 months) → five labels (~62 months) → disgust (~66 months); 5–6-year-olds are accurate for happy/angry/sad but much less for fear/surprise/disgust, and disgust stays difficult even at 11 — literature estimates — [Widen & Russell model, summarised in Maassarani et al. 2014, Frontiers / PMC4044975](https://pmc.ncbi.nlm.nih.gov/articles/PMC4044975)
- Dynamic vs static: the Tunisian test used both static and dynamic subtests, with comparable reliability (0.88 vs 0.85) — [PMC8645551](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8645551/)

### Inferences — recommended structure **[design proposals, unvalidated unless a source is cited]**
- **Categories by band.** 5–7: happy, sad, angry, scared (4 options), plus surprise from ~6. 8–10: add surprise and disgust (6 basic). 11–12: 6 basic + intensity variation (morphs at e.g. 40/70/100%). Complex/self-conscious emotions (embarrassed, proud, jealous) should go only in a separate, clearly labelled later stage, if at all. Grounding: the Widen & Russell sequence above.
- **Response format for non-readers.** Spoken audio label (Urdu/English per locale) plus an icon/emoji-style button. The child taps a choice; no reading needed. Free labelling (speaking the word) gives lower accuracy than forced choice ([PMC4044975](https://pmc.ncbi.nlm.nih.gov/articles/PMC4044975)) and would need ASR, so forced choice fits week 1.
- **Items per session.** About 12–18 trials (2–3 per emotion) in week 1. The literature reliability above needed 36+ trials (one subtest) to 114–360 trials. So the week-1 score should carry **low-to-moderate confidence**, rising as later sessions add items. This matches how `scoring/common.py` already scales confidence with trial count for `stars_not_clouds`.
- **Scoring unit.** One aggregate accuracy across emotions and intensities (more reliable per FELT). Per-emotion breakdowns are for explanation/evidence only and should not drive the plan engine.
- **Stimulus type.** Illustrated/cartoon South Asian faces (see Q1 and Q5), static first. Dynamic (short animated onset) is optional in later stages, since reliability is similar.

### Gaps
- No study found that directly estimates the **minimum** trial count for an acceptable child FER score (e.g. a Spearman-Brown curve). Number of trials versus reliability for ~12–24-item tablet tasks is not established.
- No RT reliability data for child FER was found in this pass. FELT did not report RT.

---

## Q3. How do published SIP-based vignette studies code children's responses? (and an original rubric)

### Takeaway
SIP vignette research (Crick & Dodge's six steps: encode cues → interpret/attribute intent → clarify goals → generate responses → evaluate responses → enact) codes **open-ended** generated responses into categories such as *aggressive, competent, authority/adult-seeking (punish vs intervene), passive/inept, irrelevant*. Trained coders reach very high agreement (κ ≈ .91). In multiple-choice designs the child instead **evaluates** presented competent/hostile/inept responses. That is a response-evaluation step (social knowledge and preference), not enactment.

### Cited Findings
- SIP steps: (1) encoding of cues, (2) interpretation and mental representation, (3) interactional goals, (4) response generation, (5) response evaluation, (6) enactment — [Fontaine/Dodge-style SIP study, PMC8361679](https://pmc.ncbi.nlm.nih.gov/articles/PMC8361679)
- A longitudinal SIP study (387 children, kindergarten to grade 3, 4 sites, 49% minority) measured SIP via hypothetical vignettes; SIP constructs predicted later teacher-reported aggression — [PMC2791956](https://pmc.ncbi.nlm.nih.gov/articles/PMC2791956)
- That study used **8 vignettes** (4 peer provocation, 4 peer group entry) at about age 8. It coded generated responses into 7 categories: **aggressive; competent; authority–punish; authority–intervene; passive-inept; irrelevant/other; unable to give further responses**. Intercoder agreement κ = **.91**. It measured four steps: intent attribution, response generation, response evaluation, goal orientation (instrumental vs prosocial) — literature estimates — [PMC2791956](https://pmc.ncbi.nlm.nih.gov/articles/PMC2791956)
- Evaluation-style format: after each of 3 provocation vignettes, competent, hostile and inept responses were presented one at a time; children rated their instrumental and relational consequences and how easy each would be to perform — [PMC2791956 / Fast Track-family methodology](https://pmc.ncbi.nlm.nih.gov/articles/PMC2791956); [Fast Track project](https://fasttrackproject.org/?p=470)
- Vignette assessment versus interactive VR assessment of SIP has been compared directly. The format of presentation matters for what is measured — [Interactive VR versus vignette-based assessment, BSL record](https://mijn.bsl.nl/interactive-virtual-reality-versus-vignette-based-assessment-of-/19756078); [Springer s10802-021-00879-w](https://link.springer.com/doi/10.1007/s10802-021-00879-w)

### Inferences — original rubric framework grounded in SIP theory **[design proposal, unvalidated]**
Not copied from any instrument. Category labels follow generic SIP literature vocabulary only.

Each vignette (short illustrated scene, narrated) probes up to two SIP steps through taps:
1. **Cue/intent step (optional, step 2):** "Why did Ali bump the tower?" with options *by accident / on purpose / don't know*. In ambiguous-provocation scenes, scored as benign / hostile / uncertain attribution. Record it as a descriptive signal, not a skill penalty.
2. **Response step (step 4/5 as choice):** 4 picture options, always one of each **function** below, in shuffled order:
   - **Assertive-prosocial** (states own need/feeling, negotiates, shares, takes turns)
   - **Help-seeking** (goes to a teacher/parent/elder; culturally competent in Pakistan, see Q6, so not scored lower by default)
   - **Withdraw/avoid** (walks away, stays quiet)
   - **Retaliate/assert by force** (grabs, shouts, hits back)
3. **Scoring.** Not right/wrong. Each choice adds to a **response-profile vector** (proportions across the four functions) plus a derived **flexibility** index (does the child pick context-appropriate functions across different scene types, e.g. help-seeking in safety scenes and negotiation in sharing scenes?). A single 0–100 summary, if one is needed for the plan engine, would be "proportion of context-appropriate choices", where appropriateness per scene is set in advance by a **local reviewer panel** (Pakistani teachers/psychologists). It is never inferred from Western norms.
4. **No fail states.** Every choice gets a neutral, effort-based follow-up (e.g. the story shows what happens next, gently). No red X, no "wrong".
5. **Number of vignettes.** Published SIP work used 8 vignettes in 2 contexts (literature estimate, [PMC2791956](https://pmc.ncbi.nlm.nih.gov/articles/PMC2791956)). Proposal: 6–8 per assessment window across 3–4 context types (provocation, group entry, sharing/turn-taking, needing help), spread over sessions.
6. **Agent-sourced versions** (post-week-1 live dialogue, per §12 of PROJECT.md) must carry `source=agent` and stay provisional, as already decided.

### Gaps
- No published reliability data was found for **multiple-choice, picture-based** SIP vignettes in 5–7-year-olds specifically. The κ = .91 figure is for coding open responses.
- No SIP vignette study in Pakistani/Urdu samples was found in this pass.

---

## Q4. Developmental expectations, floor/ceiling across 5–12 (bands 5–7, 8–10, 11–12)

### Takeaway
For basic-emotion forced choice, **happy, sad and angry approach ceiling by age 5–6**. Fear and surprise improve steeply through middle childhood, and disgust stays hard to label even at 11. A single fixed 6-emotion task would therefore be near floor on fear/surprise/disgust at 5 and near ceiling on happy/sad/angry by 8. Use difficulty by band (intensity morphs, more categories) to avoid ceiling at 11–12. Turn-taking latency gets faster with age in both autistic and non-autistic children.

### Cited Findings
- In French-Canadian children aged 5–11 (n = 137, free labelling), overall accuracy rose from **50.98% at 5 to 75.83% at 11**. Fear and surprise rose from roughly **20–30% at 5 to 60–70% by 11**. Happy/angry/sad were "quite accurate" at 5 with little further improvement. Disgust stayed very difficult with no meaningful improvement. 88.52% of children followed the Widen & Russell differentiation sequence — literature estimates — [Maassarani et al. 2014, PMC4044975](https://pmc.ncbi.nlm.nih.gov/articles/PMC4044975)
- Labelling sequence ages (Widen & Russell): two labels ~40 months, fear or surprise added ~56 months, five labels ~62 months, disgust ~66 months — literature estimates — [Frontiers 2014 summary](https://frontiersin.org/articles/10.3389/fpsyg.2014.00555/full); [summary notes](https://how-emotions-are-made.com/notes/Widen-1)
- Pakistani early-childhood study (ages 3–6, Urdu/English interviews with emotion cue cards and storylines): children recognise emotions, and the skill is still developing and improves with age — [Pakistani early childhood emotion recognition study (search result; via webology)](https://webology.org/data-cms/articles/20220704070534pmwebology%2018%20(6)%20-%20525.pdf) (not fetched; snippet-level)
- Response latency decreases with development in both autistic and typically developing children — [Interspeech 2012 (Lunsford et al.)](https://www.isca-archive.org/interspeech_2012/lunsford12_interspeech.html) (snippet-level)

### Inferences **[design proposal]**
- **5–7:** 4 emotions (happy, sad, angry, scared), full-intensity faces. Expect high accuracy on happy/sad/angry and a floor risk on scared. SIP vignettes: 2–3 options with picture plus narration, and simple scenes (sharing, being left out).
- **8–10:** 6 basic emotions, add surprise and disgust (expect disgust to stay low, per the sources above, so do not over-weight it). Introduce emotion-in-context (face plus scene) items. Vignettes with 4 options.
- **11–12:** 6 basic plus intensity morphs (e.g. 40/70/100%) to restore range, since FELT-style intensity variation gave reliable slopes in 9–14-year-olds ([PMC5568997](https://pmc.ncbi.nlm.nih.gov/articles/PMC5568997)). Vignettes can add ambiguous-intent scenes.
- Because progress is baseline-referenced (rule #3), floor/ceiling matters mainly for **sensitivity to change**. A child at ceiling at baseline cannot show growth. That is the main argument for band-specific difficulty, not norms.

### Gaps
- No Pakistani or South Asian normative age curves for basic-emotion recognition were found.
- No developmental data were found for picture-choice SIP vignette responses by age band.

---

## Q5. ADHD and autism patterns and confounds

### Takeaway
Emotion recognition differences in autism are **real but smaller and more task-dependent than often assumed**: d = 0.80 shrinks to 0.41 after publication-bias correction. They may be largely explained by co-occurring **alexithymia** rather than autism itself. Autistic children process **cartoon faces** more typically than real faces. ADHD shows a moderate FER difference (SMD ≈ 0.63), larger for anger and fear. In conversation, autistic children actually show **faster latencies and more overlaps**, strongly dependent on context. So "slower = worse" scoring would be invalid.

### Cited Findings
- Autism FER meta-analysis: 48 papers, 980+ autistic participants; mean effect **0.80**, reducing to **0.41** after correction for publication bias. Happiness only marginally affected, fear somewhat worse — literature estimates — [Uljarevic & Hamilton 2013, JADD (BSL record)](https://mijn.bsl.nl/recognition-of-emotions-in-autism-a-formal-meta-analysis/555206); [University of Melbourne record](https://findanexpert.unimelb.edu.au/scholarlywork/1364639-recognition-of-emotions-in-autism--a-formal-meta-analysis)
- Mixed findings are attributed to participant demographics (age, IQ), task demands and the dependent variable measured. Compensatory strategies may let some autistic individuals do well on lab tasks despite atypical processing and real-life difficulty — [Harms, Martin & Wallace 2010, Neuropsychology Review](https://www.researchgate.net/profile/Gregory_Wallace/publication/46108941_Facial_emotion_recognition_in_autism_spectrum_disorders_a_review_of_behavioral_and_neuroimaging_studies/links/0fcfd513e40bc00914000000.pdf)
- Alexithymia, not autism severity, predicted precision of facial expression attribution (adults) — [Cook, Brewer, Shah & Bird 2013, Psychological Science 24(5):723–732](https://openaccess.city.ac.uk/id/eprint/4539/)
- Cartoon versus real faces: 20 autistic children matched on age and mental ability were as accurate as controls. They used a configural strategy with cartoon faces but a local (feature-based) strategy with real faces — [Rosset et al., JADD (BSL record)](https://mijn.bsl.nl/typical-emotion-processing-for-cartoon-but-not-for-real-faces-in/547186). Autistic adolescents outperformed typical peers on static cartoon stills, with no advantage for moving cartoons — [Univ. of Bath record](https://researchportal.bath.ac.uk/en/publications/emotion-recognition-in-animated-compared-to-human-stimuli-in-adol/). Affective priming appeared in autistic children only with negative cartoon faces — [IMFAR 2012 abstract](https://insar.confex.com/imfar/2012/webprogram/Paper10520.html)
- ADHD FER meta-analysis: 142 studies, 652 effect sizes, ADHD n = 8,300 vs TD n = 7,983; **SMD = 0.63 (95% CI 0.46–0.81)**, robust to covariates and study quality — literature estimate — [PubMed 38860431](https://pubmed.ncbi.nlm.nih.gov/38860431/)
- Per-emotion ADHD effects (another meta-analysis): anger d = 0.49, fear d = 0.48, sadness d = 0.24, happiness d = 0.22 — literature estimates — [Springer, European Child & Adolescent Psychiatry s00787-020-01709-y](https://link.springer.com/article/10.1007/s00787-020-01709-y)
- Turn-taking: Cox, Fusaroli et al. 2025 (Cognitive Science 49(10):e70124). 28 autistic children (mean 10.8 y, range 6–17) and 20 TD (mean 9.6 y), matched on age/IQ. Mean latency **735 ms autism vs 871 ms TD** (with parents 580 vs 655; with unfamiliar experimenter 766 vs 1007). Unfamiliar partners slowed responses by 186–353 ms. Autistic children showed more overlaps and greater context sensitivity. Test-retest within context **r ≈ 0.36–0.66**. The authors warn latency is **not a simple proxy for social competence**, since overlaps can signal shared attention — literature estimates — [PMC12517399](https://pmc.ncbi.nlm.nih.gov/articles/PMC12517399/)
- Another study reports the opposite direction on pauses (TD mean pause 0.876 s vs autism 1.115 s, 27.3% longer) alongside faster responses due to more overlapping. Conflicting directions depend on how gaps vs overlaps are aggregated — [Interspeech 2012](https://www.isca-archive.org/interspeech_2012/lunsford12_interspeech.html) (snippet-level); contrast with [PMC12517399](https://pmc.ncbi.nlm.nih.gov/articles/PMC12517399/)
- Qualitative turn-taking violations reported in autism: not taking a turn unless directly asked, long-pause gaps, lack of reciprocity, rigid turn length, few initiations — [IMFAR 2008 abstract](https://imfar.confex.com/imfar/2008/webprogram/Paper2997.html) (snippet-level)

### Inferences
- **IQ/verbal confound.** Label-based response options need receptive vocabulary for emotion words. Pair every label with a spoken word and a picture icon, and record (not score) language/reading level from onboarding as a covariate.
- **Cartoon stimuli** reduce one autism-specific confound (local vs configural processing of real faces), which supports illustrated faces. They may also *mask* real-world difficulty (the compensation point in Harms et al.). So high accuracy on cartoon faces should not be read as real-world emotion reading, and the evidence text should say so.
- **ADHD confound.** FER errors in ADHD may partly reflect inattention or impulsive responding. Keep RT and anticipatory taps (<~200 ms **[design proposal]**) as quality flags, and consider excluding anticipatory responses from accuracy.
- **Social desirability / knowledge versus doing.** A child, especially an older or anxious one, can pick the "nice" option without being able to enact it. SIP's evaluation-vs-enactment distinction (steps 5 vs 6) predicts this gap. See Q8 below.
- **Anxiety** and unfamiliar partners slow responses ([PMC12517399](https://pmc.ncbi.nlm.nih.gov/articles/PMC12517399/)). An animated character is an unfamiliar partner, so first-session latencies will be inflated and partly measure comfort. Treat early sessions as acclimatisation and compare within-context only.

### Gaps
- No pass-located study on alexithymia and FER specifically in **children** 5–12 (Cook et al. was adults).
- No data was found on anxiety effects on vignette choices in children in this pass.

---

## Q6. Pakistan/Urdu localisation

### Takeaway
Use own-group (South Asian) faces, since an in-group advantage of about 9% is documented. Ground "competent" social responses in local norms, which a Pakistani reviewer panel should define. The literature reviewed did not supply Pakistan-specific display-rule data. Urdu emotion measures exist (e.g. an Urdu Children's Emotion Management Scales validation), showing local psychometric infrastructure but not a ready stimulus bank.

### Cited Findings
- In-group advantage of 9.3% in emotion recognition, smaller with more intergroup exposure — [Elfenbein & Ambady 2002 via SWOV](https://swov.nl/en/publicatie/universality-and-cultural-specificity-emotion-recognition-meta-analysis)
- Cross-cultural accuracy is lower in balanced designs. Universal above-chance recognition holds, but specificity exists — [in-mind.org summary](https://in-mind.org/node/306); [PMC2877627](https://pmc.ncbi.nlm.nih.gov/articles/PMC2877627)
- Urdu Children Emotion Management Scales: cross-language validation with 169 schoolchildren, internal consistency/split-half with 683, test-retest with 168; inhibition, dysregulated expression and emotional coping factors retained — [PMC11008575](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11008575/)
- Pakistani early-childhood emotion recognition was studied bilingually (Urdu/English) using emotion cue cards with storylines (ages 3–6) — [webology](https://webology.org/data-cms/articles/20220704070534pmwebology%2018%20(6)%20-%20525.pdf) (snippet-level)

### Inferences **[design proposals]**
- **Faces.** Commission South Asian child characters with a range of skin tones, hair (including hijab/dupatta and topi variants) and settings. Validate each expression with Pakistani adult raters (target agreement is a local decision; CAFE's 66–81% adult agreement ([Frontiers 2020](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.554821/full)) gives a reference point).
- **Display rules.** Expect possible dampening of negative-emotion expression toward elders, and different anger/embarrassment norms. These are hypotheses to check with local reviewers, not sourced facts (see Gaps).
- **Situations.** Siblings and cousins sharing (joint-family homes), a classroom with a teacher/"Miss", madrassa or tuition, Eid (Eidi money, new clothes), cricket in the street/gali, a guest arriving, a younger sibling breaking something, being teased about Urdu/English ability.
- **Competent responses.** **Help-seeking from an elder/teacher and deference** are normative and should be scored as competent in many scenes, not as "dependent" (Western SIP coding sometimes treats authority-seeking as less competent; [PMC2791956](https://pmc.ncbi.nlm.nih.gov/articles/PMC2791956) separates authority–punish and authority–intervene). A local panel should rate each option's appropriateness per scene before launch.
- **Language.** Emotion words in Urdu (khush, udaas, ghussa, dar/dara hua, hairaan, ghin/kiraahat) should be checked for child familiarity, especially the words for disgust and surprise, by local reviewers. Use voiced labels so reading level does not matter.

### Gaps
- **No Pakistan-specific peer-reviewed evidence on emotional display rules or on what Pakistani teachers/parents rate as competent social responses in children** was located in this pass. This is the biggest localisation gap. It needs Phase 0 interviews or a targeted literature search (e.g. South Asian collectivism and child social competence).
- No validated Urdu emotion vocabulary norms for children were found.

---

## Q7. chat_with_a_character: what is scorable without ASR versus needing NLP

### Takeaway
Without ASR, voice activity detection (VAD) on the recorded audio can give **response latency** (character finishes → child starts), **overlap/interruption** (child speech during the character's turn), **turn presence/absence**, and **turn duration**. "Staying on topic", reciprocity and content need ASR plus NLP or human coding. The timing measures are only moderately stable (r ≈ .36–.66) and highly context-dependent, and their direction differs from naive expectations in autism. They should be logged as descriptive signals with low confidence, not converted into a social_communication skill score in week 1.

### Cited Findings
- Latency/overlap measured as signed gaps (negative = overlap) from speech-segment boundaries, inter-rater κ = 0.88 with manual plus automated speech detection. Within-context test-retest 0.36–0.66. Strong partner and activity effects. Latency is not a simple competence proxy — [Cox, Fusaroli et al. 2025, PMC12517399](https://pmc.ncbi.nlm.nih.gov/articles/PMC12517399/)
- Response latency in autistic children with heterogeneous spoken-language abilities has been studied computationally — [ISI publication record](https://www.isi.edu/results/publications/20496/conversational-latency-in-autistic-children-with-heterogeneous-spoken-language-abilities/); [JSLHR 2025](https://pubs.asha.org/doi/abs/10.1044/2025_JSLHR-24-00053) (records only, not fetched)

### Inferences — scorable features and mapping **[design proposals]**
| Feature | Needs | Notes |
|---|---|---|
| Turn taken (yes/no) within window | VAD only | Window e.g. 5 s; no-response is a comfort signal (rule #5), not an error |
| Response latency (ms) | VAD + known character-turn end timestamp | Device-side; signed (negative = overlap) per Cox et al. |
| Overlap/interruption count | VAD during character playback | Echo-cancellation needed; character audio leaks into mic on tablets |
| Child turn duration | VAD | Proxy for verbosity only |
| On-topic, relevant content, reciprocity (asking back) | ASR + NLP (or human coding) | Phase 3 per D4; agent-judged parts must be `source=agent`, provisional |
| Pragmatic appropriateness | ASR + LLM / human | Least validated; keep out of scores until checked against SLP ratings |

- **Mapping to 0–100 + confidence.** Do **not** map latency to a "better/worse" scale, because both slow (shy/anxious) and fast-overlapping (autistic pattern, or enthusiasm) are ambiguous. If anything, use within-child change in turn-taking *consistency* versus baseline in the same context, with confidence capped low (e.g. ≤0.3 **[proposal]**) until validated. On-device VAD can avoid uploading raw audio for timing features, which helps rule #6 and offline tolerance.
- Audio storage requires consent (rule #6). Timing features from on-device VAD could be computed without storing audio, which is preferable.

### Gaps
- No validated child-with-animated-agent turn-taking norms were found. All latency data were from human-human conversation.
- VAD accuracy on tablet microphones with Urdu/English child speech in noisy Pakistani homes is unknown.

---

## Q8. Does a multiple-choice social vignette measure social communication or social knowledge? Naming, plus per-task verdicts

### Takeaway
A multiple-choice vignette measures **social knowledge / social problem-solving reasoning** (SIP steps 2–5: interpretation, goal and response *evaluation/selection*). It does not measure **social communication** (the enacted, real-time step 6). The honest name is something like `social_problem_solving` or `social_reasoning`. The existing `social_communication` dimension should be reserved for enacted conversational behaviour (chat_with_a_character, later with ASR), or split into two dimensions.

### Cited Findings
- SIP separates response generation/evaluation (steps 4–5) from enactment (step 6) — [PMC8361679](https://pmc.ncbi.nlm.nih.gov/articles/PMC8361679)
- Multiple-choice/evaluation formats present competent, hostile and inept options for the child to rate, which is the evaluation step — [PMC2791956](https://pmc.ncbi.nlm.nih.gov/articles/PMC2791956)
- Vignette and interactive (VR) SIP assessments have been explicitly compared as different assessment modes — [BSL record](https://mijn.bsl.nl/interactive-virtual-reality-versus-vignette-based-assessment-of-/19756078)
- Lab tasks can be passed through compensatory strategies despite real-life difficulty (the knowing-vs-doing gap in autism) — [Harms et al. 2010](https://www.researchgate.net/profile/Gregory_Wallace/publication/46108941_Facial_emotion_recognition_in_autism_spectrum_disorders_a_review_of_behavioral_and_neuroimaging_studies/links/0fcfd513e40bc00914000000.pdf)
- Conversational timing is context-dependent and not a direct competence proxy — [PMC12517399](https://pmc.ncbi.nlm.nih.gov/articles/PMC12517399/)

### Inferences — verdicts **[recommendations]**
- **how_does_she_feel → KEEP (with redesign of stimuli).** Valid, non-proprietary paradigm (forced-choice basic-emotion labelling). Fix: South Asian illustrated faces, categories by band, spoken plus icon response options, aggregate scoring, and confidence that grows over sessions because ~12–18 items per session is far below literature item counts. Optionally add an emotion-in-context variant (face plus scene) from age 8. Maps to `emotion_recognition`, with evidence text noting it measures recognition of posed/illustrated faces, not real-world reading.
- **what_would_you_do → KEEP but RENAME/RESCOPE.** Score it as `social_problem_solving` (or "social reasoning") using the original SIP-grounded response-profile rubric (Q3), with appropriateness defined by a local panel. Never show any choice as wrong. Do not let it feed `social_communication` alone. The plan engine's `social_need` rule (currently on `social_communication` or `emotion_recognition`) should be revisited if the dimension is renamed.
- **chat_with_a_character → DEFER scoring (keep as a practice/engagement activity in week 1 if desired).** Without ASR, only VAD timing is available. Its reliability is moderate, it is strongly context-dependent (unfamiliar animated partner), and its direction is ambiguous in autism, so it is unsuitable as a baseline skill score. Log timing as descriptive, low-confidence evidence. Score `social_communication` only after the Phase 3 speech pipeline, with human (SLP/teacher) validation per PROJECT.md §12. This is consistent with D4 (it keeps its original audio/Phase 3 scope).
- **Merge?** Do not merge what_would_you_do and how_does_she_feel. They target different constructs, and the emotion-in-context items can bridge them without merging dimensions.

### Gaps
- No validation study was found comparing picture-choice vignette scores with observed playground/classroom behaviour in 5–12-year-olds. The knowledge-to-behaviour correlation for this format is unknown and should be checked in pilot against teacher ratings.
