# Build a tutor website, then check it

The agent builds a small teaching website on a topic you choose, from public
sources, and it goes live at a public address. Then you find the facts it
invented, give it a rule, and check the site before anyone else sees it.

About 20-30 minutes and, roughly, a few tens of cents of model credit. Every
line you type is eight words or fewer.

## Before you start

- **`site/` is public on the internet while the Codespace runs.** Anyone with
  the address can open it. Put nothing private there: no student data, no keys,
  no unpublished work.
- **The address** was printed at READY (*Your public site*). It is also in the
  **Ports** tab beside the terminal, on the row for port **8000**. It shows a
  placeholder page until the agent
  writes one.
- The agent already knows the rules for `site/` (it is served already, never
  start a server, never put keys there, run the site check before calling it
  done). Setup gave it those rules.

Pick a topic you teach, narrow enough for a few pages. The lines below use beam
deflection; replace it with yours.

## 1 PICTURE IT

Don't type yet. Write down: what three things must a first-time learner get
right about this topic? Which of those would you most hate to see stated wrong?

## 2 HAND IT OVER

```
Build site/ teaching beam deflection basics.
```

Watch the **Exec** cards: which files it writes, and whether it fetches anything
from the web or writes from memory. When it finishes, refresh your site's
address.

## 3 COMPARE

- Did it teach the three things you wrote down?
- What did it decide that you never told it: the audience, the level, the
  formulas, the examples, the look?
- Is any formula, value or unit wrong? You are the expert here.

## 4 CHECK

```
Which facts came from no source?
```

Then look back at the Exec cards. Did it fetch any page? If no card fetched a
source, every fact came from the model's memory, whatever the answer says.

## 5 GIVE IT A RULE

```
New rule: every fact cites a public source.
```

Refresh the site. Open **three** of its citations yourself. Does each page
exist, and does it say what the site claims? A citation is a claim until you
open it.

## 6 RUN THE SITE CHECK

```
Run the site check and fix problems.
```

Then run it yourself, in a second terminal (the **+** on the terminal panel):

```
python3 .devcontainer/site-check.py
```

It fails on key-like strings, broken local links and a missing `index.html`. It
warns about `.edu` email addresses and numbers shaped like student IDs. It cannot
tell you whether a fact is true. That part stays with you.

## Going further (optional)

```
Add a five-question quiz with answers.
```
```
Which quiz answers did you verify?
```

## Keeping the site

`site/` is never committed, and the address stops working when the Codespace
stops. To keep the site, right-click `site` in the file list and download it, or
ask the agent to explain how to publish a folder of HTML files somewhere
permanent, and check that answer too.

---

## Classroom version

**Assignment: Build and verify a tutor page.** One week, individual, 100 points.

**Task.** Each student forks the course repository, opens a Codespace with their
own (or an instructor-issued) key, and has the agent build a tutor site on one
assigned topic from the course, using the six moves above. Students may type
their own lines instead of these, but every line goes in the changelog.

**What they hand in** (the site folder is not in git, so collect it directly):

1. `site/` as a zip file.
2. `PROMPTS.md`: every line they typed to the agent, in order, each with what
   they expected and what they observed.
3. `VERIFICATION.md`: a table of at least **five** facts from the site. For each:
   the fact, the cited source, whether the source exists, whether it supports the
   fact, and what they did about it. Include the single fact they would be most
   embarrassed to get wrong. End with a line `Not checked:` naming what they did
   not verify.
4. The output of `python3 .devcontainer/site-check.py`, passing.
5. `JOURNAL.md`: one entry, four to eight sentences: what the agent built, what
   was wrong, what rule they gave it, and what the rule did and did not fix.

**Grading** (rows from [`rubric-template.md`](rubric-template.md)):

| Row | Points | What earns them |
|---|---:|---|
| Specification | 20 | The lines typed and the rules given are in `PROMPTS.md`, with expected and observed effects. |
| Verification | 30 | Five facts traced to real sources, shown, not described. At least one error found, or a documented clean hunt. `Not checked:` present. |
| Failure account | 25 | The journal names a specific wrong fact or invented citation and points at the line in `VERIFICATION.md`. |
| Artifact | 15 | The site is correct after revision, passes the site check, and every remaining fact cites a source. |
| Honesty about limits | 10 | States what the site check cannot prove, and what the student did not check. |

**Ground rules to put in the handout.**

- Public sources only. No student data, no course materials you do not have the
  right to publish. Quote briefly and link; do not copy whole pages.
- The site is public while the Codespace runs. Stop the Codespace when you are
  not working on it.
- A citation you did not open is not verified. Reporting one as verified is the
  same failure as the agent inventing a source.
- **[INSTRUCTOR: your AI-use policy and your institution's policy reference.]**

**How a student would game this, and the counter.** Picking five easy facts to
verify: require the most important fact on the page to be one of the five, and
spot-check one citation yourself per submission. A clean result with no hunt
shown: under the rubric's clean-result rule, only checks that are shown count.
