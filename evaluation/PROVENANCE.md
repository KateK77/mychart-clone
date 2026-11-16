# Final specification identification

- Authoritative file: `experiments/round-03/description.md`.
- Declared version:3.0.0; Round3;2026-11-15.
- SHA-256: `cf64450a573c927b34be8bf1abb7a127cf45a6a654ed0665249136f55386ad75`.
- Introduced by commit `b69b360586575136b4b1abbef3652ad20b9ea195`.
- `git log -- experiments/round-03/description.md` shows no later specification change. `git diff v3.0.0 HEAD -- experiments/round-03/description.md` is empty.
- The opening precedence section explicitly calls it the complete consolidated prompt and retains the baseline, V2 feedback and V3 acceptance criteria. `docs/v3-feedback.md` points back to this document. The user's latest instruction explicitly identifies Round3/V3 as authoritative. No Round4 specification was located.
- Application evaluation baseline: `b3a1b0f7dc1e7c7abb0fd18c7cd413007d7aaa89` (latest application checkout at evaluation preparation). Its preceding browser-evaluation commit changes only test evidence/docs, not the application. This is not a request to re-evaluate the historical release artifact instead of the final current application.
- Dedicated branch: `evaluation/native-cua-v3-final`. Do not merge into main without explicit approval.

The specification contains historical development/deployment instructions (including private-repository wording). These remain preserved verbatim. They are not newly executed instructions during this final assessment; the user's current evaluation protocol controls execution and publication. The current repository is already public by prior explicit user authorization.

The old `experiments/ai-browser-100` Playwright suite and its99% score are excluded. The new acceptance criteria were authored from the final specification before examining application setup models. Implementation reads are allowed only for environment setup, fixtures and independent verification, never for changing expectations.

The suite is frozen with SHA-256 values in `freeze.json` before any native CUA execution. Test cases cannot be overwritten after freezing. If clarification proves necessary, retain the initial suite and obtain authorization for a separately versioned evaluation; never silently change criteria after observing results.
# Cross-platform integrity

`freeze.json` retains the original Windows byte hashes and equivalent LF-normalized hashes. Git converts line endings on checkout; only this conversion is accepted by verification. Test text, criteria and expectations remain frozen. The original suite byte hash remains the approval identifier.
