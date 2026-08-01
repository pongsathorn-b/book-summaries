---
tags: algorithms, ethics, machine-learning, fairness, privacy, accountability, AI, computer-science, policy
category: Science
summary: Michael Kearns and Aaron Roth argue that algorithmic fairness requires more than just mathematical definitions — it requires a deep understanding of ethics, incentives, and the social contexts in which algorithms operate.
---

# The Ethical Algorithm: The Science and Politics of Making Algorithms Fair

**Author:** Michael Kearns & Aaron Roth (2018)  
**Category:** Science & Computer Science / Ethics & Technology

---

## Overview

Computer scientists Michael Kearns and Aaron Roth address a question that sounds simple but isn't: *how do we make sure algorithms are fair?* As algorithms increasingly decide who gets loans, jobs, parole, and medical care, the question of algorithmic fairness has moved from academic philosophy to urgent public policy. The authors — both professors at the University of Pennsylvania — argue that fairness cannot be bolted onto algorithms after the fact; it must be embedded at the design level, which requires a genuine interdisciplinary collaboration between computer scientists, statisticians, ethicists, lawyers, and social scientists. The book is notable for its clarity in explaining complex algorithmic concepts to general readers while maintaining genuine technical depth.

---

## Core Concepts

### 1. Fairness Is Not a Single Concept
Kearns and Roth's central argument is that fairness is **conceptually pluralistic** — there is no single mathematical definition that captures everything we mean by "fair." Different fairness criteria can be mutually incompatible:
- **Demographic parity** — Algorithm makes the same proportion of positive decisions across groups
- **Equalized odds** — Algorithm has equal false positive and false negative rates across groups
- **Calibration** — When the algorithm says 60% probability, the true rate is 60% regardless of group

The **Impossibility Theorem of Fair Classification** (proved by Chouldechova and Kleinberg independently) shows that no algorithm can simultaneously satisfy calibration, equal false positive rates, and equal false negative rates across groups — unless base rates are equal. Tradeoffs are inevitable.

### 2. The Long Tail Problem
Machine learning algorithms are trained on historical data — and history contains all the biases of the humans who made the decisions that generated that data. Worse: historical data often has very few examples of rare events (the "long tail"), so algorithms trained on it will be particularly bad at predicting rare events. This is compounded when rare events are also correlated with marginalized groups.

### 3. Privacy as a Public Good
Kearns and Roth introduce **differential privacy** — a mathematical framework for releasing aggregate information about a dataset while guaranteeing that no individual's data can be inferred from the release. The US Census Bureau now uses differential privacy for certain data releases. The concept is philosophically subtle: it's not that the data is encrypted or hidden; it's that the *formal guarantees* make re-identification practically impossible regardless of what auxiliary information an attacker has.

### 4. Algorithmic Accountability and the Audit Problem
How do you check whether an algorithm is fair when:
- The algorithm is proprietary (you can't see its source code)?
- Its decision logic may be too complex for any human to understand?
- Its training data is not public?

Kearns and Roth advocate for **algorithmic auditing** — running systematic empirical tests on algorithms' behavior across demographic groups, the way drug trials test for side effects across populations. This requires legal frameworks that give auditors access without revealing trade secrets.

### 5. Mechanism Design and Incentives
The book extends to **mechanism design** — the science of designing systems (auctions, matching algorithms, voting systems) that incentivize desired behavior. A badly designed matching system can inadvertently incentivize strategic behavior that harms everyone. The authors show how the same principles apply to algorithmic systems more broadly.

### 6. The Limits of Formalism
Kearns and Roth are unusually candid about what formal methods *can't* do. Mathematical fairness criteria don't resolve disputes about *what* we should want. An algorithm that achieves perfect demographic parity might still be unfair if the underlying selection process (e.g., college admissions) is itself unjust. Formal tools are necessary but insufficient — they must be embedded in broader democratic deliberation about values.

---

## Key Lessons

1. **Algorithmic fairness is technically and philosophically hard.** TheImpossibility Theorem shows that naive notions of fairness will fail; but even sophisticated notions require difficult tradeoffs.
2. **"We've always done it this way" is a terrible justification for algorithms.** Historical data encodes historical discrimination; using it to train future decisions perpetuates that discrimination.
3. **Transparency and auditability are engineering problems, not just ethics problems.** Building algorithms that can be fairly audited requires deliberate architectural choices.
4. **The definition of fairness you choose reflects your values.** There's no neutral, technical answer to which fairness criterion is correct — it's a political and moral question.
5. **Privacy is not binary.** Differential privacy shows you can have useful data analysis with formal privacy guarantees; the question is how much accuracy you're willing to trade for privacy.
6. **Feedback loops can amplify bias.** If an algorithm makes biased decisions that change the world, and that changed world generates new training data, the algorithm's biases become self-reinforcing.
7. **Complex algorithms can be fair in some sense and unfair in another.** A model that is calibrated across groups may still have discriminatory impact.
8. **Market incentives often don't align with fairness.** Companies have strong financial incentives to maximize prediction accuracy on the majority population; there's no market reward for fairness to minorities.
9. **The long tail is where fairness most matters and algorithms most fail.** When rare events (rare diseases, unusual risk profiles, exceptional individuals) are poorly represented in training data, algorithms are most confidently wrong.
10. **Interdisciplinary collaboration is non-negotiable.** Computer scientists alone cannot solve fairness; they need ethicists, sociologists, lawyers, and affected communities in the conversation.

---

## Practical Applications

- **Evaluating AI products and services** — When using or buying algorithmic systems, asking: what data was it trained on? What fairness criteria were used? Have they been audited?
- **Policy advocacy** — Understanding the technical possibilities and limits of algorithmic regulation (GDPR, AI Act, algorithmic auditing laws) enables more effective engagement.
- **Building fairer systems** — For practitioners, understanding the tradeoffs between fairness criteria and how to measure fairness empirically.
- **Career in AI ethics/AI policy** — The field is growing rapidly; this book provides a rigorous foundation.
- **Critical consumption of algorithmic news** — When media reports an algorithm is "biased," understanding what that formally means and what the tradeoffs of fixing it might be.

---

## Controversy and Criticism

- **Academic abstraction** — Critics argue the book is more concerned with formal proofs than practical implementation; real-world algorithmic auditing is messier than the book suggests.
- **Insufficient attention to power** — The book focuses on individual fairness criteria but pays less attention to systemic power imbalances that algorithms can entrench.
- **Technical accessibility varies** — Some chapters are genuinely accessible; others (particularly on mechanism design) assume significant mathematical background.
- **Limited coverage of content moderation** — Social media algorithms that amplify misinformation or harmful content are a major algorithmic ethics issue that gets relatively light treatment.
- **Individual vs. group fairness tension** — The book is better on group fairness (e.g., demographic parity) than on the individual fairness question of whether each person is treated as they deserve.

---

## Related Books

- [[Nudge]] — Thaler & Sunstein's work on choice architecture provides complementary tools for influencing behavior ethically
- [[Thinking Fast and Slow]] — Kahneman's exploration of human cognitive limitations is directly relevant to understanding why algorithmic decision-making can fail
- [[The Black Swan]] — Taleb's analysis of rare, high-impact events is relevant to the long-tail problem in machine learning
- [[Cognitive Biases]] — Understanding the systematic errors humans bring to algorithmic design and deployment
- [[The Lean Startup]] — The iterative, empirical approach to building products is analogous to the iterative auditing and refinement of algorithmic fairness
- [[Skin in the Game]] — The importance of those affected by algorithmic decisions having a voice in their design
- [[Thinking in Systems]] — Understanding algorithms as components of larger social, economic, and political systems
