# Stakeholders

| Stakeholder | Interest | Influence |
| ----------- | -------- | --------- |
| **End users (educators)** | Fast, cheap-to-install tool; readable errors | Requirements priority |
| **Content studios / creators** | Batch rendering, themes, branding | Feature requests |
| **LLM / agent integrators** | Stable, small API; few failure modes | API design |
| **Open-source contributors** | Clear architecture, good CI | Implementation velocity |
| **Downstream packagers (Linux distros)** | Reproducible builds, license clarity | Packaging constraints |
| **Nabin Oli (author)** | Vision, roadmap, releases | Final decisions |

### Success criteria (product)

1. Meaningful reduction in **time-to-first-frame** vs a typical ManimCE LaTeX+disk pipeline.
2. **Install size** an order of magnitude smaller than TeX-based stacks for core use.
3. **Teaching workflows** supported with optional **local** narration (privacy-preserving).
