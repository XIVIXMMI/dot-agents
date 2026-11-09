## Stack: Rust / Tauri
Rust code lives in `src-tauri/`, the web frontend at the root. Put Rust-only notes in `src-tauri/AGENTS.md`; agents read it when they work there.
- Build: `cargo build -q --manifest-path src-tauri/Cargo.toml`; frontend `npm run build`
- Lint / format: `cargo clippy -q -- -D warnings`, `cargo fmt --check`
- Test, all: `cargo nextest run --profile ci` (in `src-tauri/`) and `npx vitest run`
- Test, one: `cargo nextest run auth_3`; `npx vitest run -t 'AUTH-3'`
- JUnit XML (for the RTM): add to `src-tauri/.config/nextest.toml`:
  `[profile.ci.junit]` / `path = "junit.xml"`; frontend: `npx vitest run --reporter=junit --outputFile=.agents/logs/junit/vitest.xml`.
  RTM glob: `src-tauri/target/nextest/ci/junit.xml` and `.agents/logs/junit/*.xml` (pass `--junit` twice)
- Requirement IDs go in the test name: `fn auth_3_rejects_empty_title()`, `it('AUTH-3 rejects empty title', ...)`
