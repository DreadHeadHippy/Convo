# Convo Language Definition for GitHub Linguist Submission

## Language Details

- **Name**: Convo
- **Type**: Programming Language
- **Color**: `#6366f1` (Purple-blue, representing natural conversation)
- **Extensions**: `.convo`
- **Aliases**: `convo`, `Convo Language`
- **Language ID**: TBD (assigned by GitHub)

## Sample Code

```convo
Say "Hello, World!"
Let name be "Alice"
Define greet with person:
    Say "Hello, " + person + "!"
Call greet with name
```

## Justification for Language Recognition

### 1. Complete Language Implementation
- Lexer, Parser, Interpreter architecture
- 26+ passing tests demonstrating language completeness
- Full variable, function, and control flow support

### 2. Unique Syntax Paradigm
- Natural language-like syntax distinct from existing languages
- English-readable programming constructs
- Educational focus for programming accessibility

### 3. Real-World Usage
- Active development and examples
- Discord bot framework integration
- Growing community and documentation

### 4. Technical Merit
- Turing-complete programming language
- Self-contained interpreter implementation
- Professional development practices (CI/CD, testing, documentation)

## Language Grammar (EBNF-style)

```
program = statement*
statement = say_statement | let_statement | function_def | function_call | if_statement | while_statement
say_statement = "Say" expression
let_statement = "Let" IDENTIFIER "be" expression
function_def = "Define" IDENTIFIER "with" parameter_list ":" block
function_call = "Call" IDENTIFIER "with" argument_list
if_statement = "If" expression comparison expression "then" ":" block ("Else" ":" block)?
while_statement = "While" expression comparison expression ":" block
```

## Repository Evidence
- GitHub Repository: https://github.com/DreadHeadHippy/Convo
- Example Programs: https://github.com/DreadHeadHippy/Convo/tree/main/examples
- Test Suite: https://github.com/DreadHeadHippy/Convo/tree/main/tests
- Documentation: https://github.com/DreadHeadHippy/Convo/blob/main/README.md
