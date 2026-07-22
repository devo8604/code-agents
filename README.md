# Engineering Agent Toolkit

A reusable Codex engineering team for complex software projects. The toolkit
packages specialist custom-agent templates, coordinated delivery workflows, and
fail-closed documentation verification in the `engineering-team` plugin.

The toolkit is project-neutral. Install the plugin and reusable agents once for
your user account, then bootstrap only repository context and necessary agent
overrides. Project architecture, commands, credentials, internal documentation,
and organization policy remain in the target project.

## What is included

### Specialist agents

| Agent | Responsibility |
| --- | --- |
| `system_architect` | System boundaries, contracts, tradeoffs, and staged architecture decisions |
| `api_engineer` | Python API contracts, service behavior, authorization, and tests |
| `client_engineer` | Public Python module or SDK ergonomics, compatibility, packaging, and tests |
| `mcp_engineer` | MCP tools, schemas, transports, error mapping, and protocol tests |
| `data_engineer` | Database design, migrations, backfills, data workflows, lineage, and quality |
| `govcloud_engineer` | AWS GovCloud partition, service availability, IAM, networking, encryption, and infrastructure as code |
| `security_engineer` | Threat modeling, secure design, supply-chain review, standards mapping, and evidence quality |
| `docs_researcher` | Read-only research against current, target-matched primary documentation |
| `technical_writer` | User README content, developer documentation, examples, docstrings, and durable comments |
| `quality_engineer` | Independent correctness, compatibility, operability, and test review |

### Workflows

| Skill | Use it for |
| --- | --- |
| `$install-global-agents` | Install, update, inspect, or remove reusable agents for the current user |
| `$bootstrap-project-context` | Onboard a repository and add only necessary project-specific overrides |
| `$plan-system-change` | Plan a feature, migration, refactor, or architectural change across system boundaries |
| `$deliver-system-change` | Implement an approved plan with explicit ownership and staged integration |
| `$diagnose-system-failure` | Prove the root cause of a cross-boundary failure |
| `$review-system-change` | Independently review a branch, pull request, migration, or working-tree change |
| `$verify-current-documentation` | Verify version-, Region-, partition-, or date-sensitive external claims |

## Requirements

- A current Codex CLI or ChatGPT desktop app with plugin support.
- A local checkout of this repository, or a Git repository URL that Codex can
  use as a marketplace source.
- Permission to create project-scoped `.codex/` files in repositories you
  choose to bootstrap.
- Permission to update user-level Codex configuration when installing global
  agents.

The complete custom-agent workflow is intended for Codex in the ChatGPT desktop
app or Codex CLI. Start a new chat or CLI session after installing or updating
the plugin so Codex loads the new skills.

## Install from a local checkout

Register the repository root as a local marketplace. Adjust the variable if the
checkout is elsewhere:

```bash
ENGINEERING_TOOLKIT_ROOT="$HOME/dev/agents"
codex plugin marketplace add "$ENGINEERING_TOOLKIT_ROOT"
```

Install the plugin from the marketplace:

```bash
codex plugin add engineering-team@engineering-team-toolkit
```

Confirm that Codex can see the marketplace and plugin:

```bash
codex plugin marketplace list
codex plugin list
```

In the ChatGPT desktop app, you can instead open **Plugins**, select the
**Engineering Team Toolkit** marketplace, and install **Engineering Team**.
Start a new chat after installation.

## Install agents globally

After installing the plugin, start a new chat and use:

```text
Use $install-global-agents to install the Engineering Team agents in my
user-level Codex configuration. Run a dry run first, preserve unrelated config,
and verify the installation afterward.
```

For a direct command from a local checkout, set the toolkit location and run
the manager. Adjust the first line if the checkout is elsewhere:

```bash
ENGINEERING_TOOLKIT_ROOT="$HOME/dev/agents"
python3 "$ENGINEERING_TOOLKIT_ROOT/plugins/engineering-team/scripts/manage_global_agents.py" install --dry-run
python3 "$ENGINEERING_TOOLKIT_ROOT/plugins/engineering-team/scripts/manage_global_agents.py" install
python3 "$ENGINEERING_TOOLKIT_ROOT/plugins/engineering-team/scripts/manage_global_agents.py" status
```

The manager uses `$CODEX_HOME` when set and otherwise `$HOME/.codex`. It copies
the 10 reusable role definitions into `agents/engineering-team/` below that
directory and adds a marked registration block to `config.toml`. It preserves
unrelated settings and comments, refuses role-name collisions, backs up changed
configuration under `backups/engineering-team/`, writes atomically, and refuses
to overwrite locally modified managed files unless `--force` is explicitly
used after review. No-op updates do not rewrite unchanged files.

To remove the global roles while preserving unrelated configuration and
locally modified files:

```bash
python3 "$ENGINEERING_TOOLKIT_ROOT/plugins/engineering-team/scripts/manage_global_agents.py" uninstall --dry-run
python3 "$ENGINEERING_TOOLKIT_ROOT/plugins/engineering-team/scripts/manage_global_agents.py" uninstall
```

Start a new Codex chat or CLI session after installing, updating, or removing
global roles.

## Install from Git

After this repository is published, register it directly by replacing
`OWNER/REPOSITORY` with its Git host path:

```bash
codex plugin marketplace add OWNER/REPOSITORY --ref main
codex plugin add engineering-team@engineering-team-toolkit
```

For an HTTPS or SSH Git URL, pass that URL to `codex plugin marketplace add`
instead. Workspace policy may restrict allowed marketplace sources.

## Bootstrap a project

Open the target repository in a new Codex chat or CLI session and use:

```text
Use $bootstrap-project-context to onboard this repository. Reuse globally
installed engineering-team agents, create only necessary project-specific
overrides, preserve existing guidance, and report every file you create or
change.
```

The bootstrap workflow inspects the repository before changing it and may
create or update:

- `AGENTS.md` with verified architecture, commands, conventions, and safety
  boundaries.
- `.codex/config.toml` with project-level agent coordination settings.
- `.codex/agents/*.toml` only when a role needs a project-specific override or
  the user chooses project-scoped installation.
- `.codex/documentation-evidence.json` when the project depends on versioned or
  rapidly changing external systems.

Review and commit those project-specific files in the target repository so the
same team behavior is available to future Codex sessions and collaborators.

## Use the workflows

Codex can select an installed skill from a normal request, or you can invoke it
explicitly.

Plan a cross-system feature:

```text
Use $plan-system-change to plan asynchronous CSV imports across the API,
Python client, MCP server, PostgreSQL workflows, containers, and GovCloud.
```

Implement an approved plan:

```text
Use $deliver-system-change to implement the approved import plan. Preserve
unrelated changes, assign one writer per file, and stop before deployment.
```

Diagnose a failure without automatically changing code:

```text
Use $diagnose-system-failure to determine why MCP job status differs from the
Python client and API. Diagnose only and show the complete evidence chain.
```

Review a change:

```text
Use $review-system-change to review this branch against main, including API,
client, MCP, database, security, documentation, and GovCloud risks.
```

Verify a version-sensitive premise:

```text
Use $verify-current-documentation to verify the external APIs and AWS GovCloud
service availability this change depends on before implementation begins.
```

The delivery workflows do not implicitly authorize deployment, cloud mutation,
database migration execution, package publication, releases, or external
messages. Those actions still require explicit user authorization.

## Public contract stability

Public contracts are stable by default. This includes API operations and
request, response, and error schemas; public Python imports, signatures, types,
and exceptions; MCP tools, resources, prompts, descriptions, input and output
schemas, and errors; configuration keys, commands, events, protocols, and
externally consumed data schemas.

Agents must prefer additive, backward-compatible changes. They may not silently
rename, remove, narrow, reorder, or change the meaning of a public surface. A
breaking change must be shown to be unavoidable, explicitly approved by the
user before implementation, and accompanied by versioning, deprecation,
migration, compatibility-window, consumer-impact, and rollback plans. Contract
or snapshot tests should lock the existing surface before changes begin.

## Portable documentation paths

Agents must not copy a user-specific absolute home path from a development
machine into documentation, examples, docstrings, or comments. Use
project-relative paths whenever possible. For home-relative locations, use
`$HOME/Documents` in POSIX examples, `%USERPROFILE%` in Command Prompt examples,
or `$env:USERPROFILE` in PowerShell examples. Use placeholders such as
`<repo-root>` when environment-variable expansion is not appropriate.

Validate documentation with:

```bash
python3 plugins/engineering-team/scripts/validate_portable_documentation.py .
```

## Current-documentation enforcement

Every specialist treats model training knowledge as a discovery aid, not proof.
Material external claims must identify the project's installed or targeted
version, configuration, Region, and partition and cite target-matched primary
documentation.

The verification skill stores those claims in
`.codex/documentation-evidence.json`. Its validator rejects required evidence
that is missing, inferred, unresolved, secondary-only, expired, or mismatched.
It also requires source-authority and target-match evidence and limits validity
windows according to source volatility.

Validate a target project's ledger with:

```bash
python3 /path/to/engineering-agent-toolkit/plugins/engineering-team/scripts/validate_documentation_evidence.py \
  /path/to/target-project/.codex/documentation-evidence.json
```

## Update the plugin

Pull or fetch the updated marketplace source, reinstall the plugin, and start a
new chat or CLI session:

```bash
codex plugin add engineering-team@engineering-team-toolkit
```

During local plugin development, update the plugin version or Codex cachebuster
before reinstalling so the new bundle is not confused with an older cached
copy.

## Repository layout

```text
.
├── .agents/plugins/marketplace.json
├── AGENTS.md
├── README.md
└── plugins/engineering-team/
    ├── .codex-plugin/plugin.json
    ├── scripts/
    ├── skills/
    ├── tests/
    └── templates/
        ├── custom-agents/
        └── project/
```

## Validate the toolkit source

From the repository root:

```bash
python3 plugins/engineering-team/scripts/validate_agent_templates.py
python3 plugins/engineering-team/scripts/validate_portable_documentation.py .
python3 plugins/engineering-team/tests/run.py
python3 /path/to/skill-creator/scripts/quick_validate.py \
  plugins/engineering-team/skills/<skill-name>
python3 /path/to/plugin-creator/scripts/validate_plugin.py \
  plugins/engineering-team
```

The reusable source must not contain project credentials, internal endpoints,
proprietary schemas, or organization-specific policy. Keep those in the target
repository's project-scoped guidance and authorized documentation systems.
