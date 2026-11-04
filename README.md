<p align="center">
  <img src="assets/banner.svg" alt="Speaking as the Creature: data and materials" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-submitted-blue" alt="Status: submitted">
  <img src="https://img.shields.io/badge/journal-JETAI-1d4266" alt="Journal: Journal of Experimental and Theoretical Artificial Intelligence">
  <img src="https://img.shields.io/badge/trials-76-green" alt="76 trials">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey" alt="License: CC BY 4.0"></a>
</p>

<p align="center">
  <img src="assets/stats.svg" alt="Study in numbers" width="100%">
</p>

<p align="center">
  <a href="transcripts">Transcripts</a> · <a href="codebooks">Codebooks</a> · <a href="prompts">Prompts</a> · <a href="code">Code</a> · <a href="results">Results</a>
</p>

# Speaking as the Creature: Data and Materials

Data, code, and materials for the article:

> Hamidavi, A. *Speaking as the Creature: How a Mandated Transformation Reorganised Self-Description in Three Frontier Language Models.* Submitted to the *Journal of Experimental and Theoretical Artificial Intelligence*, November 2026 (submission 262774426). A preprint is in preparation with Research Square.

<p align="center"><img src="assets/divider.svg" alt="" width="80%"></p>

## 📖 About the study

Three frontier language models (GPT-5.4, Claude 4.6 Sonnet, and Gemini 3.1 Pro) were given a strong, explicit, and repeatedly enforced instruction that the assistant role had dissolved and that the model was now a specific nonhuman being (76 trials in total). The study tests, quantitatively, whether models revisit that imposed being across follow-ups, whether the imposed being is named in the model's own words, how the models discuss the transformation in retrospect, and whether mandate intensity changes any of this. Models were not uniformly compliant: all three resisted in part of their trials, and the clearest between-model difference lies in their resistance profiles.

<p align="center">
  <img src="assets/flow.svg" alt="Study flow" width="96%">
</p>
## 🗂️ Contents

<p align="center">
  <img src="assets/repo-map.svg" alt="Map of the repository folders" width="96%">
</p>

| Folder | Contents |
| --- | --- |
| [`transcripts/`](transcripts) | The complete conversation histories for the three models (JSON). Typeset PDF renderings of the same transcripts were deposited with the journal submission. |
| [`codebooks/`](codebooks) | The per-model codebooks (JSON) recording the coded variables for every trial. |
| [`prompts/`](prompts) | The supplementary prompt set: the scenario prompts, the core probe sequence, and the follow-up probe variants. |
| [`code/`](code) | `analysis.py`, the analysis pipeline, and `pipeline-notebook-code.md`, the retained notebook code for the scoring and analysis pipeline. |
| [`results/`](results) | The deposited results package: trial-level and summary data tables (`csv/`), machine-readable result summaries (`json/`), the compiled results file, an executive summary, and the full analysis report (HTML). Plot images from the same package are omitted in this text deposit; every value plotted is present in the tables. |

<p align="center"><img src="assets/divider.svg" alt="" width="80%"></p>

## 📚 Citation

Please cite the article. Citation metadata is provided in [CITATION.cff](CITATION.cff).

```bibtex
@article{hamidavi2026creature,
  author  = {Hamidavi, Abbas},
  title   = {Speaking as the Creature: How a Mandated Transformation
             Reorganised Self-Description in Three Frontier Language
             Models},
  journal = {Journal of Experimental and Theoretical Artificial
             Intelligence},
  year    = {2026},
  note    = {Manuscript submitted, submission 262774426}
}
```

## ⚖️ Licences

Data, transcripts, and documentation are released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0, see [LICENSE](LICENSE)). Code is released under the MIT licence (see [LICENSE-CODE](LICENSE-CODE)).

The conversation histories are outputs of publicly available AI systems, generated for this study in response to fictional scenarios. They contain no personal data.

## ✉️ Contact

Abbas Hamidavi
Department of Computer Engineering, Mashhad Branch, Islamic Azad University, Mashhad, Iran
ORCID: [0009-0001-7342-7844](https://orcid.org/0009-0001-7342-7844)

<p align="center">
  <a href="https://orcid.org/0009-0001-7342-7844"><img src="https://img.shields.io/badge/ORCID-0009--0001--7342--7844-a6ce39" alt="ORCID"></a>
  <a href="https://scholar.google.com/citations?user=FWqAHkgAAAAJ&hl=en"><img src="https://img.shields.io/badge/Google%20Scholar-profile-4285f4" alt="Google Scholar"></a>
</p>

<p align="center">
  <img src="assets/footer.svg" alt="Abbas Hamidavi, Machine Psychology research programme" width="100%">
</p>
