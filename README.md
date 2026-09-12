# A Formal Framework for Synchronized Drone Swarms with Belief-Based Reinforcement

Maude code accompanying the paper of the same title (Labadze, Ölveczky, Dundua).
See the paper for all definitions, design rationale, and discussion of results;
this README only covers how to load and run the code.

## Structure

- `framework/` generic, parametric framework (Section 3)
- `case-study/` 3D drone instantiation (Section 4)
- `analysis/` evaluation and meta-level bounded search (Section 5)
- `tests/` the two worked examples from Section 5 (`example.maude`)
- `load_all.maude` loads all modules in dependency order

## Requirements

Maude 3.5.1 (<https://maude.lcc.uma.es>).

## Running

From the repository root:

```
maude tests/example.maude
```

or, equivalently:

```
cd tests
maude example.maude
```

Each query in `example.maude` states its expected result in a comment
immediately above it.

## License

MIT (see `LICENSE`).
