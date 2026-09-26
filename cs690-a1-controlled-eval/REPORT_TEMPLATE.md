# CS 690 Assignment 1 Report: Replicating a Controlled Evaluation

**Name:** Ketan Verma
**Repository:** https://github.com/kverma19863020/CS690-Assign1KV
**Results commit (short SHA):** 66d422e

## Part 1. Verification evidence

Command:

```text
python -m harness.verify
```

```text
OK: loaded 20 frozen tasks
OK: dataset sha256 5d84176547cb679f4145676d1f4dfd5061bf3b9600904911da8e5700e82eee3b
OK: generated Python executed in Docker sandbox
OK: candidate network probe was blocked
OK: model/configuration metadata written to results/verification.json
```

## Part 2. Tests and code questions

```text
20 passed in 1.64s
```

(Run as `python -m pytest -q` inside the virtual environment.)

### Q1. The path of one attempt

For task A1-001 in `tasks/cs690_eval20.json`, `load_tasks` (`harness/tasks.py`) checks the file's SHA-256 and returns a `Task`. `run` (`harness/runner.py`) fills `PROMPT_TEMPLATE` and saves it with `_save_prompt`. `_generate_with_retry` calls `OpenAIProvider.generate` (`harness/provider.py`). `extract_python` (`harness/grader.py`) pulls out the code, and `_save_candidate` stores it. `grade_candidate` calls `run_source` (`harness/sandbox.py`), which starts a container where `docker_entry.py` runs the code and asserts under a 5-second limit and returns a JSON verdict. `_append_jsonl` writes the row to `raw_results.jsonl`. The sandbox matters because the code is unreviewed model output: the container has no network, a read-only disk, no capabilities, resource limits, and a non-root user.

### Q2. What is sent and what comes back

Each request sends `model`, the model to use; `input`, the fixed prompt; `temperature` 1.0, the randomness of token choice; `reasoning.effort` "none", which means no hidden reasoning step; `max_output_tokens` 800, the answer length cap; and `store` false. `top_p` and `seed` are null, so they are not sent. The harness keeps `text`, `returned_model`, the input/output/total token counts, and `stop_reason`. A model name is an alias the provider can point to a new snapshot, so `returned_model` and `run_date_utc` are recorded too. In my run, the returned names matched the requested ones, so the run date is what identifies the model.

### Q3. Same prompt, different answers

Temperature 1.0 samples from the full token distribution and no seed is sent, so every attempt is an independent random draw. In my run, A failed A1-012 twice and then passed it. This is intended, because pass@k estimates a probability over draws. For someone else to check the run, the harness records `conditions.json`, `manifest.json` (`dataset_sha256`, `config_sha256`), the prompts in `prompts/`, the replies in `candidates/`, and in each `raw_results.jsonl` row the requested and returned model, the sampling settings, `run_date_utc`, `prompt_sha256`, `sandbox_image`, `stop_reason`, the token counts, and `passed`. The fixed `bootstrap_seed` (690) makes the interval repeatable.

### Q4. pass@k by hand

pass@k = 1 − C(n − c, k) / C(n, k), with n = 3 and c = 1:

- pass@1 = 1 − C(2,1)/C(3,1) = 1 − 2/3 = **0.3333**
- pass@2 = 1 − C(2,2)/C(3,2) = 1 − 1/3 = **0.6667**

`pass_at_k(3, 1, 1)` = 0.33333333333333337 and `pass_at_k(3, 1, 2)` = 0.6666666666666667, which match.

Shortcut: 1 − (1 − 1/3)² = **0.5556**. It is lower because it assumes draws with replacement, as if the same wrong attempt could be picked twice. pass@2 picks 2 distinct attempts out of 3, and only 1 of the 3 possible pairs is all wrong.

### Q5. Why whole problems are redrawn

`bootstrap_task_ci` (`harness/metrics.py`) converts each task to one pass@k score. With seed 690, it draws 20 task scores with replacement, records their mean, and repeats this 5,000 times. It returns the 2.5th and 97.5th percentiles. It redraws whole problems because attempts on the same problem are correlated, and the question it answers is "what if different problems had been chosen?" Drawing single attempts would make the interval too narrow. `test_task_bootstrap_resamples_tasks_not_candidate_rows` (`tests/test_metrics.py`) uses one always-pass and one always-fail task. Task-level draws produce suites scoring 0 and 1, so the interval must be exactly [0, 1]. An attempt-level bootstrap would give a narrower interval and fail the test.

## Part 3. Replication

The evidence is the committed `results/experiment/` and `prompts/` folders.

## Part 4. Results

| Condition | Requested model | Returned model version | Attempts per task | Total attempts | pass@1 | 95 percent CI for pass@1 | pass@2 | Input tokens | Output tokens | Dollars spent |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
| A | gpt-5.6-luna | gpt-5.6-luna | 3 | 60 | 0.95 | [0.8667, 1.0000] | 0.9833 | 7146 | 3756 | $0.03 |
| B | gpt-5.6-terra | gpt-5.6-terra | 3 | 60 | 1.00 | [1.0000, 1.0000] | 1.0000 | 7146 | 4162 | included in A |

### Memo

**Ranking.** By pass@1, B (gpt-5.6-terra, 1.00, 60/60 passed) ranked above A (gpt-5.6-luna, 0.95, 57/60). pass@2 had the same order: 1.00 versus 0.983.

**Uncertainty.** The gap comes from two tasks: A1-010 (A passed 2/3) and A1-012 (A passed 1/3). A's interval, [0.867, 1.000], includes B's score. B's interval, [1.000, 1.000], has no width because B solved every task every time. That reflects a ceiling, not precision. The evidence does not support a ranking.

**External validity.** CS690-Eval20 has 20 short standalone functions checked by fixed asserts, and both models scored near 100 percent, so it cannot separate them. It does not test multi-file changes, existing codebases, unclear requirements, or third-party libraries.

**Variance.** Sampling at temperature 1.0 with no seed makes every attempt a random draw. On A1-012, A failed twice and then passed. A rerun or a classmate's run would draw different attempts, and with 60 attempts per condition, one changed attempt moves pass@1 by about 1.7 points. The model behind a name can also change between run dates.

## Part 5. Reading a published score

Benchmark chosen: **HumanEval**

### 1. What does it measure?

Given a Python function signature and docstring, write a function body that passes hidden unit tests. There are 164 hand-written problems with about 7.7 tests each, scored by pass@k (Chen et al., 2021).

### 2. What does it not measure that a software project may depend on?

Each problem is one self-contained function. HumanEval does not test working in an existing codebase, multi-file design, debugging, third-party libraries, unclear requirements, performance, security, or maintainability. Passing a handful of asserts does not mean the code is correct in general.

### 3. How can a reported score rise without the underlying model becoming better?

Changing the setup changes the number. Codex solved 28.8% of problems with one sample and 70.2% with 100 samples per problem (Chen et al., 2021), so k, temperature, and prompt format all matter. Weak tests also let wrong code pass: EvalPlus added about 80 times more tests and lowered pass@k by up to 19.3–28.9% across 26 models, which also changed some rankings (Liu et al., 2023). Training on the benchmark itself raises the score too.

### 4. Could the model have seen the answers already?

This is likely for many models. HumanEval has been public since 2021. Riddell et al. (2024) found substantial overlap between the benchmark and open pretraining corpora, and they found that models scored higher on problems whose solutions they had seen. A later analysis reports that 12.2% of HumanEval samples appear in The Pile and 18.9% in The Stack, and that every prompt appears at least 43 times on public GitHub (Matton et al., 2024). The training data for the models in my run is not disclosed, so contamination can be neither confirmed nor ruled out. The benchmark is also near-saturated: one tracker reports several models at 95% or above as of April 2026 (DemandSphere, accessed September 26, 2026).

A published HumanEval score is not interchangeable with my CS690-Eval20 result. It uses different problems and tests, a different sampling setup, and a public dataset with documented contamination. Mine comes from 20 frozen course problems, three samples each at temperature 1.0, on my run date.

## References

- Chen, M., et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv:2107.03374. https://arxiv.org/abs/2107.03374
- Liu, J., Xia, C. S., Wang, Y., & Zhang, L. (2023). *Is Your Code Generated by ChatGPT Really Correct?* NeurIPS 2023. https://arxiv.org/abs/2305.01210
- Riddell, M., Ni, A., & Cohan, A. (2024). *Quantifying Contamination in Evaluating Code Generation Capabilities of Language Models*. ACL 2024. https://aclanthology.org/2024.acl-long.761/
- Matton, A., et al. (2024). *On Leakage of Code Generation Evaluation Datasets*. Findings of EMNLP 2024. https://aclanthology.org/2024.findings-emnlp.772.pdf
- DemandSphere. *HumanEval – AI Frontier Model Tracker* (as of April 2026; accessed September 26, 2026). https://www.demandsphere.com/research/demandsphere-radar/ai-frontier-model-tracker/benchmarks/human-eval/
