# Do Rust's compile-time type checks produce equivalent assembly to C while preventing state management errors?

## Abstract

### Do Rust's compile-time type checks produce equivalent assembly to C while preventing state management errors?

Memory safety vulnerabilities—use-after-free, buffer overflows, out-of-bounds write—are at the top of known exploited vulnerabilities[1]. System programming languages like C, which allow for low-level memory control, are needed to write performance critical code.
State is the current condition of an object that determines what operations are valid. C cannot enforce valid state transitions, such as reading an open file, at compile-time. Operations need to be checked explicitly at runtime if they are in a valid state before running.
Higher-level languages like Java automate detecting potentially unsafe operations, preventing errors but degrading performance. Therefore, developers have to make a tradeoff between safety and speed.

Rust has the ability to move certain behaviors to compile-time execution or analysis. This approach claims to be able to verify state validity during compilation, which could lead to preventing errors that runtime checks would detect while achieving comparable C performance.
This work tests whether Rust's compile-time guarantees produce assembly with equivalent performance to C code that omits all safety checks.

Programs must track state explicitly or implicitly. A file handle must be opened before reading; once closed, reads must fail. Verifying these transitions—the core of a state machine—requires verification logic. This work implements three versions of a file handle state machine, isolating state management from I/O overhead:

1. **Defensive C**: Uses an enum to track state, with explicit validation checks before each operation. Safe, but includes runtime conditional branches.
2. **Minimal C**: Tracks state with an enum, but omits all validation. Fast but permits invalid operations to compile.
3. **Rust**: Encodes each state as a distinct type, making invalid transitions not compile.

The resulting assembly will be compared using total instruction count, conditional branches, and state-tracking overhead.

The deliverables are side-by-side assembly comparisons showing whether Rust eliminates defensive checks present in safe C and an analysis with the above mentioned assembly. The assembly comparison will demonstrate whether encoding state in the type system eliminates defensive branches while matching minimal C's instruction count.


## Authors
*Technical University of Applied Sciences Würzburg-Schweinfurt*
Würzburg, Germany
daniel.borgs@study.thws.de

## Introduction

Memory safety vulnerabilities remain the dominant class of security flaws in systems software. According to the 2024 CWE Top 10 Known Exploited Vulnerabilities list, memory corruption issues such as out-of-bounds writes, use-after-free, and buffer overflows occupy the highest ranks[cwe_2024](https://cwe.mitre.org/top25/archive/2024/2024_kev_list.html). Microsoft reports that approximately 70% of their security vulnerabilities are memory safety issues[microsoft_safety](https://www.microsoft.com/en-us/msrc/blog/2019/07/we-need-a-safer-systems-programming-language/). The U.S. Cybersecurity and Infrastructure Security Agency (CISA) has issued guidance urging software manufacturers to adopt memory-safe languages[cisa_memory](https://www.cisa.gov/news-events/news/urgent-need-memory-safety-software-products).

The Heartbleed vulnerability (CVE-2014-0160) exemplifies the consequences of memory unsafety. A missing bounds check in OpenSSL's heartbeat extension allowed attackers to read up to 64KB of server memory per request, potentially exposing private keys and user credentials[wheeler_heartbleed](https://web.archive.org/web/20170202064748/https://www.dwheeler.com/essays/heartbleed.html). The fix was straightforward—adding a bounds check—but the damage from this single missing validation affected millions of systems[heartbleed_conv](https://web.archive.org/web/20140417090409/http://theconversation.com/how-the-heartbleed-bug-reveals-a-flaw-in-online-security-25536).

Systems programming languages like C provide the low-level control necessary for performance-critical code: operating systems, embedded systems, and cryptographic libraries. However, C places the entire burden of correctness on the programmer. State management—ensuring operations occur only when preconditions are met—must be enforced through explicit runtime checks or external documentation.

This creates a fundamental tension. Defensive programming adds conditional branches that verify state before each operation, incurring runtime overhead. Omitting these checks improves performance but permits undefined behavior when invariants are violated. Higher-level languages like Java enforce safety through garbage collection and runtime checks, but their overhead makes them unsuitable for systems programming.

Rust proposes a different approach: encoding invariants in the type system so that invalid programs fail to compile. The language's ownership system prevents use-after-free and data races at compile time[rust_embedded](https://doc.rust-lang.org/beta/embedded-book/static-guarantees/zero-cost-abstractions.html). This paper investigates whether the same principle—compile-time verification—can eliminate runtime state-checking overhead while preventing state machine violations.

## Background

### Memory Safety and State Management

Google's research defines memory safety bugs as arising ``when a program allows statements to execute that read or write memory, when the program is in a state where the memory access constitutes undefined behavior''[google_paper](https://storage.googleapis.com/gweb-research2023-media/pubtools/7665.pdf). When such statements are reachable under adversarial control, they often represent exploitable vulnerabilities.

State management is closely related. A file handle, for instance, must transition through defined states: closed → open → readable → closed. Reading from a closed handle or closing an already-closed handle represents invalid state transitions that may cause undefined behavior or resource leaks.

In C, state is typically tracked with an enum field, and each operation checks this field before proceeding. This approach is safe but introduces conditional branches that consume CPU cycles and may cause branch mispredictions. Furthermore, the compiler cannot verify that programmers consistently perform these checks.

### The Typestate Pattern

The typestate pattern encodes an object's state in its type, making state transitions explicit in the type system[rust_embedded](https://doc.rust-lang.org/beta/embedded-book/static-guarantees/zero-cost-abstractions.html). Rather than a single `FileHandle` type with a state field, each state becomes a distinct type: `FileHandle<Closed>`, `FileHandle<Open>`, `FileHandle<Readable>`.

Operations consume the input type and produce the output type. The `open` method takes `FileHandle<Closed>` by value (consuming it) and returns `FileHandle<Open>`. Attempting to call `read` on a `FileHandle<Closed>` produces a compile-time error—the method simply does not exist for that type.

This approach offers two potential advantages. First, invalid state transitions become compile errors rather than runtime failures. Second, since the compiler statically verifies state validity, runtime checks become unnecessary—suggesting that typestate-encoded programs could match the performance of unchecked C.

### Zero-Cost Abstractions

Rust's design philosophy emphasizes zero-cost abstractions: high-level constructs that compile to code as efficient as hand-written low-level equivalents[rust_embedded](https://doc.rust-lang.org/beta/embedded-book/static-guarantees/zero-cost-abstractions.html). The type parameters used in typestate patterns are erased during compilation. A `PhantomData<State>` field occupies zero bytes; it exists only to satisfy the type checker.

If this principle holds for typestate, Rust's approach would achieve what defensive C cannot: safety without runtime overhead.

## Implementation

To isolate state management from I/O overhead, we implement a minimal file handle abstraction in three variants. The handle stores only an integer `data` field, and operations simulate state transitions without actual file system calls.

### Defensive C Implementation

The defensive implementation tracks state explicitly with an enum and validates preconditions before each operation:

```c
typedef enum {
	STATE_CLOSED, STATE_OPEN, STATE_READABLE
 state_t;

typedef struct {
	state_t state;
	int data;
file_handle_t;

int read_file(file_handle_t* h) {
	if (h->state != STATE_OPEN) {
		return -1;  // Invalid state

	h->state = STATE_READABLE;
	h->data = 42;
	return h->data;
}
```

Each operation contains a conditional branch checking the current state. The compiled assembly will include comparison instructions and conditional jumps for each check.

### Minimal C Implementation

The minimal implementation omits all state tracking:

```c
typedef struct {
	int data;
file_handle_t;

int read_file(file_handle_t* h) {
	h->data = 42;
	return h->data;
}
```

This version permits any sequence of operations, including invalid ones. It represents the performance ceiling—the minimum possible overhead—but provides no safety guarantees.

## Rust Typestate Implementation

The Rust implementation encodes each state as a zero-sized type:

```rust
struct Closed;
struct Open;
struct Readable;

struct FileHandle<State> {
	data: i32,
	_state: PhantomData<State>,

impl FileHandle<Open> {
	fn read(self) -> FileHandle<Readable> {
		FileHandle {
			data: 42,
			_state: PhantomData,
		}
	}
}
```

The `PhantomData<State>` field is a zero-sized type marker that exists only for the type checker. The `read` method is only defined for `FileHandle<Open>`; calling it on other states produces a compile error. Crucially, consuming `self` by value prevents reuse of the old handle after transition.

## Analysis

### Compile-Time Guarantees

The Rust implementation rejects invalid state sequences at compile time. Attempting to compile:

```rust
let f = FileHandle::<Closed>::new();
let f = f.read();	// Error: no method `read`
					// for FileHandle<Closed>
```

produces an error because `read` is not implemented for `FileHandle<Closed>`. The defensive C version compiles equivalent code without complaint, deferring the error to runtime.

### Expected Assembly Characteristics

Based on Rust's zero-cost abstraction principle, we expect the following characteristics in optimized assembly:

The defensive C implementation should contain comparison instructions (`cmp`) and conditional jumps (`je`, `jne`) for each state check. It should also include instructions to load and store the state field.

The minimal C implementation should contain only the essential operations: memory allocation, data assignment, and deallocation. No comparisons or conditional branches for state validation.

The Rust implementation, if zero-cost abstractions hold, should produce assembly equivalent to minimal C. The `PhantomData` fields should be completely erased, and no state-checking code should appear since validity is guaranteed at compile time.

### Implications for Security

Google's Android team reported that as the proportion of new memory-unsafe code decreased, memory safety vulnerabilities dropped from 76% in 2019 to 35% in 2022[google_android](https://security.googleblog.com/2022/12/memory-safe-languages-in-android-13.html). While this correlation does not prove causation, it suggests that language choice significantly impacts vulnerability rates.

The typestate pattern extends this principle beyond memory safety to protocol correctness. APIs that enforce valid state sequences through types prevent an entire class of logic errors—not through runtime checks that might be forgotten, but through compile-time guarantees that cannot be circumvented.

## Conclusion

This work presents three implementations of a file handle state machine to investigate whether Rust's compile-time type checking can eliminate runtime state-validation overhead. The defensive C approach provides safety through explicit runtime checks at the cost of conditional branches. Minimal C omits these checks for maximum performance but permits invalid operations. Rust's typestate pattern encodes state in the type system, rejecting invalid sequences at compile time.

If Rust's zero-cost abstraction principle holds—and preliminary analysis suggests it should—the typestate implementation will produce assembly equivalent to minimal C while providing guarantees stronger than defensive C. This would demonstrate that the traditional safety-performance tradeoff is not fundamental: with sufficiently expressive type systems, safety can be a compile-time property with no runtime cost.

Future work will provide detailed assembly comparisons across multiple optimization levels and compiler versions, quantifying instruction counts and branch frequencies to validate these expectations empirically.
